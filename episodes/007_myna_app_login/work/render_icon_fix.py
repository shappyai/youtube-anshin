"""Episode 007 アイコン表現修正後の局所再render（SCENE-001/006/010/013/020）。"""
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
TARGETS = [1, 6, 10, 13, 20]


def main() -> None:
    data = load_json(EPISODE)
    for sid in TARGETS:
        result = render_episode_scenes(EPISODE, data, AI_DIR, TEMPLATE_DIR, FINAL_DIR, only_scene=sid)
        print(f"scene {sid:03d}: {result['status']} rendered={result['rendered']} errors={result['errors']}")
    # 全22sceneのcontact sheet v2（5枚は修正版・他17枚はreuse）
    scenes = data.get("scenes", [])
    make_contact_sheet(FINAL_DIR, scenes, BASE / "work" / "phase_b_review" / "scene_contact_sheet_v3.png")
    print("contact sheet v3 saved")


if __name__ == "__main__":
    main()
