"""Run the repository mechanical QA against the immutable final artifact."""
from __future__ import annotations

import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import phase2_qa as phase2_qa_module  # noqa: E402
from episode_io import apply_episode_defaults, load_json  # noqa: E402
from phase2_qa import run_qa  # noqa: E402


WORK = BASE / "work"
VENDOR_FFMPEG = ROOT / "work" / "vendor" / "imageio_ffmpeg" / "binaries" / "ffmpeg-win-x86_64-v7.1.exe"
if VENDOR_FFMPEG.exists():
    phase2_qa_module._ffmpeg_executable = lambda: str(VENDOR_FFMPEG)


def main() -> int:
    data = apply_episode_defaults(load_json(BASE / "episode.json"))
    final = BASE / "output" / "final.mp4"
    # phase2_qa derives the episode root as report_base.parent.parent; keep
    # the machine-generated report under work/ and copy it to output/review
    # after the episode-relative checks pass.
    report_base = WORK / "final_qa"
    qa = run_qa(
        data,
        WORK / "rendered_final_scenes",
        WORK / "audio_timing.json",
        final,
        report_base,
        BASE / "audio" / "voicevox_kenzaki" / "narration_kenzaki_auto.wav",
    )
    print(json.dumps({"status": qa["status"], "failures": qa["failures"], "warnings": qa["warnings"], "probe": qa["probe"]}, ensure_ascii=False, indent=2))
    return 0 if qa["status"] == "PASS" else 2 if qa["status"] == "WARN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
