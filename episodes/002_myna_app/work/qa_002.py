# -*- coding: utf-8 -*-
"""Mechanical QA for draft_v1.mp4 (episode 002)."""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[3]
EP = ROOT / "episodes" / "002_myna_app"
ASSETS = EP / "assets" / "official"
DRAFT = EP / "output" / "draft_v1.mp4"
NARRATION = EP / "audio" / "voicevox_kenzaki" / "narration_kenzaki.wav"
ASS = EP / "captions_v1.ass"
MANIFEST = EP / "audio" / "voicevox_kenzaki" / "segments_manifest.csv"

sys.path.insert(0, str(EP / "work"))
import build_video_002 as B  # noqa: E402

FFPROBE = "ffprobe"
FFMPEG = "ffmpeg"
issues: list[str] = []


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(out.stdout)["format"]["duration"])


def fmt(sec: float) -> str:
    m, s = divmod(int(round(sec)), 60)
    return f"{m}:{s:02d}"


def main() -> int:
    print("== 1. durations ==")
    v = probe_duration(DRAFT)
    a = probe_duration(NARRATION)
    print(f"video: {v:.3f}s ({fmt(v)})  narration: {a:.3f}s ({fmt(a)})  diff={abs(v-a):.3f}s")
    if abs(v - a) > 0.5:
        issues.append(f"video/audio duration mismatch: {v:.3f} vs {a:.3f}")

    print("== 2. black frames (YAVG<20) ==")
    out = subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(DRAFT),
         "-vf", "signalstats,metadata=print:file=-", "-an", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    black = 0
    mins = []
    for line in out.stdout.splitlines():
        m = re.search(r"lavfi\.signalstats\.YAVG=([\d.]+)", line)
        if m:
            y = float(m.group(1))
            mins.append(y)
            if y < 20:
                black += 1
    print(f"frames={len(mins)} black(frames YAVG<20)={black} minYAVG={min(mins) if mins else '-'}")
    if black:
        issues.append(f"{black} near-black frames")

    print("== 3. silence (audio, <-50dB, >=1.0s) ==")
    out = subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(DRAFT), "-af",
         "silencedetect=noise=-50dB:d=1.0", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    silences = re.findall(r"silence_(start|end): ([0-9.]+)", out.stderr)
    print(f"silence events: {len(silences)//2}")
    if silences:
        for i in range(0, len(silences), 2):
            print("  ", silences[i], silences[i + 1] if i + 1 < len(silences) else "")

    print("== 4. captions (ASS) ==")
    lines = ASS.read_text(encoding="utf-8").splitlines()
    cues = [l for l in lines if l.startswith("Dialogue:")]
    max_w = 0
    for c in cues:
        body = c.split(",", 9)[-1]
        text = re.sub(r"\{\\[^}]*\}", "", body)
        for ln in text.split("\\N"):
            w = sum(72 if ord(ch) > 0x2E7F or ch in "（）「」・!?―" else 36 for ch in ln)
            max_w = max(max_w, w)
    print(f"cues={len(cues)} max_line_width_px={max_w:.0f} (limit 1780)")
    if max_w > 1780:
        issues.append(f"subtitle line overflow: {max_w:.0f}px")

    print("== 5. App Store segments ==")
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        if "App Store" in r["text"]:
            print(f"  seg {r['segment_id']}: {r['notes']}")
            if not r["notes"].startswith("appstore_ok=True"):
                issues.append(f"seg {r['segment_id']} App Store override missing")

    print("== 6. crop upscale audit ==")
    for uid, p in sorted(B.V.items()):
        tpl = p["tpl"]
        if tpl == "crop":
            img = Image.open(ASSETS / p["img"])
            cw = p["crop"][2] - p["crop"][0]
            ch = p["crop"][3] - p["crop"][1]
            scale = 1800 / max(cw, 1)
            if scale > 2.6:
                issues.append(f"unit {uid}: crop upscale {scale:.1f}x (crop {cw}x{ch})")
        elif tpl == "full":
            img = Image.open(ASSETS / p["img"])
            scale = 1800 / max(img.size[0], 1)
            if scale > 2.6:
                issues.append(f"unit {uid}: full upscale {scale:.1f}x (src {img.size})")
        elif tpl == "phone":
            img = Image.open(ASSETS / p["img"])
            scale = min(1740 / max(img.size[0], 1), 830 / max(img.size[1], 1), 2.6)
            if scale > 2.6:
                issues.append(f"unit {uid}: phone upscale {scale:.1f}x (src {img.size})")
        elif tpl == "two":
            for k in ("img1", "img2"):
                img = Image.open(ASSETS / p[k])
                box = p.get("crop1" if k == "img1" else "crop2")
                w = box[2] - box[0] if box else img.size[0]
                scale = 870 / max(w, 1)
                if scale > 2.6:
                    issues.append(f"unit {uid} {k}: upscale {scale:.1f}x")
    print("upscale issues:", len([i for i in issues if "upscale" in i]))

    print("== 7. summary ==")
    if issues:
        print("ISSUES:")
        for i in issues:
            print("  -", i)
    else:
        print("no mechanical issues found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
