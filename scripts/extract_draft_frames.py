"""Extract representative frames from a draft using PyAV timestamps."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def scene_targets(episode_path: Path, timing_path: Path) -> list[dict[str, Any]]:
    data = json.loads(episode_path.read_text(encoding="utf-8"))
    timing = json.loads(timing_path.read_text(encoding="utf-8"))
    by_id = {int(row["segment_id"]): row for row in timing.get("segments", [])}
    targets: list[dict[str, Any]] = []
    for scene in data.get("scenes", []):
        start = float(by_id[int(scene["start_segment"])] ["start_sec"])
        end_row = by_id[int(scene["end_segment"])]
        end = float(end_row["end_sec"]) + float(end_row.get("pause_after") or 0.0)
        targets.append({
            "name": f"scene_{int(scene['id']):03d}",
            "scene_id": int(scene["id"]),
            "target_sec": round((start + end) / 2.0, 3),
        })
    main_duration = float(timing.get("duration") or 0.0)
    postroll = data.get("postroll") or {}
    postroll_duration = float(postroll.get("duration_sec") or 0.0)
    if postroll_duration > 0:
        targets.append({
            "name": "cta",
            "scene_id": None,
            "target_sec": round(main_duration + postroll_duration / 2.0, 3),
        })
    return targets


def extract(video_path: Path, output_dir: Path, targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    import av

    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    ordered = sorted(targets, key=lambda row: float(row["target_sec"]))
    with av.open(str(video_path)) as container:
        stream = container.streams.video[0]
        stream.thread_type = "AUTO"
        frames = iter(container.decode(stream))
        current = next(frames, None)
        for target in ordered:
            target_sec = float(target["target_sec"])
            while current is not None and float(current.time or 0.0) < target_sec:
                current = next(frames, None)
            if current is None:
                raise RuntimeError(f"video ended before target {target['name']}: {target_sec:.3f}s")
            output = output_dir / f"{target['name']}.png"
            current.to_image().convert("RGB").save(output, "PNG")
            results.append({
                **target,
                "captured_sec": round(float(current.time or 0.0), 3),
                "path": str(output),
                "width": int(current.width),
                "height": int(current.height),
            })
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("episode", type=Path)
    parser.add_argument("timing", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    targets = scene_targets(args.episode.resolve(), args.timing.resolve())
    results = extract(args.video.resolve(), args.output_dir.resolve(), targets)
    report = args.output_dir.resolve().parent / "qa_frames_draft_v1.json"
    report.write_text(json.dumps({"video": str(args.video.resolve()), "frames": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "frame_count": len(results), "report": str(report)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
