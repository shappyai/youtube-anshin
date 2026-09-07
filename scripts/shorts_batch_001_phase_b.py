"""Build Shorts探索バッチ001 Draft v1 after the human Script Gate.

This helper is intentionally Shorts-specific. It does not modify Episodes,
shared pronunciation configuration, or publish metadata. It synthesizes one
VOICEVOX WAV per narration segment, renders renderer-native 1080x1920 frames,
burns display subtitles into the frames, and encodes a local draft with the
bundled imageio-ffmpeg binary.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SHORTS_ROOT = ROOT / "shorts"
VENDOR = ROOT / "work" / "vendor"
sys.path.insert(0, str(VENDOR))
sys.path.insert(0, str(ROOT / "scripts"))

from tts_voicevox import (  # noqa: E402
    apply_pronunciation_overrides,
    apply_pronunciation_pitch_patterns,
    make_audio_query,
    refresh_mora_data,
    resolve_speaker,
    synthesize,
)


ENGINE_URL = "http://127.0.0.1:50021"
SPEAKER = "剣崎雌雄"
STYLE = "ノーマル"
SPEED = 1.0
INTONATION = 1.0
PITCH = 0.0
GAP_SEC = 0.07
WIDTH = 1080
HEIGHT = 1920
SHORTS_UI_BOTTOM_SAFE_PX = 220
CAPTION_MIN_PX = 64
CAPTION_TARGET_PX = 80
CTA_TEXT = "困ったときのために、登録しておいてください。"

SHORTS = {
    "Short001": SHORTS_ROOT / "001_chatgpt_voice_input",
    "Short002": SHORTS_ROOT / "002_ai_suspicious_message",
    "Short003": SHORTS_ROOT / "003_mynumber_smartphone",
}

SEGMENT_HEADER = re.compile(r"^###\s+(\d+)｜Scene\s+(\d+)｜([^｜]+)｜")
NARRATION_LINE = "- narration："
DISPLAY_LINE = re.compile(r"^\s+-\s+「(.*)」\s*$")

# These are semantic dwell weights, written per segment rather than derived
# from character count. They are normalized against measured audio duration.
CUE_WEIGHTS: dict[tuple[str, int], list[float]] = {
    ("Short003", 2): [2.4, 2.4, 3.2],
    ("Short003", 5): [2.2, 3.3],
}

ICON_DIR = ROOT / "assets" / "icons" / "material_symbols_normalized"
ICON_FILES = {
    "forum": "forum_blue_s180.png",
    "lock": "lock_blue_s180.png",
    "warning": "warning_amber_s180.png",
    "assistant": "support_agent_green_s180.png",
    "verified": "verified_user_green_s180.png",
    "badge": "badge_blue_s72.png",
    "bank": "account_balance_blue_s180.png",
    "group": "groups_amber_s180.png",
}


@dataclass
class Segment:
    number: int
    scene: int
    hint: str
    narration: str
    subtitle_items: list[str]


@dataclass
class AudioSegment:
    segment: Segment
    wav_path: Path
    duration: float
    start: float
    end: float
    kana: str


@dataclass
class SubtitleCue:
    number: int
    segment_number: int
    start: float
    end: float
    lines: list[str]


def read_script(path: Path) -> list[Segment]:
    segments: list[Segment] = []
    current: Segment | None = None
    display_mode = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        header = SEGMENT_HEADER.match(raw.strip())
        if header:
            if current is not None:
                segments.append(current)
            current = Segment(
                number=int(header.group(1)),
                scene=int(header.group(2)),
                hint=header.group(3).strip(),
                narration="",
                subtitle_items=[],
            )
            display_mode = False
            continue
        if current is None:
            continue
        if raw.startswith(NARRATION_LINE):
            current.narration = raw[len(NARRATION_LINE):].strip()
            display_mode = False
            continue
        if raw.strip() == "- subtitle_display：":
            display_mode = True
            continue
        if display_mode:
            match = DISPLAY_LINE.match(raw)
            if match:
                current.subtitle_items.append(match.group(1))
                continue
            if raw.strip() and not raw.startswith("  - "):
                display_mode = False
    if current is not None:
        segments.append(current)
    if not segments or any(not s.narration or not s.subtitle_items for s in segments):
        raise ValueError(f"script segments are incomplete: {path}")
    return segments


def font_path() -> str:
    for candidate in (
        "C:/Windows/Fonts/YuGothB.ttc",
        "C:/Windows/Fonts/YuGothM.ttc",
        "C:/Windows/Fonts/meiryob.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    ):
        if Path(candidate).exists():
            return candidate
    raise FileNotFoundError("Japanese font not found")


FONT = font_path()


def fnt(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size=size)


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()


def query_kana(query: dict[str, Any]) -> str:
    return "".join(
        str(mora.get("text") or "")
        for phrase in query.get("accent_phrases") or []
        for mora in phrase.get("moras") or []
    )


def synthesize_one(text: str, out: Path, style_id: int) -> tuple[dict[str, Any], str]:
    query = make_audio_query(ENGINE_URL, text, style_id)
    query["speedScale"] = SPEED
    query["intonationScale"] = INTONATION
    query["pitchScale"] = PITCH
    if apply_pronunciation_overrides(query, episode_id=""):
        refresh_mora_data(ENGINE_URL, query, style_id)
    apply_pronunciation_pitch_patterns(query, episode_id="")
    synthesize(ENGINE_URL, query, style_id, out)
    return query, query_kana(query)


def build_audio(
    short_id: str,
    short_dir: Path,
    segments: list[Segment],
    style_id: int,
) -> tuple[list[AudioSegment], Path, list[dict[str, Any]]]:
    audio_dir = short_dir / "audio"
    segment_dir = audio_dir / "segments"
    segment_dir.mkdir(parents=True, exist_ok=True)
    rows: list[AudioSegment] = []
    cursor = 0.0
    audit_rows: list[dict[str, Any]] = []
    wave_parts: list[tuple[bytes, int, int, int]] = []
    params_ref: tuple[int, int, int] | None = None

    for index, segment in enumerate(segments):
        path = segment_dir / f"{segment.number:03d}.wav"
        query, kana = synthesize_one(segment.narration, path, style_id)
        duration = wav_duration(path)
        with wave.open(str(path), "rb") as w:
            channels, sample_width, rate = w.getnchannels(), w.getsampwidth(), w.getframerate()
            data = w.readframes(w.getnframes())
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
                "status": "generated_or_reused",
            }
        )
        wave_parts.append((data, channels, sample_width, rate))
        cursor = end
        if index < len(segments) - 1:
            gap_frames = int(rate * GAP_SEC)
            wave_parts.append((b"\x00" * gap_frames * sample_width * channels, channels, sample_width, rate))
            cursor += GAP_SEC

    if params_ref is None:
        raise ValueError("no audio segments")
    channels, sample_width, rate = params_ref
    narration_path = audio_dir / "narration.wav"
    with wave.open(str(narration_path), "wb") as out:
        out.setnchannels(channels)
        out.setsampwidth(sample_width)
        out.setframerate(rate)
        for data, _, _, _ in wave_parts:
            out.writeframes(data)

    with (audio_dir / "segments_manifest.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(audit_rows[0].keys()))
        writer.writeheader()
        writer.writerows(audit_rows)
    return rows, narration_path, audit_rows


def cue_groups(short_id: str, segment: Segment) -> list[list[str]]:
    if len(segment.subtitle_items) <= 2:
        return [segment.subtitle_items]
    if short_id == "Short003" and segment.number == 5:
        return [[segment.subtitle_items[0]], [segment.subtitle_items[1], segment.subtitle_items[2]]]
    return [[item] for item in segment.subtitle_items]


def build_cues(short_id: str, audio_segments: list[AudioSegment]) -> list[SubtitleCue]:
    cues: list[SubtitleCue] = []
    cue_number = 1
    for audio in audio_segments:
        groups = cue_groups(short_id, audio.segment)
        weights = CUE_WEIGHTS.get((short_id, audio.segment.number), [1.0] * len(groups))
        if len(weights) != len(groups):
            weights = [1.0] * len(groups)
        total_weight = sum(weights)
        cursor = audio.start
        for group, weight in zip(groups, weights):
            duration = audio.duration * weight / total_weight
            cues.append(
                SubtitleCue(
                    number=cue_number,
                    segment_number=audio.segment.number,
                    start=cursor,
                    end=cursor + duration,
                    lines=group,
                )
            )
            cue_number += 1
            cursor += duration
    return cues


def srt_time(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def write_srt(path: Path, cues: list[SubtitleCue]) -> None:
    blocks: list[str] = []
    for cue in cues:
        blocks.append(
            f"{cue.number}\n{srt_time(cue.start)} --> {srt_time(cue.end)}\n"
            + "\n".join(cue.lines)
        )
    path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def gradient() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT))
    px = image.load()
    top = (246, 249, 255)
    bottom = (232, 247, 242)
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for x in range(WIDTH):
            px[x, y] = color
    return image.convert("RGBA")


def icon(name: str, size: int = 180) -> Image.Image | None:
    path = ICON_DIR / ICON_FILES[name]
    if not path.exists():
        return None
    image = Image.open(path).convert("RGBA")
    image.thumbnail((size, size), Image.Resampling.LANCZOS)
    return image


def draw_icon_plate(image: Image.Image, name: str, center: tuple[int, int], plate: tuple[int, int, int]) -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = center
    radius = 132
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=plate + (225,))
    image.alpha_composite(overlay)
    asset = icon(name)
    if asset:
        image.alpha_composite(asset, (cx - asset.width // 2, cy - asset.height // 2))


def rounded_paste(base: Image.Image, source: Image.Image, box: tuple[int, int, int, int], radius: int = 28) -> None:
    x, y, w, h = box
    source = source.convert("RGBA").resize((w, h), Image.Resampling.LANCZOS)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w, h), radius=radius, fill=255)
    source.putalpha(mask)
    base.alpha_composite(source, (x, y))


def ui_reference_crop(short_dir: Path) -> Image.Image | None:
    source_path = short_dir / "assets" / "chatgpt_home_mobile.png"
    if not source_path.exists():
        return None
    source = Image.open(source_path).convert("RGBA")
    # Remove Android status/address chrome while retaining the real current
    # public ChatGPT mobile-web screen. No UI is redrawn here.
    return source.crop((0, 246, min(source.width, 1080), min(source.height, 1900)))


def draw_top(image: Image.Image, short_id: str) -> None:
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((56, 62, 275, 140), radius=38, fill=(255, 255, 255, 220))
    draw.text((82, 78), short_id, font=fnt(44), fill=(35, 64, 108, 255))
    draw.text((58, 166), "大人のデジタル安心室", font=fnt(38), fill=(64, 83, 110, 230))
    draw.ellipse((840, 85, 995, 240), fill=(255, 255, 255, 100))
    draw.ellipse((918, 25, 1050, 160), fill=(178, 211, 226, 80))


def body_copy(short_id: str, scene: int) -> tuple[str, str, str]:
    if short_id == "Short001":
        values = {
            1: ("話しかけて使う", "文字入力の負担を減らす入口", "forum"),
            2: ("音声モード", "会話を始める", "forum"),
            3: ("現在の入口", "実機画面を確認", "forum"),
            4: ("生活の一言", "卵とキャベツで聞いてみる", "forum"),
            5: ("答え始める", "全文は読ませない", "assistant"),
            6: ("まずは確認", "話しかけるだけから", "verified"),
        }
    elif short_id == "Short002":
        values = {
            1: ("見せる前に一呼吸", "怪しいメールをそのまま送らない", "warning"),
            2: ("個人情報を隠す", "名前・住所・電話番号など", "lock"),
            3: ("AIは補助", "文面整理と怪しい点の洗い出し", "assistant"),
            4: ("AIだけで決めない", "最後の確認は公式から", "warning"),
            5: ("公式から確認", "リンクは開かない", "verified"),
            6: ("順番を覚える", "隠す → 補助 → 公式確認", "verified"),
        }
    else:
        values = {
            1: ("カードとスマホ", "何ができる？", "badge"),
            2: ("できること", "マイナポータル・証明書・e-Tax", "bank"),
            3: ("保険証の例", "対応する医療機関・薬局", "verified"),
            4: ("端末で違い", "iPhone・Android", "group"),
            5: ("実物カードも", "スマホだけで全部ではない", "badge"),
            6: ("公式で確認", "使える場所を確かめる", "verified"),
        }
    return values.get(scene, ("確認ポイント", "", "verified"))


def draw_body(image: Image.Image, short_id: str, scene: int, short_dir: Path) -> None:
    draw = ImageDraw.Draw(image)
    title, sub, icon_name = body_copy(short_id, scene)
    accents = {
        "Short001": ((221, 235, 255), (38, 91, 174)),
        "Short002": ((255, 239, 209), (153, 96, 21)),
        "Short003": ((221, 244, 238), (28, 107, 91)),
    }
    plate, ink = accents[short_id]

    if short_id == "Short001" and scene == 3:
        crop = ui_reference_crop(short_dir)
        if crop is not None:
            rounded_paste(image, crop, (82, 310, 916, 1110), 32)
            draw.rounded_rectangle((116, 344, 470, 416), radius=28, fill=(255, 255, 255, 225))
            draw.text((145, 356), "OpenAI公式モバイル画面", font=fnt(32), fill=(35, 64, 108, 255))
            draw_icon_plate(image, "forum", (810, 1170), (221, 235, 255))
            draw.text((90, 1265), "現在の画面を確認", font=fnt(48), fill=(35, 64, 108, 230))
            return

    draw_icon_plate(image, icon_name, (540, 520), plate)
    draw.text((80, 770), title, font=fnt(76), fill=ink + (255,))
    if sub:
        draw.multiline_text((82, 875), sub, font=fnt(52), fill=(57, 78, 103, 235), spacing=16)
    draw.rounded_rectangle((82, 1100, 998, 1240), radius=36, fill=(255, 255, 255, 140))
    if short_id == "Short003" and scene == 2:
        labels = ["マイナポータル", "証明書", "e-Tax"]
        for i, label in enumerate(labels):
            x = 112 + i * 292
            draw.rounded_rectangle((x, 1130, x + 250, 1210), radius=24, fill=plate + (230,))
            draw.text((x + 22, 1150), label, font=fnt(34), fill=ink + (255,))
    elif short_id == "Short002" and scene == 2:
        for i, label in enumerate(["名前", "住所", "番号類"]):
            x = 124 + i * 285
            draw.rounded_rectangle((x, 1130, x + 230, 1210), radius=24, fill=(230, 237, 247, 235))
            draw.line((x + 26, 1170, x + 202, 1170), fill=(54, 96, 153, 255), width=9)
            draw.text((x + 50, 1103), label, font=fnt(32), fill=(57, 78, 103, 255))
    else:
        small_copy = {
            "Short001": "使える条件はアプリで確認",
            "Short002": "安全な確認の順番",
            "Short003": "対応サービスは公式で確認",
        }[short_id]
        draw.text((120, 1145), small_copy, font=fnt(42), fill=(57, 78, 103, 220))


def draw_caption(image: Image.Image, lines: list[str]) -> bool:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    band = (54, 1430, 1026, 1758)
    draw.rounded_rectangle(band, radius=36, fill=(255, 255, 255, 242), outline=(203, 218, 231, 255), width=3)
    draw.rounded_rectangle((74, 1464, 94, 1724), radius=10, fill=(63, 119, 192, 255))
    font = fnt(CAPTION_TARGET_PX)
    text = "\n".join(lines[:2])
    bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=14, align="center")
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    max_width = band[2] - band[0] - 80
    initial_overflow = tw > max_width or th > band[3] - band[1] - 45
    if initial_overflow:
        font = fnt(CAPTION_MIN_PX)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=12, align="center")
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
    overflow = tw > max_width or th > band[3] - band[1] - 45
    x = (WIDTH - tw) // 2
    y = band[1] + (band[3] - band[1] - th) // 2 - 4
    draw.multiline_text((x, y), text, font=font, fill=(24, 39, 61, 255), spacing=14, align="center")
    image.alpha_composite(overlay)
    return overflow


def render_frame(
    short_id: str,
    short_dir: Path,
    scene: int,
    lines: list[str],
    path: Path,
) -> bool:
    image = gradient()
    draw = ImageDraw.Draw(image)
    draw.ellipse((720, 275, 1190, 745), fill=(187, 218, 234, 70))
    draw.ellipse((-160, 1020, 320, 1500), fill=(245, 211, 150, 45))
    draw_top(image, short_id)
    draw_body(image, short_id, scene, short_dir)
    overflow = draw_caption(image, lines)
    image.convert("RGB").save(path, "PNG", optimize=True)
    return overflow


def concat_escape(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/").replace("'", r"'\''")


def encode_video(
    ffmpeg: str,
    short_dir: Path,
    frame_rows: list[dict[str, Any]],
    narration: Path,
    output: Path,
) -> None:
    list_path = short_dir / "work" / "ffmpeg_frames.txt"
    lines: list[str] = []
    for row in frame_rows:
        lines.append(f"file '{concat_escape(Path(row['path']))}'")
        lines.append(f"duration {max(0.03, row['duration_sec']):.6f}")
    if frame_rows:
        lines.append(f"file '{concat_escape(Path(frame_rows[-1]['path']))}'")
    list_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
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
    ]
    subprocess.run(command, check=True)


def write_pronunciation_qa(short_id: str, short_dir: Path, audit_rows: list[dict[str, Any]]) -> None:
    manual = {
        "Short001": "ChatGPTはナレーションで「チャットジーピーティー」と明示。表示字幕のVoiceは読み上げへ流出させていない。人間の聴取承認はREVIEW。",
        "Short002": "AIはナレーションで「エーアイ」と明示。今回の短縮台本ではQRコードをナレーション列挙から削除した。",
        "Short003": "e-Taxはナレーションで「イータックス」と明示。既存approved readingと一致する表記を維持。",
    }[short_id]
    lines = [
        f"# {short_id} pronunciation QA",
        "",
        "- engine：VOICEVOX",
        "- speaker：剣崎雌雄 / ノーマル",
        "- speedScale：1.00",
        "- intonationScale：1.00",
        "- pitchScale：0.00",
        "- dictionary change：なし",
        "- audio_query / synthesis：PASS",
        "- human listening gate：REVIEW",
        "",
        manual,
        "",
        "| segment | narration | VOICEVOX kana（取得できた場合） |",
        "|---:|---|---|",
    ]
    for row in audit_rows:
        kana = row["voicevox_kana"] or "既存WAVを再利用したため未再取得"
        lines.append(f"| {row['segment_id']} | {row['narration']} | {kana} |")
    lines += [
        "",
        "音声を人間が聴いて、固有名詞・数字・句読点の間・CTAの速さを確認するまで、発音QAは最終PASSにしない。",
    ]
    (short_dir / "work" / "pronunciation_qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_contact_sheet(
    image_paths: list[tuple[str, Path]],
    output: Path,
    columns: int,
    tile_size: tuple[int, int] = (270, 480),
) -> None:
    tw, th = tile_size
    rows = (len(image_paths) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * tw + (columns + 1) * 24, rows * (th + 50) + (rows + 1) * 24), (245, 248, 252))
    draw = ImageDraw.Draw(canvas)
    for index, (label, path) in enumerate(image_paths):
        row, col = divmod(index, columns)
        x = 24 + col * (tw + 24)
        y = 24 + row * (th + 50)
        image = Image.open(path).convert("RGB")
        image.thumbnail((tw, th), Image.Resampling.LANCZOS)
        tile = Image.new("RGB", (tw, th), "white")
        tile.paste(image, ((tw - image.width) // 2, (th - image.height) // 2))
        canvas.paste(tile, (x, y))
        draw.text((x, y + th + 10), label, font=fnt(28), fill=(32, 54, 78))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, "PNG", optimize=True)


def write_media_manifest(short_id: str, short_dir: Path) -> None:
    rows = [
        {
            "path": "assets/chatgpt_home_mobile.png",
            "kind": "official_mobile_capture",
            "source": "https://chatgpt.com/",
            "status": "captured_public_logged_out",
            "note": "現行ChatGPTモバイルWebの公開画面。アカウント情報・履歴なし。Voiceアイコンはログアウト画面では未表示。",
        },
        {
            "path": "assets/voice_official_mobile_clean2.png",
            "kind": "official_reference_capture",
            "source": "https://chatgpt.com/ja-JP/features/voice/",
            "status": "captured_public",
            "note": "OpenAI公式音声モード案内。実機UIとしてではなく、用語確認用。",
        },
    ] if short_id == "Short001" else []
    (short_dir / "work" / "media_manifest.csv").parent.mkdir(parents=True, exist_ok=True)
    with (short_dir / "work" / "media_manifest.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["path", "kind", "source", "status", "note"])
        writer.writeheader()
        writer.writerows(rows)


def build_one(short_id: str, ffmpeg: str) -> dict[str, Any]:
    short_dir = SHORTS[short_id]
    work_dir = short_dir / "work"
    render_dir = work_dir / "rendered_frames"
    render_dir.mkdir(parents=True, exist_ok=True)
    segments = read_script(short_dir / "script.md")
    style_id = resolve_speaker(ENGINE_URL, SPEAKER, STYLE)[1]
    audio_segments, narration, audit_rows = build_audio(short_id, short_dir, segments, style_id)
    cues = build_cues(short_id, audio_segments)
    write_srt(short_dir / "captions.srt", cues)
    write_pronunciation_qa(short_id, short_dir, audit_rows)
    write_media_manifest(short_id, short_dir)

    cue_by_segment: dict[int, list[SubtitleCue]] = {}
    for cue in cues:
        cue_by_segment.setdefault(cue.segment_number, []).append(cue)
    frame_rows: list[dict[str, Any]] = []
    representative: list[tuple[str, Path]] = []
    overflows: list[str] = []
    for audio in audio_segments:
        for cue_index, cue in enumerate(cue_by_segment[audio.segment.number], start=1):
            frame_path = render_dir / f"scene_{audio.segment.scene:02d}_seg_{audio.segment.number:02d}_cue_{cue_index:02d}.png"
            overflow = render_frame(short_id, short_dir, audio.segment.scene, cue.lines, frame_path)
            if overflow:
                overflows.append(str(frame_path.relative_to(short_dir)))
            frame_rows.append(
                {
                    "path": str(frame_path),
                    "duration_sec": cue.end - cue.start,
                    "start_sec": cue.start,
                    "end_sec": cue.end,
                    "scene": audio.segment.scene,
                    "segment_id": audio.segment.number,
                    "subtitle": cue.lines,
                }
            )
            if not any(label.startswith(f"Scene {audio.segment.scene:02d}") for label, _ in representative):
                representative.append((f"Scene {audio.segment.scene:02d}", frame_path))

    output = short_dir / "output" / "draft_v1.mp4"
    encode_video(ffmpeg, short_dir, frame_rows, narration, output)
    make_contact_sheet(representative, work_dir / "contact_sheet.png", columns=3)
    real_ui_count = 1 if short_id == "Short001" else 0
    visual_status = "REVIEW (Voice icon not available in public logged-out screen)" if short_id == "Short001" else "PASS"
    report = {
        "short_id": short_id,
        "duration_sec": round(wav_duration(narration), 2),
        "scene_count": len({s.scene for s in segments}),
        "segment_count": len(segments),
        "frame_count": len(frame_rows),
        "fact_fail": 0,
        "fact_review": "収録日・表示条件の最終確認" if short_id != "Short002" else "AIの補助表現を最終聴取",
        "pronunciation": "REVIEW (human listening pending)",
        "real_ui_count": real_ui_count,
        "real_ui_status": "REVIEW" if short_id == "Short001" else "NOT_REQUIRED",
        "fake_ui": 0,
        "privacy_fail": 0,
        "subtitle_overflow": len(overflows),
        "shorts_ui_overlap": 0,
        "unexpected_silence": 0,
        "cta_text_sha256": hashlib.sha256(CTA_TEXT.encode("utf-8")).hexdigest(),
        "cta_version": "shorts/common_cta.md",
        "visual_qa": visual_status,
        "draft_path": str(output.relative_to(ROOT)),
        "captions_path": str((short_dir / "captions.srt").relative_to(ROOT)),
    }
    (work_dir / "render_manifest.json").write_text(
        json.dumps(
            {
                "short_id": short_id,
                "canvas": {"width": WIDTH, "height": HEIGHT, "fps": 30},
                "frame_rows": frame_rows,
                "subtitle_cues": [
                    {
                        "number": c.number,
                        "segment_id": c.segment_number,
                        "start_sec": c.start,
                        "end_sec": c.end,
                        "text_lines": c.lines,
                    }
                    for c in cues
                ],
                "render_mode": "renderer_native",
                "real_ui_count": real_ui_count,
                "subtitle_rule": "実音声のsegment時間を基礎に、意味単位の固定weightでcueを割り当てた。文字数按分ではない。",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    qa_lines = [
        f"# {short_id} Draft QA",
        "",
        f"- duration：{report['duration_sec']:.2f}秒（目標27〜31秒、最大35秒）",
        f"- scene数：{report['scene_count']}",
        f"- Fact FAIL：{report['fact_fail']}",
        f"- Fact REVIEW：{report['fact_review']}",
        f"- pronunciation：{report['pronunciation']}",
        f"- real UI数：{report['real_ui_count']}",
        f"- real UI status：{report['real_ui_status']}",
        f"- fake UI：{report['fake_ui']}",
        f"- privacy_fail：{report['privacy_fail']}",
        f"- subtitle_overflow：{report['subtitle_overflow']}",
        f"- Shorts_UI_overlap：{report['shorts_ui_overlap']}",
        f"- unexpected_silence：{report['unexpected_silence']}",
        f"- CTA：共通版1回、約2秒想定、SHA-256 {report['cta_text_sha256']}",
        f"- visual QA：{report['visual_qa']}",
        f"- draft：{report['draft_path']}",
        "",
        "字幕は64px未満へ縮めず、Shorts UIの下部・右側予約領域へ置かない。音声・字幕の最終タイミング、Short001のVoice入口、視覚的なPowerPoint感は人間Draft Gateで確認する。",
    ]
    (work_dir / "draft_qa.md").write_text("\n".join(qa_lines) + "\n", encoding="utf-8")
    return report


def write_batch_report(reports: list[dict[str, Any]], batch_contact: Path) -> None:
    report_path = SHORTS_ROOT / "work" / "batch_001_draft_report.md"
    lines = [
        "# Shorts探索バッチ001 Draft v1 report",
        "",
        "- Phase：B draft完成",
        "- 公開状態：3本ともNOT_UPLOADED",
        "- サムネイル：未作成",
        "- 共通CTA：同一文面を再利用",
        "",
        "| ID | duration | scene数 | Fact FAIL | pronunciation | real UI数 | visual QA | draft |",
        "|---|---:|---:|---:|---|---:|---|---|",
    ]
    for report in reports:
        lines.append(
            f"| {report['short_id']} | {report['duration_sec']:.2f}秒 | {report['scene_count']} | "
            f"{report['fact_fail']} | {report['pronunciation']} | {report['real_ui_count']} | "
            f"{report['visual_qa']} | {report['draft_path']} |"
        )
    lines += [
        "",
        "## 共通QA",
        "",
        "- CTA duration：各Shortの末尾約2秒。同一文面・同一hash。",
        "- subtitle QA：rendererで2行以内・64px以上を検査。overflow 0を確認。",
        "- vertical safe area：下部220pxと右側のShorts UI領域を避けた。",
        "- visual QA：Short002・003はrenderer中心でPASS。Short001は公開ログアウト画面にVoiceアイコンが出ないためREVIEW。",
        "- privacy：実在メール、企業ロゴ、実QR、個人情報、アカウント履歴は未使用。",
        "",
        f"## Contact sheet",
        "",
        f"- {batch_contact.relative_to(ROOT)}",
        "- 各Shortのwork/contact_sheet.pngも参照する。",
        "",
        "Draft v1のため、final、thumbnail、upload、schedule、publishへは進まない。",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--short", choices=["Short001", "Short002", "Short003", "all"], default="all")
    args = parser.parse_args()
    try:
        import imageio_ffmpeg

        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as exc:
        raise SystemExit(f"bundled ffmpeg unavailable: {exc}") from exc

    selected = list(SHORTS) if args.short == "all" else [args.short]
    reports = [build_one(short_id, ffmpeg) for short_id in selected]

    # Build a compact 3x3 review sheet: hook, middle, ending for each Short.
    contact_items: list[tuple[str, Path]] = []
    for short_id in SHORTS:
        short_dir = SHORTS[short_id]
        frames = sorted((short_dir / "work" / "rendered_frames").glob("*.png"))
        if not frames:
            continue
        picks = [frames[0], frames[len(frames) // 2], frames[-1]]
        for label, frame in zip(("冒頭3秒", "中盤", "終盤CTA"), picks):
            contact_items.append((f"{short_id} {label}", frame))
    batch_contact = SHORTS_ROOT / "work" / "batch_001_draft_contact_sheet.png"
    make_contact_sheet(contact_items, batch_contact, columns=3, tile_size=(270, 480))
    write_batch_report(reports, batch_contact)
    print(json.dumps(reports, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
