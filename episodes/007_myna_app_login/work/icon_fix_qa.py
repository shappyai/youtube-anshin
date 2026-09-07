# -*- coding: utf-8 -*-
"""Episode 007 アイコン修正QA: oversized_single_iconチェック + icon_fix_comparison.png生成."""
from __future__ import annotations
import pathlib
from PIL import Image, ImageDraw, ImageFont

BASE = pathlib.Path(r"C:\Codex\260829_youtube-anshin\episodes\007_myna_app_login")
FINAL = BASE / "work" / "rendered_final_scenes"
REVIEW = BASE / "work" / "phase_b_review"
TARGETS = [1, 6, 10, 13, 20]

def font(size, bold=True):
    try:
        return ImageFont.truetype(r"C:\Windows\Fonts\meiryob.ttc" if bold else r"C:\Windows\Fonts\meiryo.ttc", size)
    except Exception:
        return ImageFont.load_default()

def largest_color_bbox(img, target, tol=8):
    """target色（±tol）の最大連結領域のバウンディングボックスを返す（簡易・4近傍無しのピクセル列近似）."""
    w, h = img.size
    best = None
    visited = set()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if (x, y) in visited:
                continue
            r, g, b = img.getpixel((x, y))[:3]
            if abs(r - target[0]) <= tol and abs(g - target[1]) <= tol and abs(b - target[2]) <= tol:
                # BFS（簡易・4近傍）
                stack = [(x, y)]
                minx, miny, maxx, maxy = x, y, x, y
                count = 0
                while stack:
                    cx, cy = stack.pop()
                    if (cx, cy) in visited:
                        continue
                    visited.add((cx, cy))
                    count += 1
                    minx, miny, maxx, maxy = min(minx, cx), min(miny, cy), max(maxx, cx), max(maxy, cy)
                    for nx, ny in ((cx + 2, cy), (cx - 2, cy), (cx, cy + 2), (cx, cy - 2)):
                        if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                            nr, ng, nb = img.getpixel((nx, ny))[:3]
                            if abs(nr - target[0]) <= tol and abs(ng - target[1]) <= tol and abs(nb - target[2]) <= tol:
                                stack.append((nx, ny))
                area = (maxx - minx + 1) * (maxy - miny + 1)
                if best is None or area > best[0]:
                    best = (area, (minx, miny, maxx, maxy), count)
    return best

GREEN = (234, 247, 238)      # var(--green) バッジ
CREAM = (253, 243, 224)      # caution-badge 背景（fdf3e0）
reports = []
for sid in TARGETS:
    p = FINAL / f"scene_{sid:03d}.png"
    if not p.exists():
        reports.append(f"scene {sid:03d}: MISSING")
        continue
    img = Image.open(p).convert("RGB")
    w, h = img.size
    warns = []
    for name, color in (("green", GREEN), ("cream", CREAM)):
        best = largest_color_bbox(img, color)
        if best:
            area, bbox, count = best
            bw, bh = bbox[2] - bbox[0] + 1, bbox[3] - bbox[1] + 1
            ratio_w, ratio_h = bw / w, bh / h
            flag = "WARN" if ratio_w > 0.15 or ratio_h > 0.15 else "ok"
            if flag == "WARN":
                warns.append(f"{name} bbox={bbox} w={bw} h={bh} ({ratio_w:.0%}x{ratio_h:.0%})")
            reports.append(f"scene {sid:03d} {name}: bbox=({bw}x{bh}) ratios=({ratio_w:.0%},{ratio_h:.0%}) {flag}")
    reports.append(f"scene {sid:03d}: " + ("WARN: " + "; ".join(warns) if warns else "PASS (no oversized single icon)"))
print("\n".join(reports))

# icon_fix_comparison.png: 修正版5sceneを並べる
TILE = (640, 360)
cols = 3
rows = 2
W = cols * (TILE[0] + 24) + 40
H = 90 + rows * (TILE[1] + 90) + 30
canvas = Image.new("RGB", (W, H), "#eef3f8")
d = ImageDraw.Draw(canvas)
d.rectangle((0, 0, W, 90), fill="#2f74bb")
d.text((W // 2, 40), "Episode 007 アイコン表現修正 5scene（oversized_single_icon解消・2026-09-04）", font=font(34), fill="#ffffff", anchor="mm")
labels = {
    1: "SCENE-001 導入（✓は小バッジ・見出し主役）",
    6: "SCENE-006 端末ロック必須（!小バッジ＋注意）",
    10: "SCENE-010 読み取り4つの注意（!小バッジ＋注意）",
    13: "SCENE-013 何度も試さない（!小バッジ＋注意）",
    20: "SCENE-020 公式窓口（青「相談」バッジ）",
}
for i, sid in enumerate(TARGETS):
    col, row = i % cols, i // cols
    x = 20 + col * (TILE[0] + 24)
    y = 110 + row * (TILE[1] + 90)
    src = FINAL / f"scene_{sid:03d}.png"
    if src.exists():
        im = Image.open(src).convert("RGB").resize(TILE, Image.Resampling.LANCZOS)
        canvas.paste(im, (x, y))
        d.rectangle((x, y, x + TILE[0], y + TILE[1]), outline="#c9d3dc", width=2)
    d.text((x, y + TILE[1] + 10), labels.get(sid, f"SCENE-{sid:03d}"), font=font(26), fill="#173a68")
out = REVIEW / "icon_fix_comparison.png"
canvas.save(out)
print("saved", out.name, canvas.size)

