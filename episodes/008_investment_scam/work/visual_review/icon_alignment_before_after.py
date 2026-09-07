# -*- coding: utf-8 -*-
"""Create a large Episode 008 v4 -> v5 semantic-icon comparison."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


BASE = Path(__file__).resolve().parent
V4_DIR = BASE.parent / "rendered_final_scenes_v4"
V5_DIR = BASE.parent / "rendered_final_scenes_v5"
OUTPUT = BASE / "icon_alignment_before_after.png"
TARGETS = [2, 5, 7, 9, 12, 14]
THUMB_SIZE = (760, 428)
GAP = 24
SIDE = 40
HEADER = 112
LABEL_H = 38


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
    height = HEADER + 26 + len(TARGETS) * row_height
    sheet = Image.new("RGB", (width, height), "#eef4f9")
    draw = ImageDraw.Draw(sheet)
    draw.text((SIDE, 18), "Episode 008 Visual Gate v4 → v5 semantic icon比較", font=font(34), fill="#173a68")
    draw.text((SIDE, 66), "左: v4（元PNG canvas配置）　右: v5（alpha bbox trim・visual box fit・glyph中心整列）", font=font(23), fill="#587187")
    y = HEADER + 26
    for scene_id in TARGETS:
        for directory, x in ((V4_DIR, SIDE), (V5_DIR, SIDE + THUMB_SIZE[0] + GAP)):
            path = directory / f"scene_{scene_id:03d}.png"
            if not path.exists():
                raise FileNotFoundError(path)
            with Image.open(path) as source:
                thumb = ImageOps.fit(source.convert("RGB"), THUMB_SIZE, method=Image.Resampling.LANCZOS)
            sheet.paste(thumb, (x, y))
            draw.rectangle((x, y, x + THUMB_SIZE[0], y + THUMB_SIZE[1]), outline="#9db8cc", width=3)
        draw.text((SIDE, y + THUMB_SIZE[1] + 7), f"SCENE-{scene_id:03d}", font=font(22), fill="#2f74bb")
        y += row_height
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUTPUT, "PNG")
    print(f"saved {OUTPUT} {sheet.size[0]}x{sheet.size[1]}")


if __name__ == "__main__":
    main()
