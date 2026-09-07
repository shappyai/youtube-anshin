# -*- coding: utf-8 -*-
"""draft代表フレーム抽出 + End Screen mock 生成."""
from __future__ import annotations
import json, subprocess, sys
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
DRAFT = BASE / "output" / "draft_v2.mp4"
OUT = BASE / "work" / "qa_frames_draft_v2"
OUT.mkdir(parents=True, exist_ok=True)
scenes = {int(s["id"]): s for s in DATA["scenes"]}
by_seg = {int(s["segment_id"]): s for s in SEGS}

def scene_mid(scene):
    start = scene["start_segment"]
    end = scene["end_segment"]
    ss = by_seg[start]["start_sec"]
    se = by_seg[end]["end_sec"]
    return (ss + se) / 2 + 0.2

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
# CTA: narration終了 + 2s
narration_end = SEGS[-1]["end_sec"]
cta_t = min(narration_end + 2.0, TIMING["duration"] + 8.0)
out_cta = OUT / "cta.png"
subprocess.run(
    [str(FFMPEG), "-y", "-ss", f"{cta_t:.3f}", "-i", str(DRAFT), "-frames:v", "1",
     "-vf", "scale=960:540", str(out_cta)],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
)
print(f"cta t={cta_t:.1f}s {'OK' if out_cta.exists() else 'FAIL'}")

# End Screen mock（重なり確認用・draftには焼き込まない）
from PIL import Image, ImageDraw, ImageFont
cta_png = BASE / "work" / "channel_cta.png"
mock = Image.open(cta_png).convert("RGB").copy()
d = ImageDraw.Draw(mock)
def f(sz, bold=True):
    try:
        return ImageFont.truetype(r"C:\Windows\Fonts\meiryob.ttc" if bold else r"C:\Windows\Fonts\meiryo.ttc", sz)
    except Exception:
        return ImageFont.load_default()
# 関連動画枠（右上）・subscribe枠（右下）を半透明枠で
overlay = Image.new("RGBA", mock.size, (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
od.rectangle((1180, 90, 1780, 420), fill=(47, 116, 187, 60), outline=(47, 116, 187, 220), width=4)
od.rectangle((1180, 90, 1780, 160), fill=(47, 116, 187, 120))
od.ellipse((1680, 790, 1810, 920), outline=(63, 169, 117, 200), width=5)
od.ellipse((1680, 790, 1810, 920), fill=(63, 169, 117, 45))
mock = Image.alpha_composite(mock.convert("RGBA"), overlay)
d2 = ImageDraw.Draw(mock)
d2.text((1200, 98), "想定: 関連動画1枠（Episode 002候補）", font=f(26), fill="#ffffff")
d2.text((1670, 935), "想定: 登録ボタン", font=f(24), fill="#3f8c58", anchor="ra")
mock.convert("RGB").save(BASE / "work" / "phase_b_review" / "end_screen_mock_v2.png")
print("end_screen_mock saved")

