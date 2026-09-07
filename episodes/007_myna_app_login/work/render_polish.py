# -*- coding: utf-8 -*-
"""Episode 007 Visual polish: imagegen_native 5枚の正規化配置 + 影響scene再render + contact sheet v4."""
from __future__ import annotations
import sys
from pathlib import Path
from PIL import Image, ImageOps

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
RAW = BASE / "work" / "phase_b_review" / "aigen5"
NEW_SCENES = [7, 11, 14, 17, 22]
RERENDER = [1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 15, 16, 18, 19, 20, 21]  # template7+official8+compare1（最終可読性版v6）


def main() -> None:
    data = load_json(EPISODE)
    # 1) imagegen_native 5枚を正規化して正式アセットへ
    for sid in NEW_SCENES:
        raw = RAW / f"scene_{sid:03d}_raw.png"
        if not raw.exists():
            print(f"MISSING raw scene_{sid:03d}")
            continue
        im = Image.open(raw).convert("RGB")
        out = ImageOps.fit(im, (1920, 1080), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        target = AI_DIR / f"scene_{sid:03d}.png"
        out.save(target, "PNG")
        print(f"normalized scene_{sid:03d} {im.size} -> {target.relative_to(ROOT)}")
    # 2) 影響sceneだけ再render（他はreuse）
    for sid in RERENDER:
        result = render_episode_scenes(EPISODE, data, AI_DIR, TEMPLATE_DIR, FINAL_DIR, only_scene=sid)
        print(f"scene {sid:03d}: {result['status']} errors={result['errors']}")
    # 3) contact sheet v4（全22 scene）
    scenes = data.get("scenes", [])
    make_contact_sheet(FINAL_DIR, scenes, BASE / "work" / "phase_b_review" / "scene_contact_sheet_v4.png")
    print("contact sheet v4 saved")


if __name__ == "__main__":
    main()
