"""Render the 24 final scenes (readability版採用) into work/rendered_final_scenes."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from episode_io import load_json  # noqa: E402
from hybrid_scene_renderer import render_episode_scenes  # noqa: E402
from scene_renderer import make_contact_sheet  # noqa: E402

BASE = ROOT / "episodes" / "006_line_talk_backup"
EPISODE = BASE / "episode.json"
AI_DIR = BASE / "work" / "phase_b_review" / "normalized_ai"
TEMPLATE_DIR = BASE / "work" / "rendered_templates"
FINAL_DIR = BASE / "work" / "rendered_final_scenes"


def main() -> None:
    data = load_json(EPISODE)
    result = render_episode_scenes(EPISODE, data, AI_DIR, TEMPLATE_DIR, FINAL_DIR)
    print(f"render status: {result['status']} count={len(result['rendered'])}")
    for error in result.get("errors", []):
        print("ERROR:", error)
    if result["status"] == "PASS":
        scenes = data.get("scenes", [])
        make_contact_sheet(FINAL_DIR, scenes, BASE / "work" / "phase_b_review" / "final_scene_contact_sheet.png")
        print("contact sheet: final_scene_contact_sheet.png")


if __name__ == "__main__":
    main()
