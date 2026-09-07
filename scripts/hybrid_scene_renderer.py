"""Render template/official/gpt_image/hybrid scenes into one final directory.

GPT images are human-approved completed backgrounds.  Generated-image scenes
must be complete ImageGen-native images (or no-text images); large Codex text
overlay is rejected by the NO_IMAGE_TEXT_HYBRID rule.  cover_blur is explicit
fallback only.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageOps

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from episode_io import canonical_text_render_mode, canonical_visual_mode, episode_dir_from_path, load_json  # noqa: E402
from scene_renderer import (  # noqa: E402
    HEIGHT, SAFE_HEIGHT, WIDTH, draw_fitted, draw_headline, draw_section_pill, fit_text_block,
    hex_rgba, load_visual_theme, make_contact_sheet, paint_image_background, paste_asset,
    paste_assets, pil_font, prepare_assets, render_options, render_pillow_scene, rounded_rectangle,
    theme_profile_for_episode,
)


def effective_mode(scene: dict[str, Any]) -> str:
    return str(scene.get("render_mode") or "template")


def ai_image_path(ai_dir: Path, scene_id: int) -> Path:
    return ai_dir / f"scene_{scene_id:03d}.png"


def cover_blur_ai_canvas(ai_image: Image.Image) -> Image.Image:
    """Fill the 1920x900 visual area without stretching the AI subject."""
    source = ai_image.convert("RGBA")
    content_height = HEIGHT - SAFE_HEIGHT
    # The supplied compositions place the subject on the right.  Reuse that
    # same image as the background instead of inventing or redrawing content.
    focus_left = int(source.width * 0.32)
    focus = source.crop((focus_left, 0, source.width, content_height))
    background = ImageOps.fit(
        focus,
        (WIDTH, content_height),
        method=Image.Resampling.LANCZOS,
        centering=(0.55, 0.48),
    ).filter(ImageFilter.GaussianBlur(52))
    background = Image.alpha_composite(
        background,
        Image.new("RGBA", (WIDTH, content_height), (255, 255, 255, 105)),
    )

    canvas = Image.new("RGBA", (WIDTH, HEIGHT), "#f7fbfe")
    canvas.alpha_composite(background, (0, 0))

    sharp_size = (1180, 760)
    sharp = ImageOps.fit(
        focus,
        sharp_size,
        method=Image.Resampling.LANCZOS,
        centering=(0.55, 0.48),
    )
    sharp_left, sharp_top = 660, 50
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        (sharp_left + 8, sharp_top + 10, sharp_left + sharp_size[0] + 8, sharp_top + sharp_size[1] + 10),
        radius=36,
        fill=(31, 63, 95, 46),
    )
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(18)))
    mask = Image.new("L", sharp_size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, sharp_size[0] - 1, sharp_size[1] - 1), radius=34, fill=255
    )
    canvas.paste(sharp, (sharp_left, sharp_top), mask)

    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, HEIGHT - SAFE_HEIGHT, WIDTH, HEIGHT), fill="#f7fbfe")
    draw.line((0, HEIGHT - SAFE_HEIGHT, WIDTH, HEIGHT - SAFE_HEIGHT), fill="#c8deed", width=3)
    return canvas


def draw_overlay_block(
    canvas: Image.Image,
    box: tuple[int, int, int, int],
    text: str,
    max_size: int,
    min_size: int,
    fill: str,
    max_lines: int,
    align: str = "left",
    spacing_ratio: float = 0.14,
    scale: float = 1.0,
) -> None:
    """Draw exact Codex text with a small local scrim, never a full card."""
    draw = ImageDraw.Draw(canvas)
    scaled_max = max(min_size, int(round(max_size * scale)))
    scaled_min = max(40, int(round(min_size * scale)))
    font, _size, lines, line_height = fit_text_block(
        draw, str(text or ""), box[2] - box[0], box[3] - box[1],
        scaled_max, scaled_min, max_lines, spacing_ratio,
    )
    if not lines:
        return
    positions: list[tuple[int, int]] = []
    for index, line in enumerate(lines):
        line_width = int(draw.textlength(line, font=font))
        x = box[0] if align == "left" else box[0] + max(0, (box[2] - box[0] - line_width) // 2)
        positions.append((x, box[1] + index * line_height))
    left = min(x for x, _y in positions) - 18
    top = min(y for _x, y in positions) - 10
    right = max(x + int(draw.textlength(line, font=font)) for (x, _y), line in zip(positions, lines)) + 18
    bottom = max(y for _x, y in positions) + line_height + 8
    scrim = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(scrim).rounded_rectangle((left, top, right, bottom), radius=18, fill=(255, 255, 255, 132))
    canvas.alpha_composite(scrim)
    draw = ImageDraw.Draw(canvas)
    for (x, y), line in zip(positions, lines):
        draw.text(
            (x + 3, y + 4), line, font=font, fill="#27415b",
            stroke_width=5, stroke_fill="#ffffff",
        )
        draw.text(
            (x, y), line, font=font, fill=fill,
            stroke_width=2, stroke_fill="#ffffff",
        )


def validate_ai_images(data: dict[str, Any], ai_dir: Path) -> dict[str, Any]:
    missing: list[str] = []
    invalid: list[str] = []
    safe_area_warnings: list[str] = []
    for scene in data.get("scenes", []):
        if effective_mode(scene) not in {"gpt_image", "hybrid"}:
            continue
        scene_id = int(scene["id"])
        path = ai_image_path(ai_dir, scene_id)
        if not path.exists():
            missing.append(path.name)
            continue
        try:
            with Image.open(path) as image:
                if image.size != (WIDTH, HEIGHT):
                    invalid.append(f"{path.name}: {image.size[0]}x{image.size[1]} (expected 1920x1080)")
                    continue
                rgb = image.convert("RGB")
                sample = rgb.crop((0, HEIGHT - SAFE_HEIGHT, WIDTH, HEIGHT)).resize((120, 12))
                pixels = list(sample.get_flattened_data()) if hasattr(sample, "get_flattened_data") else list(sample.getdata())
                # Full-bleed backgrounds are allowed to be colored in the
                # subtitle band.  Only dark, high-contrast marks are treated
                # as likely foreground content here; pastel background color
                # alone must not turn a valid asset into REVIEW.
                active = sum(1 for pixel in pixels if min(pixel) < 190 and max(pixel) - min(pixel) > 28)
                if active / max(1, len(pixels)) > 0.08:
                    safe_area_warnings.append(f"{path.name}: bottom 180px has visible content")
        except OSError as exc:
            invalid.append(f"{path.name}: broken image ({exc})")
    status = "MISSING" if missing else "FAIL" if invalid else "REVIEW" if safe_area_warnings else "PASS"
    return {"status": status, "missing": missing, "invalid": invalid, "safe_area_warnings": safe_area_warnings}


def overlay_codex_text(canvas: Image.Image, scene: dict[str, Any], left_side: bool = True) -> None:
    if left_side:
        headline_box = (100, 110, 940, 390)
        support_box = (110, 430, 920, 580)
        message_box = (110, 630, 920, 810)
    else:
        headline_box = (980, 110, 1820, 390)
        support_box = (1000, 430, 1800, 580)
        message_box = (1000, 630, 1800, 810)
    options = render_options(scene)
    draw_overlay_block(
        canvas, headline_box, str(scene.get("headline") or ""), 112, 78,
        "#173a68", 3, "left", 0.12, float(options["headline_scale"]),
    )
    draw_overlay_block(
        canvas, support_box, str(scene.get("support_text") or ""), 52, 40,
        "#587187", 3, "left", 0.16,
    )
    draw_overlay_block(
        canvas, message_box, str(scene.get("main_message") or ""), 48, 40,
        "#2f74bb", 3, "left", 0.16,
    )


def _focus_background(theme_profile: str | None, episode_dir: Path | None) -> Image.Image:
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), "#f7fbfe")
    try:
        theme = load_visual_theme(theme_profile or "adult_digital_soft_image_bg")
        paint_image_background(canvas, theme, episode_dir)
    except (FileNotFoundError, OSError):
        pass
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, HEIGHT - SAFE_HEIGHT, WIDTH, HEIGHT), fill=(247, 251, 254, 238))
    draw.line((0, HEIGHT - SAFE_HEIGHT, WIDTH, HEIGHT - SAFE_HEIGHT), fill="#c8deed", width=3)
    return canvas


def _draw_focus_section_pill(draw: ImageDraw.ImageDraw, section_label: str) -> None:
    label = str(section_label or "").strip()
    if not label:
        return
    font = pil_font(48)
    width = int(draw.textlength(label, font=font)) + 58
    rounded_rectangle(draw, (80, 24, 80 + width, 86), 31, "#ffffff", "#c8deed", 3)
    draw.text((109, 30), label, font=font, fill="#2f74bb")


def _draw_step_stack(
    canvas: Image.Image,
    box: tuple[int, int, int, int],
    items: list[str],
    focus_index: int,
) -> None:
    draw = ImageDraw.Draw(canvas)
    left, top, right, bottom = box
    card_gap = 22
    card_h = min(126, max(104, (bottom - top - card_gap * (len(items) - 1)) // max(1, len(items))))
    total_h = card_h * len(items) + card_gap * max(0, len(items) - 1)
    start_y = top + max(0, (bottom - top - total_h) // 2)
    center_x = (left + right) // 2
    if len(items) > 1:
        first_y = start_y + card_h
        last_y = start_y + card_h * 2 + card_gap
        draw.line((center_x, first_y, center_x, last_y), fill="#6ca6d2", width=5)
        arrow_y = start_y + card_h + card_gap // 2
        draw.polygon(
            [(center_x - 14, arrow_y - 7), (center_x + 14, arrow_y - 7), (center_x, arrow_y + 15)],
            fill="#2f74bb",
        )
    for index, item in enumerate(items):
        y = start_y + index * (card_h + card_gap)
        focused = index == focus_index
        fill = "#eaf4ff" if focused else "#ffffff"
        outline = "#2f74bb" if focused else "#c8deed"
        rounded_rectangle(draw, (left, y, right, y + card_h), 24, fill, outline, 4 if focused else 3)
        draw_fitted(draw, (left + 28, y + 22, right - 28, y + card_h - 20), item, 78, 64, "#173a68", 1, "center")


def _draw_focus_highlight(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: str = "#d59c37") -> None:
    draw.rounded_rectangle(box, radius=28, outline=color, width=5)


def render_official_focus_scene(
    scene: dict[str, Any],
    assets: list[Any],
    output: Path,
    theme_profile: str | None,
    episode_dir: Path | None,
    section_label: str,
) -> None:
    """公式UIを主役にしたEpisode 009専用の焦点レイアウト。

    公式素材を描き直さず、既存のPII-free cropを大きく配置する。
    左は操作の順番、右は実画面と「ここを見る」の1箇所だけを示す。
    """
    canvas = _focus_background(theme_profile, episode_dir)
    draw = ImageDraw.Draw(canvas)
    _draw_focus_section_pill(draw, section_label)
    draw_headline(draw, (90, 92, 1830, 230), scene, 112, 88, 1, "center", 0.08)

    variant = str(scene.get("official_focus_variant") or "").lower()
    if variant == "version_open":
        _draw_step_stack(canvas, (90, 290, 670, 820), ["設定", "システム", "バージョン情報"], 2)
        rounded_rectangle(draw, (735, 270, 1830, 840), 34, "#ffffff", "#c8deed", 4)
        draw_fitted(draw, (800, 300, 1765, 372), "実際の画面", 56, 48, "#587187", 1, "left")
        if assets:
            paste_asset(canvas, assets[0], (820, 410, 1745, 690))
            _draw_focus_highlight(draw, (805, 390, 1760, 710))
        draw_fitted(draw, (820, 735, 1745, 805), "「バージョン情報」を開く", 68, 56, "#2f74bb", 1, "center")
    elif variant == "version_field":
        _draw_step_stack(canvas, (90, 310, 610, 820), ["ここを見る", "バージョン"], 1)
        rounded_rectangle(draw, (680, 270, 1830, 840), 34, "#ffffff", "#c8deed", 4)
        draw_fitted(draw, (750, 300, 1760, 370), "Windowsの仕様", 62, 52, "#173a68", 1, "center")
        if assets:
            paste_asset(canvas, assets[0], (820, 395, 1715, 620))
        rounded_rectangle(draw, (805, 650, 1725, 805), 28, "#eaf4ff", "#6ca6d2", 4)
        draw_fitted(draw, (850, 670, 1680, 735), "バージョン（例）", 60, 52, "#587187", 1, "center")
        draw_fitted(draw, (850, 730, 1680, 795), "24H2 / 25H2", 92, 72, "#173a68", 1, "center")
        _draw_focus_highlight(draw, (795, 640, 1735, 815), "#2f74bb")
    elif variant == "update_check":
        _draw_step_stack(canvas, (90, 330, 650, 820), ["設定", "Windows Update"], 1)
        rounded_rectangle(draw, (720, 270, 1830, 840), 34, "#ffffff", "#c8deed", 4)
        draw_fitted(draw, (785, 300, 1765, 390), "更新プログラムのチェック", 68, 56, "#173a68", 1, "center")
        if assets:
            paste_asset(canvas, assets[0], (800, 445, 1755, 785))
            _draw_focus_highlight(draw, (780, 425, 1775, 805))
    else:
        render_official_scene(scene, assets, output)
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, "PNG")


def render_official_scene(scene: dict[str, Any], assets: list[Any], output: Path) -> None:
    if scene.get("full_bleed_asset") and assets and assets[0].image is not None:
        # 承認済みの完成済み1920x1080 assetをそのまま全面表示する。
        # タイトル・説明・素材枠を外側に追加しない（入れ子表示の防止）。
        canvas = assets[0].image.convert("RGB")
        output.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(output, "PNG")
        return
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), "#ffffff")
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, WIDTH, 14), fill="#2f74bb")
    draw.rectangle((0, HEIGHT - SAFE_HEIGHT, WIDTH, HEIGHT), fill="#f7fbfe")
    draw_headline(draw, (100, 70, 1820, 220), scene, 108, 78, 2, "center", 0.12)
    draw_fitted(draw, (130, 225, 1790, 310), str(scene.get("support_text") or ""), 46, 40, "#587187", 2, "center")
    paste_assets(canvas, assets, (120, 330, 1800, 845), vertical=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, "PNG")


def render_ai_scene(scene: dict[str, Any], ai_path: Path, assets: list[Any], output: Path) -> None:
    source = Image.open(ai_path).convert("RGBA")
    mode = effective_mode(scene)
    if canonical_visual_mode(scene) == "invalid_generated_image_text_overlay":
        raise ValueError(
            "NO_IMAGE_TEXT_HYBRID: generated-image scene cannot receive large pil_overlay text"
        )
    fit_mode = str(scene.get("fit_mode") or "full_bleed")
    # GPT assets are human-approved completed backgrounds.  The normal path is
    # exact full-bleed placement; crop only resolves a small aspect mismatch.
    # cover_blur is an explicit last-resort fallback and is never inferred.
    if fit_mode == "cover_blur":
        canvas = cover_blur_ai_canvas(source)
    elif source.size == (WIDTH, HEIGHT):
        canvas = source
    else:
        canvas = ImageOps.fit(source, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)
    if mode == "hybrid":
        paste_assets(canvas, assets, (1080, 170, 1810, 820), vertical=len(assets) > 1)
    # imagegen_native / no_text scenes keep the generated image as-is.  Exact
    # deterministic text belongs to renderer-native template/official scenes;
    # it is never added on top of an AI background.
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, "PNG")


def render_episode_scenes(
    episode_path: Path,
    data: dict[str, Any],
    ai_dir: Path,
    template_dir: Path,
    final_dir: Path,
    only_scene: int | None = None,
) -> dict[str, Any]:
    episode_dir = episode_dir_from_path(episode_path)
    segment_by_id = {int(segment["id"]): segment for segment in data.get("narration_segments", [])}
    theme_profile = theme_profile_for_episode(data)
    rendered: list[str] = []
    errors: list[str] = []
    cache_dir = final_dir / ".asset_cache"
    for scene in data.get("scenes", []):
        scene_id = int(scene["id"])
        if only_scene and scene_id != only_scene:
            continue
        mode = effective_mode(scene)
        output = final_dir / f"scene_{scene_id:03d}.png"
        first = segment_by_id.get(int(scene["start_segment"]), {})
        section = str(scene.get("section_label") or first.get("section") or "")
        assets, missing = prepare_assets(scene, episode_dir, cache_dir)
        if missing:
            errors.extend(missing)
            continue
        if canonical_visual_mode(scene) == "invalid_generated_image_text_overlay":
            errors.append(
                f"scene {scene_id:03d}: NO_IMAGE_TEXT_HYBRID / visual_mode_exclusive violation"
            )
            continue
        try:
            if (
                mode == "template"
                and scene.get("text_render_mode")
                and canonical_text_render_mode(scene) == "imagegen_native"
            ):
                # 恒久ルール（2026-09-03 A/B確定）: 短い見出しが主役の scene は
                # imagegen_native の完成背景を full-bleed でそのまま配置する。
                # 文字は画像内に一体化されているため、Codex の見出し・補足は重ねない
                # （進行 pill などの小さな overlay は呼び出し側で個別に追加可）。
                path = ai_image_path(ai_dir, scene_id)
                if not path.exists():
                    errors.append(f"scene {scene_id:03d}: missing imagegen_native image {path.name}")
                    continue
                render_ai_scene(scene, path, [], output)
            elif mode == "template":
                template_path = template_dir / output.name
                render_pillow_scene(
                    scene,
                    section,
                    assets,
                    template_path,
                    theme_profile=theme_profile,
                    episode_dir=episode_dir,
                )
                output.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(template_path, output)
            elif mode == "official":
                if scene.get("design_variant") in {"capture_focus", "capture_focus_tall"}:
                    # Phase B layout confirmation: keep the capture aperture
                    # visible without inventing a viewer-facing UI or marking
                    # the frame as pending inside the image.  Real device
                    # assets can replace this slot later without changing the
                    # surrounding composition.
                    render_pillow_scene(
                        scene,
                        section,
                        assets,
                        output,
                        theme_profile=theme_profile,
                        episode_dir=episode_dir,
                    )
                elif not assets:
                    errors.append(f"scene {scene_id:03d}: official mode has no official_asset")
                    continue
                elif scene.get("official_focus_variant"):
                    render_official_focus_scene(scene, assets, output, theme_profile, episode_dir, section)
                else:
                    render_official_scene(scene, assets, output)
            elif mode in {"gpt_image", "hybrid"}:
                path = ai_image_path(ai_dir, scene_id)
                if not path.exists():
                    errors.append(f"scene {scene_id:03d}: missing GPT image {path.name}")
                    continue
                if mode == "hybrid" and not assets:
                    errors.append(f"scene {scene_id:03d}: hybrid mode has no official_asset")
                    continue
                render_ai_scene(scene, path, assets, output)
            else:
                errors.append(f"scene {scene_id:03d}: unsupported render_mode {mode}")
                continue
            rendered.append(output.name)
        except (OSError, ValueError) as exc:
            errors.append(f"scene {scene_id:03d}: {exc}")
    scenes = [scene for scene in data.get("scenes", []) if not only_scene or int(scene["id"]) == only_scene]
    if not errors and not only_scene:
        make_contact_sheet(final_dir, scenes, final_dir / "scene_contact_sheet.png")
    return {"status": "PASS" if not errors else "FAIL", "rendered": rendered, "errors": errors}


if __name__ == "__main__":
    raise SystemExit("Use build_episode.py; this module provides renderer functions.")
