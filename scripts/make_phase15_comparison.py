"""Build a side-by-side teacher/new-renderer comparison image."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

from scene_renderer import pil_font


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--teacher-dir", type=Path, required=True)
    parser.add_argument("--new-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scenes", nargs="+", type=int, default=[1, 3, 5, 10, 14, 22, 27, 32])
    args = parser.parse_args()

    thumb_w, thumb_h = 620, 349
    margin = 24
    gap = 24
    label_h = 38
    row_h = label_h + thumb_h + 34
    width = margin * 2 + thumb_w * 2 + gap
    height = margin * 2 + row_h * len(args.scenes)
    sheet = Image.new("RGB", (width, height), "#edf5f9")
    draw = ImageDraw.Draw(sheet)
    label_font = pil_font(25)
    note_font = pil_font(19)

    for index, scene_no in enumerate(args.scenes):
        y = margin + index * row_h
        left_x = margin
        right_x = margin + thumb_w + gap
        teacher_path = args.teacher_dir / f"frame_scene_{scene_no:03d}.png"
        new_path = args.new_dir / f"scene_{scene_no:03d}.png"
        draw.text((left_x, y), f"SCENE-{scene_no:03d}  教師データ（公開候補フレーム）", font=label_font, fill="#173a68")
        draw.text((right_x, y), f"SCENE-{scene_no:03d}  Phase 1.5 renderer", font=label_font, fill="#173a68")
        for path, x in ((teacher_path, left_x), (new_path, right_x)):
            if path.exists():
                with Image.open(path) as source:
                    thumb = ImageOps.fit(source.convert("RGB"), (thumb_w, thumb_h))
            else:
                thumb = Image.new("RGB", (thumb_w, thumb_h), "#fff2d7")
                ImageDraw.Draw(thumb).text((24, 24), f"missing: {path.name}", font=note_font, fill="#815e1e")
            sheet.paste(thumb, (x, y + label_h))
            draw.rectangle((x, y + label_h, x + thumb_w, y + label_h + thumb_h), outline="#c9d3dc", width=2)
        draw.line((margin, y + row_h - 15, width - margin, y + row_h - 15), fill="#d3e3ed", width=2)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output, "PNG")
    print(f"created={args.output} scenes={len(args.scenes)} size={width}x{height}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
