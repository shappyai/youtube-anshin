"""QA frame extraction for draft_v1.mp4 (scene midpoints + CTA).

Episode 004の`work/extract_qa_frames.py`と同一パターン。
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

FFMPEG = (
    Path(r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages")
    / "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    / "ffmpeg-8.1.1-full_build" / "bin" / "ffmpeg.exe"
)
BASE = Path(__file__).resolve().parent
EPISODE = BASE.parent
TARGETS = (1, 4, 6, 10, 12, 13, 16, 17, 18, 19, 22, 25)


def main() -> None:
    data = json.loads((EPISODE / "episode.json").read_text(encoding="utf-8"))
    timing = json.loads((BASE / "audio_timing.json").read_text(encoding="utf-8"))
    times = {int(row["segment_id"]): row for row in timing["segments"]}
    out_dir = BASE / "qa_frames"
    out_dir.mkdir(exist_ok=True)
    for scene in data["scenes"]:
        sid = int(scene["id"])
        if sid not in TARGETS:
            continue
        start = float(times[int(scene["start_segment"])]["start_sec"])
        row = times[int(scene["end_segment"])]
        end = float(row["end_sec"]) + float(row.get("pause_after") or 0)
        mid = (start + end) / 2.0
        out = out_dir / f"scene_{sid:03d}_frame.png"
        subprocess.run(
            [str(FFMPEG), "-y", "-ss", f"{mid:.3f}", "-i",
             str(EPISODE / "output" / "draft_v1.mp4"), "-frames:v", "1",
             "-q:v", "2", str(out)],
            check=True, capture_output=True,
        )
        print(f"scene {sid:03d} t={mid:.2f}s -> {out.name}")
    cta_mid = float(timing["duration"]) + 5.0
    out_cta = out_dir / "cta_frame.png"
    subprocess.run(
        [str(FFMPEG), "-y", "-ss", f"{cta_mid:.3f}", "-i",
         str(EPISODE / "output" / "draft_v1.mp4"), "-frames:v", "1",
         "-q:v", "2", str(out_cta)],
        check=True, capture_output=True,
    )
    print(f"CTA t={cta_mid:.2f}s -> {out_cta.name}")


if __name__ == "__main__":
    main()
