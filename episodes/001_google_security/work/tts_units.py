# -*- coding: utf-8 -*-
"""第2稿用: 文章単位TTS・実測タイミング・間の挿入・字幕生成（一回限りのビルド補助）。

- script.md を文単位に分割
- 各文を OpenAI TTS（gpt-4o-mini-tts / coral / ゆっくり指示）で生成し
- 各ユニットの実時間を ffprobe で取得
- ユニット間の間（0.45s）とセクション境界の追加間（+0.8s）をタイムラインへ反映
- captions.srt（正確な同期）と audio/narration_v2.mp3（無音ギャップ入り）を生成

APIキーは .env から読み込み、表示・保存しない。
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[3]
EP = ROOT / "episodes" / "001_google_security"
load_dotenv(ROOT / ".env")

MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
VOICE = os.getenv("OPENAI_TTS_VOICE", "coral")
KEY = os.getenv("OPENAI_API_KEY")
INSTRUCTION = (
    "落ち着いた自然な口調で、少しゆっくりめに読んでください。"
    "文の終わりで短く間を置き、丁寧に分かりやすく話してください。"
)

GAP_SENT = 0.20      # 文と文の間（秒）
GAP_SECTION = 0.60   # セクション境界の間（秒）
ATEMPO = 1.06        # 全体の微速調整（間と発話のバランス調整用）


def parse_script() -> list[dict]:
    """script.md を読み、セクション付きの文ユニット一覧を返す。"""
    text = (EP / "script.md").read_text(encoding="utf-8")
    units: list[dict] = []
    section = "はじめに"
    buf: list[str] = []

    def flush():
        nonlocal buf
        joined = "".join(buf)
        buf = []
        for p in re.split(r"(?<=[。！？])", joined):
            if p.strip():
                units.append({"text": p.strip(), "section": section})

    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("## "):  # セクション見出し（読み上げない）
            flush()
            section = re.sub(r"^##\s+[\d:]+\s*", "", line).strip()
            continue
        if line.startswith("#"):
            continue  # 制作メモ（読み上げない）
        line = re.sub(r"\[SHOT-\d+\]", "", line)
        line = line.replace("**", "").strip()
        if not line:
            continue
        buf.append(line)
    flush()
    return units


def tts_unit(text: str, i: int, out: Path, retries: int = 2) -> bool:
    resp = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        json={"model": MODEL, "voice": VOICE, "instructions": INSTRUCTION, "input": text},
        timeout=180,
    )
    if resp.status_code != 200:
        return False
    out.write_bytes(resp.content)
    return True


def dur_of(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        raise SystemExit(f"duration parse failed: {path}")


def main():
    if not KEY:
        raise SystemExit("OPENAI_API_KEY がありません（.env を確認）")
    units = parse_script()
    print(f"units: {len(units)} (model={MODEL} voice={VOICE})")
    audio_dir = EP / "audio"
    work = EP / "work"
    parts = []
    for i, u in enumerate(units, 1):
        p = audio_dir / f"unit_{i:03d}.mp3"
        if not p.exists():
            ok = tts_unit(u["text"], i, p)
            if not ok:
                print(f"unit {i} failed, retry...")
                time.sleep(2)
                ok = tts_unit(u["text"], i, p)
            if not ok:
                raise SystemExit(f"TTS failed at unit {i}")
            print(f"unit {i:03d} done: {u['section']}")
        parts.append({"file": p, "dur": dur_of(p), "text": u["text"], "section": u["section"]})
    # タイムライン（間を挟む）
    cursor = 0.0
    timeline = []
    for i, pt in enumerate(parts):
        start = cursor
        end = start + pt["dur"]
        pt["start"], pt["end"] = start, end
        timeline.append(pt)
        gap = GAP_SECTION if (i + 1 < len(parts) and parts[i + 1]["section"] != pt["section"]) else GAP_SENT
        cursor = end + gap
    total = cursor
    print(f"narration total (incl. gaps): {total:.2f}s")
    # 無音ギャップと連結（mp3 128k 24k mono に再エンコード）
    def make_silence(sec: float, path: Path):
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
             "-i", f"anullsrc=r=24000:cl=mono", "-t", f"{sec:.2f}",
             "-c:a", "libmp3lame", "-b:a", "128k", "-ar", "24000", "-ac", "1", str(path)],
            check=True)
    sil_s, sil_x = work / "silence_s.mp3", work / "silence_x.mp3"
    make_silence(GAP_SENT, sil_s)
    make_silence(GAP_SECTION, sil_x)
    concat_items = []
    for i, pt in enumerate(parts):
        concat_items.append(pt["file"])
        if i + 1 < len(parts):
            gap = GAP_SECTION if parts[i + 1]["section"] != pt["section"] else GAP_SENT
            concat_items.append(sil_x if gap >= GAP_SECTION else sil_s)
    lst = work / "narration_concat.txt"
    lst.write_text("\n".join(f"file '{p.as_posix()}'" for p in concat_items), encoding="utf-8")
    out = EP / "audio" / "narration_v2.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-af", f"atempo={ATEMPO}",
         "-c:a", "libmp3lame", "-b:a", "128k", "-ar", "24000", "-ac", "1", str(out)],
        check=True)
    actual = dur_of(out)
    print(f"narration_v2.mp3: {actual:.2f}s")
    # atempo に合わせてタイムラインをスケールし、字幕を作り直す
    for pt in timeline:
        pt["start"] /= ATEMPO
        pt["end"] /= ATEMPO
    def ts(sec: float) -> str:
        ms = int(round((sec - int(sec)) * 1000))
        s = int(sec) % 60
        m = int(sec) // 60 % 60
        h = int(sec) // 3600
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    lines = []
    for i, pt in enumerate(timeline, 1):
        end = min(pt["end"] + 0.22, timeline[-1]["end"])
        lines += [str(i), f"{ts(pt['start'])} --> {ts(end)}", pt["text"], ""]
    (EP / "captions.srt").write_text("\n".join(lines), encoding="utf-8")
    print(f"captions.srt: {len(timeline)} cues / last end {ts(timeline[-1]['end'])}")
    # セクション境界（歌詞カード開始時間）を保存
    sections: list[dict] = []
    for pt in timeline:
        if not sections or sections[-1]["name"] != pt["section"]:
            sections.append({"name": pt["section"], "start": pt["start"]})
    (work / "timeline.json").write_text(json.dumps(
        {"total": actual, "sections": sections,
         "units": [{k: p[k] for k in ("text", "section", "start", "end", "dur")} for p in timeline]},
        ensure_ascii=False, indent=2), encoding="utf-8")
    print("timeline.json saved")


if __name__ == "__main__":
    main()
