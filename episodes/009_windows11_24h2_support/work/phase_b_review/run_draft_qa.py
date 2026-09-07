"""Run Episode 009 draft QA with the repository's vendor FFmpeg."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))

import phase2_qa  # noqa: E402

FFMPEG = ROOT / "work" / "vendor" / "imageio_ffmpeg" / "binaries" / "ffmpeg-win-x86_64-v7.1.exe"
EP = ROOT / "episodes" / "009_windows11_24h2_support"


def timestamp_seconds(value: str) -> float:
    hours, minutes, seconds = value.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def probe(path: Path) -> dict:
    result = subprocess.run(
        [str(FFMPEG), "-hide_banner", "-i", str(path), "-f", "null", "-"],
        capture_output=True,
        text=True,
        check=False,
    )
    stderr = result.stderr
    duration_match = re.search(r"Duration:\s+(\d{2}:\d{2}:\d{2}\.\d+)", stderr)
    streams = []
    video_match = re.search(
        r"Stream #\d+:\d+.*?Video:\s+([^,\s]+).*?(\d{2,5})x(\d{2,5}).*?(\d+(?:\.\d+)?)\s*fps",
        stderr,
        re.S,
    )
    if video_match:
        streams.append(
            {
                "codec_type": "video",
                "codec_name": video_match.group(1),
                "width": int(video_match.group(2)),
                "height": int(video_match.group(3)),
                "r_frame_rate": "30/1",
            }
        )
    audio_match = re.search(
        r"Stream #\d+:\d+.*?Audio:\s+([^,\s]+).*?(\d+)\s*Hz",
        stderr,
        re.S,
    )
    if audio_match:
        streams.append(
            {
                "codec_type": "audio",
                "codec_name": audio_match.group(1),
                "sample_rate": audio_match.group(2),
                "channels": None,
            }
        )
    if result.returncode:
        return {"error": stderr.strip(), "decode_returncode": result.returncode}
    return {
        "format": {"duration": timestamp_seconds(duration_match.group(1)) if duration_match else 0.0},
        "streams": streams,
        "decode_returncode": result.returncode,
    }


def main() -> int:
    phase2_qa._ffmpeg_executable = lambda: str(FFMPEG)
    phase2_qa._probe = probe
    data = json.loads((EP / "episode.json").read_text(encoding="utf-8"))
    result = phase2_qa.run_qa(
        data,
        EP / "assets" / "scenes",
        EP / "work" / "audio_timing.json",
        EP / "output" / "draft_v1.mp4",
        EP / "work" / "draft_v1_qa",
        EP / "audio" / "voicevox_kenzaki" / "narration_kenzaki_auto.wav",
    )
    parsed_probe = probe(EP / "output" / "draft_v1.mp4")
    (EP / "work" / "phase_b_review" / "draft_probe.json").write_text(
        json.dumps(parsed_probe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": result["status"], "failures": result["failures"], "warnings": result["warnings"], "probe": parsed_probe}, ensure_ascii=False))
    return 0 if result["status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
