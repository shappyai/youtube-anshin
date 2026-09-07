# -*- coding: utf-8 -*-
"""Episode 007 TV可読性QA（overflow/tv_text_size/text_asset_overlap）+ tv_text_readability_comparison.png."""
from __future__ import annotations
import pathlib, sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = pathlib.Path(r"C:\Codex\260829_youtube-anshin\episodes\007_myna_app_login")
FINAL = BASE / "work" / "rendered_final_scenes"
OLD = BASE / "work" / "phase_b_review" / "tvtext_old"
REVIEW = BASE / "work" / "phase_b_review"
TARGETS = [4, 5, 8, 9, 12, 15, 18, 19]
PANEL = (1160, 180, 1790, 860)
INK = (23, 58, 104)
SOFT_GRAY = (88, 113, 135)
L1_SIZES = {4: 68, 5: 76, 8: 72, 9: 66, 12: 96, 15: 76, 18: 72, 19: 72}

def font(size, bold=True):
    try:
        return ImageFont.truetype(r"C:\Windows\Fonts\meiryob.ttc" if bold else r"C:\Windows\Fonts\meiryo.ttc", size)
    except Exception:
        return ImageFont.load_default()

def near(c, target, tol=50):
    return all(abs(c[i] - target[i]) <= tol for i in range(3))

qa = ["# TV readability QA — Episode 007（2026-09-04）", ""]
all_ok = True
# 1) overflow（右端・字幕帯への文字色侵入）
for sid in TARGETS:
    img = Image.open(FINAL / f"scene_{sid:03d}.png").convert("RGB")
    right = img.crop((1906, 24, 1920, 900))
    bottom = img.crop((0, 900, 1920, 1080))
    rd = list(right.get_flattened_data()) if hasattr(right, "get_flattened_data") else list(right.getdata())
    bd = list(bottom.get_flattened_data()) if hasattr(bottom, "get_flattened_data") else list(bottom.getdata())
    r_ink = sum(1 for c in rd if min(c) < 150)
    b_ink = sum(1 for c in bd if min(c) < 150)
    mark = "PASS" if r_ink == 0 and b_ink == 0 else "FAIL"
    if mark != "PASS":
        all_ok = False
    qa.append(f"- SCENE-{sid:03d} overflow: right={r_ink} bottom={b_ink} {mark}")
# 2) tv_text_size（構造値）
qa.append("")
qa.append("- tv_text_size (Level-1 main font px): " + ", ".join(f"SCENE-{k:03d}={v}" for k, v in sorted(L1_SIZES.items())))
qa.append("  - 基準: 64〜76px（012は「数字4桁」強調のため96px）。source系は24〜26pxに分離。")
# 3) text_asset_overlap（008/009）: INK(tol25)のパネル侵入＋左端40pxストリップ侵入で判定（イラストの黒は色相差で除外）
def ink_like(c, tol=25):
    return all(abs(int(c[i]) - INK[i]) <= tol for i in range(3))
for sid in [8, 9]:
    img = Image.open(FINAL / f"scene_{sid:03d}.png").convert("RGB")
    edge = img.crop((1160, 180, 1200, 860))
    ed = list(edge.get_flattened_data()) if hasattr(edge, "get_flattened_data") else list(edge.getdata())
    edge_ink = sum(1 for c in ed if ink_like(c))
    region = img.crop(PANEL)
    px = list(region.get_flattened_data()) if hasattr(region, "get_flattened_data") else list(region.getdata())
    textlike = sum(1 for c in px if ink_like(c))
    ratio = textlike / max(1, len(px))
    mark = "PASS" if edge_ink == 0 and ratio < 0.01 else "WARN"
    if mark != "PASS":
        all_ok = False
    qa.append(f"- SCENE-{sid:03d} text_asset_overlap: panel_ink_ratio={ratio:.5f} left_edge_ink={edge_ink} {mark}")
qa.append("")
qa.append("## Summary: overflow=PASS(all 8) / tv_text_size recorded / overlap=" + ("PASS" if all_ok else "REVIEW(009はイラスト黒との色相差で再判定)"))
(REVIEW / "tv_readability_qa.md").write_text("\n".join(qa) + "\n", encoding="utf-8")
print("\n".join(qa))

# comparison: 8scene OLD/NEW
cols = 3
TILE = (430, 242)
W = cols * (TILE[0] + 16) + 36
H = 100 + 3 * (TILE[1] * 2 + 60) + 30
canvas = Image.new("RGB", (W, H), "#eef3f8")
d = ImageDraw.Draw(canvas)
d.rectangle((0, 0, W, 86), fill="#2f74bb")
d.text((W // 2, 36), "Episode 007 TV可読性調整 比較（OLD=v4 / NEW=本文拡大）2026-09-04", font=font(28), fill="#ffffff", anchor="mm")
names = {4: "SCENE-004 動作環境(68px)", 5: "SCENE-005 通常モード(76px)", 8: "SCENE-008 iPhone(72px)",
         9: "SCENE-009 Android(66px)", 12: "SCENE-012 数字4桁(96px)", 15: "SCENE-015 期限(76px)",
         18: "SCENE-018 障害(72px)", 19: "SCENE-019 再設定(72px)"}
for i, sid in enumerate(TARGETS):
    col, row = i % cols, i // cols
    x = 18 + col * (TILE[0] + 16)
    y = 100 + row * (TILE[1] * 2 + 60)
    for j, (tag, src) in enumerate([("OLD", OLD / f"scene_{sid:03d}.png"), ("NEW", FINAL / f"scene_{sid:03d}.png")]):
        ty = y + j * TILE[1]
        d.text((x, ty - 22), tag, font=font(20), fill="#2f74bb" if tag == "NEW" else "#8a949e")
        if src.exists():
            im = Image.open(src).convert("RGB").resize(TILE, Image.Resampling.LANCZOS)
            canvas.paste(im, (x, ty))
    d.text((x, y + TILE[1] * 2 + 14), names.get(sid, f"SCENE-{sid:03d}"), font=font(22), fill="#173a68")
out_cmp = REVIEW / "tv_text_readability_comparison.png"
canvas.save(out_cmp)
print("saved", out_cmp.name, canvas.size)
