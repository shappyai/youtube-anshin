# -*- coding: utf-8 -*-
"""第3稿用の仮ビジュアル生成（差し替え可能なPNG）。
単純な図形（スマホ・盾・チェック・ベル）を PIL で描画する。
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WORK = Path(__file__).resolve().parent

ACCENT = (46, 109, 164, 255)
LIGHT = (226, 236, 246, 255)
DARK = (31, 42, 55, 255)
GRAY = (91, 101, 112, 255)
WHITE = (255, 255, 255, 255)


def smooth(img: Image.Image) -> Image.Image:
    return img.resize((img.width // 2, img.height // 2), Image.LANCZOS)


def draw_phone(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, fill, outline, width=6):
    d.rounded_rectangle([x, y, x + w, y + h], radius=26, outline=outline, width=width, fill=fill)
    # 画面部分（パンチホールのドット）
    d.ellipse([x + w // 2 - 5, y + 10, x + w // 2 + 5, y + 20], fill=outline)


def draw_shield(d: ImageDraw.ImageDraw, cx: int, cy: int, s: float, fill, outline):
    pts = [
        (cx, cy - 70 * s),
        (cx + 62 * s, cy - 35 * s),
        (cx + 62 * s, cy + 15 * s),
        (cx, cy + 70 * s),
        (cx - 62 * s, cy + 15 * s),
        (cx - 62 * s, cy - 35 * s),
    ]
    d.polygon(pts, fill=fill, outline=outline, width=4)


def make_intro() -> Image.Image:
    S = 2
    img = Image.new("RGBA", (1920 // S, 1080 // S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # 背景のソフトな円
    d.ellipse([160, 20, 560, 420], fill=LIGHT)
    # スマホ（左）
    draw_phone(d, 200, 60, 150, 300, (255, 255, 255, 255), ACCENT, 7)
    # スマホ内の盾＋チェック
    draw_shield(d, 275, 210, 0.8, ACCENT, ACCENT)
    d.line([(245, 205), (268, 228), (308, 182)], fill=WHITE, width=10, joint="curve")
    # チェックマークの円バッジ（右）
    d.ellipse([420, 250, 520, 350], fill=ACCENT)
    d.line([(448, 302), (470, 324), (496, 286)], fill=WHITE, width=12, joint="curve")
    # 小さなスマホ（右上、控えめ）
    draw_phone(d, 470, 60, 90, 180, (255, 255, 255, 255), GRAY, 5)
    d.line([(492, 120), (508, 140), (538, 100)], fill=GRAY, width=7, joint="curve")
    return smooth(img)


def make_cta() -> Image.Image:
    S = 2
    img = Image.new("RGBA", (1920 // S, 1080 // S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([700, 260, 980, 540], fill=LIGHT)
    # ベル（落ち着いたトーン）
    bx, by = 840, 400
    d.arc([bx - 55, by - 90, bx + 55, by + 40], start=180, end=360, fill=ACCENT, width=14)
    d.rectangle([bx - 60, by - 5, bx + 60, by + 12], fill=ACCENT)
    d.ellipse([bx - 28, by + 8, bx + 28, by + 48], fill=ACCENT)
    # チェックバッジ
    d.ellipse([855, 400, 945, 490], fill=ACCENT)
    d.line([(876, 448), (895, 467), (924, 426)], fill=WHITE, width=10, joint="curve")
    return smooth(img)


def main():
    make_intro().save(WORK / "intro_visual.png")
    make_cta().save(WORK / "cta_visual.png")
    print("intro_visual.png / cta_visual.png written")


if __name__ == "__main__":
    main()
