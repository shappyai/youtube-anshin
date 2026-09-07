# -*- coding: utf-8 -*-
"""draft_v3 代表フレーム抽出 + End Screen mock v3 + v2/v3 回帰確認 + CTA比較."""
from __future__ import annotations
import json, subprocess, sys, hashlib
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
DRAFT = BASE / "output" / "draft_v3.mp4"
OUT = BASE / "work" / "qa_frames_draft_v3"
V2 = BASE / "work" / "qa_frames_draft_v2"
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

# 回帰確認: 本編sceneは v2 と同一（CTAのみ差分）
diff_scenes = []
for f in sorted(OUT.glob("scene_*.png")):
    v2f = V2 / f.name
    if not v2f.exists():
        diff_scenes.append((f.name, "no_v2"))
        continue
    h1 = hashlib.sha256(f.read_bytes()).hexdigest()
    h2 = hashlib.sha256(v2f.read_bytes()).hexdigest()
    if h1 != h2:
        diff_scenes.append((f.name, "DIFF"))
print("REGRESSION same_as_v2:", "PASS" if not diff_scenes else diff_scenes)

# End Screen mock v3（関連動画・登録は右上/右中・右下。次はこちらと被らない配置）
from PIL import Image, ImageDraw, ImageFont

cta_png = BASE / "work" / "channel_cta.png"
mock = Image.open(cta_png).convert("RGB").copy()


def f(sz, bold=True):
    try:
        return ImageFont.truetype(r"C:\Windows\Fonts\meiryob.ttc" if bold else r"C:\Windows\Fonts\meiryo.ttc", sz)
    except Exception:
        return ImageFont.load_default()


overlay = Image.new("RGBA", mock.size, (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
# 関連動画枠（右中・「次はこちら」y110-175 とは被らない）
od.rectangle((1150, 430, 1790, 780), fill=(47, 116, 187, 60), outline=(47, 116, 187, 220), width=4)
od.rectangle((1150, 430, 1790, 500), fill=(47, 116, 187, 120))
# 登録ボタン枠（右下）
od.ellipse((1680, 795, 1810, 925), outline=(63, 169, 117, 200), width=5)
od.ellipse((1680, 795, 1810, 925), fill=(63, 169, 117, 45))
mock = Image.alpha_composite(mock.convert("RGBA"), overlay)
d2 = ImageDraw.Draw(mock)
d2.text((1170, 438), "想定: 関連動画1枠（Episode 002候補）", font=f(26), fill="#ffffff")
d2.text((1670, 940), "想定: 登録ボタン", font=f(24), fill="#3f8c58", anchor="ra")
mock.convert("RGB").save(REVIEW / "end_screen_mock_v3.png")
print("end_screen_mock_v3 saved")

# CTA v2 vs v3 比較画像
from PIL import Image as PImage

left = PImage.open(V2 / "cta.png").convert("RGB")
right = PImage.open(out_cta).convert("RGB")
W2 = left.width
comp = PImage.new("RGB", (W2 * 2, left.height + 46), "#173a68")
comp.paste(left, (0, 46))
comp.paste(right, (W2, 46))
cd = ImageDraw.Draw(comp)
cd.text((20, 8), "v2 (draft_v2 CTA)", font=f(32), fill="#ffffff")
cd.text((W2 + 20, 8), "v3 (draft_v3 CTA)", font=f(32), fill="#ffffff")
cd.line((W2 - 1, 60, W2 - 1, comp.height), fill="#d4e5f0", width=2)
comp.save(REVIEW / "cta_v2_v3_comparison.png")
print("cta_v2_v3_comparison saved")
print("DONE")
