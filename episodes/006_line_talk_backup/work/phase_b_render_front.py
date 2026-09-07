from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

ROOT = Path(r"C:\Codex\260829_youtube-anshin")
EPISODE_DIR = ROOT / "episodes" / "006_line_talk_backup"
EPISODE_JSON = EPISODE_DIR / "episode.json"
ORIGINAL_AI = EPISODE_DIR / "assets" / "generated_ai"
REVIEW_DIR = EPISODE_DIR / "work" / "phase_b_review"
NORMALIZED_AI = REVIEW_DIR / "normalized_ai"
RENDERED_DIR = REVIEW_DIR / "rendered_final_scenes"
TEMPLATE_DIR = REVIEW_DIR / "rendered_template_scenes"
sys.path.insert(0, str(ROOT / "scripts"))

from create_channel_cta import build_cta  # noqa: E402
from episode_io import load_json  # noqa: E402
from hybrid_scene_renderer import render_episode_scenes, validate_ai_images  # noqa: E402
from scene_renderer import HEIGHT, WIDTH, make_contact_sheet  # noqa: E402


def normalize_ai_images(data: dict) -> list[dict]:
    NORMALIZED_AI.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    for scene in data.get("scenes", []):
        if scene.get("render_mode") not in {"gpt_image", "hybrid"}:
            continue
        scene_id = int(scene["id"])
        source = ORIGINAL_AI / f"scene_{scene_id:03d}.png"
        target = NORMALIZED_AI / source.name
        with Image.open(source) as image:
            normalized = ImageOps.fit(image.convert("RGB"), (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)
            # Reserve the dedicated subtitle band in the render copy.  The
            # generated original remains untouched for provenance/review.
            draw = ImageDraw.Draw(normalized)
            draw.rectangle((0, HEIGHT - 180, WIDTH, HEIGHT), fill="#f7fbfe")
            draw.line((0, HEIGHT - 180, WIDTH, HEIGHT - 180), fill="#c8deed", width=3)
            normalized.save(target, "PNG", optimize=True)
        results.append({"scene_id": scene_id, "source": str(source), "normalized": str(target), "size": [WIDTH, HEIGHT]})
    return results


def main() -> None:
    data = load_json(EPISODE_JSON)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    normalized = normalize_ai_images(data)
    cta_path = EPISODE_DIR / "work" / "channel_cta.png"
    build_cta(ROOT / "config" / "channel_cta.json", cta_path)
    ai_validation = validate_ai_images(data, NORMALIZED_AI)
    render_result = render_episode_scenes(EPISODE_JSON, data, NORMALIZED_AI, TEMPLATE_DIR, RENDERED_DIR)
    if render_result.get("status") == "PASS":
        full_contact = RENDERED_DIR / "scene_contact_sheet.png"
        shutil.copy2(full_contact, REVIEW_DIR / "scene_contact_sheet.png")
        gpt_scenes = [scene for scene in data.get("scenes", []) if scene.get("render_mode") in {"gpt_image", "hybrid"}]
        make_contact_sheet(RENDERED_DIR, gpt_scenes, REVIEW_DIR / "gpt_image_contact_sheet.png")
    result = {
        "normalized_ai": normalized,
        "ai_validation": ai_validation,
        "render": render_result,
        "rendered_scene_count": len(render_result.get("rendered", [])),
        "total_scene_count": len(data.get("scenes", [])),
        "cta_path": str(cta_path),
        "contact_sheet": str(REVIEW_DIR / "scene_contact_sheet.png"),
        "gpt_contact_sheet": str(REVIEW_DIR / "gpt_image_contact_sheet.png"),
    }
    (REVIEW_DIR / "render_front_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
