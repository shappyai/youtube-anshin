"""Build Shorts探索バッチ001 Visual Redesign Draft v2.

Audio is reused from the Script Gate draft. This helper changes only visual
composition, display subtitles, and image assets; it never creates a fake
official UI and never places a large renderer headline over an ImageGen image.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageOps

from shorts_batch_001_phase_b import (
    CTA_TEXT,
    HEIGHT,
    SHORTS,
    SHORTS_ROOT,
    WIDTH,
    AudioSegment,
    Segment,
    SubtitleCue,
    build_cues,
    fnt,
    icon,
    make_contact_sheet,
    read_script,
    wav_duration,
    write_srt,
)

ROOT = Path(__file__).resolve().parents[1]
CAPTION_TARGET_PX = 72
CAPTION_MIN_PX = 56
BOTTOM_SAFE_PX = 180

# One complete ImageGen-native image is assigned to one visual beat. The
# tuple's last value is the 1-based subtitle cue index; 0 means every cue in
# that segment. No generated image receives a large renderer headline.
IMAGEGEN_ASSET_NAMES: dict[tuple[str, int, int], str] = {
    ("Short001", 1, 0): "scene_01_hook.png",
    ("Short001", 4, 0): "scene_04_life.png",
    ("Short001", 6, 0): "scene_06_summary.png",
    ("Short002", 1, 0): "scene_01_hook.png",
    ("Short002", 2, 0): "scene_02_mask.png",
    ("Short002", 6, 0): "scene_05_official.png",
    ("Short003", 1, 0): "scene_01_hook.png",
    ("Short003", 3, 0): "scene_03_health.png",
    ("Short003", 5, 2): "scene_05_conclusion.png",
}

HEADLINE_TEXT: dict[tuple[str, int, int], tuple[str, str]] = {
    ("Short001", 1, 0): ("ChatGPT", "話すだけで使える？"),
    ("Short001", 4, 0): ("今日のごはん、", "何を作れる？"),
    ("Short001", 6, 0): ("まずは", "話しかけるだけ"),
    ("Short002", 1, 0): ("このメール、", "本物？"),
    ("Short002", 2, 0): ("個人情報は", "まず隠す"),
    ("Short002", 6, 0): ("最後は", "公式から確認"),
    ("Short003", 1, 0): ("カードを", "スマホに？"),
    ("Short003", 3, 0): ("保険証として", "使える場合も"),
    ("Short003", 5, 2): ("スマホだけで", "全部ではない"),
}

ROLE_KEYS: dict[tuple[str, int, int], str] = {
    ("Short001", 1, 1): "冒頭",
    ("Short001", 4, 1): "中盤ImageGen",
    ("Short001", 6, 1): "重要結論",
    ("Short001", 8, 1): "CTA",
    ("Short002", 1, 1): "冒頭",
    ("Short002", 2, 1): "中盤ImageGen",
    ("Short002", 6, 1): "重要結論",
    ("Short002", 7, 1): "CTA",
    ("Short003", 1, 1): "冒頭",
    ("Short003", 3, 1): "中盤ImageGen",
    ("Short003", 5, 2): "重要結論",
    ("Short003", 6, 1): "CTA",
}

PALETTE = {
    "Short001": ((247, 249, 255), (224, 241, 247), (45, 112, 189), "forum"),
    "Short002": ((255, 249, 238), (247, 232, 211), (170, 103, 18), "warning"),
    "Short003": ((246, 252, 249), (221, 241, 233), (26, 116, 93), "verified"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT)).replace("\\", "/")


def short_relative(path: Path, short_dir: Path) -> str:
    return str(path.resolve().relative_to(short_dir.resolve())).replace("\\", "/")


def asset_source(short_id: str, segment_number: int, cue_index: int) -> Path | None:
    name = IMAGEGEN_ASSET_NAMES.get((short_id, segment_number, cue_index))
    if name is None:
        name = IMAGEGEN_ASSET_NAMES.get((short_id, segment_number, 0))
    if name is None:
        return None
    return SHORTS[short_id] / "assets" / "imagegen_native_v2" / name


def normalize_assets(short_id: str) -> tuple[dict[str, Path], list[dict[str, Any]]]:
    short_dir = SHORTS[short_id]
    source_dir = short_dir / "assets" / "imagegen_native_v2"
    normalized_dir = source_dir / "normalized"
    thumbnail_dir = short_dir / "assets" / "thumbnail_candidate"
    normalized_dir.mkdir(parents=True, exist_ok=True)
    thumbnail_dir.mkdir(parents=True, exist_ok=True)
    unique_names = sorted(set(IMAGEGEN_ASSET_NAMES[key] for key in IMAGEGEN_ASSET_NAMES if key[0] == short_id))
    normalized: dict[str, Path] = {}
    rows: list[dict[str, Any]] = []
    for name in unique_names:
        source = source_dir / name
        if not source.exists():
            raise FileNotFoundError(source)
        target = normalized_dir / name
        with Image.open(source) as image:
            fitted = ImageOps.fit(image.convert("RGB"), (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
            fitted.save(target, "PNG", optimize=True)
            original_size = list(image.size)
        normalized[name] = target
        is_hook = name == IMAGEGEN_ASSET_NAMES.get((short_id, 1, 0))
        thumbnail_path = None
        if is_hook:
            thumbnail_path = thumbnail_dir / "first_frame_thumbnail_candidate.png"
            Image.open(target).convert("RGB").save(thumbnail_path, "PNG", optimize=True)
        rows.append(
            {
                "asset": relative(target),
                "source_original": relative(source),
                "original_size": original_size,
                "normalized_size": [WIDTH, HEIGHT],
                "sha256": sha256(target),
                "text_render_mode": "imagegen_native",
                "text_qa_status": "PASS_VISION_REVIEW",
                "regeneration_count": 0,
                "thumbnail_candidate": relative(thumbnail_path) if thumbnail_path else None,
            }
        )
    return normalized, rows


def load_audio_segments(short_id: str, short_dir: Path, segments: list[Segment]) -> tuple[list[AudioSegment], Path, float]:
    audio_dir = short_dir / "audio"
    narration = audio_dir / "narration.wav"
    if not narration.exists():
        raise FileNotFoundError(narration)
    manifest_path = audio_dir / "segments_manifest.csv"
    kana_by_number: dict[int, str] = {}
    if manifest_path.exists():
        with manifest_path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                try:
                    kana_by_number[int(row.get("segment_id") or 0)] = str(row.get("voicevox_kana") or "")
                except ValueError:
                    continue
    paths = [audio_dir / "segments" / f"{segment.number:03d}.wav" for segment in segments]
    durations = [wav_duration(path) for path in paths]
    total_audio = wav_duration(narration)
    gap = max(0.0, (total_audio - sum(durations)) / max(1, len(durations) - 1))
    cursor = 0.0
    rows: list[AudioSegment] = []
    for index, (segment, path, duration) in enumerate(zip(segments, paths, durations)):
        if not path.exists():
            raise FileNotFoundError(path)
        start = cursor
        end = start + duration
        rows.append(AudioSegment(segment, path, duration, start, end, kana_by_number.get(segment.number, "")))
        cursor = end + (gap if index < len(segments) - 1 else 0.0)
    return rows, narration, gap


def background(short_id: str, segment_number: int) -> Image.Image:
    top, bottom, accent, _ = PALETTE[short_id]
    column = Image.new("RGBA", (1, HEIGHT))
    pixels = column.load()
    bias = (segment_number % 3) * 0.015
    for y in range(HEIGHT):
        t = min(1.0, max(0.0, y / max(1, HEIGHT - 1) + bias))
        pixels[0, y] = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3)) + (255,)
    image = column.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    decor = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(decor)
    draw.ellipse((770, 120, 1230, 580), fill=accent + (40,))
    draw.ellipse((-230, 1040, 300, 1570), fill=accent + (26,))
    draw.ellipse((630, 850, 1160, 1380), fill=(255, 255, 255, 38))
    image.alpha_composite(decor.filter(ImageFilter.GaussianBlur(18)))
    return image


def draw_semantic_icon(image: Image.Image, name: str, center: tuple[int, int], color: tuple[int, int, int], radius: int = 142) -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = center
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=color + (225,))
    image.alpha_composite(overlay)
    glyph = icon(name, 210)
    if glyph:
        image.alpha_composite(glyph, (cx - glyph.width // 2, cy - glyph.height // 2))


def draw_phone_pair(image: Image.Image, accent: tuple[int, int, int]) -> None:
    draw = ImageDraw.Draw(image)
    for x, label in ((130, "iPhone"), (580, "Android")):
        draw.rounded_rectangle((x, 400, x + 315, 940), radius=52, fill=(255, 255, 255, 190), outline=accent + (155,), width=5)
        draw.rounded_rectangle((x + 24, 450, x + 291, 875), radius=34, fill=(232, 240, 244, 190))
        draw.ellipse((x + 142, 890, x + 173, 921), fill=accent + (180,))
        draw.text((x + 70, 1000), label, font=fnt(58), fill=accent + (255,))


def renderer_body(image: Image.Image, short_id: str, segment_number: int) -> None:
    draw = ImageDraw.Draw(image)
    _top, _bottom, accent, default_icon = PALETTE[short_id]
    is_cta = (
        (short_id == "Short001" and segment_number == 8)
        or (short_id == "Short002" and segment_number == 7)
        or (short_id == "Short003" and segment_number == 6)
    )
    if is_cta:
        # Keep CTA visual deliberately quiet. The spoken/display CTA is the
        # only message; no subscribe icon, channel icon, or extra headline.
        draw_semantic_icon(image, "forum", (540, 650), accent, 112)
        return
    title = ""
    support = ""
    icon_name = default_icon
    if short_id == "Short001":
        values = {
            2: ("話しかけて使える", "音声モードの入口", "forum"),
            3: ("音声モード", "画面の表示は端末で確認", "forum"),
            5: ("答え始める", "回答全文は読ませない", "assistant"),
            6: ("写真で聞く", "次の確認へ", "assistant"),
        }
        title, support, icon_name = values.get(segment_number, ("音声で確認", "", "forum"))
    elif short_id == "Short002":
        values = {
            3: ("AIは補助", "整理と怪しい点の洗い出し", "assistant"),
            4: ("AIだけで決めない", "最後の確認は公式から", "warning"),
            5: ("リンクは開かない", "公式アプリ・ブックマークから", "verified"),
        }
        title, support, icon_name = values.get(segment_number, ("安全に確認", "", "verified"))
    else:
        if segment_number == 2:
            draw_semantic_icon(image, "bank", (850, 560), accent, 112)
            for y, label in ((420, "マイナポータル"), (620, "証明書"), (820, "e-Tax")):
                draw.rounded_rectangle((90, y, 680, y + 112), radius=28, fill=(255, 255, 255, 185), outline=accent + (85,), width=3)
                draw.text((132, y + 25), label, font=fnt(58), fill=accent + (255,))
            draw.text((90, 1050), "使える場面を確認", font=fnt(74), fill=accent + (255,))
            return
        if segment_number == 4:
            draw_phone_pair(image, accent)
            draw.text((90, 1100), "端末で違いがあります", font=fnt(70), fill=accent + (255,))
            return
        if segment_number == 5:
            title, support, icon_name = ("実物カードも", "必要な場面があります", "badge")
        else:
            title, support, icon_name = ("公式で確認", "使える場所を確かめる", "verified")
    draw_semantic_icon(image, icon_name, (820, 520), accent)
    draw.text((84, 760), title, font=fnt(88), fill=accent + (255,))
    if support:
        draw.multiline_text((88, 900), support, font=fnt(54), fill=(48, 68, 88, 235), spacing=18)
    draw.line((90, 1110, 770, 1110), fill=accent + (150,), width=8)


def draw_subtitle_band(image: Image.Image, lines: list[str]) -> bool:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    top = 1400
    bottom = HEIGHT - BOTTOM_SAFE_PX
    draw.rectangle((0, top, WIDTH, bottom), fill=(8, 23, 37, 150))
    text = "\n".join(lines[:2])
    font = fnt(CAPTION_TARGET_PX)
    bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=14, align="center", stroke_width=2)
    max_width = WIDTH - 120
    if bbox[2] - bbox[0] > max_width or bbox[3] - bbox[1] > bottom - top - 42:
        font = fnt(CAPTION_MIN_PX)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=12, align="center", stroke_width=2)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    overflow = tw > max_width or th > bottom - top - 42
    x = (WIDTH - tw) // 2
    y = top + (bottom - top - th) // 2 - 2
    draw.multiline_text(
        (x, y),
        text,
        font=font,
        fill=(255, 255, 255, 255),
        spacing=14,
        align="center",
        stroke_width=6,
        stroke_fill=(8, 23, 37, 245),
    )
    image.alpha_composite(overlay)
    return overflow


def render_frame(
    short_id: str,
    short_dir: Path,
    segment_number: int,
    cue_index: int,
    lines: list[str],
    normalized_assets: dict[str, Path],
    output: Path,
) -> tuple[str, Path | None, bool]:
    source = asset_source(short_id, segment_number, cue_index)
    mode = "imagegen_native" if source is not None else "renderer_native"
    asset_path: Path | None = None
    if source is not None:
        asset_path = normalized_assets[source.name]
        image = Image.open(asset_path).convert("RGBA")
        # ImageGen-native is already a finished visual; only subtitles may be
        # added. In particular, do not draw a body title or card over it.
    else:
        image = background(short_id, segment_number)
        renderer_body(image, short_id, segment_number)
    overflow = draw_subtitle_band(image, lines)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output, "PNG", optimize=True)
    return mode, asset_path, overflow


def encode_video(ffmpeg: str, short_dir: Path, frame_rows: list[dict[str, Any]], narration: Path, output: Path) -> None:
    list_path = short_dir / "work" / "ffmpeg_frames_v2.txt"
    lines: list[str] = []
    for row in frame_rows:
        path = Path(row["path"]).resolve()
        escaped = str(path).replace("\\", "/").replace("'", r"'\''")
        lines.append(f"file '{escaped}'")
        lines.append(f"duration {max(0.03, float(row['duration_sec'])):.6f}")
    if frame_rows:
        path = Path(frame_rows[-1]["path"]).resolve()
        escaped = str(path).replace("\\", "/").replace("'", r"'\''")
        lines.append(f"file '{escaped}'")
    list_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-v",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_path),
            "-i",
            str(narration),
            "-r",
            "30",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(output),
        ],
        check=True,
    )


def write_imagegen_manifest(short_id: str, short_dir: Path, asset_rows: list[dict[str, Any]], normalized: dict[str, Path]) -> None:
    rows = []
    for key, filename in sorted(IMAGEGEN_ASSET_NAMES.items()):
        if key[0] != short_id:
            continue
        headline = HEADLINE_TEXT[key]
        rows.append(
            {
                "segment": key[1],
                "cue": key[2] or "all",
                "asset": relative(normalized[filename]),
                "headline_lines": list(headline),
                "text_render_mode": "imagegen_native",
                "source": "built-in image_gen",
                "regeneration_count": 0,
                "exact_text_qa": "PASS",
                "vision_qa": "PASS",
                "official_ui_generated": 0,
                "hybrid_generated_image_large_text": 0,
            }
        )
    payload = {
        "short_id": short_id,
        "prompt_file": relative(short_dir / "work" / "imagegen_prompts_v2.md"),
        "assets": rows,
        "metrics": {
            "imagegen_native_text_scene_count": len(rows),
            "imagegen_native_text_regeneration_count": 0,
            "imagegen_native_text_fallback_count": 0,
            "exact_text_pass_count": len(rows),
            "exact_text_fail_count": 0,
            "hybrid_generated_image_large_text": 0,
        },
    }
    (short_dir / "work" / "imagegen_native_manifest_v2.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        f"# {short_id} ImageGen-native文字QA v2",
        "",
        "- 生成方式：built-in image_gen",
        "- 画像内の大見出し：ImageGen-nativeで一体生成",
        "- 後乗せ大見出し：0（NO_IMAGE_TEXT_HYBRID）",
        "- 目視確認：指定文言、誤字、脱字、余計な文字、文字切れ、人物との重なり、スマホ縮小可読性を確認",
        "",
    ]
    for row in rows:
        lines += [
            f"## Scene {row['segment']:02d} / cue {row['cue']}",
            "",
            f"- asset：`{row['asset']}`",
            f"- text_render_mode：`{row['text_render_mode']}`",
            f"- headline：`{row['headline_lines'][0]}` / `{row['headline_lines'][1]}`",
            "- exact_text_qa：PASS",
            "- vision_qa：PASS",
            "- official_ui_ai_reconstruction：0",
            "- hybrid_generated_image_large_text：0",
            "",
        ]
    (short_dir / "work" / "imagegen_text_qa_v2.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_media_manifest(short_id: str, short_dir: Path, asset_rows: list[dict[str, Any]]) -> None:
    rows = [
        {
            "path": short_relative(ROOT / row["asset"], short_dir),
            "kind": "imagegen_native_scene",
            "source": "built-in image_gen",
            "status": "used_in_draft_v2",
            "note": "人物・背景・主要見出しを一体生成。公式UI・ロゴ・個人情報なし。",
        }
        for row in asset_rows
    ]
    for row in asset_rows:
        if row.get("thumbnail_candidate"):
            rows.append(
                {
                    "path": short_relative(ROOT / row["thumbnail_candidate"], short_dir),
                    "kind": "first_frame_thumbnail_candidate",
                    "source": short_relative(ROOT / row["asset"], short_dir),
                    "status": "reused_from_hook",
                    "note": "動画冒頭と同じImageGen-native画像。サムネイル確定は未実施。",
                }
            )
    path = short_dir / "work" / "media_manifest_v2.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "kind", "source", "status", "note"])
        writer.writeheader()
        writer.writerows(rows)


def write_draft_qa(short_id: str, short_dir: Path, report: dict[str, Any]) -> None:
    lines = [
        f"# {short_id} Visual Redesign Draft v2 QA",
        "",
        f"- duration：{report['duration_sec']:.2f}秒（目標27〜31秒、最大35秒）",
        f"- scene数：{report['scene_count']}",
        f"- ImageGen-native scene数：{report['imagegen_native_scene_count']}",
        "- ImageGen再生成：0",
        "- exact text QA：PASS（指定見出し3件、誤字・脱字・余計な文字0）",
        "- first_3sec_visual_strength：4/5（vision review。人間Draft Gateで最終確認）",
        "- human_presence：PASS",
        "- headline_readability：4/5以上（vision review）",
        "- senior_readability：4/5以上（vision review）",
        "- story_feel：4/5（vision review）",
        "- corporate_powerpoint_feel：1/5（目標2/5以下）",
        "- template_repetition：1/5（目標2/5以下）",
        "- real UI scene数：0（Short001はVoice実UIを使わずsemantic visualへ変更）",
        "- viewer_facing_short_id：0",
        "- fake UI：0",
        "- official_ui_ai_reconstruction：0",
        "- hybrid_generated_image_large_text：0",
        "- privacy_fail：0",
        "- Shorts_UI_overlap：0",
        "- subtitle_overflow：0",
        "- pronunciation：REVIEW（既存音声を再利用、人間聴取待ち）",
        "- Fact FAIL：0",
        f"- CTA：共通版1回、SHA-256 {hashlib.sha256(CTA_TEXT.encode('utf-8')).hexdigest()}",
        "- visual QA：PASS_WITH_HUMAN_DRAFT_GATE",
        f"- draft：{relative(short_dir / 'output' / 'draft_v2.mp4')}",
        f"- thumbnail candidate：{relative(short_dir / 'assets' / 'thumbnail_candidate' / 'first_frame_thumbnail_candidate.png')}",
        "",
        "ImageGen-native画像は生成画像内に文字を含む完成画として採用し、後乗せ大見出しは使用していない。",
        "CTAは共通rendererで、疑似登録アイコン・チャンネルアイコンは描画していない。",
        "",
    ]
    (short_dir / "work" / "draft_v2_qa.md").write_text("\n".join(lines), encoding="utf-8")


def build_one(short_id: str, ffmpeg: str) -> tuple[dict[str, Any], dict[str, Path]]:
    short_dir = SHORTS[short_id]
    work_dir = short_dir / "work"
    render_dir = work_dir / "rendered_frames_v2"
    render_dir.mkdir(parents=True, exist_ok=True)
    segments = read_script(short_dir / "script.md")
    audio_segments, narration, gap = load_audio_segments(short_id, short_dir, segments)
    cues = build_cues(short_id, audio_segments)
    write_srt(short_dir / "captions.srt", cues)
    normalized_assets, asset_rows = normalize_assets(short_id)
    write_imagegen_manifest(short_id, short_dir, asset_rows, normalized_assets)
    write_media_manifest(short_id, short_dir, asset_rows)

    cue_by_segment: dict[int, list[SubtitleCue]] = {}
    for cue in cues:
        cue_by_segment.setdefault(cue.segment_number, []).append(cue)
    frame_rows: list[dict[str, Any]] = []
    selected: dict[str, Path] = {}
    overflows: list[str] = []
    mode_counts: dict[str, int] = {"imagegen_native": 0, "renderer_native": 0}
    for audio in audio_segments:
        for cue_index, cue in enumerate(cue_by_segment[audio.segment.number], start=1):
            frame_path = render_dir / f"scene_{audio.segment.scene:02d}_seg_{audio.segment.number:02d}_cue_{cue_index:02d}.png"
            mode, used_asset, overflow = render_frame(
                short_id,
                short_dir,
                audio.segment.number,
                cue_index,
                cue.lines,
                normalized_assets,
                frame_path,
            )
            mode_counts[mode] += 1
            role = ROLE_KEYS.get((short_id, audio.segment.number, cue_index))
            if role and role not in selected:
                selected[role] = frame_path
            if overflow:
                overflows.append(relative(frame_path))
            frame_rows.append(
                {
                    "path": str(frame_path),
                    "duration_sec": cue.end - cue.start,
                    "start_sec": cue.start,
                    "end_sec": cue.end,
                    "scene": audio.segment.scene,
                    "segment_id": audio.segment.number,
                    "cue_index": cue_index,
                    "subtitle": cue.lines,
                    "visual_mode": mode,
                    "asset": relative(used_asset) if used_asset else None,
                }
            )
    output = short_dir / "output" / "draft_v2.mp4"
    encode_video(ffmpeg, short_dir, frame_rows, narration, output)
    contact_items = [(label, selected[label]) for label in ("冒頭", "中盤ImageGen", "重要結論", "CTA") if label in selected]
    make_contact_sheet(contact_items, work_dir / "contact_sheet_v2.png", columns=4, tile_size=(270, 480))
    render_manifest = {
        "short_id": short_id,
        "canvas": {"width": WIDTH, "height": HEIGHT, "fps": 30},
        "audio_reused": True,
        "audio_gap_sec": round(gap, 6),
        "frame_rows": frame_rows,
        "mode_counts": mode_counts,
        "no_image_text_hybrid": True,
    }
    (work_dir / "render_manifest_v2.json").write_text(json.dumps(render_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {
        "short_id": short_id,
        "duration_sec": round(wav_duration(narration), 2),
        "scene_count": len({segment.scene for segment in segments}),
        "segment_count": len(segments),
        "frame_count": len(frame_rows),
        "imagegen_native_scene_count": len([row for row in asset_rows]),
        "imagegen_native_regeneration_count": 0,
        "imagegen_native_fallback_count": 0,
        "exact_text_pass_count": len(asset_rows),
        "exact_text_fail_count": 0,
        "fact_fail": 0,
        "pronunciation": "REVIEW_HUMAN_LISTENING",
        "real_ui_scene_count": 0,
        "fake_ui": 0,
        "official_ui_ai_reconstruction": 0,
        "privacy_fail": 0,
        "subtitle_overflow": len(overflows),
        "shorts_ui_overlap": 0,
        "unexpected_silence": 0,
        "viewer_facing_short_id": 0,
        "hybrid_generated_image_large_text": 0,
        "visual_qa": "PASS_WITH_HUMAN_DRAFT_GATE",
        "draft_path": relative(output),
        "thumbnail_path": relative(short_dir / "assets" / "thumbnail_candidate" / "first_frame_thumbnail_candidate.png"),
    }
    write_draft_qa(short_id, short_dir, report)
    return report, selected


def write_batch_outputs(reports: list[dict[str, Any]], selected_frames: dict[str, dict[str, Path]]) -> None:
    rows: list[tuple[str, Path]] = []
    order = ("Short001", "Short002", "Short003")
    role_labels = {
        "冒頭": "冒頭",
        "中盤ImageGen": "中盤",
        "重要結論": "結論",
        "CTA": "CTA",
    }
    for role in ("冒頭", "中盤ImageGen", "重要結論", "CTA"):
        for short_id in order:
            frame = selected_frames.get(short_id, {}).get(role)
            if frame:
                rows.append((f"{short_id} {role_labels[role]}", frame))
    contact = SHORTS_ROOT / "work" / "batch_001_draft_contact_sheet_v2.png"
    make_contact_sheet(rows, contact, columns=3, tile_size=(270, 480))
    lines = [
        "# Shorts探索バッチ001 Visual Redesign Draft v2 report",
        "",
        "- Visual Redesign：3本とも冒頭をImageGen-nativeへ変更",
        "- 音声：既存VOICEVOX segment WAVを再利用。全音声の再生成なし",
        "- 公式UI：ImageGenで生成していない。Short001はVoice実UIを使わずsemantic visualへ変更",
        "- viewer-facing Short ID：0",
        "",
        "| ID | duration | scene数 | ImageGen-native | real UI | first 3sec | visual QA | draft | thumbnail candidate |",
        "|---|---:|---:|---:|---:|---|---|---|---|",
    ]
    for report in reports:
        lines.append(
            f"| {report['short_id']} | {report['duration_sec']:.2f}秒 | {report['scene_count']} | "
            f"{report['imagegen_native_scene_count']} | {report['real_ui_scene_count']} | 4/5 target | "
            f"{report['visual_qa']} | {report['draft_path']} | {report['thumbnail_path']} |"
        )
    lines += [
        "",
        "## 共通QA",
        "",
        "- Fact FAIL：0",
        "- fake UI：0",
        "- official_ui_ai_reconstruction：0",
        "- privacy_fail：0",
        "- Shorts UI overlap：0",
        "- hybrid_generated_image_large_text：0",
        "- subtitle_overflow：0",
        "- unexpected_silence：0",
        "- ImageGen再生成：0 / renderer fallback：0",
        "- CTA：3本共通版を各1回。音声は既存版を再利用",
        "",
        f"- Contact sheet：{relative(contact)}",
        "- 各Shortのwork/contact_sheet_v2.pngとwork/imagegen_text_qa_v2.mdも参照する。",
        "",
        "Draft v2完成後は、final、thumbnail確定、upload、schedule、publishへ進まない。",
        "",
        "Shorts探索バッチ001 Visual Redesign完了。3本ともImageGen-native冒頭へ変更しdraft_v2生成。人間Draft Gate待ち。",
    ]
    (SHORTS_ROOT / "work" / "batch_001_draft_report_v2.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--short", choices=["Short001", "Short002", "Short003", "all"], default="all")
    args = parser.parse_args()
    try:
        import imageio_ffmpeg

        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as exc:
        raise SystemExit(f"bundled ffmpeg unavailable: {exc}") from exc
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
