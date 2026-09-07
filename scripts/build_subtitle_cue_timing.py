"""Create VOICEVOX-measured duration weights for split subtitle cues.

The narration WAV remains the timing authority for each narration segment.  For
segments that have multiple display cues, this helper asks the same VOICEVOX
engine for each cue and records its estimated speech duration so cue boundaries
are not allocated from character counts.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from episode_io import load_json  # noqa: E402
from tts_voicevox import (  # noqa: E402
    apply_pronunciation_overrides,
    apply_pronunciation_pitch_patterns,
    apply_segment_accent_overrides,
    make_audio_query,
    refresh_mora_data,
    resolve_speaker,
)
from voicevox_preflight import expected_reading  # noqa: E402


def query_duration(query: dict[str, Any]) -> float:
    """Approximate synthesized duration from the engine's mora timings."""
    duration = float(query.get("prePhonemeLength") or 0.0)
    duration += float(query.get("postPhonemeLength") or 0.0)
    for phrase in query.get("accent_phrases") or []:
        for mora in phrase.get("moras") or []:
            duration += float(mora.get("consonant_length") or 0.0)
            duration += float(mora.get("vowel_length") or 0.0)
        pause = phrase.get("pause_mora")
        if isinstance(pause, dict):
            duration += float(pause.get("vowel_length") or 0.0)
    return max(0.05, duration)


def build_measurements(
    data: dict[str, Any], engine_url: str, speaker_name: str, style_name: str,
) -> dict[str, Any]:
    episode_id = str(data.get("episode", {}).get("episode_id") or "")
    segments = {int(row["id"]): row for row in data.get("narration_segments", [])}
    _speaker_uuid, style_id = resolve_speaker(engine_url, speaker_name, style_name)
    rows: dict[str, Any] = {}
    for cue in data.get("subtitles", []):
        cue_id = str(cue.get("id") or "")
        segment = segments[int(cue["segment_id"])]
        text = "".join(str(line) for line in cue.get("text_lines", []))
        pseudo_segment = {
            "narration": text,
            "spoken_text": text,
            "reading_overrides": segment.get("reading_overrides") or {},
            "accent_overrides": segment.get("accent_overrides") or {},
        }
        effective_text, approvals = expected_reading(pseudo_segment, [], episode_id)
        query = make_audio_query(engine_url, effective_text, style_id)
        query["speedScale"] = 1.0
        query["intonationScale"] = 1.0
        query["pitchScale"] = 0.0
        changed = apply_pronunciation_overrides(query, episode_id=episode_id)
        changed = apply_segment_accent_overrides(query, pseudo_segment) or changed
        if changed:
            refresh_mora_data(engine_url, query, style_id)
        apply_pronunciation_pitch_patterns(query, episode_id=episode_id)
        rows[cue_id] = {
            "cue_id": cue_id,
            "segment_id": int(cue["segment_id"]),
            "display_text": text,
            "effective_text": effective_text,
            "duration_sec": round(query_duration(query), 6),
            "kana": str(query.get("kana") or ""),
            "reading_overrides": approvals,
        }
    return {
        "version": 1,
        "method": "VOICEVOX audio_query mora duration; segment boundaries remain measured WAV timing",
        "engine_url": engine_url,
        "speaker": speaker_name,
        "style": style_name,
        "style_id": style_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cue_count": len(rows),
        "cues": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("episode", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--engine-url", default="http://127.0.0.1:50021")
    parser.add_argument("--speaker", default="剣崎雌雄")
    parser.add_argument("--style", default="ノーマル")
    args = parser.parse_args()
    episode_path = args.episode.resolve()
    output = (args.output or episode_path.parent / "work" / "subtitle_cue_timing.json").resolve()
    result = build_measurements(load_json(episode_path), args.engine_url, args.speaker, args.style)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "output": str(output), "cue_count": result["cue_count"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
