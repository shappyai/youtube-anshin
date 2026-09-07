"""Build GPT image-generation manifests for gpt_image/hybrid scenes.

The prompt contract follows docs/text_render_policy.md: ``imagegen_native``
scenes ask ImageGen to render background and exact Japanese text together,
``pil_overlay`` is reserved for renderer-native template/official scenes;
generated-image scenes must not reserve space for a later large text layer.
``no_text`` scenes forbid any readable text in the image.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from episode_io import canonical_text_render_mode, load_json, validate_episode  # noqa: E402

COMMON_PROMPT = (
    "Generate exactly ONE standalone 16:9 image for this scene. "
    "Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. "
    "Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video "
    "for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual "
    "hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. "
    "Do not leave a blank white half or a large empty white area. A text area may be quiet, but it "
    "must remain a real background that continues to the screen edges. No presentation card layout "
    "unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. "
    "No tiny text, no fake official UI, no invented government logos, no unnecessary decoration."
)
MUST_NOT = [
    "collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image",
    "blank white half or large empty white canvas",
    "presentation card layout unless explicitly required by the scene",
    "official UI or app screen",
    "real or invented government logo",
    "fake screenshot",
    "tiny or garbled Japanese text",
    "personal information",
    "content in the bottom 180px subtitle area",
]


def native_text_direction(scene: dict[str, Any]) -> str:
    """ImageGen-native text contract built from the scene, not hardcoded copy."""
    headline = str(scene.get("headline") or "").strip()
    support = str(scene.get("support_text") or "").strip()
    lines = [f"line 1: \"{headline}\""] if headline else []
    if support:
        lines.append(f"line 2: \"{support}\"")
    if not lines:
        lines = ["(no headline or support text declared)"]
    placement = str(scene.get("image_text_placement") or "a calm, low-detail area, upper-left preferred")
    style = str(scene.get("image_text_style") or "white Japanese type with a dark blue outline, high contrast, large and legible")
    return (
        "Render exact Japanese text inside the image, in this order: "
        + " and ".join(lines)
        + ". Spell it correctly: no typos, no missing characters, no extra "
        "characters, no mojibake, no unnatural kanji substitution. Preserve the "
        "declared line order and do not merge or reorder lines. Place the text in "
        + placement
        + ". Use " + style + ". The main headline must stay readable when the image "
        "is scaled down to a smartphone thumbnail. Do not clip the text, do not let "
        "it touch the image edges, and do not place it over the main subject or "
        "important objects. Keep the bottom 180 pixels (subtitle-safe area) free of "
        "text and content."
    )


def no_text_direction() -> str:
    return (
        "This scene must contain NO readable text at all: no letters, no numbers, "
        "no words, no labels, no signage, no captions, no logos, no UI strings, "
        "nothing that can be read as text anywhere in the image."
    )


def pil_overlay_direction(scene: dict[str, Any]) -> str:
    headline = str(scene.get("headline") or "")
    support = str(scene.get("support_text") or "")
    return (
        f"Create a visual-first background for the message '{headline}'. "
        f"Use the supporting idea '{support}'. Place the main focal object where the "
        "composition is visually balanced near the center, and continue the "
        "background to all four edges. This direction is for renderer-native "
        "template/official scenes only; do NOT combine this generated image with "
        "a later large text overlay. Do NOT render any readable text in the image."
    )


def segment_narration(data: dict[str, Any], scene: dict[str, Any]) -> str:
    start, end = int(scene["start_segment"]), int(scene["end_segment"])
    return "".join(str(seg.get("narration") or "") for seg in data.get("narration_segments", []) if start <= int(seg["id"]) <= end)


def build_prompt(scene: dict[str, Any]) -> str:
    custom = str(scene.get("image_prompt") or "").strip()
    text_mode = canonical_text_render_mode(scene)
    if custom:
        contract = (
            "Generation contract: render the declared Japanese text inside the "
            "image exactly as written (imagegen_native)."
            if text_mode == "imagegen_native"
            else "Generation contract: this is one finished standalone scene "
                "background; keep the visual edge-to-edge. This generated image "
                "must not be combined with a later large text overlay."
            if text_mode == "pil_overlay"
            else "Generation contract: this is one finished standalone scene with "
            "NO readable text anywhere in the image."
        )
        return (
            f"{COMMON_PROMPT} Scene direction: {custom} " + contract
        )
    mode = scene.get("render_mode", "template")
    if text_mode == "imagegen_native":
        direction = native_text_direction(scene)
    elif text_mode == "no_text":
        direction = no_text_direction()
    else:
        direction = pil_overlay_direction(scene)
    if mode == "hybrid":
        direction += (
            " Leave a calm, fully painted low-detail slot occupying 35 to 50 percent "
            "for a real official asset added later by Codex; do not make that slot a "
            "blank white panel."
        )
    return COMMON_PROMPT + " Scene direction: " + direction


def must_not_items(text_mode: str) -> list[str]:
    items = list(MUST_NOT)
    if text_mode == "no_text":
        items.extend([
            "any readable text, letters, numbers, words, labels, signage, or captions",
        ])
    return items


def manifest_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for scene in data.get("scenes", []):
        mode = scene.get("render_mode", "template")
        if mode not in {"gpt_image", "hybrid"}:
            continue
        scene_id = int(scene["id"])
        narration = segment_narration(data, scene)
        text_mode = canonical_text_render_mode(scene)
        rows.append({
            "scene_id": f"SCENE-{scene_id:03d}",
            "filename": f"scene_{scene_id:03d}.png",
            "narration": narration,
            "main_message": scene.get("main_message", ""),
            "headline": scene.get("headline", ""),
            "support_text": scene.get("support_text", ""),
            "duration": scene.get("duration") or round(max(2.0, len(narration) / 5.2), 1),
            "render_mode": mode,
            "text_render_mode": text_mode,
            "text_spec": {
                "headline": scene.get("headline", ""),
                "support_text": scene.get("support_text", ""),
                "placement": scene.get("image_text_placement") or "calm low-detail area, upper-left preferred",
                "style": scene.get("image_text_style") or "white Japanese type with dark blue outline, high contrast",
                "aspect_ratio": scene.get("image_aspect_ratio") or "16:9",
            },
            "text_qa": {"status": "pending", "retry_count": 0, "fallback": None},
            "fit_mode": scene.get("fit_mode", "full_bleed"),
            "background_fill": scene.get("background_fill", "none"),
            "animation_default": scene.get("animation", "static"),
            "image_prompt": build_prompt(scene),
            "official_asset": scene.get("official_asset", []),
            "official_asset_slot": scene.get("official_asset_slot", "right 35-50%" if mode == "hybrid" else None),
            "safe_area": {"canvas": [1920, 1080], "content": [0, 0, 1920, 900]},
            "bottom_subtitle_reserved": 180,
            "asset_contract": {
                "format": "PNG",
                "width": 1920,
                "height": 1080,
                "one_scene_per_image": True,
                "full_frame": True,
            },
            "must_not_generate": must_not_items(text_mode),
            "status": "image_required",
        })
    return rows


def write_manifest(rows: list[dict[str, Any]], json_path: Path, md_path: Path) -> None:
    payload = {
        "version": "2.0",
        "prompt_contract": "one_scene_full_frame_text_v2",
        "image_count": len(rows),
        "scenes": rows,
    }
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# GPT image generation manifest", "",
        f"Required images: {len(rows)}", "",
        "text_render_mode: imagegen_native = ImageGenで背景と文字を同時生成（QA必須）・"
        "pil_overlay = 背景のみ生成しPIL/HTMLで文字後乗せ・no_text = 画像内に文字なし。"
        "詳細は docs/text_render_policy.md。", "",
    ]
    for row in rows:
        lines.extend([
            f"## {row['scene_id']} — {row['render_mode']} / text_render_mode={row['text_render_mode']}", "",
            f"- filename: `{row['filename']}`", f"- text_render_mode: `{row['text_render_mode']}`",
            f"- fit_mode: `{row['fit_mode']}`", f"- animation_default: `{row['animation_default']}`",
            f"- text_qa: `{row['text_qa']['status']}`（retry={row['text_qa']['retry_count']}）",
            f"- status: `{row['status']}`", "",
        ])
        if row["text_render_mode"] == "imagegen_native":
            text_spec = row["text_spec"]
            lines.extend([
                "### Text spec（imagegen_native文字QAの正）", "",
                f"- headline: `{text_spec['headline']}`",
                f"- support_text: `{text_spec['support_text']}`",
                f"- placement: {text_spec['placement']}",
                f"- style: {text_spec['style']}",
                f"- aspect_ratio: {text_spec['aspect_ratio']}", "",
            ])
        lines.extend([
            "### Prompt", "", row["image_prompt"], "",
            "### Must not generate", "", *[f"- {item}" for item in row["must_not_generate"]], "",
        ])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("episode", type=Path)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--markdown", type=Path)
    args = parser.parse_args()
    data = load_json(args.episode.resolve())
    issues = validate_episode(data)
    if issues:
        raise SystemExit("episode.json validation failed:\n- " + "\n- ".join(issues))
    rows = manifest_rows(data)
    work = args.episode.parent / "work"
    json_path = (args.json or work / "image_generation_manifest.json").resolve()
    md_path = (args.markdown or work / "image_generation_manifest.md").resolve()
    write_manifest(rows, json_path, md_path)
    print(f"image_generation_manifest={len(rows)} json={json_path} markdown={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
