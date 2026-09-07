# -*- coding: utf-8 -*-
"""Episode 007 semantic SVG icon QA + semantic_icon_comparison.png生成."""
from __future__ import annotations
import pathlib
from PIL import Image, ImageDraw, ImageFont

BASE = pathlib.Path(r"C:\Codex\260829_youtube-anshin\episodes\007_myna_app_login")
ROOT = pathlib.Path(r"C:\Codex\260829_youtube-anshin")
FINAL = BASE / "work" / "rendered_final_scenes"
OLD = BASE / "work" / "phase_b_review" / "icon_badge_v1"
REVIEW = BASE / "work" / "phase_b_review"
ICON_DIR = ROOT / "assets" / "icons" / "material_symbols"
TARGETS = [1, 6, 10, 13, 20]

def font(size, bold=True):
    try:
        return ImageFont.truetype(r"C:\Windows\Fonts\meiryob.ttc" if bold else r"C:\Windows\Fonts\meiryo.ttc", size)
    except Exception:
        return ImageFont.load_default()

def largest_dark_bbox(img, max_channel=110):
    w, h = img.size
    best = None
    visited = set()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if (x, y) in visited:
                continue
            r, g, b = img.getpixel((x, y))[:3]
            if min(r, g, b) <= max_channel:
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
                            if min(nr, ng, nb) <= max_channel:
                                stack.append((nx, ny))
                area = (maxx - minx + 1) * (maxy - miny + 1)
                if best is None or area > best[0]:
                    best = (area, (minx, miny, maxx, maxy), count)
    return best

qa_lines = ["# semantic_icon_quality QA — Episode 007（2026-09-04）", ""]
scene_icons = {1: "login", 6: "lock", 10: "contactless", 13: "block", 20: "support_agent"}
tones = {1: "navy", 6: "blue", 10: "blue", 13: "amber", 20: "green"}
allpass = True
for sid in TARGETS:
    p = FINAL / f"scene_{sid:03d}.png"
    if not p.exists():
        qa_lines.append(f"- SCENE-{sid:03d}: MISSING"); allpass = False; continue
    img = Image.open(p).convert("RGB")
    w, h = img.size
    best = largest_dark_bbox(img)
    if best:
        area, bbox, count = best
        bw, bh = bbox[2] - bbox[0] + 1, bbox[3] - bbox[1] + 1
        area_ratio = area / (w * h)
        mark = "PASS" if area_ratio <= 0.15 else "WARN(oversized)"
        if mark != "PASS":
            allpass = False
        qa_lines.append(
            f"- SCENE-{sid:03d}: icon={scene_icons[sid]}/{tones[sid]} dark_bbox=({bw}x{bh}) "
            f"area_ratio={area_ratio:.3f} {mark} (threshold 0.15)"
        )
    else:
        qa_lines.append(f"- SCENE-{sid:03d}: dark icon not detected")
        allpass = False
    asset = ICON_DIR / f"{scene_icons[sid]}_{tones[sid]}.png"
    if not asset.exists():
        qa_lines.append(f"- SCENE-{sid:03d}: MISSING asset {asset.name}")
        allpass = False
    else:
        with Image.open(asset) as aim:
            rgba = aim.convert("RGBA")
            corners = [rgba.getpixel(p) for p in [(2, 2), (510, 2), (2, 510), (510, 510)]]
            alpha_ok = all(c[3] == 0 for c in corners)
            qa_lines.append(f"- SCENE-{sid:03d}: asset {asset.name} transparent_corners={'PASS' if alpha_ok else 'REVIEW'}")
qr = "PASS（automated）" if allpass else "REVIEW"
qa_lines += [
    "",
    "## REVIEW（人間目視）",
    "",
    "- icon matches scene meaning / not generic punctuation / not emoji-like / not tiny UI badge / TV readable: 各sceneをcontact sheet（v3）とsemantic_icon_comparisonで確認する。",
    "- license/source: assets/icons/LICENSES.md に記録。",
    "",
    f"## Summary: automated_results={qr} scenes=5",
]
out_md = REVIEW / "semantic_icon_qa.md"
out_md.write_text("\n".join(qa_lines) + "\n", encoding="utf-8")
print("\n".join(qa_lines[-8:]))

# semantic_icon_comparison.png: 上段OLD(badge v1) 下段NEW(semantic icon) x 5scene
TILE = (480, 270)
gap = 16
W = 5 * TILE[0] + 6 * gap + 40
H = 150 + 2 * (TILE[1] + 110) + 60
canvas = Image.new("RGB", (W, H), "#eef3f8")
d = ImageDraw.Draw(canvas)
d.rectangle((0, 0, W, 90), fill="#2f74bb")
d.text((W // 2, 36), "Episode 007 semantic SVG icon 比較（OLD=丸バッジ版 / NEW=Material Symbols Rounded）2026-09-04", font=font(32), fill="#ffffff", anchor="mm")
names = {1: "SCENE-001 ログインできない？", 6: "SCENE-006 端末ロック必須", 10: "SCENE-010 読み取り注意", 13: "SCENE-013 何度も試さない", 20: "SCENE-020 公式窓口相談"}
for i, sid in enumerate(TARGETS):
    x = 20 + gap + i * (TILE[0] + gap)
    rows = [("OLD", OLD / f"scene_{sid:03d}.png"), ("NEW", FINAL / f"scene_{sid:03d}.png")]
    for j, (label, src) in enumerate(rows):
        y = 110 + j * (TILE[1] + 110)
        d.text((x, y - 28), label, font=font(26), fill="#2f74bb" if label == "NEW" else "#8a949e")
        if src.exists():
            im = Image.open(src).convert("RGB").resize(TILE, Image.Resampling.LANCZOS)
            canvas.paste(im, (x, y))
            d.rectangle((x, y, x + TILE[0], y + TILE[1]), outline="#c9d3dc", width=2)
        if j == 0:
            d.text((x, y + TILE[1] + 10), names.get(sid, f"SCENE-{sid:03d}"), font=font(26), fill="#173a68")
        else:
            ic = scene_icons[sid]
            d.text((x, y + TILE[1] + 10), f"icon: {ic} / tint: {tones[sid]}", font=font(24), fill="#587187")
out = REVIEW / "semantic_icon_comparison.png"
canvas.save(out)
print("saved", out.name, canvas.size)

