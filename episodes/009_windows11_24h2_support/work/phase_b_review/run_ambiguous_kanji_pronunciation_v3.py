"""Preflight ambiguous ``方`` usage before Episode 009 draft_v3 synthesis."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
EP = ROOT / "episodes" / "009_windows11_24h2_support"
EPISODE_PATH = EP / "episode.json"
SCRIPT_PATH = EP / "script.md"
CONFIG_PATH = ROOT / "config" / "voicevox_pronunciation.yaml"
REPORT_JSON = EP / "work" / "phase_b_review" / "ambiguous_kanji_pronunciation_v3.json"
REPORT_MD = EP / "work" / "phase_b_review" / "ambiguous_kanji_pronunciation_v3.md"

OLD_PHRASES = {
    6: "三つ目、更新が表示されないときの考え方です。",
    38: "24H2の方は、まず25H2が表示されるかを確認してください。",
}
NEW_PHRASES = {
    6: "三つ目は、更新が表示されないときに考えるポイントです。",
    38: "24H2の場合は、まず25H2が表示されるかを確認してください。",
}


def classify(text: str, index: int) -> tuple[str, str, str]:
    """Return category, status, and reason for one occurrence."""
    before = text[max(0, index - 10):index]
    after = text[index + 1:index + 8]
    if any(term in text[max(0, index - 4):index + 5] for term in ("考え方", "やり方", "使い方")):
        return "C", "REWRITE", "複合語は自然な代替表現を優先"
    if "の方は" in text[max(0, index - 2):index + 4] or "方は" in text[index:index + 3]:
        return "D", "REWRITE", "「〜の方は」は冗長表現の候補"
    if any(term in text[max(0, index - 6):index + 4] for term in ("右の方", "左の方", "上の方", "下の方", "こちらの方")):
        return "B", "SAFE", "方向・比較の表現"
    if "方" in before or "方" in after:
        return "A", "REVIEW", "人を指す敬語表現のため文脈確認"
    return "A", "REVIEW", "人を指す可能性があるため文脈確認"


def walk_strings(value: Any, path: str = "") -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            rows.extend(walk_strings(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            rows.extend(walk_strings(child, f"{path}[{index}]"))
    elif isinstance(value, str) and "方" in value:
        rows.append({"path": path, "value": value})
    return rows


def main() -> int:
    data = json.loads(EPISODE_PATH.read_text(encoding="utf-8"))
    segments = data.get("narration_segments") or []
    narration_rows: list[dict[str, Any]] = []
    for segment in segments:
        sid = int(segment["id"])
        text = str(segment.get("narration") or "")
        for index, _char in enumerate(text):
            if text[index] != "方":
                continue
            category, status, reason = classify(text, index)
            narration_rows.append({
                "segment_id": sid,
                "category": category,
                "status": status,
                "context": text,
                "reason": reason,
            })

    script_lines = SCRIPT_PATH.read_text(encoding="utf-8").splitlines()
    script_rows = [
        {"line": line_number, "text": line}
        for line_number, line in enumerate(script_lines, 1)
        if "方" in line
    ]
    non_narration_json = walk_strings(data)
    config_text = CONFIG_PATH.read_text(encoding="utf-8") if CONFIG_PATH.exists() else ""
    global方_entry = bool(re.search(r"(?m)^\s*-?\s*surface:\s*[\"']?方[\"']?\s*$", config_text))

    target_checks = []
    narration_by_id = {int(segment["id"]): str(segment.get("narration") or "") for segment in segments}
    subtitles_by_segment: dict[int, str] = {}
    for cue in data.get("subtitles") or []:
        sid = int(cue["segment_id"])
        subtitles_by_segment[sid] = subtitles_by_segment.get(sid, "") + "".join(str(x) for x in cue.get("text_lines") or [])
    failures: list[str] = []
    for sid, old in OLD_PHRASES.items():
        narration = narration_by_id.get(sid, "")
        subtitle = subtitles_by_segment.get(sid, "")
        new = NEW_PHRASES[sid]
        ok = old not in narration and new == narration and old not in subtitle and new == subtitle
        target_checks.append({
            "segment_id": sid,
            "old_phrase_absent": old not in narration and old not in subtitle,
            "new_phrase_matches_narration": narration == new,
            "new_phrase_matches_subtitle": subtitle == new,
            "status": "PASS" if ok else "FAIL",
        })
        if not ok:
            failures.append(f"segment {sid:03d}: target wording or subtitle mismatch")
    if global方_entry:
        failures.append("global 方 pronunciation dictionary entry exists")

    review_rows = [row for row in narration_rows if row["status"] != "SAFE"]
    result = {
        "status": "FAIL" if failures else "REVIEW" if review_rows else "PASS",
        "preflight": "ambiguous_kanji_pronunciation",
        "target_checks": target_checks,
        "narration_segment_count": len(segments),
        "narration_occurrence_count": len(narration_rows),
        "narration_occurrences": narration_rows,
        "script_occurrence_count": sum(line["text"].count("方") for line in script_rows),
        "script_occurrences": script_rows,
        "episode_json_non_narration_occurrences": non_narration_json,
        "global_方_dictionary_entry": global方_entry,
        "failures": failures,
        "deferred_review_count": len(review_rows),
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Episode 009 ambiguous_kanji_pronunciation v3",
        "",
        f"- status: **{result['status']}**",
        "- rule: `ambiguous_方_avoidance`",
        f"- narration segments scanned: {len(segments)}",
        f"- `方` in narration: {len(narration_rows)}",
        f"- `方` in script.md: {result['script_occurrence_count']}（見出しを含む）",
        f"- global `方` dictionary entry: {'あり' if global方_entry else 'なし'}",
        "",
        "## Targeted wording changes",
        "",
        "| segment | result |",
        "|---:|---|",
    ]
    for check in target_checks:
        lines.append(f"| {check['segment_id']:03d} | {check['status']} |")
    lines.extend(["", "## Narration occurrences", "", "| segment | category | status | context |", "|---:|:---:|:---:|---|"])
    for row in narration_rows:
        lines.append(f"| {row['segment_id']:03d} | {row['category']} | {row['status']} | {row['context']} |")
    if not narration_rows:
        lines.append("| — | — | PASS | なし |")
    lines.extend(["", "- A: 人を指す", "- B: 方向・比較", "- C: 複合語", "- D: 冗長な「〜の方は」", "", "## Deferred review", ""])
    if review_rows:
        lines.extend(f"- segment {row['segment_id']:03d}: {row['status']} — {row['reason']}（今回は人間指摘の2箇所以外なので改稿せず記録）" for row in review_rows)
    else:
        lines.append("- なし")
    lines.extend(["", "## script.md occurrences", ""])
    if script_rows:
        lines.extend(f"- line {row['line']}: {row['text']}" for row in script_rows)
    else:
        lines.append("- なし")
    lines.extend(["", "## FAIL", ""])
    lines.extend(f"- {failure}" for failure in failures) or lines.append("- なし")
    lines.extend(["", "##判定", "", "- targeted wording: PASS" if not failures else "- targeted wording: FAIL", "- deferred non-target narration occurrences are documented above", ""])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "narration_occurrence_count": len(narration_rows), "script_occurrence_count": result["script_occurrence_count"], "failures": failures}, ensure_ascii=False))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
