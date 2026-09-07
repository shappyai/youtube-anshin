"""Verify human-approved pronunciation patterns for every Episode 009 occurrence."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EP = ROOT / "episodes" / "009_windows11_24h2_support"
EPISODE_PATH = EP / "episode.json"
AUDIT_PATH = EP / "work" / "phase_b_review" / "pronunciation_fix_v2_query_audit.json"
TIMING_PATH = EP / "work" / "audio_timing.json"
REPORT_JSON = EP / "work" / "phase_b_review" / "pronunciation_fix_v2_qa.json"
REPORT_MD = EP / "work" / "phase_b_review" / "pronunciation_fix_v2_qa.md"

TARGETS = {
    "Windows": {"reading": "ウィンドオズ", "accent": 5},
    "Update": {"reading": "アップデエト", "accent": 6},
    "ID": {"reading": "アイディイ", "accent": 3},
}


def all_moras(query: dict) -> list[dict]:
    result = []
    for phrase_index, phrase in enumerate(query.get("accent_phrases") or []):
        for mora_index, mora in enumerate(phrase.get("moras") or []):
            result.append({
                "text": str(mora.get("text") or ""),
                "phrase_index": phrase_index,
                "mora_index": mora_index,
                "accent": int(phrase.get("accent") or 0),
            })
    return result


def find_reading(query: dict, reading: str) -> list[dict]:
    target = str(reading).replace(" ", "")
    moras = all_moras(query)
    matches = []
    for start in range(len(moras)):
        joined = ""
        for end in range(start, len(moras)):
            joined += moras[end]["text"]
            if not target.startswith(joined):
                break
            if joined == target:
                phrases = {moras[index]["phrase_index"] for index in range(start, end + 1)}
                accents = {moras[index]["accent"] for index in range(start, end + 1)}
                matches.append({
                    "start_mora": start,
                    "end_mora": end,
                    "mora_count": end - start + 1,
                    "phrase_indexes": sorted(phrases),
                    "accent_values": sorted(accents),
                    "mora_text": [moras[index]["text"] for index in range(start, end + 1)],
                })
    return matches


def main() -> int:
    episode = json.loads(EPISODE_PATH.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8")).get("audit") or {}
    timing = {int(row["segment_id"]): row for row in json.loads(TIMING_PATH.read_text(encoding="utf-8")).get("segments", [])}
    occurrences = {term: [] for term in ["方", "Windows", "Update", "ID"]}
    failures = []
    for segment in episode.get("narration_segments", []):
        sid = int(segment["id"])
        text = str(segment.get("narration") or "")
        item = audit.get(str(sid)) or {}
        query = item.get("query") or {}
        effective = str(item.get("effective_text") or "")
        timestamp = float((timing.get(sid) or {}).get("start_sec") or 0.0)
        if "方" in text:
            expected = "かた" if sid in {1, 11} else "ほう"
            if sid in {1, 11}:
                ok = "かた" in effective and "カタ" in "".join(m["text"] for m in all_moras(query))
            else:
                mora_text = "".join(m["text"] for m in all_moras(query))
                ok = expected == "ほう" and "ほう" in effective and "ホオ" in mora_text and "カタ" not in mora_text
            occurrences["方"].append({"segment_id": sid, "timestamp_sec": timestamp, "context": text, "expected": expected, "effective_text": effective, "approved_pronunciation_match": ok})
            if not ok:
                failures.append(f"方 segment {sid:03d}: expected {expected}")
        for term, spec in TARGETS.items():
            if term not in text:
                continue
            matches = find_reading(query, spec["reading"])
            ok = bool(matches) and all(match["accent_values"] == [spec["accent"]] for match in matches)
            occurrences[term].append({"segment_id": sid, "timestamp_sec": timestamp, "context": text, "expected_reading": spec["reading"], "expected_accent": spec["accent"], "matches": matches, "approved_pronunciation_match": ok})
            if not ok:
                failures.append(f"{term} segment {sid:03d}: expected {spec['reading']} accent={spec['accent']}")
    result = {
        "status": "PASS" if not failures else "FAIL",
        "qa": "approved_pronunciation_match",
        "failures": failures,
        "counts": {term: len(rows) for term, rows in occurrences.items()},
        "segment_ids": {term: [row["segment_id"] for row in rows] for term, rows in occurrences.items()},
        "occurrences": occurrences,
        "context_rules": {"方": {"person_segments": [1, 11], "direction_or_comparison_segments": [6, 38]}},
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Episode 009 pronunciation fix v2 QA", "", f"- status: **{result['status']}**", "- qa: `approved_pronunciation_match`", "",
        "|語|出現segment数|segment IDs|判定|", "|---|---:|---|---|",
    ]
    for term in ["方", "Windows", "Update", "ID"]:
        rows = occurrences[term]
        ids_text = ", ".join(f"{row['segment_id']:03d}" for row in rows)
        verdict = "PASS" if all(row["approved_pronunciation_match"] for row in rows) else "FAIL"
        lines.append(f"| {term} | {len(rows)} | {ids_text} | {verdict} |")
    lines.extend([
        "", "## Context rule: 方", "", "- person: segment 001 / 011 → かた", "- direction or comparison: segment 006 / 038 → ほう", "- global 方 dictionary entry: none", "",
        "## Approved patterns", "", "- Windows: ウィンドオズ / accent=5（語末ズ）", "- Update: アップデエト / accent=6（語末ト）", "- ID: アイディイ / accent=3（ディ。表示はIDのまま）", "",
        "## FAIL", "", *(f"- {failure}" for failure in failures or ["なし"]), "",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "counts": result["counts"], "segment_ids": result["segment_ids"], "failures": failures}, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
