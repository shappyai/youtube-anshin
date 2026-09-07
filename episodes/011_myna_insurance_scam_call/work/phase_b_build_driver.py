"""Episode 011 Phase B driver: VOICEVOX, measured captions, CTA, draft, QA."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

# Use the project-pinned WinGet FFmpeg when it is available; phase2_video also
# has imageio-ffmpeg as a fallback.
FFMPEG_BIN = (
    Path(r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages")
    / "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    / "ffmpeg-8.1.1-full_build"
    / "bin"
)
try:
    if FFMPEG_BIN.exists():
        os.environ["PATH"] = str(FFMPEG_BIN) + os.pathsep + os.environ.get("PATH", "")
except PermissionError:
    # The bundled imageio-ffmpeg fallback may still be available.
    pass

from build_subtitle_cue_timing import build_measurements  # noqa: E402
from build_subtitle_timeline import build_from_files  # noqa: E402
from create_channel_cta import build_cta, load_config, synthesize_cta_audio  # noqa: E402
from episode_io import apply_episode_defaults, load_json  # noqa: E402
import phase2_qa as phase2_qa_module  # noqa: E402
import phase2_video as phase2_video_module  # noqa: E402
from phase2_qa import run_qa  # noqa: E402
from phase2_video import build_video  # noqa: E402
from voicevox_incremental import generate_incremental, wav_duration  # noqa: E402


BASE = ROOT / "episodes" / "011_myna_insurance_scam_call"
ENGINE = "http://127.0.0.1:50021"
CTA_CONFIG = BASE / "work" / "cta_registration_conversion_v1.json"
CTA_SCREEN = BASE / "work" / "cta_registration_conversion_v1.png"
CTA_AUDIO = BASE / "audio" / "voicevox_kenzaki" / "cta_registration_conversion_v1.wav"
VENDOR_FFMPEG = ROOT / "work" / "vendor" / "imageio_ffmpeg" / "binaries" / "ffmpeg-win-x86_64-v7.1.exe"

# The project vendor keeps a versioned filename, so expose it directly to the
# existing video/QA modules instead of copying or renaming the binary.
if VENDOR_FFMPEG.exists():
    phase2_video_module._ffmpeg_executable = lambda: str(VENDOR_FFMPEG)
    phase2_qa_module._ffmpeg_executable = lambda: str(VENDOR_FFMPEG)


def _vendor_probe(path: Path) -> dict:
    """Probe the draft with the project-pinned FFmpeg when ffprobe/PyAV are unavailable."""
    if not VENDOR_FFMPEG.exists() or not path.exists():
        return {}
    result = subprocess.run(
        [str(VENDOR_FFMPEG), "-hide_banner", "-i", str(path), "-f", "null", "-"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    raw = result.stderr
    duration_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", raw)
    video_match = re.search(
        r"Video:\s*([^,\s]+).*?(\d{2,5})x(\d{2,5}).*?(\d+(?:\.\d+)?)\s*fps",
        raw,
        flags=re.S,
    )
    audio_match = re.search(
        r"Audio:\s*([^,\s]+).*?(\d+)\s*Hz(?:,\s*([^,\r\n]+))?",
        raw,
    )
    if not duration_match or not video_match:
        return {"error": "vendor FFmpeg probe could not parse the draft metadata"}
    hours, minutes, seconds = duration_match.groups()
    duration = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    video_codec, width, height, fps = video_match.groups()
    streams = [{
        "codec_type": "video",
        "codec_name": video_codec,
        "width": int(width),
        "height": int(height),
        "r_frame_rate": f"{round(float(fps))}/1",
    }]
    if audio_match:
        audio_codec, sample_rate, channel_text = audio_match.groups()
        channels = 2 if "stereo" in (channel_text or "").lower() else 1
        streams.append({
            "codec_type": "audio",
            "codec_name": audio_codec,
            "sample_rate": int(sample_rate),
            "channels": channels,
        })
    return {"format": {"duration": duration}, "streams": streams}


# phase2_qa normally uses ffprobe or PyAV. This workspace intentionally keeps
# only the pinned FFmpeg binary, so use the local parser for reproducible QA.
if VENDOR_FFMPEG.exists():
    phase2_qa_module._probe = _vendor_probe


def main() -> int:
    data = apply_episode_defaults(load_json(BASE / "episode.json"))
    work = BASE / "work"
    audio_dir = BASE / "audio" / "voicevox_kenzaki"
    work.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)

    if "--qa-only" in sys.argv:
        draft = BASE / "output" / "draft_v1.mp4"
        audio = audio_dir / "narration_kenzaki_auto.wav"
        qa = run_qa(
            data,
            work / "rendered_final_scenes",
            work / "audio_timing.json",
            draft,
            work / "draft_v1_qa",
            audio,
        )
        result_path = work / "phase_b_qa_only_result.json"
        result_path.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(qa, ensure_ascii=False, indent=2))
        return 0 if qa["status"] == "PASS" else 2 if qa["status"] == "WARN" else 1

    if "--regen-midroll" in sys.argv:
        voice = generate_incremental(
            data,
            BASE,
            work,
            ENGINE,
            force_segment=13,
            audio_dir=audio_dir,
        )
        print(json.dumps({
            "status": voice.get("status"),
            "regenerated_segment": 13,
            "planned": voice.get("planned", []),
            "skipped": voice.get("skipped", []),
            "duration": voice.get("duration"),
        }, ensure_ascii=False, indent=2))
        return 0

    if "--subtitles-only" in sys.argv:
        timing = work / "audio_timing.json"
        cue_timing = build_measurements(data, ENGINE, "剣崎雌雄", "ノーマル")
        (work / "subtitle_cue_timing.json").write_text(
            json.dumps(cue_timing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        srt = work / "captions_auto.srt"
        ass = work / "captions_auto.ass"
        build_from_files(data, timing, srt, ass, work / "subtitle_cue_timing.json")
        shutil.copy2(srt, BASE / "captions.srt")
        shutil.copy2(ass, BASE / "captions.ass")
        print(json.dumps({
            "status": "PASS",
            "srt": str(BASE / "captions.srt"),
            "ass": str(BASE / "captions.ass"),
            "cue_count": len(data.get("subtitles", [])),
        }, ensure_ascii=False, indent=2))
        return 0

    # Keep the copied Episode 010 asset if present; regenerate only when the
    # local exact-config asset is missing.
    if not CTA_SCREEN.exists():
        build_cta(config_path=CTA_CONFIG, output_path=CTA_SCREEN)
    cta_config = load_config(CTA_CONFIG)
    if not CTA_AUDIO.exists():
        synthesize_cta_audio(config_path=CTA_CONFIG, engine_url=ENGINE, output_path=CTA_AUDIO)
    cta_duration = wav_duration(CTA_AUDIO)
    postroll = data.get("postroll") or {}
    declared_postroll = float(postroll.get("duration_sec") or 0.0)
    cta_trailing = max(0.0, declared_postroll - cta_duration)

    voice = generate_incremental(data, BASE, work, ENGINE, audio_dir=audio_dir)
    timing = work / "audio_timing.json"

    # Split-cue weights are measured from the same VOICEVOX engine; segment
    # boundaries still come from the synthesized segment WAVs.
    cue_timing = build_measurements(data, ENGINE, "剣崎雌雄", "ノーマル")
    (work / "subtitle_cue_timing.json").write_text(
        json.dumps(cue_timing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    srt = work / "captions_auto.srt"
    ass = work / "captions_auto.ass"
    build_from_files(data, timing, srt, ass, work / "subtitle_cue_timing.json")
    shutil.copy2(srt, BASE / "captions.srt")
    shutil.copy2(ass, BASE / "captions.ass")

    draft = BASE / "output" / "draft_v1.mp4"
    if draft.exists():
        raise SystemExit(f"STOP: draft already exists: {draft}")
    audio = audio_dir / "narration_kenzaki_auto.wav"
    video = build_video(
        data,
        work / "rendered_final_scenes",
        timing,
        audio,
        ass,
        work,
        draft,
        cta_audio_path=CTA_AUDIO,
        cta_trailing=cta_trailing,
    )
    if video.get("status") != "PASS":
        raise SystemExit("STOP: " + "; ".join(video.get("errors", [])))

    qa = run_qa(
        data,
        work / "rendered_final_scenes",
        timing,
        draft,
        work / "draft_v1_qa",
        audio,
    )
    result = {
        "status": qa["status"],
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
            "canonical_text": cta_config.get("canonical_text"),
        },
        "subtitles": {"srt": str(BASE / "captions.srt"), "ass": str(BASE / "captions.ass"), "cue_count": len(data.get("subtitles", []))},
        "video": video,
        "qa": qa,
    }
    (work / "phase_b_build_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if qa["status"] == "PASS" else 2 if qa["status"] == "WARN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
