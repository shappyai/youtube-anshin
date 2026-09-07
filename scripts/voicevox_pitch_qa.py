"""QA human-approved mora pitch shapes from saved VOICEVOX audio_query JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from episode_io import load_json, load_pronunciation_entries, segment_spoken_text


def _positions(query: dict[str, Any]) -> list[tuple[int, int, str, float]]:
    result: list[tuple[int, int, str, float]] = []
    for phrase_index, phrase in enumerate(query.get("accent_phrases") or []):
        for mora_index, mora in enumerate(phrase.get("moras") or []):
            result.append(
                (
                    phrase_index,
                    mora_index,
                    str(mora.get("text") or ""),
                    float(mora.get("pitch") or 0.0),
                )
            )
    return result


def _matching_starts(query: dict[str, Any], reading: str) -> list[int]:
    target = [char for char in str(reading).replace(" ", "") if char.strip()]
    positions = _positions(query)
    return [
        index
        for index in range(max(0, len(positions) - len(target) + 1))
        if [item[2] for item in positions[index:index + len(target)]] == target
    ]


def _entry_for_segment(segment: dict[str, Any], entries: list[dict[str, Any]], episode_id: str) -> list[dict[str, Any]]:
    text = segment_spoken_text(segment)
    result: list[dict[str, Any]] = []
    for entry in entries:
        if str(entry.get("pitch_shape") or "") != "low_high_plateau":
            continue
        surface = str(entry.get("surface") or "")
        scope = str(entry.get("scope") or "")
        if surface and surface in text and (not scope or episode_id in scope or "標準辞書" in scope):
            result.append(entry)
    return result


def check_segment(
    segment: dict[str, Any], query: dict[str, Any], entries: list[dict[str, Any]], episode_id: str,
    timing: dict[int, dict[str, Any]], tolerance: float = 1e-6,
) -> dict[str, Any]:
    positions = _positions(query)
    checks: list[dict[str, Any]] = []
    for entry in _entry_for_segment(segment, entries, episode_id):
        reading = str(entry.get("reading") or "").replace(" ", "")
        target = [char for char in reading if char.strip()]
        for start in _matching_starts(query, reading):
            end = start + len(target) - 1
            pitches = [item[3] for item in positions[start:end + 1]]
            first_mora_low = len(pitches) >= 2 and pitches[0] < pitches[1]
            high_values = pitches[1:]
            later_mora_plateau = bool(high_values) and max(high_values) - min(high_values) <= tolerance
            following_delta: float | None = None
            following_same = 0
            if end + 1 < len(positions) and target[-1] == positions[end][2] == positions[end + 1][2]:
                previous_phrase = positions[end][0]
                next_phrase = positions[end + 1][0]
                phrases = query.get("accent_phrases") or []
                contiguous = next_phrase == previous_phrase or (
                    next_phrase == previous_phrase + 1
                    and not phrases[previous_phrase].get("pause_mora")
                )
                if contiguous:
                    following_delta = abs(positions[end + 1][3] - pitches[-1])
                    following_same = 1
            checks.append(
                {
                    "surface": str(entry.get("surface") or ""),
                    "reading": reading,
                    "mora_text": target,
                    "pitch": pitches,
                    "first_mora_low": first_mora_low,
                    "second_mora_rise": first_mora_low,
                    "later_mora_plateau": later_mora_plateau,
                    "consecutive_same_mora_count": following_same,
                    "consecutive_same_mora_pitch_delta": following_delta,
                    "consecutive_same_mora_pass": following_delta is None or following_delta <= tolerance,
                }
            )
    row = timing.get(int(segment["id"]), {})
    passed = bool(checks) and all(
        item["first_mora_low"]
        and item["second_mora_rise"]
        and item["later_mora_plateau"]
        and item["consecutive_same_mora_pass"]
        for item in checks
    )
    return {
        "segment_id": int(segment["id"]),
        "narration": segment_spoken_text(segment),
        "start_sec": row.get("start_sec"),
        "end_sec": row.get("end_sec"),
        "checks": checks,
        "approved_pitch_shape_match": passed,
    }


def run_qa(
    episode_path: Path, query_audit_path: Path, timing_path: Path, report_path: Path,
    tolerance: float = 1e-6,
) -> dict[str, Any]:
    data = load_json(episode_path)
    audit = json.loads(query_audit_path.read_text(encoding="utf-8"))
    timing_data = json.loads(timing_path.read_text(encoding="utf-8"))
    timing = {int(row["segment_id"]): row for row in timing_data.get("segments", [])}
    entries = load_pronunciation_entries()
    episode_id = str(data["episode"]["episode_id"])
    rows: list[dict[str, Any]] = []
    missing: list[int] = []
    for segment in data.get("narration_segments", []):
        if not _entry_for_segment(segment, entries, episode_id):
            continue
        segment_id = int(segment["id"])
        item = audit.get(str(segment_id)) or {}
        query = item.get("query") if isinstance(item, dict) else None
        if not isinstance(query, dict):
            missing.append(segment_id)
            continue
        rows.append(check_segment(segment, query, entries, episode_id, timing, tolerance))
    failures = [row for row in rows if not row["approved_pitch_shape_match"]]
    failures.extend({"segment_id": segment_id, "reason": "query missing"} for segment_id in missing)
    result = {
        "status": "PASS" if rows and not failures else "FAIL",
        "qa": "approved_pitch_shape_match",
        "surface": "信用",
        "target_segment_ids": [int(segment["id"]) for segment in data.get("narration_segments", []) if _entry_for_segment(segment, entries, episode_id)],
        "tolerance": tolerance,
        "rows": rows,
        "failures": failures,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.with_suffix(".json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# VOICEVOX pitch shape QA",
        "",
        "- qa: `approved_pitch_shape_match`",
        f"- status: **{result['status']}**",
        f"- target segments: {result['target_segment_ids']}",
        f"- tolerance: {tolerance}",
        "",
        "| segment | timestamp | first low | second rise | later plateau | O-O delta | result |",
        "|---:|---|---|---|---|---:|---|",
    ]
    for row in rows:
        checks = row["checks"]
        check = checks[0] if checks else {}
        delta = check.get("consecutive_same_mora_pitch_delta")
        timestamp = f"{float(row['start_sec']):.3f}s" if row.get("start_sec") is not None else "-"
        lines.append(
            f"| {row['segment_id']:03d} | {timestamp} | "
            f"{'PASS' if check.get('first_mora_low') else 'FAIL'} | "
            f"{'PASS' if check.get('second_mora_rise') else 'FAIL'} | "
            f"{'PASS' if check.get('later_mora_plateau') else 'FAIL'} | "
            f"{delta if delta is not None else 'n/a'} | "
            f"{'PASS' if row['approved_pitch_shape_match'] else 'FAIL'} |"
        )
    if missing:
        lines.extend(["", "Missing query: " + ", ".join(str(item) for item in missing)])
    report_path.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("episode", type=Path)
    parser.add_argument("query_audit", type=Path)
    parser.add_argument("timing", type=Path)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    result = run_qa(args.episode.resolve(), args.query_audit.resolve(), args.timing.resolve(), args.report.resolve())
    print(json.dumps({key: result[key] for key in ("status", "target_segment_ids", "failures")}, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
