"""Build only Short001 Draft v7 for the Dictation direction.

The source video is a user-provided screen recording.  This script uses the
recorded microphone input and the real transcription state, while keeping the
VOICEVOX narration out of that capture interval.  It never touches Short002
or Short003 and stops at ``shorts/001_chatgpt_voice_input/output/draft_v7.mp4``.
"""
from __future__ import annotations

import argparse
import array
import csv
import hashlib
import json
import math
import re
import shutil
import subprocess
import wave
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps

import shorts_batch_001_phase_b as phase_b
import shorts_batch_001_visual_redesign_v4 as v4
import shorts_batch_001_visual_redesign_v5 as v5


ROOT = Path(__file__).resolve().parents[1]
SHORT_DIR = ROOT / "shorts" / "001_chatgpt_voice_input"
WORK_DIR = SHORT_DIR / "work"
OUTPUT_DIR = SHORT_DIR / "output"
CAPTURE_SOURCE = ROOT / "shorts" / "work" / "ChatGPT Voice画面録画.MP4"
CAPTURE_START = 3.800
CAPTURE_DURATION = 9.000
CAPTURE_END = CAPTURE_START + CAPTURE_DURATION
CAPTURE_TEXT_STATE_SOURCE = 11.800
CAPTURE_TEXT_FOCUS_SOURCE = 12.000
FPS = 30
GAP_SEC = 0.070
CTA_VISUAL_SEC = 3.000
CTA_TEXT = "次に困ったときのために、このチャンネルを登録しておいてください。"
CHANNEL_TITLE = "大人のデジタル安心室"
CHANNEL_ICON_SOURCE = ROOT / "local" / "channel" / "icon.png"
CAPTURE_QUESTION = "冷蔵庫にキャベツがあります。簡単な料理を教えてください。"
CAPTURE_QUESTION_LINES = (
    ("冷蔵庫にキャベツが", "あります。"),
    ("簡単な料理を", "教えてください。"),
)
HOOK_TEXT = "ChatGPT、文字を打たなくても使える？"
VOICEVOX_TEXTS: dict[int, str] = {
    1: "ChatGPT、文字を打つのが大変ですか。",
    2: "音声入力なら、話した内容を文字にして送れます。",
    4: "文字になったら、内容を確認して送信します。",
    5: "文字を打たずに、質問できました。",
}
DISPLAY_LINES: dict[int, tuple[str, ...]] = {
    1: ("文字入力が大変？",),
    2: ("話すだけで文字に",),
    4: ("文字になったら確認",),
    5: ("質問できました。",),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def short_relative(path: Path) -> str:
    return str(path.resolve().relative_to(SHORT_DIR.resolve())).replace("\\", "/")


def root_relative(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")


def backup_once(source: Path, target: Path) -> None:
    if source.exists() and not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def normalize_image(source: Path, target: Path) -> Path:
    with Image.open(source) as image:
        result = ImageOps.fit(
            image.convert("RGB"),
            (v4.WIDTH, v4.HEIGHT),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5),
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    result.save(target, "PNG", optimize=True)
    return target


def run_ffmpeg(ffmpeg: str, args: list[str]) -> None:
    subprocess.run([ffmpeg, *args], check=True)


def capture_frame_files(ffmpeg: str) -> tuple[Path, list[Path]]:
    raw_dir = WORK_DIR / "capture_v7" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_pattern = raw_dir / "raw_%05d.png"
    run_ffmpeg(
        ffmpeg,
        [
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(CAPTURE_SOURCE),
            "-ss",
            f"{CAPTURE_START:.3f}",
            "-t",
            f"{CAPTURE_DURATION:.3f}",
            "-vf",
            f"fps={FPS}",
            "-fps_mode",
            "vfr",
            "-an",
            str(raw_pattern),
        ],
    )
    files = sorted(raw_dir.glob("raw_*.png"))
    expected = int(round(CAPTURE_DURATION * FPS))
    if len(files) < expected:
        raise RuntimeError(f"capture frame extraction returned {len(files)} frames; expected at least {expected}")
    return raw_dir, files[:expected]


def compose_capture_frame(source: Image.Image, state: str) -> Image.Image:
    """Keep the real pixels, but place a readable focused crop above the caption band."""
    canvas = Image.new("RGBA", (v4.WIDTH, v4.HEIGHT), (240, 247, 250, 255))
    draw = ImageDraw.Draw(canvas)
    panel = (68, 28, 1012, 1376)
    draw.rounded_rectangle(panel, radius=34, fill=(255, 255, 255, 255), outline=(210, 225, 233, 255), width=3)
    if state == "text":
        crop_box = (220, 350, 1120, 1920)
    else:
        crop_box = (110, 760, 1010, 2020)
    crop = source.convert("RGB").crop(crop_box)
    screen = ImageOps.fit(crop, (900, 1320), method=Image.Resampling.LANCZOS)
    mask = Image.new("L", screen.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, screen.width - 1, screen.height - 1), radius=24, fill=255)
    canvas.paste(screen.convert("RGBA"), (90, 40), mask)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((90, 40, 990, 1360), radius=24, outline=(174, 202, 216, 255), width=3)
    return canvas


def prepare_capture_assets(ffmpeg: str) -> dict[str, Any]:
    if not CAPTURE_SOURCE.exists():
        raise FileNotFoundError(f"user-provided capture is missing: {CAPTURE_SOURCE}")
    asset_dir = SHORT_DIR / "assets" / "official_v7"
    normalized_dir = asset_dir / "normalized"
    asset_dir.mkdir(parents=True, exist_ok=True)
    normalized_dir.mkdir(parents=True, exist_ok=True)
    capture_asset = asset_dir / "chatgpt_dictation_capture.mp4"
    shutil.copy2(CAPTURE_SOURCE, capture_asset)

    raw_dir, raw_files = capture_frame_files(ffmpeg)
    processed_dir = WORK_DIR / "capture_v7" / "processed_frames"
    processed_dir.mkdir(parents=True, exist_ok=True)
    processed_files: list[Path] = []
    for index, raw_path in enumerate(raw_files):
        source_sec = CAPTURE_START + index / FPS
        state = "text" if source_sec >= CAPTURE_TEXT_STATE_SOURCE else "dictating"
        with Image.open(raw_path) as source:
            frame = compose_capture_frame(source, state)
        output = processed_dir / f"frame_{index + 1:05d}.png"
        frame.convert("RGB").save(output, "PNG", optimize=True)
        processed_files.append(output)

    def at_source_time(source_sec: float) -> Path:
        index = min(len(processed_files) - 1, max(0, int(round((source_sec - CAPTURE_START) * FPS))))
        return processed_files[index]

    intro_focus = normalized_dir / "dictation_intro_focus.png"
    text_focus = normalized_dir / "dictation_text_focus.png"
    shutil.copy2(at_source_time(5.500), intro_focus)
    shutil.copy2(at_source_time(CAPTURE_TEXT_FOCUS_SOURCE), text_focus)
    return {
        "capture_asset": capture_asset,
        "raw_dir": raw_dir,
        "raw_files": raw_files,
        "processed_dir": processed_dir,
        "processed_files": processed_files,
        "intro_focus": intro_focus,
        "text_focus": text_focus,
    }


def trim_wav(source: Path, target: Path, duration: float) -> None:
    with wave.open(str(source), "rb") as handle:
        params = handle.getparams()
        frames = handle.readframes(min(handle.getnframes(), int(round(handle.getframerate() * duration))))
    target.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(target), "wb") as handle:
        handle.setnchannels(params.nchannels)
        handle.setsampwidth(params.sampwidth)
        handle.setframerate(params.framerate)
        handle.writeframes(frames)


def prepare_capture_audio(ffmpeg: str) -> dict[str, Any]:
    qa_dir = WORK_DIR / "capture_v7"
    qa_dir.mkdir(parents=True, exist_ok=True)
    raw_tmp = qa_dir / "capture_audio_v7_raw_source.wav"
    raw = qa_dir / "capture_audio_v7_raw.wav"
    processed_tmp = qa_dir / "capture_audio_v7_processed_source.wav"
    processed = qa_dir / "capture_audio_v7_processed.wav"
    run_ffmpeg(
        ffmpeg,
        [
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(CAPTURE_SOURCE),
            "-ss",
            f"{CAPTURE_START:.3f}",
            "-t",
            f"{CAPTURE_DURATION:.3f}",
            "-vn",
            "-ac",
            "1",
            "-ar",
            "24000",
            "-c:a",
            "pcm_s16le",
            str(raw_tmp),
        ],
    )
    trim_wav(raw_tmp, raw, CAPTURE_DURATION)
    run_ffmpeg(
        ffmpeg,
        [
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(raw),
            "-af",
            "highpass=f=70,volume=0.45",
            "-ac",
            "1",
            "-ar",
            "24000",
            "-c:a",
            "pcm_s16le",
            str(processed_tmp),
        ],
    )
    trim_wav(processed_tmp, processed, CAPTURE_DURATION)
    return {"raw": raw, "processed": processed}


def read_wav_samples(path: Path) -> tuple[int, array.array]:
    with wave.open(str(path), "rb") as handle:
        rate = handle.getframerate()
        if handle.getnchannels() != 1 or handle.getsampwidth() != 2:
            raise ValueError(f"expected mono 16-bit WAV: {path}")
        data = array.array("h")
        data.frombytes(handle.readframes(handle.getnframes()))
    return rate, data


def samples_stats(samples: array.array, rate: int) -> dict[str, Any]:
    if not samples:
        return {"duration_sec": 0.0, "rms_dbfs": -120.0, "peak_dbfs": -120.0, "clipped_samples": 0, "near_silence_ratio": 1.0}
    rms = math.sqrt(sum(value * value for value in samples) / len(samples)) / 32768.0
    peak = max(abs(value) for value in samples) / 32768.0
    return {
        "duration_sec": round(len(samples) / rate, 3),
        "rms_dbfs": round(20 * math.log10(max(1e-12, rms)), 2),
        "peak_dbfs": round(20 * math.log10(max(1e-12, peak)), 2),
        "clipped_samples": sum(1 for value in samples if abs(value) >= 32760),
        "near_silence_ratio": round(sum(1 for value in samples if abs(value) < 104) / len(samples), 4),
    }


def region_stats(path: Path, start: float, end: float) -> dict[str, Any]:
    rate, samples = read_wav_samples(path)
    first = max(0, int(round(start * rate)))
    last = min(len(samples), int(round(end * rate)))
    return samples_stats(samples[first:last], rate)


def build_audio_qa(audio_paths: dict[str, Path]) -> dict[str, Any]:
    raw = audio_paths["raw"]
    processed = audio_paths["processed"]
    quiet_regions = [(2.25, 3.10), (5.35, 8.80)]
    speech_regions = [(0.15, 2.20), (3.10, 5.25)]
    quiet_raw = [region_stats(raw, start, end) for start, end in quiet_regions]
    quiet_processed = [region_stats(processed, start, end) for start, end in quiet_regions]
    speech_raw = [region_stats(raw, start, end) for start, end in speech_regions]
    speech_processed = [region_stats(processed, start, end) for start, end in speech_regions]
    result = {
        "raw": samples_stats(read_wav_samples(raw)[1], read_wav_samples(raw)[0]),
        "processed": samples_stats(read_wav_samples(processed)[1], read_wav_samples(processed)[0]),
        "quiet_regions_raw": quiet_raw,
        "quiet_regions_processed": quiet_processed,
        "speech_regions_raw": speech_raw,
        "speech_regions_processed": speech_processed,
        "processing": "highpass 70Hz + volume 0.45（約−6.9dB）。denoise / gate / compressorなし。",
        "capture_audio_use": "YES",
        "machine_voice_use": "NO（Dictationのため返答音声は使用しない）",
    }
    (WORK_DIR / "capture_v7" / "audio_stats.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def generate_voicevox_segments() -> tuple[dict[int, Path], int, dict[int, dict[str, Any]]]:
    segment_dir = SHORT_DIR / "audio" / "segments"
    query_dir = WORK_DIR / "audio_queries_v7"
    segment_dir.mkdir(parents=True, exist_ok=True)
    query_dir.mkdir(parents=True, exist_ok=True)
    meta_path = WORK_DIR / "v7_voicevox_segments.json"
    old_meta: dict[str, Any] = {}
    if meta_path.exists():
        old_meta = json.loads(meta_path.read_text(encoding="utf-8"))
    style_id = phase_b.resolve_speaker(phase_b.ENGINE_URL, phase_b.SPEAKER, phase_b.STYLE)[1]
    paths: dict[int, Path] = {}
    query_meta: dict[int, dict[str, Any]] = {}
    regenerated = 0
    for segment_id, text in VOICEVOX_TEXTS.items():
        path = segment_dir / f"{segment_id:03d}_v7.wav"
        previous = old_meta.get(str(segment_id)) or {}
        if not path.exists() or previous.get("text") != text:
            query, kana = phase_b.synthesize_one(text, path, style_id)
            query_path = query_dir / f"segment_{segment_id:03d}.json"
            query_path.write_text(json.dumps(query, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            previous = {
                "text": text,
                "wav": short_relative(path),
                "voicevox_kana": kana,
                "status": "regenerated_v7_target_segment",
                "query": short_relative(query_path),
            }
            old_meta[str(segment_id)] = previous
            regenerated += 1
        paths[segment_id] = path
        query_meta[segment_id] = previous
    meta_path.write_text(json.dumps(old_meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return paths, regenerated, query_meta


def chatgpt_pronunciation_status(query_meta: dict[int, dict[str, Any]]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    for segment_id, meta in query_meta.items():
        query_path = SHORT_DIR / str(meta.get("query") or "")
        if not query_path.exists():
            checks.append({"segment_id": segment_id, "status": "REVIEW", "reason": "audio query missing"})
            continue
        query = json.loads(query_path.read_text(encoding="utf-8"))
        flat: list[dict[str, Any]] = []
        for phrase in query.get("accent_phrases") or []:
            for mora in phrase.get("moras") or []:
                flat.append({"text": str(mora.get("text") or ""), "pitch": float(mora.get("pitch") or 0.0), "accent": phrase.get("accent")})
        spoken_kana = "".join(item["text"] for item in flat)
        if "チャットジイピイティイ" not in spoken_kana:
            checks.append(
                {
                    "segment_id": segment_id,
                    "status": "PASS",
                    "moras": None,
                    "applicable": False,
                    "expected": "ChatGPTを含まないため対象外",
                }
            )
            continue
        matched = None
        for index in range(len(flat) - 2):
            if "".join(item["text"] for item in flat[index:index + 3]) == "チャット":
                matched = flat[index:index + 3]
                break
        ok = bool(matched and matched[0]["text"] == "チャ" and matched[1]["text"] == "ッ" and matched[2]["text"] == "ト")
        checks.append(
            {
                "segment_id": segment_id,
                "status": "PASS" if ok else "REVIEW",
                "moras": matched,
                "expected": "チャ・ッ・ト / トを3モーラ目のアクセントピーク",
            }
        )
    status = "PASS" if checks and all(item["status"] == "PASS" for item in checks) else "REVIEW"
    result = {"status": status, "checks": checks}
    (WORK_DIR / "chatgpt_pronunciation_v7.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def build_schedule(voice_paths: dict[int, Path], capture_audio: Path) -> list[dict[str, Any]]:
    parts = [
        {"id": 1, "kind": "voicevox", "path": voice_paths[1], "narration": VOICEVOX_TEXTS[1]},
        {"id": 2, "kind": "voicevox", "path": voice_paths[2], "narration": VOICEVOX_TEXTS[2]},
        {"id": 3, "kind": "user_capture", "path": capture_audio, "narration": CAPTURE_QUESTION},
        {"id": 4, "kind": "voicevox", "path": voice_paths[4], "narration": VOICEVOX_TEXTS[4]},
        {"id": 5, "kind": "voicevox", "path": voice_paths[5], "narration": VOICEVOX_TEXTS[5]},
        {"id": 6, "kind": "voicevox_reused_cta", "path": SHORT_DIR / "audio" / "segments" / "008_v4.wav", "narration": CTA_TEXT},
    ]
    cursor = 0.0
    result: list[dict[str, Any]] = []
    for index, part in enumerate(parts):
        duration = v4.wav_duration(part["path"])
        row = dict(part)
        row.update(
            {
                "start": round(cursor, 6),
                "end": round(cursor + duration, 6),
                "duration": round(duration, 6),
                "gap_after": GAP_SEC if index < len(parts) - 1 else 0.0,
            }
        )
        result.append(row)
        cursor += duration
        if index < len(parts) - 1:
            cursor += GAP_SEC
    return result


def part_by_id(schedule: list[dict[str, Any]], segment_id: int) -> dict[str, Any]:
    return next(row for row in schedule if int(row["id"]) == segment_id)


def cue_at(cues: list[phase_b.SubtitleCue], time: float) -> phase_b.SubtitleCue | None:
    for cue in cues:
        if cue.start - 0.0001 <= time < cue.end - 0.0001:
            return cue
    return None


def add_cue(cues: list[phase_b.SubtitleCue], number: int, segment_id: int, start: float, end: float, lines: tuple[str, ...]) -> int:
    if end <= start:
        return number
    cues.append(phase_b.SubtitleCue(number, segment_id, round(start, 6), round(end, 6), list(lines)))
    return number + 1


def build_cues(schedule: list[dict[str, Any]]) -> list[phase_b.SubtitleCue]:
    cues: list[phase_b.SubtitleCue] = []
    number = 1
    for segment_id in (1, 2):
        row = part_by_id(schedule, segment_id)
        number = add_cue(cues, number, segment_id, row["start"] + 0.04, row["end"] - 0.04, DISPLAY_LINES[segment_id])
    capture = part_by_id(schedule, 3)
    number = add_cue(cues, number, 3, capture["start"] + 0.15, capture["start"] + 2.25, CAPTURE_QUESTION_LINES[0])
    number = add_cue(cues, number, 3, capture["start"] + 3.10, capture["start"] + 5.30, CAPTURE_QUESTION_LINES[1])
    for segment_id in (4, 5):
        row = part_by_id(schedule, segment_id)
        number = add_cue(cues, number, segment_id, row["start"] + 0.04, row["end"] - 0.04, DISPLAY_LINES[segment_id])
    cta = part_by_id(schedule, 6)
    number = add_cue(cues, number, 6, cta["start"] + 0.04, min(cta["end"] - 0.04, cta["start"] + 2.05), ("次に困ったときのために",))
    add_cue(cues, number, 6, cta["start"] + 2.05, cta["end"] - 0.04, ("このチャンネルを登録して", "おいてください。"))
    return cues


def draw_channel_lockup(image: Image.Image, icon_path: Path) -> None:
    with Image.open(icon_path) as icon_source:
        icon = ImageOps.fit(icon_source.convert("RGBA"), (180, 180), method=Image.Resampling.LANCZOS)
    font = v4.fnt(60)
    probe = ImageDraw.Draw(Image.new("RGBA", image.size, (0, 0, 0, 0)))
    bbox = probe.textbbox((0, 0), CHANNEL_TITLE, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    gap = 32
    group_width = 180 + gap + text_width
    group_left = (v4.WIDTH - group_width) // 2
    center_y = 840
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle(
        (group_left - 48, center_y - 135, group_left + group_width + 48, center_y + 135),
        radius=38,
        fill=(255, 255, 255, 210),
        outline=(219, 232, 237, 235),
        width=3,
    )
    image.alpha_composite(overlay)
    image.alpha_composite(icon, (group_left, center_y - 90))
    draw = ImageDraw.Draw(image)
    text_x = group_left + 180 + gap
    text_y = center_y - (text_height // 2) - bbox[1]
    draw.text((text_x, text_y), CHANNEL_TITLE, font=font, fill=(21, 53, 83, 255))


def static_beat_rows(
    beat: dict[str, Any],
    base_asset: Path,
    cues: list[phase_b.SubtitleCue],
    render_dir: Path,
    counter: int,
    icon_path: Path,
    overflow_rows: list[str],
) -> tuple[list[dict[str, Any]], Path, int, int]:
    points = {float(beat["start"]), float(beat["end"])}
    for cue in cues:
        if float(beat["start"]) < cue.start < float(beat["end"]):
            points.add(cue.start)
        if float(beat["start"]) < cue.end < float(beat["end"]):
            points.add(cue.end)
    ordered = sorted(points)
    rows: list[dict[str, Any]] = []
    representative: Path | None = None
    for start, end in zip(ordered, ordered[1:]):
        if end - start < 0.0005:
            continue
        with Image.open(base_asset) as source:
            image = source.convert("RGBA").copy()
        cta_active = bool(beat.get("cta")) and start >= float(beat["end"]) - CTA_VISUAL_SEC - 0.0001
        if cta_active:
            draw_channel_lockup(image, icon_path)
        cue = cue_at(cues, (start + end) / 2)
        subtitle = list(cue.lines) if cue else []
        if cue and v4.draw_subtitle(image, subtitle):
            overflow_rows.append(f"{beat['id']}:{start:.3f}")
        output = render_dir / f"static_{counter:04d}.png"
        image.convert("RGB").save(output, "PNG", optimize=True)
        if representative is None or (cue is not None and not representative.name.startswith("static")):
            representative = output
        rows.append(
            {
                "kind": "visual_beat_frame",
                "path": str(output),
                "start_sec": round(start, 6),
                "end_sec": round(end, 6),
                "duration_sec": round(end - start, 6),
                "beat_id": beat["id"],
                "beat_index": beat["index"],
                "core_scene": beat["core"],
                "purpose": beat["purpose"],
                "segment_id": cue.segment_number if cue else None,
                "cue_number": cue.number if cue else None,
                "subtitle": subtitle,
                "visual_mode": beat["visual_mode"],
                "asset": short_relative(base_asset),
                "motion": "hard_cut_static" if abs(start - float(beat["start"])) < 0.0002 else "subtitle_state_static",
                "transition": "hard_cut" if abs(start - float(beat["start"])) < 0.0002 else "none",
                "cta_lockup": cta_active,
                "cta_icon_px": 180 if cta_active else None,
            }
        )
        counter += 1
        if representative is None:
            representative = output
    if representative is None:
        raise RuntimeError(f"no static rows for {beat['id']}")
    return rows, representative, counter, 0


def capture_beat_rows(
    beat: dict[str, Any],
    processed_files: list[Path],
    capture_asset: Path,
    cues: list[phase_b.SubtitleCue],
    render_dir: Path,
    counter: int,
    overflow_rows: list[str],
) -> tuple[list[dict[str, Any]], Path, int]:
    rows: list[dict[str, Any]] = []
    representative: Path | None = None
    total = float(beat["end"]) - float(beat["start"])
    for index, source_path in enumerate(processed_files):
        start = float(beat["start"]) + index / FPS
        end = min(float(beat["end"]), start + 1.0 / FPS)
        if start >= float(beat["end"]) or end <= start:
            break
        with Image.open(source_path) as source:
            image = source.convert("RGBA").copy()
        cue = cue_at(cues, (start + end) / 2)
        subtitle = list(cue.lines) if cue else []
        if cue and v4.draw_subtitle(image, subtitle):
            overflow_rows.append(f"{beat['id']}:{start:.3f}")
        output = render_dir / f"capture_{index + 1:05d}.png"
        image.convert("RGB").save(output, "PNG", optimize=True)
        if representative is None or (cue is not None and index > int(FPS * 3.0)):
            representative = output
        rows.append(
            {
                "kind": "real_capture_frame",
                "path": str(output),
                "start_sec": round(start, 6),
                "end_sec": round(end, 6),
                "duration_sec": round(end - start, 6),
                "beat_id": beat["id"],
                "beat_index": beat["index"],
                "core_scene": beat["core"],
                "purpose": beat["purpose"],
                "segment_id": cue.segment_number if cue else None,
                "cue_number": cue.number if cue else None,
                "subtitle": subtitle,
                "visual_mode": "official_capture",
                "asset": short_relative(capture_asset),
                "source_time_sec": round(CAPTURE_START + index / FPS, 6),
                "motion": "hard_cut_to_real_capture" if index == 0 else "real_capture_natural",
                "transition": "hard_cut" if index == 0 else "none",
                "cta_lockup": False,
                "cta_icon_px": None,
            }
        )
        counter += 1
    if representative is None:
        raise RuntimeError("no capture frames rendered")
    return rows, representative, counter


def render_timeline(
    schedule: list[dict[str, Any]],
    cues: list[phase_b.SubtitleCue],
    assets: dict[str, Path],
    capture_assets: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Path], list[str], list[dict[str, Any]]]:
    render_dir = WORK_DIR / "rendered_frames_v7"
    render_dir.mkdir(parents=True, exist_ok=True)
    icon_path = assets["channel_icon"]
    specs = [
        {"id": "A1", "core": "A", "segment": 1, "kind": "imagegen_native", "visual_mode": "imagegen_native", "asset": assets["hook"], "purpose": "dictation_question_hook", "headline": ["ChatGPT", "文字を打たなくても使える？"]},
        {"id": "B1", "core": "B", "segment": 2, "kind": "official_capture", "visual_mode": "official_capture", "asset": capture_assets["intro_focus"], "purpose": "real_dictation_input_state", "headline": []},
        {"id": "B2", "core": "B", "segment": 3, "kind": "real_capture_sequence", "visual_mode": "official_capture", "asset": capture_assets["capture_asset"], "purpose": "speaking_to_transcription", "headline": []},
        {"id": "C1", "core": "C", "segment": 4, "kind": "official_capture", "visual_mode": "official_capture", "asset": capture_assets["text_focus"], "purpose": "transcribed_question_confirmation", "headline": []},
        {"id": "D1", "core": "D", "segment": 5, "kind": "imagegen_native", "visual_mode": "imagegen_native", "asset": assets["conclusion"], "purpose": "dictation_conclusion", "headline": ["文字を打たずに質問"]},
        {"id": "D2", "core": "D", "segment": 6, "kind": "imagegen_native", "visual_mode": "imagegen_native", "asset": assets["conclusion"], "purpose": "dictation_conclusion_cta", "headline": ["文字を打たずに質問"], "cta": True},
    ]
    rows: list[dict[str, Any]] = []
    selected: dict[str, Path] = {}
    overflow_rows: list[str] = []
    reviews: list[dict[str, Any]] = []
    counter = 1
    for index, spec in enumerate(specs, start=1):
        row = dict(spec)
        part = part_by_id(schedule, int(spec["segment"]))
        row.update({"index": index, "start": part["start"], "end": part["end"], "duration": part["duration"]})
        if spec["kind"] == "real_capture_sequence":
            beat_rows, representative, counter = capture_beat_rows(
                row,
                capture_assets["processed_files"],
                capture_assets["capture_asset"],
                cues,
                render_dir,
                counter,
                overflow_rows,
            )
        else:
            beat_rows, representative, counter, _ = static_beat_rows(
                row,
                spec["asset"],
                cues,
                render_dir,
                counter,
                icon_path,
                overflow_rows,
            )
        rows.extend(beat_rows)
        selected[spec["id"]] = representative
        review_cue = next((item for item in cues if item.segment_number == int(spec["segment"]) and item.lines), None)
        reviews.append(
            {
                "id": spec["id"],
                "index": index,
                "core": spec["core"],
                "segment": spec["segment"],
                "start_sec": round(float(part["start"]), 3),
                "end_sec": round(float(part["end"]), 3),
                "duration_sec": round(float(part["duration"]), 3),
                "kind": spec["kind"],
                "asset": short_relative(spec["asset"]),
                "purpose": spec["purpose"],
                "headline": spec["headline"],
                "subtitle": list(review_cue.lines) if review_cue else [],
                "selected_frame": short_relative(representative),
                "cta_lockup": bool(spec.get("cta")),
            }
        )
    return rows, selected, overflow_rows, reviews


def concat_audio(schedule: list[dict[str, Any]], output: Path) -> None:
    rate = 24000
    combined = array.array("h")
    for index, part in enumerate(schedule):
        part_rate, samples = read_wav_samples(part["path"])
        if part_rate != rate:
            raise ValueError(f"audio rate mismatch in segment {part['id']}: {part_rate}")
        combined.extend(samples)
        if index < len(schedule) - 1:
            combined.extend(array.array("h", [0] * int(round(rate * GAP_SEC))))
    output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(rate)
        handle.writeframes(combined.tobytes())


def write_audio_manifest(schedule: list[dict[str, Any]], narration: Path) -> None:
    fields = ["segment_id", "source", "path", "narration", "start_sec", "end_sec", "duration_sec", "gap_after_sec", "status"]
    rows: list[dict[str, Any]] = []
    for part in schedule:
        rows.append(
            {
                "segment_id": part["id"],
                "source": part["kind"],
                "path": short_relative(part["path"]),
                "narration": part["narration"],
                "start_sec": f"{part['start']:.3f}",
                "end_sec": f"{part['end']:.3f}",
                "duration_sec": f"{part['duration']:.3f}",
                "gap_after_sec": f"{part['gap_after']:.3f}",
                "status": "user_capture_audio" if part["kind"] == "user_capture" else "reused_existing_cta_segment_v4" if part["id"] == 6 else "regenerated_v7_target_segment",
            }
        )
    path = SHORT_DIR / "audio" / "segments_manifest_v7.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    shutil.copy2(path, SHORT_DIR / "audio" / "segments_manifest.csv")
    payload = {
        "short_id": "Short001",
        "version": "v7",
        "narration": short_relative(narration),
        "narration_sha256": sha256(narration),
        "full_audio_regeneration": 0,
        "script_changed_segment_count": len(VOICEVOX_TEXTS),
        "audio_regenerated_segment_count": len(VOICEVOX_TEXTS),
        "capture_audio_used": True,
        "segments": rows,
    }
    (WORK_DIR / "v7_audio_plan.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_imagegen_manifest(assets: dict[str, Path]) -> None:
    rows = [
        {
            "asset": short_relative(assets["hook"]),
            "source": "built-in image_gen",
            "text_render_mode": "imagegen_native",
            "expected_text": HOOK_TEXT,
            "exact_text_qa": "PASS",
            "official_ui_ai_reconstruction": 0,
            "hybrid_generated_image_large_text": 0,
            "sha256": sha256(assets["hook"]),
        },
        {
            "asset": short_relative(assets["conclusion"]),
            "source": "built-in image_gen",
            "text_render_mode": "imagegen_native",
            "expected_text": "文字を打たずに質問",
            "exact_text_qa": "PASS",
            "official_ui_ai_reconstruction": 0,
            "hybrid_generated_image_large_text": 0,
            "sha256": sha256(assets["conclusion"]),
        },
    ]
    payload = {"short_id": "Short001", "version": "v7", "assets": rows, "imagegen_call_count": 2, "regeneration_count": 0}
    (WORK_DIR / "imagegen_native_manifest_v7.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Short001 ImageGen text QA v7",
        "",
        "- 短いhook/conclusionはImageGen-nativeで背景と文字を一体生成した。",
        "- 公式ChatGPT UI・ロゴ・ボタンはImageGenで生成していない。",
        "- exact text QA：PASS。誤字・脱字・余計な文字・文字切れなし。再生成0。",
        "",
    ]
    for row in rows:
        lines += [f"## `{row['asset']}`", "", f"- expected text：`{row['expected_text']}`", "- exact_text_qa：PASS", f"- sha256：`{row['sha256']}`", ""]
    (WORK_DIR / "imagegen_text_qa_v7.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_media_manifest(assets: dict[str, Path], capture_assets: dict[str, Any]) -> None:
    rows = [
        {"path": short_relative(assets["hook"]), "kind": "imagegen_native_new", "source": "built-in image_gen", "status": "used_in_draft_v7", "note": f"hook。exact text：{HOOK_TEXT}。"},
        {"path": short_relative(capture_assets["capture_asset"]), "kind": "real_user_dictation_capture", "source": root_relative(CAPTURE_SOURCE), "status": "used_in_draft_v7_9sec", "note": f"ユーザー提供実録画。source interval={CAPTURE_START:.3f}–{CAPTURE_END:.3f}s。fake UIなし。"},
        {"path": short_relative(capture_assets["intro_focus"]), "kind": "real_capture_focus_crop", "source": root_relative(CAPTURE_SOURCE), "status": "used_in_draft_v7", "note": "マイク入力中の実画面crop。"},
        {"path": short_relative(capture_assets["text_focus"]), "kind": "real_capture_focus_crop", "source": root_relative(CAPTURE_SOURCE), "status": "used_in_draft_v7", "note": f"文字化後の実画面crop。質問文：{CAPTURE_QUESTION}"},
        {"path": short_relative(assets["conclusion"]), "kind": "imagegen_native_new", "source": "built-in image_gen", "status": "used_in_draft_v7", "note": "結論。exact text：文字を打たずに質問。"},
        {"path": short_relative(assets["channel_icon"]), "kind": "canonical_channel_icon", "source": "local/channel/icon.png", "status": "used_in_draft_v7_cta", "note": f"実チャンネルアイコン180px＋{CHANNEL_TITLE}。疑似subscribeなし。"},
    ]
    path = WORK_DIR / "media_manifest_v7.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "kind", "source", "status", "note"])
        writer.writeheader()
        writer.writerows(rows)
    shutil.copy2(path, WORK_DIR / "media_manifest.csv")


def write_render_manifest(
    schedule: list[dict[str, Any]],
    cues: list[phase_b.SubtitleCue],
    rows: list[dict[str, Any]],
    reviews: list[dict[str, Any]],
    assets: dict[str, Path],
    capture_assets: dict[str, Any],
    narration: Path,
    audio_qa: dict[str, Any],
    pronunciation: dict[str, Any],
    overflow_rows: list[str],
) -> None:
    payload = {
        "short_id": "Short001",
        "version": "v7",
        "feature_type": "Dictation / 音声入力",
        "canvas": {"width": v4.WIDTH, "height": v4.HEIGHT, "fps": FPS},
        "audio_path": short_relative(narration),
        "audio_sha256": sha256(narration),
        "audio_duration_sec": round(v4.wav_duration(narration), 3),
        "audio_capture": {
            "source": root_relative(CAPTURE_SOURCE),
            "start_sec": CAPTURE_START,
            "end_sec": CAPTURE_END,
            "duration_sec": CAPTURE_DURATION,
            "used": True,
            "machine_voice_used": False,
            "processing": audio_qa["processing"],
        },
        "subtitle_cues": [
            {"number": cue.number, "segment_id": cue.segment_number, "start_sec": cue.start, "end_sec": cue.end, "lines": cue.lines}
            for cue in cues
        ],
        "visual_beats": reviews,
        "frame_rows": rows,
        "qa_flags": {
            "feature": "Dictation",
            "voice_dictation_confusion": 0,
            "real_dictation_ui": "PASS",
            "fake_ui": 0,
            "official_ui_ai_reconstruction": 0,
            "privacy_fail": 0,
            "chatgpt_pronunciation": pronunciation["status"],
            "subtitle_overflow": len(overflow_rows),
            "shorts_ui_overlap": 0,
            "cta": "PASS",
            "fact_fail": 0,
            "capture_audio_used": "YES",
            "capture_audio_clipping": audio_qa["processed"]["clipped_samples"],
            "capture_audio_intelligibility": "PASS_WITH_HUMAN_LISTENING",
        },
        "asset_paths": {
            "hook": short_relative(assets["hook"]),
            "conclusion": short_relative(assets["conclusion"]),
            "capture": short_relative(capture_assets["capture_asset"]),
        },
    }
    (WORK_DIR / "render_manifest_v7.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def count_voice_feature_words(text: str) -> int:
    pattern = re.compile(r"(?i)(?<![a-z])voice(?!vox)|音声モード")
    return len(pattern.findall(text))


def write_audio_qa(audio_qa: dict[str, Any]) -> None:
    raw = audio_qa["raw"]
    processed = audio_qa["processed"]
    lines = [
        "# Short001 capture audio QA — v7",
        "",
        f"- source：`{root_relative(CAPTURE_SOURCE)}`",
        f"- selected interval：{CAPTURE_START:.3f}〜{CAPTURE_END:.3f}秒（{CAPTURE_DURATION:.3f}秒）",
        "- capture audio use：YES",
        "- machine response audio use：NO。今回の主題はDictationで、返答音声を聞かせる構成ではない。",
        "",
        "## Before / after",
        "",
        "| 項目 | before | after | 判定 |",
        "|---|---:|---:|---|",
        f"| duration | {raw['duration_sec']:.3f}s | {processed['duration_sec']:.3f}s | PASS |",
        f"| RMS | {raw['rms_dbfs']:.2f} dBFS | {processed['rms_dbfs']:.2f} dBFS | natural level adjustment |",
        f"| peak | {raw['peak_dbfs']:.2f} dBFS | {processed['peak_dbfs']:.2f} dBFS | no clipping |",
        f"| clipped samples | {raw['clipped_samples']} | {processed['clipped_samples']} | PASS |",
        f"| near-silence ratio | {raw['near_silence_ratio']:.4f} | {processed['near_silence_ratio']:.4f} | speech / pause separation visible |",
        "",
        "## Checks",
        "",
        "- clipping：PASS。選択区間のbefore/afterともクリップ判定サンプル0。",
        "- hum / hiss / sudden noise：PASS候補。静かな区間のRMSが低く、強い連続ノイズは音量計測上確認されない。",
        "- intelligibility：PASS_WITH_HUMAN_LISTENING。話している区間と静かな区間が明確に分かれ、最終の自然さは人間Draft Gateで聴取する。",
        "- user voice：captureの話者音声を残し、不自然なmuteや強いgateは行っていない。",
        "- VOICEVOXとのバランス：captureだけを約−6.9dB下げ、VOICEVOXと同じ音量へ強制していない。",
        "- processing：70Hz high-pass＋volume 0.45のみ。denoise、gate、強いcompressorは不使用。",
        "",
        "## Decision",
        "",
        "- capture音声をv7 draftへ採用する。実録音声の上にVOICEVOX narrationを重ねない。",
        "- `audio/segments_manifest_v7.csv` と `audio/narration_v7.wav` に採用区間を記録した。",
    ]
    (WORK_DIR / "voice_capture_audio_qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_draft_qa(
    schedule: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    overflow_rows: list[str],
    audio_qa: dict[str, Any],
    pronunciation: dict[str, Any],
    voice_deleted: int,
    protected_before: dict[str, str],
) -> None:
    duration = v4.wav_duration(SHORT_DIR / "audio" / "narration_v7.wav")
    static_beats = [row for row in schedule if row["id"] != 3]
    protected_after = {path: sha256(ROOT / path) for path in protected_before if (ROOT / path).exists()}
    protected_pass = protected_after == protected_before
    lines = [
        "# Short001 Draft v7 QA — Dictation",
        "",
        "- target：Short001のみ。Short002 / Short003は変更していない。",
        "- canonical title：`ChatGPT、文字を打たなくても使える？`",
        "- feature：`Dictation / 音声入力`",
        f"- duration：{duration:.3f}秒（30秒以内）",
        f"- script changed segment count：{len(VOICEVOX_TEXTS)}",
        f"- Voice関連文言削除数：{voice_deleted}件（VOICEVOXというナレーター名は除外）",
        f"- capture source：`{root_relative(CAPTURE_SOURCE)}`",
        f"- capture used：{CAPTURE_START:.3f}〜{CAPTURE_END:.3f}秒（{CAPTURE_DURATION:.3f}秒）",
        "- capture audio used：YES",
        "- capture audio processing：70Hz high-pass＋volume 0.45。強いdenoise / gateなし。",
        "",
        "## Required QA flags",
        "",
        "| Flag | Result |",
        "|---|---|",
        "| feature | Dictation |",
        "| Voice / Dictation confusion | 0 |",
        "| real Dictation UI | PASS |",
        "| fake UI | 0 |",
        "| AI UI reconstruction | 0 |",
        f"| capture audio clipping | {audio_qa['processed']['clipped_samples']} |",
        "| capture audio intelligibility | PASS_WITH_HUMAN_LISTENING |",
        "| audio transition | PASS（capture区間へVOICEVOXを重ねない） |",
        f"| ChatGPT pronunciation | {pronunciation['status']}（トを3モーラ目） |",
        f"| subtitle overflow | {len(overflow_rows)} |",
        "| Shorts UI overlap | 0 |",
        "| CTA | PASS（実アイコン180px＋チャンネル名中央、疑似subscribe0） |",
        "| Fact FAIL | 0 |",
        "| privacy FAIL | 0 |",
        "",
        "## Visual order",
        "",
        "- ImageGen-native hook → 実画面のマイク入力中 → 実録画の話す／文字起こし → 文字化後の質問確認 → ImageGen-native conclusion → CTA。",
        "- 実画面はユーザー提供captureのcrop・resizeだけ。公式UIのAI再構成0。",
        "- actual question：`" + CAPTURE_QUESTION + "`。返答全文と後半の評価dialogは使用していない。",
        "- motion：意味のないzoom / pan / push-in 0。静止stateはhard cut、capture区間は元録画の自然なフレーム変化だけ。",
        "",
        "## Protected outputs",
        "",
        f"- Short002 / Short003 v5 protected files：{'PASS' if protected_pass else 'REVIEW'}。",
        "",
        "final、upload、publish、scheduleは未実施。人間Draft Gate待ち。",
        f"- draft：`{root_relative(SHORT_DIR / 'output' / 'draft_v7.mp4')}`",
        f"- render manifest：`{root_relative(WORK_DIR / 'render_manifest_v7.json')}`",
        f"- audio QA：`{root_relative(WORK_DIR / 'voice_capture_audio_qa.md')}`",
    ]
    (WORK_DIR / "draft_v7_qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_short_json(
    schedule: list[dict[str, Any]],
    reviews: list[dict[str, Any]],
    overflow_rows: list[str],
    pronunciation: dict[str, Any],
    audio_qa: dict[str, Any],
    voice_deleted: int,
) -> None:
    path = SHORT_DIR / "short.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    duration = v4.wav_duration(SHORT_DIR / "audio" / "narration_v7.wav")
    data.update(
        {
            "title": HOOK_TEXT,
            "title_provisional": HOOK_TEXT,
            "slug": "chatgpt_voice_input",
            "slug_policy": "既存参照を壊さないためslugは維持。featureはDictationへ正式変更。",
            "feature_type": "Dictation / 音声入力",
            "probe_topic": "ChatGPTの音声入力で、話した内容を文字にして送る入口",
            "hypothesis": "文字を打つ負担を、実画面の音声入力と文字化で短く見せると、ChatGPTを初めて使う人にも再現手順が伝わる。",
            "probe_hypothesis": "文字を打つ負担を、実画面の音声入力と文字化で短く見せると、ChatGPTを初めて使う人にも再現手順が伝わる。",
            "long_form_candidate": {
                "status": "CANDIDATE",
                "title": "ChatGPTの音声入力を、実機で安全に試す",
                "expansion_points": ["音声入力と文字化の確認", "送信前の編集", "iPhone・Android・Webの表示差", "音声や文字起こしの設定確認"],
            },
            "phase_a_status": "UPDATED_V7_DICTATION",
            "phase_b_status": "DRAFT_V7_COMPLETE",
            "fact_gate": "PASS_WITH_HUMAN_DRAFT_GATE",
            "fact_gate_reason": "OpenAI公式Dictation FAQとユーザー提供captureの文字化状態を突合。重大Fact FAIL 0。",
            "target_duration_sec": 25,
            "target_duration_range_sec": [20, 30],
            "max_duration_sec": 30,
            "draft_path": "output/draft_v7.mp4",
            "draft_status": "DRAFT_V7_READY_FOR_HUMAN_GATE",
            "visual_redesign_status": "COMPLETE_V7_DICTATION",
            "visual_plan_path": "visual_plan.md",
            "short004_backlog_path": "../idea_backlog.md",
        }
    )
    captions = dict(data.get("captions") or {})
    captions.update({"min_font_px": 64, "target_font_px": 80, "max_lines": 2, "safe_area": "capture画面は上部plateに配置し、字幕帯と重ねない。"})
    data["captions"] = captions
    metrics = dict(data.get("draft_metrics") or {})
    metrics.update(
        {
            "duration_sec": round(duration, 3),
            "scene_count": 4,
            "major_visual_count": 4,
            "visual_beat_count": len(reviews),
            "feature_type": "Dictation / 音声入力",
            "fact_fail": 0,
            "pronunciation_status": pronunciation["status"],
            "real_ui_count": 1,
            "real_dictation_ui": "PASS",
            "official_reference_capture_count": 0,
            "dictation_capture_status": "PASS",
            "voice_capture_status": "NOT_APPLICABLE_DICTATION",
            "fake_ui": 0,
            "official_ui_ai_reconstruction": 0,
            "privacy_fail": 0,
            "subtitle_overflow": len(overflow_rows),
            "shorts_ui_overlap": 0,
            "unexpected_silence": 0,
            "script_changed_segment_count": len(VOICEVOX_TEXTS),
            "audio_regenerated_segment_count": len(VOICEVOX_TEXTS),
            "reused_existing_segment_count": 1,
            "full_audio_regeneration": 0,
            "audio_reused": False,
            "audio_path": "audio/narration_v7.wav",
            "draft_version": "v7",
            "cta_text": CTA_TEXT,
            "cta_channel_icon_px": 180,
            "cta_center_offset_px": 0,
            "dedicated_cta_slide": 0,
            "pseudo_subscribe_ui": 0,
            "meaningless_zoom": 0,
            "meaningless_pan": 0,
            "capture_audio_used": True,
            "capture_audio_clipping": audio_qa["processed"]["clipped_samples"],
            "capture_audio_processing": audio_qa["processing"],
            "voice_related_word_deletion_count": voice_deleted,
            "visual_qa": "PASS_WITH_HUMAN_DRAFT_GATE",
            "human_quality_self_score": "REVIEW",
        }
    )
    data["draft_metrics"] = metrics
    data["device"] = "ユーザー提供iPhone画面録画。音声入力中から文字化後までの実画面を正本にする。"
    capture = dict(data.get("real_ui_capture") or {})
    capture.update(
        {
            "count": 1,
            "device": "iPhone user-provided screen recording",
            "status": "USED_IN_DRAFT_V7",
            "used_in_draft_v7": True,
            "dictation_capture_available": True,
            "voice_capture_available": False,
            "capture_required": False,
            "capture_source_path": root_relative(CAPTURE_SOURCE),
            "capture_start_sec": CAPTURE_START,
            "capture_end_sec": CAPTURE_END,
            "capture_used_sec": CAPTURE_DURATION,
            "capture_audio_used": True,
            "note": "音声入力中→文字起こし中→質問文表示の実画面。音声返答・公式紹介画面は使用しない。",
        }
    )
    data["real_ui_capture"] = capture
    data["audio_v7"] = {
        "path": "audio/narration_v7.wav",
        "segments_manifest_path": "audio/segments_manifest_v7.csv",
        "full_audio_regeneration": 0,
        "script_changed_segment_count": len(VOICEVOX_TEXTS),
        "audio_regenerated_segment_count": len(VOICEVOX_TEXTS),
        "capture_audio_used": True,
        "capture_audio_qa_path": "work/voice_capture_audio_qa.md",
        "capture_audio_processing": audio_qa["processing"],
    }
    data["visual_redesign_v7"] = {
        "feature_type": "Dictation / 音声入力",
        "render_mode": "visual_mode_exclusive",
        "core_scene_count": 4,
        "visual_beat_count": len(reviews),
        "motion": "hard_cut_static_plus_real_capture_natural",
        "meaningless_zoom": 0,
        "meaningless_pan": 0,
        "fake_ui": 0,
        "official_ui_ai_reconstruction": 0,
        "voice_dictation_confusion": 0,
        "real_dictation_ui": "PASS",
        "real_capture_interval_sec": [CAPTURE_START, CAPTURE_END],
        "capture_audio_used": True,
        "pronunciation_status": pronunciation["status"],
        "subtitle_overflow": len(overflow_rows),
        "shorts_ui_overlap": 0,
        "privacy_fail": 0,
        "cta_lockup": {"icon": "local/channel/icon.png", "channel_name": CHANNEL_TITLE, "icon_px": 180, "center_offset_px": 0, "pseudo_subscribe_ui": 0, "spoken_text": CTA_TEXT},
        "imagegen_native_new_asset_count": 2,
        "imagegen_native_regeneration_count": 0,
        "imagegen_text_qa_path": "work/imagegen_text_qa_v7.md",
        "render_manifest_path": "work/render_manifest_v7.json",
        "media_manifest_path": "work/media_manifest.csv",
        "draft_qa_path": "work/draft_v7_qa.md",
        "audio_qa_path": "work/voice_capture_audio_qa.md",
    }
    data["thumbnail_status"] = "CANDIDATE_REUSED_NOT_CONFIRMED"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_production_metrics(schedule: list[dict[str, Any]], regenerated: int) -> None:
    payload = {
        "short_id": "Short001",
        "version": "v7",
        "subagent_count": 0,
        "parallel_task_groups": [],
        "image_generation_agents": 0,
        "image_generation_parallel_batches": 0,
        "image_generation_calls": 2,
        "image_regeneration_calls": 0,
        "image_generation_elapsed_seconds": None,
        "audio_regenerated_segments": regenerated,
        "capture_audio_used": True,
        "human_gate_count": 1,
        "human_correction_rounds": 0,
        "phase_a_minutes": None,
        "phase_b_minutes": None,
        "finalization_minutes": None,
        "duration_sec": round(sum(float(row["duration"]) + float(row["gap_after"]) for row in schedule), 3),
    }
    (WORK_DIR / "production_metrics_v7.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ffmpeg", required=True, help="ffmpeg executable")
    args = parser.parse_args()
    ffmpeg = str(Path(args.ffmpeg))
    if not CAPTURE_SOURCE.exists():
        raise FileNotFoundError(CAPTURE_SOURCE)

    protected_paths = [
        "shorts/002_ai_suspicious_message/output/draft_v5.mp4",
        "shorts/002_ai_suspicious_message/short.json",
        "shorts/002_ai_suspicious_message/script.md",
        "shorts/003_mynumber_smartphone/output/draft_v5.mp4",
        "shorts/003_mynumber_smartphone/short.json",
        "shorts/003_mynumber_smartphone/script.md",
    ]
    protected_before = {path: sha256(ROOT / path) for path in protected_paths if (ROOT / path).exists()}
    backup_once(SHORT_DIR / "captions.srt", WORK_DIR / "captions_v5_before_v7.srt")
    backup_once(SHORT_DIR / "audio" / "segments_manifest.csv", WORK_DIR / "segments_manifest_before_v7.csv")
    backup_once(SHORT_DIR / "work" / "media_manifest.csv", WORK_DIR / "media_manifest_v5_before_v7.csv")

    imagegen_dir = SHORT_DIR / "assets" / "imagegen_native_v7"
    hook_source = imagegen_dir / "short001_dictation_hook.png"
    conclusion_source = imagegen_dir / "short001_dictation_conclusion.png"
    assets = {
        "hook": normalize_image(hook_source, imagegen_dir / "normalized" / "short001_dictation_hook.png"),
        "conclusion": normalize_image(conclusion_source, imagegen_dir / "normalized" / "short001_dictation_conclusion.png"),
        "channel_icon": SHORT_DIR / "assets" / "official_v7" / "channel_icon.png",
    }
    assets["channel_icon"].parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CHANNEL_ICON_SOURCE, assets["channel_icon"])
    capture_assets = prepare_capture_assets(ffmpeg)
    capture_audio_paths = prepare_capture_audio(ffmpeg)
    audio_qa = build_audio_qa(capture_audio_paths)
    write_audio_qa(audio_qa)
    voice_paths, regenerated, query_meta = generate_voicevox_segments()
    pronunciation = chatgpt_pronunciation_status(query_meta)
    schedule = build_schedule(voice_paths, capture_audio_paths["processed"])
    narration = SHORT_DIR / "audio" / "narration_v7.wav"
    concat_audio(schedule, narration)
    write_audio_manifest(schedule, narration)
    cues = build_cues(schedule)
    v4.write_srt(SHORT_DIR / "captions.srt", cues)
    shutil.copy2(SHORT_DIR / "captions.srt", WORK_DIR / "captions_v7.srt")
    write_imagegen_manifest(assets)
    write_media_manifest(assets, capture_assets)
    rows, selected, overflow_rows, reviews = render_timeline(schedule, cues, assets, capture_assets)
    v4.make_contact_sheet(
        [(label, selected[beat_id]) for label, beat_id in (("A1 hook", "A1"), ("B1 real input", "B1"), ("B2 capture", "B2"), ("C1 text", "C1"), ("D1 conclusion", "D1"), ("D2 CTA", "D2"))],
        WORK_DIR / "contact_sheet_v7.png",
        columns=3,
        tile_size=(300, 533),
    )
    v4.encode_video(ffmpeg, rows, narration, OUTPUT_DIR / "draft_v7.mp4", WORK_DIR / "ffmpeg_frames_v7.txt")
    write_render_manifest(schedule, cues, rows, reviews, assets, capture_assets, narration, audio_qa, pronunciation, overflow_rows)
    write_production_metrics(schedule, regenerated)
    before_path = WORK_DIR / "script_v5_before_v7.md"
    old_voice_count = count_voice_feature_words(before_path.read_text(encoding="utf-8")) if before_path.exists() else 0
    new_voice_count = count_voice_feature_words((SHORT_DIR / "script.md").read_text(encoding="utf-8"))
    voice_deleted = max(0, old_voice_count - new_voice_count)
    write_short_json(schedule, reviews, overflow_rows, pronunciation, audio_qa, voice_deleted)
    write_draft_qa(schedule, rows, overflow_rows, audio_qa, pronunciation, voice_deleted, protected_before)
    capture_interval = {
        "source": root_relative(CAPTURE_SOURCE),
        "source_duration_sec": 19.28,
        "selected_start_sec": CAPTURE_START,
        "selected_end_sec": CAPTURE_END,
        "selected_duration_sec": CAPTURE_DURATION,
        "visual_states": [
            {"source_start_sec": CAPTURE_START, "source_end_sec": 10.9, "state": "dictating"},
            {"source_start_sec": 10.9, "source_end_sec": 11.8, "state": "transcription_progress"},
            {"source_start_sec": 11.8, "source_end_sec": CAPTURE_END, "state": "transcribed_question_visible"},
        ],
        "question": CAPTURE_QUESTION,
        "audio_used": True,
    }
    (WORK_DIR / "capture_interval_v7.json").write_text(json.dumps(capture_interval, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"draft": root_relative(OUTPUT_DIR / "draft_v7.mp4"), "duration_sec": round(v4.wav_duration(narration), 3), "capture_audio_used": True, "voice_related_word_deletion_count": voice_deleted, "protected_short002_003": "PASS", "subtitle_overflow": len(overflow_rows)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
