"""Create readable crops from portrait Android emulator captures."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


# Boxes are deliberately conservative: they retain the real UI while removing
# most status/navigation chrome so the official slot stays readable in 1080p.
BOXES = {
    "backup_status_item.png": (0, 1550, 1080, 2150),
    "delete_photo_trash.png": (0, 1830, 1080, 2424),
    "trash_days.png": (0, 1000, 1080, 1607),
    "delete_from_device.png": (0, 620, 1080, 1227),
    "free_up_space.png": (0, 520, 1080, 1127),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    directory = args.directory.resolve()
    for source_name, box in BOXES.items():
        source = directory / source_name
        if not source.exists():
            print(f"skip missing: {source_name}")
            continue
        destination = directory / source_name.replace(".png", "_crop.png")
        with Image.open(source) as image:
            bounded = (
                max(0, box[0]),
                max(0, box[1]),
                min(image.width, box[2]),
                min(image.height, box[3]),
            )
            image.crop(bounded).convert("RGB").save(destination, "PNG", optimize=False)
        print(f"{destination}: {bounded} {destination.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
