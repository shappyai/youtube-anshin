"""Render episode.json scenes to 1920x1080 PNGs and a contact sheet.

The preferred path is HTML/CSS rendered by a locally installed Chromium-family
browser (Microsoft Edge is detected on Windows).  Pillow is a dependency-light
fallback for headless/CI environments.  Official assets are cropped and
composited only from paths declared in episode.json; no UI is redrawn by AI.
GPT-image scenes are completed full-frame backgrounds; Codex text is an
overlay only, never a second card/layout pass.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps

from episode_io import ROOT, asset_path_from_item, episode_dir_from_path, load_json, resolve_repo_path, validate_episode

WIDTH = 1920
HEIGHT = 1080
SAFE_HEIGHT = 180
TEMPLATE_DIR = ROOT / "templates" / "scenes"
NORMALIZED_ICON_DIR = ROOT / "assets" / "icons" / "material_symbols_normalized"
FORBIDDEN_DECORATIVE_GLYPHS = frozenset({"✓", "!", "?", "×", "✕"})
OFFICIAL_TEXT_BOX = (120, 310, 930, 840)
OFFICIAL_TEXT_BOX_CENTERED = (240, 310, 1680, 840)
OFFICIAL_VISUAL_BOX = (970, 300, 1810, 830)

LAYOUT_TEMPLATES = {
    "layout_01_hero": "layout_01_hero.html",
    "layout_02_list": "layout_02_list.html",
    "layout_03_visual_text": "layout_03_visual_text.html",
    "layout_04_text_official": "layout_04_text_official.html",
    "layout_05_compare": "layout_05_compare.html",
    "layout_06_caution": "layout_06_caution.html",
    "layout_07_summary": "layout_07_summary.html",
    "layout_08_section": "layout_08_section.html",
}


@dataclass
class AssetRender:
    kind: str
    label: str
    path: Path | None = None
    image: Image.Image | None = None
    text: str = ""
    source: str = ""
    missing: bool = False


def esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def find_font_path() -> str | None:
    candidates = [
        "C:/Windows/Fonts/YuGothB.ttc",
        "C:/Windows/Fonts/YuGothM.ttc",
        "C:/Windows/Fonts/meiryob.ttc",
        "C:/Windows/Fonts/meiryo.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    ]
    for value in candidates:
        if Path(value).exists():
            return value
    return None


def pil_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = find_font_path()
    if path:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


# 日本語禁則処理（Episode 004以降の恒久ルール）
# - 行頭禁則: 、。，．・：；！？％）」』】〕〉｝＞ー…
# - 行末禁則: （「『【〔〈｛＜
# - 1文字だけの孤立行を作らない（前後の行へ統合して単語分断を防ぐ）
START_FORBIDDEN = "、。，．・：；！？％）」』】〕〉｝＞ー…ゃゅょぁぃぅぇぉっャュョァィゥェォッ"
END_FORBIDDEN = "（「『【〔〈｛＜"


def _wrap_paragraph_japanese(text: str, font: ImageFont.ImageFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    """Greedy wrap with Japanese kinsoku, ASCII token protection, parenthetical span protection,
    and single-char orphan prevention."""
    lines: list[str] = []
    current = ""
    paren_open = False
    for char in text:
        candidate = current + char
        if current and draw.textlength(candidate, font=font) > max_width:
            if char in START_FORBIDDEN:
                # 行頭禁止文字は前行へ残してでも行頭に置かない
                current = candidate
                continue
            # ASCII連続token（英数字＋記号＋半角スペース）は途中分断しない
            # （「20:00」「0120-95-0178」等の数字・記号列を離さない。恒久ルール）
            if char.isascii() and current[-1].isascii():
                current = candidate
                continue
            # 開き括弧は行頭へ送り、括弧内は分断しない（「60日（バッ / クアップ済み）」禁止。
            # 「60日」＋「（バックアップ済み）」のような意味境界は許容）
            if char == "（":
                lines.append(current)
                current = candidate
                paren_open = True
                continue
            if paren_open:
                # 括弧が前行の末尾から始まって幅を超えた場合は、開き括弧ごと
                # 次行へ移す。括弧内そのものが長すぎる場合は、fit_text_block
                # が指定の最小サイズまで下げて別途判定する。
                open_index = current.find("（")
                if open_index > 0:
                    lines.append(current[:open_index])
                    current = current[open_index:] + char
                    continue
                current = candidate
                continue
            lines.append(current)
            current = char
        else:
            current = candidate
        if char == "（":
            paren_open = True
        elif char == "）":
            paren_open = False
    if current or not lines:
        lines.append(current)

    # 行末禁則: 行末に開き括弧が残る場合は次行へ送る
    for index in range(len(lines) - 1):
        if lines[index] and lines[index][-1] in END_FORBIDDEN and len(lines[index]) > 1:
            lines[index + 1] = lines[index][-1] + lines[index + 1]
            lines[index] = lines[index][:-1]

    # 行頭禁則の後処理（幅超過で行頭禁止文字が送られた場合に備え、前行へ寄せる）
    for index in range(len(lines) - 1, 0, -1):
        if lines[index][:1] in START_FORBIDDEN and lines[index - 1]:
            lines[index - 1] += lines[index][:1]
            lines[index] = lines[index][1:]

    # 1文字だけの孤立行は隣の行へ統合（「番 / 号」のような分断を防ぐ）
    index = 0
    while index < len(lines):
        if len(lines[index]) == 1 and len(lines) > 1:
            if index < len(lines) - 1:
                lines[index + 1] = lines[index][0] + lines[index + 1]
            else:
                lines[index - 1] += lines[index][0]
            del lines[index]
            continue
        index += 1
    return [line for line in lines if line != ""]


def wrap_text(text: str, font: ImageFont.ImageFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    lines: list[str] = []
    for paragraph in str(text).splitlines() or [""]:
        lines.extend(_wrap_paragraph_japanese(paragraph, font, max_width, draw))
    return lines


def file_url(path: Path) -> str:
    return path.resolve().as_uri()


def crop_boxes(item: dict[str, Any], crop_specs: list[dict[str, Any]]) -> list[list[int] | None]:
    matching: list[list[int] | None] = []
    for spec in crop_specs:
        if spec.get("asset_index") != item.get("_index"):
            continue
        box = spec.get("box")
        if isinstance(box, list) and len(box) == 4 and all(isinstance(v, int) for v in box):
            matching.append(box)
        else:
            matching.append(None)
    return matching or [None]


def prepare_assets(
    scene: dict[str, Any],
    episode_dir: Path,
    cache_dir: Path,
) -> tuple[list[AssetRender], list[str]]:
    assets = scene.get("official_asset") or []
    crop_specs = scene.get("official_asset_crop") or []
    prepared: list[AssetRender] = []
    missing: list[str] = []
    cache_dir.mkdir(parents=True, exist_ok=True)

    if not isinstance(assets, list):
        return [AssetRender("placeholder", "公式素材の形式が不正です", missing=True)], ["official_asset"]

    for index, raw_item in enumerate(assets):
        if not isinstance(raw_item, dict):
            prepared.append(AssetRender("placeholder", "公式素材の形式が不正です", missing=True))
            missing.append(f"scene {scene.get('id')}: asset {index}")
            continue
        item = dict(raw_item)
        item["_index"] = index
        slot = scene.get("official_asset_slot")
        slot_status = slot.get("status") if isinstance(slot, dict) else ""
        capture_status = str(
            item.get("capture_status")
            or item.get("official_capture_status")
            or scene.get("official_capture_status")
            or slot_status
            or ""
        ).strip().lower()
        if capture_status == "official_capture_failed":
            # Fail closed: OCR/partial extraction must never be shown as an
            # official page. The caller records the missing asset and stops
            # the production gate until an explicit recovery is selected.
            prepared.append(
                AssetRender(
                    kind="placeholder",
                    label="公式素材の取得失敗：再取得が必要です",
                    missing=True,
                )
            )
            missing.append(f"scene {scene.get('id')}: official_capture_failed")
            continue
        kind = str(item.get("kind", "placeholder"))
        label = str(item.get("label") or "公式素材")
        if kind == "quote":
            prepared.append(
                AssetRender(
                    kind="quote",
                    label=label,
                    text=str(item.get("text") or ""),
                    source=str(item.get("source") or ""),
                )
            )
            continue
        path = asset_path_from_item(item, episode_dir)
        if kind != "image" or path is None or not path.exists():
            missing_name = str(item.get("path") or label)
            prepared.append(
                AssetRender(
                    kind="placeholder",
                    label=f"公式素材が未配置: {missing_name}",
                    path=path,
                    missing=True,
                )
            )
            missing.append(f"scene {scene.get('id')}: {missing_name}")
            continue
        try:
            source_image = Image.open(path).convert("RGBA")
            for crop_index, box in enumerate(crop_boxes(item, crop_specs)):
                image = source_image.copy()
                rendered_path = path
                if box:
                    left, top, right, bottom = box
                    if right <= left or bottom <= top:
                        raise ValueError(f"invalid crop box {box}")
                    left = max(0, min(left, image.width - 1))
                    top = max(0, min(top, image.height - 1))
                    right = max(left + 1, min(right, image.width))
                    bottom = max(top + 1, min(bottom, image.height))
                    image = image.crop((left, top, right, bottom))
                    cache_path = cache_dir / f"scene_{int(scene['id']):03d}_asset_{index:02d}_crop_{crop_index:02d}.png"
                    image.save(cache_path)
                    rendered_path = cache_path
                prepared.append(AssetRender(kind="image", label=label, path=rendered_path, image=image))
            source_image.close()
        except (OSError, ValueError) as exc:
            prepared.append(
                AssetRender(
                    kind="placeholder",
                    label=f"公式素材を読めません: {label}",
                    path=path,
                    missing=True,
                )
            )
            missing.append(f"scene {scene.get('id')}: {exc}")
    return prepared, missing


def asset_card_html(asset: AssetRender) -> str:
    label = f'<span class="asset-label">{esc(asset.label)}</span>'
    if asset.kind == "image" and asset.path:
        return f'<div class="official-card">{label}<img src="{esc(file_url(asset.path))}" alt="{esc(asset.label)}"></div>'
    if asset.kind == "quote":
        source = f'<span class="asset-source">{esc(asset.source)}</span>' if asset.source else ""
        return f'<div class="official-card">{label}<div class="asset-quote">{esc(asset.text)}{source}</div></div>'
    return f'<div class="official-card"><div class="asset-placeholder">{esc(asset.label)}</div></div>'


def official_html(assets: list[AssetRender]) -> str:
    if not assets:
        return ""
    two = " two" if len(assets) > 1 else ""
    return f'<div class="official-slot{two}">{"".join(asset_card_html(asset) for asset in assets)}</div>'


# 単一アイコンの背景円の淡色（semantic icon 用・恒久ルール）
ICON_CIRCLE = {
    "navy": "#e9edf5",
    "blue": "#eaf4ff",
    "green": "#eaf7ee",
    "amber": "#fdf3e0",
}


def semantic_icon_html(scene: dict[str, Any]) -> str | None:
    """sceneのicon_name/icon_toneから高品質SVG由来のアイコン画像を出力する。

    Material Symbols Rounded を公式配布元から取得し tint したPNG（assets/icons/material_symbols/）
    を参照する。指摘されるような単純記号バッジ（!/✓丸）ではなく、意味を持つアイコンを使う。
    """
    name = str(scene.get("icon_name") or "")
    tone = str(scene.get("icon_tone") or "")
    if not name or not tone:
        return None
    path = normalized_semantic_icon_path(name, tone, 180)
    if path is None:
        return None
    tone_class = "tone-" + esc(tone) if tone in ICON_CIRCLE else "tone-blue"
    return (
        f'<div class="icon-stage {tone_class}">'
        f'<img class="svg-icon" src="{file_url(path)}" alt=""></div>'
    )


def normalized_semantic_icon_path(name: str, tone: str, visual_box_size: int = 180) -> Path | None:
    """Return a transparent-padding-normalized semantic icon cache.

    The source tint PNGs are retained unchanged. Their visible alpha bbox is
    trimmed, fitted with aspect ratio preserved into a fixed visual box, and
    centered so the glyph—not the source canvas—lands on the intended axis.
    """
    source_path = ROOT / "assets" / "icons" / "material_symbols" / f"{name}_{tone}.png"
    if not source_path.exists():
        return None
    size = max(1, int(visual_box_size))
    cache_path = NORMALIZED_ICON_DIR / f"{name}_{tone}_s{size}.png"
    try:
        if cache_path.exists() and cache_path.stat().st_mtime >= source_path.stat().st_mtime:
            return cache_path
    except OSError:
        pass
    try:
        with Image.open(source_path) as source:
            rgba = source.convert("RGBA")
            alpha = rgba.getchannel("A")
            # Ignore near-zero antialias fringe when finding the true glyph
            # bounds; the original source remains untouched.
            trim_mask = alpha.point(lambda value: 255 if value >= 4 else 0)
            bbox = trim_mask.getbbox()
            if bbox is None:
                return source_path
            trimmed = rgba.crop(bbox)
            fitted = ImageOps.contain(
                trimmed,
                (size, size),
                method=Image.Resampling.LANCZOS,
            )
            normalized = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            left = (size - fitted.width) // 2
            top = (size - fitted.height) // 2
            normalized.alpha_composite(fitted, (left, top))
            NORMALIZED_ICON_DIR.mkdir(parents=True, exist_ok=True)
            normalized.save(cache_path, "PNG")
            return cache_path
    except (OSError, ValueError):
        return source_path


def official_visual_variant(scene: dict[str, Any]) -> str:
    """Return the data-driven visual variant for an official two-column scene."""
    raw = str(scene.get("official_visual_variant") or "").strip().lower()
    if raw in {
        "safe_entry_options",
        "safe_entry_options_centered",
        "semantic_operation",
        "phone",
        "browser",
        "neutral_frame",
    }:
        return raw
    if str(scene.get("visual_role") or "").strip().lower() == "safe_entry_options":
        return "safe_entry_options"
    return "neutral_frame"


def official_frame_kind(scene: dict[str, Any]) -> str:
    """Choose an abstract browser or phone frame from declared slot metadata."""
    variant = official_visual_variant(scene)
    if variant == "phone":
        return "phone"
    slot = scene.get("official_asset_slot")
    try:
        slot_text = json.dumps(slot, ensure_ascii=False)
    except (TypeError, ValueError):
        slot_text = str(slot or "")
    return "phone" if any(token in slot_text.lower() for token in ("app", "スマホ", "phone")) else "browser"


def visual_points(scene: dict[str, Any]) -> list[str]:
    raw = scene.get("visual_points")
    if not isinstance(raw, list):
        return []
    return [str(item).strip() for item in raw if str(item).strip()]


def visual_points_html(scene: dict[str, Any]) -> str:
    """Render short, data-declared left-column points without filler glyphs."""
    points = visual_points(scene)
    if not points:
        return ""
    if official_visual_variant(scene) in {"safe_entry_options", "safe_entry_options_centered"}:
        options = scene.get("official_entry_options")
        if not isinstance(options, list):
            options = []
        cards: list[str] = []
        for option in options:
            if not isinstance(option, dict):
                continue
            label = str(option.get("label") or "").strip()
            if not label:
                continue
            icon_path = normalized_semantic_icon_path(
                str(option.get("icon_name") or ""),
                str(option.get("icon_tone") or "blue"),
                72,
            )
            icon = f'<img class="entry-option-icon" src="{esc(file_url(icon_path))}" alt="">' if icon_path else ""
            cards.append(
                f'<div class="entry-option">{icon}<span>{esc(label)}</span></div>'
            )
        if cards:
            return "".join(cards)
    return "".join(
        f'<div class="visual-point"><span class="visual-point-rule"></span><span>{esc(point)}</span></div>'
        for point in points
    )


def neutral_official_html(scene: dict[str, Any]) -> str:
    """Return a non-viewer-facing official capture frame for Phase A.

    The frame contains no placeholder/pending copy, URL, logo, or reconstructed
    UI text. It is a balanced visual slot that can be replaced by an official
    capture in Phase B.
    """
    if official_visual_variant(scene) in {"safe_entry_options_centered", "semantic_operation"}:
        return ""
    kind = official_frame_kind(scene)
    if kind == "phone":
        inner = (
            '<div class="neutral-phone">'
            '<span class="neutral-phone-speaker"></span>'
            '<span class="neutral-phone-panel neutral-phone-panel-top"></span>'
            '<span class="neutral-phone-panel neutral-phone-panel-mid"></span>'
            '<span class="neutral-phone-panel neutral-phone-panel-bottom"></span>'
            '</div>'
        )
    else:
        inner = (
            '<div class="neutral-browser">'
            '<div class="neutral-browser-chrome">'
            '<span class="neutral-browser-dot"></span><span class="neutral-browser-dot"></span>'
            '<span class="neutral-browser-dot"></span><span class="neutral-browser-address"></span>'
            '</div>'
            '<div class="neutral-browser-body">'
            '<span class="neutral-browser-hero"></span>'
            '<span class="neutral-browser-line neutral-browser-line-wide"></span>'
            '<span class="neutral-browser-line neutral-browser-line-mid"></span>'
            '<span class="neutral-browser-card"></span>'
            '</div>'
            '</div>'
        )
    return f'<div class="official-neutral-slot {kind}" aria-hidden="true">{inner}</div>'


def semantic_operation_html(scene: dict[str, Any]) -> str:
    """Render a concrete safe-entry operation without inventing an app UI."""
    raw_steps = scene.get("official_operation_steps")
    steps = raw_steps if isinstance(raw_steps, list) else []
    cards: list[str] = []
    for step in steps[:2]:
        if not isinstance(step, dict):
            continue
        label = str(step.get("label") or "").strip()
        if not label:
            continue
        icon_path = normalized_semantic_icon_path(
            str(step.get("icon_name") or ""),
            str(step.get("icon_tone") or "blue"),
            92,
        )
        icon = f'<img class="operation-icon" src="{esc(file_url(icon_path))}" alt="">' if icon_path else ""
        cards.append(f'<div class="operation-step">{icon}<span>{esc(label)}</span></div>')
    if len(cards) < 2:
        return ""
    return (
        '<div class="official-operation">'
        f'{cards[0]}<div class="operation-arrow" aria-hidden="true">↓</div>{cards[1]}'
        '</div>'
    )


def visual_html(scene: dict[str, Any], layout: str, assets: list[AssetRender]) -> str:
    headline = str(scene.get("headline", ""))
    if layout in {"layout_01_hero", "layout_03_visual_text"} and assets:
        return official_html(assets)
    if layout == "layout_06_caution":
        icon = semantic_icon_html(scene)
        if icon:
            return icon
        return '<span class="neutral-symbol-frame" aria-hidden="true"></span>'
    if layout == "layout_08_section":
        icon = semantic_icon_html(scene)
        if icon:
            return icon
        return '<span class="neutral-symbol-frame" aria-hidden="true"></span>'
    if layout == "layout_03_visual_text":
        if "バトンタッチ" in headline or "1つ" in headline or "1つに" in headline:
            items = [str(item) for item in (scene.get("items") or [])]
            step1 = items[0] if len(items) > 0 else "手順1"
            step2 = items[1] if len(items) > 1 else "手順2"
            return (
                f'<div class="diagram"><div class="diagram-step">{esc(step1)}</div>'
                f'<div class="diagram-arrow">→</div><div class="diagram-step">{esc(step2)}</div></div>'
            )
        icon = semantic_icon_html(scene)
        if icon:
            return icon
        target = headline + str(scene.get("support_text") or "")
        if "相談" in target or "窓口" in target:
            # 相談・窓口のニュアンスは成功チェックではなく「案内」の青バッジ
            return '<span class="status-badge blue">相談</span>'
        return '<span class="neutral-symbol-frame" aria-hidden="true"></span>'
    if layout == "layout_01_hero":
        icon = semantic_icon_html(scene)
        if icon:
            return icon
        return '<span class="neutral-symbol-frame" aria-hidden="true"></span>'
    return ""


def items_html(scene: dict[str, Any]) -> str:
    items = scene.get("items") or [scene.get("main_message", "確認ポイント")]
    return "".join(
        f'<div class="list-row"><span class="number">{index}</span><span>{esc(item)}</span></div>'
        for index, item in enumerate(items, 1)
    )


def actions_html(scene: dict[str, Any]) -> str:
    items = scene.get("items") or [scene.get("main_message", "確認する")]
    return "".join(
        f'<div class="action-row"><span class="check">✓</span><span>{esc(item)}</span></div>'
        for item in items
    )


def compare_default(scene: dict[str, Any]) -> list[tuple[str, str, str]]:
    """比較カードは現在のepisodeのsceneデータ（compare_cards / items）からだけ作る。

    他エピソード固有の文言をdefaultとして持たない（Episode 004のregression対策）。
    """
    raw_cards = scene.get("compare_cards") or []
    cards: list[tuple[str, str, str]] = []
    if isinstance(raw_cards, list):
        for index, raw in enumerate(raw_cards[:2]):
            if isinstance(raw, dict):
                title = str(raw.get("title") or "")
                body = str(raw.get("body") or "")
                color = str(raw.get("color") or ("blue-card" if index == 0 else "green-card"))
            else:
                title = str(raw)
                body = ""
                color = "blue-card" if index == 0 else "green-card"
            cards.append((title, body, color))
    if len(cards) == 2:
        return cards
    items = [str(item) for item in (scene.get("items") or [])]
    if len(items) >= 2:
        return [(items[0], "", "blue-card"), (items[1], "", "green-card")]
    return [("項目1", "", "blue-card"), ("項目2", "", "green-card")]


def compare_html(scene: dict[str, Any], assets: list[AssetRender]) -> str:
    cards = compare_default(scene)
    output: list[str] = []
    for index, (title, body, color) in enumerate(cards):
        asset_markup = asset_card_html(assets[index]) if index < len(assets) else ""
        output.append(
            f'<div class="compare-card {color}"><div class="compare-title">{esc(title)}</div>'
            f'<div class="compare-text">{esc(body)}</div>{asset_markup}</div>'
        )
    return "".join(output)


def render_html_scene(
    scene: dict[str, Any],
    section_label: str,
    assets: list[AssetRender],
    html_path: Path,
    theme_profile: str | None = None,
    episode_dir: Path | None = None,
) -> None:
    layout = str(scene.get("layout"))
    template_name = LAYOUT_TEMPLATES.get(layout)
    if not template_name:
        raise ValueError(f"unsupported layout: {layout}")
    template = (TEMPLATE_DIR / template_name).read_text(encoding="utf-8")
    theme_classes = {"intro": "theme-intro", "sec1": "theme-sec1", "sec2": "theme-sec2", "sec3": "theme-sec3", "contact": "theme-contact", "summary": "theme-summary"}
    selected_profile = str(theme_profile or THEME_DEFAULT_PROFILE)
    theme = load_visual_theme(selected_profile)
    profile_class = theme_profile_css_class(selected_profile)
    theme_class = f"{theme_classes.get(theme_section_key(section_label), 'theme-intro')} {profile_class}"
    context = {
        "theme_class": theme_class,
        "section_label": esc(scene.get("section_label") or section_label),
        "headline": esc(scene.get("headline")),
        "support_text": esc(scene.get("support_text")),
        "main_message": esc(scene.get("main_message")),
        "visual_html": visual_html(scene, layout, assets),
        "visual_points_html": visual_points_html(scene),
        "items_html": items_html(scene),
        "actions_html": actions_html(scene),
        "compare_html": compare_html(scene, assets),
        "official_html": (
            official_html(assets)
            if assets
            else semantic_operation_html(scene)
            if layout == "layout_04_text_official" and official_visual_variant(scene) == "semantic_operation"
            else neutral_official_html(scene)
            if layout == "layout_04_text_official"
            else ""
        ),
        "safe_zone": '<div class="subtitle-safe-zone"></div>',
    }
    for key, value in context.items():
        template = template.replace("{{" + key + "}}", value)
    css_url = file_url(TEMPLATE_DIR / "styles.css")
    theme_style = ""
    if str(theme.get("background_type") or "gradient") == "image":
        background_path = theme_background_path(theme, episode_dir)
        theme_style = (
            f'<style>body.{profile_class}'
            f' {{ --theme-background-image: url("{esc(file_url(background_path))}"); }}</style>'
        )
    document = (
        '<!doctype html><html lang="ja"><head><meta charset="utf-8">'
        f'<link rel="stylesheet" href="{esc(css_url)}">{theme_style}</head><body>{template}</body></html>'
    )
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(document.replace("<body>", "<body class=\"" + esc(context.get("theme_class", "theme-intro")) + "\">"), encoding="utf-8")


def edge_path() -> str | None:
    candidates = [
        shutil.which("msedge"),
        shutil.which("microsoft-edge"),
        "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
        "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    return None


def render_with_edge(edge: str, html_path: Path, output_path: Path) -> bool:
    with tempfile.TemporaryDirectory(prefix="anshin_edge_") as profile:
        command = [
            edge,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--no-first-run",
            "--no-default-browser-check",
            f"--user-data-dir={profile}",
            f"--window-size={WIDTH},{HEIGHT}",
            f"--screenshot={output_path.resolve()}",
            file_url(html_path),
        ]
        try:
            completed = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            return False
    if completed.returncode != 0 or not output_path.exists():
        return False
    try:
        with Image.open(output_path) as image:
            return image.size == (WIDTH, HEIGHT)
    except OSError:
        return False


def rounded_rectangle(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill: str, outline: str | None = None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def fit_text_block(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    max_height: int | None,
    max_size: int,
    min_size: int,
    max_lines: int,
    spacing_ratio: float = 0.14,
) -> tuple[ImageFont.ImageFont, int, list[str], int]:
    clean = str(text or "").strip()
    if not clean:
        return pil_font(max(min_size, 1)), 0, [], 0
    for size in range(max_size, min_size - 1, -2):
        font = pil_font(size)
        lines = wrap_text(clean, font, max_width, draw)
        line_height = max(size + 4, int(size * (1.0 + spacing_ratio)))
        widest = max((draw.textlength(line, font=font) for line in lines), default=0)
        total_height = len(lines) * line_height
        if len(lines) <= max_lines and widest <= max_width and (max_height is None or total_height <= max_height):
            return font, size, lines, line_height
    font = pil_font(min_size)
    lines = wrap_text(clean, font, max_width, draw)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    return font, min_size, lines, max(min_size + 4, int(min_size * (1.0 + spacing_ratio)))


def draw_fitted(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    max_size: int,
    min_size: int,
    fill: str,
    max_lines: int = 2,
    align: str = "left",
    spacing_ratio: float = 0.14,
) -> dict[str, Any]:
    left, top, right, bottom = box
    font, size, lines, line_height = fit_text_block(
        draw, text, right - left, bottom - top, max_size, min_size, max_lines, spacing_ratio
    )
    y = top
    for line in lines:
        line_width = draw.textlength(line, font=font)
        x = left if align == "left" else left + max(0, (right - left - int(line_width)) // 2)
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return {
        "font_size": size,
        "lines": len(lines),
        "line_height": line_height,
        "box": [left, top, right, bottom],
        "text": str(text or ""),
    }


def render_options(scene: dict[str, Any]) -> dict[str, Any]:
    """Read optional per-scene emphasis hints without changing episode.json."""
    raw_emphasis = scene.get("visual_emphasis", "normal")
    if isinstance(raw_emphasis, dict):
        raw_emphasis = raw_emphasis.get("level", "normal")
    emphasis = str(raw_emphasis or "normal").lower()
    if emphasis not in {"normal", "strong", "quiet", "hero"}:
        emphasis = "normal"
    try:
        scale = float(scene.get("headline_scale", 1.0))
    except (TypeError, ValueError):
        scale = 1.0
    scale = max(0.8, min(1.35, scale))
    if emphasis in {"strong", "hero"}:
        scale = min(1.35, scale * 1.08)
    raw_composition = scene.get("composition", "default")
    if isinstance(raw_composition, dict):
        raw_composition = raw_composition.get("mode", "default")
    composition = str(raw_composition or "default").lower()
    if composition not in {"default", "visual_left", "visual_right", "center"}:
        composition = "default"
    return {"headline_scale": scale, "visual_emphasis": emphasis, "composition": composition}


def draw_headline(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    scene: dict[str, Any],
    max_size: int,
    min_size: int,
    max_lines: int,
    align: str = "left",
    spacing_ratio: float = 0.12,
) -> dict[str, Any]:
    options = render_options(scene)
    scale = float(options["headline_scale"])
    scaled_max = max(min_size, int(round(max_size * scale)))
    scaled_min = max(40, int(round(min_size * scale)))
    return draw_fitted(draw, box, str(scene.get("headline") or ""), scaled_max, scaled_min, "#173a68", max_lines, align, spacing_ratio)


def draw_text_block(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    size: int,
    max_width: int,
    fill: str = "#173a68",
    spacing: int = 10,
    max_lines: int | None = None,
) -> int:
    font = pil_font(size)
    lines = wrap_text(str(text or ""), font, max_width, draw)
    if max_lines:
        lines = lines[:max_lines]
    x, y = xy
    line_height = size + spacing
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return y


def draw_message_bar(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    fill: str = "#eaf4ff",
    text_fill: str = "#2f74bb",
) -> dict[str, Any]:
    rounded_rectangle(draw, box, 30, fill)
    return draw_fitted(draw, (box[0] + 42, box[1] + 12, box[2] - 42, box[3] - 12), text, 58, 40, text_fill, 2, "left")


def draw_symbol(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    symbol: str,
    fill: str = "#dff1e5",
    symbol_fill: str = "#63a975",
) -> None:
    if symbol in FORBIDDEN_DECORATIVE_GLYPHS:
        raise ValueError(f"decorative glyph is not allowed as a visual filler: {symbol}")
    rounded_rectangle(draw, box, 64, fill, "#c9d3dc", 2)
    left, top, right, bottom = box
    size = max(64, min(right - left, bottom - top) // 2)
    font = pil_font(size)
    width = int(draw.textlength(symbol, font=font))
    bbox = draw.textbbox((0, 0), symbol, font=font)
    height = bbox[3] - bbox[1]
    draw.text(((left + right - width) // 2, (top + bottom - height) // 2 - bbox[1]), symbol, font=font, fill=symbol_fill)


def draw_badge(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    fill: str = "#eaf7ee",
    text_fill: str = "#3f8c58",
    font_size: int = 52,
) -> None:
    """Draw a small text badge; decorative glyphs are rejected by policy."""
    if text in FORBIDDEN_DECORATIVE_GLYPHS:
        raise ValueError(f"decorative glyph is not allowed as a visual filler: {text}")
    rounded_rectangle(draw, box, 54, fill, "#c9d3dc", 2)
    left, top, right, bottom = box
    font = pil_font(font_size)
    width = int(draw.textlength(text, font=font))
    bbox = draw.textbbox((0, 0), text, font=font)
    height = bbox[3] - bbox[1]
    draw.text(((left + right - width) // 2, (top + bottom - height) // 2 - bbox[1]), text, font=font, fill=text_fill)


def draw_icon_stage(
    canvas: Image.Image,
    scene: dict[str, Any],
    center: tuple[int, int],
    circle_fill: str = "#eaf4ff",
    diameter: int = 230,
    icon_size: int = 180,
    plate_theme: dict[str, Any] | None = None,
) -> bool:
    """sceneのicon_name/icon_tone（Material Symbols Rounded由来のtint PNG）を淡い円に載せて描く。

    意味を持つSVGアイコンを使う（単純な!/✓の丸バッジを卒業する恒久ルール）。
    アセットが無い場合はFalseを返し、呼び出し側は意味のないglyphへ
    fallbackせず、neutral frameまたは空欄へ進む。
    """
    name = str(scene.get("icon_name") or "")
    tone = str(scene.get("icon_tone") or "")
    if not name or not tone:
        return False
    scene_diameter = scene.get("icon_diameter_px")
    scene_icon_size = scene.get("icon_size_px")
    if isinstance(scene_diameter, (int, float)):
        diameter = int(scene_diameter)
    if isinstance(scene_icon_size, (int, float)):
        icon_size = int(scene_icon_size)
    if diameter == 230:
        selected_plate_theme = plate_theme if isinstance(plate_theme, dict) else load_visual_theme().get("icon_plate", {})
        if isinstance(selected_plate_theme, dict) and selected_plate_theme:
            if not isinstance(scene_diameter, (int, float)):
                diameter = int(selected_plate_theme.get("circle_diameter", 230))
            if not isinstance(scene_icon_size, (int, float)):
                icon_size = int(selected_plate_theme.get("icon_size", 180))
    icon_path = normalized_semantic_icon_path(name, tone, icon_size)
    if icon_path is None:
        return False
    draw = ImageDraw.Draw(canvas)
    cx, cy = center
    draw.ellipse(
        (cx - diameter // 2, cy - diameter // 2, cx + diameter // 2, cy + diameter // 2),
        fill=circle_fill
    )
    icon = Image.open(icon_path).convert("RGBA")
    icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    canvas.alpha_composite(icon, (cx - icon_size // 2, cy - icon_size // 2))
    return True


def draw_small_semantic_icon(
    canvas: Image.Image,
    name: str,
    tone: str,
    center: tuple[int, int],
    size: int = 72,
) -> bool:
    path = normalized_semantic_icon_path(str(name or ""), str(tone or ""), size)
    if path is None:
        return False
    icon = Image.open(path).convert("RGBA")
    icon = icon.resize((size, size), Image.Resampling.LANCZOS)
    canvas.alpha_composite(icon, (center[0] - size // 2, center[1] - size // 2))
    return True


def draw_neutral_visual_frame(
    canvas: Image.Image,
    box: tuple[int, int, int, int],
    scene: dict[str, Any],
) -> None:
    """Draw a calm, abstract official-capture slot with no placeholder copy."""
    draw = ImageDraw.Draw(canvas)
    left, top, right, bottom = box
    rounded_rectangle(draw, box, 34, "#f8fbfd", "#8fb6ce", 4)
    inner = (left + 28, top + 28, right - 28, bottom - 28)
    if official_frame_kind(scene) == "phone":
        frame_width = min(360, max(290, (right - left) // 2))
        phone_left = (left + right - frame_width) // 2
        phone = (phone_left, top + 20, phone_left + frame_width, bottom - 20)
        rounded_rectangle(draw, phone, 34, "#ffffff", "#7faec9", 5)
        screen = (phone[0] + 26, phone[1] + 68, phone[2] - 26, phone[3] - 30)
        rounded_rectangle(draw, screen, 22, "#f2f8fc", "#d3e4ee", 3)
        draw.line((phone[0] + frame_width // 2 - 38, phone[1] + 30, phone[0] + frame_width // 2 + 38, phone[1] + 30), fill="#bdd4e2", width=7)
        draw.rounded_rectangle((screen[0] + 24, screen[1] + 42, screen[2] - 24, screen[1] + 116), radius=18, fill="#e5f1f8")
        draw.rounded_rectangle((screen[0] + 24, screen[1] + 150, screen[2] - 24, screen[1] + 188), radius=16, fill="#d5e8f2")
        draw.rounded_rectangle((screen[0] + 24, screen[1] + 220, screen[2] - 74, screen[1] + 258), radius=16, fill="#d5e8f2")
        draw.rounded_rectangle((screen[0] + 24, screen[1] + 290, screen[2] - 24, screen[1] + 364), radius=18, fill="#e8f4f9")
    else:
        rounded_rectangle(draw, inner, 28, "#ffffff", "#9fc4d8", 4)
        chrome_bottom = top + 104
        draw.line((inner[0], chrome_bottom, inner[2], chrome_bottom), fill="#d2e3ec", width=3)
        for index in range(3):
            x = inner[0] + 34 + index * 28
            draw.ellipse((x - 7, top + 54 - 7, x + 7, top + 54 + 7), fill="#c3d9e5")
        address = (inner[0] + 150, top + 38, inner[2] - 42, top + 70)
        rounded_rectangle(draw, address, 16, "#f1f7fa", "#d6e6ee", 2)
        body = (inner[0] + 36, chrome_bottom + 38, inner[2] - 36, inner[3] - 36)
        rounded_rectangle(draw, (body[0], body[1], body[2], body[1] + 112), 22, "#eaf4fb")
        rounded_rectangle(draw, (body[0], body[1] + 158, body[2] - 170, body[1] + 198), 14, "#d8eaf3")
        rounded_rectangle(draw, (body[0], body[1] + 222, body[2] - 280, body[1] + 262), 14, "#d8eaf3")
        rounded_rectangle(draw, (body[0], body[1] + 296, body[2], body[1] + 394), 20, "#f4f9fc", "#d5e6ee", 2)


def draw_semantic_operation_visual(
    canvas: Image.Image,
    box: tuple[int, int, int, int],
    scene: dict[str, Any],
) -> None:
    """Show the safe-entry action as two explicit steps, not a fake phone UI."""
    draw = ImageDraw.Draw(canvas)
    left, top, right, bottom = box
    rounded_rectangle(draw, box, 34, "#f8fbfd", "#8fb6ce", 4)
    raw_steps = scene.get("official_operation_steps")
    steps = [item for item in raw_steps if isinstance(item, dict)] if isinstance(raw_steps, list) else []
    steps = steps[:2]
    if len(steps) < 2:
        return
    card_left, card_right = left + 54, right - 54
    card_height = 146
    first_top = top + 54
    second_top = bottom - 54 - card_height
    positions = [(first_top, "#eaf4ff", "#2f74bb"), (second_top, "#eaf7ee", "#63a975")]
    for index, step in enumerate(steps):
        label = str(step.get("label") or "").strip()
        y, fill, outline = positions[index]
        rounded_rectangle(draw, (card_left, y, card_right, y + card_height), 26, fill, outline, 4)
        icon_size = 86
        icon_center = (card_left + 86, y + card_height // 2)
        draw_small_semantic_icon(
            canvas,
            str(step.get("icon_name") or ""),
            str(step.get("icon_tone") or "blue"),
            icon_center,
            icon_size,
        )
        draw_fitted(
            draw,
            (card_left + 150, y + 20, card_right - 24, y + card_height - 20),
            label,
            58,
            48,
            "#173a68",
            2,
            "left",
            0.10,
        )
    arrow_y = (first_top + card_height + second_top) // 2
    draw_fitted(draw, (left + 250, arrow_y - 42, right - 250, arrow_y + 42), "↓", 78, 64, "#2f74bb", 1, "center")


def draw_official_text_column(
    draw: ImageDraw.ImageDraw,
    canvas: Image.Image,
    scene: dict[str, Any],
    box: tuple[int, int, int, int],
    soft: str,
    blue: str,
    blue_strong: str,
) -> None:
    """Render concise left-column points and keep the right slot visually active."""
    left, top, right, bottom = box
    points = visual_points(scene)
    message_box = (left, bottom - 132, right, bottom - 12)
    if official_visual_variant(scene) in {"safe_entry_options", "safe_entry_options_centered"}:
        options = scene.get("official_entry_options")
        options = options if isinstance(options, list) else []
        usable = [item for item in options if isinstance(item, dict) and str(item.get("label") or "").strip()]
        gap = 18
        card_width = max(1, (right - left - gap * max(0, len(usable) - 1)) // max(1, len(usable)))
        card_top = top + 16
        card_bottom = message_box[1] - 26
        for index, option in enumerate(usable):
            card_left = left + index * (card_width + gap)
            card_right = card_left + card_width
            fill = ["#eaf4ff", "#eaf7ee", "#fff2d7"][index % 3]
            rounded_rectangle(draw, (card_left, card_top, card_right, card_bottom), 24, fill, "#c9d3dc", 3)
            center = ((card_left + card_right) // 2, card_top + 74)
            draw_small_semantic_icon(
                canvas,
                str(option.get("icon_name") or ""),
                str(option.get("icon_tone") or "blue"),
                center,
                72,
            )
            draw_fitted(
                draw,
                (card_left + 14, card_top + 132, card_right - 14, card_bottom - 18),
                str(option.get("label") or ""),
                52,
                44,
                "#173a68",
                2,
                "center",
                0.12,
            )
    elif points:
        gap = 20
        points_top = top + 18
        points_bottom = message_box[1] - 26
        card_height = max(92, (points_bottom - points_top - gap * max(0, len(points) - 1)) // max(1, len(points)))
        for index, point in enumerate(points):
            y = points_top + index * (card_height + gap)
            rounded_rectangle(draw, (left, y, right, y + card_height), 24, "#f4f9fc" if index % 2 else "#eaf4ff", "#c9ddec", 3)
            draw.line((left + 28, y + 24, left + 28, y + card_height - 24), fill=blue_strong, width=7)
            draw_fitted(draw, (left + 62, y + 12, right - 24, y + card_height - 12), point, 52, 44, "#173a68", 2, "left", 0.12)
    else:
        draw_fitted(draw, (left + 10, top + 24, right - 10, message_box[1] - 22), str(scene.get("support_text") or ""), 52, 44, soft, 3, "left", 0.14)
    main_message = str(scene.get("main_message") or "")
    if main_message:
        draw_message_bar(draw, message_box, main_message, blue, blue_strong)


def draw_concept(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], headline: str) -> None:
    """Draw a quiet abstract concept panel; never use a glyph as filler."""
    left, top, right, bottom = box
    rounded_rectangle(draw, (left + 42, top + 34, right - 42, bottom - 34), 28, "#f7fbfd", "#d2e3ec", 3)
    for index, width_ratio in enumerate((0.76, 0.58, 0.68)):
        y = top + 96 + index * 78
        line_right = left + 42 + int((right - left - 84) * width_ratio)
        rounded_rectangle(draw, (left + 86, y, line_right, y + 20), 10, "#d8eaf3")


def paste_asset(canvas: Image.Image, asset: AssetRender, box: tuple[int, int, int, int]) -> None:
    left, top, right, bottom = box
    draw = ImageDraw.Draw(canvas)
    if asset.kind == "image" and asset.image is not None:
        rounded_rectangle(draw, box, 28, "#f8fbfd", "#c9d3dc", 3)
        label_box = (left + 24, top + 18, right - 24, top + 78)
        rounded_rectangle(draw, label_box, 16, "#eaf4ff", "#c9ddec", 2)
        draw_fitted(draw, (left + 40, top + 22, right - 40, top + 72), asset.label, 46, 44, "#173a68", 1, "left", 0.08)
        image = ImageOps.contain(asset.image, (max(1, right - left - 28), max(1, bottom - top - 112)))
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        x = left + (right - left - image.width) // 2
        y = top + 94 + max(0, (bottom - top - 94 - image.height) // 2)
        canvas.alpha_composite(image, (x, y))
    elif asset.kind == "quote":
        rounded_rectangle(draw, box, 28, "#ffffff", "#c9d3dc", 3)
        draw_fitted(draw, (left + 34, top + 24, right - 34, top + 82), asset.label, 46, 44, "#4c9b65", 1, "left", 0.08)
        quote_bottom = bottom - (100 if asset.source else 28)
        draw_fitted(draw, (left + 34, top + 100, right - 34, quote_bottom), asset.text, 52, 44, "#173a68", 5, "left", 0.18)
        if asset.source:
            draw_fitted(draw, (left + 34, bottom - 78, right - 34, bottom - 22), asset.source, 44, 40, "#587187", 1, "left")
    else:
        rounded_rectangle(draw, box, 28, "#fff2d7", "#d3922e", 3)
        draw_fitted(draw, (left + 28, top + 34, right - 28, bottom - 34), asset.label, 38, 30, "#815e1e", 5, "center")


def asset_boxes(box: tuple[int, int, int, int], count: int, gap: int = 24, vertical: bool = False) -> list[tuple[int, int, int, int]]:
    if count <= 0:
        return []
    left, top, right, bottom = box
    if count == 1:
        return [box]
    if vertical:
        each = max(1, (bottom - top - gap * (count - 1)) // count)
        return [(left, top + index * (each + gap), right, top + index * (each + gap) + each) for index in range(count)]
    each = max(1, (right - left - gap * (count - 1)) // count)
    return [(left + index * (each + gap), top, left + index * (each + gap) + each, bottom) for index in range(count)]


def paste_assets(canvas: Image.Image, assets: list[AssetRender], box: tuple[int, int, int, int], vertical: bool = False) -> None:
    for asset, asset_box in zip(assets, asset_boxes(box, len(assets), vertical=vertical)):
        paste_asset(canvas, asset, asset_box)


def _redesign_accent(scene: dict[str, Any]) -> tuple[str, str, str]:
    """Return semantic colors for the Episode 013 redesign variants."""
    role = str(scene.get("visual_role") or "")
    if role in {"case_a", "case_b", "case_c", "case_d"}:
        if role == "case_a":
            return "#eaf7ee", "#63a975", "#3f8c58"
        if role == "case_b":
            return "#eaf4ff", "#2f74bb", "#205d9d"
        if role == "case_c":
            return "#e1f3f3", "#2f857f", "#246e69"
        return "#fff2d7", "#d3922e", "#9b681d"
    return "#eaf4ff", "#2f74bb", "#173a68"


def draw_redesign_threshold_focus(
    canvas: Image.Image,
    scene: dict[str, Any],
    ink: str,
    soft: str,
    blue: str,
    blue_strong: str,
    green: str,
    green_strong: str,
) -> None:
    """大きな数字を主役にする、Episode 013の閾値専用レイアウト。"""
    draw = ImageDraw.Draw(canvas)
    draw_headline(draw, (110, 158, 1810, 315), scene, 112, 82, 2, "center", 0.10)
    draw_fitted(draw, (180, 318, 1740, 388), str(scene.get("support_text") or ""), 54, 46, soft, 2, "center", 0.12)
    cards = compare_default(scene)
    columns = [(100, 430, 900, 800), (1020, 430, 1820, 800)]
    fills = ["#eaf4ff", "#eaf7ee"]
    outlines = [blue_strong, green_strong]
    for index, (title, body, _color) in enumerate(cards):
        left, top, right, bottom = columns[index]
        rounded_rectangle(draw, (left + 8, top + 10, right + 8, bottom + 10), 34, "#b9ccd8")
        rounded_rectangle(draw, (left, top, right, bottom), 34, fills[index], outlines[index], 5)
        draw.rectangle((left, top, left + 18, bottom), fill=outlines[index])
        draw_fitted(draw, (left + 64, top + 38, right - 44, top + 116), title, 58, 46, ink, 1, "left", 0.10)
        draw_fitted(draw, (left + 54, top + 146, right - 44, bottom - 46), body, 132, 84, ink, 2, "center", 0.08)
    if str(scene.get("main_message") or ""):
        message_fill = green if "全員" in str(scene.get("main_message")) else blue
        message_text = green_strong if "全員" in str(scene.get("main_message")) else blue_strong
        message_box = (330, 824, 1590, 892)
        rounded_rectangle(draw, message_box, 30, message_fill)
        draw_fitted(draw, (message_box[0] + 42, message_box[1] + 6, message_box[2] - 42, message_box[3] - 6), str(scene.get("main_message") or ""), 64, 48, message_text, 2, "center")


def draw_redesign_fact_focus(
    canvas: Image.Image,
    scene: dict[str, Any],
    ink: str,
    soft: str,
    blue: str,
    blue_strong: str,
    green: str,
    green_strong: str,
) -> None:
    """公式Factを、公式UIを再現せず一つの数字メッセージで見せる。"""
    draw = ImageDraw.Draw(canvas)
    draw_headline(draw, (120, 142, 1800, 294), scene, 112, 80, 2, "center", 0.10)
    draw_fitted(draw, (220, 306, 1700, 374), str(scene.get("support_text") or ""), 56, 52, soft, 1, "center", 0.12)

    panel = (280, 398, 1640, 720)
    rounded_rectangle(draw, panel, 44, "#eef6fc", "#cfe0f0", 4)
    draw.rectangle((panel[0], panel[1] + 44, panel[0] + 18, panel[3] - 44), fill=blue_strong)

    # 端末の輪郭だけを使い、LINEの画面やロゴを再現しない。
    phone = (430, 448, 650, 672)
    rounded_rectangle(draw, phone, 34, "#f8fbfe", blue_strong, 5)
    draw.rounded_rectangle((495, 466, 585, 477), radius=5, fill="#9fc6df")
    draw.ellipse((520, 625, 560, 665), outline="#9fc6df", width=4)

    draw_fitted(draw, (760, 430, 1500, 530), "LINE", 96, 76, ink, 1, "left", 0.10)
    draw_fitted(draw, (730, 540, 1530, 686), "14.6.3以上", 132, 88, blue_strong, 1, "left", 0.08)

    message = str(scene.get("main_message") or "")
    if message:
        message_box = (200, 752, 1720, 900)
        rounded_rectangle(draw, message_box, 30, "#eaf4ff")
        draw_fitted(draw, (242, 766, 1678, 888), message, 60, 52, blue_strong, 2, "center", 0.10)


def draw_redesign_capture_focus(
    canvas: Image.Image,
    scene: dict[str, Any],
    assets: list[AssetRender],
    ink: str,
    soft: str,
    blue: str,
    blue_strong: str,
) -> None:
    """実機差し替え後も画面が主役になるCapture Required用レイアウト。"""
    draw = ImageDraw.Draw(canvas)
    draw_headline(draw, (100, 154, 1820, 294), scene, 110, 80, 2, "center", 0.10)
    left, top, right, bottom = (100, 342, 820, 842)
    points = [str(point) for point in (scene.get("visual_points") or []) if str(point).strip()]
    if points:
        gap = 24
        card_h = max(128, (bottom - top - gap * (len(points) - 1)) // len(points))
        for index, point in enumerate(points[:3]):
            y = top + index * (card_h + gap)
            fill = "#eaf4ff" if index % 2 == 0 else "#eaf7ee"
            outline = blue_strong if index % 2 == 0 else "#63a975"
            rounded_rectangle(draw, (left, y, right, y + card_h), 28, fill, outline, 4)
            draw.line((left + 30, y + 28, left + 30, y + card_h - 28), fill=outline, width=8)
            draw_fitted(draw, (left + 72, y + 24, right - 28, y + card_h - 24), point, 60, 48, ink, 2, "left", 0.10)
    else:
        rounded_rectangle(draw, (left, top, right, top + 210), 28, "#eaf4ff", blue_strong, 4)
        draw_fitted(draw, (left + 30, top + 40, right - 30, top + 166), str(scene.get("support_text") or ""), 58, 48, ink, 2, "center", 0.10)
    if str(scene.get("main_message") or ""):
        draw_message_bar(draw, (left, 704, right, 842), str(scene.get("main_message") or ""), blue, blue_strong)
    capture_box = (930, 330, 1810, 842)
    rounded_rectangle(draw, capture_box, 38, "#ffffff", "#8fb6ce", 5)
    if assets:
        paste_assets(canvas, assets, (990, 390, 1750, 790), vertical=False)
    else:
        draw_fitted(draw, (1010, 352, 1730, 418), "見る場所", 52, 46, soft, 1, "center")
        draw_neutral_visual_frame(canvas, (1010, 430, 1730, 790), scene)


def draw_redesign_capture_focus_tall(
    canvas: Image.Image,
    scene: dict[str, Any],
    assets: list[AssetRender],
    ink: str,
    soft: str,
    blue: str,
    blue_strong: str,
) -> None:
    """OS更新の実機枠を縦長端末として見せる差分レイアウト。"""
    draw = ImageDraw.Draw(canvas)
    draw_headline(draw, (100, 154, 1820, 294), scene, 110, 80, 2, "center", 0.10)
    left, top, right = (100, 338, 820)
    points = [str(point) for point in (scene.get("visual_points") or []) if str(point).strip()]
    has_message = bool(str(scene.get("main_message") or "").strip())
    point_bottom = 610 if has_message else 842
    if points:
        gap = 24
        card_h = max(128, (point_bottom - top - gap * (len(points) - 1)) // len(points))
        for index, point in enumerate(points[:3]):
            y = top + index * (card_h + gap)
            fill = "#eaf4ff" if index % 2 == 0 else "#e1f3f3"
            outline = blue_strong if index % 2 == 0 else "#2f857f"
            rounded_rectangle(draw, (left, y, right, y + card_h), 28, fill, outline, 4)
            draw.line((left + 30, y + 28, left + 30, y + card_h - 28), fill=outline, width=8)
            draw_fitted(draw, (left + 72, y + 24, right - 28, y + card_h - 24), point, 60, 48, ink, 2, "left", 0.10)
    else:
        rounded_rectangle(draw, (left, top, right, point_bottom), 28, "#eaf4ff", blue_strong, 4)
        draw_fitted(draw, (left + 30, top + 40, right - 30, point_bottom - 40), str(scene.get("support_text") or ""), 58, 48, ink, 2, "center", 0.10)
    if has_message:
        draw_message_bar(draw, (left, 654, right, 842), str(scene.get("main_message") or ""), blue, blue_strong)
    capture_box = (970, 308, 1810, 842)
    rounded_rectangle(draw, capture_box, 38, "#ffffff", "#8fb6ce", 5)
    if assets:
        paste_assets(canvas, assets, (1100, 350, 1720, 800), vertical=True)
    else:
        draw_fitted(draw, (1080, 334, 1700, 400), "見る場所", 52, 46, soft, 1, "center")
        draw_neutral_visual_frame(canvas, (1135, 410, 1665, 790), scene)


def draw_redesign_flow_focus(
    canvas: Image.Image,
    scene: dict[str, Any],
    ink: str,
    soft: str,
    blue_strong: str,
) -> None:
    """LINE → OS → LINEを図解ではなく一つの大きな進行として描く。"""
    draw = ImageDraw.Draw(canvas)
    draw_headline(draw, (120, 150, 1800, 292), scene, 112, 82, 2, "center", 0.10)
    draw_fitted(draw, (220, 305, 1700, 374), str(scene.get("support_text") or ""), 54, 46, soft, 2, "center", 0.12)
    steps = [str(item) for item in (scene.get("flow_steps") or ["LINE", "OS", "LINE"])][:3]
    substeps = [str(item) for item in (scene.get("flow_substeps") or [])][:3]
    centers = [370, 960, 1550]
    fills = ["#eaf4ff", "#e1f3f3", "#eaf7ee"]
    outlines = ["#2f74bb", "#2f857f", "#63a975"]
    for index, center in enumerate(centers):
        if index < len(centers) - 1:
            next_center = centers[index + 1]
            draw.line((center + 188, 566, next_center - 188, 566), fill="#8eb8c9", width=8)
            draw.polygon([(next_center - 205, 548), (next_center - 205, 584), (next_center - 170, 566)], fill="#2f74bb")
        rounded_rectangle(draw, (center - 220, 420, center + 220, 716), 42, fills[index], outlines[index], 5)
        draw_fitted(draw, (center - 190, 462, center + 190, 580), steps[index] if index < len(steps) else "", 108, 78, ink, 1, "center", 0.08)
        if index < len(substeps):
            draw_fitted(draw, (center - 180, 612, center + 180, 684), substeps[index], 54, 46, ink, 2, "center", 0.10)
    if str(scene.get("main_message") or ""):
        draw_message_bar(draw, (290, 800, 1630, 890), str(scene.get("main_message") or ""), "#eaf4ff", blue_strong)


def draw_redesign_case_result(
    canvas: Image.Image,
    scene: dict[str, Any],
    ink: str,
    soft: str,
) -> None:
    """ケースA〜Dを、同じ表ではなく状況→次の一手の分岐として描く。"""
    draw = ImageDraw.Draw(canvas)
    fill, outline, strong = _redesign_accent(scene)
    draw_headline(draw, (130, 158, 1790, 300), scene, 112, 78, 2, "center", 0.10)
    case_label = str(scene.get("case_label") or "")
    condition = str(scene.get("case_condition") or "")
    action = str(scene.get("case_action") or scene.get("main_message") or "")
    note = str(scene.get("case_note") or "")
    left_box = (120, 410, 850, 774)
    right_box = (1070, 410, 1800, 774)
    rounded_rectangle(draw, left_box, 38, "#ffffff", outline, 5)
    rounded_rectangle(draw, right_box, 38, fill, outline, 5)
    draw_fitted(draw, (170, 448, 800, 512), case_label, 52, 46, strong, 1, "left", 0.10)
    draw_fitted(draw, (170, 548, 800, 704), condition, 76, 58, ink, 3, "left", 0.10)
    draw_fitted(draw, (1120, 448, 1750, 512), "次にすること", 52, 46, strong, 1, "left", 0.10)
    draw_fitted(draw, (1120, 548, 1750, 704), action, 82, 60, ink, 3, "left", 0.10)
    draw.line((880, 592, 1000, 592), fill=outline, width=8)
    draw.polygon([(1000, 570), (1000, 614), (1040, 592)], fill=outline)
    if str(scene.get("icon_name") or ""):
        draw_small_semantic_icon(canvas, str(scene.get("icon_name") or ""), str(scene.get("icon_tone") or "blue"), (1650, 670), 84)
    if note:
        draw_message_bar(draw, (260, 812, 1660, 892), note, fill, strong)


def draw_redesign_bridge_clean(
    canvas: Image.Image,
    scene: dict[str, Any],
    theme: dict[str, Any],
    ink: str,
    soft: str,
) -> None:
    """関連動画への橋渡しを、注意表ではなく一つの落ち着いた案内にする。"""
    draw = ImageDraw.Draw(canvas)
    draw_headline(draw, (140, 166, 1790, 316), scene, 112, 80, 2, "center", 0.10)
    draw_icon_stage(
        canvas,
        scene,
        (470, 562),
        "#eaf7ee",
        diameter=190,
        icon_size=132,
        plate_theme=theme.get("icon_plate", {}),
    )
    rounded_rectangle(draw, (720, 390, 1780, 760), 40, "#eaf4ff", "#2f74bb", 5)
    draw_fitted(draw, (790, 460, 1710, 560), str(scene.get("support_text") or ""), 66, 54, ink, 2, "left", 0.10)
    draw_message_bar(draw, (790, 610, 1710, 712), str(scene.get("main_message") or ""), "#ffffff", "#2f74bb")


def draw_redesign_summary_three(
    canvas: Image.Image,
    scene: dict[str, Any],
    ink: str,
    blue_strong: str,
) -> None:
    """まとめを大きな1/2/3と短い語句に絞る。"""
    draw = ImageDraw.Draw(canvas)
    draw_headline(draw, (130, 150, 1790, 292), scene, 112, 82, 2, "center", 0.10)
    draw_fitted(draw, (220, 305, 1700, 374), str(scene.get("support_text") or ""), 54, 46, "#587187", 2, "center", 0.12)
    items = [str(item) for item in (scene.get("items") or [])][:3]
    centers = [370, 960, 1550]
    fills = ["#eaf4ff", "#eaf7ee", "#e1f3f3"]
    outlines = ["#2f74bb", "#63a975", "#2f857f"]
    for index, center in enumerate(centers):
        rounded_rectangle(draw, (center - 220, 420, center + 220, 770), 42, fills[index], outlines[index], 5)
        draw_fitted(draw, (center - 180, 462, center + 180, 610), str(index + 1), 132, 100, outlines[index], 1, "center", 0.06)
        draw_fitted(draw, (center - 180, 635, center + 180, 724), items[index] if index < len(items) else "", 58, 46, ink, 2, "center", 0.10)
    if str(scene.get("main_message") or ""):
        draw_message_bar(draw, (220, 810, 1700, 892), str(scene.get("main_message") or ""), "#eaf7ee", "#3f8c58")


THEME_DEFAULT_PROFILE = "adult_digital_soft_background"

_SECTION_THEME_KEY = {
    "はじめに": "intro",
    "1 / 3": "sec1",
    "2 / 3": "sec2",
    "3 / 3": "sec3",
    "困ったとき": "contact",
    "困ったときは": "contact",
    "まとめ": "summary",
}


def theme_profile_for_episode(data: dict[str, Any]) -> str:
    """Return the episode-selected visual theme profile.

    The selector is intentionally metadata-only so an episode can reuse the
    same renderer with a different background asset without hard-coding an
    episode-specific branch.
    """
    metadata = data.get("metadata")
    if isinstance(metadata, dict) and metadata.get("visual_theme"):
        return str(metadata["visual_theme"])
    if data.get("visual_theme"):
        return str(data["visual_theme"])
    return THEME_DEFAULT_PROFILE


def theme_profile_css_class(profile: str) -> str:
    """Convert a config profile name into a safe CSS class suffix."""
    safe = "".join(char if char.isalnum() else "-" for char in str(profile).lower())
    return "theme-profile-" + (safe or "default")


def load_visual_theme(profile: str | None = None) -> dict[str, Any]:
    """共通Background System（config/visual_theme.json・Episode 008以降の恒久ルール）。"""
    path = ROOT / "config" / "visual_theme.json"
    try:
        root = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(root, dict):
        return {}
    profiles = root.get("profiles", {})
    if isinstance(profiles, dict):
        requested = str(profile or THEME_DEFAULT_PROFILE)
        for profile_name in (requested, THEME_DEFAULT_PROFILE, "default"):
            found = profiles.get(profile_name)
            if isinstance(found, dict):
                return found
    return root if "base" in root else {}


def theme_background_path(theme: dict[str, Any], episode_dir: Path | None = None) -> Path:
    """Resolve an image-theme asset and fail closed when it is unavailable."""
    asset = theme.get("asset") or theme.get("background_asset")
    if not asset:
        raise FileNotFoundError("visual theme background asset is not configured")
    path = resolve_repo_path(str(asset), episode_dir)
    if not path.exists():
        raise FileNotFoundError(f"visual theme background asset is missing: {path}")
    return path


def paint_image_background(canvas: Image.Image, theme: dict[str, Any], episode_dir: Path | None = None) -> Path:
    """Place the configured background image full-screen with aspect-preserving cover fit."""
    path = theme_background_path(theme, episode_dir)
    with Image.open(path) as source:
        background = ImageOps.fit(
            source.convert("RGBA"),
            (WIDTH, HEIGHT),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5),
        )
    canvas.alpha_composite(background, (0, 0))
    return path


def hex_rgba(color: str, alpha: int) -> tuple[int, int, int, int]:
    text = str(color or "").lstrip("#")
    try:
        if len(text) == 3:
            text = "".join(ch * 2 for ch in text)
        return (int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16), int(alpha))
    except (ValueError, IndexError):
        return (47, 116, 187, int(alpha))


def theme_section_key(section_label: str) -> str:
    return _SECTION_THEME_KEY.get(str(section_label or "").strip(), "intro")


def section_style(section_label: str, layout: str, theme: dict[str, Any]) -> dict[str, Any]:
    style = dict(theme.get("sections", {}).get(theme_section_key(section_label), {}))
    if layout == "layout_06_caution":
        caution = theme.get("caution", {})
        if isinstance(caution, dict) and caution:
            style.update(caution)
    return style


def paint_gradient(canvas: Image.Image, theme: dict[str, Any]) -> None:
    """白に近い淡いブルーのsoft gradient（左上→中央ほぼ白→右下にわずかな青み）。

    上端は top_left→center、下端は center→bottom_right を水平補間し、縦にブレンドする。
    全画素で重み和=1になるため黒落ちしない。
    """
    base = theme.get("base", {})
    top_left = hex_rgba(base.get("top_left", "#eef6fc"), 255)[:3]
    center = hex_rgba(base.get("center", "#ffffff"), 255)[:3]
    bottom_right = hex_rgba(base.get("bottom_right", "#edf5fb"), 255)[:3]
    gw, gh = 148, 84
    small = Image.new("RGB", (gw, gh))
    pixels = ImageDraw.Draw(small)
    for y in range(gh):
        v = y / max(1, gh - 1)
        for x in range(gw):
            u = x / max(1, gw - 1)
            top_edge = tuple(int(top_left[i] * (1 - u) + center[i] * u) for i in range(3))
            bottom_edge = tuple(int(center[i] * (1 - u) + bottom_right[i] * u) for i in range(3))
            color = tuple(int(top_edge[i] * (1 - v) + bottom_edge[i] * v) for i in range(3))
            pixels.point((x, y), fill=color)
    gradient = small.resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)
    canvas.paste(gradient, (0, 0))


def paint_decorations(canvas: Image.Image, scene: dict[str, Any], section_label: str, theme: dict[str, Any], layout: str) -> None:
    """共通の薄い装飾（large translucent circle・dot cluster・thin accent line・tint面）。

    decorationには意味がない・文字の下に描く・低opacityで文字より目立たせない（恒久ルール）。
    RGBAオーバーレイに描いてからalpha_compositeする（convert RGB時にアルファが消えないため）。
    """
    style = section_style(section_label, layout, theme)
    accent = hex_rgba(style.get("accent_hex", "#2f74bb"), 255)[:3]
    tint = hex_rgba(style.get("tint", "#dbe9f7"), 255)[:3]
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    pos = str(style.get("tint_position", "top_left"))
    if pos == "right_top":
        ellipse = (1360, 60, 2000, 760)
    elif pos == "left_bottom":
        ellipse = (-80, 540, 860, 1080)
    elif pos == "right_bottom":
        ellipse = (1280, 560, 2000, 1020)
    else:
        ellipse = (-80, -120, 900, 620)
    draw.ellipse(ellipse, fill=tint + (26,))
    deco = theme.get("decoration", {})
    circle = deco.get("circle", {})
    if circle.get("enabled", True):
        diameter = int(circle.get("diameter", 720))
        alpha = int(float(circle.get("opacity", 0.07)) * 255)
        left, top = int(circle.get("x", 90)), int(circle.get("y", 120))
        draw.ellipse((left, top, left + diameter, top + diameter), fill=accent + (alpha,))
    dots = deco.get("dots", {})
    if dots.get("enabled", True):
        count = int(dots.get("count", 4))
        radius = max(2, int(dots.get("diameter", 13)) // 2)
        alpha = int(float(dots.get("opacity", 0.10)) * 255)
        base_x, base_y = int(dots.get("x", 1810)), int(dots.get("y", 850))
        for index in range(count):
            dx = base_x - index * 34
            dy = base_y - (index % 2) * 26
            draw.ellipse((dx - radius, dy - radius, dx + radius, dy + radius), fill=accent + (alpha,))
    line = deco.get("line", {})
    if line.get("enabled", True):
        alpha = int(float(line.get("opacity", 0.10)) * 255)
        width = int(line.get("width", 6))
        x0 = int(line.get("x", 120))
        y0 = int(line.get("y", 208))
        length = int(line.get("length", 300))
        draw.line((x0, y0, x0 + length, y0), fill=accent + (alpha,), width=width)
    canvas.alpha_composite(overlay)


def draw_section_pill(draw: ImageDraw.ImageDraw, section_label: str, theme: dict[str, Any], layout: str) -> None:
    """セクション表示（左上のrounded pill・44px以上・恒久ルール）。"""
    label = str(section_label or "").strip()
    if not label:
        return
    pill = theme.get("section_pill", {})
    font_size = max(int(pill.get("min_font", 44)), int(pill.get("default_font", 52)))
    font = pil_font(font_size)
    padding = int(pill.get("padding_x", 46))
    width = int(draw.textlength(label, font=font)) + padding * 2
    x = int(pill.get("x", 100))
    y = int(pill.get("y", 88))
    height = int(pill.get("height", 72))
    rounded_rectangle(
        draw,
        (x, y, x + width, y + height),
        int(pill.get("radius", 36)),
        str(pill.get("fill", "#ffffff")),
        str(pill.get("outline", "#c8deed")),
        int(pill.get("outline_width", 3)),
    )
    text_color = str(section_style(section_label, layout, theme).get("pill_text", "#2f74bb"))
    draw.text((x + padding, y + (height - font_size) // 2), label, font=font, fill=text_color)


def draw_minimal_accent_line(
    draw: ImageDraw.ImageDraw,
    section_label: str,
    theme: dict[str, Any],
    layout: str,
) -> None:
    """Draw only the purposeful thin section/caution accent for image themes."""
    config = theme.get("minimal_accent_line", {})
    if not isinstance(config, dict) or not config.get("enabled"):
        return
    excluded = config.get("exclude_layouts", [])
    if isinstance(excluded, list) and layout in {str(value) for value in excluded}:
        return
    style = section_style(section_label, layout, theme)
    color = str(style.get("accent_hex", "#2f74bb"))
    x = int(config.get("x", 520))
    y = int(config.get("y", 174))
    length = int(config.get("length", 280))
    width = max(1, int(config.get("width", 4)))
    draw.line((x, y, x + length, y), fill=color, width=width)


def fill_soft_gradient(canvas: Image.Image) -> None:
    """Give a text-only scene a calm full-width visual field."""
    top = 14
    bottom = HEIGHT - SAFE_HEIGHT
    gradient = Image.new("RGB", (WIDTH, bottom - top))
    pixels = ImageDraw.Draw(gradient)
    left = (235, 247, 255)
    right = (255, 247, 226)
    for x in range(WIDTH):
        ratio = x / max(1, WIDTH - 1)
        color = tuple(round(left[index] * (1 - ratio) + right[index] * ratio) for index in range(3))
        pixels.line((x, 0, x, bottom - top), fill=color)
    canvas.paste(gradient, (0, top))


def render_pillow_scene(
    scene: dict[str, Any],
    section_label: str,
    assets: list[AssetRender],
    output_path: Path,
    theme_enabled: bool = True,
    theme_profile: str | None = None,
    episode_dir: Path | None = None,
) -> None:
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), "#ffffff")
    render_mode = str(scene.get("render_mode") or "template")
    layout = str(scene.get("layout") or "")
    theme: dict[str, Any] = {}
    if theme_enabled and render_mode != "gpt_image":
        theme = load_visual_theme(theme_profile)
        if str(theme.get("background_type") or "gradient") == "image":
            # The configured asset is authoritative.  Missing assets fail
            # closed so a dummy white/placeholder background cannot reach a
            # contact sheet or draft.
            paint_image_background(canvas, theme, episode_dir)
        else:
            paint_gradient(canvas, theme)
            if theme.get("overlay_decorations", True):
                paint_decorations(canvas, scene, section_label, theme, layout)
    if str(scene.get("background_fill") or "") == "soft_gradient":
        fill_soft_gradient(canvas)

    draw = ImageDraw.Draw(canvas)
    if theme_enabled and render_mode != "gpt_image":
        if theme.get("top_bar_enabled", True):
            draw.rectangle((0, 0, WIDTH, 14), fill=str(theme.get("top_bar", "#2f74bb")))
    else:
        draw.rectangle((0, 0, WIDTH, 14), fill="#2f74bb")
    # Subtitle-safe band is always renderer-owned and starts at y=900.
    draw.rectangle((0, HEIGHT - SAFE_HEIGHT, WIDTH, HEIGHT), fill="#f7fbfe")
    draw.line((0, HEIGHT - SAFE_HEIGHT, WIDTH, HEIGHT - SAFE_HEIGHT), fill="#c8deed", width=3)

    layout = str(scene.get("layout"))
    headline = str(scene.get("headline") or "")
    support = str(scene.get("support_text") or "")
    main_message = str(scene.get("main_message") or "")
    ink, soft = "#173a68", "#587187"
    blue, blue_strong = "#eaf4ff", "#2f74bb"
    green, green_strong = "#eaf7ee", "#63a975"
    amber = "#fff2d7"
    image_theme = str(theme.get("background_type") or "gradient") == "image"

    if section_label:
        draw_section_pill(draw, section_label, theme, layout)
        if str(theme.get("background_type") or "") == "image":
            draw_minimal_accent_line(draw, section_label, theme, layout)

    design_variant = str(scene.get("design_variant") or "").strip()
    if design_variant == "fact_focus":
        draw_redesign_fact_focus(canvas, scene, ink, soft, blue, blue_strong, green, green_strong)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.convert("RGB").save(output_path, "PNG")
        return
    if design_variant == "threshold_focus":
        draw_redesign_threshold_focus(canvas, scene, ink, soft, blue, blue_strong, green, green_strong)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.convert("RGB").save(output_path, "PNG")
        return
    if design_variant == "capture_focus":
        draw_redesign_capture_focus(canvas, scene, assets, ink, soft, blue, blue_strong)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.convert("RGB").save(output_path, "PNG")
        return
    if design_variant == "capture_focus_tall":
        draw_redesign_capture_focus_tall(canvas, scene, assets, ink, soft, blue, blue_strong)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.convert("RGB").save(output_path, "PNG")
        return
    if design_variant == "flow_focus":
        draw_redesign_flow_focus(canvas, scene, ink, soft, blue_strong)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.convert("RGB").save(output_path, "PNG")
        return
    if design_variant == "case_result":
        draw_redesign_case_result(canvas, scene, ink, soft)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.convert("RGB").save(output_path, "PNG")
        return
    if design_variant == "bridge_clean":
        draw_redesign_bridge_clean(canvas, scene, theme, ink, soft)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.convert("RGB").save(output_path, "PNG")
        return
    if design_variant == "summary_three":
        draw_redesign_summary_three(canvas, scene, ink, blue_strong)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.convert("RGB").save(output_path, "PNG")
        return

    if layout == "layout_01_hero":
        if assets:
            paste_assets(canvas, assets, (40, 140, 760, 800))
            draw_headline(draw, (760, 138, 1800, 490), scene, 122, 78, 3, "left", 0.12)
            draw_fitted(draw, (760, 505, 1770, 625), support, 54, 42, soft, 2, "left", 0.16)
            if main_message:
                draw_message_bar(draw, (760, 680, 1780, 805), main_message, blue, blue_strong)
        else:
            # semantic icon: 意味を持つSVGアイコン（login等）を淡い円に載せる
            numeric_scene = any(ch.isdigit() for ch in headline)
            icon_center = (960, 205) if numeric_scene else (960, 225)
            if not draw_icon_stage(
                canvas, scene, icon_center, ICON_CIRCLE.get(str(scene.get("icon_tone") or ""), "#e9edf5"),
                plate_theme=theme.get("icon_plate", {}),
            ):
                draw_neutral_visual_frame(canvas, (760, 130, 1160, 320), scene)
            if numeric_scene:
                panel = theme.get("numerical_panel", {})
                rounded_rectangle(
                    draw, (350, 350, 1570, 690), int(panel.get("radius", 44)),
                    str(panel.get("fill", "#eef6fc")), str(panel.get("outline", "#cfe0f0")),
                    int(panel.get("outline_width", 4)),
                )
                motif_alpha = int(panel.get("motif_alpha", 40))
                if motif_alpha > 0:
                    draw.ellipse((430, 380, 700, 650), fill=hex_rgba("#dcebf9", motif_alpha))
                    draw.ellipse((1220, 380, 1490, 650), fill=hex_rgba("#e4f3ea", motif_alpha))
                draw_headline(draw, (420, 380, 1500, 660), scene, 116, 80, 2, "center", 0.10)
            else:
                draw_headline(draw, (240, 380, 1680, 600), scene, 118, 76, 2, "center", 0.12)
            support_box = (140, 700, 1780, 764) if image_theme else (140, 706, 1780, 804)
            draw_fitted(draw, support_box, support, 52, 44, soft, 2, "center", 0.16)
            if main_message:
                if image_theme:
                    # v4: 数字panelと同じ中央軸・同じ幅に揃え、source/supportとの
                    # 縦階層を保ったまま字幕帯の直上へ置く。
                    message_box = (350, 778, 1570, 898)
                else:
                    message_box = (500, 812, 1420, 888)
                    if draw.textlength(main_message, font=pil_font(52)) > 760:
                        # 長い補助文は横幅を確保し、字幕帯と重ねず読ませる。
                        message_box = (400, 780, 1780, 890)
                draw_message_bar(draw, message_box, main_message, blue, blue_strong)
    elif layout == "layout_02_list":
        headline_box = (150, 160, 1770, 300) if image_theme else (150, 106, 1770, 250)
        support_box = (170, 310, 1750, 380) if image_theme else (170, 256, 1750, 336)
        draw_headline(draw, headline_box, scene, 112, 82, 2, "center", 0.12)
        draw_fitted(draw, support_box, support, 52, 44, soft, 2, "center", 0.12)
        rows = [str(item) for item in (scene.get("items") or [main_message or "確認ポイント"])]
        top = 400 if image_theme else 368
        bottom = 838
        row_h = max(96, (bottom - top) // max(1, len(rows)))
        card = theme.get("list_item_card", {})
        for index, item in enumerate(rows, 1):
            y = top + (index - 1) * row_h
            rounded_rectangle(
                draw, (150, y + int(card.get("inset_y", 6)), 1770, y + row_h - 14),
                int(card.get("radius", 26)), str(card.get("fill", "#ffffff")),
                str(card.get("outline", "#d9e7ef")), int(card.get("outline_width", 3)),
            )
            draw.ellipse((176, y + 16, 254, y + 94), fill=green)
            draw_fitted(draw, (176, y + 24, 254, y + 88), str(index), 46, 44, "#438a58", 1, "center")
            draw_fitted(draw, (298, y + 14, 1740, y + row_h - 10), item, 52 if len(rows) <= 4 else 48, 46, ink, 2, "left", 0.12)
    elif layout == "layout_03_visual_text":
        visual_box = (50, 145, 830, 795)
        if assets:
            paste_assets(canvas, assets, visual_box)
        elif "バトンタッチ" in headline or "1つ" in headline:
            items = [str(item) for item in (scene.get("items") or [])]
            step1 = items[0] if len(items) > 0 else "手順1"
            step2 = items[1] if len(items) > 1 else "手順2"
            rounded_rectangle(draw, visual_box, 42, blue)
            node_left = (170, 315, 690, 435)
            node_right = (170, 565, 690, 685)
            rounded_rectangle(draw, node_left, 26, "#ffffff")
            rounded_rectangle(draw, node_right, 26, green)
            draw_fitted(draw, (205, 335, 655, 415), step1, 52, 40, ink, 1, "center")
            draw_fitted(draw, (205, 585, 655, 665), step2, 52, 40, ink, 1, "center")
            draw_fitted(draw, (330, 438, 530, 570), "↓", 90, 64, blue_strong, 1, "center")
            draw_headline(draw, (900, 138, 1800, 425), scene, 116, 78, 3, "left", 0.12)
            draw_fitted(draw, (900, 460, 1780, 600), support, 52, 42, soft, 3, "left", 0.16)
            if main_message:
                draw_fitted(draw, (900, 650, 1770, 780), main_message, 44, 40, soft, 3, "left", 0.16)
        else:
            # semantic icon: 意味を持つSVGアイコン（support_agent等）を淡い円に載せる
            if not draw_icon_stage(
                canvas, scene, (960, 220), ICON_CIRCLE.get(str(scene.get("icon_tone") or ""), "#eaf7ee"),
                plate_theme=theme.get("icon_plate", {}),
            ):
                if "相談" in headline or "相談" in support or "窓口" in headline or "窓口" in support:
                    draw_badge(draw, (906, 152, 1014, 260), "相談", blue, blue_strong, 36)
                else:
                    draw_neutral_visual_frame(canvas, (760, 130, 1160, 320), scene)
            draw_headline(draw, (240, 350, 1680, 570), scene, 112, 74, 2, "center", 0.12)
            draw_fitted(draw, (140, 600, 1780, 710), support, 54, 46, soft, 2, "center", 0.16)
            if main_message:
                draw_fitted(draw, (140, 722, 1780, 836), main_message, 52, 44, soft, 2, "center", 0.16)
    elif layout == "layout_04_text_official":
        headline_box = (110, 150, 1810, 285) if image_theme else (110, 82, 1810, 225)
        draw_headline(draw, headline_box, scene, 112, 82, 2, "center", 0.12)
        variant = official_visual_variant(scene)
        text_box = OFFICIAL_TEXT_BOX_CENTERED if variant == "safe_entry_options_centered" else OFFICIAL_TEXT_BOX
        draw_official_text_column(draw, canvas, scene, text_box, soft, blue, blue_strong)
        if assets:
            paste_assets(canvas, assets, OFFICIAL_VISUAL_BOX, vertical=len(assets) > 1)
        elif variant == "semantic_operation":
            draw_semantic_operation_visual(canvas, OFFICIAL_VISUAL_BOX, scene)
        elif variant != "safe_entry_options_centered":
            draw_neutral_visual_frame(canvas, OFFICIAL_VISUAL_BOX, scene)
    elif layout == "layout_05_compare":
        # Image-theme section pills sit in the quiet upper-left-center area;
        # keep the two-line compare headline below them before the cards.
        draw_headline(draw, (110, 130, 1810, 340), scene, 112, 88, 2, "center", 0.12)
        draw_fitted(draw, (150, 342, 1770, 398), support, 54, 44, soft, 2, "center", 0.14)
        cards = compare_default(scene)
        columns = [(110, 410, 900, 835), (1020, 410, 1810, 835)]
        fills = ["#eaf4ff", "#eaf7ee"]
        shadow = theme.get("compare", {}).get("shadow", {})
        for index, (title, body, _color) in enumerate(cards):
            left, top, right, bottom = columns[index]
            if shadow:
                rounded_rectangle(
                    draw,
                    (left + int(shadow.get("dx", 8)), top + int(shadow.get("dy", 10)), right + int(shadow.get("dx", 8)), bottom + int(shadow.get("dy", 10))),
                    int(shadow.get("radius", 34)), hex_rgba(str(shadow.get("fill", "#8fa9bd")), int(shadow.get("alpha", 55))),
                )
            rounded_rectangle(draw, (left, top, right, bottom), 34, fills[index])
            draw.rectangle((left, top, left + 16, bottom), fill=blue_strong if index == 0 else green_strong)
            draw_fitted(draw, (left + 54, top + 36, right - 40, top + 114), title, 54, 46, ink, 2, "left")
            if index < len(assets):
                paste_asset(canvas, assets[index], (left + 38, top + 140, right - 38, bottom - 28))
            else:
                draw_fitted(draw, (left + 54, top + 170, right - 44, bottom - 36), body, 52, 44, ink, 3, "left", 0.16)
    elif layout == "layout_06_caution":
        try:
            content_offset_x = int(scene.get("content_offset_x") or 0)
        except (TypeError, ValueError):
            content_offset_x = 0

        def shifted(box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
            return tuple(value + (content_offset_x if index % 2 == 0 else 0) for index, value in enumerate(box))

        # semantic icon: 意味を持つSVGアイコンを淡い円に載せる。
        # 単純記号の装飾fallbackは使わず、空き枠はneutral frameで処理する。
        if assets:
            caution_headline = (620, 90, 1080, 385)
            caution_support = (620, 430, 1080, 570)
            caution_message = (620, 620, 1080, 800)
        else:
            caution_headline = (240, 340, 1680, 560)
            caution_support = (140, 590, 1780, 700)
            caution_message = (140, 720, 1780, 830)
        draw_headline(draw, shifted(caution_headline), scene, 104, 70, 4, "center" if not assets else "left", 0.12)
        if not assets:
            draw_icon_stage(
                canvas, scene, (960, 215), ICON_CIRCLE.get(str(scene.get("icon_tone") or ""), "#fdf3e0"),
                plate_theme=theme.get("icon_plate", {}),
            )
        draw_fitted(draw, shifted(caution_support), support, 54, 44, soft, 3, "center" if not assets else "left", 0.16)
        if main_message:
            draw_fitted(draw, shifted(caution_message), main_message, 52, 44, soft, 3, "center" if not assets else "left", 0.16)
        if assets:
            paste_assets(canvas, assets, shifted((1120, 180, 1810, 840)), vertical=len(assets) > 1)
    elif layout == "layout_07_summary":
        configured_headline_box = scene.get("summary_headline_box")
        summary_headline_box = (120, 160, 1800, 303) if image_theme else (120, 82, 1800, 225)
        if isinstance(configured_headline_box, list) and len(configured_headline_box) == 4:
            try:
                summary_headline_box = tuple(int(value) for value in configured_headline_box)
            except (TypeError, ValueError):
                summary_headline_box = (120, 160, 1800, 303) if image_theme else (120, 82, 1800, 225)
        summary_support_box = (150, 310, 1770, 380) if image_theme else (150, 235, 1770, 315)
        draw_headline(draw, summary_headline_box, scene, 108, 80, 2, "center", 0.12)
        draw_fitted(draw, summary_support_box, support, 54, 44, soft, 2, "center", 0.14)
        rows = [str(item) for item in (scene.get("items") or [main_message or "確認ポイント"])]
        top = 400 if image_theme else 360
        row_h = max(88, 400 // max(1, len(rows)))
        for index, item in enumerate(rows):
            y = top + index * row_h
            draw.line((250, y + row_h - 16, 1680, y + row_h - 16), fill="#d9e7ef", width=3)
            draw.ellipse((180, y + 18, 270, y + 108), fill=green_strong)
            draw_fitted(draw, (180, y + 30, 270, y + 98), "✓", 52, 42, "#ffffff", 1, "center")
            draw_fitted(draw, (330, y + 20, 1680, y + row_h - 24), item, 58, 44, ink, 2, "left", 0.14)
    else:  # layout_08_section and a defensive fallback
        draw_headline(draw, (190, 215, 1730, 465), scene, 124, 84, 2, "center", 0.12)
        draw_fitted(draw, (230, 505, 1690, 640), support, 54, 42, soft, 2, "center", 0.16)
        draw_icon_stage(
            canvas, scene, (960, 754), ICON_CIRCLE.get(str(scene.get("icon_tone") or ""), "#eaf7ee"),
            plate_theme=theme.get("icon_plate", {}),
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output_path, "PNG")


def make_contact_sheet(output_dir: Path, scenes: list[dict[str, Any]], output_path: Path) -> None:
    columns = 5
    thumb_w, thumb_h = 320, 180
    cell_w, cell_h = 340, 270
    rows = max(1, (len(scenes) + columns - 1) // columns)
    sheet = Image.new("RGB", (columns * cell_w + 40, rows * cell_h + 40), "#eef6fa")
    draw = ImageDraw.Draw(sheet)
    label_font = pil_font(22)
    small_font = pil_font(18)
    for index, scene in enumerate(scenes):
        path = output_dir / f"scene_{int(scene['id']):03d}.png"
        x = 20 + (index % columns) * cell_w
        y = 20 + (index // columns) * cell_h
        if path.exists():
            try:
                with Image.open(path) as source:
                    thumb = ImageOps.fit(source.convert("RGB"), (thumb_w, thumb_h))
                sheet.paste(thumb, (x, y))
                draw.rectangle((x, y, x + thumb_w, y + thumb_h), outline="#c9d3dc", width=2)
            except OSError:
                draw.rectangle((x, y, x + thumb_w, y + thumb_h), fill="#fff0cf")
        else:
            draw.rectangle((x, y, x + thumb_w, y + thumb_h), fill="#fff0cf")
        label_y = y + thumb_h + 8
        draw.text((x, label_y), f"SCENE-{int(scene['id']):03d}", font=label_font, fill="#173a68")
        headline = str(scene.get("headline", ""))
        one_line = headline.replace("\n", " ")
        if len(one_line) > 20:
            one_line = one_line[:19] + "…"
        draw.text((x, label_y + 38), one_line, font=small_font, fill="#587187")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, "PNG")


def render_episode(
    episode_path: Path,
    output_dir: Path,
    contact_sheet_path: Path,
    engine: str = "auto",
    keep_html: bool = False,
    theme_enabled: bool = True,
    theme_profile: str | None = None,
) -> tuple[int, int, str]:
    data = load_json(episode_path)
    issues = validate_episode(data)
    if issues:
        raise SystemExit("episode.json validation failed:\n- " + "\n- ".join(issues))
    episode_dir = episode_dir_from_path(episode_path)
    selected_theme_profile = str(theme_profile or theme_profile_for_episode(data))
    scenes = data["scenes"]
    segment_by_id = {segment["id"]: segment for segment in data.get("narration_segments", [])}
    html_dir = output_dir / ".render_html"
    cache_dir = output_dir / ".asset_cache"
    if keep_html:
        html_dir.mkdir(parents=True, exist_ok=True)
    use_edge = engine in {"auto", "edge"}
    edge = edge_path() if use_edge else None
    edge_failed = False
    generated = 0
    missing: list[str] = []

    for scene in scenes:
        scene_id = int(scene["id"])
        first_segment = segment_by_id.get(int(scene["start_segment"]), {})
        section_label = str(scene.get("section_label") or first_segment.get("section") or "")
        assets, asset_missing = prepare_assets(scene, episode_dir, cache_dir)
        missing.extend(asset_missing)
        output_path = output_dir / f"scene_{scene_id:03d}.png"
        if edge and not scene.get("design_variant"):
            html_path = html_dir / f"scene_{scene_id:03d}.html"
            render_html_scene(scene, section_label, assets, html_path, selected_theme_profile, episode_dir)
            if render_with_edge(edge, html_path, output_path):
                generated += 1
                print(f"[OK] scene_{scene_id:03d}.png (edge)")
                continue
            if engine == "edge":
                print(f"[FAIL] scene_{scene_id:03d}.png (edge render failed)")
                continue
            if not edge_failed:
                print("[INFO] Edge/Chromium render unavailable; using Pillow for remaining scenes")
                edge_failed = True
            edge = None
        render_pillow_scene(
            scene,
            section_label,
            assets,
            output_path,
            theme_enabled=theme_enabled,
            theme_profile=selected_theme_profile,
            episode_dir=episode_dir,
        )
        generated += 1
        print(f"[OK] scene_{scene_id:03d}.png (pillow)")

    if not keep_html and html_dir.exists():
        shutil.rmtree(html_dir, ignore_errors=True)
    make_contact_sheet(output_dir, scenes, contact_sheet_path)
    print(f"[OK] {contact_sheet_path}")
    if missing:
        print("OFFICIAL_ASSET_FAIL")
        for value in missing:
            print(f"  {value}")
        return generated, len(missing), "fail"
    return generated, 0, "pass"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("episode", type=Path, help="path to episode.json")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "assets" / "generated_scenes")
    parser.add_argument("--contact-sheet", type=Path)
    parser.add_argument("--engine", choices=["auto", "edge", "pillow"], default="auto")
    parser.add_argument("--theme", choices=["auto", "none"], default="auto", help="共通Background System（config/visual_theme.json）を有効にするか。none=旧白背景（比較用）")
    parser.add_argument("--theme-profile", help="config/visual_theme.jsonのprofile名。未指定時はepisode.jsonのvisual_themeを使う")
    parser.add_argument("--keep-html", action="store_true", help="keep generated HTML for inspection")
    args = parser.parse_args()
    output_dir = args.output_dir.resolve()
    contact = (args.contact_sheet or output_dir / "scene_contact_sheet.png").resolve()
    theme_enabled = args.theme != "none"
    generated, missing, status = render_episode(
        args.episode.resolve(),
        output_dir,
        contact,
        args.engine,
        args.keep_html,
        theme_enabled=theme_enabled,
        theme_profile=args.theme_profile,
    )
    print(f"rendered={generated} expected={len(load_json(args.episode.resolve())['scenes'])} missing_official_assets={missing}")
    return 2 if status == "fail" else 1 if generated == 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
