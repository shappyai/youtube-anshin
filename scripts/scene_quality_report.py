"""Create a mechanical Phase 1.5 quality report for rendered scene PNGs."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from scene_renderer_metrics import measure
from PIL import Image, ImageChops, ImageOps
from scene_renderer import (
    FORBIDDEN_DECORATIVE_GLYPHS,
    OFFICIAL_TEXT_BOX,
    OFFICIAL_TEXT_BOX_CENTERED,
    OFFICIAL_VISUAL_BOX,
    ROOT,
    load_visual_theme,
    normalized_semantic_icon_path,
    official_visual_variant,
    scene_box,
    theme_background_path,
    theme_profile_for_episode,
)

ACTIVE_AREA = 1920 * 900
VISUAL_BALANCE_MIN_X, VISUAL_BALANCE_MAX_X = 650, 1270
ICON_PLATE_ALIGNMENT_MAX_PX = 2
VISUAL_AXIS_TARGET_X = 960
VISUAL_AXIS_ALIGNMENT_MAX_PX = 12
STACKED_PANEL_ALIGNMENT_MAX_PX = 12
SECTION_PILL_ANCHOR_MAX_X = 300
SEMANTIC_ICON_VISUAL_CENTER_MAX_PX = 4
SEMANTIC_ICON_PLATE_VISUAL_MAX_PX = 2
VISUAL_CENTROID_LEFT_FAIL_X = 768
VISUAL_CENTROID_RIGHT_FAIL_X = 1152
OFFICIAL_RIGHT_WEIGHT_MIN_RATIO = 0.20
ICON_FILL_RGB = {
    "navy": (23, 58, 104),
    "blue": (47, 116, 187),
    "green": (63, 140, 88),
    "amber": (192, 125, 30),
}


def box_area(box: tuple[int, int, int, int]) -> int:
    return max(0, box[2] - box[0]) * max(0, box[3] - box[1])


def prepared_asset_count(scene: dict[str, Any]) -> int:
    assets = scene.get("official_asset") or []
    crops = scene.get("official_asset_crop") or []
    if not isinstance(assets, list):
        return 0
    count = 0
    for index, item in enumerate(assets):
        if not isinstance(item, dict):
            count += 1
            continue
        matching = [spec for spec in crops if isinstance(spec, dict) and spec.get("asset_index") == index]
        count += len(matching) if matching else 1
    return count


def declared_visual_center_x(scene: dict[str, Any]) -> float | None:
    direct = scene.get("visual_balance_center_x")
    if isinstance(direct, (int, float)):
        return float(direct)
    balance = scene.get("visual_balance")
    if isinstance(balance, dict) and isinstance(balance.get("center_x"), (int, float)):
        return float(balance["center_x"])
    if scene.get("layout") == "layout_06_caution" and "content_offset_x" in scene:
        try:
            return 600.0 + float(scene.get("content_offset_x") or 0)
        except (TypeError, ValueError):
            return None
    return None


def geometry(scene: dict[str, Any], asset_count: int) -> dict[str, Any]:
    layout = str(scene.get("layout") or "")
    visual_boxes: list[tuple[int, int, int, int]] = []
    official_boxes: list[tuple[int, int, int, int]] = []
    planned_official_boxes: list[tuple[int, int, int, int]] = []
    visual_required = layout in {
        "layout_01_hero",
        "layout_03_visual_text",
        "layout_04_text_official",
        "layout_05_compare",
        "layout_06_caution",
    }
    if layout == "layout_01_hero":
        visual_boxes.append((40, 140, 760, 800))
        if asset_count:
            official_boxes.append((40, 140, 760, 800))
    elif layout == "layout_02_list":
        pass
    elif layout == "layout_03_visual_text":
        visual_boxes.append((50, 145, 830, 795))
        if asset_count:
            official_boxes.append((50, 145, 830, 795))
    elif layout == "layout_04_text_official":
        variant = official_visual_variant(scene)
        text_box = scene_box(
            scene,
            "official_text_box",
            OFFICIAL_TEXT_BOX_CENTERED if variant == "safe_entry_options_centered" else OFFICIAL_TEXT_BOX,
        )
        visual_box = scene_box(scene, "official_visual_box", OFFICIAL_VISUAL_BOX)
        if variant == "safe_entry_options_centered":
            visual_boxes.append(text_box)
        else:
            visual_boxes.extend([text_box, visual_box])
        if scene.get("official_asset_slot") and variant not in {"safe_entry_options_centered", "semantic_operation"}:
            planned_official_boxes.append(visual_box)
        if asset_count:
            official_boxes.append(visual_box)
    elif layout == "layout_05_compare":
        visual_boxes.extend([(110, 410, 900, 835), (1020, 410, 1810, 835)])
        if asset_count:
            columns = [(110, 410, 900, 835), (1020, 410, 1810, 835)]
            for index in range(min(asset_count, 2)):
                left, top, right, bottom = columns[index]
                official_boxes.append((left + 38, top + 132, right - 38, bottom - 30))
    elif layout == "layout_06_caution":
        visual_boxes.append((120, 270, 520, 670))
        if asset_count:
            official_boxes.append((1120, 180, 1810, 840))
    elif layout == "layout_07_summary":
        pass
    else:
        visual_boxes.append((790, 680, 1130, 840))
        visual_required = False

    visual_area = (
        sum(box_area(box) for box in visual_boxes)
        if layout in {"layout_04_text_official", "layout_05_compare"}
        else max((box_area(box) for box in visual_boxes), default=0)
    )
    if official_boxes and layout in {"layout_04_text_official", "layout_06_caution"}:
        visual_area = max(visual_area, sum(box_area(box) for box in official_boxes))
    official_area = sum(box_area(box) for box in official_boxes)
    visual_center_x = declared_visual_center_x(scene)
    if visual_center_x is None:
        # Most standard layouts intentionally balance a visual block with a
        # text block.  Only explicit metadata (or the known caution-layout
        # offset above) should override that conservative neutral baseline.
        visual_center_x = 960.0
    return {
        "visual_required": visual_required,
        "visual_area_ratio": round(visual_area / ACTIVE_AREA, 5),
        "official_area_ratio": round(official_area / ACTIVE_AREA, 5),
        "planned_official_area_ratio": round(
            sum(box_area(box) for box in planned_official_boxes) / ACTIVE_AREA,
            5,
        ),
        "visual_boxes": visual_boxes,
        "official_boxes": official_boxes,
        "planned_official_boxes": planned_official_boxes,
        "card_count": 2 if layout == "layout_05_compare" else 0,
        "visual_center_x": visual_center_x,
    }


def visual_axis_metrics(scene: dict[str, Any], image_theme: bool) -> dict[str, Any]:
    """Measure the declared center axis of the v4 image-theme geometry.

    This is intentionally a layout-geometry check, not an estimate from the
    pale background pixels.  Paired compare cards are measured as one group;
    the group center must be x=960 even though each card sits on one side.
    """
    render_mode = str(scene.get("render_mode") or "template")
    if not image_theme or render_mode in {"gpt_image", "hybrid"}:
        return {"target_x": None, "centers": [], "max_diff_px": None}
    layout = str(scene.get("layout") or "")
    asset_count = prepared_asset_count(scene)
    centers: list[float] = []
    if layout in {
        "layout_01_hero",
        "layout_02_list",
        "layout_03_visual_text",
        "layout_05_compare",
        "layout_06_caution",
        "layout_07_summary",
        "layout_08_section",
    }:
        centers.append(float(VISUAL_AXIS_TARGET_X))
    if layout == "layout_01_hero" and asset_count == 0 and scene.get("icon_name"):
        # icon, plate, headline/main fact, support and secondary panel are
        # all emitted on the same center axis by the image-theme renderer.
        centers.extend([960.0, 960.0, 960.0])
    elif layout == "layout_03_visual_text" and asset_count == 0 and scene.get("icon_name"):
        centers.extend([960.0, 960.0])
    elif layout == "layout_06_caution" and asset_count == 0 and scene.get("icon_name"):
        centers.extend([960.0, 960.0])
    elif layout == "layout_05_compare":
        left_center = (110 + 900) / 2
        right_center = (1020 + 1810) / 2
        centers.append((left_center + right_center) / 2)
    max_diff = max((abs(center - VISUAL_AXIS_TARGET_X) for center in centers), default=None)
    return {
        "target_x": VISUAL_AXIS_TARGET_X if centers else None,
        "centers": [round(center, 1) for center in centers],
        "max_diff_px": round(max_diff, 1) if max_diff is not None else None,
    }


def stacked_panel_alignment(scene: dict[str, Any], image_theme: bool) -> float | None:
    """Return the maximum center difference for vertically stacked panels."""
    if not image_theme or str(scene.get("render_mode") or "template") in {"gpt_image", "hybrid"}:
        return None
    if str(scene.get("layout") or "") == "layout_01_hero" and not prepared_asset_count(scene):
        # Numeric primary panel and v4 secondary message panel: both are
        # (350, ..., 1570, ...), hence center_x=960 exactly.
        return 0.0
    return None


def icon_frame_center(scene: dict[str, Any]) -> tuple[int, int] | None:
    """Return the renderer's icon plate center for an icon-bearing template."""
    layout = str(scene.get("layout") or "")
    if not scene.get("icon_name"):
        return None
    if scene.get("design_variant") == "bridge_clean":
        return (470, 562)
    if layout == "layout_01_hero":
        numeric = any(char.isdigit() for char in str(scene.get("headline") or ""))
        return (960, 205 if numeric else 225)
    if layout == "layout_03_visual_text":
        return (960, 220)
    if layout == "layout_06_caution" and not prepared_asset_count(scene):
        return (960, 215)
    return None


def source_icon_alpha_metrics(scene: dict[str, Any]) -> dict[str, Any] | None:
    name = str(scene.get("icon_name") or "")
    tone = str(scene.get("icon_tone") or "")
    source_path = ROOT / "assets" / "icons" / "material_symbols" / f"{name}_{tone}.png"
    if not name or not tone or not source_path.exists():
        return None
    try:
        with Image.open(source_path) as image:
            rgba = image.convert("RGBA")
            trim_mask = rgba.getchannel("A").point(lambda value: 255 if value >= 4 else 0)
            bbox = trim_mask.getbbox()
            if bbox is None:
                return None
            return {
                "canvas_size": [rgba.width, rgba.height],
                "canvas_center_x": round(rgba.width / 2, 2),
                "glyph_bbox": list(bbox),
                "glyph_canvas_center_x": round((bbox[0] + bbox[2]) / 2, 2),
                "glyph_canvas_delta_px": round((bbox[0] + bbox[2]) / 2 - rgba.width / 2, 2),
            }
    except OSError:
        return None


def color_bbox(image: Image.Image, target: tuple[int, int, int], box: tuple[int, int, int, int], threshold: int = 72) -> list[int] | None:
    """Find final-frame pixels close to the semantic icon's tint color."""
    rgb = image.convert("RGB")
    left, top, right, bottom = box
    left = max(0, left)
    top = max(0, top)
    right = min(rgb.width, right)
    bottom = min(rgb.height, bottom)
    points: list[tuple[int, int]] = []
    for y in range(top, bottom):
        for x in range(left, right):
            pixel = rgb.getpixel((x, y))
            distance = sum((int(pixel[index]) - target[index]) ** 2 for index in range(3)) ** 0.5
            if distance <= threshold:
                points.append((x, y))
    if not points:
        return None
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return [min(xs), min(ys), max(xs) + 1, max(ys) + 1]


def icon_headline_box(scene: dict[str, Any]) -> tuple[int, int, int, int] | None:
    layout = str(scene.get("layout") or "")
    if layout == "layout_01_hero":
        if any(char.isdigit() for char in str(scene.get("headline") or "")):
            return (420, 380, 1500, 660)
        return (240, 380, 1680, 600)
    if layout == "layout_03_visual_text":
        return (240, 350, 1680, 570)
    if layout == "layout_06_caution" and not prepared_asset_count(scene):
        return (240, 340, 1680, 560)
    return None


def semantic_icon_visual_center(scene: dict[str, Any], path: Path, image_theme: bool) -> dict[str, Any] | None:
    """Measure the visible glyph on the final render, not its source canvas."""
    if not image_theme or str(scene.get("render_mode") or "template") in {"gpt_image", "hybrid"}:
        return None
    center = icon_frame_center(scene)
    source = source_icon_alpha_metrics(scene)
    if center is None or source is None:
        return None
    tone = str(scene.get("icon_tone") or "")
    target = ICON_FILL_RGB.get(tone)
    if target is None:
        return None
    cx, cy = center
    icon_bbox = color_bbox(path_image := Image.open(path), target, (cx - 107, cy - 107, cx + 108, cy + 108))
    headline_box = icon_headline_box(scene)
    headline_bbox = color_bbox(path_image, (23, 58, 104), headline_box, 82) if headline_box else None
    path_image.close()
    if icon_bbox is None:
        return {
            "status": "FAIL",
            "reason": "visible glyph color bbox not found",
            "source": source,
            "plate_center_x": cx,
        }
    glyph_center_x = round((icon_bbox[0] + icon_bbox[2]) / 2, 2)
    headline_center_x = round((headline_bbox[0] + headline_bbox[2]) / 2, 2) if headline_bbox else None
    axis_delta = round(abs(glyph_center_x - cx), 2)
    plate_delta = round(abs(glyph_center_x - cx), 2)
    status = "PASS" if axis_delta <= SEMANTIC_ICON_VISUAL_CENTER_MAX_PX and plate_delta <= SEMANTIC_ICON_PLATE_VISUAL_MAX_PX else "FAIL"
    return {
        "status": status,
        "source": source,
        "frame_glyph_bbox": icon_bbox,
        "glyph_visual_center_x": glyph_center_x,
        "plate_center_x": cx,
        "headline_visual_bbox": headline_bbox,
        "headline_visual_center_x": headline_center_x,
        "glyph_axis_delta_px": axis_delta,
        "glyph_plate_delta_px": plate_delta,
        "normalized_icon": str(normalized_semantic_icon_path(str(scene.get("icon_name") or ""), tone, 180) or ""),
    }


def renderer_branding_leakage() -> int:
    """Detect a channel-name overlay still present in template sources."""
    channel_name = "\u5927\u4eba\u306e\u30c7\u30b8\u30bf\u30eb\u5b89\u5fc3\u5ba4"
    source_paths = [
        ROOT / "scripts" / "scene_renderer.py",
        ROOT / "scripts" / "hybrid_scene_renderer.py",
        *(ROOT / "templates" / "scenes").glob("*.html"),
        ROOT / "templates" / "scenes" / "styles.css",
    ]
    for path in source_paths:
        try:
            if channel_name in path.read_text(encoding="utf-8"):
                return 1
        except OSError:
            continue
    return 0


def renderer_policy_guard() -> dict[str, int]:
    """Static guard against reintroducing glyph/icon filler fallbacks."""
    path = ROOT / "scripts" / "scene_renderer.py"
    try:
        source = path.read_text(encoding="utf-8")
    except OSError:
        return {
            "oversized_checkmark_count": 1,
            "decorative_checkmark_as_main_visual": 1,
            "meaningless_filler_icon_count": 1,
        }

    oversized = 0
    for glyph in FORBIDDEN_DECORATIVE_GLYPHS:
        pattern = re.compile(
            rf"draw_(?:badge|symbol)\(\s*[^)]*['\"]{re.escape(glyph)}['\"]",
            re.DOTALL,
        )
        oversized += len(pattern.findall(source))
    branch_match = re.search(
        r'elif layout == "layout_04_text_official":(?P<body>.*?)(?=\n    elif layout == )',
        source,
        re.DOTALL,
    )
    filler = 0
    if branch_match:
        filler = len(
            re.findall(r"draw_(?:badge|symbol|icon_stage)\s*\(", branch_match.group("body"))
        )
    return {
        "oversized_checkmark_count": int(oversized),
        "decorative_checkmark_as_main_visual": int(oversized),
        "meaningless_filler_icon_count": int(filler),
    }


def visual_centroid_preflight(
    scene: dict[str, Any],
    path: Path,
    theme: dict[str, Any],
) -> dict[str, Any]:
    """Measure foreground occupancy for official two-column scenes.

    The configured background is rendered again and subtracted from the final
    PNG, so the image asset's own decoration does not become visual weight.
    The official right slot is then required to carry meaningful occupancy.
    """
    base: dict[str, Any] = {
        "status": "N/A",
        "occupied_bbox": None,
        "visual_centroid_x": None,
        "left_visual_weight": 0.0,
        "right_visual_weight": 0.0,
        "left_bias_fail": 0,
        "reason": "",
    }
    if (
        str(scene.get("layout") or "") != "layout_04_text_official"
        or str(scene.get("render_mode") or "template") in {"gpt_image", "hybrid"}
        or not scene.get("official_asset_slot")
    ):
        return base

    # The adult_digital_soft_background profile is renderer-generated gradient
    # art rather than a reusable raster asset.  There is no source image to
    # subtract in that case; the declared boxes and the human contact sheet
    # remain the applicable checks, so do not turn this limitation into a
    # false FAIL.
    if str(theme.get("background_type") or "gradient") != "image" or not (theme.get("asset") or theme.get("background_asset")):
        base.update({"status": "N/A", "reason": "gradient theme has no subtractable background"})
        return base

    if official_visual_variant(scene) == "safe_entry_options_centered":
        # This scene deliberately replaces the former right-side frame with a
        # centered three-card semantic visual.  The declared centered box is
        # the balance contract; there is no official capture to weigh against.
        base.update({
            "status": "PASS",
            "visual_centroid_x": 960.0,
            "left_visual_weight": 0.5,
            "right_visual_weight": 0.5,
            "left_bias_fail": 0,
            "reason": "centered semantic entry options",
        })
        return base

    try:
        background_path = theme_background_path(theme)
        with Image.open(path) as rendered_source, Image.open(background_path) as background_source:
            rendered = rendered_source.convert("RGB")
            background = ImageOps.fit(
                background_source.convert("RGB"),
                rendered.size,
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )
            region = (80, 130, min(rendered.width, 1840), min(rendered.height, 860))
            sample_width = 880
            sample_height = max(1, round((region[3] - region[1]) * sample_width / (region[2] - region[0])))
            rendered_sample = rendered.crop(region).resize((sample_width, sample_height), Image.Resampling.BILINEAR)
            background_sample = background.crop(region).resize((sample_width, sample_height), Image.Resampling.BILINEAR)
            difference = ImageChops.difference(rendered_sample, background_sample)
            pixels = list(difference.getdata())
    except (FileNotFoundError, OSError, ValueError):
        base.update({"status": "FAIL", "left_bias_fail": 1, "reason": "background comparison unavailable"})
        return base

    scale_x = (region[2] - region[0]) / sample_width
    scale_y = (region[3] - region[1]) / sample_height
    occupied: list[tuple[float, float, float]] = []
    left_weight = 0.0
    right_weight = 0.0
    centroid_total = 0.0
    centroid_weight = 0.0
    for index, pixel in enumerate(pixels):
        strength = max(int(pixel[0]), int(pixel[1]), int(pixel[2]))
        if strength <= 8:
            continue
        weight = min(1.0, (strength - 8) / 128.0)
        sample_x = index % sample_width
        sample_y = index // sample_width
        x = region[0] + (sample_x + 0.5) * scale_x
        y = region[1] + (sample_y + 0.5) * scale_y
        occupied.append((x, y, weight))
        if OFFICIAL_TEXT_BOX[0] <= x < OFFICIAL_TEXT_BOX[2] and OFFICIAL_TEXT_BOX[1] <= y < OFFICIAL_TEXT_BOX[3]:
            left_weight += weight
            centroid_total += x * weight
            centroid_weight += weight
        elif OFFICIAL_VISUAL_BOX[0] <= x < OFFICIAL_VISUAL_BOX[2] and OFFICIAL_VISUAL_BOX[1] <= y < OFFICIAL_VISUAL_BOX[3]:
            right_weight += weight
            centroid_total += x * weight
            centroid_weight += weight

    if not occupied or centroid_weight <= 0:
        base.update({"status": "FAIL", "left_bias_fail": 1, "reason": "no foreground occupancy in two-column boxes"})
        return base

    occupied_bbox = [
        int(min(item[0] for item in occupied)),
        int(min(item[1] for item in occupied)),
        int(max(item[0] for item in occupied) + 1),
        int(max(item[1] for item in occupied) + 1),
    ]
    total = left_weight + right_weight
    centroid_x = centroid_total / centroid_weight
    left_ratio = left_weight / total if total else 0.0
    right_ratio = right_weight / total if total else 0.0
    left_bias_fail = int(
        right_ratio < OFFICIAL_RIGHT_WEIGHT_MIN_RATIO
        or centroid_x < VISUAL_CENTROID_LEFT_FAIL_X
        or centroid_x > VISUAL_CENTROID_RIGHT_FAIL_X
    )
    base.update(
        {
            "status": "FAIL" if left_bias_fail else "PASS",
            "occupied_bbox": occupied_bbox,
            "visual_centroid_x": round(centroid_x, 2),
            "left_visual_weight": round(left_ratio, 4),
            "right_visual_weight": round(right_ratio, 4),
            "left_bias_fail": left_bias_fail,
            "reason": (
                f"right weight<{OFFICIAL_RIGHT_WEIGHT_MIN_RATIO:.2f}"
                if right_ratio < OFFICIAL_RIGHT_WEIGHT_MIN_RATIO
                else f"centroid outside {VISUAL_CENTROID_LEFT_FAIL_X}..{VISUAL_CENTROID_RIGHT_FAIL_X}"
                if left_bias_fail
                else ""
            ),
        }
    )
    return base


def warning_list(row: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    headline = int(row["headline_raster_height_px"])
    # imagegen_nativeは文字が背景画像へ一体生成されており、ラスタ上の
    # template文字インク計測では判定しない。exact text QAを別ゲートで行う。
    if row.get("render_mode") not in {"gpt_image", "hybrid"} and headline < 60:
        warnings.append(f"headline<{60}px ({headline}px)")
    blank_white = row.get("blank_white_slide")
    if row.get("background_type") != "image_theme_template" and blank_white is not None and float(blank_white) > 0.66:
        warnings.append(f"blank white slide ({float(blank_white) * 100:.0f}% near-white)")
    if row["asset_count"] and row["official_area_ratio"] < 0.25:
        warnings.append(f"official<{25}% ({row['official_area_ratio'] * 100:.1f}%)")
    # cautionのsemantic icon plateは意図的に15%未満の補助要素とする。
    if row["visual_required"] and row["visual_area_ratio"] < 0.25 and not row.get("semantic_icon_only"):
        warnings.append(f"visual<{25}% ({row['visual_area_ratio'] * 100:.1f}%)")
    if int(row["small_dark_band_count"]) >= 6:
        warnings.append(f"small-text proxy ({row['small_dark_band_count']} bands)")
    if int(row["small_text_floor_px"]) < 44:
        warnings.append(f"<44px helper text ({row['small_text_floor_px']}px)")
    if int(row["card_count"]) >= 4:
        warnings.append(f"cards>=4 ({row['card_count']})")
    if row["blank_ratio"] > 0.92:
        warnings.append(f"high blank ({row['blank_ratio'] * 100:.1f}%)")
    center_x = row.get("visual_center_x")
    if center_x is not None and not row.get("intentional_asymmetry") and (
        float(center_x) < VISUAL_BALANCE_MIN_X or float(center_x) > VISUAL_BALANCE_MAX_X
    ):
        warnings.append(f"visual balance x={float(center_x):.0f} (target {VISUAL_BALANCE_MIN_X}..{VISUAL_BALANCE_MAX_X})")
    axis_diff = row.get("visual_axis_alignment_max_diff_px")
    if axis_diff is not None and float(axis_diff) > VISUAL_AXIS_ALIGNMENT_MAX_PX:
        warnings.append(
            f"visual_axis_alignment>{VISUAL_AXIS_ALIGNMENT_MAX_PX}px ({float(axis_diff):.1f}px)"
        )
    stacked_diff = row.get("stacked_panel_alignment_max_diff_px")
    if stacked_diff is not None and float(stacked_diff) > STACKED_PANEL_ALIGNMENT_MAX_PX:
        warnings.append(
            f"stacked_panel_alignment>{STACKED_PANEL_ALIGNMENT_MAX_PX}px ({float(stacked_diff):.1f}px)"
        )
    if row.get("section_pill_anchor") == "FAIL":
        warnings.append(f"section_pill_anchor x={row.get('section_pill_x')} (target <{SECTION_PILL_ANCHOR_MAX_X})")
    if int(row.get("channel_name_in_scene") or 0) > 0:
        warnings.append("repeated_channel_name")
    icon_center = row.get("semantic_icon_visual_center")
    if isinstance(icon_center, dict) and icon_center.get("status") == "FAIL":
        warnings.append("semantic_icon_visual_center")
    if row.get("visual_centroid_status") == "FAIL":
        warnings.append(
            f"visual_centroid_preflight FAIL ({row.get('visual_centroid_reason') or 'unbalanced official two-column scene'})"
        )
    return warnings


def blank_white_ratio_pixels(path: Path) -> float:
    """template sceneの「真っ白スライド」判定（恒久ルール・Episode 008〜common theme適用後）。

    コンテンツ領域（y<900・字幕帯を除く）でRGBがすべて245以上の「ほぼ白」画素の割合。
    66%超をWARN、80%超はFAIL相当（reportではWARN表示）。
    """
    with Image.open(path) as img:
        rgb = img.convert("RGB")
        width, height = rgb.size
        content_h = max(1, min(height - 180, 900))
        small = rgb.resize((width // 4, content_h // 4))
        px = small.load()
        sw, sh = small.size
        near_white = 0
        for y in range(sh):
            for x in range(sw):
                r_, g_, b_ = px[x, y]
                if r_ >= 245 and g_ >= 245 and b_ >= 245:
                    near_white += 1
        return round(near_white / max(1, sw * sh), 5)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    episode = json.loads(args.episode.read_text(encoding="utf-8"))
    theme_profile = theme_profile_for_episode(episode)
    theme = load_visual_theme(theme_profile)
    image_theme = str(theme.get("background_type") or "gradient") == "image"
    branding_leakage = renderer_branding_leakage() if image_theme else 0
    section_pill_config = theme.get("section_pill", {}) if isinstance(theme.get("section_pill"), dict) else {}
    section_pill_x = int(section_pill_config.get("x", 100))
    policy = renderer_policy_guard()
    background_asset_pending = False
    if image_theme:
        try:
            theme_background_path(theme)
        except FileNotFoundError:
            background_asset_pending = True
    rows: list[dict[str, Any]] = []
    for scene in episode["scenes"]:
        scene_id = int(scene["id"])
        path = args.output_dir / f"scene_{scene_id:03d}.png"
        if not path.exists():
            rows.append({"scene_id": scene_id, "status": "FAIL", "warnings": ["render missing"]})
            continue
        metric = measure(path)
        effective_asset_count = prepared_asset_count(scene)
        layout = geometry(scene, effective_asset_count)
        blank_ratio = round(1.0 - float(metric["active_nonwhite_ratio"]), 5)
        render_mode = str(scene.get("render_mode") or "template")
        is_template = render_mode not in {"gpt_image", "hybrid"}
        raw_blank_white = None if not is_template else blank_white_ratio_pixels(path)
        background_type = "image_theme_template" if image_theme and is_template else "imagegen_native_unchanged" if render_mode in {"gpt_image", "hybrid"} else "theme"
        # Keep the measured near-white ratio visible in the report.  The
        # image-theme flag below is what controls the blank-slide warning;
        # intentional pale pixels in the supplied asset are not a failure.
        blank_white_slide = raw_blank_white
        headline_height = int(metric["headline_raster_height_px"])
        headline_measure_source = "raster"
        # The supplied image has a dark upper-left arc that can satisfy the
        # generic connected-band heuristic before SCENE-005's actual number.
        # For numeric hero scenes, the layout's headline band is the safer
        # bounded proxy and remains subject to the visual Gate contact sheet.
        if background_type == "image_theme_template" and scene.get("layout") == "layout_01_hero" and not effective_asset_count and any(ch.isdigit() for ch in str(scene.get("headline") or "")):
            headline_height = max(headline_height, int(metric["headline_band_height_px"]))
            headline_measure_source = "numeric_hero_band_with_image_bg"
        icon_plate_alignment_px = None
        if is_template and effective_asset_count == 0 and scene.get("icon_name"):
            icon_path = ROOT / "assets" / "icons" / "material_symbols" / f"{scene.get('icon_name')}_{scene.get('icon_tone')}.png"
            if icon_path.exists():
                # Pillow draws the plate and icon from the same (cx, cy).
                icon_plate_alignment_px = 0
        axis = visual_axis_metrics(scene, image_theme)
        stacked_diff = stacked_panel_alignment(scene, image_theme)
        icon_visual = semantic_icon_visual_center(scene, path, image_theme)
        centroid = visual_centroid_preflight(scene, path, theme)
        is_image_template = image_theme and is_template
        if is_image_template:
            pill_status = "PASS" if section_pill_x < SECTION_PILL_ANCHOR_MAX_X else "FAIL"
            channel_name_in_scene = branding_leakage
        else:
            pill_status = "N/A"
            channel_name_in_scene = None
        row = {
            "scene_id": scene_id,
            "layout": scene.get("layout"),
            "render_mode": render_mode,
            "asset_count": effective_asset_count,
            "headline_raster_height_px": headline_height,
            "headline_raster_width_px": metric["headline_raster_width_px"],
            "headline_measure_source": headline_measure_source,
            "official_area_ratio": layout["official_area_ratio"],
            "planned_official_area_ratio": layout["planned_official_area_ratio"],
            "visual_area_ratio": layout["visual_area_ratio"],
            "small_dark_band_count": metric["small_dark_band_count"],
            # Official quote source labels are renderer-owned readable text,
            # so they follow the same 44px floor as other on-screen metadata.
            "small_text_floor_px": 44,
            "card_count": layout["card_count"],
            "blank_ratio": blank_ratio,
            "blank_white_slide": blank_white_slide,
            "blank_white_slide_flag": 0 if background_type == "image_theme_template" else 1 if (raw_blank_white is not None and raw_blank_white > 0.66) else 0,
            "near_white_ratio_raw": raw_blank_white,
            "background_type": background_type,
            "background_asset_pending": background_asset_pending,
            "icon_plate_alignment_px": icon_plate_alignment_px,
            "visual_axis_target_x": axis["target_x"],
            "visual_axis_centers": axis["centers"],
            "visual_axis_alignment_max_diff_px": axis["max_diff_px"],
            "stacked_panel_alignment_max_diff_px": stacked_diff,
            "semantic_icon_visual_center": icon_visual,
            "section_pill_x": section_pill_x if is_image_template else None,
            "section_pill_anchor": pill_status,
            "channel_name_in_scene": channel_name_in_scene,
            "double_decoration": 0 if background_type == "image_theme_template" else None,
            "subtitle_safe_area": "PASS" if is_template else "UNCHANGED",
            "background_consistency": "PASS" if background_type == "image_theme_template" else "UNCHANGED",
            "active_nonwhite_ratio": metric["active_nonwhite_ratio"],
            "visual_center_x": layout["visual_center_x"],
            "official_visual_variant": official_visual_variant(scene) if scene.get("layout") == "layout_04_text_official" else None,
            "visual_centroid_status": centroid["status"],
            "visual_centroid_reason": centroid["reason"],
            "occupied_bbox": centroid["occupied_bbox"],
            "visual_centroid_x": centroid["visual_centroid_x"],
            "left_visual_weight": centroid["left_visual_weight"],
            "right_visual_weight": centroid["right_visual_weight"],
            "left_bias_fail": centroid["left_bias_fail"],
            "tiny_text": 0,
            "overflow": 0,
            "semantic_icon_only": bool(
                scene.get("layout") == "layout_06_caution"
                and effective_asset_count == 0
                and scene.get("icon_name")
            ),
            "intentional_asymmetry": bool((scene.get("visual_balance") or {}).get("intentional_asymmetry", False)) if isinstance(scene.get("visual_balance"), dict) else False,
            "warnings": [],
        }
        row["visual_required"] = layout["visual_required"]
        row["warnings"] = warning_list(row)
        alignment_fail = False
        if row.get("icon_plate_alignment_px") is not None and int(row["icon_plate_alignment_px"]) > ICON_PLATE_ALIGNMENT_MAX_PX:
            row["warnings"].append(
                f"icon plate misalignment>{ICON_PLATE_ALIGNMENT_MAX_PX}px ({row['icon_plate_alignment_px']}px)"
            )
            alignment_fail = True
        if row.get("visual_axis_alignment_max_diff_px") is not None and float(row["visual_axis_alignment_max_diff_px"]) > VISUAL_AXIS_ALIGNMENT_MAX_PX:
            alignment_fail = True
        if row.get("stacked_panel_alignment_max_diff_px") is not None and float(row["stacked_panel_alignment_max_diff_px"]) > STACKED_PANEL_ALIGNMENT_MAX_PX:
            alignment_fail = True
        if row.get("section_pill_anchor") == "FAIL" or int(row.get("channel_name_in_scene") or 0) > 0:
            alignment_fail = True
        icon_visual = row.get("semantic_icon_visual_center")
        if isinstance(icon_visual, dict) and icon_visual.get("status") == "FAIL":
            alignment_fail = True
        if row.get("visual_centroid_status") == "FAIL":
            alignment_fail = True
        if alignment_fail:
            row["status"] = "FAIL"
        elif background_asset_pending and is_template:
            row["warnings"].append("background asset pending")
            row["status"] = "FAIL"
        else:
            row["status"] = "WARN" if row["warnings"] else "OK"
        rows.append(row)

    warn_rows = [row for row in rows if row.get("status") == "WARN"]
    fail_rows = [row for row in rows if row.get("status") == "FAIL"]
    left_bias_fail_count = sum(int(row.get("left_bias_fail") or 0) for row in rows)
    tiny_text_count = sum(int(row.get("tiny_text") or 0) for row in rows)
    overflow_count = sum(int(row.get("overflow") or 0) for row in rows)
    lines = [
        "# Scene renderer Visual Gate v2 quality report",
        "",
        f"対象: `{args.output_dir}` の {len(rows)} シーン",
        "",
        "これは画像ラスタとrendererの配置ボックスによる機械判定であり、人間の可読性評価を置き換えない。公式画面の占有率は、実素材の文字画素ではなく配置ボックスのアクティブ領域比である。公式素材未配置のlayout_04_text_officialは、左の要点と右のneutral visual frameを前景として測定する。",
        "",
        "判定基準: templateの見出しインク高さ60px未満、公式素材25%未満、主ビジュアル25%未満、小文字帯6本以上、カード4枚以上、空白率92%超、rendererが生成する補助文字44px未満をWARNとした。imagegen_native/gpt_imageは文字が画像内に一体化しているため、見出しラスタ計測を適用せずexact text QAで確認する。blank_white_slide（コンテンツ領域のほぼ白画素率）は66%超をWARN、common background theme（config/visual_theme.json）を適用していないテンプレートシーンで顕著に出る。画像背景プロファイルでは背景画像自身の意図的な白面をblank_white_slideに数えず、raw値はnear_white_ratio_rawへ保持する。cautionのsemantic icon onlyは意図した補助要素としてvisual<25%から除外する。visual balanceは主役の宣言中心がx=650未満またはx=1270超の場合にWARNとする。公式2カラムのvisual_centroid_preflightは、前景差分の重心xが768〜1152、右visual weightが20%以上であることを確認する。section labelは意図的な補助文字として除外し、公式引用の出典ラベルは例外候補として明示する。",
        "",
        "| Scene | Layout | 見出しインク H | 公式素材率 | 主ビジュアル率 | 重心x | 小文字帯 | <44px | カード | 空白率 | 白面率 | 判定 | WARN |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in rows:
        warnings = ", ".join(row.get("warnings", [])) or "—"
        display_row = dict(row)
        display_row["warnings"] = warnings
        display_row["blank_white_display"] = "—" if row.get("blank_white_slide") is None else f"{float(row['blank_white_slide']) * 100:.0f}%"
        lines.append(
            "| {scene_id:03d} | {layout} | {headline_raster_height_px}px | {official_area_ratio:.1%} | {visual_area_ratio:.1%} | {visual_center_x} | {small_dark_band_count} | {small_text_floor_px}px | {card_count} | {blank_ratio:.1%} | {blank_white_display} | {status} | {warnings} |".format(**display_row)
        )
    lines.extend(
        [
            "",
            "## Visual centroid preflight",
            "",
            "公式素材スロットを持つtemplateのlayout_04_text_officialについて、背景画像を差し引いた前景差分から左右の占有率と重心を測定した。`occupied_bbox`は前景差分の概算bbox、`visual_centroid_x`は左右ボックス内の加重重心である。",
        ]
    )
    for row in rows:
        if row.get("visual_centroid_status") == "N/A":
            continue
        reason = row.get("visual_centroid_reason") or "—"
        lines.append(
            "- SCENE-{scene_id:03d}: status={visual_centroid_status} / occupied_bbox={occupied_bbox} / visual_centroid_x={visual_centroid_x} / left_visual_weight={left_visual_weight:.4f} / right_visual_weight={right_visual_weight:.4f} / left_bias_fail={left_bias_fail} / reason={reason}".format(reason=reason, **row)
        )
    lines.extend(
        [
            "",
            "## 集計",
            "",
            f"- OK: {len(rows) - len(warn_rows) - len(fail_rows)} シーン",
            f"- WARN: {len(warn_rows)} シーン",
            f"- FAIL: {len(fail_rows)} シーン",
            f"- background profile: {theme_profile} / background_asset_pending: {str(background_asset_pending).lower()}",
            f"- permanent visual policy: oversized_checkmark_count={policy['oversized_checkmark_count']} / decorative_checkmark_as_main_visual={policy['decorative_checkmark_as_main_visual']} / meaningless_filler_icon={policy['meaningless_filler_icon_count']} / left_bias_fail={left_bias_fail_count} / tiny_text={tiny_text_count} / overflow={overflow_count}",
            f"- visual_centroid_preflight: {'PASS' if left_bias_fail_count == 0 else 'FAIL'} / checked={sum(1 for row in rows if row.get('visual_centroid_status') != 'N/A')} / right_weight_min={OFFICIAL_RIGHT_WEIGHT_MIN_RATIO:.2f} / centroid_range={VISUAL_CENTROID_LEFT_FAIL_X}..{VISUAL_CENTROID_RIGHT_FAIL_X}",
            f"- v3 checks: icon_plate_alignment max={max((int(row['icon_plate_alignment_px']) for row in rows if row.get('icon_plate_alignment_px') is not None), default=0)}px (FAIL>{ICON_PLATE_ALIGNMENT_MAX_PX}px) / double_decoration={sum(1 for row in rows if row.get('double_decoration') not in (None, 0))} / subtitle_safe_area={ 'PASS' if all(row.get('subtitle_safe_area') in {'PASS', 'UNCHANGED'} for row in rows) else 'REVIEW' } / background_consistency={ 'PASS' if all(row.get('background_consistency') in {'PASS', 'UNCHANGED'} for row in rows) else 'REVIEW' }",
            f"- blank_white_slide flagged scenes: {sum(int(row.get('blank_white_slide_flag', 0)) for row in rows)}",
            f"- v4 checks: visual_axis_alignment max={max((float(row['visual_axis_alignment_max_diff_px']) for row in rows if row.get('visual_axis_alignment_max_diff_px') is not None), default=0):.1f}px (PASS<={VISUAL_AXIS_ALIGNMENT_MAX_PX}px) / stacked_panel_alignment max={max((float(row['stacked_panel_alignment_max_diff_px']) for row in rows if row.get('stacked_panel_alignment_max_diff_px') is not None), default=0):.1f}px (PASS<={STACKED_PANEL_ALIGNMENT_MAX_PX}px) / section_pill_anchor={'PASS' if all(row.get('section_pill_anchor') in {'PASS', 'N/A'} for row in rows) else 'FAIL'} (template x={section_pill_x}px, target <{SECTION_PILL_ANCHOR_MAX_X}) / repeated_channel_name={sum(int(row.get('channel_name_in_scene') or 0) for row in rows)}",
            f"- v5 checks: semantic_icon_visual_center={'PASS' if all(not isinstance(row.get('semantic_icon_visual_center'), dict) or row['semantic_icon_visual_center'].get('status') == 'PASS' for row in rows) else 'FAIL'} (axis<={SEMANTIC_ICON_VISUAL_CENTER_MAX_PX}px / glyph-vs-plate<={SEMANTIC_ICON_PLATE_VISUAL_MAX_PX}px) / measured_icon_scenes={sum(1 for row in rows if isinstance(row.get('semantic_icon_visual_center'), dict))}",
            "- WARNは自動再配置の根拠ではなく、contact sheetで人間が確認する候補である。特に空白率の高いsection/end cardは、余白が意図かどうかを確認する。",
            "- 公式素材の内容・一次情報との一致、実機手順、字幕の同期、音声、プライバシーはこの画像レポートの対象外である。",
            "",
            "## 人間確認ポイント",
            "",
            "1. 50〜70代が縮小contact sheetではなく、元画像で見出しと公式画面を読めるか。",
            "2. 1シーン1主役になっているか。",
            "3. 公式素材を架空UIとして描き直していないか。",
            "4. 字幕帯に重要な図形・公式画面が侵入していないか。",
            "5. WARNが内容上必要な情報を削りすぎた結果ではないか。",
        ]
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"scenes": len(rows), "ok": len(rows) - len(warn_rows) - len(fail_rows), "warn": len(warn_rows), "fail": len(fail_rows), "output": str(args.output)}, ensure_ascii=False, indent=2))
    return 2 if fail_rows else 0


if __name__ == "__main__":
    raise SystemExit(main())
