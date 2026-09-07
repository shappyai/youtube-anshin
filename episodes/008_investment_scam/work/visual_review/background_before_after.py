# -*- coding: utf-8 -*-
"""Create the Episode 008 v2 vs user-background visual comparison."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


BASE = Path(__file__).resolve().parent
V2_DIR = BASE.parent / "rendered_final_scenes"
V3_DIR = BASE.parent / "rendered_final_scenes_v3"
OUTPUT = BASE / "background_before_after.png"
TARGETS = [2, 5, 7, 9, 12, 15, 17, 18]
THUMB_SIZE = (480, 270)
GAP = 18
SIDE = 36
HEADER = 94
LABEL_H = 34


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in ("C:/Windows/Fonts/YuGothB.ttc", "C:/Windows/Fonts/meiryob.ttc"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def main() -> None:
    width = SIDE * 2 + THUMB_SIZE[0] * 2 + GAP
    row_height = THUMB_SIZE[1] + LABEL_H
    height = HEADER + 24 + len(TARGETS) * row_height
    sheet = Image.new("RGB", (width, height), "#eef4f9")
    draw = ImageDraw.Draw(sheet)
    draw.text((SIDE, 16), "Episode 008 Visual Gate v3 — 背景比較", font=font(28), fill="#173a68")
    draw.text((SIDE, 56), "左: v2 gradient/decorations  ／  右: ユーザー提供背景・装飾overlayなし", font=font(21), fill="#587187")
    y = HEADER + 24
    for scene_id in TARGETS:
        for directory, x in ((V2_DIR, SIDE), (V3_DIR, SIDE + THUMB_SIZE[0] + GAP)):
            path = directory / f"scene_{scene_id:03d}.png"
            if not path.exists():
                raise FileNotFoundError(path)
            with Image.open(path) as source:
                thumb = ImageOps.fit(source.convert("RGB"), THUMB_SIZE, method=Image.Resampling.LANCZOS)
            sheet.paste(thumb, (x, y))
            draw.rectangle((x, y, x + THUMB_SIZE[0], y + THUMB_SIZE[1]), outline="#9db8cc", width=2)
        draw.text((SIDE, y + THUMB_SIZE[1] + 6), f"SCENE-{scene_id:03d}", font=font(20), fill="#2f74bb")
        y += row_height
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUTPUT, "PNG")
    print(f"saved {OUTPUT} {sheet.size[0]}x{sheet.size[1]}")


if __name__ == "__main__":
    main()
