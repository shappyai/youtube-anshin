"""Create fixed crops from saved official-page screenshots for scene review."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


BOXES = {
    "apple_guide_delete_photos_viewport.png": (220, 100, 1220, 663),
    "google_photos_delete_ios_viewport.png": (100, 145, 1000, 651),
    "apple_recently_deleted_viewport.png": (250, 190, 1250, 753),
    # Google公式ヘルプの該当手順だけを残し、ヘッダー・右サイドバーを除去。
    "google_photos_backup_android_viewport.png": (170, 295, 960, 575),
    "google_photos_restore_android_steps_viewport.png": (128, 210, 960, 570),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    directory = args.directory.resolve()
    for source_name, box in BOXES.items():
        source = directory / source_name
        destination = directory / source_name.replace("_viewport.png", "_crop.png")
        with Image.open(source) as image:
            image.crop(box).convert("RGB").save(destination, "PNG", optimize=False)
        print(f"{destination}: {box} {destination.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
