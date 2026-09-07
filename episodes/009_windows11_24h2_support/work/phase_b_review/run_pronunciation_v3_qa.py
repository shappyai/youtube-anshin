"""Verify preserved and regenerated VOICEVOX pronunciation for draft_v3."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
EP = ROOT / "episodes" / "009_windows11_24h2_support"
EPISODE_PATH = EP / "episode.json"
CURRENT_AUDIT = EP / "work" / "voicevox_query_audit.json"
V2_AUDIT = EP / "work" / "phase_b_review" / "pronunciation_fix_v2_query_audit.json"
REPORT_JSON = EP / "work" / "phase_b_review" / "pronunciation_v3_qa.json"
REPORT_MD = EP / "work" / "phase_b_review" / "pronunciation_v3_qa.md"

TARGETS = {
    "Windows": "ウィンドオズ",
    "Update": "アップデエト",
    "ID": "アイディイ",
    "24H2": "ニジュウヨンエイチツー",
    "25H2": "ニジュウゴエイチツー",
    "26H1": "ニジュウロクエイチワン",
}


def normalize_kana(value: str) -> str:
    return re.sub(r"[^ァ-ヶー]", "", value).replace("ヵ", "カ").replace("ツウ", "ツー")


def query_kana(query: dict[str, Any]) -> str:
    parts: list[str] = []
    for phrase in query.get("accent_phrases") or []:
        parts.extend(str(mora.get("text") or "") for mora in phrase.get("moras") or [])
    return "".join(parts)


def audit_for_segment(sid: int, current: dict[str, Any], old: dict[str, Any]) -> dict[str, Any]:
    return (current.get(str(sid)) or old.get(str(sid)) or {})


def main() -> int:
    data = json.loads(EPISODE_PATH.read_text(encoding="utf-8"))
    current = json.loads(CURRENT_AUDIT.read_text(encoding="utf-8")) if CURRENT_AUDIT.exists() else {}
    old_root = json.loads(V2_AUDIT.read_text(encoding="utf-8")) if V2_AUDIT.exists() else {}
    old = old_root.get("audit") or {}
    failures: list[str] = []
    occurrences: dict[str, list[dict[str, Any]]] = {term: [] for term in TARGETS}
    for segment in data.get("narration_segments") or []:
        sid = int(segment["id"])
        text = str(segment.get("narration") or "")
        audit = audit_for_segment(sid, current, old)
        query = audit.get("query") or {}
        kana = query_kana(query)
        normalized = normalize_kana(kana)
        for term, expected in TARGETS.items():
            if term not in text:
                continue
            target = normalize_kana(expected)
            ok = target in normalized
            row = {
                "segment_id": sid,
                "text": text,
                "expected_reading": expected,
                "query_kana": kana,
                "match": ok,
                "source": "regenerated" if str(sid) in current else "reused_v2_audit",
            }
            occurrences[term].append(row)
            if not ok:
                failures.append(f"{term} segment {sid:03d}: reading mismatch")

    # The two person usages remain approved as かた; the targeted 006/038 usages
    # were removed from narration rather than pronunciation-overridden.
    for sid, expected in ((1, "カタ"), (11, "カタ")):
        text = next(str(s.get("narration") or "") for s in data["narration_segments"] if int(s["id"]) == sid)
        audit = audit_for_segment(sid, current, old)
        normalized = normalize_kana(query_kana(audit.get("query") or {}))
        ok = "方" in text and normalize_kana(expected) in normalized
        occurrences.setdefault("方", []).append({"segment_id": sid, "expected_reading": "かた", "query_kana": query_kana(audit.get("query") or {}), "match": ok, "source": "reused_v2_audit"})
        if not ok:
            failures.append(f"方 segment {sid:03d}: expected かた")

    result = {
        "status": "PASS" if not failures else "FAIL",
        "qa": "pronunciation_preserved_and_regenerated",
        "failures": failures,
        "targets": occurrences,
        "regenerated_segments": sorted(int(key) for key in current if key.isdigit()),
        "reused_segment_count": sum(1 for segment in data.get("narration_segments") or [] if str(int(segment["id"])) not in current),
        "global_方_dictionary_entry": bool(re.search(r"(?m)^\s*-?\s*surface:\s*[\"']?方[\"']?\s*$", (ROOT / "config" / "voicevox_pronunciation.yaml").read_text(encoding="utf-8"))),
    }
    if result["global_方_dictionary_entry"]:
        result["failures"].append("global 方 pronunciation dictionary entry exists")
        result["status"] = "FAIL"
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Episode 009 pronunciation v3 QA",
        "",
        f"- status: **{result['status']}**",
        "- Windows / Update / ID / 24H2 / 25H2 / 26H1: preserved or regenerated reading match",
        f"- regenerated segments: {', '.join(f'{sid:03d}' for sid in result['regenerated_segments'])}",
        f"- reused segments: {result['reused_segment_count']}",
        "- global `方` dictionary entry: なし" if not result["global_方_dictionary_entry"] else "- global `方` dictionary entry: あり",
        "",
        "| term | occurrences | result |",
        "|---|---:|---|",
    ]
    for term in ["Windows", "Update", "ID", "24H2", "25H2", "26H1", "方"]:
        rows = occurrences.get(term, [])
        lines.append(f"| {term} | {len(rows)} | {'PASS' if rows and all(row['match'] for row in rows) else 'N/A' if not rows else 'FAIL'} |")
    lines.extend(["", "## FAIL", ""])
    lines.extend(f"- {failure}" for failure in result["failures"]) or lines.append("- なし")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": result["status"], "regenerated": result["regenerated_segments"], "reused": result["reused_segment_count"], "failures": result["failures"]}, ensure_ascii=False))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
