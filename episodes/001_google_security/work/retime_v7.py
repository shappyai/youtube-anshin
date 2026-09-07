# -*- coding: utf-8 -*-
"""v7: 1:55付近の過剰説明（「再設定」の意味解説）を削除してタイムラインを再構築。

- ユニット18の文言を「次は、再設定用の電話番号とメールアドレスを確認します。」へ差し替え
- ユニット19（「再設定」は「もう一度設定し直す」という意味です。）を削除
- 間（0.20/0.60）・atempo1.06・CTA・末尾無音10.3秒 を再適用
- 出力: audio/unit_018.mp3（差し替えTTS）/ audio/narration_v5.mp3
       work/timeline_v7.json / episodes/captions_v7.srt
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[3]
EP = ROOT / "episodes" / "001_google_security"
WORK = EP / "work"
load_dotenv(ROOT / ".env")

MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
VOICE = os.getenv("OPENAI_TTS_VOICE", "coral")
KEY = os.getenv("OPENAI_API_KEY")
INSTRUCTION = (
    "落ち着いた自然な口調で、少しゆっくりめに読んでください。"
    "文の終わりで短く間を置き、丁寧に分かりやすく話してください。"
)
GAP_SENT, GAP_SECTION, ATEMPO = 0.20, 0.60, 1.06
CTA = "役に立ったら、チャンネル登録して、次回も一緒に確認しましょう。"
END_SILENCE = 10.3


def dur_of(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    if not KEY:
        raise SystemExit("OPENAI_API_KEY がありません")
    old = json.loads((WORK / "timeline.json").read_text(encoding="utf-8"))
    old_units = old["units"]
    new_text_18 = "次は、再設定用の電話番号とメールアドレスを確認します。"

    # ユニット18 を差し替えTTSで再生成（19は削除対象のため再生成しない）
    p18 = EP / "audio" / "unit_018.mp3"
    resp = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        json={"model": MODEL, "voice": VOICE, "instructions": INSTRUCTION,
              "input": new_text_18},
        timeout=180)
    if resp.status_code != 200:
        raise SystemExit(f"TTS failed for unit18: {resp.status_code}")
    p18.write_bytes(resp.content)
    print("unit_018.mp3 regenerated")

    # ユニット列（19削除・18文言差し替え）
    units = []
    for i, u in enumerate(old_units, 1):
        if i == 19:
            continue  # 過剰説明を削除
        text = new_text_18 if i == 18 else u["text"]
        units.append({"index": i, "text": text, "section": u["section"]})

    # 尺取得（19以外の既存mp3を利用）
    items = []
    for u in units:
        p = EP / "audio" / f"unit_{u['index']:03d}.mp3"
        items.append({**u, "file": p, "dur": dur_of(p)})

    # タイムライン（間・セクション境界）
    cursor = 0.0
    for i, it in enumerate(items):
        it["start"] = cursor
        it["end"] = cursor + it["dur"]
        cursor = it["end"]
        if i + 1 < len(items) and items[i + 1]["section"] != it["section"]:
            cursor += GAP_SECTION
        else:
            cursor += GAP_SENT
    total_units = cursor

    cta = EP / "audio" / "cta.mp3"
    cta_dur = dur_of(cta)
    cta_start = total_units + 0.8
    cta_end = cta_start + cta_dur
    total_audio = cta_end + END_SILENCE

    # captions_v7.srt（ユニット単位 + CTA）
    def ts(sec: float) -> str:
        ms = int(round((sec - int(sec)) * 1000))
        s = int(sec) % 60
        m = int(sec) // 60 % 60
        h = int(sec) // 3600
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    lines = []
    for i, it in enumerate(items, 1):
        end = it["end"] + 0.22
        lines += [str(i), f"{ts(it['start'])} --> {ts(end)}", it["text"], ""]
    lines += [str(len(items) + 1), f"{ts(cta_start)} --> {ts(cta_end + 0.15)}", CTA, ""]
    (EP / "captions_v7.srt").write_text("\n".join(lines), encoding="utf-8")

    # 音声連結（units + 間 + CTA + 末尾無音）→ narration_v5.mp3
    def make_silence(sec, path):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
                        "-i", "anullsrc=r=24000:cl=mono", "-t", f"{sec:.2f}",
                        "-c:a", "libmp3lame", "-b:a", "128k", "-ar", "24000",
                        "-ac", "1", str(path)], check=True)

    sil_s = WORK / "v7_sil_s.mp3"
    sil_x = WORK / "v7_sil_x.mp3"
    sil_e = WORK / "v7_sil_e.mp3"
    make_silence(GAP_SENT, sil_s)
    make_silence(GAP_SECTION, sil_x)
    make_silence(END_SILENCE, sil_e)
    lst = []
    for i, it in enumerate(items):
        lst.append(it["file"])
        if i + 1 < len(items):
            lst.append(sil_x if items[i + 1]["section"] != it["section"] else sil_s)
    lst.append(EP / "audio" / "cta.mp3")
    lst.append(sil_s)  # CTA直後の短い間
    lst.append(sil_e)
    concat = WORK / "v7_concat_audio.txt"
    concat.write_text("\n".join(f"file '{p.as_posix()}'" for p in lst), encoding="utf-8")
    out = EP / "audio" / "narration_v5.mp3"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(concat), "-af", f"atempo={ATEMPO}",
                    "-c:a", "libmp3lame", "-b:a", "128k", "-ar", "24000", "-ac", "1",
                    str(out)], check=True)

    # スケール後のタイムライン/メタを保存（ビルダーと字幕はフランス時間で利用）
    for it in items:
        it["start"] /= ATEMPO
        it["end"] /= ATEMPO
    sec_bounds = []
    for it in items:
        if not sec_bounds or sec_bounds[-1]["name"] != it["section"]:
            sec_bounds.append({"name": it["section"], "start": it["start"]})
    meta = {
        "total_units": total_units / ATEMPO,
        "cta_start": cta_start / ATEMPO,
        "cta_end": cta_end / ATEMPO,
        "end_audio_total": dur_of(out),
        "sections": sec_bounds,
    }
    (WORK / "timeline_v7.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2),
                                           encoding="utf-8")
    print(f"narration_v5.mp3 total: {dur_of(out):.2f}s (atempo {ATEMPO})")


if __name__ == "__main__":
    main()
