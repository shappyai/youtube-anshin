# -*- coding: utf-8 -*-
"""Episode 007 Visual polish QA（text_asset_overlap・safe area）＋ visual_polish_comparison.png 生成."""
from __future__ import annotations
import pathlib, sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image, ImageDraw, ImageFont

BASE = pathlib.Path(r"C:\Codex\260829_youtube-anshin\episodes\007_myna_app_login")
FINAL = BASE / "work" / "rendered_final_scenes"
OLD = BASE / "work" / "phase_b_review" / "v3_as_old"
REVIEW = BASE / "work" / "phase_b_review"
OVERLAP_SCENES = [8, 9]
PANEL = (1060, 160, 1820, 860)
INK = (23, 58, 104)
SOFT_GRAY = (88, 113, 135)
COMPARE_SCENES = [2, 4, 5, 8, 9, 12, 15, 16, 18, 19, 21]

def font(size, bold=True):
    try:
        return ImageFont.truetype(r"C:\Windows\Fonts\meiryob.ttc" if bold else r"C:\Windows\Fonts\meiryo.ttc", size)
    except Exception:
        return ImageFont.load_default()

def near(c, target, tol=45):
    return all(abs(c[i] - target[i]) <= tol for i in range(3))

qa = ["# Visual polish QA — Episode 007（2026-09-04）", ""]
ok = True
# 1) text/asset overlap（右パネル領域に文字色が侵入していないか）
for sid in OVERLAP_SCENES:
    p = FINAL / f"scene_{sid:03d}.png"
    img = Image.open(p).convert("RGB")
    region = img.crop(PANEL)
    px = list(region.get_flattened_data()) if hasattr(region, "get_flattened_data") else list(region.getdata())
    textlike = sum(1 for c in px if near(c, INK) or near(c, SOFT_GRAY))
    ratio = textlike / max(1, len(px))
    mark = "PASS" if ratio < 0.01 else "WARN"
    if mark != "PASS":
        ok = False
    qa.append(f"- SCENE-{sid:03d} text_asset_overlap: panel_region={PANEL} text_like_ratio={ratio:.5f} {mark} (threshold 1%)")
# 2) subtitle safe area（全22）
issues = []
scenes_png = sorted(FINAL.glob("scene_*.png"))
for p in scenes_png:
    img = Image.open(p).convert("RGB")
    strip = img.crop((0, 900, 1920, 1080)).resize((120, 12))
    data = list(strip.get_flattened_data()) if hasattr(strip, "get_flattened_data") else list(strip.getdata())
    active = sum(1 for c in data if min(c) < 190 and max(c) - min(c) > 28)
    if active / len(data) > 0.03:
        issues.append(p.name)
qa.append(f"- subtitle safe area: scenes={len(scenes_png)} issues={len(issues)} {'PASS' if not issues else 'WARN: ' + ','.join(issues)}")
# 3) visual_polish_comparison.png（OLD v3 / NEW）
TILE = (430, 242)
cols = 3
W = cols * (TILE[0] + 18) + 40
H = 110 + 4 * (TILE[1] + 66) + 30
canvas = Image.new("RGB", (W, H), "#eef3f8")
d = ImageDraw.Draw(canvas)
d.rectangle((0, 0, W, 90), fill="#2f74bb")
d.text((W // 2, 36), "Episode 007 Visual polish 比較（OLD=v3 / NEW=v4）2026-09-04", font=font(30), fill="#ffffff", anchor="mm")
labels = {2: "SCENE-002 一覧(soft gradient)", 4: "SCENE-004 動作環境", 5: "SCENE-005 FAQ",
          8: "SCENE-008 iPhone読み取り(2カラム)", 9: "SCENE-009 Android読み取り(2カラム)", 12: "SCENE-012 登録(+dialpad)",
          15: "SCENE-015 有効期限(+badge)", 16: "SCENE-016 比較(soft gradient)", 18: "SCENE-018 障害(+construction)",
          19: "SCENE-019 再設定(+lock_reset)", 21: "SCENE-021 まとめ(行間fix)"}
for i, sid in enumerate(COMPARE_SCENES):
    col, row = i % cols, i // cols
    x = 20 + col * (TILE[0] + 18)
    y = 110 + row * (TILE[1] + 66)
    for j, (tag, src) in enumerate([("OLD", OLD / f"scene_{sid:03d}.png"), ("NEW", FINAL / f"scene_{sid:03d}.png")]):
        ty = y + j * (TILE[1] // 2 + 8)
        d.text((x, ty - 20), tag, font=font(20), fill="#2f74bb" if tag == "NEW" else "#8a949e")
        if src.exists():
            im = Image.open(src).convert("RGB").resize((TILE[0], TILE[1] // 2), Image.Resampling.LANCZOS)
            canvas.paste(im, (x, ty))
    d.text((x, y + TILE[1] + 12), labels.get(sid, f"SCENE-{sid:03d}"), font=font(22), fill="#173a68")
out_cmp = REVIEW / "visual_polish_comparison.png"
canvas.save(out_cmp)
qa += ["", f"## Summary: text_asset_overlap={'PASS' if ok else 'REVIEW'} / safe_area={'PASS' if not issues else 'REVIEW'} / comparison saved: {out_cmp.name}"]
(REVIEW / "visual_polish_qa.md").write_text("\n".join(qa) + "\n", encoding="utf-8")
print("\n".join(qa))
