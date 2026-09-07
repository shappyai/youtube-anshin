# -*- coding: utf-8 -*-
"""第3稿: エンディングCTA文のTTSと narration_v3・字幕80コマ目 の追加。"""

from __future__ import annotations

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
CTA = "役に立ったら、チャンネル登録して、次回も一緒に確認しましょう。"
GAP_BEFORE_CTA = 0.8


def dur_of(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    if not KEY:
        raise SystemExit("OPENAI_API_KEY がありません")
    cta = EP / "audio" / "cta.mp3"
    if not cta.exists():
        resp = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
            json={"model": MODEL, "voice": VOICE, "instructions": INSTRUCTION, "input": CTA},
            timeout=180)
        if resp.status_code != 200:
            raise SystemExit(f"CTA TTS failed: {resp.status_code}")
        cta.write_bytes(resp.content)
        print("cta.mp3 generated")
    cta_dur = dur_of(cta)
    print(f"cta dur: {cta_dur:.2f}s")

    v2 = EP / "audio" / "narration_v2.mp3"
    total_v2 = dur_of(v2)
    sil = WORK / "silence_080.mp3"
    if not sil.exists():
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
             "-i", "anullsrc=r=24000:cl=mono", "-t", f"{GAP_BEFORE_CTA:.2f}",
             "-c:a", "libmp3lame", "-b:a", "128k", "-ar", "24000", "-ac", "1", str(sil)],
            check=True)
    lst = WORK / "narration_v3_list.txt"
    lst.write_text(
        f"file '{v2.as_posix()}'\nfile '{sil.as_posix()}'\nfile '{cta.as_posix()}'\n",
        encoding="utf-8")
    out = EP / "audio" / "narration_v3.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c:a", "libmp3lame", "-b:a", "128k", "-ar", "24000", "-ac", "1", str(out)],
        check=True)
    total = dur_of(out)
    print(f"narration_v3.mp3: {total:.2f}s")

    # 字幕にCTAコマを追加
    srt = EP / "captions.srt"
    lines = srt.read_text(encoding="utf-8").splitlines()
    cues = [i for i, l in enumerate(lines) if l.strip().isdigit()]
    n = len(cues) + 1
    start = total_v2 + GAP_BEFORE_CTA
    end = start + cta_dur + 0.15

    def ts(sec: float) -> str:
        ms = int(round((sec - int(sec)) * 1000))
        s = int(sec) % 60
        m = int(sec) // 60 % 60
        h = int(sec) // 3600
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    add = ["", str(n), f"{ts(start)} --> {ts(end)}", CTA, ""]
    srt.write_text("\n".join(lines + add) + "\n", encoding="utf-8")
    print(f"captions.srt: {n} cues")
    # ビルド用メタ（outro 秒数）
    (WORK / "outro_meta.json").write_text(
        __import__("json").dumps(
            {"cta_dur": cta_dur, "gap": GAP_BEFORE_CTA, "start": start, "end": end,
             "video_after_v2": GAP_BEFORE_CTA + cta_dur + 0.7},
            ensure_ascii=False, indent=2), encoding="utf-8")
    print("outro_meta.json saved")


if __name__ == "__main__":
    main()
