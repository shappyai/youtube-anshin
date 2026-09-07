# -*- coding: utf-8 -*-
"""draft_v5 代表フレーム抽出 + v4/v5 回帰確認 + CTA比較."""
from __future__ import annotations
import json, subprocess, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "episodes" / "007_myna_app_login"
FFMPEG = (
    Path(r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages")
    / "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    / "ffmpeg-8.1.1-full_build" / "bin" / "ffmpeg.exe"
)
DATA = json.loads((BASE / "episode.json").read_text(encoding="utf-8"))
TIMING = json.loads((BASE / "work" / "audio_timing.json").read_text(encoding="utf-8"))
SEGS = TIMING["segments"]
DRAFT = BASE / "output" / "draft_v5.mp4"
OUT = BASE / "work" / "qa_frames_draft_v5"
V4 = BASE / "work" / "qa_frames_draft_v4"
REVIEW = BASE / "work" / "phase_b_review"
OUT.mkdir(parents=True, exist_ok=True)
scenes = {int(s["id"]): s for s in DATA["scenes"]}
by_seg = {int(s["segment_id"]): s for s in SEGS}


def scene_mid(scene):
    start = scene["start_segment"]
    end = scene["end_segment"]
    return (by_seg[start]["start_sec"] + by_seg[end]["end_sec"]) / 2 + 0.2


targets = [1, 3, 5, 7, 8, 9, 11, 12, 14, 15, 17, 18, 19, 20, 22]
for sid in targets:
    t = scene_mid(scenes[sid])
    out = OUT / f"scene_{sid:03d}.png"
    subprocess.run(
        [str(FFMPEG), "-y", "-ss", f"{t:.3f}", "-i", str(DRAFT), "-frames:v", "1",
         "-vf", "scale=960:540", str(out)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    )
    print(f"scene {sid:03d} t={t:.1f}s {'OK' if out.exists() else 'FAIL'}")
narration_end = SEGS[-1]["end_sec"]
cta_t = min(narration_end + 2.0, TIMING["duration"] + 8.0)
out_cta = OUT / "cta.png"
subprocess.run(
    [str(FFMPEG), "-y", "-ss", f"{cta_t:.3f}", "-i", str(DRAFT), "-frames:v", "1",
     "-vf", "scale=960:540", str(out_cta)],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
)
print(f"cta t={cta_t:.1f}s {'OK' if out_cta.exists() else 'FAIL'}")

# 回帰: 本編sceneは v4 と同一
diff_scenes = []
for f in sorted(OUT.glob("scene_*.png")):
    v4f = V4 / f.name
    if not v4f.exists():
        diff_scenes.append((f.name, "no_v4"))
        continue
    if hashlib.sha256(f.read_bytes()).hexdigest() != hashlib.sha256(v4f.read_bytes()).hexdigest():
        diff_scenes.append((f.name, "DIFF"))
print("REGRESSION same_as_v4:", "PASS" if not diff_scenes else diff_scenes)

# CTA v4 vs v5 比較画像
from PIL import Image as PImage, ImageDraw, ImageFont


def f(sz, bold=True):
    try:
        return ImageFont.truetype(r"C:\Windows\Fonts\meiryob.ttc" if bold else r"C:\Windows\Fonts\meiryo.ttc", sz)
    except Exception:
        return ImageFont.load_default()


left = PImage.open(V4 / "cta.png").convert("RGB")
right = PImage.open(out_cta).convert("RGB")
W2 = left.width
comp = PImage.new("RGB", (W2 * 2, left.height + 46), "#173a68")
comp.paste(left, (0, 46))
comp.paste(right, (W2, 46))
cd = ImageDraw.Draw(comp)
cd.text((20, 8), "v4 (draft_v4 CTA: ロゴ+チャンネル名あり)", font=f(26), fill="#ffffff")
cd.text((W2 + 20, 8), "v5 (draft_v5 CTA: チャンネル名も削除)", font=f(26), fill="#ffffff")
cd.line((W2 - 1, 46, W2 - 1, comp.height), fill="#d4e5f0", width=2)
comp.save(REVIEW / "cta_v4_v5_comparison.png")
print("cta_v4_v5_comparison saved")
print("DONE")
