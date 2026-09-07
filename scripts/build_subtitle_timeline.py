"""Build SRT/ASS from explicit episode subtitles and measured segment times."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def timestamp_srt(seconds: float) -> str:
    milliseconds = int(round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def timestamp_ass(seconds: float) -> str:
    centiseconds = int(round(seconds * 100))
    hours, remainder = divmod(centiseconds, 360_000)
    minutes, remainder = divmod(remainder, 6000)
    secs, cs = divmod(remainder, 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{cs:02d}"


def measured_cue_weight(cue: dict[str, Any], cue_timing: dict[str, Any] | None) -> float:
    """Use VOICEVOX-measured cue duration; never derive timing from character count."""
    if cue_timing:
        row = cue_timing.get(str(cue.get("id"))) or {}
        try:
            value = float(row.get("duration_sec") or 0.0)
            if value > 0:
                return value
        except (TypeError, ValueError):
            pass
    # Equal fallback keeps legacy episodes usable without reintroducing
    # character-count timing. New Phase B builds should provide cue timing.
    return 1.0


def build_cue_times(
    data: dict[str, Any], audio_timing: dict[str, Any],
    cue_timing: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    segment_times = {int(row["segment_id"]): row for row in audio_timing.get("segments", [])}
    by_segment: dict[int, list[dict[str, Any]]] = {}
    for cue in data.get("subtitles", []):
        by_segment.setdefault(int(cue["segment_id"]), []).append(cue)
    result: list[dict[str, Any]] = []
    for segment in data.get("narration_segments", []):
        segment_id = int(segment["id"])
        timing = segment_times.get(segment_id)
        if not timing:
            raise ValueError(f"missing audio timing for segment {segment_id}")
        cues = by_segment.get(segment_id, [])
        if not cues:
            raise ValueError(f"missing subtitle cue for segment {segment_id}")
        start, end = float(timing["start_sec"]), float(timing["end_sec"])
        weights = [measured_cue_weight(cue, cue_timing) for cue in cues]
        total = sum(weights)
        cursor = start
        for index, (cue, weight) in enumerate(zip(cues, weights)):
            cue_end = end if index == len(cues) - 1 else cursor + (end - start) * weight / total
            result.append({**cue, "start_sec": round(cursor, 3), "end_sec": round(cue_end, 3)})
            cursor = cue_end
    return result


def write_subtitles(cues: list[dict[str, Any]], srt_path: Path, ass_path: Path) -> None:
    srt: list[str] = []
    for index, cue in enumerate(cues, 1):
        srt.extend([str(index), f"{timestamp_srt(cue['start_sec'])} --> {timestamp_srt(cue['end_sec'])}", *cue["text_lines"], ""])
    srt_path.parent.mkdir(parents=True, exist_ok=True)
    srt_path.write_text("\n".join(srt), encoding="utf-8")
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Yu Gothic,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H0016263F,-1,0,0,0,100,100,0,0,1,4,0,2,60,60,25,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for cue in cues:
        prefix = ""
        fs = cue.get("font_px")
        if fs and int(fs) != 72:
            # 長文 cue の2行収納用に cue 単位でフォントを下げる（最小44px・恒久ルール）
            prefix = "{\\fs%d}" % int(fs)
        text = "\\N".join(str(line) for line in cue["text_lines"])
        events.append(
            f"Dialogue: 0,{timestamp_ass(cue['start_sec'])},{timestamp_ass(cue['end_sec'])},"
            f"Default,,0,0,0,,{prefix}{text}"
        )
    ass_path.write_text(header + "\n".join(events) + "\n", encoding="utf-8")


def build_from_files(
    data: dict[str, Any], timing_path: Path, srt_path: Path, ass_path: Path,
    cue_timing_path: Path | None = None,
) -> dict[str, Any]:
    timing = json.loads(timing_path.read_text(encoding="utf-8"))
    candidate = cue_timing_path or timing_path.with_name("subtitle_cue_timing.json")
    cue_timing: dict[str, Any] | None = None
    if candidate.exists():
        loaded = json.loads(candidate.read_text(encoding="utf-8"))
        cue_timing = loaded.get("cues") if isinstance(loaded, dict) else None
    cues = build_cue_times(data, timing, cue_timing)
    write_subtitles(cues, srt_path, ass_path)
    return {"status": "PASS", "cue_count": len(cues), "srt": str(srt_path), "ass": str(ass_path)}
