"""Build Episode 011 draft_v2 from the v2 scene, changed narration, and reused assets."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_subtitle_cue_timing import build_measurements  # noqa: E402
from build_subtitle_timeline import build_from_files  # noqa: E402
from episode_io import apply_episode_defaults, load_json  # noqa: E402
import phase2_qa as phase2_qa_module  # noqa: E402
import phase2_video as phase2_video_module  # noqa: E402
from phase2_qa import run_qa  # noqa: E402
from phase2_video import build_video  # noqa: E402
from voicevox_incremental import generate_incremental, wav_duration  # noqa: E402


BASE = ROOT / "episodes" / "011_myna_insurance_scam_call"
WORK = BASE / "work"
V2_WORK = WORK / "draft_v2_build"
ENGINE = "http://127.0.0.1:50021"
CTA_CONFIG = WORK / "cta_registration_conversion_v1.json"
CTA_SCREEN = WORK / "cta_registration_conversion_v1.png"
CTA_AUDIO = BASE / "audio" / "voicevox_kenzaki" / "cta_registration_conversion_v1.wav"
VENDOR_FFMPEG = ROOT / "work" / "vendor" / "imageio_ffmpeg" / "binaries" / "ffmpeg-win-x86_64-v7.1.exe"


if VENDOR_FFMPEG.exists():
    phase2_video_module._ffmpeg_executable = lambda: str(VENDOR_FFMPEG)
    phase2_qa_module._ffmpeg_executable = lambda: str(VENDOR_FFMPEG)


def main() -> int:
    data = apply_episode_defaults(load_json(BASE / "episode.json"))
    V2_WORK.mkdir(parents=True, exist_ok=True)
    audio_dir = BASE / "audio" / "voicevox_kenzaki"

    voice = generate_incremental(data, BASE, WORK, ENGINE, audio_dir=audio_dir)
    timing = WORK / "audio_timing.json"

    cue_timing = build_measurements(data, ENGINE, "剣崎雌雄", "ノーマル")
    cue_timing_path = V2_WORK / "subtitle_cue_timing.json"
    cue_timing_path.write_text(json.dumps(cue_timing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    srt = V2_WORK / "captions_auto.srt"
    ass = V2_WORK / "captions_auto.ass"
    build_from_files(data, timing, srt, ass, cue_timing_path)
    shutil.copy2(srt, BASE / "captions.srt")
    shutil.copy2(ass, BASE / "captions.ass")

    draft = BASE / "output" / "draft_v2.mp4"
    if draft.exists():
        raise SystemExit(f"STOP: draft already exists: {draft}")
    cta_duration = wav_duration(CTA_AUDIO)
    declared_postroll = float((data.get("postroll") or {}).get("duration_sec") or 0.0)
    cta_trailing = max(0.0, declared_postroll - cta_duration)
    video = build_video(
        data,
        WORK / "rendered_final_scenes",
        timing,
        audio_dir / "narration_kenzaki_auto.wav",
        ass,
        V2_WORK,
        draft,
        cta_audio_path=CTA_AUDIO,
        cta_trailing=cta_trailing,
    )
    if video.get("status") != "PASS":
        raise SystemExit("STOP: " + "; ".join(video.get("errors", [])))
    qa = run_qa(
        data,
        WORK / "rendered_final_scenes",
        timing,
        draft,
        WORK / "draft_v2_qa",
        audio_dir / "narration_kenzaki_auto.wav",
    )
    result = {
        "status": qa["status"],
        "image": {
            "scene": "SCENE-018",
            "text_render_mode": "imagegen_native",
            "post_text_overlay": 0,
            "text_qa": "PASS",
        },
        "voice": {
            "planned": voice.get("planned", []),
            "skipped": voice.get("skipped", []),
            "segment_count": len(voice.get("rows", [])),
            "duration": voice.get("duration"),
        },
        "cta": {
            "config": str(CTA_CONFIG),
            "screen": str(CTA_SCREEN),
            "audio": str(CTA_AUDIO),
            "duration": round(cta_duration, 3),
            "trailing": round(cta_trailing, 3),
            "declared_postroll": round(declared_postroll, 3),
            "canonical_text": (load_json(CTA_CONFIG)).get("canonical_text"),
        },
        "subtitles": {
            "srt": str(BASE / "captions.srt"),
            "ass": str(BASE / "captions.ass"),
            "cue_count": len(data.get("subtitles", [])),
        },
        "video": video,
        "qa": qa,
    }
    (WORK / "phase_b_v2_build_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if qa["status"] == "PASS" else 2 if qa["status"] == "WARN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
