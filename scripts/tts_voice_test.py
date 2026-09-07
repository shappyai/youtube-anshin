"""Voice comparison test: same script text, multiple gpt-4o-mini-tts voices.

Generates raw TTS MP3s only. No speed/pitch/EQ/volume processing.
Never prints or saves the API key.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

EP_AUDIO = ROOT / "episodes" / "001_google_security" / "audio"
OUT_DIR = EP_AUDIO / "voice_test"
SCRIPT_TXT = OUT_DIR / "voice_test_script.txt"
SCRIPT_MD = ROOT / "episodes" / "001_google_security" / "script.md"
CAPTIONS_SRT = ROOT / "episodes" / "001_google_security" / "captions_v8.srt"

MODEL = "gpt-4o-mini-tts"
VOICES = ["coral", "cedar", "marin", "sage"]

INSTRUCTIONS = (
    "50代から70代の視聴者に、スマートフォン教室の講師が隣で丁寧に説明するように話してください。"
    "落ち着いて親しみやすく、安心感のある話し方にしてください。"
    "ニュース読みやアナウンサー調にはせず、会話として自然にしてください。"
    "急がず、一度聞いただけで内容を理解できる速度にしてください。"
    "重要な言葉には自然な範囲で軽く強調を入れてください。"
    "文章ごとに同じ抑揚・同じ語尾にならないようにしてください。"
    "過度に明るくしたり、子ども向けのような話し方にはしないでください。"
    "ただし、極端に遅くならず、普段の動画と同じくらいの速度を保ってください。"
)


def normalize(s: str) -> str:
    """Keep only CJK/digits/letters so line breaks and tags don't break matching."""
    return re.sub(r"\s+", "", s)


def normalize_script() -> str:
    """Mirror strip_markdown_for_speech: drop headings and [SHOT-xx] tags."""
    lines = []
    for line in SCRIPT_MD.read_text(encoding="utf-8").splitlines():
        if re.match(r"^#", line.strip()):
            continue
        line = re.sub(r"\[SHOT-[0-9]+\]", "", line)
        if line.strip():
            lines.append(line.strip())
    return normalize("\n".join(lines))


def normalize_captions() -> str:
    """Keep only the spoken caption lines, dropping indexes and timestamps."""
    lines = []
    for line in CAPTIONS_SRT.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.isdigit() or "-->" in s:
            continue
        lines.append(s)
    return normalize("\n".join(lines))


def check_passage_used(text: str) -> None:
    """Fail loudly if the passage is not verbatim in script.md and in the v8 captions."""
    body = normalize(text)
    for src, label in ((normalize_script(), "script.md"), (normalize_captions(), "captions_v8.srt")):
        if body not in src:
            raise SystemExit(f"passage not found verbatim in {label}; aborting")


def main() -> int:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("OPENAI_API_KEY is not set.", file=sys.stderr)
        return 1

    text = SCRIPT_TXT.read_text(encoding="utf-8").strip()
    if not text:
        print(f"{SCRIPT_TXT} is empty", file=sys.stderr)
        return 1
    check_passage_used(text)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"model={MODEL} voices={','.join(VOICES)} chars={len(text)}")
    failed: list[str] = []
    for voice in VOICES:
        out = OUT_DIR / f"voice_test_{voice}.mp3"
        if out.exists():
            print(f"{voice}: skip (file already exists: {out.name})")
            continue
        resp = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": MODEL,
                "voice": voice,
                "input": text,
                "instructions": INSTRUCTIONS,
            },
            timeout=180,
        )
        if not resp.ok:
            failed.append(voice)
            print(f"{voice}: FAILED ({resp.status_code}) {resp.text[:300]}")
            continue
        out.write_bytes(resp.content)
        print(f"{voice}: OK -> {out.relative_to(ROOT)} ({len(resp.content)} bytes)")

    if failed:
        print(f"failed voices: {', '.join(failed)}", file=sys.stderr)
        return 1
    print("all requested voices generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
