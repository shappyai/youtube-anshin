"""Episode 013 Phase B audio/subtitle preparation only.

This driver intentionally does not render or assemble a video. It generates
the measured narration and captions, reuses the already approved
registration_conversion_v1 CTA, and leaves final draft gating to the human
visual/pronunciation review.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_subtitle_cue_timing import build_measurements  # noqa: E402
from build_subtitle_timeline import build_from_files  # noqa: E402
from episode_io import apply_episode_defaults, load_json  # noqa: E402
from voicevox_incremental import generate_incremental  # noqa: E402

BASE = ROOT / "episodes" / "013_line_old_version_support_end"
ENGINE = "http://127.0.0.1:50021"
SPEAKER = "剣崎雌雄"
STYLE = "ノーマル"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main() -> int:
    data = apply_episode_defaults(load_json(BASE / "episode.json"))
    work = BASE / "work"
    audio_dir = BASE / "audio" / "voicevox_kenzaki"
    work.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)

    cta_audio = audio_dir / "cta_registration_conversion_v1.wav"
    cta_visual = work / "cta_registration_conversion_v1.png"
    expected_audio_sha = "1D21F765F5606310CA08BC0264EC6ED0136F68F5A7DA07318B5018F1735FDBC9"
    expected_visual_sha = "96EFB5195CD7F3D7121472A79F300AF19999108186D6B35C370EFA488185EAE0"
    if not cta_audio.exists() or sha256(cta_audio) != expected_audio_sha:
        raise SystemExit("STOP: approved CTA audio is missing or SHA-256 mismatched")
    if not cta_visual.exists() or sha256(cta_visual) != expected_visual_sha:
        raise SystemExit("STOP: approved CTA visual is missing or SHA-256 mismatched")

    voice = generate_incremental(data, BASE, work, ENGINE, audio_dir=audio_dir)
    timing = work / "audio_timing.json"
    cue_timing_path = work / "subtitle_cue_timing.json"
    cue_timing = build_measurements(data, ENGINE, SPEAKER, STYLE)
    cue_timing_path.write_text(json.dumps(cue_timing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    srt = work / "captions_auto.srt"
    ass = work / "captions_auto.ass"
    subtitle_result = build_from_files(data, timing, srt, ass, cue_timing_path)
    shutil.copy2(srt, BASE / "captions.srt")
    shutil.copy2(ass, BASE / "captions.ass")

    real_capture_count = data.get("phase_a", {}).get("real_capture_scene_count")
    required_capture_count = data.get("phase_a", {}).get("real_capture_required_scene_count")
    capture_gate = (
        "PASS_7_REAL_UI_PLUS_SCENE005_RENDERER"
        if real_capture_count == required_capture_count == 7
        else "CAPTURE_REQUIRED"
    )
    report = {
        "status": "PASS",
        "episode_id": "013",
        "speaker": SPEAKER,
        "style": STYLE,
        "narration_segment_count": len(voice.get("rows", [])),
        "narration_duration_sec": voice.get("duration"),
        "planned_segments": voice.get("planned", []),
        "reused_segments": voice.get("skipped", []),
        "subtitle_cue_count": subtitle_result.get("cue_count"),
        "subtitle_timing_method": "measured WAV segment bounds + VOICEVOX audio_query mora weights",
        "cta_audio_sha256": sha256(cta_audio),
        "cta_visual_sha256": sha256(cta_visual),
        "cta_reused": True,
        "draft_created": False,
        "capture_gate": capture_gate,
        "draft_gate": "HUMAN_VISUAL_GATE_AND_PRONUNCIATION_REVIEW_REQUIRED",
    }
    (work / "audio_subtitle_phase_b_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
