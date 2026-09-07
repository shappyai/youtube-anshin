"""Create two 1280x720 publish thumbnail candidates from SCENE-001."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))
from scene_renderer import pil_font  # noqa: E402

BASE = ROOT / "episodes" / "006_line_talk_backup"
SOURCE = BASE / "assets" / "generated_ai" / "scene_001.png"
OUT_DIR = BASE / "work" / "publish_review"
NAVY = "#173a68"
RED = "#c0392b"
WHITE = "#ffffff"


def draw_text_block(
    draw: ImageDraw.ImageDraw,
    lines: list[tuple[str, str, int]],
    x: int,
    y: int,
) -> None:
    for text, color, size in lines:
        font = pil_font(size, bold=True)
        draw.text((x + 5, y + 5), text, font=font, fill="#173a68", stroke_width=10, stroke_fill="#ffffff")
        draw.text((x, y), text, font=font, fill=color, stroke_width=4, stroke_fill="#ffffff")
        y += size + 18


def brand_chip(draw: ImageDraw.ImageDraw) -> None:
    label = "大人のデジタル安心室"
    font = pil_font(34, bold=True)
    width = int(draw.textlength(label, font=font)) + 56
    draw.rounded_rectangle((24, 648, 24 + width, 696), radius=24, fill=NAVY)
    draw.text((52, 660), label, font=font, fill=WHITE)


def line_pill(draw: ImageDraw.ImageDraw) -> None:
    label = "LINE"
    font = pil_font(30, bold=True)
    width = int(draw.textlength(label, font=font)) + 44
    draw.rounded_rectangle((24, 24, 24 + width, 66), radius=21, fill=WHITE, outline=NAVY, width=3)
    draw.text((46, 30), label, font=font, fill="#06c755" if False else NAVY)


def make_a() -> Path:
    image = Image.open(SOURCE).convert("RGB")
    crop = image.crop((280, 130, 1560, 850))
    draw = ImageDraw.Draw(crop)
    line_pill(draw)
    draw_text_block(
        draw,
        [
            ("機種変更しても、", NAVY, 88),
            ("トークは残る？", RED, 104),
        ],
        70,
        120,
    )
    brand_chip(draw)
    output = OUT_DIR / "thumbnail_a.png"
    crop.save(output, "PNG", optimize=True)
    return output


def make_b() -> Path:
    image = Image.open(SOURCE).convert("RGB")
    crop = image.crop((430, 150, 1710, 870))
    draw = ImageDraw.Draw(crop)
    line_pill(draw)
    draw_text_block(
        draw,
        [
            ("トーク、消えない？", RED, 108),
            ("機種変更の前に確認", NAVY, 60),
        ],
        66,
        150,
    )
    brand_chip(draw)
    output = OUT_DIR / "thumbnail_b.png"
    crop.save(output, "PNG", optimize=True)
    return output


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    a = make_a()
    b = make_b()
    for path in (a, b):
        with Image.open(path) as im:
            print(f"{path.name}: {im.size} {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
