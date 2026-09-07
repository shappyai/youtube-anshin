"""Extract Episode 011 draft frames with the pinned FFmpeg binary."""
from __future__ import annotations

import json
import argparse
import subprocess
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from extract_draft_frames import scene_targets  # noqa: E402


FFMPEG = ROOT / "work" / "vendor" / "imageio_ffmpeg" / "binaries" / "ffmpeg-win-x86_64-v7.1.exe"
BASE = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=Path, default=BASE / "output" / "draft_v1.mp4")
    parser.add_argument("--output-dir", type=Path, default=BASE / "work" / "qa_frames_draft_v1")
    parser.add_argument("--report", type=Path, default=BASE / "work" / "qa_frames_draft_v1.json")
    args = parser.parse_args()
    video = args.video if args.video.is_absolute() else BASE / args.video
    timing = BASE / "work" / "audio_timing.json"
    output_dir = args.output_dir if args.output_dir.is_absolute() else BASE / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    targets = scene_targets(BASE / "episode.json", timing)
    frames: list[dict] = []
    for target in targets:
        output = output_dir / f"{target['name']}.png"
        command = [
            str(FFMPEG), "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{float(target['target_sec']):.3f}", "-i", str(video),
            "-frames:v", "1", "-an", str(output),
        ]
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        if result.returncode or not output.exists():
            raise SystemExit(f"frame extraction failed for {target['name']}: {result.stderr.strip()}")
        from PIL import Image

        with Image.open(output) as image:
            width, height = image.size
        frames.append({
            **target,
            "captured_sec": float(target["target_sec"]),
            "path": str(output),
            "width": width,
            "height": height,
            "method": "ffmpeg_seek_single_frame",
        })
    report = args.report if args.report.is_absolute() else BASE / args.report
    report.write_text(
        json.dumps({"video": str(video), "frames": frames}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "PASS", "frame_count": len(frames), "report": str(report)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
