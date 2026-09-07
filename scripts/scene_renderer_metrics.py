"""Measure raster-level layout proxies for the Phase 1.5 renderer review."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image

try:
    import numpy as np
except ImportError:  # pragma: no cover - bundled workspace runtime includes numpy
    np = None  # type: ignore[assignment]

WIDTH, HEIGHT, ACTIVE_HEIGHT = 1920, 1080, 900


def bbox(mask: Any) -> tuple[int, int, int, int] | None:
    ys, xs = mask.nonzero()
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)


def bands(mask: Any, min_row_pixels: int = 8) -> list[dict[str, int]]:
    row_counts = mask.sum(axis=1)
    rows = row_counts >= min_row_pixels
    groups: list[tuple[int, int]] = []
    start: int | None = None
    for index, active in enumerate(rows.tolist() + [False]):
        if active and start is None:
            start = index
        elif not active and start is not None:
            if index - start >= 2:
                groups.append((start, index))
            start = None
    result: list[dict[str, int]] = []
    for top, bottom in groups:
        region = mask[top:bottom]
        current_bbox = bbox(region)
        if current_bbox is None:
            continue
        left, _top, right, _bottom = current_bbox
        result.append(
            {
                "top": top,
                "bottom": bottom,
                "height": bottom - top,
                "left": left,
                "right": right,
                "width": right - left,
                "pixels": int(region.sum()),
            }
        )
    return result


def largest_coarse_component(mask: Any) -> tuple[int, tuple[int, int, int, int] | None]:
    height, width = mask.shape
    visited = set()
    best_area = 0
    best_box: tuple[int, int, int, int] | None = None
    for y in range(height):
        for x in range(width):
            if not mask[y, x] or (x, y) in visited:
                continue
            stack = [(x, y)]
            visited.add((x, y))
            points: list[tuple[int, int]] = []
            while stack:
                px, py = stack.pop()
                points.append((px, py))
                for nx in range(max(0, px - 1), min(width, px + 2)):
                    for ny in range(max(0, py - 1), min(height, py + 2)):
                        if mask[ny, nx] and (nx, ny) not in visited:
                            visited.add((nx, ny))
                            stack.append((nx, ny))
            if len(points) > best_area:
                best_area = len(points)
                xs = [point[0] for point in points]
                ys = [point[1] for point in points]
                best_box = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
    return best_area, best_box


def measure(path: Path) -> dict[str, Any]:
    if np is None:
        raise SystemExit("numpy is required for scene metrics")
    image = Image.open(path).convert("RGB")
    array = np.asarray(image)
    active = array[:ACTIVE_HEIGHT]
    luminance = active.mean(axis=2)
    spread = active.max(axis=2) - active.min(axis=2)
    dark = (active[:, :, 0] < 105) & (active[:, :, 1] < 155) & (active[:, :, 2] < 215)
    nonwhite = (active.min(axis=2) < 242) | (spread > 18)
    color = (spread > 22) & (active.mean(axis=2) < 248)
    dark_bands = bands(dark)
    headline_bands = [
        band for band in dark_bands
        if 50 <= band["top"] < 620 and band["pixels"] >= 60
    ]
    headline_candidates = [
        band for band in dark_bands
        if 70 <= band["top"] < 420
        and band["height"] >= 35
        and band["width"] >= 250
        and band["pixels"] >= 500
    ]
    headline_first = min(
        headline_candidates,
        key=lambda band: band["top"],
        default={"height": 0, "width": 0, "left": 0, "right": 0, "top": 0, "bottom": 0, "pixels": 0},
    )
    headline = max(
        headline_bands,
        key=lambda band: (band["width"] * band["height"], band["pixels"]),
        default={"height": 0, "width": 0, "left": 0, "right": 0, "top": 0, "bottom": 0, "pixels": 0},
    )
    coarse_h, coarse_w = 90, 120
    coarse_color = color.reshape(coarse_h, ACTIVE_HEIGHT // coarse_h, coarse_w, WIDTH // coarse_w).mean(axis=(1, 3)) > 0.12
    component_area, component_box = largest_coarse_component(coarse_color)
    current_bbox = bbox(nonwhite)
    return {
        "path": str(path),
        "width": int(image.width),
        "height": int(image.height),
        "dark_area_ratio": round(float(dark.mean()), 5),
        "color_area_ratio": round(float(color.mean()), 5),
        "active_nonwhite_ratio": round(float(nonwhite.mean()), 5),
        "active_bbox": current_bbox,
        "active_bbox_area_ratio": round(
            ((current_bbox[2] - current_bbox[0]) * (current_bbox[3] - current_bbox[1]) / (WIDTH * ACTIVE_HEIGHT))
            if current_bbox else 0,
            5,
        ),
        "headline_band_height_px": int(headline["height"]),
        "headline_band_width_px": int(headline["width"]),
        "headline_width_ratio": round(float(headline["width"] / WIDTH), 5),
        "headline_raster_height_px": int(headline_first["height"]),
        "headline_raster_width_px": int(headline_first["width"]),
        "headline_raster_top_px": int(headline_first["top"]),
        "headline_band_count": len(headline_bands),
        "small_dark_band_count": sum(1 for band in dark_bands if band["height"] <= 20 and band["pixels"] >= 20),
        "largest_color_component_area_ratio": round(float(component_area / (coarse_h * coarse_w)), 5),
        "largest_color_component_box": component_box,
    }


def scene_paths(folder: Path) -> list[Path]:
    return sorted(folder.glob("scene_[0-9][0-9][0-9].png"))


def summarize(rows: list[dict[str, Any]]) -> dict[str, float]:
    keys = (
        "dark_area_ratio",
        "color_area_ratio",
        "active_nonwhite_ratio",
        "active_bbox_area_ratio",
        "headline_band_height_px",
        "headline_band_width_px",
        "headline_width_ratio",
        "headline_raster_height_px",
        "headline_raster_width_px",
        "headline_raster_top_px",
        "headline_band_count",
        "small_dark_band_count",
        "largest_color_component_area_ratio",
    )
    return {key: round(sum(float(row[key]) for row in rows) / len(rows), 5) for key in keys} if rows else {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--teacher-dir", type=Path, required=True)
    parser.add_argument("--auto-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    teacher = [measure(path) for path in scene_paths(args.teacher_dir)]
    auto = [measure(path) for path in scene_paths(args.auto_dir)]
    result = {
        "teacher_count": len(teacher),
        "auto_count": len(auto),
        "teacher_summary": summarize(teacher),
        "auto_summary": summarize(auto),
        "teacher": teacher,
        "auto": auto,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"teacher_count": len(teacher), "auto_count": len(auto), "teacher_summary": result["teacher_summary"], "auto_summary": result["auto_summary"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
