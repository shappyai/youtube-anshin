"""Render Episode 005 scenes for Phase B review without audio/video build."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from episode_io import load_json  # noqa: E402
from hybrid_scene_renderer import render_episode_scenes, validate_ai_images  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    episode = args.episode.resolve()
    output = args.output.resolve()
    data = load_json(episode)
    template_dir = output / "template_scenes"
    normalized_ai_dir = output / "normalized_ai"
    ai_dir = normalized_ai_dir if normalized_ai_dir.exists() else episode.parent / "assets" / "generated_ai"
    result = render_episode_scenes(episode, data, ai_dir, template_dir, output / "rendered_scenes")
    print(json.dumps({"ai": validate_ai_images(data, ai_dir), "render": result}, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
