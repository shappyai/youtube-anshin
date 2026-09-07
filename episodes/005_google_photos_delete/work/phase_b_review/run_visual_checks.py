"""Run deterministic visual checks for the Phase B review render."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from episode_io import load_json  # noqa: E402
from phase2_qa import linebreak_issues, narration_item_count_issues, scene_visual_warnings  # noqa: E402
from subtitle_preflight import run_preflight  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--rendered", type=Path, required=True)
    parser.add_argument("--ai", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    data = load_json(args.episode.resolve())
    rendered = args.rendered.resolve()
    ai = args.ai.resolve()
    scene_rows = []
    for scene in data.get("scenes", []):
        scene_id = int(scene["id"])
        path = rendered / f"scene_{scene_id:03d}.png"
        row = {"scene": scene_id, "exists": path.exists(), "warnings": []}
        if path.exists():
            with Image.open(path) as image:
                row["size"] = image.size
            row["warnings"] = scene_visual_warnings(scene, path)
        scene_rows.append(row)
    hashes: dict[str, list[str]] = {}
    ai_rows = []
    for path in sorted(ai.glob("scene_*.png")):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes.setdefault(digest, []).append(path.name)
        with Image.open(path) as image:
            ai_rows.append({"file": path.name, "size": image.size, "sha256": digest})
    duplicate_groups = [names for names in hashes.values() if len(names) > 1]
    subtitle_report = args.report.with_name("subtitle_preflight_machine.md")
    subtitle = run_preflight(args.episode.resolve(), subtitle_report)
    result = {
        "rendered_count": sum(1 for row in scene_rows if row["exists"]),
        "scene_count": len(scene_rows),
        "missing_scenes": [row["scene"] for row in scene_rows if not row["exists"]],
        "scene_rows": scene_rows,
        "ai_rows": ai_rows,
        "ai_duplicate_groups": duplicate_groups,
        "linebreak_issues": linebreak_issues(data),
        "item_count_issues": narration_item_count_issues(data),
        "subtitle": subtitle,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
