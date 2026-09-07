# -*- coding: utf-8 -*-
"""Episode 007 Phase B前半 QA: 描画sceneの安全領域・サイズ・重複SHA + imagegen_native text contact sheet."""
from __future__ import annotations
import hashlib, pathlib
from PIL import Image, ImageDraw, ImageFont
BASE = pathlib.Path(r"C:\Codex\260829_youtube-anshin\episodes\007_myna_app_login")
FINAL = BASE / "work" / "rendered_final_scenes"
REVIEW = BASE / "work" / "phase_b_review"

def font(size, bold=True):
    try:
        return ImageFont.truetype(r"C:\Windows\Fonts\meiryob.ttc" if bold else r"C:\Windows\Fonts\meiryo.ttc", size)
    except Exception:
        return ImageFont.load_default()

def safe_area_check(img):
    w, h = img.size
    strip = img.crop((0, h - 180, w, h)).resize((120, 12))
    px = list(strip.get_flattened_data()) if hasattr(strip, "get_flattened_data") else list(strip.getdata())
    active = sum(1 for p in px if min(p) < 190 and max(p) - min(p) > 28)
    return active / max(1, len(px))

# 1) QA: rendered scenes
issues = []
for p in sorted(FINAL.glob("scene_*.png")):
    im = Image.open(p)
    if im.size != (1920, 1080):
        issues.append(f"{p.name}: size {im.size}")
    ratio = safe_area_check(im)
    if ratio > 0.08:
        issues.append(f"{p.name}: bottom band active {ratio:.3f}")
print(f"rendered={len(list(FINAL.glob('scene_*.png')))} issues={len(issues)}")
for i in issues:
    print("ISSUE:", i)

# 2) SHA256 duplicates across assets
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
items = {}
for root in [BASE / "assets" / "generated_ai", BASE / "assets" / "official"]:
    if root.exists():
        for p in sorted(root.glob("*.*")):
            items[str(p.relative_to(BASE))] = sha(p)
rev = {}
for k, v in items.items():
    rev.setdefault(v, []).append(k)
dups = {h: ks for h, ks in rev.items() if len(ks) > 1}
print(f"assets_hashed={len(items)} duplicate_groups={len(dups)}")
for h, ks in dups.items():
    print("DUP:", ks)

# 3) imagegen_native text contact sheet（SCENE-003採用 + 保留5枚の指示ラベル）
targets = [
    (3, "imagegen_native", "スマホが、対応しているか", "STATUS: 採用（A/B Candidate A）"),
    (11, "imagegen_native", "暗証番号で、止まる", "PENDING（imagegen復旧後に生成）"),
    (14, "imagegen_native", "カードと、証明書の期限", "PENDING（imagegen復旧後に生成）"),
    (17, "imagegen_native", "それでも、ダメなら", "PENDING（imagegen復旧後に生成）"),
    (7, "concept+text", "カードを、読み取る", "PENDING（imagegen復旧後に生成）"),
    (22, "concept+text", "あわてずに、確認しましょう", "PENDING（imagegen復旧後に生成）"),
]
TILE = (760, 428)
W = TILE[0] * 3 + 80
H = 200 + TILE[1] * 2 + 120
canvas = Image.new("RGB", (W, H), "#eef3f8")
d = ImageDraw.Draw(canvas)
d.rectangle((0, 0, W, 90), fill="#2f74bb")
d.text((W // 2, 40), "Episode 007 imagegen_native text scenes contact sheet（2026-09-03・SCENE-003採用／他5枚は生成待ち）", font=font(34), fill="#ffffff", anchor="mm")
for i, (sid, mode, text, status) in enumerate(targets):
    col, row = i % 3, i // 3
    x = 40 + col * (TILE[0] + 20)
    y = 110 + row * (TILE[1] + 80)
    src = FINAL / f"scene_{sid:03d}.png"
    if src.exists():
        im = Image.open(src).convert("RGB").resize(TILE, Image.Resampling.LANCZOS)
        canvas.paste(im, (x, y))
    else:
        d.rounded_rectangle((x, y, x + TILE[0], y + TILE[1]), radius=18, fill="#ffffff", outline="#c9d3dc", width=2)
        d.text((x + TILE[0] // 2, y + 150), f"SCENE-{sid:03d}", font=font(42), fill="#173a68", anchor="mm")
        d.text((x + TILE[0] // 2, y + 210), text, font=font(30), fill="#587187", anchor="mm")
        d.text((x + TILE[0] // 2, y + 270), status, font=font(26), fill="#d3922e", anchor="mm")
    d.text((x + 6, y + TILE[1] + 8), f"SCENE-{sid:03d} {mode}｜{text}", font=font(24), fill="#173a68")
    d.text((x + 6, y + TILE[1] + 38), status, font=font(22), fill="#8a949e")
out = REVIEW / "imagegen_native_text_contact_sheet.png"
canvas.save(out)
print("saved", out.name, canvas.size)

