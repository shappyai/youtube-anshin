"""Normalize the ImageGen-native SCENE-018 source to the project 16:9 canvas.

This performs only a cover crop and LANCZOS resize. It never draws or edits text.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work" / "imagegen_raw" / "scene_018_v2_native_source.png"
OUTPUT = ROOT / "assets" / "generated_ai" / "scene_018.png"
TARGET_SIZE = (1920, 1080)


def main() -> None:
    with Image.open(SOURCE) as image:
        image = image.convert("RGB")
        target_ratio = TARGET_SIZE[0] / TARGET_SIZE[1]
        source_ratio = image.width / image.height
        if source_ratio > target_ratio:
            crop_width = round(image.height * target_ratio)
            left = (image.width - crop_width) // 2
            box = (left, 0, left + crop_width, image.height)
        else:
            crop_height = round(image.width / target_ratio)
            top = (image.height - crop_height) // 2
            box = (0, top, image.width, top + crop_height)
        normalized = image.crop(box).resize(TARGET_SIZE, Image.Resampling.LANCZOS)
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        normalized.save(OUTPUT, format="PNG", optimize=True)
        print({"source": str(SOURCE), "source_size": image.size, "crop": box, "output": str(OUTPUT), "output_size": normalized.size})


if __name__ == "__main__":
    main()
