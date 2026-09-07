"""Blind comparison copies: loudness-only normalization (linear gain) + A-D shuffle.

Originals in audio/voice_test/ are never modified. Outputs go to
audio/voice_test/blind/ as voice_A.mp3 .. voice_D.mp3 with no voice identity
in filename or MP3 tags. The mapping is written only to blind_key.txt.
"""
from __future__ import annotations

import json
import random
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "episodes" / "001_google_security" / "audio" / "voice_test"
OUT_DIR = SRC_DIR / "blind"
KEY_FILE = OUT_DIR / "blind_key.txt"
VOICES = ["coral", "cedar", "marin", "sage"]
LETTERS = ["A", "B", "C", "D"]

FFMPEG_CANDIDATES = [
    ROOT / "local" / "ffmpeg" / "bin" / "ffmpeg.exe",
    Path(r"C:\Codex\260525_Shadowing\functions\node_modules\ffmpeg-static\ffmpeg.exe"),
]
FFMPEG = next((p for p in FFMPEG_CANDIDATES if p.exists()), None)
if FFMPEG is None:
    raise SystemExit("ffmpeg not found")

TARGET_LUFS = -16.0
MAX_TP = -1.5


def measure(path: Path) -> dict:
    r = subprocess.run(
        [str(FFMPEG), "-hide_banner", "-i", str(path), "-map", "0:a:0",
         "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    err = r.stderr
    # Progress lines (CR-separated) report "I: ..." from the start of the file;
    # the final "Summary" block at the very end holds the integrated value.
    i_all = re.findall(r"I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", err)
    i = float(i_all[-1]) if i_all else None
    # ebur128 summary prints "True peak:" then "Peak: X dBFS" (some builds use
    # "True peak: X dBTP"); per-frame running max is "TPK: X dBFS".
    tp_m = re.search(r"True peak:\s*\n\s*Peak:\s*(-?\d+(?:\.\d+)?)\s*dBFS", err)
    if not tp_m:
        tp_m = re.search(r"True peak:\s*(-?\d+(?:\.\d+)?)\s*dBTP", err)
    if not tp_m:
        tpks = re.findall(r"TPK:\s*(-?\d+(?:\.\d+)?)\s*dB", err)
        tp = max(float(x) for x in tpks) if tpks else None
    else:
        tp = float(tp_m.group(1))
    d = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", err)
    sr = re.search(r"Audio:\s*\S+,\s*(\d+)\s*Hz,\s*(\S+),\s*(\S+),\s*(\d+)\s*kb/s", err)
    dur = None
    if d:
        dur = int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3))
    return {
        "lufs": i,
        "tp_dbtp": tp,
        "duration_s": dur,
        "sample_rate": int(sr.group(1)) if sr else None,
    }


def loudnorm_measure(src: Path) -> dict:
    """Pass 1: measure with loudnorm's own meter and get the target offset."""
    r = subprocess.run(
        [str(FFMPEG), "-hide_banner", "-i", str(src),
         "-af", f"loudnorm=I={TARGET_LUFS}:TP={MAX_TP}:LRA=11:print_format=json",
         "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    blocks = re.findall(r"\{[^{}]*\}", r.stderr)
    if not blocks:
        raise SystemExit(f"loudnorm measurement failed for {src.name}")
    obj = json.loads(blocks[-1])
    return {
        "input_i": obj["input_i"],
        "input_tp": obj["input_tp"],
        "input_lra": obj["input_lra"],
        "input_thresh": obj["input_thresh"],
        "target_offset": obj["target_offset"],
    }


def render(src: Path, dst: Path, measured: dict) -> None:
    subprocess.run(
        [str(FFMPEG), "-hide_banner", "-y",
         "-i", str(src),
         "-map_metadata", "-1",
         "-af", (
             f"loudnorm=I={TARGET_LUFS}:TP={MAX_TP}:LRA=11:"
             f"measured_I={measured['input_i']}:"
             f"measured_TP={measured['input_tp']}:"
             f"measured_LRA={measured['input_lra']}:"
             f"measured_thresh={measured['input_thresh']}:"
             f"offset={measured['target_offset']}"
         ),
         "-ar", "24000", "-ac", "1",
         "-codec:a", "libmp3lame", "-b:a", "128k",
         "-write_id3v1", "0", "-write_id3v2", "0",
         str(dst)],
        check=True, capture_output=True,
    )


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    order = LETTERS.copy()
    random.SystemRandom().shuffle(order)
    mapping = dict(zip(order, VOICES))

    results = {}
    src_meta = {}
    for letter in LETTERS:
        voice = mapping[letter]
        src = SRC_DIR / f"voice_test_{voice}.mp3"
        if not src.exists():
            raise SystemExit(f"missing source: {src}")
        m = loudnorm_measure(src)
        src_meta[voice] = m
        dst = OUT_DIR / f"voice_{letter}.mp3"
        if dst.exists():
            dst.unlink()
        render(src, dst, m)
        q = measure(dst)
        src_m = measure(src)
        results[letter] = {
            "path": str(dst),
            "lufs": q["lufs"],
            "tp_dbtp": q["tp_dbtp"],
            "duration_s": q["duration_s"],
            "sample_rate": q["sample_rate"],
            "src_duration_s": src_m["duration_s"],
            "src_lufs": src_m["lufs"],
            "src_tp_dbtp": src_m["tp_dbtp"],
            "offset_dB": float(src_meta[voice]["target_offset"]),
        }

    KEY_FILE.write_text(
        "\n".join(f"{letter}: {mapping[letter]}" for letter in LETTERS) + "\n",
        encoding="utf-8",
    )

    report = {
        "method": "ffmpeg loudnorm two-pass (I=-16 LUFS, TP=-1.5 dBTP, LRA=11)",
        "target": {"I": TARGET_LUFS, "TP": MAX_TP},
        "files": results,
        "unify": {
            "max_lufs_spread": round(
                max(r["lufs"] for r in results.values())
                - min(r["lufs"] for r in results.values()), 2),
            "duration_match": all(
                abs(r["duration_s"] - r["src_duration_s"]) < 0.15  # mp3 encoder padding
                for r in results.values()),
            "sample_rate": sorted({r["sample_rate"] for r in results.values()}),
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
