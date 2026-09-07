"""Normalize Phase B still assets and build review contact sheets."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1920
HEIGHT = 1080


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize(source: Path, destination: Path) -> dict[str, object]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image.load()
        original_size = image.size
        normalized = image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        normalized.save(destination, "PNG", optimize=False)
    return {
        "source": str(source),
        "destination": str(destination),
        "original_size": original_size,
        "size": (WIDTH, HEIGHT),
        "bytes": destination.stat().st_size,
        "sha256": sha256(destination),
    }


def font(size: int):
    candidates = [
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/meiryo.ttc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            try:
                return ImageFont.truetype(str(candidate), size)
            except OSError:
                continue
    return ImageFont.load_default()


def contact_sheet(paths: list[Path], output: Path, title: str) -> None:
    columns = 2 if len(paths) > 1 else 1
    tile_width = 960
    tile_height = 600
    header_height = 72
    rows = (len(paths) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * tile_width, header_height + rows * tile_height), "#eef3f5")
    draw = ImageDraw.Draw(sheet)
    draw.text((28, 20), title, fill="#173a68", font=font(32))
    for index, path in enumerate(paths):
        col = index % columns
        row = index // columns
        left = col * tile_width
        top = header_height + row * tile_height
        draw.rectangle((left + 12, top + 12, left + tile_width - 12, top + tile_height - 12), fill="#ffffff", outline="#c8d6dc", width=2)
        with Image.open(path) as image:
            image = image.convert("RGB")
            image.thumbnail((tile_width - 36, tile_height - 84), Image.Resampling.LANCZOS)
            x = left + (tile_width - image.width) // 2
            y = top + 22 + (tile_height - 84 - image.height) // 2
            sheet.paste(image, (x, y))
        draw.text((left + 28, top + tile_height - 52), path.stem, fill="#173a68", font=font(26))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, "PNG", optimize=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode-dir", type=Path, required=True)
    parser.add_argument("--review-dir", type=Path, required=True)
    args = parser.parse_args()

    episode_dir = args.episode_dir.resolve()
    review_dir = args.review_dir.resolve()
    source_dir = episode_dir / "assets" / "generated_ai"
    normalized_dir = review_dir / "normalized_ai"
    sources = sorted(source_dir.glob("scene_*.png"))
    records = []
    normalized = []
    for source in sources:
        destination = normalized_dir / source.name
        records.append(normalize(source, destination))
        normalized.append(destination)
    contact_sheet(normalized, review_dir / "gpt_image_contact_sheet.png", "Episode 005 GPT image scenes")
    for record in records:
        print(record)
    print(f"normalized={len(normalized)}")
    print(f"contact_sheet={review_dir / 'gpt_image_contact_sheet.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
