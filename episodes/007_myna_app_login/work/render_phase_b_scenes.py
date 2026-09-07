"""Render Episode 007 scenes into work/rendered_final_scenes (Phase B前半)."""
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

BASE = ROOT / "episodes" / "007_myna_app_login"
EPISODE = BASE / "episode.json"
AI_DIR = BASE / "assets" / "generated_ai"
TEMPLATE_DIR = BASE / "work" / "rendered_templates"
FINAL_DIR = BASE / "work" / "rendered_final_scenes"


def main() -> None:
    data = load_json(EPISODE)
    result = render_episode_scenes(EPISODE, data, AI_DIR, TEMPLATE_DIR, FINAL_DIR)
    print(f"render status: {result['status']} count={len(result['rendered'])}")
    for error in result.get("errors", []):
        print("ERROR:", error)
    # 欠落scene（未生成画像）があっても、生成済みsceneのcontact sheetは作る
    missing = [e.split(":")[0] for e in result.get("errors", []) if "missing" in e]
    scenes = [s for s in data.get("scenes", []) if f"scene_{int(s['id']):03d}" not in missing and f"scene_{int(s['id']):03d}.png" not in missing]
    if scenes:
        make_contact_sheet(FINAL_DIR, scenes, BASE / "work" / "phase_b_review" / "scene_contact_sheet.png")
        print(f"contact sheet (partial): scene_contact_sheet.png scenes={len(scenes)}")


if __name__ == "__main__":
    main()

