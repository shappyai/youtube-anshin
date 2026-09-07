"""Make a labeled contact sheet from draft representative frames."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

from scene_renderer import pil_font


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("frame_report", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    report = json.loads(args.frame_report.read_text(encoding="utf-8"))
    frames = report.get("frames") or []
    columns = 5
    thumb_w, thumb_h = 360, 203
    cell_w, cell_h = 390, 255
    rows = max(1, (len(frames) + columns - 1) // columns)
    sheet = Image.new("RGB", (columns * cell_w + 40, rows * cell_h + 40), "#eef6fa")
    draw = ImageDraw.Draw(sheet)
    label_font = pil_font(24)
    time_font = pil_font(18, bold=False)
    for index, item in enumerate(frames):
        x = 20 + (index % columns) * cell_w
        y = 20 + (index // columns) * cell_h
        path = Path(str(item["path"]))
        with Image.open(path) as source:
            thumb = ImageOps.fit(source.convert("RGB"), (thumb_w, thumb_h))
        sheet.paste(thumb, (x, y))
        draw.rectangle((x, y, x + thumb_w, y + thumb_h), outline="#c9d3dc", width=2)
        name = "CTA" if item.get("scene_id") is None else f"SCENE-{int(item['scene_id']):03d}"
        draw.text((x, y + thumb_h + 8), name, font=label_font, fill="#173a68")
        draw.text((x, y + thumb_h + 42), f"t={float(item['captured_sec']):.3f}s", font=time_font, fill="#587187")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output, "PNG")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
