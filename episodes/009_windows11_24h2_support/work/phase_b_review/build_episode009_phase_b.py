"""Prepare Episode 009 Phase B canonical narration overrides and subtitles."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
EPISODE_PATH = ROOT / "episodes" / "009_windows11_24h2_support" / "episode.json"

# TTS-only readings. The visible display text remains the original ASCII version.
VERSION_READINGS = {
    "24H2": "にじゅうよん、エイチ、ツー",
    "25H2": "にじゅうご、エイチ、ツー",
    "26H1": "にじゅうろく、エイチ、ワン",
}
PROTECTED_TERMS = (
    "Windows 11",
    "Windows Update",
    "24H2",
    "25H2",
    "26H1",
    "Microsoft",
    "Pro Education",
    "Pro for Workstations",
)


def load_width_tools():
    import sys

    scripts = ROOT / "scripts"
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    from subtitle_preflight import estimated_width

    return estimated_width


def safe_cut(text: str, cut: int) -> bool:
    left, right = text[:cut], text[cut:]
    if len(left.strip()) < 4 or len(right.strip()) < 4:
        return False
    for term in PROTECTED_TERMS:
        start = text.find(term)
        while start >= 0:
            end = start + len(term)
            if start < cut < end:
                return False
            start = text.find(term, start + 1)
    return True


def punctuation_cuts(text: str) -> list[int]:
    return [index + 1 for index, char in enumerate(text) if char in "、。！？?!"]


def choose_cut(text: str, max_width: int, estimated_width) -> int | None:
    candidates = [
        cut
        for cut in punctuation_cuts(text)
        if safe_cut(text, cut)
        and estimated_width(text[:cut]) <= max_width
        and estimated_width(text[cut:]) > 0
    ]
    if candidates:
        # Prefer a cut near the visual middle while keeping the opening phrase readable.
        midpoint = len(text) / 2
        return min(candidates, key=lambda cut: abs(cut - midpoint))
    for cut in range(min(len(text) - 4, 26), 3, -1):
        if safe_cut(text, cut) and estimated_width(text[:cut]) <= max_width:
            return cut
    return None


def split_fragments(text: str, estimated_width) -> list[str]:
    # Keep each cue below two lines with generous width headroom. Clause-level
    # grouping makes the split semantic instead of relying on character count.
    clauses = [part for part in re.findall(r".*?[、。！？?!]|.+$", text) if part]
    fragments: list[str] = []
    current = ""
    for clause in clauses:
        candidate = current + clause
        if current and estimated_width(candidate) > 3000:
            fragments.append(current)
            current = clause
        else:
            current = candidate
    if current:
        fragments.append(current)

    result: list[str] = []
    for fragment in fragments:
        remaining = fragment
        while estimated_width(remaining) > 3000:
            cut = choose_cut(remaining, 1800, estimated_width)
            if cut is None:
                break
            result.append(remaining[:cut])
            remaining = remaining[cut:]
        result.append(remaining)
    return [fragment for fragment in result if fragment.strip()]


def cue_lines(text: str, estimated_width) -> list[str]:
    if estimated_width(text) <= 1800:
        return [text]
    candidates = [
        cut
        for cut in punctuation_cuts(text)
        if safe_cut(text, cut)
        and estimated_width(text[:cut]) <= 1800
        and estimated_width(text[cut:]) <= 1800
    ]
    cut = min(candidates, key=lambda value: abs(value - len(text) / 2)) if candidates else None
    if cut is None:
        candidates = [
            value
            for value in range(4, len(text) - 3)
            if safe_cut(text, value)
            and estimated_width(text[:value]) <= 1800
            and estimated_width(text[value:]) <= 1800
        ]
        if candidates:
            cut = min(candidates, key=lambda value: abs(value - len(text) / 2))
    lines = [text[:cut], text[cut:]]
    if any(not line.strip() or estimated_width(line) > 1800 for line in lines):
        raise ValueError(f"subtitle line does not fit safely: {text!r} -> {lines!r}")
    return lines


def build() -> dict[str, Any]:
    estimated_width = load_width_tools()
    data = json.loads(EPISODE_PATH.read_text(encoding="utf-8"))

    for segment in data["narration_segments"]:
        narration = str(segment["narration"])
        segment["display_text"] = narration
        overrides = dict(segment.get("reading_overrides") or {})
        for surface, reading in VERSION_READINGS.items():
            if surface in narration:
                overrides[surface] = reading
        segment["reading_overrides"] = overrides

    subtitles: list[dict[str, Any]] = []
    for segment in data["narration_segments"]:
        segment_id = int(segment["id"])
        fragments = split_fragments(str(segment["display_text"]), estimated_width)
        ids: list[str] = []
        for order, fragment in enumerate(fragments):
            subtitle_id = f"SUB-{segment_id:03d}" if len(fragments) == 1 else f"SUB-{segment_id:03d}-{order + 1}"
            ids.append(subtitle_id)
            subtitles.append(
                {
                    "id": subtitle_id,
                    "text_lines": cue_lines(fragment, estimated_width),
                    "segment_id": segment_id,
                    "display_order": order,
                    "font_px": 72,
                }
            )
        segment["subtitle_ids"] = ids
    data["subtitles"] = subtitles

    for scene in data["scenes"]:
        scene["subtitle_ids"] = [
            subtitle_id
            for segment in data["narration_segments"]
            if int(scene["start_segment"]) <= int(segment["id"]) <= int(scene["end_segment"])
            for subtitle_id in segment.get("subtitle_ids", [])
        ]

    data["metadata"]["production_phase"] = "Phase B（VOICEVOX・字幕・draft）"
    data["narration"]["segment_policy"] = "1文ずつaudio_query→synthesis。実測WAVで字幕・scene timelineを作成。"
    data["postroll"].update(
        {
            "kind": "channel_cta",
            "profile": "channel_common_cta",
            "cta_profile": "channel_common_cta",
            "audio_required": True,
            "duration_mode": "audio_based",
            "asset": "work/channel_cta.png",
            "cta_audio": "audio/voicevox_kenzaki/cta_channel_common.wav",
            "duration_sec": 15,
            "animation": "static",
            "status": "phase_b_ready",
        }
    )
    data["episode"]["status"] = "draft"

    EPISODE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "segment_count": len(data["narration_segments"]),
        "subtitle_count": len(subtitles),
        "split_segment_count": sum(1 for segment in data["narration_segments"] if len(segment["subtitle_ids"]) > 1),
        "version_override_segments": [
            int(segment["id"])
            for segment in data["narration_segments"]
            if any(surface in (segment.get("reading_overrides") or {}) for surface in VERSION_READINGS)
        ],
    }


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False))
