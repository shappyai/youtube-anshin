"""Compare teacher base frames, the Phase 1 renderer, and final review frames."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image

try:
    import numpy as np
except ImportError:  # pragma: no cover - bundled workspace runtime includes numpy
    np = None  # type: ignore[assignment]

from scene_renderer_metrics import measure


def changed_metrics(base_path: Path, final_path: Path, threshold: int = 14) -> dict[str, Any]:
    if np is None:
        raise SystemExit("numpy is required for comparison metrics")
    base = np.asarray(Image.open(base_path).convert("RGB"))[:900].astype("int16")
    final = np.asarray(Image.open(final_path).convert("RGB"))[:900].astype("int16")
    diff = np.max(np.abs(base - final), axis=2)
    changed = diff >= threshold
    ys, xs = changed.nonzero()
    current_bbox = None
    if len(xs):
        current_bbox = [int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)]
    return {
        "threshold": threshold,
        "changed_ratio": round(float(changed.mean()), 5),
        "changed_bbox": current_bbox,
        "changed_bbox_area_ratio": round(
            float(((current_bbox[2] - current_bbox[0]) * (current_bbox[3] - current_bbox[1])) / (1920 * 900))
            if current_bbox else 0,
            5,
        ),
    }


def composite_area(scene_no: int, build_video_module: Any) -> dict[str, Any]:
    boxes = [spec[0] for spec in build_video_module.COMPOSITES.get(scene_no, [])]
    area = sum(max(0, box[2] - box[0]) * max(0, box[3] - box[1]) for box in boxes)
    return {
        "boxes": boxes,
        "area_px": area,
        "area_ratio_full_frame": round(area / (1920 * 1080), 5),
        "area_ratio_active_frame": round(area / (1920 * 900), 5),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--teacher-dir", type=Path, required=True)
    parser.add_argument("--auto-dir", type=Path, required=True)
    parser.add_argument("--final-dir", type=Path, required=True)
    parser.add_argument("--episode-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scenes", nargs="+", type=int, default=[1, 3, 5, 10, 14, 22, 27, 32])
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    work_dir = args.episode_dir / "work"
    if str(work_dir) not in sys.path:
        sys.path.insert(0, str(work_dir))
    import build_video_v2 as build_video  # noqa: E402

    episode = json.loads((args.episode_dir / "episode.json").read_text(encoding="utf-8"))
    scenes = {int(scene["id"]): scene for scene in episode["scenes"]}
    rows: list[dict[str, Any]] = []
    for scene_no in args.scenes:
        teacher = args.teacher_dir / f"scene_{scene_no:03d}.png"
        auto = args.auto_dir / f"scene_{scene_no:03d}.png"
        final = args.final_dir / f"frame_scene_{scene_no:03d}.png"
        if not (teacher.exists() and auto.exists() and final.exists()):
            rows.append({"scene_id": scene_no, "missing": True})
            continue
        rows.append(
            {
                "scene_id": scene_no,
                "layout": scenes.get(scene_no, {}).get("layout"),
                "teacher": measure(teacher),
                "auto": measure(auto),
                "final_vs_teacher_base": changed_metrics(teacher, final),
                "teacher_composite_reference": composite_area(scene_no, build_video),
            }
        )
    result = {
        "method": {
            "teacher": "assets/generated_scenes raster before final-video compositing",
            "auto": f"{args.auto_dir} raster from the renderer under comparison",
            "final": "output/review_frames_v4/frame_scene_###.png",
            "changed_threshold": 14,
            "active_height": 900,
            "note": "Teacher composite reference boxes are the existing Phase 1 final-video compositor geometry; changed pixels include official overlays and any final-frame additions.",
        },
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
