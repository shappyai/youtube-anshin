"""Extract the required Episode 009 draft review frames with vendor FFmpeg."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
from extract_draft_frames import scene_targets  # noqa: E402

FFMPEG = ROOT / "work" / "vendor" / "imageio_ffmpeg" / "binaries" / "ffmpeg-win-x86_64-v7.1.exe"
EP = ROOT / "episodes" / "009_windows11_24h2_support"
REQUIRED = {
    "scene_001", "scene_002", "scene_003", "scene_004", "scene_006", "scene_007",
    "scene_008", "scene_009", "scene_010", "scene_011", "scene_012", "scene_013",
    "scene_015", "scene_017", "scene_018", "scene_019", "cta",
}


def main() -> int:
    video = EP / "output" / "draft_v1.mp4"
    timing = EP / "work" / "audio_timing.json"
    output_dir = EP / "work" / "qa_frames_draft_v1"
    output_dir.mkdir(parents=True, exist_ok=True)
    targets = [item for item in scene_targets(EP / "episode.json", timing) if item["name"] in REQUIRED]
    results = []
    for item in sorted(targets, key=lambda value: float(value["target_sec"])):
        output = output_dir / f"{item['name']}.png"
        command = [
            str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y",
            "-ss", f"{float(item['target_sec']):.3f}", "-i", str(video),
            "-frames:v", "1", str(output),
        ]
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
        if completed.returncode or not output.exists():
            raise RuntimeError(f"frame extraction failed for {item['name']}: {completed.stderr.strip()}")
        results.append({
            **item,
            "captured_sec": round(float(item["target_sec"]), 3),
            "path": str(output),
            "width": 1920,
            "height": 1080,
        })
    report = output_dir.parent / "qa_frames_draft_v1.json"
    report.write_text(json.dumps({"video": str(video), "frames": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "frame_count": len(results), "report": str(report)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
