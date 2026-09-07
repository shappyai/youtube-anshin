# -*- coding: utf-8 -*-
"""draft_v2 QA: 空スロット残存（最重要）・尺・黒画面・無音・字幕・review frames."""
from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[3]
EP = ROOT / "episodes" / "002_myna_app"
GEN = EP / "assets" / "generated_scenes"
COMPOSED = EP / "work" / "v2_composed"
DRAFT = Path(os.environ.get("EPISODE_002_DRAFT", str(EP / "output" / "draft_v2.mp4")))
NARRATION = EP / "audio" / "voicevox_kenzaki" / "narration_kenzaki.wav"
ASS = Path(os.environ.get("EPISODE_002_ASS", str(EP / "captions_v2.ass")))
FRAMES = Path(os.environ.get("EPISODE_002_FRAMES", str(EP / "output" / "review_frames_v2")))

sys.path.insert(0, str(EP / "work"))
import build_video_v2 as B  # noqa: E402

issues: list[str] = []


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(out.stdout)["format"]["duration"])


def main() -> int:
    print("== 1. durations ==")
    v = probe_duration(DRAFT)
    a = probe_duration(NARRATION)
    print(f"video={v:.3f}s narration={a:.3f}s diff={abs(v-a):.3f}s")
    if abs(v - a) > 0.5:
        issues.append("duration mismatch")

    print("== 2. slot residual (composed vs generated) ==")
    residual = 0
    for scene_no, specs in B.COMPOSITES.items():
        orig = Image.open(GEN / f"scene_{scene_no:03d}.png").convert("RGB")
        comp = Image.open(COMPOSED / f"scene_{scene_no:03d}.png").convert("RGB")
        for box, *_ in specs:
            x0, y0, x1, y1 = box
            o = orig.crop((x0, y0, x1, y1))
            c = comp.crop((x0, y0, x1, y1))
            diff = ImageChops.difference(o, c)
            # 白地の公式Web画面は平均差分が小さくなりやすいため、平均値だけで
            # 判定しない。一定量の非ゼロ差分があれば、実素材が入ったとみなす。
            stats = list(diff.convert("L").resize((128, 128)).getdata())
            mean = sum(stats) / len(stats)
            changed_ratio = sum(v > 8 for v in stats) / len(stats)
            filled = changed_ratio > 0.002 or (max(stats, default=0) > 40 and changed_ratio > 0.0005)
            flag = "OK" if filled else "RESIDUAL?"
            if not filled:
                residual += 1
            print(f"  scene_{scene_no:03d} slot {box}: mean_diff={mean:.1f} changed={changed_ratio:.3f} {flag}")
    if residual:
        issues.append(f"{residual} slot(s) look empty")
    else:
        print("  all slots composited")

    print("== 3. black frames ==")
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(DRAFT),
         "-vf", "signalstats,metadata=print:file=-", "-an", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    vals = [float(m.group(1)) for m in re.finditer(r"YAVG=([\d.]+)", out.stdout)]
    black = sum(1 for x in vals if x < 20)
    print(f"frames={len(vals)} black={black} minYAVG={min(vals) if vals else '-'}")
    if black:
        issues.append("black frames")

    print("== 4. silence ==")
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(DRAFT), "-af",
         "silencedetect=noise=-50dB:d=1.0", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    n = len(re.findall(r"silence_start", out.stderr))
    print(f"silence>=1s events: {n}")
    if n:
        issues.append(f"{n} silence event(s) >=1s")

    print("== 5. captions ==")
    lines = ASS.read_text(encoding="utf-8").splitlines()
    cues = [l for l in lines if l.startswith("Dialogue:")]
    bad_single = 0
    over = 0
    for c in cues:
        body = c.split(",", 9)[-1]
        txt = re.sub(r"\{\\[^}]*\}", "", body).replace("\\N", "")
        bare = txt.strip()
        if len(bare) <= 2:
            bad_single += 1
            issues.append(f"too-short cue: {bare}")
        for ln in txt.split("\\N") if "\\N" in txt else txt.split("\n"):
            pass
    # width check via est_w（1920px幅・左右60pxを確保）
    sys.path.insert(0, str(EP / "work"))
    for c in cues:
        body = c.split(",", 9)[-1]
        txt = re.sub(r"\{\\[^}]*\}", "", body)
        for ln in txt.split("\\N"):
            w = sum(72 if ord(ch) > 0x2E7F or ch in "（）「」・!?―" else 36 for ch in ln)
            if w > B.SUBTITLE_MAX_W:
                over += 1
    print(f"cues={len(cues)} too_short={bad_single} width_over={over}")
    if len(cues) != 97:
        issues.append(f"caption cue count is {len(cues)} (expected 97)")
    if over:
        issues.append(f"{over} caption line(s) exceed subtitle safe width")

    print("== 6. manifest notes (App Store / seg1) ==")
    with (EP / "audio" / "voicevox_kenzaki" / "segments_manifest.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        if r["segment_id"] in ("1", "37", "62", "63"):
            print(f"  seg {r['segment_id']}: {r['notes'][:80]}")

    print("== 7. review frames ==")
    FRAMES.mkdir(parents=True, exist_ok=True)
    targets = [1, 3, 5, 8, 10, 14, 18, 21, 22, 27, 29, 32, 34, 35]
    for n in targets:
        start = B.SCENES[f"SCENE-{n:03d}"][0]
        end = B.SCENES[f"SCENE-{n:03d}"][1]
        mid = start + (end - start) / 2
        out_p = FRAMES / f"frame_scene_{n:03d}.png"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", f"{mid:.2f}", "-i", str(DRAFT),
             "-frames:v", "1", str(out_p)],
            check=True,
        )
    print(f"  saved {len(targets)} frames to {FRAMES}")

    print("== 8. summary ==")
    if issues:
        for i in issues:
            print("  ISSUE:", i)
    else:
        print("  no issues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
