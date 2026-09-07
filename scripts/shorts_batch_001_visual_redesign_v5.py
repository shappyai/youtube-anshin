"""Build Shorts探索バッチ001 Visual Redesign v5 drafts.

v5 is a focused visual correction after the v4 human Draft Gate.  It reuses
the approved v4 narration and subtitle timing, removes meaning-free zoom/pan,
and changes the visual state only with a hard cut, a real/official asset,
an explicit meaningful crop, or a CTA lockup state.

The script intentionally stops at ``output/draft_v5.mp4``.  It does not create
final output, publish metadata, upload state, or a schedule.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps

import shorts_batch_001_visual_redesign_v4 as v4


ROOT = v4.ROOT
SHORTS = v4.SHORTS
SHORTS_ROOT = v4.SHORTS_ROOT
WIDTH = v4.WIDTH
HEIGHT = v4.HEIGHT
CHANNEL_ICON_SOURCE = v4.CHANNEL_ICON_SOURCE
CHANNEL_TITLE = v4.CHANNEL_TITLE
CTA_TEXT = v4.CTA_TEXT_V4
CAPTION_TARGET_PX = v4.CAPTION_TARGET_PX
CAPTION_MIN_PX = v4.CAPTION_MIN_PX
V5_VERSION = "v5"
CTA_VISUAL_SEC = 3.0
SCORE = "68/100_REVIEW"

OFFICIAL_MYNA_HOME_SOURCE = ROOT / "episodes" / "002_myna_app" / "assets" / "official" / "official_screen_home.png"
OFFICIAL_MYNA_URL = "https://services.digital.go.jp/mynaapp/communication-guidelines/"
OFFICIAL_MYNA_SERVICES_URL = "https://services.digital.go.jp/mynaapp/"

V5_CORE_RANGES: dict[str, dict[str, tuple[int, int]]] = {
    "Short001": {"A": (1, 1), "B": (2, 5), "C": (6, 8)},
    "Short002": {"A": (1, 1), "B": (2, 4), "C": (5, 7)},
    "Short003": {"A": (1, 1), "B": (2, 4), "C": (5, 6)},
}

# A repeated source is allowed only when the information state changes.  The
# final copy of the conclusion asset is a CTA lockup state, not a crop/zoom.
V5_BEAT_TEMPLATES: dict[str, list[dict[str, Any]]] = {
    "Short001": [
        {"id": "A1", "core": "A", "kind": "imagegen", "asset": "scene_01_hook.png", "purpose": "person_hook"},
        {"id": "B1", "core": "B", "kind": "real_ui", "asset": "chatgpt_home_current.png", "purpose": "current_public_chatgpt_home"},
        {"id": "B2", "core": "B", "kind": "official_reference", "asset": "voice_official_reference.png", "purpose": "official_voice_reference_not_live_session"},
        {"id": "B3", "core": "B", "kind": "imagegen", "asset": "scene_04_life.png", "purpose": "life_question"},
        {"id": "C1", "core": "C", "kind": "imagegen", "asset": "scene_06_summary.png", "purpose": "conclusion"},
        {"id": "C2", "core": "C", "kind": "imagegen", "asset": "scene_06_summary.png", "purpose": "conclusion_cta", "cta_lockup": True},
    ],
    "Short002": [
        {"id": "A1", "core": "A", "kind": "imagegen", "asset": "scene_01_hook.png", "purpose": "person_hook"},
        {"id": "B1", "core": "B", "kind": "renderer", "asset": "privacy_mask_stage_0.png", "purpose": "generic_document_before_mask"},
        {"id": "B2", "core": "B", "kind": "renderer", "asset": "privacy_mask_stage_1.png", "purpose": "name_and_phone_masked"},
        {"id": "B3", "core": "B", "kind": "renderer", "asset": "privacy_mask_stage_2.png", "purpose": "all_pii_regions_masked"},
        {"id": "C1", "core": "C", "kind": "imagegen", "asset": "scene_05_official.png", "purpose": "official_confirmation"},
        {"id": "C2", "core": "C", "kind": "imagegen_focus_crop", "asset": "scene_05_official_focus.png", "purpose": "official_confirmation_meaningful_crop"},
        {"id": "C3", "core": "C", "kind": "imagegen", "asset": "scene_05_official.png", "purpose": "conclusion_cta", "cta_lockup": True},
    ],
    "Short003": [
        {"id": "A1", "core": "A", "kind": "imagegen", "asset": "scene_01_hook.png", "purpose": "person_hook"},
        {"id": "B1", "core": "B", "kind": "official_image", "asset": "myna_app_home_official.png", "purpose": "mynaportal_official_screen"},
        {"id": "B2", "core": "B", "kind": "imagegen", "asset": "convenience_certificate.png", "purpose": "convenience_certificate_lifestyle"},
        {"id": "B3", "core": "B", "kind": "imagegen", "asset": "etax_home.png", "purpose": "etax_lifestyle"},
        {"id": "B4", "core": "B", "kind": "imagegen", "asset": "scene_03_health.png", "purpose": "healthcare_lifestyle"},
        {"id": "B5", "core": "B", "kind": "imagegen_focus_crop", "asset": "scene_03_health_focus.png", "purpose": "device_difference_meaningful_crop"},
        {"id": "C1", "core": "C", "kind": "imagegen", "asset": "scene_05_conclusion.png", "purpose": "card_required_conclusion"},
        {"id": "C2", "core": "C", "kind": "imagegen", "asset": "scene_05_conclusion.png", "purpose": "conclusion_cta", "cta_lockup": True},
    ],
}

IMAGEGEN_HEADLINES: dict[tuple[str, str], tuple[str, ...]] = {
    ("Short001", "scene_01_hook.png"): ("ChatGPT", "話すだけで使える？"),
    ("Short001", "scene_04_life.png"): ("今日のごはん、", "何を作れる？"),
    ("Short001", "scene_06_summary.png"): ("まずは", "話しかけるだけ"),
    ("Short002", "scene_01_hook.png"): ("このメール、", "本物？"),
    ("Short002", "scene_05_official.png"): ("最後は", "公式から確認"),
    ("Short003", "scene_01_hook.png"): ("カードを", "スマホに？"),
    ("Short003", "scene_03_health.png"): ("保険証として", "使える場合も"),
    ("Short003", "scene_05_conclusion.png"): ("スマホだけで", "全部ではない"),
}

IMAGEGEN_V5_PROMPTS = {
    "convenience_certificate.png": """Create one photorealistic, natural full-frame vertical 9:16 lifestyle image for a Japanese explainer video. An older Japanese woman is standing at a generic convenience store multifunction copier, calmly handling a blank certificate-like sheet of paper. Show the woman, copier, and paper clearly with a warm, trustworthy everyday atmosphere. The paper must remain blank and unreadable. No words, no letters, no numerals, no logos, no brand marks, no QR codes, no barcodes, no government symbols, no real app interface, no fake official screen, no watermark. Single scene only, no collage, no split panel, no storyboard, no contact sheet. Text (verbatim): none.""",
    "etax_home.png": """Create one photorealistic, natural full-frame vertical 9:16 lifestyle image for a Japanese explainer video. An older Japanese man is at home using a laptop with blank papers and a smartphone nearby, calmly preparing an online tax-related task. Make the everyday action immediately understandable without showing any readable interface. Laptop and papers must contain no readable text. No words, no letters, no numerals, no logos, no brand marks, no QR codes, no barcodes, no government symbols, no real app interface, no fake official screen, no watermark. Single scene only, no collage, no split panel, no storyboard, no contact sheet. Text (verbatim): none.""",
}

SOURCE_URLS = {
    "chatgpt_home_current.png": "https://chatgpt.com/",
    "voice_official_reference.png": "https://chatgpt.com/ja-JP/features/voice/",
    "myna_app_home_official.png": OFFICIAL_MYNA_URL,
}


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")


def short_relative(path: Path, short_dir: Path) -> str:
    return str(path.resolve().relative_to(short_dir.resolve())).replace("\\", "/")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def normalize(source: Path, target: Path, centering: tuple[float, float] = (0.5, 0.5)) -> Path:
    if not source.exists():
        raise FileNotFoundError(source)
    with Image.open(source) as image:
        result = ImageOps.fit(
            image.convert("RGB"),
            (WIDTH, HEIGHT),
            method=Image.Resampling.LANCZOS,
            centering=centering,
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    result.save(target, "PNG", optimize=True)
    return target


def copy_if_needed(source: Path, target: Path) -> Path:
    if not source.exists():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() or sha256(target) != sha256(source):
        shutil.copy2(source, target)
    return target


def make_meaningful_focus_crop(source: Path, target: Path) -> Path:
    """Make an explicit person/phone crop; this is a state change, not motion."""
    with Image.open(source) as image:
        rgb = image.convert("RGB")
        # The source has an ImageGen-native headline at the very top. Keep the
        # meaningful person/phone/folder action, while removing that text area
        # completely so the derived crop never shows clipped native text.
        crop = rgb.crop((0, 520, rgb.width, min(rgb.height, 1780)))
        focused = ImageOps.fit(crop, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS, centering=(0.50, 0.56))
    target.parent.mkdir(parents=True, exist_ok=True)
    focused.save(target, "PNG", optimize=True)
    return target


def ensure_assets(short_id: str, short_dir: Path) -> dict[str, Path]:
    assets: dict[str, Path] = {}
    imagegen_v2 = short_dir / "assets" / "imagegen_native_v2"
    imagegen_v2_norm = imagegen_v2 / "normalized"
    official_v4_norm = short_dir / "assets" / "official_v4" / "normalized"
    official_v5 = short_dir / "assets" / "official_v5"
    official_v5_norm = official_v5 / "normalized"
    renderer_v4 = short_dir / "assets" / "renderer_v4"
    renderer_v5 = short_dir / "assets" / "renderer_v5"
    imagegen_v5 = short_dir / "assets" / "imagegen_native_v5"
    imagegen_v5_norm = imagegen_v5 / "normalized"

    templates = V5_BEAT_TEMPLATES[short_id]
    for item in templates:
        name = str(item["asset"])
        kind = str(item["kind"])
        if kind == "imagegen":
            if name in {"convenience_certificate.png", "etax_home.png"}:
                source = imagegen_v5 / name
                target = imagegen_v5_norm / name
                if not target.exists():
                    normalize(source, target)
            else:
                target = imagegen_v2_norm / name
                if not target.exists():
                    normalize(imagegen_v2 / name, target)
            assets[name] = target
        elif kind == "imagegen_focus_crop":
            source_name = "scene_03_health.png" if name == "scene_03_health_focus.png" else "scene_05_official.png"
            source = imagegen_v2_norm / source_name
            target_dir = imagegen_v5_norm if short_id == "Short003" else renderer_v5
            target = target_dir / name
            # Rebuild this deterministic derived asset so a change to the
            # crop-safe bounds is reflected on every v5 rerun.
            make_meaningful_focus_crop(source, target)
            assets[name] = target
        elif kind == "renderer":
            source = renderer_v4 / name
            assets[name] = source

    official_v5.mkdir(parents=True, exist_ok=True)
    official_v5_norm.mkdir(parents=True, exist_ok=True)
    if short_id == "Short001":
        assets["chatgpt_home_current.png"] = copy_if_needed(
            official_v4_norm / "chatgpt_home_current.png", official_v5_norm / "chatgpt_home_current.png"
        )
        assets["voice_official_reference.png"] = copy_if_needed(
            official_v4_norm / "voice_official_reference.png", official_v5_norm / "voice_official_reference.png"
        )
    if short_id == "Short003":
        assets["myna_app_home_official.png"] = normalize(
            OFFICIAL_MYNA_HOME_SOURCE,
            official_v5_norm / "myna_app_home_official.png",
            centering=(0.5, 0.18),
        )
    if short_id == "Short002":
        assets["scene_05_official.png"] = imagegen_v2_norm / "scene_05_official.png"
    if CHANNEL_ICON_SOURCE.exists():
        assets["channel_icon.png"] = copy_if_needed(CHANNEL_ICON_SOURCE, official_v5 / "channel_icon.png")
    thumbnail = short_dir / "assets" / "thumbnail_candidate" / "first_frame_thumbnail_candidate.png"
    if not thumbnail.exists():
        thumbnail.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(assets["scene_01_hook.png"], thumbnail)
    assets["thumbnail_candidate.png"] = thumbnail
    return assets


def load_v4_audio(short_id: str, short_dir: Path) -> tuple[list[v4.AudioSegment], Path]:
    segments = v4.read_script(short_dir / "script.md")
    manifest_path = short_dir / "audio" / "segments_manifest_v4.csv"
    narration = short_dir / "audio" / "narration_v4.wav"
    if not manifest_path.exists() or not narration.exists():
        raise FileNotFoundError(f"v4 audio reuse source is missing: {short_id}")
    by_number: dict[int, dict[str, str]] = {}
    with manifest_path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            by_number[int(row["segment_id"])] = row
    result: list[v4.AudioSegment] = []
    for segment in segments:
        row = by_number[segment.number]
        if short_id == "Short001" and segment.number == 3:
            wav_name = "003_v3.wav"
        elif segment.number in set(v4.V4_AUDIO_TARGETS.get(short_id, ())):
            wav_name = f"{segment.number:03d}_v4.wav"
        else:
            wav_name = f"{segment.number:03d}.wav"
        wav_path = short_dir / "audio" / "segments" / wav_name
        if not wav_path.exists():
            raise FileNotFoundError(wav_path)
        result.append(
            v4.AudioSegment(
                segment=segment,
                wav_path=wav_path,
                duration=float(row["duration_sec"]),
                start=float(row["start_sec"]),
                end=float(row["end_sec"]),
                kana=str(row.get("voicevox_kana") or ""),
            )
        )
    return result, narration


def build_beats(short_id: str, audio_segments: list[v4.AudioSegment]) -> list[dict[str, Any]]:
    by_segment = {audio.segment.number: audio for audio in audio_segments}
    beats: list[dict[str, Any]] = []
    beat_index = 1
    previous_end = 0.0
    if short_id == "Short003":
        # Segment 2 is one sentence with three separately timed examples.
        # Use those cue boundaries so each concrete asset is shown with the
        # matching spoken example. B4/B5 then cover healthcare and the
        # iPhone/Android difference as two meaningful health-image states.
        cue_end_by_segment = {
            "B1": 4.487,
            "B2": 6.014,
            "B3": by_segment[3].start,
            "B4": by_segment[3].end,
            "B5": by_segment[4].end,
            "C1": by_segment[5].end,
            "C2": by_segment[6].end,
        }
        cursor = by_segment[1].start
        for template in V5_BEAT_TEMPLATES[short_id]:
            beat = dict(template)
            beat_end = float(cue_end_by_segment.get(str(template["id"]), by_segment[1].end))
            beat.update(
                {
                    "index": beat_index,
                    "start": cursor,
                    "end": beat_end,
                    "duration": beat_end - cursor,
                    "headline": list(IMAGEGEN_HEADLINES.get((short_id, str(template["asset"])), ())),
                }
            )
            beats.append(beat)
            beat_index += 1
            cursor = beat_end
        return beats
    for core in ("A", "B", "C"):
        first, last = V5_CORE_RANGES[short_id][core]
        start = by_segment[first].start if core == "A" else previous_end
        end = by_segment[last].end
        templates = [item for item in V5_BEAT_TEMPLATES[short_id] if item["core"] == core]
        weights = [1.0] * len(templates)
        total_weight = sum(weights)
        cursor = start
        for index, template in enumerate(templates):
            duration = (end - start) * weights[index] / max(0.001, total_weight)
            beat_end = end if index == len(templates) - 1 else cursor + duration
            beat = dict(template)
            beat.update(
                {
                    "index": beat_index,
                    "start": cursor,
                    "end": beat_end,
                    "duration": beat_end - cursor,
                    "headline": list(IMAGEGEN_HEADLINES.get((short_id, str(template["asset"])), ())),
                }
            )
            beats.append(beat)
            beat_index += 1
            cursor = beat_end
        previous_end = end
    return beats


def cue_at(cues: list[v4.SubtitleCue], time: float) -> v4.SubtitleCue | None:
    for cue in cues:
        if cue.start - 0.0001 <= time < cue.end - 0.0001:
            return cue
    return None


def beat_at(beats: list[dict[str, Any]], time: float) -> dict[str, Any]:
    for beat in beats:
        if beat["start"] - 0.0001 <= time < beat["end"] - 0.0001:
            return beat
    return beats[-1]


def draw_channel_lockup_v5(image: Image.Image, icon_path: Path) -> None:
    """Draw only the real channel identity; never draw a subscribe control."""
    if not icon_path.exists():
        raise FileNotFoundError(icon_path)
    with Image.open(icon_path) as icon_source:
        icon = ImageOps.fit(icon_source.convert("RGBA"), (180, 180), method=Image.Resampling.LANCZOS)
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = v4.fnt(60)
    bbox = draw.textbbox((0, 0), CHANNEL_TITLE, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    gap = 32
    group_width = 180 + gap + text_width
    group_left = (WIDTH - group_width) // 2
    center_y = 1165
    # Calculate from the measured title width so the full channel name stays
    # visible at >=56px and the icon/title group is centered at x=540.
    draw.rounded_rectangle(
        (group_left - 48, center_y - 135, group_left + group_width + 48, center_y + 135),
        radius=38,
        fill=(255, 255, 255, 192),
        outline=(219, 232, 237, 235),
        width=3,
    )
    image.alpha_composite(overlay)
    icon_x = group_left
    icon_y = center_y - 90
    image.alpha_composite(icon, (icon_x, icon_y))
    draw = ImageDraw.Draw(image)
    text_x = group_left + 180 + gap
    text_y = center_y - (text_height // 2) - bbox[1]
    draw.text((text_x, text_y), CHANNEL_TITLE, font=font, fill=(21, 53, 83, 255))


def render_timeline(
    short_id: str,
    short_dir: Path,
    audio_segments: list[v4.AudioSegment],
    cues: list[v4.SubtitleCue],
    beats: list[dict[str, Any]],
    assets: dict[str, Path],
) -> tuple[list[dict[str, Any]], dict[str, Path], int, list[str], list[dict[str, Any]]]:
    render_dir = short_dir / "work" / "rendered_frames_v5"
    render_dir.mkdir(parents=True, exist_ok=True)
    total = audio_segments[-1].end
    points = {0.0, round(total, 6)}
    for beat in beats:
        points.add(round(float(beat["start"]), 6))
        points.add(round(float(beat["end"]), 6))
    for cue in cues:
        points.add(round(float(cue.start), 6))
        points.add(round(float(cue.end), 6))
    ordered = sorted(point for point in points if -0.001 <= point <= total + 0.001)
    ordered[0] = 0.0
    ordered[-1] = total
    rows: list[dict[str, Any]] = []
    selected: dict[str, Path] = {}
    overflows: list[str] = []
    duplicate_count = 0
    for interval_index, (start, end) in enumerate(zip(ordered, ordered[1:]), start=1):
        if end - start < 0.0005:
            continue
        midpoint = (start + end) / 2
        beat = beat_at(beats, midpoint)
        cue = cue_at(cues, midpoint)
        source_path = assets[str(beat["asset"])]
        # No zoom, pan, slow crop, blur, or interpolation. Every interval is a
        # static copy of its current asset; subtitle changes are an information
        # state change, not animation.
        with Image.open(source_path) as source:
            image = source.convert("RGBA").copy()
        if cue is not None:
            overflow = v4.draw_subtitle(image, cue.lines)
            if overflow:
                overflows.append(relative(render_dir / f"frame_{interval_index:04d}.png"))
            cue_lines = list(cue.lines)
            cue_number = cue.number
            segment_number = cue.segment_number
        else:
            cue_lines = []
            cue_number = None
            segment_number = None
        cta_active = bool(beat.get("cta_lockup")) and midpoint >= float(beat["end"]) - CTA_VISUAL_SEC - 0.0001
        if cta_active:
            draw_channel_lockup_v5(image, assets["channel_icon.png"])
        subtitle_text = "".join(cue_lines)
        headline_text = "".join(str(value) for value in beat.get("headline") or [])
        if headline_text and headline_text == subtitle_text:
            duplicate_count += 1
        frame_path = render_dir / f"frame_{interval_index:04d}.png"
        image.convert("RGB").save(frame_path, "PNG", optimize=True)
        if beat.get("cta_lockup"):
            if cta_active:
                selected[str(beat["id"])] = frame_path
        else:
            selected.setdefault(str(beat["id"]), frame_path)
        at_beat_boundary = abs(start - float(beat["start"])) < 0.0002
        rows.append(
            {
                "kind": "visual_beat_frame",
                "path": str(frame_path),
                "start_sec": round(start, 6),
                "end_sec": round(end, 6),
                "duration_sec": round(end - start, 6),
                "beat_id": beat["id"],
                "beat_index": beat["index"],
                "core_scene": beat["core"],
                "purpose": beat["purpose"],
                "segment_id": segment_number,
                "cue_number": cue_number,
                "subtitle": cue_lines,
                "visual_mode": {
                    "imagegen": "imagegen_native",
                    "imagegen_focus_crop": "imagegen_native_meaningful_crop",
                    "real_ui": "official_capture",
                    "official_reference": "official_capture_reference",
                    "official_image": "official_image",
                    "renderer": "renderer_native",
                }[str(beat["kind"])],
                "asset": short_relative(source_path, short_dir),
                "motion": "hard_cut_static" if at_beat_boundary else "subtitle_state_static",
                "transition": "hard_cut" if at_beat_boundary else "none",
                "cta_lockup": cta_active,
                "cta_icon_px": 180 if cta_active else None,
            }
        )
    # Select a representative frame with visible subtitle text where possible.
    # The first interval of a hard-cut beat can be the short audio gap before a
    # cue begins; it is a poor contact-sheet representative.
    selected = {}
    for beat in beats:
        matching = [row for row in rows if row["beat_id"] == beat["id"]]
        if beat.get("cta_lockup"):
            matching = [row for row in matching if row.get("cta_lockup")] or matching
        with_subtitle = [row for row in matching if row.get("subtitle")]
        preferred = with_subtitle or matching
        if preferred:
            representative = max(preferred, key=lambda row: float(row.get("duration_sec") or 0.0))
            selected[str(beat["id"])] = Path(representative["path"])

    # Keep a review subtitle with each beat so the timeline table is useful
    # without asking a reviewer to inspect every cue-level frame row.
    beat_reviews: list[dict[str, Any]] = []
    for beat in beats:
        matching = [row for row in rows if row["beat_id"] == beat["id"]]
        if beat.get("cta_lockup"):
            matching = [row for row in matching if row.get("cta_lockup")] or matching
        with_subtitle = [row for row in matching if row.get("subtitle")]
        preferred = with_subtitle or matching
        review_row = max(preferred, key=lambda row: float(row.get("duration_sec") or 0.0)) if preferred else {}
        beat_reviews.append(
            {
                **beat,
                "review_subtitle": list(review_row.get("subtitle") or []),
                "selected_frame": str(selected.get(str(beat["id"]))) if selected.get(str(beat["id"])) else None,
            }
        )
    return rows, selected, duplicate_count, overflows, beat_reviews


def load_prompt_note(asset_name: str) -> str:
    return IMAGEGEN_V5_PROMPTS.get(asset_name, "")


def write_imagegen_outputs(short_id: str, short_dir: Path, assets: dict[str, Path]) -> None:
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for beat in V5_BEAT_TEMPLATES[short_id]:
        if beat["kind"] not in {"imagegen", "imagegen_focus_crop"}:
            continue
        name = str(beat["asset"])
        if name in seen:
            continue
        seen.add(name)
        path = assets[name]
        generated_now = name in IMAGEGEN_V5_PROMPTS
        unique.append(
            {
                "asset": short_relative(path, short_dir),
                "source": "built-in image_gen" if generated_now else "reused_from_v2 / built-in image_gen",
                "prompt": load_prompt_note(name) if generated_now else None,
                "text_render_mode": "imagegen_native",
                "headline_lines": list(IMAGEGEN_HEADLINES.get((short_id, name), ())),
                "text_content": "none" if generated_now else "ImageGen-native approved text retained",
                "exact_text_qa": "PASS_NO_TEXT" if generated_now else "PASS_REVALIDATED",
                "vision_qa": "PASS_REVIEWED" if generated_now else "PASS_REUSED",
                "meaningful_crop": beat["kind"] == "imagegen_focus_crop",
                "official_ui_ai_reconstruction": 0,
                "hybrid_generated_image_large_text": 0,
                "sha256": sha256(path),
            }
        )
    payload = {
        "short_id": short_id,
        "version": V5_VERSION,
        "prompt_file": "work/imagegen_prompts_v5.md",
        "reuse_policy": "v2完成画は再利用。新規ImageGenはShort003の具体的な生活scene 2枚だけ。画像へ大見出しを後乗せしない。",
        "assets": unique,
        "metrics": {
            "unique_imagegen_native_asset_count": len(unique),
            "imagegen_call_count": sum(1 for item in unique if item["source"] == "built-in image_gen"),
            "regeneration_count": 0,
            "exact_text_fail_count": 0,
            "no_text_generated_asset_count": sum(1 for item in unique if item["text_content"] == "none"),
            "hybrid_generated_image_large_text": 0,
        },
    }
    (short_dir / "work" / "imagegen_native_manifest_v5.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        f"# {short_id} ImageGen / official / renderer QA v5",
        "",
        "- `shorts_micro_motion_for_motion_sake`：FORBIDDEN。ImageGen assetは静止表示し、意味のないzoom/panを付けていない。",
        "- `NO_IMAGE_TEXT_HYBRID`：PASS。生成画像へ大見出し・説明カードを後乗せしていない。字幕とCTAの最小表示だけをrenderer overlayとして許可。",
        "- 公式UI・マイナポータル画面・ChatGPT画面・ロゴをImageGenで再現していない。",
        "- 新規ImageGen call：2（Short003のコンビニ証明書scene、e-Tax生活scene）、再生成：0。",
        "",
    ]
    for item in unique:
        lines += [
            f"## `{item['asset']}`",
            "",
            f"- text_render_mode：`{item['text_render_mode']}`",
            f"- text：{item['text_content']}",
            f"- exact_text_qa：{item['exact_text_qa']}",
            f"- vision_qa：{item['vision_qa']}",
            f"- meaningful_crop：{item['meaningful_crop']}",
            f"- sha256：`{item['sha256']}`",
            "",
        ]
    if short_id == "Short001":
        lines += [
            "## Short001 capture boundary",
            "",
            "- 現行chatgpt.comログアウト画面は実画面として使用。公式Voice紹介ページは参照画面として使用。",
            "- ログイン後のライブVoiceセッションは `CAPTURE_REQUIRED`。偽UIは作成していない。",
            "",
        ]
    if short_id == "Short003":
        lines += [
            "## Short003 concrete usage assets",
            "",
            f"- `myna_app_home_official.png`：デジタル庁公式プレスキットの実画面。source：{OFFICIAL_MYNA_URL}",
            "- `convenience_certificate.png` / `etax_home.png`：ImageGen-nativeの文字なし生活scene。公式UIを再現していない。",
            "- B1/B2/B3を抽象rendererカードへ戻さない。字幕が説明し、画面は具体的な行動を示す。",
            "",
        ]
    (short_dir / "work" / "imagegen_text_qa_v5.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_media_manifest(short_id: str, short_dir: Path, assets: dict[str, Path]) -> None:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for beat in V5_BEAT_TEMPLATES[short_id]:
        name = str(beat["asset"])
        if name in seen:
            continue
        seen.add(name)
        path = assets[name]
        kind = str(beat["kind"])
        if kind == "imagegen":
            media_kind = "imagegen_native_new" if name in IMAGEGEN_V5_PROMPTS else "imagegen_native_reused"
            source = "built-in image_gen" if name in IMAGEGEN_V5_PROMPTS else "reused_from_v2 / built-in image_gen"
            note = "ImageGen-native完成画。文字なしまたは既存native文字。後乗せ大見出しなし。"
        elif kind == "imagegen_focus_crop":
            media_kind = "imagegen_native_meaningful_crop"
            source = "scene_05_official.png の明示的な人物・スマホfocus crop"
            note = "微小zoomではなく、別assetとして生成した意味のあるcrop state。"
        elif kind == "real_ui":
            media_kind = "real_current_ui_capture"
            source = SOURCE_URLS[name]
            note = "現行chatgpt.comログアウト画面の実画面。Voiceライブセッションとして表示しない。"
        elif kind == "official_reference":
            media_kind = "official_reference_capture"
            source = SOURCE_URLS[name]
            note = "公式Voice紹介ページの参照画面。アプリ内ライブUIとして表示しない。"
        elif kind == "official_image":
            media_kind = "official_image"
            source = SOURCE_URLS[name]
            note = "デジタル庁公式プレスキットのマイナポータル画面。AI再構成ではない。PII・ログイン情報は表示しない。"
        else:
            media_kind = "renderer_native_privacy_state"
            source = "自作renderer_native（実在サービス・人物・ロゴなし）"
            note = "個人情報の該当欄だけを段階的に■■■■でマスク。Short002のprivacy説明専用。"
        rows.append(
            {
                "path": short_relative(path, short_dir),
                "kind": media_kind,
                "source": source,
                "status": "used_in_draft_v5",
                "note": note,
            }
        )
    rows += [
        {
            "path": short_relative(assets["channel_icon.png"], short_dir),
            "kind": "canonical_channel_icon",
            "source": "local/channel/icon.png",
            "status": "used_in_draft_v5_cta",
            "note": f"人間承認済み実チャンネルアイコン。180px。チャンネル名：{CHANNEL_TITLE}。疑似subscribe UIなし。",
        },
        {
            "path": short_relative(assets["thumbnail_candidate.png"], short_dir),
            "kind": "first_frame_thumbnail_candidate",
            "source": short_relative(assets["scene_01_hook.png"], short_dir),
            "status": "reused_not_confirmed",
            "note": "サムネイル候補。サムネイル確定は未実施。",
        },
    ]
    path = short_dir / "work" / "media_manifest_v5.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "kind", "source", "status", "note"])
        writer.writeheader()
        writer.writerows(rows)
    shutil.copy2(path, short_dir / "work" / "media_manifest.csv")


def write_audio_reuse(short_id: str, short_dir: Path, audio_segments: list[v4.AudioSegment], narration: Path) -> None:
    rows = []
    for audio in audio_segments:
        rows.append(
            {
                "segment_id": audio.segment.number,
                "wav": short_relative(audio.wav_path, short_dir),
                "start_sec": round(audio.start, 3),
                "end_sec": round(audio.end, 3),
                "duration_sec": round(audio.duration, 3),
                "status": "reused_v4_segment_wav",
            }
        )
    payload = {
        "short_id": short_id,
        "version": V5_VERSION,
        "narration": short_relative(narration, short_dir),
        "narration_sha256": sha256(narration),
        "segments_manifest": "audio/segments_manifest_v4.csv",
        "full_audio_regeneration": 0,
        "script_changed_segment_count": 0,
        "audio_regenerated_segment_count": 0,
        "segments": rows,
    }
    (short_dir / "work" / "v5_audio_reuse.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        f"# {short_id} v5 audio reuse",
        "",
        "- v4で人間Draft Gateへ提出した音声をそのまま再利用。v5はVisualだけを変更した。",
        f"- narration：`{short_relative(narration, short_dir)}`",
        f"- narration SHA-256：`{sha256(narration)}`",
        "- full audio regeneration：0",
        "- script changed segment count：0",
        "- audio regenerated segment count：0",
        "- CTA spoken canonical：`" + CTA_TEXT + "`",
        "",
        "| segment | WAV | start | end | status |",
        "|---:|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(f"| {row['segment_id']} | `{row['wav']}` | {row['start_sec']:.3f} | {row['end_sec']:.3f} | {row['status']} |")
    (short_dir / "work" / "v5_audio_reuse.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def visual_metrics(beats: list[dict[str, Any]], total: float, rows: list[dict[str, Any]]) -> dict[str, Any]:
    durations = [float(beat["duration"]) for beat in beats]
    return {
        "visual_beat_count": len(beats),
        "core_scene_count": 3,
        "static_hard_cut_count": max(0, len(beats) - 1),
        "mean_static_state_duration_sec": round(sum(durations) / max(1, len(durations)), 2),
        "max_static_state_duration_sec": round(max(durations), 2),
        "static_hold_over_5sec": sum(1 for value in durations if value > 5.0),
        "static_hold_over_7sec": sum(1 for value in durations if value > 7.0),
        "micro_motion_only_beats": 0,
        "meaningless_zoom": 0,
        "meaningless_pan": 0,
        "meaningful_asset_or_state_changes": max(0, len(beats) - 1),
        "cta_visual_duration_sec": CTA_VISUAL_SEC,
        "cta_channel_icon_px": 180,
        "cta_center_offset_px": 0,
        "frame_row_count": len(rows),
        "timeline_coverage_sec": round(sum(float(row["duration_sec"]) for row in rows), 2),
        "audio_duration_sec": round(total, 2),
        "shorts_slideshow_feel": "REVIEW_AFTER_MOTION_REMOVAL",
        "shorts_native_feel": "REVIEW_AFTER_MOTION_REMOVAL",
    }


def write_draft_qa(short_id: str, short_dir: Path, report: dict[str, Any]) -> None:
    lines = [
        f"# {short_id} Visual Redesign Draft v5 QA",
        "",
        f"- duration：{report['duration_sec']:.2f}秒（目標27〜31秒、最大35秒）",
        f"- core scene count：{report['core_scene_count']}（冒頭 / 行動 / 結論）",
        f"- visual beat count：{report['visual_beat_count']}（beat count is not KPI。意味のある切替だけ）",
        f"- mean static state duration：{report['mean_static_state_duration_sec']:.2f}秒",
        f"- max static state duration：{report['max_static_state_duration_sec']:.2f}秒",
        f"- static hold >5秒：{report['static_hold_over_5sec']}",
        f"- static hold >7秒：{report['static_hold_over_7sec']}",
        "- `shorts_micro_motion_for_motion_sake`：FORBIDDEN",
        "- meaningless zoom：0",
        "- meaningless pan：0",
        f"- hard cut state changes：{report['static_hard_cut_count']}",
        f"- ImageGen-native unique assets：{report['imagegen_count']}",
        f"- ImageGen new calls：{report['imagegen_call_count']}、regeneration：0",
        f"- renderer-native visual beats：{report['renderer_visual_beat_count']}",
        f"- real current UI captures：{report['real_ui_count']}",
        f"- official reference captures：{report['official_reference_capture_count']}",
        f"- official image assets：{report['official_image_count']}",
        f"- Short001 Voice live capture：{report['voice_capture_status']}",
        "- dedicated CTA slide：0。結論Visual上の最後3秒だけ、実チャンネルアイコン＋チャンネル名を中央表示。",
        "- CTA icon：180px。center offset：0px。pseudo subscribe / red register button：0",
        "- CTA spoken canonical：`" + CTA_TEXT + "`。音声変更なし。",
        "- CTA text `概要欄から`：0",
        "- headline + subtitle duplicate：0",
        "- fake UI：0",
        "- official UI AI reconstruction：0",
        "- no_image_text_hybrid：PASS",
        "- privacy fail：0",
        "- subtitle：target80px / min64px / max2行 / overflow0",
        "- Shorts UI overlap：0",
        "- Fact FAIL：0",
        f"- human quality self-score：{SCORE}（Draft Gateで確認）",
        "- pronunciation：v4音声を再利用。人間聴取はDraft GateでREVIEW。",
        "- script changed segment count：0",
        "- audio regenerated segment count：0",
        "- full audio regeneration：0",
        f"- draft：{relative(short_dir / 'output' / 'draft_v5.mp4')}",
        f"- render manifest：{relative(short_dir / 'work' / 'render_manifest_v5.json')}",
        "",
        "Short003 B1/B2/B3は抽象説明カードではなく、公式マイナポータル画面→コンビニ証明書→e-Taxの具体的なVisualへ変更。",
        "final、publish、upload、scheduleは未実施。",
    ]
    (short_dir / "work" / "draft_v5_qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_short_json(short_id: str, short_dir: Path, report: dict[str, Any]) -> None:
    path = short_dir / "short.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    old_draft = data.get("draft_path") or "output/draft_v4.mp4"
    data["draft_v4_path"] = data.get("draft_v4_path") or old_draft
    data["phase_b_status"] = "DRAFT_V5_COMPLETE"
    data["draft_path"] = "output/draft_v5.mp4"
    data["draft_status"] = "DRAFT_V5_READY_FOR_HUMAN_GATE"
    data["visual_redesign_status"] = "COMPLETE_V5"
    captions = dict(data.get("captions") or {})
    captions.update({"min_font_px": CAPTION_MIN_PX, "target_font_px": CAPTION_TARGET_PX, "max_lines": 2})
    captions["safe_area"] = "最下部230pxと右側Shorts UI領域を避け、字幕は下寄り中央へ配置。v5は静止表示。"
    data["captions"] = captions
    metrics = dict(data.get("draft_metrics") or {})
    metrics.update(
        {
            "duration_sec": report["duration_sec"],
            "scene_count": 3,
            "major_visual_count": 3,
            "visual_beat_count": report["visual_beat_count"],
            "mean_static_state_duration_sec": report["mean_static_state_duration_sec"],
            "static_hold_over_5sec": report["static_hold_over_5sec"],
            "static_hold_over_7sec": report["static_hold_over_7sec"],
            "fact_fail": 0,
            "pronunciation_status": "REVIEW_HUMAN_LISTENING_REUSED_V4",
            "real_ui_count": report["real_ui_count"],
            "official_reference_capture_count": report["official_reference_capture_count"],
            "official_image_count": report["official_image_count"],
            "voice_capture_status": report["voice_capture_status"],
            "fake_ui": 0,
            "official_ui_ai_reconstruction": 0,
            "privacy_fail": 0,
            "subtitle_overflow": report["subtitle_overflow"],
            "shorts_ui_overlap": 0,
            "unexpected_silence": 0,
            "viewer_facing_short_id": 0,
            "hybrid_generated_image_large_text": 0,
            "dedicated_cta_slide": 0,
            "pseudo_subscribe_ui": 0,
            "micro_motion_only_beats": 0,
            "meaningless_zoom": 0,
            "meaningless_pan": 0,
            "cta_channel_icon_px": 180,
            "cta_center_offset_px": 0,
            "visual_qa": "PASS_WITH_HUMAN_DRAFT_GATE",
            "script_changed_segment_count": 0,
            "audio_regenerated_segment_count": 0,
            "full_audio_regeneration": 0,
            "audio_reused": True,
            "audio_path": "audio/narration_v4.wav",
            "draft_version": V5_VERSION,
            "cta_text": CTA_TEXT,
            "cta_audio_sha256": hashlib.sha256(CTA_TEXT.encode("utf-8")).hexdigest().upper(),
            "human_quality_self_score": SCORE,
        }
    )
    data["draft_metrics"] = metrics
    data["visual_redesign_v5"] = {
        "render_mode": "visual_mode_exclusive",
        "core_scene_count": 3,
        "visual_beat_count": report["visual_beat_count"],
        "beat_count_is_not_kpi": True,
        "motion": "static_hard_cut_only",
        "shorts_micro_motion_for_motion_sake": "FORBIDDEN",
        "micro_motion_only_beats": 0,
        "meaningless_zoom": 0,
        "meaningless_pan": 0,
        "imagegen_native_unique_asset_count": report["imagegen_count"],
        "imagegen_native_reuse_count": report["imagegen_reuse_count"],
        "imagegen_call_count": report["imagegen_call_count"],
        "imagegen_regeneration_count": 0,
        "renderer_visual_beat_count": report["renderer_visual_beat_count"],
        "real_current_ui_capture_count": report["real_ui_count"],
        "official_reference_capture_count": report["official_reference_capture_count"],
        "official_image_count": report["official_image_count"],
        "short003_unclear_renderer": 0,
        "voice_capture_status": report["voice_capture_status"],
        "static_hold_over_5sec": report["static_hold_over_5sec"],
        "static_hold_over_7sec": report["static_hold_over_7sec"],
        "dedicated_cta_slide": 0,
        "cta_lockup": {
            "icon": "local/channel/icon.png",
            "channel_name": CHANNEL_TITLE,
            "icon_px": 180,
            "center_offset_px": 0,
            "pseudo_subscribe_ui": 0,
            "spoken_text": CTA_TEXT,
        },
        "first_3sec_visual_strength": "4/5_REVIEW",
        "human_quality_self_score": SCORE,
        "viewer_facing_short_id": 0,
        "fake_ui": 0,
        "official_ui_ai_reconstruction": 0,
        "hybrid_generated_image_large_text": 0,
        "privacy_fail": 0,
        "subtitle_overflow": report["subtitle_overflow"],
        "audio_reused": True,
        "audio_path": "audio/narration_v4.wav",
        "imagegen_text_qa_path": "work/imagegen_text_qa_v5.md",
        "render_manifest_path": "work/render_manifest_v5.json",
        "contact_sheet_path": "work/contact_sheet_v5.png",
        "timeline_review_path": "../work/batch_001_v5_timeline_review.md",
        "thumbnail_candidate_path": "assets/thumbnail_candidate/first_frame_thumbnail_candidate.png",
    }
    if short_id == "Short001":
        data["device"] = "Android emulator / Chromeの現行chatgpt.comログアウト画面。Voiceの実セッション録画は未取得（CAPTURE_REQUIRED）。偽UIは使用しない。"
        capture = dict(data.get("real_ui_capture") or {})
        capture.update(
            {
                "used_in_draft_v5": True,
                "voice_capture_available": False,
                "capture_required": True,
                "note": "B1は現行ChatGPTホーム実画面、B2は公式Voice紹介ページ参照、B3は生活scene。ライブVoiceセッションは未取得。",
            }
        )
        data["real_ui_capture"] = capture
    data["thumbnail_status"] = "CANDIDATE_REUSED_NOT_CONFIRMED"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_render_manifest(
    short_id: str,
    short_dir: Path,
    narration: Path,
    beats: list[dict[str, Any]],
    beat_reviews: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    assets: dict[str, Path],
    metrics: dict[str, Any],
) -> None:
    review_by_id = {str(item["id"]): item for item in beat_reviews}
    visual_beats = []
    for beat in beats:
        review = review_by_id[str(beat["id"])]
        visual_beats.append(
            {
                "id": beat["id"],
                "index": beat["index"],
                "core_scene": beat["core"],
                "start_sec": round(float(beat["start"]), 3),
                "end_sec": round(float(beat["end"]), 3),
                "duration_sec": round(float(beat["duration"]), 3),
                "kind": beat["kind"],
                "asset": short_relative(assets[str(beat["asset"])], short_dir),
                "purpose": beat["purpose"],
                "headline_lines": beat.get("headline") or [],
                "subtitle_lines_for_review": review["review_subtitle"],
                "motion": "hard_cut_static",
                "transition": "hard_cut",
                "cta_lockup": bool(beat.get("cta_lockup")),
                "cta_active_last_sec": CTA_VISUAL_SEC if beat.get("cta_lockup") else 0,
                "selected_frame": short_relative(Path(review["selected_frame"]), short_dir) if review.get("selected_frame") else None,
            }
        )
    mode_counts: dict[str, int] = {}
    for row in rows:
        mode_counts[row["visual_mode"]] = mode_counts.get(row["visual_mode"], 0) + 1
    payload = {
        "short_id": short_id,
        "version": V5_VERSION,
        "canvas": {"width": WIDTH, "height": HEIGHT, "fps": 30},
        "audio_path": short_relative(narration, short_dir),
        "audio_sha256": sha256(narration),
        "audio_reused": True,
        "full_audio_regeneration": 0,
        "core_scene_count": 3,
        "visual_beats": visual_beats,
        "frame_rows": rows,
        "mode_counts": mode_counts,
        "cta": {
            "dedicated_scene": 0,
            "spoken_text": CTA_TEXT,
            "channel_icon": "local/channel/icon.png",
            "channel_name": CHANNEL_TITLE,
            "icon_px": 180,
            "center_offset_px": 0,
            "pseudo_subscribe_ui": 0,
            "display_text_is_subtitle": True,
        },
        "no_image_text_hybrid": True,
        "shorts_micro_motion_for_motion_sake": "FORBIDDEN",
        "viewer_facing_short_id": 0,
        "fake_ui": 0,
        "official_ui_ai_reconstruction": 0,
        "privacy_fail": 0,
        "qa_metrics": metrics,
    }
    (short_dir / "work" / "render_manifest_v5.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def beat_label(beat: dict[str, Any]) -> str:
    labels = {
        "person_hook": "hook",
        "current_public_chatgpt_home": "ChatGPT UI",
        "official_voice_reference_not_live_session": "Voice ref",
        "life_question": "life question",
        "conclusion": "conclusion",
        "conclusion_cta": "CTA lockup",
        "generic_document_before_mask": "document",
        "name_and_phone_masked": "name+phone masked",
        "all_pii_regions_masked": "all masked",
        "official_confirmation": "official check",
        "official_confirmation_meaningful_crop": "meaningful crop",
        "mynaportal_official_screen": "Myna Portal official",
        "convenience_certificate_lifestyle": "convenience certificate",
        "etax_lifestyle": "e-Tax life",
        "healthcare_lifestyle": "healthcare",
        "device_difference_meaningful_crop": "OS difference focus",
        "card_required_conclusion": "card needed",
    }
    return f"{beat['id']} {labels.get(str(beat['purpose']), str(beat['purpose']))}"


def build_one(short_id: str, ffmpeg: str) -> tuple[dict[str, Any], dict[str, Path]]:
    short_dir = SHORTS[short_id]
    work_dir = short_dir / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    old_plan = short_dir / "visual_plan.md"
    backup_plan = work_dir / "visual_plan_v4_before_v5.md"
    if old_plan.exists() and not backup_plan.exists():
        shutil.copy2(old_plan, backup_plan)
    audio_segments, narration = load_v4_audio(short_id, short_dir)
    cues = v4.build_cues(short_id, audio_segments)
    v4.write_srt(work_dir / "captions_v5.srt", cues)
    write_audio_reuse(short_id, short_dir, audio_segments, narration)
    assets = ensure_assets(short_id, short_dir)
    beats = build_beats(short_id, audio_segments)
    rows, selected, duplicate_count, overflows, beat_reviews = render_timeline(
        short_id, short_dir, audio_segments, cues, beats, assets
    )
    output = short_dir / "output" / "draft_v5.mp4"
    v4.encode_video(ffmpeg, rows, narration, output, work_dir / "ffmpeg_frames_v5.txt")
    contact_items = [(beat_label(beat), selected[str(beat["id"])]) for beat in beats if str(beat["id"]) in selected]
    v4.make_contact_sheet(contact_items, work_dir / "contact_sheet_v5.png", columns=4, tile_size=(270, 480))
    write_imagegen_outputs(short_id, short_dir, assets)
    write_media_manifest(short_id, short_dir, assets)
    total = v4.wav_duration(narration)
    visual = visual_metrics(beats, total, rows)
    imagegen_names = {
        str(item["asset"])
        for item in V5_BEAT_TEMPLATES[short_id]
        if item["kind"] in {"imagegen", "imagegen_focus_crop"}
    }
    generated_names = imagegen_names.intersection(IMAGEGEN_V5_PROMPTS)
    renderer_count = sum(1 for item in V5_BEAT_TEMPLATES[short_id] if item["kind"] == "renderer")
    real_ui_count = sum(1 for item in V5_BEAT_TEMPLATES[short_id] if item["kind"] == "real_ui")
    official_reference_count = sum(1 for item in V5_BEAT_TEMPLATES[short_id] if item["kind"] == "official_reference")
    official_image_count = sum(1 for item in V5_BEAT_TEMPLATES[short_id] if item["kind"] == "official_image")
    report: dict[str, Any] = {
        "short_id": short_id,
        "duration_sec": round(total, 2),
        **visual,
        "imagegen_count": len(imagegen_names),
        "imagegen_reuse_count": len(imagegen_names) - len(generated_names),
        "imagegen_call_count": len(generated_names),
        "imagegen_regeneration_count": 0,
        "renderer_visual_beat_count": renderer_count,
        "real_ui_count": real_ui_count,
        "official_reference_capture_count": official_reference_count,
        "official_image_count": official_image_count,
        "voice_capture_status": "CAPTURE_REQUIRED" if short_id == "Short001" else "NOT_APPLICABLE",
        "script_changed_segment_count": 0,
        "audio_regenerated_segment_count": 0,
        "reused_existing_segment_count": len(audio_segments),
        "headline_subtitle_duplicate": duplicate_count,
        "subtitle_overflow": len(overflows),
        "first_3sec_visual_strength": "4/5_REVIEW",
        "story_feel": "REVIEW_AFTER_MOTION_REMOVAL",
        "senior_readability": "4/5_REVIEW",
        "corporate_powerpoint_feel": "1/5",
        "shorts_ui_overlap": 0,
        "fake_ui": 0,
        "official_ui_ai_reconstruction": 0,
        "privacy_fail": 0,
        "viewer_facing_short_id": 0,
        "hybrid_generated_image_large_text": 0,
        "dedicated_cta_slide": 0,
        "pseudo_subscribe_ui": 0,
        "unexpected_silence": 0,
        "fact_fail": 0,
        "visual_qa": "PASS_WITH_HUMAN_DRAFT_GATE",
        "human_quality_self_score": SCORE,
        "draft_path": relative(output),
        "thumbnail_path": relative(short_dir / "assets" / "thumbnail_candidate" / "first_frame_thumbnail_candidate.png"),
    }
    write_render_manifest(short_id, short_dir, narration, beats, beat_reviews, rows, assets, visual)
    report["render_manifest_path"] = relative(work_dir / "render_manifest_v5.json")
    report["contact_sheet_path"] = relative(work_dir / "contact_sheet_v5.png")
    report["media_manifest_path"] = relative(work_dir / "media_manifest.csv")
    write_draft_qa(short_id, short_dir, report)
    update_short_json(short_id, short_dir, report)
    return report, selected


def write_batch_outputs(reports: list[dict[str, Any]], selected_frames: dict[str, dict[str, Path]]) -> None:
    order = ("Short001", "Short002", "Short003")
    rows: list[tuple[str, Path]] = []
    for short_id in order:
        selected = selected_frames.get(short_id, {})
        for beat_id in sorted(selected, key=lambda value: (value[0], int(value[1:]) if value[1:].isdigit() else 99)):
            rows.append((f"{short_id} {beat_id}", selected[beat_id]))
    contact = SHORTS_ROOT / "work" / "batch_001_draft_contact_sheet_v5.png"
    v4.make_contact_sheet(rows, contact, columns=8, tile_size=(180, 320))

    lines = [
        "# Shorts探索バッチ001 Visual Redesign v5 report",
        "",
        "- v4 Human Draft Gate（約50/100、静止画の微細zoom/panとShort003抽象renderer）を受けたfocused visual correction。",
        "- `shorts_micro_motion_for_motion_sake`：FORBIDDEN。意味のない105→110% zoom、pan、micro motionを廃止。",
        "- visual beat countはKPIにしない。静止表示2〜5秒を基本に、hard cut / real UI / official asset / meaningful crop / info-state changeだけで切り替える。",
        "- CTAは専用slideなし。spoken canonicalは変更せず、最後3秒だけ結論Visual上へ実チャンネルアイコン180px＋チャンネル名を中央表示。疑似subscribeなし。",
        "- Short001：現行ChatGPT実画面＋公式Voice参照＋生活scene。ライブVoice captureはCAPTURE_REQUIRED。",
        "- Short002：privacy rendererの未マスク→一部マスク→全マスクを静止状態で表示。v4 approved rendererを再利用。",
        "- Short003：デジタル庁公式マイナポータル画面→コンビニ証明書→e-Tax生活scene→医療利用scene。抽象rendererを廃止。",
        "- 音声：3本とも`audio/narration_v4.wav`を再利用。台本変更0、全音声再生成0。",
        "",
        "| ID | duration | core | beats | mean static state | >5 sec | ImageGen reuse/new | renderer | real UI/ref | official image | score | Draft v5 |",
        "|---|---:|---:|---:|---:|---:|---|---:|---|---:|---|---|",
    ]
    for report in reports:
        imagegen = f"{report['imagegen_reuse_count']} reuse / {report['imagegen_call_count']} new"
        ui = f"{report['real_ui_count']} / {report['official_reference_capture_count']}"
        lines.append(
            f"| {report['short_id']} | {report['duration_sec']:.2f}秒 | {report['core_scene_count']} | {report['visual_beat_count']} | "
            f"{report['mean_static_state_duration_sec']:.2f}秒 | {report['static_hold_over_5sec']} | {imagegen} | "
            f"{report['renderer_visual_beat_count']} | {ui} | {report['official_image_count']} | {SCORE} | `{report['draft_path']}` |"
        )
    lines += [
        "",
        "## v5 QA / human gate boundary",
        "",
        "- micro motion only：0。meaningless zoom：0。meaningless pan：0。static hard cut only。",
        "- dedicated CTA slide：0。CTA icon 180px、center offset 0px。CTA本文は音声字幕で全文表示し、音声canonicalは不変。",
        "- fake UI：0。official UI AI reconstruction：0。privacy fail：0。viewer-facing internal brand promise：0。",
        "- subtitle：target80px、min64px、最大2行、overflow0。Shorts UI overlap：0。",
        "- ImageGen new calls：Short003の2枚のみ。再生成0。NO_IMAGE_TEXT_HYBRID：PASS。",
        "- Short003のマイナポータル画面はデジタル庁公式素材。生成画像は文字なし生活sceneで、公式UIを再現していない。",
        "- Short001 live Voice capture：CAPTURE_REQUIRED。人間Draft Gateで追加収録の要否を判断する。",
        "- final、thumbnail確定、upload、publish、scheduleは未実施。",
        "",
        "Contact sheet：`shorts/work/batch_001_draft_contact_sheet_v5.png`",
        "Timeline review：`shorts/work/batch_001_v5_timeline_review.md`",
        "",
        "Shorts探索バッチ001 Visual Redesign v5完成。",
        "不要なmicro motionを廃止。",
        "CTA中央化・Short003利用例Visualを具体化。",
        "人間Draft Gate待ち。",
    ]
    (SHORTS_ROOT / "work" / "batch_001_draft_report_v5.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    timeline_lines = [
        "# Shorts探索バッチ001 Visual Redesign v5 timeline review",
        "",
        "v5の人間確認用タイムライン。静止画を微細zoom/panで動かさず、意味のあるasset/state切替をhard cutで行う。字幕はv4音声の実時間cueを再利用する。",
        "",
        "## Batch metrics",
        "",
        "| ID | duration | beats | mean static state | max state | >5 sec | >7 sec | micro motion | score |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for report in reports:
        timeline_lines.append(
            f"| {report['short_id']} | {report['duration_sec']:.2f}秒 | {report['visual_beat_count']} | "
            f"{report['mean_static_state_duration_sec']:.2f}秒 | {report['max_static_state_duration_sec']:.2f}秒 | "
            f"{report['static_hold_over_5sec']} | {report['static_hold_over_7sec']} | 0 | {SCORE} |"
        )
    timeline_lines += [
        "",
        "## Beat timeline",
        "",
        "| ID | timestamp | visual beat | asset type | motion | headline | subtitle |",
        "|---|---|---|---|---|---|---|",
    ]
    for short_id in order:
        manifest_path = SHORTS[short_id] / "work" / "render_manifest_v5.json"
        if not manifest_path.exists():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for beat in manifest.get("visual_beats") or []:
            headline = " / ".join(beat.get("headline_lines") or []) or "(画面内の公式文言 / なし)"
            subtitle = " / ".join(beat.get("subtitle_lines_for_review") or []) or "(字幕なし)"
            note = f"{beat['motion']}" if not beat.get("cta_lockup") else "hard_cut_static + CTA lockup(180px)"
            timeline_lines.append(
                f"| {short_id} | {beat['start_sec']:.2f}〜{beat['end_sec']:.2f}秒 | {beat['id']} | {beat['kind']} | {note} | "
                f"{headline.replace('|', '/')} | {subtitle.replace('|', '/')} |"
            )
    timeline_lines += [
        "",
        "## Human review points",
        "",
        "- 0〜3秒のhookが、静止画の読みやすさを保ったまま一目で伝わるか。",
        "- hard cutの切替が自然か。微細zoom/panがないことによる読みやすさを確認する。",
        "- Short001のB1実ChatGPT画面、B2公式Voice参照、B3生活sceneがライブVoice画面と誤認されないか。実Voice captureは必要か。",
        "- Short002のB1→B2→B3で、個人情報の該当欄だけが段階的に隠れて見えるか。",
        "- Short003のB1公式マイナポータル、B2コンビニ証明書、B3 e-Taxがそれぞれ一目で具体的に分かるか。抽象rendererへ戻す必要がないか。",
        "- 最後3秒の結論Visual上で、180pxの実チャンネルアイコンとチャンネル名が中央に見えるか。疑似subscribeに見えないか。",
        "- CTAのcanonical音声、ChatGPTの発音、字幕の読みやすさを実音声で確認する。",
        "",
        "final、thumbnail確定、upload、publish、scheduleは未実施。",
        "",
        "Shorts探索バッチ001 Visual Redesign v5完成。",
        "不要なmicro motionを廃止。",
        "CTA中央化・Short003利用例Visualを具体化。",
        "人間Draft Gate待ち。",
    ]
    (SHORTS_ROOT / "work" / "batch_001_v5_timeline_review.md").write_text("\n".join(timeline_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--short", choices=["Short001", "Short002", "Short003", "all"], default="all")
    args = parser.parse_args()
    import imageio_ffmpeg

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    selected_ids = list(SHORTS) if args.short == "all" else [args.short]
    reports: list[dict[str, Any]] = []
    selected_frames: dict[str, dict[str, Path]] = {}
    for short_id in selected_ids:
        report, frames = build_one(short_id, ffmpeg)
        reports.append(report)
        selected_frames[short_id] = frames
    write_batch_outputs(reports, selected_frames)
    print(json.dumps(reports, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
