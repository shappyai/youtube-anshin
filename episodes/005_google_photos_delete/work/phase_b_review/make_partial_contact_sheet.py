"""Build a review sheet even when a scene is intentionally missing an asset."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def get_font(size: int):
    for candidate in ("C:/Windows/Fonts/meiryo.ttc", "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def centered(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, font) -> None:
    bounds = draw.multiline_textbbox((0, 0), text, font=font, align="center")
    x = (box[0] + box[2] - (bounds[2] - bounds[0])) // 2
    y = (box[1] + box[3] - (bounds[3] - bounds[1])) // 2 - bounds[1]
    draw.multiline_text((x, y), text, font=font, fill="#815e1e", align="center", spacing=8)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rendered", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--count", type=int, default=25)
    args = parser.parse_args()
    rendered = args.rendered.resolve()
    output = args.output.resolve()
    columns, tile_w, tile_h, label_h = 5, 360, 240, 40
    rows = (args.count + columns - 1) // columns
    sheet = Image.new("RGB", (columns * tile_w + 40, rows * (tile_h + label_h) + 40), "#eef6fa")
    draw = ImageDraw.Draw(sheet)
    label_font = get_font(22)
    missing_font = get_font(25)
    for scene_id in range(1, args.count + 1):
        col = (scene_id - 1) % columns
        row = (scene_id - 1) // columns
        x = 20 + col * tile_w
        y = 20 + row * (tile_h + label_h)
        path = rendered / f"scene_{scene_id:03d}.png"
        if path.exists():
            with Image.open(path) as image:
                image = image.convert("RGB")
                image.thumbnail((tile_w - 12, tile_h - 12), Image.Resampling.LANCZOS)
                paste_x = x + (tile_w - image.width) // 2
                paste_y = y + (tile_h - image.height) // 2
                sheet.paste(image, (paste_x, paste_y))
        else:
            draw.rectangle((x, y, x + tile_w - 1, y + tile_h - 1), fill="#fff2d7", outline="#d3922e", width=3)
            centered(draw, (x + 10, y + 10, x + tile_w - 10, y + tile_h - 10), f"SCENE-{scene_id:03d}\n未取得\n人間確認待ち", missing_font)
        draw.rectangle((x, y + tile_h, x + tile_w - 1, y + tile_h + label_h - 1), fill="#ffffff")
        draw.text((x + 10, y + tile_h + 8), f"SCENE-{scene_id:03d}", font=label_font, fill="#173a68")
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, "PNG", optimize=False)
    print(f"saved={output} missing={sum(not (rendered / f'scene_{i:03d}.png').exists() for i in range(1, args.count + 1))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
