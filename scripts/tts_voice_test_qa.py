"""QA for voice-test MP3s: duration, sample rate, bitrate, silence, loudness facts.

Analysis only: decodes to a temp WAV/PCM pipeline; never modifies the MP3s.
"""
from __future__ import annotations

import json
import math
import re
import struct
import subprocess
import tempfile
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "episodes" / "001_google_security" / "audio" / "voice_test"
VOICES = ["coral", "cedar", "marin", "sage"]

FFMPEG_CANDIDATES = [
    ROOT / "local" / "ffmpeg" / "bin" / "ffmpeg.exe",
    Path(r"C:\Codex\260525_Shadowing\functions\node_modules\ffmpeg-static\ffmpeg.exe"),
]
FFMPEG = next((p for p in FFMPEG_CANDIDATES if p.exists()), None)
if FFMPEG is None:
    raise SystemExit("ffmpeg not found")

ANALYSIS_SR = 24000


def probe(mp3: Path) -> dict:
    r = subprocess.run(
        [str(FFMPEG), "-hide_banner", "-i", str(mp3)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    info = r.stderr
    dur = None
    m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", info)
    if m:
        dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    rate = None
    bitrate = None
    m = re.search(r"Audio:\s*(\S+),\s*(\d+(?:\.\d+)?)\s*Hz,\s*(\S+),\s*(\S+),\s*(\d+)\s*kb/s", info)
    if m:
        rate = float(m.group(2))
        bitrate = int(m.group(5))
    return {"duration_ffmpeg": dur, "sample_rate": rate, "bitrate_kbps": bitrate}


def decode_pcm(mp3: Path) -> tuple[list[int], int]:
    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "decoded.wav"
        subprocess.run(
            [
                str(FFMPEG), "-hide_banner", "-y",
                "-i", str(mp3),
                "-ac", "1", "-ar", str(ANALYSIS_SR),
                "-f", "wav", str(wav),
            ],
            check=True,
            capture_output=True,
        )
        with wave.open(str(wav), "rb") as w:
            assert w.getframerate() == ANALYSIS_SR and w.getnchannels() == 1
            raw = w.readframes(w.getnframes())
            return list(struct.unpack(f"<{w.getnframes()}h", raw)), w.getnframes()


def rms_db(samples: list[int]) -> float:
    if not samples:
        return -float("inf")
    mean = sum(s * s for s in samples) / len(samples)
    return 20 * math.log10(math.sqrt(mean) + 1e-12)


def longest_silence(samples: list[int], frames: int, threshold: int = 250) -> float:
    """Longest gap of consecutive frames (100 ms windows, 25 ms hop) below amplitude."""
    win = ANALYSIS_SR // 10  # 100 ms
    hop = ANALYSIS_SR // 40  # 25 ms
    active = False  # silence run currently open
    start = 0
    longest = 0.0
    i = 0
    while i + win <= frames:
        seg = samples[i : i + win]
        peak = max(abs(s) for s in seg)
        if peak < threshold:
            if not active:
                active = True
                start = i
        else:
            if active:
                longest = max(longest, (i - start) / ANALYSIS_SR)
                active = False
        i += hop
    if active:
        longest = max(longest, (frames - start) / ANALYSIS_SR)
    return longest


def main() -> int:
    results = {}
    for voice in VOICES:
        mp3 = OUT_DIR / f"voice_test_{voice}.mp3"
        if not mp3.exists():
            results[voice] = {"status": "MISSING"}
            continue
        info = probe(mp3)
        samples, frames = decode_pcm(mp3)
        results[voice] = {
            "status": "ok",
            "bytes": mp3.stat().st_size,
            "duration_s": round(frames / ANALYSIS_SR, 3),
            **info,
            "rms_db": round(rms_db(samples), 1),
            "longest_silence_s": round(longest_silence(samples, frames), 2),
        }
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
