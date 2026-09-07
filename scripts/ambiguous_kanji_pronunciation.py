"""Scan narration and script text for ambiguous ``方`` usage before TTS."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "voicevox_pronunciation.yaml"


def classify(text: str, index: int) -> tuple[str, str, str]:
    context = text[max(0, index - 8):index + 8]
    if any(term in context for term in ("考え方", "やり方", "使い方")):
        return "C", "REWRITE", "複合語は自然な代替表現を優先"
    if "の方は" in context or text[index:index + 2] == "方は":
        return "D", "REWRITE", "「〜の方は」は冗長表現の候補"
    if any(term in context for term in ("右の方", "左の方", "上の方", "下の方", "こちらの方")):
        return "B", "SAFE", "方向・比較の表現"
    return "A", "REVIEW", "人を指す表現のため文脈確認"


def scan(episode_path: Path) -> dict[str, Any]:
    data = json.loads(episode_path.read_text(encoding="utf-8"))
    script_path = episode_path.parent / "script.md"
    occurrences: list[dict[str, Any]] = []
    for segment in data.get("narration_segments") or []:
        sid = int(segment["id"])
        text = str(segment.get("narration") or "")
        for index, char in enumerate(text):
            if char != "方":
                continue
            category, status, reason = classify(text, index)
            occurrences.append({"segment_id": sid, "category": category, "status": status, "context": text, "reason": reason})
    script_lines = script_path.read_text(encoding="utf-8").splitlines() if script_path.exists() else []
    script_occurrences = [{"line": n, "text": line} for n, line in enumerate(script_lines, 1) if "方" in line]
    config_text = CONFIG_PATH.read_text(encoding="utf-8") if CONFIG_PATH.exists() else ""
    global_entry = bool(re.search(r"(?m)^\s*-?\s*surface:\s*[\"']?方[\"']?\s*$", config_text))
    failures = ["global 方 pronunciation dictionary entry exists"] if global_entry else []
    return {
        "status": "FAIL" if failures else "REVIEW" if occurrences else "PASS",
        "preflight": "ambiguous_kanji_pronunciation",
        "rule": "ambiguous_方_avoidance",
        "episode": episode_path.parent.name,
        "narration_segment_count": len(data.get("narration_segments") or []),
        "narration_occurrence_count": len(occurrences),
        "narration_occurrences": occurrences,
        "script_occurrence_count": sum(row["text"].count("方") for row in script_occurrences),
        "script_occurrences": script_occurrences,
        "global_方_dictionary_entry": global_entry,
        "failures": failures,
    }


def write_report(result: dict[str, Any], report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "\n".join([
            "# ambiguous_kanji_pronunciation",
            "",
            f"- status: **{result['status']}**",
            f"- rule: `{result['rule']}`",
            f"- narration segments scanned: {result['narration_segment_count']}",
            f"- `方` in narration: {result['narration_occurrence_count']}",
            f"- `方` in script.md: {result['script_occurrence_count']}",
            f"- global `方` dictionary entry: {'あり' if result['global_方_dictionary_entry'] else 'なし'}",
            "",
            "## Classification",
            "",
            "| segment | category | status | context |",
            "|---:|:---:|:---:|---|",
            *[f"| {row['segment_id']:03d} | {row['category']} | {row['status']} | {row['context']} |" for row in result["narration_occurrences"]],
            *( ["| — | — | PASS | なし |"] if not result["narration_occurrences"] else [] ),
            "",
            "- A: 人を指す",
            "- B: 方向・比較",
            "- C: 複合語",
            "- D: 冗長な「〜の方は」",
            "",
            "## FAIL",
            "",
            *[f"- {failure}" for failure in result["failures"]],
            *( ["- なし"] if not result["failures"] else [] ),
            "",
        ]) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("episode", type=Path, help="episode.json")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    episode_path = args.episode.resolve()
    result = scan(episode_path)
    report_path = (args.report or episode_path.parent / "work" / "ambiguous_kanji_pronunciation.md").resolve()
    write_report(result, report_path)
    report_json = report_path.with_suffix(".json")
    report_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "narration_occurrence_count": result["narration_occurrence_count"], "script_occurrence_count": result["script_occurrence_count"], "report": str(report_path)}, ensure_ascii=False))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
