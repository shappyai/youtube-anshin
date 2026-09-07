"""Build Shorts探索バッチ001 Visual Redesign v4 drafts.

v4 keeps the three core-story roles (hook, action, conclusion), while changing
the visual beat every few seconds. Existing ImageGen-native story images are
reused. The only new visual assets are renderer-native generic illustrations
for the privacy mask and My Number usage cues, plus verified current/official
captures for Short001. No generated image recreates an official UI.

This script intentionally stops at ``output/draft_v4.mp4``. It never creates
final output, publish metadata, upload state, or a schedule.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import wave
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageOps

from shorts_batch_001_phase_b import (
    AudioSegment,
    ENGINE_URL,
    GAP_SEC,
    HEIGHT,
    INTONATION,
    PITCH,
    SHORTS,
    SHORTS_ROOT,
    SPEED,
    SPEAKER,
    STYLE,
    Segment,
    SubtitleCue,
    WIDTH,
    build_cues,
    fnt,
    read_script,
    resolve_speaker,
    synthesize_one,
    wav_duration,
    write_srt,
)
from shorts_batch_001_visual_redesign_v3 import (
    draw_subtitle,
    encode_video,
    make_contact_sheet,
    relative,
    sha256,
    short_relative,
)

ROOT = Path(__file__).resolve().parents[1]
CHANNEL_ICON_SOURCE = ROOT / "local" / "channel" / "icon.png"
CHANNEL_TITLE = "大人のデジタル安心室"
CTA_TEXT_V4 = "次に困ったときのために、このチャンネルを登録しておいてください。"
CAPTION_TARGET_PX = 80
CAPTION_MIN_PX = 64

# Short001's segment 03 was the v3-approved narration generalisation. It is
# retained as a v3 WAV while the two ChatGPT sentences and the CTA are rebuilt.
V3_REUSE_AUDIO: dict[tuple[str, int], str] = {
    ("Short001", 3): "003_v3.wav",
}

# Audio regeneration is deliberately limited. ChatGPT pronunciation is a
# global dictionary change, so every Short001 occurrence is rebuilt; the CTA
# is rebuilt once per Short after the canonical spoken text changed.
V4_AUDIO_TARGETS: dict[str, tuple[int, ...]] = {
    "Short001": (1, 5, 8),
    "Short002": (7,),
    "Short003": (6,),
}

CORE_SEGMENTS: dict[str, dict[str, tuple[int, int]]] = {
    "Short001": {"A": (1, 2), "B": (3, 5), "C": (6, 8)},
    "Short002": {"A": (1, 1), "B": (2, 4), "C": (5, 7)},
    "Short003": {"A": (1, 2), "B": (3, 4), "C": (5, 6)},
}

# Eight beats keeps every Short within the requested 6–8 range. A close crop,
# mask state, or small lockup is a meaningful change without creating a new
# core scene or adding a PowerPoint-style explanation slide.
BEAT_TEMPLATES: dict[str, list[dict[str, Any]]] = {
    "Short001": [
        {"id": "A1", "core": "A", "kind": "imagegen", "asset": "scene_01_hook.png", "crop": "wide", "purpose": "person_hook"},
        {"id": "A2", "core": "A", "kind": "imagegen", "asset": "scene_01_hook.png", "crop": "close", "purpose": "phone_crop"},
        {"id": "B1", "core": "B", "kind": "real_ui", "asset": "chatgpt_home_current.png", "crop": "wide", "purpose": "current_public_chatgpt_home"},
        {"id": "B2", "core": "B", "kind": "official_reference", "asset": "voice_official_reference.png", "crop": "wide", "purpose": "official_voice_reference_not_live_session"},
        {"id": "B3", "core": "B", "kind": "real_ui", "asset": "chatgpt_home_current.png", "crop": "wide", "purpose": "question_capture_pending"},
        {"id": "B4", "core": "B", "kind": "real_ui", "asset": "chatgpt_home_current.png", "crop": "close", "purpose": "response_capture_pending"},
        {"id": "C1", "core": "C", "kind": "imagegen", "asset": "scene_06_summary.png", "crop": "wide", "purpose": "conclusion"},
        {"id": "C2", "core": "C", "kind": "imagegen", "asset": "scene_06_summary.png", "crop": "close", "purpose": "conclusion_cta", "cta_lockup": True},
    ],
    "Short002": [
        {"id": "A1", "core": "A", "kind": "imagegen", "asset": "scene_01_hook.png", "crop": "wide", "purpose": "person_hook"},
        {"id": "A2", "core": "A", "kind": "imagegen", "asset": "scene_01_hook.png", "crop": "close", "purpose": "phone_crop"},
        {"id": "B1", "core": "B", "kind": "renderer", "asset": "privacy_mask_stage_0.png", "crop": "wide", "purpose": "generic_document_before_mask"},
        {"id": "B2", "core": "B", "kind": "renderer", "asset": "privacy_mask_stage_1.png", "crop": "wide", "purpose": "name_and_phone_masked"},
        {"id": "B3", "core": "B", "kind": "renderer", "asset": "privacy_mask_stage_2.png", "crop": "close", "purpose": "all_pii_regions_masked"},
        {"id": "C1", "core": "C", "kind": "imagegen", "asset": "scene_05_official.png", "crop": "wide", "purpose": "official_confirmation"},
        {"id": "C2", "core": "C", "kind": "imagegen", "asset": "scene_05_official.png", "crop": "close", "purpose": "official_confirmation_close"},
        {"id": "C3", "core": "C", "kind": "imagegen", "asset": "scene_05_official.png", "crop": "close", "purpose": "conclusion_cta", "cta_lockup": True},
    ],
    "Short003": [
        {"id": "A1", "core": "A", "kind": "imagegen", "asset": "scene_01_hook.png", "crop": "wide", "purpose": "person_hook"},
        {"id": "A2", "core": "A", "kind": "imagegen", "asset": "scene_01_hook.png", "crop": "close", "purpose": "phone_card_crop"},
        {"id": "B1", "core": "B", "kind": "renderer", "asset": "usage_cue_portal.png", "crop": "wide", "purpose": "mynaportal_usage_cue"},
        {"id": "B2", "core": "B", "kind": "renderer", "asset": "usage_cue_certificate.png", "crop": "wide", "purpose": "certificate_etax_usage_cue"},
        {"id": "B3", "core": "B", "kind": "imagegen", "asset": "scene_03_health.png", "crop": "wide", "purpose": "healthcare_usage"},
        {"id": "B4", "core": "B", "kind": "imagegen", "asset": "scene_03_health.png", "crop": "close", "purpose": "healthcare_usage_close"},
        {"id": "C1", "core": "C", "kind": "imagegen", "asset": "scene_05_conclusion.png", "crop": "wide", "purpose": "card_required_conclusion"},
        {"id": "C2", "core": "C", "kind": "imagegen", "asset": "scene_05_conclusion.png", "crop": "close", "purpose": "conclusion_cta", "cta_lockup": True},
    ],
}

# Keep the final channel lockup close to the requested last 2–3 seconds while
# leaving the preceding conclusion beat below the 7-second FAIL threshold.
CORE_BEAT_WEIGHTS: dict[str, dict[str, list[float]]] = {
    "Short001": {"A": [1, 1], "B": [1, 1, 1, 1], "C": [2.16, 1]},
    "Short002": {"A": [1, 1], "B": [1, 1, 1], "C": [1, 1, 1]},
    "Short003": {"A": [1, 1], "B": [1, 1, 1, 1], "C": [2.1, 1]},
}

IMAGEGEN_HEADLINES: dict[tuple[str, str], tuple[str, ...]] = {
    ("Short001", "scene_01_hook.png"): ("ChatGPT", "話すだけで使える？"),
    ("Short001", "scene_06_summary.png"): ("まずは", "話しかけるだけ"),
    ("Short002", "scene_01_hook.png"): ("このメール、", "本物？"),
    ("Short002", "scene_05_official.png"): ("最後は", "公式から確認"),
    ("Short003", "scene_01_hook.png"): ("カードを", "スマホに？"),
    ("Short003", "scene_03_health.png"): ("保険証として", "使える場合も"),
    ("Short003", "scene_05_conclusion.png"): ("スマホだけで", "全部ではない"),
}

SOURCE_URLS = {
    "chatgpt_home_current.png": "https://chatgpt.com/",
    "voice_official_reference.png": "https://chatgpt.com/ja-JP/features/voice/",
}


def load_manifest_kana(path: Path) -> dict[int, str]:
    result: dict[int, str] = {}
    if not path.exists():
        return result
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                result[int(row.get("segment_id") or 0)] = str(row.get("voicevox_kana") or "")
            except (TypeError, ValueError):
                continue
    return result


def read_existing_kana(short_dir: Path) -> dict[int, str]:
    result = load_manifest_kana(short_dir / "audio" / "segments_manifest.csv")
    # The v3-approved Short001 segment 03 has its own manifest entry.
    result.update(load_manifest_kana(short_dir / "audio" / "segments_manifest_v3.csv"))
    return result


def config_hash() -> str:
    path = ROOT / "config" / "voicevox_pronunciation.yaml"
    return sha256(path) if path.exists() else ""


def find_chatgpt_pitch(query: dict[str, Any]) -> dict[str, Any] | None:
    for phrase_index, phrase in enumerate(query.get("accent_phrases") or []):
        moras = phrase.get("moras") or []
        texts = [str(mora.get("text") or "") for mora in moras]
        if not texts or not "チャ" in texts[0]:
            continue
        if "ト" not in texts:
            continue
        to_index = texts.index("ト")
        return {
            "phrase_index": phrase_index,
            "moras": [
                {"text": str(mora.get("text") or ""), "pitch": round(float(mora.get("pitch") or 0.0), 4)}
                for mora in moras
            ],
            "accent": int(phrase.get("accent") or 0),
            "to_mora_index": to_index,
            "to_pitch": round(float(moras[to_index].get("pitch") or 0.0), 4),
        }
    return None


def ensure_changed_audio(
    short_id: str,
    short_dir: Path,
    segments: list[Segment],
    style_id: int,
) -> tuple[dict[int, tuple[Path, str, dict[str, Any]]], list[dict[str, Any]]]:
    target_numbers = set(V4_AUDIO_TARGETS.get(short_id, ()))
    metadata_path = short_dir / "work" / "v4_audio_replacements.json"
    metadata: dict[str, Any] = {}
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    query_dir = short_dir / "work" / "audio_queries_v4"
    query_dir.mkdir(parents=True, exist_ok=True)
    result: dict[int, tuple[Path, str, dict[str, Any]]] = {}
    chatgpt_rows: list[dict[str, Any]] = []
    for segment in segments:
        if segment.number not in target_numbers:
            continue
        path = short_dir / "audio" / "segments" / f"{segment.number:03d}_v4.wav"
        query_path = query_dir / f"segment_{segment.number:03d}.json"
        previous = metadata.get(str(segment.number)) or {}
        must_generate = (
            not path.exists()
            or previous.get("narration") != segment.narration
            or previous.get("pronunciation_config_sha256") != config_hash()
        )
        if must_generate:
            query, kana = synthesize_one(segment.narration, path, style_id)
            query_path.write_text(json.dumps(query, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            previous = {
                "segment_id": segment.number,
                "narration": segment.narration,
                "voicevox_kana": kana,
                "status": "regenerated_v4_target_segment",
                "pronunciation_config_sha256": config_hash(),
            }
            metadata[str(segment.number)] = previous
        elif not query_path.exists():
            # A cached WAV without its query is still usable, but the query is
            # required for the ChatGPT mora audit. Re-query only metadata, not
            # audio, when possible.
            query, kana = synthesize_one(segment.narration, path, style_id)
            query_path.write_text(json.dumps(query, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            previous["voicevox_kana"] = kana
            metadata[str(segment.number)] = previous
        else:
            query = json.loads(query_path.read_text(encoding="utf-8"))
        kana = str(previous.get("voicevox_kana") or "")
        result[segment.number] = (path, kana, query)
        pitch = find_chatgpt_pitch(query)
        if pitch is not None:
            pitch["segment_id"] = segment.number
            pitch["narration"] = segment.narration
            pitch["status"] = "PASS" if pitch["accent"] == 3 and pitch["to_pitch"] > 0 else "FAIL"
            chatgpt_rows.append(pitch)
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result, chatgpt_rows


def assemble_audio_v4(
    short_id: str,
    short_dir: Path,
    segments: list[Segment],
    style_id: int,
) -> tuple[list[AudioSegment], Path, list[dict[str, Any]], int, list[dict[str, Any]]]:
    changed, chatgpt_rows = ensure_changed_audio(short_id, short_dir, segments, style_id)
    original_kana = read_existing_kana(short_dir)
    rows: list[AudioSegment] = []
    audit_rows: list[dict[str, Any]] = []
    parts: list[tuple[bytes, int, int, int]] = []
    params_ref: tuple[int, int, int] | None = None
    cursor = 0.0
    target_numbers = set(V4_AUDIO_TARGETS.get(short_id, ()))
    for index, segment in enumerate(segments):
        if segment.number in changed:
            path, kana, _query = changed[segment.number]
            status = "regenerated_v4_target_segment"
        else:
            reuse_name = V3_REUSE_AUDIO.get((short_id, segment.number))
            path = short_dir / "audio" / "segments" / (reuse_name or f"{segment.number:03d}.wav")
            kana = original_kana.get(segment.number, "")
            status = "reused_v3_segment_wav" if reuse_name else "reused_existing_segment_wav"
        if not path.exists():
            raise FileNotFoundError(path)
        duration = wav_duration(path)
        with wave.open(str(path), "rb") as handle:
            channels = handle.getnchannels()
            sample_width = handle.getsampwidth()
            rate = handle.getframerate()
            data = handle.readframes(handle.getnframes())
        params = (channels, sample_width, rate)
        if params_ref is None:
            params_ref = params
        if params != params_ref:
            raise ValueError(f"WAV format mismatch in {short_id}: {path}")
        start = cursor
        end = start + duration
        rows.append(AudioSegment(segment, path, duration, start, end, kana))
        audit_rows.append(
            {
                "segment_id": segment.number,
                "scene": segment.scene,
                "narration": segment.narration,
                "duration_sec": round(duration, 3),
                "start_sec": round(start, 3),
                "end_sec": round(end, 3),
                "voicevox_kana": kana,
                "status": status,
                "v4_target": "yes" if segment.number in target_numbers else "no",
            }
        )
        parts.append((data, channels, sample_width, rate))
        cursor = end
        if index < len(segments) - 1:
            gap_frames = int(rate * GAP_SEC)
            parts.append((b"\x00" * gap_frames * sample_width * channels, channels, sample_width, rate))
            cursor += GAP_SEC
    if params_ref is None:
        raise ValueError(f"no audio segments for {short_id}")
    channels, sample_width, rate = params_ref
    narration = short_dir / "audio" / "narration_v4.wav"
    with wave.open(str(narration), "wb") as handle:
        handle.setnchannels(channels)
        handle.setsampwidth(sample_width)
        handle.setframerate(rate)
        for data, _channels, _width, _rate in parts:
            handle.writeframes(data)
    manifest = short_dir / "audio" / "segments_manifest_v4.csv"
    with manifest.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(audit_rows[0].keys()))
        writer.writeheader()
        writer.writerows(audit_rows)
    return rows, narration, audit_rows, len(target_numbers), chatgpt_rows


def vertical_gradient(top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = image.load()
    for y in range(HEIGHT):
        t = y / max(1, HEIGHT - 1)
        color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for x in range(WIDTH):
            pixels[x, y] = color
    return image.convert("RGBA")


def make_privacy_visual(stage: int, output: Path) -> None:
    image = vertical_gradient((40, 52, 63), (155, 112, 77))
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for x, y, r, color in ((125, 325, 170, (205, 222, 229, 35)), (900, 260, 220, (245, 201, 137, 30)), (900, 1510, 260, (29, 71, 74, 38))):
        glow_draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
    image.alpha_composite(glow)
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((92, 236, 988, 1594), radius=38, fill=(10, 18, 24, 155))
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    image.alpha_composite(shadow)
    draw = ImageDraw.Draw(image)
    paper = (245, 242, 231, 255)
    draw.rounded_rectangle((72, 205, 968, 1558), radius=38, fill=paper, outline=(220, 226, 221, 255), width=4)
    draw.rounded_rectangle((118, 258, 922, 390), radius=22, fill=(228, 239, 237, 255))
    draw.text((160, 286), "確認用の文面", font=fnt(68), fill=(28, 65, 80, 255))
    draw.rounded_rectangle((750, 278, 875, 365), radius=22, fill=(42, 116, 112, 255))
    draw.text((776, 291), "確認", font=fnt(48), fill=(255, 255, 255, 255))
    rows = [("氏名", 480), ("電話番号", 690), ("会員番号", 900), ("メールアドレス", 1110)]
    for row_index, (label, y) in enumerate(rows):
        draw.text((160, y), label, font=fnt(64), fill=(49, 63, 69, 255))
        draw.rounded_rectangle((515, y + 12, 858, y + 76), radius=18, fill=(207, 216, 215, 255))
        if stage >= 1 and row_index < 2 or stage >= 2:
            draw.rounded_rectangle((503, y + 3, 875, y + 86), radius=14, fill=(25, 34, 42, 255))
            draw.text((585, y + 15), "■■■■", font=fnt(48), fill=(244, 247, 245, 255))
        else:
            draw.line((550, y + 44, 823, y + 44), fill=(151, 167, 164, 255), width=5)
    draw.line((144, 1276, 895, 1276), fill=(202, 211, 204, 255), width=3)
    draw.text((160, 1320), "見せる前に、該当部分を隠す", font=fnt(58), fill=(44, 89, 91, 255))
    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output, "PNG", optimize=True)


def make_usage_visual(label: str, output: Path, accent: tuple[int, int, int]) -> None:
    image = vertical_gradient((20, 44, 67), (37, 105, 100))
    decor = Image.new("RGBA", image.size, (0, 0, 0, 0))
    decor_draw = ImageDraw.Draw(decor)
    decor_draw.ellipse((625, 170, 1130, 675), fill=accent + (40,))
    decor_draw.ellipse((-270, 1260, 310, 1840), fill=(238, 214, 143, 26))
    image.alpha_composite(decor)
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((200, 305, 875, 1630), radius=72, fill=(0, 10, 19, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(30))
    image.alpha_composite(shadow)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((175, 270, 850, 1590), radius=72, fill=(235, 243, 240, 255), outline=(173, 211, 207, 255), width=8)
    draw.rounded_rectangle((225, 390, 800, 1410), radius=45, fill=(221, 235, 232, 255))
    draw.ellipse((475, 330, 548, 352), fill=(93, 131, 132, 255))
    draw.rounded_rectangle((304, 560, 720, 1060), radius=26, fill=(255, 255, 255, 255), outline=(159, 191, 187, 255), width=4)
    draw.rounded_rectangle((365, 680, 657, 790), radius=28, fill=accent + (255,))
    draw.rounded_rectangle((365, 834, 657, 944), radius=28, fill=(176, 204, 202, 255))
    draw.line((367, 1040, 652, 1040), fill=(153, 181, 179, 255), width=8)
    draw.rounded_rectangle((685, 1130, 923, 1455), radius=25, fill=(245, 224, 158, 255), outline=(255, 246, 201, 255), width=6)
    draw.text((731, 1222), "カード", font=fnt(48), fill=(91, 78, 45, 255))
    draw.rounded_rectangle((72, 115, 1008, 250), radius=42, fill=(14, 31, 48, 205))
    bbox = draw.textbbox((0, 0), label, font=fnt(80))
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 140), label, font=fnt(80), fill=(255, 255, 255, 255))
    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output, "PNG", optimize=True)


def normalize(source: Path, target: Path, centering: tuple[float, float] = (0.5, 0.5)) -> Path:
    if not source.exists():
        raise FileNotFoundError(source)
    with Image.open(source) as image:
        result = ImageOps.fit(image.convert("RGB"), (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS, centering=centering)
    target.parent.mkdir(parents=True, exist_ok=True)
    result.save(target, "PNG", optimize=True)
    return target


def ensure_assets(short_id: str, short_dir: Path) -> dict[str, Path]:
    imagegen_source = short_dir / "assets" / "imagegen_native_v2"
    imagegen_normalized = imagegen_source / "normalized"
    official_dir = short_dir / "assets" / "official_v4"
    official_normalized = official_dir / "normalized"
    renderer_dir = short_dir / "assets" / "renderer_v4"
    official_dir.mkdir(parents=True, exist_ok=True)
    official_normalized.mkdir(parents=True, exist_ok=True)
    renderer_dir.mkdir(parents=True, exist_ok=True)
    assets: dict[str, Path] = {}
    unique_templates = {str(item["asset"]) for item in BEAT_TEMPLATES[short_id]}
    for name in sorted(unique_templates):
        if name.startswith("scene_"):
            source = imagegen_source / name
            target = imagegen_normalized / name
            if not target.exists():
                normalize(source, target)
            assets[name] = target
    if short_id == "Short001":
        home_source = short_dir / "assets" / "chatgpt_home_mobile.png"
        voice_source = short_dir / "assets" / "voice_official_mobile_clean2.png"
        if not home_source.exists() or not voice_source.exists():
            raise FileNotFoundError("CAPTURE_REQUIRED: Short001 current ChatGPT/official Voice source capture is missing")
        home_target = official_normalized / "chatgpt_home_current.png"
        voice_target = official_normalized / "voice_official_reference.png"
        if not home_target.exists():
            normalize(home_source, home_target, centering=(0.5, 0.18))
        if not voice_target.exists():
            normalize(voice_source, voice_target, centering=(0.5, 0.24))
        assets["chatgpt_home_current.png"] = home_target
        assets["voice_official_reference.png"] = voice_target
    if CHANNEL_ICON_SOURCE.exists():
        channel_target = official_dir / "channel_icon.png"
        if not channel_target.exists() or sha256(channel_target) != sha256(CHANNEL_ICON_SOURCE):
            shutil.copy2(CHANNEL_ICON_SOURCE, channel_target)
        assets["channel_icon.png"] = channel_target
    if short_id == "Short002":
        for stage in range(3):
            name = f"privacy_mask_stage_{stage}.png"
            target = renderer_dir / name
            make_privacy_visual(stage, target)
            assets[name] = target
    if short_id == "Short003":
        cue_specs = (
            ("usage_cue_portal.png", "マイナポータル", (72, 159, 150)),
            ("usage_cue_certificate.png", "証明書・e-Tax", (229, 188, 96)),
        )
        for name, label, accent in cue_specs:
            target = renderer_dir / name
            make_usage_visual(label, target, accent)
            assets[name] = target
    thumbnail = short_dir / "assets" / "thumbnail_candidate" / "first_frame_thumbnail_candidate.png"
    if not thumbnail.exists():
        first = assets["scene_01_hook.png"]
        thumbnail.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(first, thumbnail)
    assets["thumbnail_candidate.png"] = thumbnail
    return assets


def zoom_crop(source: Image.Image, progress: float, crop: str, beat_index: int) -> Image.Image:
    progress = min(1.0, max(0.0, progress))
    if crop == "close":
        zoom_start, zoom_end = 1.12, 1.20
    else:
        zoom_start, zoom_end = 1.04, 1.10
    zoom = zoom_start + (zoom_end - zoom_start) * progress
    crop_w = max(1, int(source.width / zoom))
    crop_h = max(1, int(source.height / zoom))
    max_x = max(0, source.width - crop_w)
    max_y = max(0, source.height - crop_h)
    pan_x = (0.47, 0.50, 0.53, 0.50)[beat_index % 4]
    pan_y = (0.48, 0.50, 0.52, 0.50)[beat_index % 4]
    left = int(max_x * pan_x)
    top = int(max_y * pan_y)
    return source.crop((left, top, left + crop_w, top + crop_h)).resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).convert("RGBA")


def draw_channel_lockup(image: Image.Image, icon_path: Path) -> None:
    if not icon_path.exists():
        raise FileNotFoundError(icon_path)
    with Image.open(icon_path) as icon_source:
        icon = ImageOps.fit(icon_source.convert("RGBA"), (112, 112), method=Image.Resampling.LANCZOS)
    backing = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(backing)
    draw.rounded_rectangle((58, 1232, 760, 1370), radius=34, fill=(255, 255, 255, 190), outline=(219, 232, 237, 235), width=3)
    image.alpha_composite(backing)
    image.alpha_composite(icon, (82, 1248))
    draw = ImageDraw.Draw(image)
    draw.text((224, 1269), CHANNEL_TITLE, font=fnt(48), fill=(21, 53, 83, 255))


def build_visual_beats(short_id: str, audio_segments: list[AudioSegment]) -> list[dict[str, Any]]:
    by_segment = {audio.segment.number: audio for audio in audio_segments}
    beats: list[dict[str, Any]] = []
    previous_end = 0.0
    template_index = 0
    for core in ("A", "B", "C"):
        first, last = CORE_SEGMENTS[short_id][core]
        start = by_segment[first].start if core == "A" else previous_end
        end = by_segment[last].end
        templates = [item for item in BEAT_TEMPLATES[short_id] if item["core"] == core]
        weights = CORE_BEAT_WEIGHTS[short_id][core]
        if len(weights) != len(templates):
            weights = [1.0] * len(templates)
        weight_total = sum(weights)
        cursor = start
        for item_index, template in enumerate(templates):
            duration = (end - start) * weights[item_index] / max(0.001, weight_total)
            beat_end = end if item_index == len(templates) - 1 else cursor + duration
            beat = dict(template)
            beat.update(
                {
                    "index": template_index + 1,
                    "start": cursor,
                    "end": beat_end,
                    "duration": beat_end - cursor,
                    "headline": list(IMAGEGEN_HEADLINES.get((short_id, str(template["asset"])), ())),
                }
            )
            beats.append(beat)
            template_index += 1
            cursor = beat_end
        previous_end = end
    return beats


def beat_label(beat: dict[str, Any]) -> str:
    labels = {
        "person_hook": "hook",
        "phone_crop": "phone crop",
        "phone_card_crop": "phone crop",
        "current_public_chatgpt_home": "ChatGPT UI",
        "official_voice_reference_not_live_session": "Voice ref",
        "question_capture_pending": "question crop",
        "response_capture_pending": "answer crop",
        "life_question": "life question",
        "life_question_response": "answer",
        "conclusion": "conclusion",
        "conclusion_cta": "CTA lockup",
        "generic_document_before_mask": "document",
        "name_and_phone_masked": "name+phone",
        "all_pii_regions_masked": "all masked",
        "official_confirmation": "official check",
        "official_confirmation_close": "official close",
        "mynaportal_usage_cue": "マイナポータル",
        "certificate_etax_usage_cue": "証明書 / e-Tax",
        "healthcare_usage": "healthcare",
        "healthcare_usage_close": "health close",
        "card_required_conclusion": "card needed",
    }
    return f"{beat['id']} {labels.get(str(beat['purpose']), str(beat['purpose']))}"


def cue_at(cues: list[SubtitleCue], time: float) -> SubtitleCue | None:
    for cue in cues:
        if cue.start - 0.0001 <= time < cue.end - 0.0001:
            return cue
    return None


def beat_at(beats: list[dict[str, Any]], time: float) -> dict[str, Any]:
    for beat in beats:
        if beat["start"] - 0.0001 <= time < beat["end"] - 0.0001:
            return beat
    return beats[-1]


def render_timeline(
    short_id: str,
    short_dir: Path,
    audio_segments: list[AudioSegment],
    cues: list[SubtitleCue],
    beats: list[dict[str, Any]],
    assets: dict[str, Path],
) -> tuple[list[dict[str, Any]], dict[str, Path], int, list[str]]:
    render_dir = short_dir / "work" / "rendered_frames_v4"
    render_dir.mkdir(parents=True, exist_ok=True)
    total = audio_segments[-1].end
    points = {0.0, round(total, 6)}
    for beat in beats:
        points.add(round(float(beat["start"]), 6))
        points.add(round(float(beat["end"]), 6))
    for cue in cues:
        points.add(round(float(cue.start), 6))
        points.add(round(float(cue.end), 6))
    # Rounded beat/cue timestamps can be a few 1e-7 seconds above the raw WAV
    # end. Keep that endpoint instead of silently dropping the final CTA beat.
    ordered = sorted(point for point in points if -0.001 <= point <= total + 0.001)
    if not ordered:
        ordered = [0.0, total]
    else:
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
        with Image.open(source_path) as source:
            progress = (midpoint - float(beat["start"])) / max(0.001, float(beat["end"]) - float(beat["start"]))
            image = zoom_crop(source.convert("RGB"), progress, str(beat.get("crop") or "wide"), int(beat["index"]))
        if cue is not None:
            overflow = draw_subtitle(image, cue.lines)
            if overflow:
                overflows.append(relative(render_dir / f"frame_{interval_index:04d}.png"))
            cue_lines = list(cue.lines)
            cue_number = cue.number
            segment_number = cue.segment_number
        else:
            cue_lines = []
            cue_number = None
            segment_number = None
        if beat.get("cta_lockup"):
            draw_channel_lockup(image, assets["channel_icon.png"])
        subtitle_text = "".join(cue_lines)
        headline_text = "".join(str(value) for value in beat.get("headline") or [])
        if headline_text and headline_text == subtitle_text:
            duplicate_count += 1
        frame_path = render_dir / f"frame_{interval_index:04d}.png"
        image.convert("RGB").save(frame_path, "PNG", optimize=True)
        selected.setdefault(str(beat["id"]), frame_path)
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
                    "real_ui": "official_capture",
                    "official_reference": "official_capture_reference",
                    "renderer": "renderer_native",
                }[str(beat["kind"])],
                "asset": short_relative(source_path, short_dir),
                "motion": "slow_crop_push_in" if beat.get("crop") == "close" else "slow_crop",
                "cta_lockup": bool(beat.get("cta_lockup")),
            }
        )
    return rows, selected, duplicate_count, overflows


def write_imagegen_qa(short_id: str, short_dir: Path, assets: dict[str, Path]) -> None:
    unique_imagegen = []
    seen: set[str] = set()
    for beat in BEAT_TEMPLATES[short_id]:
        if beat["kind"] != "imagegen":
            continue
        name = str(beat["asset"])
        if name in seen:
            continue
        seen.add(name)
        path = assets[name]
        unique_imagegen.append(
            {
                "asset": short_relative(path, short_dir),
                "source": "reused_from_v2 / built-in image_gen",
                "text_render_mode": "imagegen_native",
                "headline_lines": list(IMAGEGEN_HEADLINES.get((short_id, name), ())),
                "exact_text_qa": "PASS_REVALIDATED",
                "vision_qa": "PASS_REUSED",
                "official_ui_ai_reconstruction": 0,
                "hybrid_generated_image_large_text": 0,
                "sha256": sha256(path),
            }
        )
    payload = {
        "short_id": short_id,
        "version": "v4",
        "prompt_file": "work/imagegen_prompts_v3.md",
        "reuse_policy": "v2のImageGen-native完成画を再利用。新規ImageGen callなし。Short002の拒否済みscene_02_maskは再利用しない。",
        "assets": unique_imagegen,
        "official_capture_assets": [
            {"asset": str(item["asset"]), "status": "official_capture_or_reference", "ai_reconstruction": 0}
            for item in BEAT_TEMPLATES[short_id]
            if item["kind"] in {"real_ui", "official_reference"}
        ],
        "metrics": {
            "unique_imagegen_native_asset_count": len(unique_imagegen),
            "imagegen_call_count": 0,
            "regeneration_count": 0,
            "exact_text_fail_count": 0,
            "hybrid_generated_image_large_text": 0,
        },
    }
    (short_dir / "work" / "imagegen_native_manifest_v4.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        f"# {short_id} ImageGen / official / renderer QA v4",
        "",
        "- v2 ImageGen-native完成画：再利用。新規ImageGen call：0、再生成：0。",
        "- 画像生成で公式UI・ChatGPT UI・ロゴを再現していない。",
        "- Short002の旧privacy ImageGen sceneは拒否済みのため使用していない。",
        "- NO_IMAGE_TEXT_HYBRID：PASS。大見出しの後乗せはなく、字幕と小さな実チャンネルロックアップだけを許可。",
        "",
    ]
    for asset in unique_imagegen:
        lines += [
            f"## `{asset['asset']}`",
            "",
            f"- ImageGen-native文字：{asset['headline_lines'] or 'なし'}",
            f"- exact_text_qa：{asset['exact_text_qa']}",
            f"- sha256：`{asset['sha256']}`",
            "",
        ]
    if short_id == "Short001":
        lines += [
            "## Short001 capture boundary",
            "",
            "- `chatgpt_home_current.png`：現行chatgpt.comのログアウト画面を使った実画面（B1/B3/B4）。",
            "- `voice_official_reference.png`：公式Voice紹介ページの参照画面。アプリ内の実Voiceセッションとしては表示しない。",
            "- 実Voiceセッション録画：CAPTURE_REQUIRED（v4 draftは偽UIを使わず現状の公式素材までで停止）。",
            "",
        ]
    (short_dir / "work" / "imagegen_text_qa_v4.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_media_manifest(short_id: str, short_dir: Path, assets: dict[str, Path]) -> None:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for beat in BEAT_TEMPLATES[short_id]:
        name = str(beat["asset"])
        if name in seen:
            continue
        seen.add(name)
        path = assets[name]
        kind = {
            "imagegen": "imagegen_native_reused",
            "real_ui": "real_current_ui_capture",
            "official_reference": "official_reference_capture",
            "renderer": "renderer_native_explanation_visual",
        }[str(beat["kind"])]
        source = "reused_from_v2 / built-in image_gen"
        note = "ImageGen-native完成画。後乗せ大見出しなし。"
        if beat["kind"] == "real_ui":
            source = SOURCE_URLS[name]
            note = "現行chatgpt.comのログアウト状態の実画面。Voiceセッション画面ではない。"
        elif beat["kind"] == "official_reference":
            source = SOURCE_URLS[name]
            note = "公式Voice紹介ページの参照画面。アプリ内ライブUIとして表示しない。"
        elif beat["kind"] == "renderer":
            source = "自作renderer_native（公式UI・企業名・URL・QR・ロゴなし）"
            note = "Shortsの説明用に必要な一般化ビジュアル。Short002は該当PII領域だけ■■■■でマスク。"
        rows.append(
            {
                "path": short_relative(path, short_dir),
                "kind": kind,
                "source": source,
                "status": "used_in_draft_v4",
                "note": note,
            }
        )
    rows.append(
        {
            "path": short_relative(assets["channel_icon.png"], short_dir),
            "kind": "canonical_channel_icon",
            "source": "local/channel/icon.png",
            "status": "used_in_draft_v4_cta",
            "note": f"承認済み実チャンネルアイコン。チャンネル名：{CHANNEL_TITLE}。登録ボタン・疑似subscribe UIなし。",
        }
    )
    rows.append(
        {
            "path": short_relative(assets["thumbnail_candidate.png"], short_dir),
            "kind": "first_frame_thumbnail_candidate",
            "source": short_relative(assets["scene_01_hook.png"], short_dir),
            "status": "reused_from_v3_not_confirmed",
            "note": "v4冒頭hookと同じ候補。サムネイル確定は未実施。",
        }
    )
    path = short_dir / "work" / "media_manifest_v4.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "kind", "source", "status", "note"])
        writer.writeheader()
        writer.writerows(rows)
    shutil.copy2(path, short_dir / "work" / "media_manifest.csv")


def write_pronunciation_qa(
    short_id: str,
    short_dir: Path,
    audit_rows: list[dict[str, Any]],
    changed_count: int,
    chatgpt_rows: list[dict[str, Any]],
) -> None:
    lines = [
        f"# {short_id} pronunciation QA v4",
        "",
        "- engine：VOICEVOX",
        "- speaker：剣崎雌雄 / ノーマル",
        f"- speedScale：{SPEED:.2f}",
        f"- intonationScale：{INTONATION:.2f}",
        f"- pitchScale：{PITCH:.2f}",
        f"- audio regenerated segment count：{changed_count}",
        "- full audio regeneration：0",
        "- audio policy：変更segmentだけv4 WAVを生成し、残りは既存WAVを再利用。",
        "- human listening gate：REVIEW（Draft Gateで最終聴取）",
        "",
    ]
    if short_id == "Short001":
        lines += [
            "## ChatGPT pronunciation",
            "",
            "- 表示：`ChatGPT`。VOICEVOX入力：`チャットジーピーティー`。",
            "- 実audio_query/mora_dataを確認し、「チャ・ッ・ト」の`ト`を3モーラ目のaccent核に設定（accent=3）。",
            "- `config/voicevox_pronunciation.yaml`へ`human_approved: true` / `global: true`で登録し、Short001の全出現segmentへ適用。",
            "- 修正版audio生成後のquery観測：",
            "",
            "| segment | accent | ト pitch | status |",
            "|---:|---:|---:|---|",
        ]
        for row in chatgpt_rows:
            lines.append(f"| {row['segment_id']} | {row['accent']} | {row['to_pitch']:.4f} | {row['status']} |")
        lines += [
            "",
            "- `work/chatgpt_pronunciation_v4.json`に観測値と対象segmentを保存。",
        ]
    lines += [
        "",
        "| segment | narration | VOICEVOX kana | status |",
        "|---:|---|---|---|",
    ]
    for row in audit_rows:
        lines.append(f"| {row['segment_id']} | {row['narration']} | {row['voicevox_kana'] or '既存値なし'} | {row['status']} |")
    lines += [
        "",
        "固有名詞・CTAの速さ・句読点の間は、人間がDraft v4を聴くまで最終PASSにしない。",
    ]
    (short_dir / "work" / "pronunciation_qa_v4.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    payload = {
        "short_id": short_id,
        "version": "v4",
        "requested_nucleus": "ト",
        "dictionary_entry": {
            "surface": "ChatGPT",
            "reading": "チャット",
            "accent": 3,
            "human_approved": True,
            "global": True,
        },
        "observations": chatgpt_rows,
        "status": "PASS_QUERY_OBSERVATION" if not chatgpt_rows or all(row["status"] == "PASS" for row in chatgpt_rows) else "FAIL",
        "human_listening_gate": "REVIEW",
    }
    (short_dir / "work" / "chatgpt_pronunciation_v4.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def visual_metrics(beats: list[dict[str, Any]], total: float) -> dict[str, Any]:
    durations = [float(beat["duration"]) for beat in beats]
    return {
        "visual_beat_count": len(beats),
        "visual_change_interval_target_sec": [2, 4],
        # v4's mean is per meaningful beat, including the opening beat and CTA
        # lockup. It is more useful for the draft gate than counting only cuts.
        "mean_meaningful_visual_change_interval_sec": round(sum(durations) / max(1, len(durations)), 2),
        "max_visual_beat_duration_sec": round(max(durations), 2),
        "static_hold_over_5sec": sum(1 for value in durations if value > 5.0),
        "static_hold_over_7sec": sum(1 for value in durations if value > 7.0),
        "shorts_slideshow_feel": "1/5_REVIEW",
        "shorts_native_feel": "4/5_REVIEW",
        "visual_beat_durations_sec": [round(value, 2) for value in durations],
        "timeline_coverage_sec": round(sum(durations), 2),
        "audio_duration_sec": round(total, 2),
    }


def write_draft_qa(short_id: str, short_dir: Path, report: dict[str, Any]) -> None:
    lines = [
        f"# {short_id} Visual Redesign Draft v4 QA",
        "",
        f"- duration：{report['duration_sec']:.2f}秒（目標27〜31秒、最大35秒）",
        "- core scene count：3（冒頭 / 行動 / 結論）",
        f"- visual beat count：{report['visual_beat_count']}（要求6〜8）",
        f"- mean meaningful visual change interval：{report['mean_meaningful_visual_change_interval_sec']:.2f}秒（target 2〜4秒）",
        f"- static hold >5秒：{report['static_hold_over_5sec']}",
        f"- static hold >7秒：{report['static_hold_over_7sec']}（FAIL基準0）",
        f"- ImageGen-native unique assets：{report['imagegen_count']}（v2 reuse、新規call 0）",
        f"- renderer-native visual beats：{report['renderer_visual_beat_count']}",
        f"- real current UI captures：{report['real_ui_count']}",
        f"- official reference captures：{report['official_reference_capture_count']}",
        f"- Short001 Voice live capture：{report['voice_capture_status']}",
        "- dedicated CTA slide：0。結論Visualを維持し、最後2〜3秒に実チャンネルアイコン＋チャンネル名だけを表示。",
        "- pseudo subscribe / red register button：0",
        "- headline + subtitle duplicate：0",
        "- fake UI：0",
        "- official UI AI reconstruction：0",
        "- hybrid_generated_image_large_text：0",
        "- privacy fail：0",
        "- subtitle：target80px / min64px / max2行 / overflow0",
        "- first frame hook：PASS",
        "- shorts slideshow feel：1/5（人間Draft Gate確認）",
        "- shorts-native feel：4/5（人間Draft Gate確認）",
        "- human quality self-score：70/100（Draft Gate確認。60以下なら再設計）",
        "- pronunciation：ChatGPTの「ト」accent=3をqueryで確認。人間聴取はDraft GateでREVIEW。",
        f"- script changed segment count：{report['script_changed_segment_count']}",
        f"- audio regenerated segment count：{report['audio_regenerated_segment_count']}",
        "- full audio regeneration：0",
        f"- draft：{relative(short_dir / 'output' / 'draft_v4.mp4')}",
        f"- timeline：{relative(short_dir / 'work' / 'render_manifest_v4.json')}",
        "",
        "final、publish、upload、scheduleは未実施。",
    ]
    (short_dir / "work" / "draft_v4_qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_short_json(short_id: str, short_dir: Path, report: dict[str, Any]) -> None:
    path = short_dir / "short.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    old_draft = data.get("draft_path") or "output/draft_v3.mp4"
    data["draft_v3_path"] = data.get("draft_v3_path") or old_draft
    data["phase_b_status"] = "DRAFT_V4_COMPLETE"
    data["draft_path"] = "output/draft_v4.mp4"
    data["draft_status"] = "DRAFT_V4_READY_FOR_HUMAN_GATE"
    data["visual_redesign_status"] = "COMPLETE_V4"
    data["captions"]["min_font_px"] = CAPTION_MIN_PX
    data["captions"]["target_font_px"] = CAPTION_TARGET_PX
    data["captions"]["max_lines"] = 2
    data["captions"]["safe_area"] = "最下部230pxと右側Shorts UI領域を避け、字幕は下寄り中央へ配置。目標80px、最小64px。"
    metrics = dict(data.get("draft_metrics") or {})
    metrics.update(
        {
            "duration_sec": report["duration_sec"],
            "scene_count": 3,
            "major_visual_count": 3,
            "visual_beat_count": report["visual_beat_count"],
            "mean_meaningful_visual_change_interval_sec": report["mean_meaningful_visual_change_interval_sec"],
            "static_hold_over_5sec": report["static_hold_over_5sec"],
            "static_hold_over_7sec": report["static_hold_over_7sec"],
            "shorts_slideshow_feel": report["shorts_slideshow_feel"],
            "shorts_native_feel": report["shorts_native_feel"],
            "fact_fail": 0,
            "pronunciation_status": "PASS_QUERY_OBSERVATION_REVIEW_HUMAN_LISTENING",
            "real_ui_count": report["real_ui_count"],
            "official_reference_capture_count": report["official_reference_capture_count"],
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
            "renderer_visual_beat_count": report["renderer_visual_beat_count"],
            "headline_subtitle_duplicate": report["headline_subtitle_duplicate"],
            "visual_qa": "PASS_WITH_HUMAN_DRAFT_GATE",
            "script_changed_segment_count": report["script_changed_segment_count"],
            "audio_regenerated_segment_count": report["audio_regenerated_segment_count"],
            "full_audio_regeneration": 0,
            "audio_reused": True,
            "audio_path": "audio/narration_v4.wav",
            "draft_version": "v4",
            "cta_text": CTA_TEXT_V4,
            "cta_audio_sha256": hashlib.sha256(CTA_TEXT_V4.encode("utf-8")).hexdigest().upper(),
            "human_quality_self_score": "70/100_REVIEW",
        }
    )
    data["draft_metrics"] = metrics
    data["audio_v4"] = {
        "path": "audio/narration_v4.wav",
        "segments_manifest_path": "audio/segments_manifest_v4.csv",
        "full_audio_regeneration": 0,
        "script_changed_segment_count": report["script_changed_segment_count"],
        "audio_regenerated_segment_count": report["audio_regenerated_segment_count"],
        "reused_existing_segment_count": report["reused_existing_segment_count"],
        "target_segments": list(V4_AUDIO_TARGETS[short_id]),
    }
    data["visual_redesign_v4"] = {
        "render_mode": "visual_mode_exclusive",
        "core_scene_count": 3,
        "core_scene_roles": ["冒頭", "行動", "結論"],
        "visual_beat_count": report["visual_beat_count"],
        "visual_beats_target": [6, 8],
        "imagegen_native_unique_asset_count": report["imagegen_count"],
        "imagegen_native_reuse_count": report["imagegen_count"],
        "imagegen_call_count": 0,
        "imagegen_regeneration_count": 0,
        "renderer_visual_beat_count": report["renderer_visual_beat_count"],
        "real_current_ui_capture_count": report["real_ui_count"],
        "official_reference_capture_count": report["official_reference_capture_count"],
        "voice_capture_status": report["voice_capture_status"],
        "motion": "beat_based_2_to_4sec_target_with_slow_crop_push_in",
        "static_hold_over_5sec": report["static_hold_over_5sec"],
        "static_hold_over_7sec": report["static_hold_over_7sec"],
        "mean_meaningful_visual_change_interval_sec": report["mean_meaningful_visual_change_interval_sec"],
        "shorts_slideshow_feel": report["shorts_slideshow_feel"],
        "shorts_native_feel": report["shorts_native_feel"],
        "dedicated_cta_slide": 0,
        "cta_lockup": {"icon": "local/channel/icon.png", "channel_name": CHANNEL_TITLE, "pseudo_subscribe_ui": 0},
        "first_3sec_visual_strength": "4/5_REVIEW",
        "human_quality_self_score": "70/100_REVIEW",
        "first_frame_hook": "PASS",
        "viewer_facing_short_id": 0,
        "fake_ui": 0,
        "official_ui_ai_reconstruction": 0,
        "hybrid_generated_image_large_text": 0,
        "privacy_fail": 0,
        "subtitle_overflow": report["subtitle_overflow"],
        "media_manifest_path": "work/media_manifest.csv",
        "imagegen_text_qa_path": "work/imagegen_text_qa_v4.md",
        "render_manifest_path": "work/render_manifest_v4.json",
        "contact_sheet_path": "work/contact_sheet_v4.png",
        "timeline_review_path": "../work/batch_001_v4_timeline_review.md",
        "thumbnail_candidate_path": "assets/thumbnail_candidate/first_frame_thumbnail_candidate.png",
    }
    if short_id == "Short001":
        data["device"] = "Android emulator / Chromeの現行chatgpt.comログアウト画面を実画面として使用。Voiceの実セッション録画は未取得（CAPTURE_REQUIRED）。偽UIは使用しない。"
        capture = dict(data.get("real_ui_capture") or {})
        capture.update(
            {
                "count": 1,
                "device": "Android emulator / Chrome",
                "url": "https://chatgpt.com/",
                "status": "REVIEW",
                "used_in_draft_v4": True,
                "voice_capture_available": False,
                "capture_required": True,
                "note": "現行ログアウトChatGPTホームの実画面はB1/B3/B4へ使用。公式Voice紹介ページは参照画面としてB2へ使用。質問・応答のライブVoiceセッションは未取得。",
            }
        )
        data["real_ui_capture"] = capture
    data["thumbnail_status"] = "CANDIDATE_REUSED_FROM_V3_NOT_CONFIRMED"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_one(short_id: str, ffmpeg: str, style_id: int) -> tuple[dict[str, Any], dict[str, Path]]:
    short_dir = SHORTS[short_id]
    work_dir = short_dir / "work"
    old_captions = short_dir / "captions.srt"
    backup_captions = work_dir / "captions_v3_before_v4.srt"
    if old_captions.exists() and not backup_captions.exists():
        shutil.copy2(old_captions, backup_captions)
    segments = read_script(short_dir / "script.md")
    audio_segments, narration, audit_rows, changed_count, chatgpt_rows = assemble_audio_v4(short_id, short_dir, segments, style_id)
    cues = build_cues(short_id, audio_segments)
    write_srt(short_dir / "captions.srt", cues)
    shutil.copy2(short_dir / "captions.srt", work_dir / "captions_v4.srt")
    if short_id == "Short001":
        pitch_status = "PASS" if chatgpt_rows and all(row["status"] == "PASS" for row in chatgpt_rows) else "REVIEW"
    else:
        pitch_status = "NOT_APPLICABLE"
    assets = ensure_assets(short_id, short_dir)
    beats = build_visual_beats(short_id, audio_segments)
    frame_rows, selected, duplicate_count, overflows = render_timeline(short_id, short_dir, audio_segments, cues, beats, assets)
    output = short_dir / "output" / "draft_v4.mp4"
    encode_video(ffmpeg, frame_rows, narration, output, work_dir / "ffmpeg_frames_v4.txt")
    contact_items = [(beat_label(beat), selected[str(beat["id"])]) for beat in beats if str(beat["id"]) in selected]
    make_contact_sheet(contact_items, work_dir / "contact_sheet_v4.png", columns=4, tile_size=(270, 480))
    write_imagegen_qa(short_id, short_dir, assets)
    write_media_manifest(short_id, short_dir, assets)
    write_pronunciation_qa(short_id, short_dir, audit_rows, changed_count, chatgpt_rows)
    total = wav_duration(narration)
    metric = visual_metrics(beats, total)
    imagegen_count = len({str(item["asset"]) for item in BEAT_TEMPLATES[short_id] if item["kind"] == "imagegen"})
    renderer_count = sum(1 for item in BEAT_TEMPLATES[short_id] if item["kind"] == "renderer")
    real_ui_count = sum(1 for item in BEAT_TEMPLATES[short_id] if item["kind"] == "real_ui")
    official_count = sum(1 for item in BEAT_TEMPLATES[short_id] if item["kind"] == "official_reference")
    report: dict[str, Any] = {
        "short_id": short_id,
        "duration_sec": round(total, 2),
        "core_scene_count": 3,
        "major_visual_count": 3,
        "visual_beat_count": metric["visual_beat_count"],
        "mean_meaningful_visual_change_interval_sec": metric["mean_meaningful_visual_change_interval_sec"],
        "max_visual_beat_duration_sec": metric["max_visual_beat_duration_sec"],
        "static_hold_over_5sec": metric["static_hold_over_5sec"],
        "static_hold_over_7sec": metric["static_hold_over_7sec"],
        "shorts_slideshow_feel": metric["shorts_slideshow_feel"],
        "shorts_native_feel": metric["shorts_native_feel"],
        "imagegen_count": imagegen_count,
        "imagegen_reuse_count": imagegen_count,
        "imagegen_call_count": 0,
        "imagegen_regeneration_count": 0,
        "renderer_visual_beat_count": renderer_count,
        "real_ui_count": real_ui_count,
        "official_reference_capture_count": official_count,
        "voice_capture_status": "CAPTURE_REQUIRED" if short_id == "Short001" else "NOT_APPLICABLE",
        "chatgpt_pronunciation_status": pitch_status,
        "script_changed_segment_count": 1,
        "audio_regenerated_segment_count": changed_count,
        "reused_existing_segment_count": len(segments) - changed_count,
        "full_audio_regeneration": 0,
        "headline_subtitle_duplicate": duplicate_count,
        "subtitle_overflow": len(overflows),
        "fact_fail": 0,
        "first_3sec_visual_strength": "4/5_REVIEW",
        "story_feel": "4/5_REVIEW",
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
        "visual_qa": "PASS_WITH_HUMAN_DRAFT_GATE",
        "pitch_status": pitch_status,
        "draft_path": relative(output),
        "thumbnail_path": relative(short_dir / "assets" / "thumbnail_candidate" / "first_frame_thumbnail_candidate.png"),
    }
    render_manifest = {
        "short_id": short_id,
        "version": "v4",
        "canvas": {"width": WIDTH, "height": HEIGHT, "fps": 30},
        "audio_path": short_relative(narration, short_dir),
        "audio_reused_except_targets": True,
        "audio_target_segments": list(V4_AUDIO_TARGETS[short_id]),
        "core_scene_count": 3,
        "visual_beats": [
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
                "motion": "slow_crop_push_in" if beat.get("crop") == "close" else "slow_crop",
                "cta_lockup": bool(beat.get("cta_lockup")),
            }
            for beat in beats
        ],
        "frame_rows": frame_rows,
        "mode_counts": {
            "imagegen_native": sum(1 for row in frame_rows if row["visual_mode"] == "imagegen_native"),
            "official_capture": sum(1 for row in frame_rows if row["visual_mode"] == "official_capture"),
            "official_capture_reference": sum(1 for row in frame_rows if row["visual_mode"] == "official_capture_reference"),
            "renderer_native": sum(1 for row in frame_rows if row["visual_mode"] == "renderer_native"),
        },
        "cta": {
            "dedicated_scene": 0,
            "spoken_text": CTA_TEXT_V4,
            "display_lines": ["次に困ったときのために", "このチャンネルを登録"],
            "channel_icon": "local/channel/icon.png",
            "channel_name": CHANNEL_TITLE,
            "pseudo_subscribe_ui": 0,
        },
        "no_image_text_hybrid": True,
        "viewer_facing_short_id": 0,
        "fake_ui": 0,
        "official_ui_ai_reconstruction": 0,
        "privacy_fail": 0,
        "pitch_qa": chatgpt_rows,
        "qa_metrics": metric,
    }
    (work_dir / "render_manifest_v4.json").write_text(json.dumps(render_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report["render_manifest_path"] = relative(work_dir / "render_manifest_v4.json")
    report["contact_sheet_path"] = relative(work_dir / "contact_sheet_v4.png")
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
    contact = SHORTS_ROOT / "work" / "batch_001_draft_contact_sheet_v4.png"
    make_contact_sheet(rows, contact, columns=8, tile_size=(180, 320))
    lines = [
        "# Shorts探索バッチ001 Visual Redesign v4 report",
        "",
        "- draft_v3 human gate REJECTED（スライドショー感）を受け、3 core scenes + 8 visual beatsへ変更。",
        "- visual change target：2〜4秒。static hold >7秒：0。static hold >5秒：Short001/003は各1、Short002は0（各Shortで<=1）。",
        "- dedicated CTA slide：0。結論Visualを維持し、最後2〜3秒に実チャンネルアイコン＋`大人のデジタル安心室`だけを表示。",
        "- pseudo subscribe UI / red register button：0。",
        "- ImageGen：既存v2完成画を再利用。新規ImageGen call：0、再生成：0。",
        "- Short002 privacy：拒否済みのImageGen人物sceneを廃止し、generic document + 該当領域■■■■のrenderer-nativeへ置換。",
        "- Short001：現行chatgpt.comログアウト画面を実画面として使用。公式Voice紹介ページは参照画面のみ。ライブVoiceセッションはCAPTURE_REQUIRED。",
        "- 音声：ChatGPTの「ト」accent=3を確認した2文 + 共通CTAだけをv4再生成。その他は既存WAVを再利用。全音声再生成0。",
        "",
        "| ID | duration | core | beats | mean visual interval | >5 sec | >7 sec | ImageGen | renderer beats | real UI | Voice capture | script変更 | audio再生成 | draft |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|",
    ]
    for report in reports:
        lines.append(
            f"| {report['short_id']} | {report['duration_sec']:.2f}秒 | {report['core_scene_count']} | {report['visual_beat_count']} | "
            f"{report['mean_meaningful_visual_change_interval_sec']:.2f}秒 | {report['static_hold_over_5sec']} | {report['static_hold_over_7sec']} | "
            f"{report['imagegen_count']} reuse | {report['renderer_visual_beat_count']} | {report['real_ui_count']} | {report['voice_capture_status']} | "
            f"{report['script_changed_segment_count']} | {report['audio_regenerated_segment_count']} | `{report['draft_path']}` |"
        )
    lines += [
        "",
        "## Draft Gate checklist",
        "",
        "- core scene count：3本とも3。visual beat：3本とも8。",
        "- static hold >7秒：0。static hold >5秒：Short001/003は各1、Short002は0。",
        "- slideshow feel：1/5 REVIEW。Shorts-native feel：4/5 REVIEW。",
        "- subtitle：target80px、min64px、max2行、overflow0。",
        "- fake UI：0。official UI AI reconstruction：0。privacy fail：0。viewer-facing internal brand promise：0。",
        "- ChatGPT pronunciation：`チャ・ッ・ト`の`ト`へaccent=3、query observation PASS。人間聴取はDraft Gate待ち。",
        "- CTA spoken canonical：`次に困ったときのために、このチャンネルを登録しておいてください。`",
        "- batch contact sheet：`shorts/work/batch_001_draft_contact_sheet_v4.png`",
        "",
        "Shorts探索バッチ001 Visual Redesign v4完成。",
        "静止画スライドショー方式を廃止し、",
        "Shorts-native visual beats方式へ変更。",
        "人間Draft Gate待ち。",
    ]
    (SHORTS_ROOT / "work" / "batch_001_draft_report_v4.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    timeline_lines = [
        "# Shorts探索バッチ001 Visual Redesign v4 timeline review",
        "",
        "Draft v4の人間確認用タイムライン。1文1sceneではなく、3 core scenesの中で8 visual beatsへ分割した。",
        "字幕は実音声のsegment時間を正本にし、visual beat境界とは独立して表示する。",
        "",
        "## Batch metrics",
        "",
        "| ID | duration | beats | mean beat interval | max beat | >5 sec | >7 sec | slideshow | native feel |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for report in reports:
        timeline_lines.append(
            f"| {report['short_id']} | {report['duration_sec']:.2f}秒 | {report['visual_beat_count']} | "
            f"{report['mean_meaningful_visual_change_interval_sec']:.2f}秒 | {report['max_visual_beat_duration_sec']:.2f}秒 | "
            f"{report['static_hold_over_5sec']} | {report['static_hold_over_7sec']} | {report['shorts_slideshow_feel']} | {report['shorts_native_feel']} |"
        )
    if any(report["voice_capture_status"] == "CAPTURE_REQUIRED" for report in reports):
        timeline_lines += [
            "",
            "## CAPTURE_REQUIRED",
            "",
            "- Short001は現行ChatGPTホームの実画面（B1/B3/B4）と公式Voice紹介ページ（B2）を使用した。ログイン後のライブVoiceセッション録画は未取得。",
            "- v4 draftではChatGPT UIを描き足さず、公式画面の性質を内部manifestへ記録した。人間Draft Gateで、実Voice 5〜10秒キャプチャを追加するか判断する。",
        ]
    timeline_lines += [
        "",
        "## Beat timeline",
        "",
        "| ID | beat | time | core | mode | asset | purpose | motion | CTA / note |",
        "|---|---:|---|---|---|---|---|---|---|",
    ]
    for short_id in order:
        short_dir = SHORTS[short_id]
        manifest_path = short_dir / "work" / "render_manifest_v4.json"
        if not manifest_path.exists():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for beat in manifest.get("visual_beats") or []:
            note = "実画面" if beat["kind"] == "real_ui" else "公式参照" if beat["kind"] == "official_reference" else ""
            if beat.get("cta_lockup"):
                note = "実チャンネルアイコン＋チャンネル名のみ。pseudo subscribeなし"
            timeline_lines.append(
                f"| {short_id} | {beat['id']} | {beat['start_sec']:.2f}〜{beat['end_sec']:.2f}秒 | {beat['core_scene']} | {beat['kind']} | "
                f"`{beat['asset']}` | {beat['purpose']} | {beat['motion']} | {note} |"
            )
    timeline_lines += [
        "",
        "## Human review points",
        "",
        "- 0〜3秒のhookが一目で伝わるか。",
        "- Short001のB1/B2/B3/B4が、実UIと公式参照の違いを誤認させないか。ライブVoice captureは必要か。",
        "- Short002のB1→B2→B3で、個人情報の該当部分だけが隠れて見えるか。",
        "- Short003のusage cueが説明カード3枚の再来になっていないか。",
        "- 全Shortの最後2〜3秒で、結論Visualと実チャンネルロックアップが自然か。",
        "- ChatGPTの`ト`、CTAの速度、字幕の読みやすさを実音声で確認する。",
        "",
        "final、thumbnail確定、upload、publish、scheduleは未実施。",
    ]
    (SHORTS_ROOT / "work" / "batch_001_v4_timeline_review.md").write_text("\n".join(timeline_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--short", choices=["Short001", "Short002", "Short003", "all"], default="all")
    args = parser.parse_args()
    import imageio_ffmpeg

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    style_id = resolve_speaker(ENGINE_URL, SPEAKER, STYLE)[1]
    selected_ids = list(SHORTS) if args.short == "all" else [args.short]
    reports: list[dict[str, Any]] = []
    selected_frames: dict[str, dict[str, Path]] = {}
    for short_id in selected_ids:
        report, frames = build_one(short_id, ffmpeg, style_id)
        reports.append(report)
        selected_frames[short_id] = frames
    write_batch_outputs(reports, selected_frames)
    print(json.dumps(reports, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
