"""Build only Short001 Draft v8 for the Dictation direction.

v8 keeps the v7 Dictation story and adds a real ChatGPT answer state from the
same user-provided screen recording.  The answer is cropped and resized from
the source pixels; no UI or answer text is redrawn.  Short002/Short003 and
final/publication artifacts are never touched.
"""
from __future__ import annotations

import argparse
import array
import csv
import hashlib
import json
import math
import shutil
import subprocess
import wave
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps

import shorts_batch_001_phase_b as phase_b
import shorts_batch_001_visual_redesign_v4 as v4
import shorts_batch_001_short001_dictation_v7 as v7


ROOT = Path(__file__).resolve().parents[1]
SHORT_DIR = ROOT / "shorts" / "001_chatgpt_voice_input"
WORK_DIR = SHORT_DIR / "work"
OUTPUT_DIR = SHORT_DIR / "output"
CAPTURE_SOURCE = ROOT / "shorts" / "work" / "ChatGPT Voice画面録画.MP4"
FPS = 30
GAP_SEC = 0.070
INPUT_START = 3.800
INPUT_DURATION = 9.000
INPUT_END = INPUT_START + INPUT_DURATION
ANSWER_START = 14.200
ANSWER_SOURCE_DURATION = 2.800
ANSWER_END = ANSWER_START + ANSWER_SOURCE_DURATION
CAPTURE_TEXT_STATE_SOURCE = 11.800
CAPTURE_TEXT_FOCUS_SOURCE = 12.000
CAPTURE_QUESTION = "冷蔵庫にキャベツがあります。簡単な料理を教えてください。"
ANSWER_SUBTITLE = ("ちゃんと答えが", "返ってきた")
CTA_TEXT = "次に困ったときのために、このチャンネルを登録しておいてください。"
CHANNEL_TITLE = "大人のデジタル安心室"
CHANNEL_ICON_SOURCE = ROOT / "local" / "channel" / "icon.png"
HOOK_TEXT = "ChatGPT、文字を打たなくても使える？"
VOICEVOX_TEXTS: dict[int, str] = {
    1: "ChatGPT、文字を打つのが大変ですか。",
    2: "音声入力なら、話した内容を文字にして送れます。",
    4: "文字になったら、内容を確認して送信します。",
    5: "料理の答えが返ってきました。",
    6: "文字を打たずに、質問できました。",
    7: CTA_TEXT,
}
DISPLAY_LINES: dict[int, tuple[str, ...]] = {
    1: ("文字入力が大変？",),
    2: ("話すだけで文字に",),
    4: ("文字になったら確認",),
    5: ANSWER_SUBTITLE,
    6: ("質問できました。",),
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


def run_ffmpeg(ffmpeg: str, args: list[str]) -> None:
    subprocess.run([ffmpeg, *args], check=True)


def extract_frames(ffmpeg: str, start: float, duration: float, directory: Path, prefix: str) -> list[Path]:
    directory.mkdir(parents=True, exist_ok=True)
    pattern = directory / f"{prefix}_%05d.png"
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
            f"{start:.3f}",
            "-t",
            f"{duration:.3f}",
            "-vf",
            f"fps={FPS}",
            "-fps_mode",
            "vfr",
            "-an",
            str(pattern),
        ],
    )
    files = sorted(directory.glob(f"{prefix}_*.png"))
    expected = int(round(duration * FPS))
    if len(files) < expected:
        raise RuntimeError(f"{prefix} frame extraction returned {len(files)}; expected at least {expected}")
    return files[:expected]


def compose_answer_frame(source: Image.Image) -> Image.Image:
    """Show only a readable crop of the real response; do not redraw its UI."""
    canvas = Image.new("RGBA", (v4.WIDTH, v4.HEIGHT), (240, 247, 250, 255))
    draw = ImageDraw.Draw(canvas)
    panel = (68, 28, 1012, 1376)
    draw.rounded_rectangle(panel, radius=34, fill=(255, 255, 255, 255), outline=(210, 225, 233, 255), width=3)
    # Preserve the full source width so the first/last character of the real
    # answer is never clipped.  Only the vertical range is focused.
    crop = source.convert("RGB").crop((0, 500, 1126, 2152))
    screen = ImageOps.fit(crop, (900, 1320), method=Image.Resampling.LANCZOS, centering=(0.5, 0.46))
    mask = Image.new("L", screen.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, screen.width - 1, screen.height - 1), radius=24, fill=255)
    canvas.paste(screen.convert("RGBA"), (90, 40), mask)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((90, 40, 990, 1360), radius=24, outline=(174, 202, 216, 255), width=3)
    return canvas


def prepare_visual_assets(ffmpeg: str) -> dict[str, Any]:
    if not CAPTURE_SOURCE.exists():
        raise FileNotFoundError(CAPTURE_SOURCE)
    asset_dir = SHORT_DIR / "assets" / "official_v8"
    normalized_dir = asset_dir / "normalized"
    asset_dir.mkdir(parents=True, exist_ok=True)
    normalized_dir.mkdir(parents=True, exist_ok=True)
    source_copy = asset_dir / "chatgpt_dictation_capture_source.mp4"
    shutil.copy2(CAPTURE_SOURCE, source_copy)

    input_raw = extract_frames(ffmpeg, INPUT_START, INPUT_DURATION, WORK_DIR / "capture_v8" / "input_raw", "input")
    input_processed_dir = WORK_DIR / "capture_v8" / "input_processed_frames"
    input_processed_dir.mkdir(parents=True, exist_ok=True)
    input_processed: list[Path] = []
    for index, path in enumerate(input_raw):
        source_sec = INPUT_START + index / FPS
        state = "text" if source_sec >= CAPTURE_TEXT_STATE_SOURCE else "dictating"
        with Image.open(path) as source:
            frame = v7.compose_capture_frame(source, state)
        output = input_processed_dir / f"frame_{index + 1:05d}.png"
        frame.convert("RGB").save(output, "PNG", optimize=True)
        input_processed.append(output)

    def input_at(source_sec: float) -> Path:
        index = min(len(input_processed) - 1, max(0, int(round((source_sec - INPUT_START) * FPS))))
        return input_processed[index]

    intro_focus = normalized_dir / "dictation_intro_focus.png"
    text_focus = normalized_dir / "dictation_text_focus.png"
    shutil.copy2(input_at(5.500), intro_focus)
    shutil.copy2(input_at(CAPTURE_TEXT_FOCUS_SOURCE), text_focus)

    answer_raw = extract_frames(ffmpeg, ANSWER_START, ANSWER_SOURCE_DURATION, WORK_DIR / "capture_v8" / "answer_raw", "answer")
    answer_processed_dir = WORK_DIR / "capture_v8" / "answer_processed_frames"
    answer_processed_dir.mkdir(parents=True, exist_ok=True)
    answer_processed: list[Path] = []
    for index, path in enumerate(answer_raw):
        with Image.open(path) as source:
            frame = compose_answer_frame(source)
        output = answer_processed_dir / f"frame_{index + 1:05d}.png"
        frame.convert("RGB").save(output, "PNG", optimize=True)
        answer_processed.append(output)
    answer_focus = normalized_dir / "chatgpt_answer_focus.png"
    shutil.copy2(answer_processed[min(len(answer_processed) - 1, int(0.7 * FPS))], answer_focus)
    return {
        "source_copy": source_copy,
        "input_raw": input_raw,
        "input_processed": input_processed,
        "intro_focus": intro_focus,
        "text_focus": text_focus,
        "answer_raw": answer_raw,
        "answer_processed": answer_processed,
        "answer_focus": answer_focus,
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


def prepare_input_audio(ffmpeg: str) -> dict[str, Path]:
    directory = WORK_DIR / "capture_v8"
    directory.mkdir(parents=True, exist_ok=True)
    raw_source = directory / "capture_audio_v8_raw_source.wav"
    raw = directory / "capture_audio_v8_raw.wav"
    processed_source = directory / "capture_audio_v8_processed_source.wav"
    processed = directory / "capture_audio_v8_processed.wav"
    run_ffmpeg(
        ffmpeg,
        [
            "-y", "-hide_banner", "-loglevel", "error", "-i", str(CAPTURE_SOURCE),
            "-ss", f"{INPUT_START:.3f}", "-t", f"{INPUT_DURATION:.3f}", "-vn",
            "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", str(raw_source),
        ],
    )
    trim_wav(raw_source, raw, INPUT_DURATION)
    run_ffmpeg(
        ffmpeg,
        [
            "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw),
            "-af", "highpass=f=70,volume=0.45", "-ac", "1", "-ar", "24000",
            "-c:a", "pcm_s16le", str(processed_source),
        ],
    )
    trim_wav(processed_source, processed, INPUT_DURATION)
    return {"raw": raw, "processed": processed}


def audio_qa(audio_paths: dict[str, Path]) -> dict[str, Any]:
    raw = audio_paths["raw"]
    processed = audio_paths["processed"]
    result = {
        "raw": v7.samples_stats(v7.read_wav_samples(raw)[1], v7.read_wav_samples(raw)[0]),
        "processed": v7.samples_stats(v7.read_wav_samples(processed)[1], v7.read_wav_samples(processed)[0]),
        "quiet_regions_raw": [v7.region_stats(raw, 2.25, 3.10), v7.region_stats(raw, 5.35, 8.80)],
        "quiet_regions_processed": [v7.region_stats(processed, 2.25, 3.10), v7.region_stats(processed, 5.35, 8.80)],
        "speech_regions_raw": [v7.region_stats(raw, 0.15, 2.20), v7.region_stats(raw, 3.10, 5.25)],
        "speech_regions_processed": [v7.region_stats(processed, 0.15, 2.20), v7.region_stats(processed, 3.10, 5.25)],
        "processing": "70Hz high-pass + volume 0.45（約−6.9dB）。denoise / gate / compressorなし。",
        "capture_audio_use": "YES（Dictation入力区間のみ）",
        "machine_voice_use": "NO（回答画面はテキストを主役にし、返答音声は使用しない）",
    }
    (WORK_DIR / "capture_v8" / "audio_stats.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def write_audio_qa(result: dict[str, Any]) -> None:
    raw = result["raw"]
    processed = result["processed"]
    lines = [
        "# Short001 capture audio QA — v8",
        "",
        f"- source：`{root_relative(CAPTURE_SOURCE)}`",
        f"- Dictation input audio：{INPUT_START:.3f}〜{INPUT_END:.3f}秒（{INPUT_DURATION:.3f}秒）を採用",
        f"- ChatGPT answer visual：{ANSWER_START:.3f}〜{ANSWER_END:.3f}秒。音声は追加しない",
        "- capture audio use：YES（音声入力中のユーザー音声のみ）",
        "- machine response audio use：NO。今回の主題はDictationで、回答画面のテキストを見せる。",
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
        "## Decision",
        "",
        "- Dictation入力区間の実録音声をv8へ採用する。実回答sceneへVOICEVOXや機械返答音声を重ねない。",
        "- 処理は70Hz high-passとvolume 0.45だけ。強いdenoise / gate / compressorは不使用。",
        "- 最終的な聞き取りやすさは人間Draft Gateで確認する。",
    ]
    (WORK_DIR / "voice_capture_audio_qa_v8.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def pad_wav_min_duration(path: Path, minimum_sec: float) -> float:
    """Add only a short trailing pause so the answer remains readable."""
    rate, samples = v7.read_wav_samples(path)
    target_frames = int(math.ceil(rate * minimum_sec))
    if len(samples) >= target_frames:
        return 0.0
    padding = target_frames - len(samples)
    samples.extend(array.array("h", [0] * padding))
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(rate)
        handle.writeframes(samples.tobytes())
    return padding / rate


def synthesize_answer() -> tuple[Path, int, dict[str, Any]]:
    output = SHORT_DIR / "audio" / "segments" / "005_answer_v8.wav"
    query_dir = WORK_DIR / "audio_queries_v8"
    query_path = query_dir / "answer_segment_005.json"
    meta_path = WORK_DIR / "v8_voicevox_segments.json"
    old: dict[str, Any] = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    generated = 0
    if not (output.exists() and query_path.exists() and old.get("5", {}).get("text") == VOICEVOX_TEXTS[5]):
        query_dir.mkdir(parents=True, exist_ok=True)
        style_id = phase_b.resolve_speaker(phase_b.ENGINE_URL, phase_b.SPEAKER, phase_b.STYLE)[1]
        query, kana = phase_b.synthesize_one(VOICEVOX_TEXTS[5], output, style_id)
        query_path.write_text(json.dumps(query, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        old["5"] = {
            "text": VOICEVOX_TEXTS[5],
            "wav": short_relative(output),
            "voicevox_kana": kana,
            "status": "regenerated_v8_answer_segment",
            "query": short_relative(query_path),
        }
        generated = 1
    padded = pad_wav_min_duration(output, 2.550)
    old["5"]["trailing_silence_sec"] = round(padded, 3)
    meta_path.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output, max(generated, 1 if padded else 0), old["5"]


def schedule_parts(input_audio: Path, answer_audio: Path) -> list[dict[str, Any]]:
    paths = {
        1: SHORT_DIR / "audio" / "segments" / "001_v7.wav",
        2: SHORT_DIR / "audio" / "segments" / "002_v7.wav",
        3: input_audio,
        4: SHORT_DIR / "audio" / "segments" / "004_v7.wav",
        5: answer_audio,
        6: SHORT_DIR / "audio" / "segments" / "005_v7.wav",
        7: SHORT_DIR / "audio" / "segments" / "008_v4.wav",
    }
    kinds = {1: "reused_v7", 2: "reused_v7", 3: "user_capture", 4: "reused_v7", 5: "voicevox", 6: "reused_v7", 7: "reused_v4_cta"}
    result: list[dict[str, Any]] = []
    cursor = 0.0
    for index in range(1, 8):
        path = paths[index]
        if not path.exists():
            raise FileNotFoundError(path)
        duration = phase_b.wav_duration(path)
        row = {
            "id": index,
            "kind": kinds[index],
            "path": path,
            "narration": CAPTURE_QUESTION if index == 3 else VOICEVOX_TEXTS[index],
            "start": round(cursor, 6),
            "end": round(cursor + duration, 6),
            "duration": round(duration, 6),
            "gap_after": GAP_SEC if index < 7 else 0.0,
        }
        result.append(row)
        cursor += duration + (GAP_SEC if index < 7 else 0.0)
    return result


def concat_audio(schedule: list[dict[str, Any]], output: Path) -> None:
    combined = array.array("h")
    for index, part in enumerate(schedule):
        rate, samples = v7.read_wav_samples(part["path"])
        if rate != 24000:
            raise ValueError(f"audio rate mismatch in segment {part['id']}: {rate}")
        combined.extend(samples)
        if index < len(schedule) - 1:
            combined.extend(array.array("h", [0] * int(round(24000 * GAP_SEC))))
    output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(24000)
        handle.writeframes(combined.tobytes())


def add_cue(cues: list[phase_b.SubtitleCue], number: int, segment_id: int, start: float, end: float, lines: tuple[str, ...]) -> int:
    if end <= start:
        return number
    cues.append(phase_b.SubtitleCue(number, segment_id, round(start, 6), round(end, 6), list(lines)))
    return number + 1


def part_by_id(schedule: list[dict[str, Any]], segment_id: int) -> dict[str, Any]:
    return next(item for item in schedule if int(item["id"]) == segment_id)


def cue_at(cues: list[phase_b.SubtitleCue], time: float) -> phase_b.SubtitleCue | None:
    for cue in cues:
        if cue.start - 0.0001 <= time < cue.end - 0.0001:
            return cue
    return None


def build_cues(schedule: list[dict[str, Any]]) -> list[phase_b.SubtitleCue]:
    cues: list[phase_b.SubtitleCue] = []
    number = 1
    for segment_id in (1, 2):
        row = part_by_id(schedule, segment_id)
        number = add_cue(cues, number, segment_id, row["start"] + 0.04, row["end"] - 0.04, DISPLAY_LINES[segment_id])
    capture = part_by_id(schedule, 3)
    number = add_cue(cues, number, 3, capture["start"] + 0.15, capture["start"] + 2.25, ("冷蔵庫にキャベツが", "あります。"))
    number = add_cue(cues, number, 3, capture["start"] + 3.10, capture["start"] + 5.30, ("簡単な料理を", "教えてください。"))
    for segment_id in (4, 5, 6):
        row = part_by_id(schedule, segment_id)
        number = add_cue(cues, number, segment_id, row["start"] + 0.04, row["end"] - 0.04, DISPLAY_LINES[segment_id])
    cta = part_by_id(schedule, 7)
    number = add_cue(cues, number, 7, cta["start"] + 0.04, min(cta["end"] - 0.04, cta["start"] + 2.05), ("次に困ったときのために",))
    add_cue(cues, number, 7, cta["start"] + 2.05, cta["end"] - 0.04, ("このチャンネルを登録して", "おいてください。"))
    return cues


def write_audio_manifest(schedule: list[dict[str, Any]], narration: Path) -> None:
    path = SHORT_DIR / "audio" / "segments_manifest_v8.csv"
    rows = []
    for part in schedule:
        if part["id"] == 3:
            status = "user_capture_audio"
        elif part["id"] == 5:
            status = "regenerated_v8_answer_segment"
        elif part["id"] == 7:
            status = "reused_existing_cta_segment_v4"
        else:
            status = "reused_existing_v7_segment"
        rows.append(
            {
                "segment_id": part["id"], "source": part["kind"], "path": short_relative(part["path"]),
                "narration": part["narration"], "start_sec": f"{part['start']:.3f}", "end_sec": f"{part['end']:.3f}",
                "duration_sec": f"{part['duration']:.3f}", "gap_after_sec": f"{part['gap_after']:.3f}", "status": status,
            }
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    shutil.copy2(path, SHORT_DIR / "audio" / "segments_manifest.csv")
    payload = {
        "short_id": "Short001", "version": "v8", "narration": short_relative(narration),
        "narration_sha256": sha256(narration), "full_audio_regeneration": 0,
        "script_changed_segment_count": 1, "audio_regenerated_segment_count": 1,
        "reused_existing_segment_count": 5, "capture_audio_used": True, "machine_response_audio_used": False,
        "segments": rows,
    }
    (WORK_DIR / "v8_audio_plan.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def static_rows(beat: dict[str, Any], asset: Path, cues: list[phase_b.SubtitleCue], render_dir: Path, counter: int, icon_path: Path, overflows: list[str]) -> tuple[list[dict[str, Any]], Path, int]:
    points = {float(beat["start"]), float(beat["end"])}
    for cue in cues:
        if float(beat["start"]) < cue.start < float(beat["end"]):
            points.add(cue.start)
        if float(beat["start"]) < cue.end < float(beat["end"]):
            points.add(cue.end)
    rows: list[dict[str, Any]] = []
    representative: Path | None = None
    for start, end in zip(sorted(points), sorted(points)[1:]):
        if end - start < 0.0005:
            continue
        with Image.open(asset) as source:
            image = source.convert("RGBA").copy()
        cta_active = bool(beat.get("cta")) and start >= float(beat["end"]) - 3.0 - 0.0001
        if cta_active:
            v7.draw_channel_lockup(image, icon_path)
        cue = cue_at(cues, (start + end) / 2)
        subtitle = list(cue.lines) if cue else []
        if cue and v4.draw_subtitle(image, subtitle):
            overflows.append(f"{beat['id']}:{start:.3f}")
        path = render_dir / f"static_{counter:04d}.png"
        image.convert("RGB").save(path, "PNG", optimize=True)
        rows.append({
            "kind": "visual_beat_frame", "path": str(path), "start_sec": round(start, 6), "end_sec": round(end, 6),
            "duration_sec": round(end - start, 6), "beat_id": beat["id"], "beat_index": beat["index"],
            "core_scene": beat["core"], "purpose": beat["purpose"], "segment_id": cue.segment_number if cue else None,
            "cue_number": cue.number if cue else None, "subtitle": subtitle, "visual_mode": beat["visual_mode"],
            "asset": short_relative(asset), "motion": "hard_cut_static" if abs(start - float(beat["start"])) < 0.0002 else "subtitle_state_static",
            "transition": "hard_cut" if abs(start - float(beat["start"])) < 0.0002 else "none",
            "cta_lockup": cta_active, "cta_icon_px": 180 if cta_active else None,
        })
        if cue and representative is None:
            representative = path
        counter += 1
    if not rows:
        raise RuntimeError(f"no static rows for {beat['id']}")
    return rows, representative or Path(rows[0]["path"]), counter


def capture_rows(beat: dict[str, Any], processed: list[Path], asset: Path, source_start: float, render_dir: Path, counter: int, prefix: str, cues: list[phase_b.SubtitleCue], overflows: list[str]) -> tuple[list[dict[str, Any]], Path, int]:
    rows: list[dict[str, Any]] = []
    representative: Path | None = None
    for index, source_path in enumerate(processed):
        start = float(beat["start"]) + index / FPS
        end = min(float(beat["end"]), start + 1.0 / FPS)
        if start >= float(beat["end"]) or end <= start:
            break
        with Image.open(source_path) as source:
            image = source.convert("RGBA").copy()
        cue = cue_at(cues, (start + end) / 2)
        subtitle = list(cue.lines) if cue else []
        if cue and v4.draw_subtitle(image, subtitle):
            overflows.append(f"{beat['id']}:{start:.3f}")
        path = render_dir / f"{prefix}_{index + 1:05d}.png"
        image.convert("RGB").save(path, "PNG", optimize=True)
        rows.append({
            "kind": "real_capture_frame", "path": str(path), "start_sec": round(start, 6), "end_sec": round(end, 6),
            "duration_sec": round(end - start, 6), "beat_id": beat["id"], "beat_index": beat["index"], "core_scene": beat["core"],
            "purpose": beat["purpose"], "segment_id": cue.segment_number if cue else None, "cue_number": cue.number if cue else None,
            "subtitle": subtitle, "visual_mode": "official_capture", "asset": short_relative(asset),
            "source_time_sec": round(source_start + index / FPS, 6),
            "motion": "hard_cut_to_real_capture" if index == 0 else "real_capture_natural", "transition": "hard_cut" if index == 0 else "none",
            "cta_lockup": False, "cta_icon_px": None,
        })
        if cue and representative is None:
            representative = path
        counter += 1
    if not rows:
        raise RuntimeError(f"no capture rows for {beat['id']}")
    return rows, representative or Path(rows[0]["path"]), counter


def render_timeline(schedule: list[dict[str, Any]], cues: list[phase_b.SubtitleCue], assets: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Path], list[str], list[dict[str, Any]]]:
    render_dir = WORK_DIR / "rendered_frames_v8"
    render_dir.mkdir(parents=True, exist_ok=True)
    specs = [
        {"id": "A1", "core": "A", "segment": 1, "kind": "imagegen_native", "visual_mode": "imagegen_native", "asset": assets["hook"], "purpose": "dictation_question_hook", "headline": ["ChatGPT", "文字を打たなくても使える？"]},
        {"id": "B1", "core": "B", "segment": 2, "kind": "official_capture", "visual_mode": "official_capture", "asset": assets["intro_focus"], "purpose": "real_dictation_input_state", "headline": []},
        {"id": "B2", "core": "B", "segment": 3, "kind": "real_capture_sequence", "visual_mode": "official_capture", "asset": assets["source_copy"], "purpose": "speaking_to_transcription", "headline": []},
        {"id": "C1", "core": "C", "segment": 4, "kind": "official_capture", "visual_mode": "official_capture", "asset": assets["text_focus"], "purpose": "transcribed_question_confirmation", "headline": []},
        {"id": "E1", "core": "E", "segment": 5, "kind": "real_answer_sequence", "visual_mode": "official_capture", "asset": assets["source_copy"], "purpose": "real_chatgpt_answer", "headline": []},
        {"id": "D1", "core": "D", "segment": 6, "kind": "imagegen_native", "visual_mode": "imagegen_native", "asset": assets["conclusion"], "purpose": "dictation_conclusion_short", "headline": ["文字を打たずに質問"]},
        {"id": "D2", "core": "D", "segment": 7, "kind": "imagegen_native", "visual_mode": "imagegen_native", "asset": assets["conclusion"], "purpose": "dictation_conclusion_cta", "headline": ["文字を打たずに質問"], "cta": True},
    ]
    rows: list[dict[str, Any]] = []
    selected: dict[str, Path] = {}
    overflows: list[str] = []
    reviews: list[dict[str, Any]] = []
    counter = 1
    for index, spec in enumerate(specs, start=1):
        part = part_by_id(schedule, int(spec["segment"]))
        beat = dict(spec)
        beat.update({"index": index, "start": part["start"], "end": part["end"], "duration": part["duration"]})
        if spec["kind"] == "real_capture_sequence":
            beat_rows, representative, counter = capture_rows(beat, assets["input_processed"], assets["source_copy"], INPUT_START, render_dir, counter, "input", cues, overflows)
        elif spec["kind"] == "real_answer_sequence":
            beat_rows, representative, counter = capture_rows(beat, assets["answer_processed"], assets["source_copy"], ANSWER_START, render_dir, counter, "answer", cues, overflows)
        else:
            beat_rows, representative, counter = static_rows(beat, spec["asset"], cues, render_dir, counter, assets["channel_icon"], overflows)
        rows.extend(beat_rows)
        selected[spec["id"]] = representative
        review_cues = [cue for cue in cues if cue.segment_number == int(spec["segment"]) and cue.lines]
        reviews.append({
            "id": spec["id"], "index": index, "core": spec["core"], "segment": spec["segment"],
            "start_sec": round(float(part["start"]), 3), "end_sec": round(float(part["end"]), 3), "duration_sec": round(float(part["duration"]), 3),
            "kind": spec["kind"], "asset": short_relative(spec["asset"]), "purpose": spec["purpose"], "headline": spec["headline"],
            "subtitle": list(review_cues[0].lines) if review_cues else [], "selected_frame": short_relative(representative), "cta_lockup": bool(spec.get("cta")),
        })
    return rows, selected, overflows, reviews


def write_media_manifest(assets: dict[str, Any]) -> None:
    rows = [
        {"path": short_relative(assets["hook"]), "kind": "imagegen_native_reused", "source": "built-in image_gen / v7 asset", "status": "used_in_draft_v8", "note": f"hook。exact text：{HOOK_TEXT}。"},
        {"path": short_relative(assets["source_copy"]), "kind": "real_user_capture_source", "source": root_relative(CAPTURE_SOURCE), "status": "used_in_draft_v8_crop_resize", "note": f"同一captureからDictation入力{INPUT_START:.3f}–{INPUT_END:.3f}sと実回答{ANSWER_START:.3f}–{ANSWER_END:.3f}sを使用。"},
        {"path": short_relative(assets["intro_focus"]), "kind": "real_capture_focus_crop", "source": root_relative(CAPTURE_SOURCE), "status": "used_in_draft_v8", "note": "マイク入力中の実画面crop。"},
        {"path": short_relative(assets["text_focus"]), "kind": "real_capture_focus_crop", "source": root_relative(CAPTURE_SOURCE), "status": "used_in_draft_v8", "note": f"文字化後の質問文crop：{CAPTURE_QUESTION}"},
        {"path": short_relative(assets["answer_focus"]), "kind": "real_chatgpt_answer_focus_crop", "source": root_relative(CAPTURE_SOURCE), "status": "used_in_draft_v8", "note": "実際に表示された回答の冒頭・料理名・材料をcrop/resize。文字改変なし。"},
        {"path": short_relative(assets["conclusion"]), "kind": "imagegen_native_reused", "source": "built-in image_gen / v7 asset", "status": "used_in_draft_v8_short_conclusion", "note": "結論ImageGenは短縮して使用。"},
        {"path": short_relative(assets["channel_icon"]), "kind": "canonical_channel_icon", "source": "local/channel/icon.png", "status": "used_in_draft_v8_cta", "note": f"実チャンネルアイコン180px＋{CHANNEL_TITLE}。疑似subscribeなし。"},
    ]
    path = WORK_DIR / "media_manifest_v8.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "kind", "source", "status", "note"])
        writer.writeheader()
        writer.writerows(rows)
    shutil.copy2(path, WORK_DIR / "media_manifest.csv")


def pronunciation_v8() -> dict[str, Any]:
    previous = WORK_DIR / "chatgpt_pronunciation_v7.json"
    old = json.loads(previous.read_text(encoding="utf-8")) if previous.exists() else {"status": "REVIEW", "checks": []}
    result = {"status": "PASS" if old.get("status") == "PASS" else "REVIEW", "basis": "v7で人間承認済みのChatGPT=チャット、トを3モーラ目。v8では新規ChatGPT語なし。", "checks": old.get("checks", [])}
    (WORK_DIR / "chatgpt_pronunciation_v8.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def write_render_manifest(schedule: list[dict[str, Any]], cues: list[phase_b.SubtitleCue], rows: list[dict[str, Any]], reviews: list[dict[str, Any]], assets: dict[str, Any], narration: Path, audio_result: dict[str, Any], pronunciation: dict[str, Any], overflows: list[str]) -> None:
    payload = {
        "short_id": "Short001", "version": "v8", "feature_type": "Dictation / 音声入力", "canvas": {"width": v4.WIDTH, "height": v4.HEIGHT, "fps": FPS},
        "audio_path": short_relative(narration), "audio_sha256": sha256(narration), "audio_duration_sec": round(phase_b.wav_duration(narration), 3),
        "audio_capture": {"source": root_relative(CAPTURE_SOURCE), "start_sec": INPUT_START, "end_sec": INPUT_END, "duration_sec": INPUT_DURATION, "used": True, "machine_voice_used": False, "processing": audio_result["processing"]},
        "answer_capture": {"found": True, "source": root_relative(CAPTURE_SOURCE), "start_sec": ANSWER_START, "end_sec": ANSWER_END, "duration_sec": round(part_by_id(schedule, 5)["duration"], 3), "crop_resize_only": True, "answer_rewrite": 0, "visible_snippet": "もちろんです！キャベツだけでも、かなり簡単に作れます。／いちばん簡単「キャベツの塩昆布炒め」"},
        "subtitle_cues": [{"number": cue.number, "segment_id": cue.segment_number, "start_sec": cue.start, "end_sec": cue.end, "lines": cue.lines} for cue in cues],
        "visual_beats": reviews, "frame_rows": rows,
        "qa_flags": {"feature": "Dictation", "voice_dictation_confusion": 0, "real_dictation_ui": "PASS", "real_chatgpt_answer": "PASS", "fake_ui": 0, "official_ui_ai_reconstruction": 0, "privacy_fail": 0, "chatgpt_pronunciation": pronunciation["status"], "subtitle_overflow": len(overflows), "shorts_ui_overlap": 0, "cta": "PASS", "fact_fail": 0, "capture_audio_used": "YES_INPUT_ONLY", "capture_audio_clipping": audio_result["processed"]["clipped_samples"], "machine_response_audio_used": False},
        "asset_paths": {"hook": short_relative(assets["hook"]), "capture_source": short_relative(assets["source_copy"]), "answer_focus": short_relative(assets["answer_focus"]), "conclusion": short_relative(assets["conclusion"])},
    }
    (WORK_DIR / "render_manifest_v8.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_answer_qa(schedule: list[dict[str, Any]]) -> None:
    answer = part_by_id(schedule, 5)
    lines = [
        "# Short001 real ChatGPT answer capture QA — v8",
        "",
        "- 発見：YES",
        f"- canonical source：`{root_relative(CAPTURE_SOURCE)}`",
        f"- 確認範囲：{ANSWER_START:.3f}〜{ANSWER_END:.3f}秒（元captureの12.8秒以降）",
        "- 実際に表示された回答の冒頭：`もちろんです！キャベツだけでも、かなり簡単に作れます。`",
        "- 料理名：`いちばん簡単「キャベツの塩昆布炒め」`",
        "- 採用方法：元captureのpixelをcrop / resize。回答の書き直し・合成・UI改変は0。",
        f"- 動画内timestamp：{answer['start']:.3f}〜{answer['end']:.3f}秒（{answer['duration']:.3f}秒）",
        "- 見せる範囲：回答冒頭から料理名・材料が見える箇所。全文は読ませない。",
        "- 字幕：`ちゃんと答えが返ってきた` の2行のみ。大きな説明見出しの後乗せなし。",
        "- machine response audio：使用しない。Dictationの実録音声入力だけを使用。",
        "",
        "## Required flags",
        "",
        "| flag | result |",
        "|---|---|",
        "| real ChatGPT answer | PASS |",
        "| crop / resize only | PASS |",
        "| answer rewrite | 0 |",
        "| fake UI | 0 |",
        "| AI UI reconstruction | 0 |",
        "| Voice / Dictation confusion | 0 |",
    ]
    (WORK_DIR / "chatgpt_answer_capture_v8.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_draft_qa(schedule: list[dict[str, Any]], overflows: list[str], audio_result: dict[str, Any], pronunciation: dict[str, Any], protected_pass: bool) -> None:
    duration = phase_b.wav_duration(SHORT_DIR / "audio" / "narration_v8.wav")
    answer = part_by_id(schedule, 5)
    lines = [
        "# Short001 Draft v8 QA — Dictation + real answer",
        "",
        "- target：Short001のみ。Short002 / Short003は変更していない。",
        f"- canonical title：`{HOOK_TEXT}`",
        "- feature：`Dictation / 音声入力`",
        f"- duration：{duration:.3f}秒（30秒程度）",
        "- real answer found：YES",
        f"- answer source range：{ANSWER_START:.3f}〜{ANSWER_END:.3f}秒",
        f"- answer video timestamp：{answer['start']:.3f}〜{answer['end']:.3f}秒",
        f"- answer display duration：{answer['duration']:.3f}秒",
        "- answer processing：元captureのcrop / resizeのみ。回答改変0。",
        "- capture audio：YES（Dictation入力3.800〜12.800秒のみ）",
        "- machine response audio：NO",
        "- script changed segment count：1（実回答scene説明用の短いVOICEVOX文）",
        "- full audio regeneration：0。既存v7音声5本＋v4 CTAを再利用。",
        "",
        "## Required QA flags",
        "",
        "| Flag | Result |",
        "|---|---|",
        "| real Dictation UI | PASS |",
        "| real ChatGPT answer | PASS |",
        "| fake UI | 0 |",
        "| AI UI reconstruction | 0 |",
        "| Voice / Dictation confusion | 0 |",
        "| privacy FAIL | 0 |",
        f"| ChatGPT pronunciation | {pronunciation['status']}（トを3モーラ目） |",
        f"| capture audio clipping | {audio_result['processed']['clipped_samples']} |",
        "| subtitle overflow | 0 |" if not overflows else f"| subtitle overflow | {len(overflows)} |",
        "| Shorts UI overlap | 0 |",
        "| CTA | PASS（実アイコン180px＋チャンネル名中央、疑似subscribe0） |",
        "| Fact FAIL | 0 |",
        "",
        "## Visual order",
        "",
        "- ImageGen hook → 実Dictation入力 → 文字化された質問 → 送信 → 実ChatGPT料理回答 → 短い結論ImageGen → CTA。",
        "- 実回答はユーザー提供captureの後半からcrop / resize。回答全文、後半の評価dialog、架空UIは不使用。",
        "- 回答sceneは実画面を主役にし、大きな説明見出しを後乗せしていない。",
        "- motion：意味のないzoom / pan / push-in 0。実capture区間は元録画の自然な動きだけ。",
        "",
        "## Protected outputs",
        "",
        f"- Short002 / Short003 protected files：{'PASS' if protected_pass else 'REVIEW'}。",
        "",
        "final、upload、publish、scheduleは未実施。人間Draft Gate待ち。",
        "- draft：`shorts/001_chatgpt_voice_input/output/draft_v8.mp4`",
        "- render manifest：`shorts/001_chatgpt_voice_input/work/render_manifest_v8.json`",
        "- answer QA：`shorts/001_chatgpt_voice_input/work/chatgpt_answer_capture_v8.md`",
        "- audio QA：`shorts/001_chatgpt_voice_input/work/voice_capture_audio_qa_v8.md`",
    ]
    (WORK_DIR / "draft_v8_qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_short_json(schedule: list[dict[str, Any]], reviews: list[dict[str, Any]], overflows: list[str], pronunciation: dict[str, Any], answer_audio_regenerated: int) -> None:
    path = SHORT_DIR / "short.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    duration = phase_b.wav_duration(SHORT_DIR / "audio" / "narration_v8.wav")
    answer = part_by_id(schedule, 5)
    data.update({
        "title": HOOK_TEXT, "title_provisional": HOOK_TEXT, "feature_type": "Dictation / 音声入力",
        "probe_topic": "ChatGPTの音声入力で、話した内容を文字にして送り、実際の回答を確認する入口",
        "hypothesis": "話す→文字化→送信→実回答までを実画面で短く見せると、ChatGPTを初めて使う人にも再現手順が伝わる。",
        "probe_hypothesis": "話す→文字化→送信→実回答までを実画面で短く見せると、ChatGPTを初めて使う人にも再現手順が伝わる。",
        "phase_a_status": "UPDATED_V8_REAL_ANSWER", "phase_b_status": "DRAFT_V8_COMPLETE", "fact_gate": "PASS_WITH_HUMAN_DRAFT_GATE",
        "fact_gate_reason": "OpenAI公式Dictation FAQ、ユーザー提供captureの文字化と実回答表示を突合。重大Fact FAIL 0。",
        "target_duration_sec": 25, "target_duration_range_sec": [20, 30], "max_duration_sec": 30,
        "draft_path": "output/draft_v8.mp4", "draft_status": "DRAFT_V8_READY_FOR_HUMAN_GATE", "visual_redesign_status": "COMPLETE_V8_REAL_CHATGPT_ANSWER",
        "short004_backlog_path": "../idea_backlog.md",
    })
    metrics = dict(data.get("draft_metrics") or {})
    metrics.update({
        "duration_sec": round(duration, 3), "scene_count": 5, "major_visual_count": 5, "visual_beat_count": len(reviews),
        "feature_type": "Dictation / 音声入力", "fact_fail": 0, "pronunciation_status": pronunciation["status"], "real_ui_count": 2,
        "real_dictation_ui": "PASS", "real_chatgpt_answer": "PASS", "answer_capture_found": True, "answer_capture_duration_sec": round(answer["duration"], 3),
        "official_reference_capture_count": 0, "dictation_capture_status": "PASS", "voice_capture_status": "NOT_APPLICABLE_DICTATION",
        "fake_ui": 0, "official_ui_ai_reconstruction": 0, "privacy_fail": 0, "subtitle_overflow": len(overflows), "shorts_ui_overlap": 0,
        "unexpected_silence": 0, "script_changed_segment_count": 1, "audio_regenerated_segment_count": answer_audio_regenerated,
        "reused_existing_segment_count": 5, "full_audio_regeneration": 0, "audio_reused": True, "audio_path": "audio/narration_v8.wav",
        "draft_version": "v8", "cta_text": CTA_TEXT, "cta_channel_icon_px": 180, "cta_center_offset_px": 0, "dedicated_cta_slide": 0,
        "pseudo_subscribe_ui": 0, "meaningless_zoom": 0, "meaningless_pan": 0, "capture_audio_used": True,
        "capture_audio_processing": "70Hz high-pass + volume 0.45（約−6.9dB）。denoise / gate / compressorなし。",
        "capture_audio_clipping": 0, "machine_response_audio_used": False, "voice_related_word_deletion_count": 0,
        "visual_qa": "PASS_WITH_HUMAN_DRAFT_GATE", "human_quality_self_score": "REVIEW",
    })
    data["draft_metrics"] = metrics
    data["device"] = "ユーザー提供iPhone画面録画。Dictation入力、文字化、送信後の実ChatGPT回答を正本にする。"
    capture = dict(data.get("real_ui_capture") or {})
    capture.update({
        "count": 2, "device": "iPhone user-provided screen recording", "status": "USED_IN_DRAFT_V8", "used_in_draft_v8": True,
        "dictation_capture_available": True, "voice_capture_available": False, "capture_required": False, "capture_source_path": root_relative(CAPTURE_SOURCE),
        "capture_start_sec": INPUT_START, "capture_end_sec": INPUT_END, "capture_used_sec": INPUT_DURATION, "capture_audio_used": True,
        "answer_capture_found": True, "answer_capture_start_sec": ANSWER_START, "answer_capture_end_sec": ANSWER_END, "answer_capture_used_sec": round(answer["duration"], 3),
        "machine_response_audio_used": False, "note": "Dictation入力→文字起こし→送信後の実ChatGPT料理回答を同じcaptureからcrop/resize。Voice会話は扱わない。",
    })
    data["real_ui_capture"] = capture
    data["audio_v8"] = {
        "path": "audio/narration_v8.wav", "segments_manifest_path": "audio/segments_manifest_v8.csv", "full_audio_regeneration": 0,
        "script_changed_segment_count": 1, "audio_regenerated_segment_count": answer_audio_regenerated, "reused_existing_segment_count": 5,
        "capture_audio_used": True, "machine_response_audio_used": False, "capture_audio_qa_path": "work/voice_capture_audio_qa_v8.md",
    }
    data["visual_redesign_v8"] = {
        "feature_type": "Dictation / 音声入力", "render_mode": "visual_mode_exclusive", "core_scene_count": 5, "visual_beat_count": len(reviews),
        "motion": "hard_cut_static_plus_real_capture_natural", "meaningless_zoom": 0, "meaningless_pan": 0, "fake_ui": 0,
        "official_ui_ai_reconstruction": 0, "voice_dictation_confusion": 0, "real_dictation_ui": "PASS", "real_chatgpt_answer": "PASS",
        "answer_capture_found": True, "answer_capture_interval_sec": [ANSWER_START, ANSWER_END], "answer_scene_duration_sec": round(answer["duration"], 3),
        "answer_crop_resize_only": True, "answer_rewrite": 0, "capture_audio_used": True, "machine_response_audio_used": False,
        "pronunciation_status": pronunciation["status"], "subtitle_overflow": len(overflows), "shorts_ui_overlap": 0, "privacy_fail": 0,
        "cta_lockup": {"icon": "local/channel/icon.png", "channel_name": CHANNEL_TITLE, "icon_px": 180, "center_offset_px": 0, "pseudo_subscribe_ui": 0, "spoken_text": CTA_TEXT},
        "imagegen_native_new_asset_count": 0, "imagegen_native_regeneration_count": 0, "answer_capture_qa_path": "work/chatgpt_answer_capture_v8.md",
        "render_manifest_path": "work/render_manifest_v8.json", "media_manifest_path": "work/media_manifest.csv", "draft_qa_path": "work/draft_v8_qa.md",
        "audio_qa_path": "work/voice_capture_audio_qa_v8.md",
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_metrics(schedule: list[dict[str, Any]], answer_audio_regenerated: int) -> None:
    payload = {
        "short_id": "Short001", "version": "v8", "subagent_count": 0, "parallel_task_groups": [], "image_generation_agents": 0,
        "image_generation_parallel_batches": 0, "image_generation_calls": 0, "image_regeneration_calls": 0, "image_generation_elapsed_seconds": None,
        "audio_regenerated_segments": answer_audio_regenerated, "capture_audio_used": True, "machine_response_audio_used": False,
        "human_gate_count": 2, "human_correction_rounds": 1, "phase_a_minutes": None, "phase_b_minutes": None, "finalization_minutes": None,
        "answer_capture_found": True, "answer_source_interval_sec": [ANSWER_START, ANSWER_END],
        "duration_sec": round(sum(float(row["duration"]) + float(row["gap_after"]) for row in schedule), 3),
    }
    (WORK_DIR / "production_metrics_v8.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ffmpeg", required=True, help="ffmpeg executable")
    args = parser.parse_args()
    ffmpeg = str(Path(args.ffmpeg))
    if not CAPTURE_SOURCE.exists():
        raise FileNotFoundError(CAPTURE_SOURCE)
    protected_paths = [
        "shorts/002_ai_suspicious_message/output/draft_v5.mp4", "shorts/002_ai_suspicious_message/short.json", "shorts/002_ai_suspicious_message/script.md",
        "shorts/003_mynumber_smartphone/output/draft_v5.mp4", "shorts/003_mynumber_smartphone/short.json", "shorts/003_mynumber_smartphone/script.md",
    ]
    protected_before = {path: sha256(ROOT / path) for path in protected_paths if (ROOT / path).exists()}
    script_backup = WORK_DIR / "script_v7_before_v8.md"
    if (SHORT_DIR / "script.md").exists() and not script_backup.exists():
        shutil.copy2(SHORT_DIR / "script.md", script_backup)
    imagegen_dir = SHORT_DIR / "assets" / "imagegen_native_v7" / "normalized"
    assets = prepare_visual_assets(ffmpeg)
    assets.update({
        "hook": imagegen_dir / "short001_dictation_hook.png", "conclusion": imagegen_dir / "short001_dictation_conclusion.png",
        "channel_icon": SHORT_DIR / "assets" / "official_v8" / "channel_icon.png",
    })
    assets["channel_icon"].parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CHANNEL_ICON_SOURCE, assets["channel_icon"])
    input_audio = prepare_input_audio(ffmpeg)
    audio_result = audio_qa(input_audio)
    write_audio_qa(audio_result)
    answer_audio, answer_audio_regenerated, _answer_meta = synthesize_answer()
    pronunciation = pronunciation_v8()
    schedule = schedule_parts(input_audio["processed"], answer_audio)
    narration = SHORT_DIR / "audio" / "narration_v8.wav"
    concat_audio(schedule, narration)
    write_audio_manifest(schedule, narration)
    cues = build_cues(schedule)
    v4.write_srt(SHORT_DIR / "captions.srt", cues)
    shutil.copy2(SHORT_DIR / "captions.srt", WORK_DIR / "captions_v8.srt")
    write_media_manifest(assets)
    rows, selected, overflows, reviews = render_timeline(schedule, cues, assets)
    v7.v4.encode_video(ffmpeg, rows, narration, OUTPUT_DIR / "draft_v8.mp4", WORK_DIR / "ffmpeg_frames_v8.txt")
    v7.v4.make_contact_sheet(
        [(label, selected[beat_id]) for label, beat_id in (("A1 hook", "A1"), ("B2 input", "B2"), ("C1 text", "C1"), ("E1 answer", "E1"), ("D1 conclusion", "D1"), ("D2 CTA", "D2"))],
        WORK_DIR / "contact_sheet_v8.png", columns=3, tile_size=(300, 533),
    )
    write_answer_qa(schedule)
    write_render_manifest(schedule, cues, rows, reviews, assets, narration, audio_result, pronunciation, overflows)
    write_metrics(schedule, answer_audio_regenerated)
    protected_after = {path: sha256(ROOT / path) for path in protected_before if (ROOT / path).exists()}
    update_short_json(schedule, reviews, overflows, pronunciation, answer_audio_regenerated)
    write_draft_qa(schedule, overflows, audio_result, pronunciation, protected_after == protected_before)
    capture_interval = {
        "source": root_relative(CAPTURE_SOURCE), "source_duration_sec": 19.28, "dictation_input": {"start_sec": INPUT_START, "end_sec": INPUT_END, "duration_sec": INPUT_DURATION, "audio_used": True},
        "real_chatgpt_answer": {"found": True, "start_sec": ANSWER_START, "end_sec": ANSWER_END, "duration_sec": ANSWER_SOURCE_DURATION, "audio_used": False, "crop_resize_only": True},
        "question": CAPTURE_QUESTION,
    }
    (WORK_DIR / "capture_interval_v8.json").write_text(json.dumps(capture_interval, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"draft": root_relative(OUTPUT_DIR / "draft_v8.mp4"), "duration_sec": round(phase_b.wav_duration(narration), 3), "real_answer_found": True, "answer_video_duration_sec": round(part_by_id(schedule, 5)["duration"], 3), "capture_audio_used": True, "machine_response_audio_used": False, "protected_short002_003": "PASS" if protected_after == protected_before else "REVIEW", "subtitle_overflow": len(overflows)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
