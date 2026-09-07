# -*- coding: utf-8 -*-
"""publish/thumbnail_A/B/C.png (1280x720) — 001完成版用サムネイル3案。
シンプルグラフィック（スマホ・盾・チェック）のみで構成。Googleロゴ・公式UIの模倣はしない。
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EP = Path(__file__).resolve().parents[1]
WORK = EP / "work"
OUT = EP / "publish"
FONT = str(WORK / "font.ttc")

W, H = 1280, 720
SCALE = 2
NAVY = (31, 42, 55)
BLUE = (46, 109, 164)
GREEN = (62, 142, 110)
AMBER = (217, 142, 50)
BG = (247, 245, 242)
WARM = (236, 232, 224)
WHITE = (255, 255, 255)


def canvas():
    return Image.new("RGB", (W * SCALE, H * SCALE), BG)


def rr(d, box, radius, fill):
    d.rounded_rectangle([x * SCALE for x in box], radius=radius * SCALE, fill=fill)


def txt(d, pos, text, size, fill, anchor="mm", bold_font=None):
    f = ImageFont.truetype(FONT, size * SCALE)
    d.text((pos[0] * SCALE, pos[1] * SCALE), text, font=f, fill=fill,
           anchor=anchor)


def check_mark(d, cx, cy, r, color=WHITE):
    s = SCALE
    pts = [(int(cx - r * 0.45), int(cy + 0.02 * r)), (int(cx - r * 0.10), int(cy + r * 0.42)),
           (int(cx + r * 0.55), int(cy - r * 0.38))]
    d.line([(x * s, y * s) for x, y in pts], fill=color, width=16 * s, joint="curve")


def shield_path(cx, cy, w, h):
    s = SCALE
    return [(int(cx - w / 2), int(cy - h / 2)), (int(cx), int(cy - h / 2 - h * 0.10)),
            (int(cx + w / 2), int(cy - h / 2)), (int(cx + w / 2), int(cy + h * 0.08)),
            (int(cx), int(cy + h / 2)), (int(cx - w / 2), int(cy + h * 0.08))]


def phone(d, cx, cy, w, h, body=NAVY, screen=WHITE):
    rr(d, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 34, body)
    rr(d, (cx - w / 2 + 14, cy - h / 2 + 14, cx + w / 2 - 14, cy + h / 2 - 14), 24, screen)


def thumb_a():
    im = canvas()
    d = ImageDraw.Draw(im)
    rr(d, (60, 80, 620, 640), 44, WARM)            # 左パネル
    rr(d, (700, 80, 1240, 640), 44, NAVY)           # 右パネル
    txt(d, (340, 220), "まず確認", 96, NAVY)
    txt(d, (340, 370), "5項目", 170, BLUE)
    for i in range(5):
        cx = 180 + i * 80
        d.ellipse([(cx - 34) * SCALE, 470 * SCALE, (cx + 34) * SCALE, 538 * SCALE],
                  fill=WHITE, outline=GREEN, width=6 * SCALE)
        check_mark(d, cx, 504, 26, color=GREEN)
    phone(d, 970, 300, 230, 400, body=BLUE)
    d.polygon(shield_path(970, 300, 90, 110), fill=GREEN)
    check_mark(d, 970, 300, 34)
    txt(d, (970, 550), "Googleアカウント", 44, WHITE)
    return im


def thumb_b():
    im = canvas()
    d = ImageDraw.Draw(im)
    rr(d, (60, 80, 620, 640), 44, WARM)
    d.polygon(shield_path(340, 360, 250, 300), fill=BLUE)
    check_mark(d, 340, 360, 90)
    txt(d, (930, 250), "安全チェック", 120, NAVY)
    txt(d, (930, 420), "Googleアカウント", 66, BLUE)
    rr(d, (700, 460, 940, 620), 26, GREEN)
    txt(d, (820, 540), "5つ", 92, WHITE)
    txt(d, (640, 660), "公式情報で確認", 46, (120, 128, 135))
    return im


def thumb_c():
    im = canvas()
    d = ImageDraw.Draw(im)
    im2 = Image.new("RGB", (W * SCALE, H * SCALE), (237, 241, 245))
    d = ImageDraw.Draw(im2)
    phone(d, 400, 360, 260, 430, body=NAVY)
    rr(d, (400 - 80, 300 - 80, 400 + 80, 300 + 80), 20, AMBER)
    d.ellipse([(400 - 38) * SCALE, (300 - 22) * SCALE, (400 + 38) * SCALE, (300 + 54) * SCALE],
              fill=NAVY)
    d.ellipse([(400 - 18) * SCALE, (300 + 2) * SCALE, (400 + 18) * SCALE, (300 + 38) * SCALE],
              fill=AMBER)
    rr(d, (400 - 8, 300 + 38, 400 + 8, 300 + 90), 8, AMBER)
    txt(d, (900, 250), "乗っ取り前に", 96, NAVY)
    txt(d, (900, 410), "5項目を確認", 120, BLUE)
    rr(d, (660, 500, 1160, 512), 6, GREEN)
    return im2


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [("A", thumb_a), ("B", thumb_b), ("C", thumb_c)]:
        im = fn().resize((W, H), Image.LANCZOS)
        p = OUT / f"thumbnail_{name}.png"
        im.save(p)
        print(p, p.stat().st_size)


if __name__ == "__main__":
    main()
