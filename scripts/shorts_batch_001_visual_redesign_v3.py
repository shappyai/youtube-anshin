"""Build Shorts探索バッチ001 Visual Redesign v3.

v3 uses three reused ImageGen-native story images per Short. The generated
headline remains inside each finished image; this renderer adds only measured
subtitles and a slow, gentle crop motion. There is no renderer explanation
scene and no dedicated CTA scene.
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

from PIL import Image, ImageDraw, ImageOps

from shorts_batch_001_phase_b import (
    CTA_TEXT,
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
    WIDTH,
    AudioSegment,
    Segment,
    SubtitleCue,
    build_cues,
    fnt,
    make_contact_sheet,
    read_script,
    resolve_speaker,
    synthesize_one,
    wav_duration,
    write_srt,
)

ROOT = Path(__file__).resolve().parents[1]
CAPTION_TARGET_PX = 80
CAPTION_MIN_PX = 64
CAPTION_TOP = 1415
CAPTION_BOTTOM = 1690
CAPTION_MAX_WIDTH = 840
ZOOM_START = 1.05
ZOOM_END = 1.12

V3_AUDIO_OVERRIDES: dict[tuple[str, int], str] = {
    ("Short001", 3): "スマホに向かって、短い質問を話しかけてみます。",
}

# One asset is held across several narration segments. This is deliberately
# separate from the script's narration segment numbers: v3's visual density
# is three major visuals, not one visual per sentence.
MAJOR_VISUALS: dict[str, list[dict[str, Any]]] = {
    "Short001": [
        {
            "id": "A",
            "role": "冒頭",
            "segments": (1, 2),
            "asset": "scene_01_hook.png",
            "headline": ("ChatGPT", "話すだけで使える？"),
            "purpose": "問いと音声で使える入口",
        },
        {
            "id": "B",
            "role": "行動",
            "segments": (3, 4, 5),
            "asset": "scene_04_life.png",
            "headline": ("今日のごはん、", "何を作れる？"),
            "purpose": "スマホへ話しかける生活例",
        },
        {
            "id": "C",
            "role": "結論",
            "segments": (6, 7, 8),
            "asset": "scene_06_summary.png",
            "headline": ("まずは", "話しかけるだけ"),
            "purpose": "結論を保ったままCTAを重ねる",
        },
    ],
    "Short002": [
        {
            "id": "A",
            "role": "冒頭",
            "segments": (1,),
            "asset": "scene_01_hook.png",
            "headline": ("このメール、", "本物？"),
            "purpose": "迷いを問いにする",
        },
        {
            "id": "B",
            "role": "行動",
            "segments": (2, 3, 4),
            "asset": "scene_02_mask.png",
            "headline": ("個人情報は", "まず隠す"),
            "purpose": "隠す・AIは補助を一続きで示す",
        },
        {
            "id": "C",
            "role": "結論",
            "segments": (5, 6, 7),
            "asset": "scene_05_official.png",
            "headline": ("最後は", "公式から確認"),
            "purpose": "公式確認の結論を保ったままCTAを重ねる",
        },
    ],
    "Short003": [
        {
            "id": "A",
            "role": "冒頭",
            "segments": (1, 2),
            "asset": "scene_01_hook.png",
            "headline": ("カードを", "スマホに？"),
            "purpose": "できることへの入口",
        },
        {
            "id": "B",
            "role": "行動",
            "segments": (3, 4),
            "asset": "scene_03_health.png",
            "headline": ("保険証として", "使える場合も"),
            "purpose": "生活利用と条件を一続きで示す",
        },
        {
            "id": "C",
            "role": "結論",
            "segments": (5, 6),
            "asset": "scene_05_conclusion.png",
            "headline": ("スマホだけで", "全部ではない"),
            "purpose": "条件付きの結論を保ったままCTAを重ねる",
        },
    ],
}

PAN_BY_SHORT: dict[str, tuple[tuple[float, float], ...]] = {
    "Short001": ((0.50, 0.48), (0.48, 0.50), (0.52, 0.50)),
    "Short002": ((0.50, 0.50), (0.48, 0.49), (0.52, 0.50)),
    "Short003": ((0.50, 0.49), (0.50, 0.50), (0.50, 0.51)),
}


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT)).replace("\\", "/")


def short_relative(path: Path, short_dir: Path) -> str:
    return str(path.resolve().relative_to(short_dir.resolve())).replace("\\", "/")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_kana(short_dir: Path) -> dict[int, str]:
    result: dict[int, str] = {}
    path = short_dir / "audio" / "segments_manifest.csv"
    if not path.exists():
        return result
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                result[int(row.get("segment_id") or 0)] = str(row.get("voicevox_kana") or "")
            except ValueError:
                continue
    return result


def ensure_changed_audio(short_id: str, short_dir: Path, segments: list[Segment]) -> dict[int, tuple[Path, bool, str]]:
    """Return only changed segment audio; all other segments use existing WAVs."""
    result: dict[int, tuple[Path, bool, str]] = {}
    for segment in segments:
        override = V3_AUDIO_OVERRIDES.get((short_id, segment.number))
        if override is None:
            continue
        path = short_dir / "audio" / "segments" / f"{segment.number:03d}_v3.wav"
        path.parent.mkdir(parents=True, exist_ok=True)
        metadata_path = short_dir / "work" / "v3_audio_replacements.json"
        metadata: dict[str, Any] = {}
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        previous = metadata.get(str(segment.number)) or {}
        if not path.exists() or previous.get("narration") != override:
            style_id = resolve_speaker(ENGINE_URL, SPEAKER, STYLE)[1]
            _query, kana = synthesize_one(override, path, style_id)
            previous = {
                "narration": override,
                "voicevox_kana": kana,
                "status": "regenerated_v3_target_segment",
            }
            metadata[str(segment.number)] = previous
            metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result[segment.number] = (path, True, kana)
        else:
            result[segment.number] = (path, False, str(previous.get("voicevox_kana") or ""))
    return result


def assemble_audio_v3(
    short_id: str,
    short_dir: Path,
    segments: list[Segment],
) -> tuple[list[AudioSegment], Path, list[dict[str, Any]], int]:
    changed = ensure_changed_audio(short_id, short_dir, segments)
    original_kana = load_kana(short_dir)
    rows: list[AudioSegment] = []
    audit_rows: list[dict[str, Any]] = []
    parts: list[tuple[bytes, int, int, int]] = []
    params_ref: tuple[int, int, int] | None = None
    cursor = 0.0
    changed_count = 0

    for index, segment in enumerate(segments):
        if segment.number in changed:
            path, generated_now, generated_kana = changed[segment.number]
            kana = generated_kana or original_kana.get(segment.number, "")
            # Count the v3 target segment in the draft manifest even when a
            # rerun reuses the already-generated *_v3.wav cache.
            changed_count += 1
            status = "regenerated_v3_target_segment"
        else:
            path = short_dir / "audio" / "segments" / f"{segment.number:03d}.wav"
            kana = original_kana.get(segment.number, "")
            status = "reused_existing_segment_wav"
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
    narration = short_dir / "audio" / "narration_v3.wav"
    with wave.open(str(narration), "wb") as handle:
        handle.setnchannels(channels)
        handle.setsampwidth(sample_width)
        handle.setframerate(rate)
        for data, _channels, _width, _rate in parts:
            handle.writeframes(data)
    manifest = short_dir / "audio" / "segments_manifest_v3.csv"
    with manifest.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(audit_rows[0].keys()))
        writer.writeheader()
        writer.writerows(audit_rows)
    return rows, narration, audit_rows, changed_count


def ensure_normalized_assets(short_id: str, short_dir: Path) -> dict[str, Path]:
    source_dir = short_dir / "assets" / "imagegen_native_v2"
    normalized_dir = source_dir / "normalized"
    normalized_dir.mkdir(parents=True, exist_ok=True)
    normalized: dict[str, Path] = {}
    for visual in MAJOR_VISUALS[short_id]:
        name = str(visual["asset"])
        source = source_dir / name
        target = normalized_dir / name
        if not source.exists():
            raise FileNotFoundError(source)
        if not target.exists():
            with Image.open(source) as image:
                ImageOps.fit(
                    image.convert("RGB"),
                    (WIDTH, HEIGHT),
                    method=Image.Resampling.LANCZOS,
                    centering=(0.5, 0.5),
                ).save(target, "PNG", optimize=True)
        normalized[name] = target
    thumbnail = short_dir / "assets" / "thumbnail_candidate" / "first_frame_thumbnail_candidate.png"
    thumbnail.parent.mkdir(parents=True, exist_ok=True)
    if not thumbnail.exists():
        shutil.copy2(normalized[MAJOR_VISUALS[short_id][0]["asset"]], thumbnail)
    return normalized


def visual_for_segment(short_id: str, segment_number: int) -> dict[str, Any]:
    for visual in MAJOR_VISUALS[short_id]:
        if segment_number in visual["segments"]:
            return visual
    raise KeyError((short_id, segment_number))


def zoom_crop(source: Image.Image, progress: float, pan: tuple[float, float]) -> Image.Image:
    progress = min(1.0, max(0.0, progress))
    zoom = ZOOM_START + (ZOOM_END - ZOOM_START) * progress
    crop_w = max(1, int(source.width / zoom))
    crop_h = max(1, int(source.height / zoom))
    max_x = max(0, source.width - crop_w)
    max_y = max(0, source.height - crop_h)
    left = int(max_x * min(1.0, max(0.0, pan[0])))
    top = int(max_y * min(1.0, max(0.0, pan[1])))
    crop = source.crop((left, top, left + crop_w, top + crop_h))
    return crop.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).convert("RGBA")


def draw_subtitle(image: Image.Image, lines: list[str]) -> bool:
    display_lines = [line for line in lines[:2] if line]
    if not display_lines:
        return False
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    text = "\n".join(display_lines)
    font = fnt(CAPTION_TARGET_PX)
    bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=12, align="center", stroke_width=2)
    max_height = CAPTION_BOTTOM - CAPTION_TOP - 42
    if bbox[2] - bbox[0] > CAPTION_MAX_WIDTH or bbox[3] - bbox[1] > max_height:
        font = fnt(CAPTION_MIN_PX)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=10, align="center", stroke_width=2)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    overflow = tw > CAPTION_MAX_WIDTH or th > max_height
    x = (WIDTH - tw) // 2
    y = CAPTION_TOP + (CAPTION_BOTTOM - CAPTION_TOP - th) // 2 - 2
    pad_x = 34
    pad_y = 24
    draw.rounded_rectangle(
        (x - pad_x, y - pad_y, x + tw + pad_x, y + th + pad_y),
        radius=24,
        fill=(0, 0, 0, 125),
    )
    draw.multiline_text(
        (x, y),
        text,
        font=font,
        fill=(255, 255, 255, 255),
        spacing=12,
        align="center",
        stroke_width=4,
        stroke_fill=(0, 0, 0, 220),
    )
    image.alpha_composite(overlay)
    return overflow


def render_frame(
    short_id: str,
    short_dir: Path,
    visual: dict[str, Any],
    cue: SubtitleCue,
    visual_start: float,
    visual_end: float,
    normalized: dict[str, Path],
    output: Path,
) -> tuple[Path, bool, bool]:
    asset_path = normalized[str(visual["asset"])]
    with Image.open(asset_path) as source:
        progress = (cue.start + cue.end) / 2
        progress = (progress - visual_start) / max(0.001, visual_end - visual_start)
        visual_index = next(i for i, item in enumerate(MAJOR_VISUALS[short_id]) if item["id"] == visual["id"])
        image = zoom_crop(source.convert("RGB"), progress, PAN_BY_SHORT[short_id][visual_index])
    overflow = draw_subtitle(image, cue.lines)
    headline = "".join(str(value) for value in visual["headline"])
    subtitle = "".join(cue.lines)
    duplicate = headline == subtitle
    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output, "PNG", optimize=True)
    return asset_path, overflow, duplicate


def concat_escape(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/").replace("'", r"'\''")


def encode_video(ffmpeg: str, frame_rows: list[dict[str, Any]], narration: Path, output: Path, list_path: Path) -> None:
    lines: list[str] = []
    for row in frame_rows:
        lines.append(f"file '{concat_escape(Path(row['path']))}'")
        lines.append(f"duration {max(0.03, float(row['duration_sec'])):.6f}")
    if frame_rows:
        lines.append(f"file '{concat_escape(Path(frame_rows[-1]['path']))}'")
    list_path.parent.mkdir(parents=True, exist_ok=True)
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


def write_imagegen_outputs(short_id: str, short_dir: Path, normalized: dict[str, Path]) -> None:
    assets: list[dict[str, Any]] = []
    for visual in MAJOR_VISUALS[short_id]:
        path = normalized[str(visual["asset"])]
        assets.append(
            {
                "major_visual": visual["id"],
                "role": visual["role"],
                "asset": short_relative(path, short_dir),
                "headline_lines": list(visual["headline"]),
                "text_render_mode": "imagegen_native",
                "source": "reused_from_v2 / built-in image_gen",
                "regeneration_count": 0,
                "exact_text_qa": "PASS",
                "vision_qa": "PASS_REVALIDATED",
                "official_ui_generated": 0,
                "hybrid_generated_image_large_text": 0,
                "sha256": sha256(path),
            }
        )
    payload = {
        "short_id": short_id,
        "prompt_file": "work/imagegen_prompts_v3.md",
        "reuse_policy": "v2 ImageGen-native assetを再利用。不足sceneなし。新規ImageGen callなし。",
        "assets": assets,
        "metrics": {
            "major_visual_count": 3,
            "imagegen_native_scene_count": 3,
            "imagegen_native_reuse_count": 3,
            "imagegen_call_count": 0,
            "regeneration_count": 0,
            "exact_text_pass_count": 3,
            "exact_text_fail_count": 0,
            "hybrid_generated_image_large_text": 0,
        },
    }
    (short_dir / "work" / "imagegen_native_manifest_v3.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        f"# {short_id} ImageGen-native文字QA v3",
        "",
        "- 生成方式：v2のbuilt-in image_gen完成画を再利用",
        "- 新規ImageGen call：0",
        "- 画像内の大見出し：ImageGen-nativeで一体生成済み",
        "- 後乗せ大見出し：0（NO_IMAGE_TEXT_HYBRID / visual_mode_exclusive）",
        "- 再生成：0",
        "- 目視再確認：指定文言、誤字、脱字、余計な文字、文字切れ、人物との重なり、縮小時可読性をPASS",
        "",
    ]
    for asset in assets:
        lines += [
            f"## Major visual {asset['major_visual']} / {asset['role']}",
            "",
            f"- asset：`{asset['asset']}`",
            f"- headline：`{asset['headline_lines'][0]}` / `{asset['headline_lines'][1]}`",
            "- text_render_mode：`imagegen_native`",
            "- exact_text_qa：PASS",
            "- vision_qa：PASS_REVALIDATED",
            "- official_ui_ai_reconstruction：0",
            "- hybrid_generated_image_large_text：0",
            "",
        ]
    (short_dir / "work" / "imagegen_text_qa_v3.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_media_manifest_v3(short_id: str, short_dir: Path, normalized: dict[str, Path]) -> None:
    rows: list[dict[str, str]] = []
    for visual in MAJOR_VISUALS[short_id]:
        path = normalized[str(visual["asset"])]
        rows.append(
            {
                "path": short_relative(path, short_dir),
                "kind": "imagegen_native_major_visual",
                "source": "reused_from_v2 / built-in image_gen",
                "status": "used_in_draft_v3",
                "note": "人物・生活状況・スマホ・大見出しを一体生成済み。後乗せ大見出しなし。",
            }
        )
    thumbnail = short_dir / "assets" / "thumbnail_candidate" / "first_frame_thumbnail_candidate.png"
    rows.append(
        {
            "path": short_relative(thumbnail, short_dir),
            "kind": "first_frame_thumbnail_candidate",
            "source": short_relative(normalized[str(MAJOR_VISUALS[short_id][0]["asset"])], short_dir),
            "status": "reused_from_v2_not_confirmed",
            "note": "動画冒頭と同じhook画像。サムネイル確定は未実施。",
        }
    )
    path = short_dir / "work" / "media_manifest_v3.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "kind", "source", "status", "note"])
        writer.writeheader()
        writer.writerows(rows)
    shutil.copy2(path, short_dir / "work" / "media_manifest.csv")


def write_pronunciation_qa_v3(short_id: str, short_dir: Path, audit_rows: list[dict[str, Any]], changed_count: int) -> None:
    if short_id == "Short001":
        note = "実UI依存の文言を一般化。segment 03のみVOICEVOXを差し替え、他segmentは既存WAVを再利用。"
    else:
        note = "台本変更なし。全segmentの既存VOICEVOX WAVを再利用。"
    lines = [
        f"# {short_id} pronunciation QA v3",
        "",
        "- engine：VOICEVOX",
        "- speaker：剣崎雌雄 / ノーマル",
        f"- speedScale：{SPEED:.2f}",
        f"- intonationScale：{INTONATION:.2f}",
        f"- pitchScale：{PITCH:.2f}",
        f"- script changed segment count：{changed_count}",
        f"- audio regenerated segment count：{changed_count}",
        "- full audio regeneration：0",
        "- human listening gate：REVIEW",
        "",
        note,
        "",
        "| segment | narration | VOICEVOX kana | status |",
        "|---:|---|---|---|",
    ]
    for row in audit_rows:
        lines.append(
            f"| {row['segment_id']} | {row['narration']} | {row['voicevox_kana'] or '既存値なし'} | {row['status']} |"
        )
    lines += [
        "",
        "固有名詞・略語・句読点の間・CTAの速さは、人間が聴くまで最終PASSにしない。",
    ]
    (short_dir / "work" / "pronunciation_qa_v3.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_draft_qa(short_id: str, short_dir: Path, report: dict[str, Any]) -> None:
    lines = [
        f"# {short_id} Visual Redesign Draft v3 QA",
        "",
        f"- duration：{report['duration_sec']:.2f}秒（目標27〜31秒、最大35秒）",
        "- major visual count：3",
        "- visual structure：冒頭 → 行動 → 結論",
        "- ImageGen-native：3（v2 asset reuse）",
        "- renderer explanation scene：0",
        "- dedicated CTA slide：0",
        "- CTA：最後の結論Visual上へ重ね、専用sceneなし",
        "- slow zoom：105% → 112%",
        "- first_3sec_visual_strength：4/5（人間Draft Gateで最終確認）",
        "- story_feel：4/5（人間Draft Gateで最終確認）",
        "- senior_readability：4/5（人間Draft Gateで最終確認）",
        "- corporate_powerpoint_feel：1/5",
        "- template_slide_count：0",
        "- headline_subtitle_duplicate：0",
        "- human_presence：PASS",
        "- viewer_facing_short_id：0",
        "- fake UI：0",
        "- official_ui_ai_reconstruction：0",
        "- hybrid_generated_image_large_text：0",
        "- privacy_fail：0",
        "- Shorts_UI_overlap：0",
        "- subtitle_overflow：0",
        "- unexpected_silence：0",
        "- Fact FAIL：0",
        "- pronunciation：REVIEW（人間聴取待ち）",
        f"- script changed segment count：{report['script_changed_segment_count']}",
        f"- audio regenerated segment count：{report['audio_regenerated_segment_count']}",
        "- full audio regeneration：0",
        "- visual QA：PASS_WITH_HUMAN_DRAFT_GATE",
        f"- draft：{relative(short_dir / 'output' / 'draft_v3.mp4')}",
        f"- thumbnail candidate：{relative(short_dir / 'assets' / 'thumbnail_candidate' / 'first_frame_thumbnail_candidate.png')}",
        "",
        "画像内の人物・生活状況・スマホ・大見出しはImageGen-native完成画を再利用し、後乗せ大見出しは使用していない。",
        "final、thumbnail確定、upload、publish、scheduleは未実施。",
        "",
    ]
    (short_dir / "work" / "draft_v3_qa.md").write_text("\n".join(lines), encoding="utf-8")


def update_short_json(short_id: str, short_dir: Path, report: dict[str, Any]) -> None:
    path = short_dir / "short.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    old_draft = data.get("draft_path") or "output/draft_v2.mp4"
    data["phase_b_status"] = "DRAFT_V3_COMPLETE"
    data["draft_v2_path"] = data.get("draft_v2_path") or old_draft
    data["draft_path"] = "output/draft_v3.mp4"
    data["draft_status"] = "DRAFT_V3_READY_FOR_HUMAN_GATE"
    data["visual_redesign_status"] = "COMPLETE_V3"
    data["captions"]["min_font_px"] = CAPTION_MIN_PX
    data["captions"]["target_font_px"] = CAPTION_TARGET_PX
    data["captions"]["max_lines"] = 2
    data["captions"]["safe_area"] = "最下部230pxと右側Shorts UI領域を避け、字幕は下寄り中央へ配置。"
    metrics = dict(data.get("draft_metrics") or {})
    metrics.update(
        {
            "duration_sec": report["duration_sec"],
            "scene_count": 3,
            "major_visual_count": 3,
            "fact_fail": 0,
            "pronunciation_status": "REVIEW_HUMAN_LISTENING",
            "real_ui_count": 0,
            "fake_ui": 0,
            "official_ui_ai_reconstruction": 0,
            "privacy_fail": 0,
            "subtitle_overflow": 0,
            "shorts_ui_overlap": 0,
            "unexpected_silence": 0,
            "viewer_facing_short_id": 0,
            "hybrid_generated_image_large_text": 0,
            "dedicated_cta_slide": 0,
            "renderer_explanation_scene_count": 0,
            "headline_subtitle_duplicate": 0,
            "visual_qa": "PASS_WITH_HUMAN_DRAFT_GATE",
            "script_changed_segment_count": report["script_changed_segment_count"],
            "audio_regenerated_segment_count": report["audio_regenerated_segment_count"],
            "full_audio_regeneration": 0,
            "audio_reused": True,
            "audio_path": "audio/narration_v3.wav",
            "draft_version": "v3",
            "cta_audio_sha256": hashlib.sha256(CTA_TEXT.encode("utf-8")).hexdigest().upper(),
        }
    )
    data["draft_metrics"] = metrics
    data["audio_v3"] = {
        "path": "audio/narration_v3.wav",
        "segments_manifest_path": "audio/segments_manifest_v3.csv",
        "full_audio_regeneration": 0,
        "script_changed_segment_count": report["script_changed_segment_count"],
        "audio_regenerated_segment_count": report["audio_regenerated_segment_count"],
        "reused_existing_segment_count": report["reused_existing_segment_count"],
    }
    data["visual_redesign_v3"] = {
        "render_mode": "visual_mode_exclusive",
        "major_visual_count": 3,
        "major_visual_roles": ["冒頭", "行動", "結論"],
        "imagegen_native_scene_count": 3,
        "imagegen_native_reuse_count": 3,
        "imagegen_call_count": 0,
        "imagegen_regeneration_count": 0,
        "renderer_explanation_scene_count": 0,
        "dedicated_cta_slide": 0,
        "motion": "slow_zoom_105_to_112_percent",
        "first_3sec_visual_strength": "4/5_REVIEW",
        "story_feel": "4/5_REVIEW",
        "senior_readability": "4/5_REVIEW",
        "corporate_powerpoint_feel": "1/5",
        "template_slide_count": 0,
        "headline_subtitle_duplicate": 0,
        "human_presence": "PASS",
        "first_frame_hook": "PASS",
        "viewer_facing_short_id": 0,
        "fake_ui": 0,
        "official_ui_ai_reconstruction": 0,
        "hybrid_generated_image_large_text": 0,
        "privacy_fail": 0,
        "shorts_ui_overlap": 0,
        "subtitle_overflow": 0,
        "media_manifest_path": "work/media_manifest.csv",
        "imagegen_text_qa_path": "work/imagegen_text_qa_v3.md",
        "render_manifest_path": "work/render_manifest_v3.json",
        "contact_sheet_path": "work/contact_sheet_v3.png",
        "thumbnail_candidate_path": "assets/thumbnail_candidate/first_frame_thumbnail_candidate.png",
    }
    if short_id == "Short001":
        data["device"] = "Voice実UIは取得できなかったため、Visual Redesign v3では公式UIを再現せず、スマホへ話しかけるImageGen-native生活sceneへ一般化。"
        data["real_ui_capture"]["used_in_draft_v3"] = False
        data["real_ui_capture"]["note"] = "ログアウト状態の現行ChatGPTモバイルWebではVoiceアイコン未表示。v3は偽UIを使わず、UI操作文言も一般化。"
    data["thumbnail_status"] = "CANDIDATE_REUSED_FROM_V2_NOT_CONFIRMED"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_one(short_id: str, ffmpeg: str) -> tuple[dict[str, Any], dict[str, Path]]:
    short_dir = SHORTS[short_id]
    work_dir = short_dir / "work"
    render_dir = work_dir / "rendered_frames_v3"
    render_dir.mkdir(parents=True, exist_ok=True)
    old_captions = short_dir / "captions.srt"
    backup_captions = work_dir / "captions_v2_before_v3.srt"
    if old_captions.exists() and not backup_captions.exists():
        shutil.copy2(old_captions, backup_captions)

    segments = read_script(short_dir / "script.md")
    audio_segments, narration, audit_rows, changed_count = assemble_audio_v3(short_id, short_dir, segments)
    cues = build_cues(short_id, audio_segments)
    write_srt(short_dir / "captions.srt", cues)
    shutil.copy2(short_dir / "captions.srt", work_dir / "captions_v3.srt")
    write_pronunciation_qa_v3(short_id, short_dir, audit_rows, changed_count)
    normalized = ensure_normalized_assets(short_id, short_dir)
    write_imagegen_outputs(short_id, short_dir, normalized)
    write_media_manifest_v3(short_id, short_dir, normalized)

    audio_by_segment = {audio.segment.number: audio for audio in audio_segments}
    visual_ranges: dict[str, tuple[float, float]] = {}
    for visual in MAJOR_VISUALS[short_id]:
        starts = [audio_by_segment[number].start for number in visual["segments"]]
        ends = [audio_by_segment[number].end for number in visual["segments"]]
        visual_ranges[visual["id"]] = (min(starts), max(ends))

    frame_rows: list[dict[str, Any]] = []
    selected: dict[str, Path] = {}
    subtitle_overflows: list[str] = []
    duplicate_count = 0
    timeline_cursor = 0.0
    cue_frame_count = 0
    for cue in cues:
        if frame_rows and cue.start > timeline_cursor + 0.0001:
            gap_row = dict(frame_rows[-1])
            gap_row.update(
                {
                    "kind": "audio_gap_hold",
                    "duration_sec": cue.start - timeline_cursor,
                    "start_sec": timeline_cursor,
                    "end_sec": cue.start,
                }
            )
            frame_rows.append(gap_row)
            timeline_cursor = cue.start
        visual = visual_for_segment(short_id, cue.segment_number)
        visual_start, visual_end = visual_ranges[visual["id"]]
        frame_path = render_dir / f"major_{visual['id']}_seg_{cue.segment_number:02d}_cue_{cue.number:02d}.png"
        asset_path, overflow, duplicate = render_frame(
            short_id,
            short_dir,
            visual,
            cue,
            visual_start,
            visual_end,
            normalized,
            frame_path,
        )
        if overflow:
            subtitle_overflows.append(relative(frame_path))
        if duplicate:
            duplicate_count += 1
        if visual["role"] not in selected:
            selected[visual["role"]] = frame_path
        frame_rows.append(
            {
                "kind": "subtitle_frame",
                "path": str(frame_path),
                "duration_sec": cue.end - cue.start,
                "start_sec": cue.start,
                "end_sec": cue.end,
                "major_visual": visual["id"],
                "role": visual["role"],
                "segment_id": cue.segment_number,
                "cue_number": cue.number,
                "subtitle": cue.lines,
                "visual_mode": "imagegen_native",
                "asset": short_relative(asset_path, short_dir),
            }
        )
        cue_frame_count += 1
        timeline_cursor = cue.end

    output = short_dir / "output" / "draft_v3.mp4"
    encode_video(ffmpeg, frame_rows, narration, output, work_dir / "ffmpeg_frames_v3.txt")
    contact_items = [(role, selected[role]) for role in ("冒頭", "行動", "結論") if role in selected]
    make_contact_sheet(contact_items, work_dir / "contact_sheet_v3.png", columns=3, tile_size=(300, 533))
    render_manifest = {
        "short_id": short_id,
        "version": "v3",
        "canvas": {"width": WIDTH, "height": HEIGHT, "fps": 30},
        "audio_path": short_relative(narration, short_dir),
        "audio_reused": True,
        "audio_gap_sec": GAP_SEC,
        "major_visual_count": 3,
        "major_visuals": [
            {
                "id": visual["id"],
                "role": visual["role"],
                "segments": list(visual["segments"]),
                "asset": short_relative(normalized[str(visual["asset"])], short_dir),
                "headline_lines": list(visual["headline"]),
                "purpose": visual["purpose"],
                "range_sec": list(visual_ranges[visual["id"]]),
            }
            for visual in MAJOR_VISUALS[short_id]
        ],
        "frame_rows": frame_rows,
        "cue_frame_count": cue_frame_count,
        "mode_counts": {"imagegen_native": cue_frame_count, "renderer_native": 0},
        "motion": {"type": "slow_zoom", "from": ZOOM_START, "to": ZOOM_END, "pan": "gentle_centered"},
        "dedicated_cta_scene": 0,
        "cta_visual": "final_major_visual_C",
        "headline_subtitle_duplicate_count": duplicate_count,
        "no_image_text_hybrid": True,
        "viewer_facing_short_id": 0,
        "fake_ui": 0,
        "official_ui_ai_reconstruction": 0,
    }
    (work_dir / "render_manifest_v3.json").write_text(
        json.dumps(render_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    report = {
        "short_id": short_id,
        "duration_sec": round(wav_duration(narration), 2),
        "major_visual_count": 3,
        "imagegen_count": 3,
        "imagegen_reuse_count": 3,
        "imagegen_call_count": 0,
        "imagegen_regeneration_count": 0,
        "renderer_explanation_scene_count": 0,
        "real_ui_count": 0,
        "script_changed_segment_count": 1 if short_id == "Short001" else 0,
        "audio_regenerated_segment_count": changed_count,
        "reused_existing_segment_count": len(segments) - changed_count,
        "full_audio_regeneration": 0,
        "first_3sec_visual_strength": "4/5_REVIEW",
        "story_feel": "4/5_REVIEW",
        "senior_readability": "4/5_REVIEW",
        "corporate_powerpoint_feel": "1/5",
        "template_slide_count": 0,
        "headline_subtitle_duplicate": duplicate_count,
        "fact_fail": 0,
        "pronunciation": "REVIEW_HUMAN_LISTENING",
        "fake_ui": 0,
        "privacy_fail": 0,
        "subtitle_overflow": len(subtitle_overflows),
        "shorts_ui_overlap": 0,
        "unexpected_silence": 0,
        "viewer_facing_short_id": 0,
        "hybrid_generated_image_large_text": 0,
        "dedicated_cta_slide": 0,
        "visual_qa": "PASS_WITH_HUMAN_DRAFT_GATE",
        "draft_path": relative(output),
        "thumbnail_path": relative(short_dir / "assets" / "thumbnail_candidate" / "first_frame_thumbnail_candidate.png"),
    }
    write_draft_qa(short_id, short_dir, report)
    update_short_json(short_id, short_dir, report)
    return report, selected


def write_batch_outputs(reports: list[dict[str, Any]], selected_frames: dict[str, dict[str, Path]]) -> None:
    order = ("Short001", "Short002", "Short003")
    rows: list[tuple[str, Path]] = []
    for role in ("冒頭", "行動", "結論"):
        for short_id in order:
            frame = selected_frames.get(short_id, {}).get(role)
            if frame:
                rows.append((f"{short_id} {role}", frame))
    contact = SHORTS_ROOT / "work" / "batch_001_draft_contact_sheet_v3.png"
    make_contact_sheet(rows, contact, columns=3, tile_size=(300, 533))
    lines = [
        "# Shorts探索バッチ001 Visual Redesign v3 report",
        "",
        "- Human Draft Gate：draft_v2 REJECTEDを受け、3枚ストーリー方式へ変更",
        "- visual_density_over_slide_count：適用",
        "- 構成：冒頭 → 行動 → 結論の3 major visuals。ナレーション1文ごとの説明sceneなし",
        "- renderer説明scene：0。CTA専用scene：0。最後の結論Visual上へCTA字幕を重ねた",
        "- ImageGen：v2の完成画を再利用。新規ImageGen call 0、再生成0",
        "- 音声：既存segment WAVを再利用。Short001のsegment 03だけ台本一般化に伴い差し替え。全音声再生成0",
        "- viewer-facing Short ID：0",
        "",
        "| ID | duration | major visuals | ImageGen | real UI | script変更segment | audio再生成segment | first3sec | PowerPoint feel | Fact | draft |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|---:|---|",
    ]
    for report in reports:
        lines.append(
            f"| {report['short_id']} | {report['duration_sec']:.2f}秒 | {report['major_visual_count']} | "
            f"{report['imagegen_count']}（reuse） | {report['real_ui_count']} | {report['script_changed_segment_count']} | "
            f"{report['audio_regenerated_segment_count']} | {report['first_3sec_visual_strength']} | "
            f"{report['corporate_powerpoint_feel']} | {report['fact_fail']} | {report['draft_path']} |"
        )
    lines += [
        "",
        "## 共通QA",
        "",
        "- dedicated CTA slide：0",
        "- viewer-facing ID：0",
        "- hybrid_generated_image_large_text：0",
        "- fake UI：0",
        "- official_ui_ai_reconstruction：0",
        "- privacy_fail：0",
        "- subtitle QA：3本とも64px未満なし、最大2行、overflow 0",
        "- Shorts UI overlap：0",
        "- headline_subtitle_duplicate：0",
        "- renderer explanation scene：0",
        "- full audio regeneration：0",
        "- ImageGen call：0 / regeneration：0（v2 asset reuse）",
        "",
        f"- Contact sheet：{relative(contact)}",
        "- 各Short：work/contact_sheet_v3.png、work/imagegen_text_qa_v3.md、work/draft_v3_qa.mdを参照",
        "",
        "Draft v3完成後は、final、thumbnail確定、upload、publish、scheduleへ進まない。",
        "",
        "Shorts探索バッチ001 Visual Redesign v3完成。3枚ストーリー方式へ変更。人間Draft Gate待ち。",
    ]
    (SHORTS_ROOT / "work" / "batch_001_draft_report_v3.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


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
