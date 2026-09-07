"""Mechanical QA checks for Phase 2 scenes, subtitles, audio, and draft video."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import wave
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

from episode_io import canonical_text_render_mode  # noqa: E402
from scene_renderer import _wrap_paragraph_japanese, pil_font, wrap_text  # noqa: E402
from subtitle_preflight import estimated_width

PLACEHOLDER_PATTERN = re.compile(r"GPT\s*IMAGE\s*HERE|PLACEHOLDER|TODO|DUMMY", re.IGNORECASE)
WIDTH, HEIGHT, SAFE_HEIGHT = 1920, 1080, 180
VISUAL_BALANCE_MIN_X, VISUAL_BALANCE_MAX_X = 650, 1270
ROOT = Path(__file__).resolve().parents[1]


def _ffmpeg_executable() -> str | None:
    executable = shutil.which("ffmpeg")
    if executable:
        return executable
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None

# 単語途中分断の検出用（画像描画はwrap_textの禁則処理で防ぐが、QA側の回帰防止に使う）
SPLIT_TOKENS = ("番号", "判断", "電話", "センター", "休止", "ブロック", "相談", "確認", "利用", "国際", "警察", "詐欺", "注意", "可能性", "表示")
ASCII_RUN = re.compile(r"[A-Za-z0-9]+")
SMALL_KANA_START = "ゃゅょぁぃぅぇぉっャュョァィゥェォッ"
PROTECTED_SCENE_TERMS = (
    "Googleフォト", "Googleアカウント", "バックアップ済み", "未バックアップ",
    "バックアップ", "デバイスから削除", "最近削除した項目", "空き容量を増やす",
    "iPhone", "Android", "YouTube", "LINE", "App Store",
)


def unresolved_placeholders(data: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for scene in data.get("scenes", []):
        scene_id = int(scene.get("id", 0))
        if PLACEHOLDER_PATTERN.search(json.dumps(scene, ensure_ascii=False)):
            issues.append(f"scene {scene_id:03d}: unresolved placeholder text")
        for asset in scene.get("official_asset") or []:
            if isinstance(asset, dict) and asset.get("kind") == "placeholder":
                issues.append(f"scene {scene_id:03d}: placeholder asset")
    return issues


def text_boxes_for(layout: str, render_mode: str) -> dict[str, tuple[tuple[int, int, int, int], int, int, int, float]]:
    """pill renderer / overlay と同じ本文boxの写し（linebreak QA用）。

    layout: text kind -> (box, max_size, min_size, max_lines, spacing_ratio)。
    renderer側の座標を変えた場合はここも同期する。
    """
    if render_mode in {"gpt_image", "hybrid"}:
        return {
            "headline": ((100, 110, 940, 390), 112, 78, 3, 0.12),
            "support_text": ((110, 430, 920, 580), 52, 40, 3, 0.16),
            "main_message": ((110, 630, 920, 810), 48, 40, 3, 0.16),
        }
    if layout == "layout_01_hero":
        return {
            "headline": ((760, 138, 1800, 490), 122, 78, 3, 0.12),
            "support_text": ((760, 505, 1770, 625), 54, 42, 2, 0.16),
            "main_message": ((760, 680, 1780, 805), 48, 40, 1, 0.18),
        }
    if layout == "layout_02_list":
        return {
            "headline": ((150, 88, 1770, 225), 112, 82, 2, 0.12),
            "support_text": ((170, 235, 1750, 315), 48, 40, 2, 0.12),
        }
    if layout == "layout_03_visual_text":
        return {
            "headline": ((900, 138, 1800, 425), 116, 78, 3, 0.12),
            "support_text": ((900, 460, 1780, 600), 52, 42, 3, 0.16),
            "main_message": ((900, 650, 1770, 780), 44, 40, 3, 0.16),
        }
    if layout == "layout_04_text_official":
        return {
            "headline": ((110, 82, 1810, 225), 112, 82, 2, 0.12),
            "support_text": ((130, 625, 910, 725), 48, 40, 2, 0.14),
        }
    if layout == "layout_05_compare":
        return {
            "headline": ((110, 82, 1810, 225), 108, 78, 2, 0.12),
            "support_text": ((150, 235, 1770, 315), 46, 40, 2, 0.14),
        }
    if layout == "layout_06_caution":
        return {
            "headline": ((620, 90, 1080, 385), 104, 70, 4, 0.12),
            "support_text": ((620, 430, 1080, 570), 50, 40, 3, 0.16),
            "main_message": ((620, 620, 1080, 800), 44, 40, 3, 0.16),
        }
    if layout == "layout_07_summary":
        return {
            "headline": ((120, 82, 1800, 225), 108, 80, 2, 0.12),
            "support_text": ((150, 235, 1770, 315), 46, 40, 2, 0.14),
        }
    return {
        "headline": ((190, 215, 1730, 465), 124, 84, 2, 0.12),
        "support_text": ((230, 505, 1690, 640), 54, 42, 2, 0.16),
    }


def linebreak_issues(data: dict[str, Any]) -> list[str]:
    """日本語の禁則・孤立行・単語分断を、renderと同じwrap処理で回帰検出する。"""
    issues: list[str] = []
    draw = ImageDraw.Draw(Image.new("RGB", (WIDTH, HEIGHT)))
    for scene in data.get("scenes", []):
        scene_id = int(scene.get("id", 0))
        layout = str(scene.get("layout") or "")
        render_mode = str(scene.get("render_mode") or "template")
        text_mode = canonical_text_render_mode(scene)
        if render_mode in {"gpt_image", "hybrid"} and text_mode in {"imagegen_native", "no_text"}:
            # ImageGen内文字のためPIL wrap前提のlinebreak QAは適用しない。
            # この種のsceneの文字QAは scripts/text_qa.py（目視相当チェック）で行う。
            continue
        boxes = text_boxes_for(layout, render_mode)
        scale = float(scene.get("headline_scale") or 1.0)
        for kind, (box, max_size, min_size, max_lines, spacing) in boxes.items():
            text = str(scene.get(kind) or "")
            if not text:
                continue
            width = box[2] - box[0]
            max_font = int(round(max_size * (scale if kind == "headline" else 1.0)))
            max_font = max(min_size, max_font)
            font = pil_font(max_font)
            lines = wrap_text(text, font, width, draw)
            for line in lines:
                if line[:1] in "、。，．・：；！？％）」』】〕〉｝＞ー…":
                    issues.append(
                        f"scene {scene_id:03d} {kind}: 行頭禁則文字が行頭（{line[:1]}）: {text}"
                    )
            if len(lines) > 1:
                for line in lines:
                    if len(line) == 1:
                        issues.append(f"scene {scene_id:03d} {kind}: 1文字の孤立行（{line}）: {text}")
            for index in range(len(lines) - 1):
                pair = lines[index][-1:] + lines[index + 1][:1]
                for token in SPLIT_TOKENS:
                    if len(token) == 2 and pair == token:
                        issues.append(
                            f"scene {scene_id:03d} {kind}: 単語途中分断（{token}）: {text}"
                        )
                        break
                # 電話番号・記号+数字の分断（例: ＃/9110）
                if lines[index][-1:] in {"＃", "＋", "+"} and lines[index + 1][:1].isdigit():
                    issues.append(f"scene {scene_id:03d} {kind}: 記号と数字が分断（{lines[index][-1:]} / 数字）: {text}")
                # ASCII英数字tokenの途中分断（Google / LINE / iPhone等。一般化して検出）
                right_match = ASCII_RUN.match(lines[index + 1])
                if right_match:
                    left_matches = list(ASCII_RUN.finditer(lines[index]))
                    left_match = left_matches[-1] if left_matches else None
                    if left_match and left_match.end() == len(lines[index]):
                        left_run, right_run = left_match.group(0), right_match.group(0)
                        combined = left_run + right_run
                        # 元テキスト内で境界を挟まず連続していれば、同一tokenの途中分断
                        if combined in text:
                            issues.append(
                                f"scene {scene_id:03d} {kind}: ASCII英数字token途中分断（{left_run} / {right_run}）: {text}"
                            )
                # 仮名の単語途中分断: 次行頭が小書き仮名・促音・長音符で始まる（例: いっし / ょに）
                if lines[index + 1][:1] in SMALL_KANA_START + "ー":
                    issues.append(
                        f"scene {scene_id:03d} {kind}: 仮名の単語途中分断（{lines[index][-1]} / {lines[index + 1][:1]}）: {text}"
                    )
                # 数字と単位の分断（例: 30 / 日、60 / 日）
                if lines[index][-1:].isdigit() and lines[index + 1][:1] in "日月年時分秒円個件台":
                    issues.append(
                        f"scene {scene_id:03d} {kind}: 数字と単位の分断（{lines[index][-1:]} / {lines[index + 1][:1]}）: {text}"
                    )
                # 行末に開き括弧を残さない（wrap側で防止されるが回帰検出）
                if lines[index][-1:] in "（「『":
                    issues.append(f"scene {scene_id:03d} {kind}: 行末に開き括弧（{lines[index][-1]}）: {text}")
                # 閉じ括弧だけを次行へ送らない
                if lines[index + 1][:1] in "）」』":
                    issues.append(f"scene {scene_id:03d} {kind}: 閉じ括弧が行頭（{lines[index + 1][:1]}）: {text}")
            # 括弧内で改行していないか（（…）が行境界をまたぐ場合）
            if "（" in text:
                joined = "".join(lines)
                boundary = 0
                for line in lines[:-1]:
                    boundary += len(line)
                    if joined[:boundary].count("（") > joined[:boundary].count("）"):
                        issues.append(f"scene {scene_id:03d} {kind}: 括弧の中で改行: {text}")
                        break
            # 保護語（Googleフォト／バックアップ済み等）が行境界をまたいで分断されていないか
            joined_text = "".join(lines)
            for term in PROTECTED_SCENE_TERMS:
                found = joined_text.find(term)
                if found < 0 or len(lines) < 2:
                    continue
                boundary = len(lines[0])
                for line in lines[1:-1]:
                    if found < boundary < found + len(term):
                        issues.append(f"scene {scene_id:03d} {kind}: 保護語の途中分断（{term}）: {text}")
                        break
                    boundary += len(line)
                else:
                    if found < boundary < found + len(term):
                        issues.append(f"scene {scene_id:03d} {kind}: 保護語の途中分断（{term}）: {text}")
            # compareカードのtitle/bodyも同じ改行QA対象にする
            for raw in scene.get("compare_cards") or []:
                if not isinstance(raw, dict):
                    continue
                for sub_kind, sub_text, card_width, card_max, card_min, card_lines in (
                    ("compare_title", str(raw.get("title") or ""), 692, 52, 42, 1),
                    ("compare_body", str(raw.get("body") or ""), 692, 48, 40, 3),
                ):
                    if not sub_text:
                        continue
                    sub_lines = wrap_text(sub_text, pil_font(card_max), card_width, draw)
                    if len(sub_lines) > card_lines:
                        issues.append(f"scene {scene_id:03d} {sub_kind}: 行数超過（{len(sub_lines)} > {card_lines}）: {sub_text}")
                    if len(sub_lines) > 1:
                        for sub_line in sub_lines:
                            if len(sub_line) == 1:
                                issues.append(f"scene {scene_id:03d} {sub_kind}: 1文字の孤立行（{sub_line}）: {sub_text}")
    return issues


def narration_item_count_issues(data: dict[str, Any]) -> list[str]:
    """ナレーションが「Nつ」と明示するsceneで、画面のitems数と一致するか検査する。"""
    issues: list[str] = []
    count_pattern = re.compile(r"(?:次の)?([0-9０-９]+)つ(?!目)")
    for scene in data.get("scenes", []):
        scene_id = int(scene.get("id", 0))
        items = scene.get("items") or []
        if not items:
            continue
        text = " ".join(
            str(seg.get("narration") or "")
            for seg in data.get("narration_segments", [])
            if int(scene["start_segment"]) <= int(seg["id"]) <= int(scene["end_segment"])
        )
        matches = list(count_pattern.finditer(text))
        if matches:
            # 「5つの場面を見ましたが、覚えることは3つです」のように、
            # 既出の総数と今回の表示項目数が同じsceneに出る場合は、
            # 最後に明示された現在の項目数を比較対象にする。
            # 「4つのケースに分けます」は分岐の総数であり、同じsceneの
            # 条件カード数ではないため、項目数比較の対象から除外する。
            count_match = next(
                (
                    match
                    for match in reversed(matches)
                    if not text[match.end():].lstrip().startswith("のケース")
                ),
                None,
            )
            if count_match is None:
                continue
            spoken = int(count_match.group(1))
            if spoken != len(items):
                issues.append(
                    f"scene {scene_id:03d}: ナレーションは「{spoken}つ」だが画面の項目数は{len(items)}"
                )
    return issues


def approved_draft_filename(review: dict[str, Any]) -> str | None:
    video = review.get("video", {})
    if not isinstance(video, dict):
        return None
    approved: list[str] = []
    for key, value in video.items():
        if value != "approved":
            continue
        name = str(key)
        if not (name.startswith("draft_auto_") or name.startswith("draft_v")):
            continue
        approved.append(name if name.lower().endswith(".mp4") else f"{name}.mp4")
    return approved[0] if len(approved) == 1 else None


def finalize_allowed(review_path: Path, output_dir: Path | None = None) -> tuple[bool, str]:
    if not review_path.exists():
        return False, "human_review.json is missing"
    try:
        review = json.loads(review_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"human_review.json is invalid: {exc}"
    filename = approved_draft_filename(review)
    if not filename:
        return False, "exactly one draft_auto_* or draft_vN video must be human-approved"
    if output_dir is not None and not (output_dir / filename).exists():
        return False, f"approved draft is missing: {filename}"
    return True, f"approved: {filename}"


def _probe(path: Path) -> dict[str, Any]:
    ffprobe = shutil.which("ffprobe")
    if ffprobe and path.exists():
        result = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "format=duration", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels", "-of", "json", str(path)],
            check=False, capture_output=True, text=True,
        )
        if not result.returncode:
            return json.loads(result.stdout)
        return {"error": result.stderr.strip()}
    if not path.exists():
        return {}
    try:
        import av

        container = av.open(str(path))
        streams: list[dict[str, Any]] = []
        for stream in container.streams:
            codec_name = getattr(stream.codec_context, "name", None)
            if stream.type == "video":
                rate = stream.average_rate or stream.base_rate
                streams.append({
                    "codec_type": "video",
                    "codec_name": codec_name,
                    "width": stream.codec_context.width,
                    "height": stream.codec_context.height,
                    "r_frame_rate": f"{rate.numerator}/{rate.denominator}" if rate else None,
                })
            elif stream.type == "audio":
                streams.append({
                    "codec_type": "audio",
                    "codec_name": codec_name,
                    "sample_rate": stream.codec_context.sample_rate,
                    "channels": stream.codec_context.channels,
                })
        duration = (container.duration / av.time_base) if container.duration is not None else 0.0
        container.close()
        return {"format": {"duration": duration}, "streams": streams}
    except Exception as exc:
        # The managed desktop runtime may provide the bundled ffmpeg binary
        # without installing PyAV or ffprobe.  Keep the same mechanical QA
        # checks available by parsing ffmpeg's input summary as a fallback.
        ffmpeg = _ffmpeg_executable()
        if not ffmpeg:
            return {"error": f"PyAV probe failed: {exc}"}
        result = subprocess.run(
            [ffmpeg, "-hide_banner", "-i", str(path)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        summary = result.stderr
        duration_match = re.search(
            r"Duration:\s*(\d+):(\d{2}):(\d+(?:\.\d+)?)",
            summary,
        )
        if not duration_match:
            return {"error": f"PyAV probe failed: {exc}; ffmpeg summary unavailable"}
        hours, minutes, seconds = duration_match.groups()
        duration = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
        streams: list[dict[str, Any]] = []
        for line in summary.splitlines():
            if "Video:" in line:
                video_match = re.search(
                    r"Video:\s*([^\s,(]+).*?(\d{2,5})x(\d{2,5}).*?(\d+(?:\.\d+)?)\s*fps",
                    line,
                )
                if video_match:
                    codec, width, height, fps = video_match.groups()
                    fps_value = float(fps)
                    if abs(fps_value - 29.97) < 0.02:
                        fps_numerator, fps_denominator = 30000, 1001
                    else:
                        fps_numerator, fps_denominator = round(fps_value), 1
                    streams.append({
                        "codec_type": "video",
                        "codec_name": codec,
                        "width": int(width),
                        "height": int(height),
                        "r_frame_rate": f"{fps_numerator}/{fps_denominator}",
                    })
            elif "Audio:" in line:
                audio_match = re.search(
                    r"Audio:\s*([^\s,(]+).*?(\d+)\s*Hz,\s*([^,\s]+)",
                    line,
                )
                if audio_match:
                    codec, sample_rate, channel_label = audio_match.groups()
                    channels = {"mono": 1, "stereo": 2}.get(channel_label.lower())
                    if channels is None:
                        channel_count = re.search(r"(\d+)\s*channels?", line)
                        channels = int(channel_count.group(1)) if channel_count else None
                    stream = {
                        "codec_type": "audio",
                        "codec_name": codec,
                        "sample_rate": int(sample_rate),
                    }
                    if channels is not None:
                        stream["channels"] = channels
                    streams.append(stream)
        return {"format": {"duration": duration}, "streams": streams}


def _black_frames(path: Path) -> list[str]:
    ffmpeg = _ffmpeg_executable()
    if not ffmpeg or not path.exists():
        return []
    result = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", str(path), "-vf", "blackdetect=d=0.5:pix_th=0.10", "-an", "-f", "null", "-"],
        check=False, capture_output=True, text=True,
    )
    return [line.strip() for line in result.stderr.splitlines() if "black_start:" in line]


def _long_silences(path: Path) -> list[str]:
    ffmpeg = _ffmpeg_executable()
    if not ffmpeg or not path.exists():
        return []
    result = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", str(path), "-af", "silencedetect=n=-45dB:d=2.0", "-f", "null", "-"],
        check=False, capture_output=True, text=True,
    )
    return [line.strip() for line in result.stderr.splitlines() if "silence_duration:" in line]


def declared_visual_center_x(scene: dict[str, Any]) -> float | None:
    """Return an optional/renderer-known visual center for a WARN-only check."""
    direct = scene.get("visual_balance_center_x")
    if isinstance(direct, (int, float)):
        return float(direct)
    balance = scene.get("visual_balance")
    if isinstance(balance, dict) and isinstance(balance.get("center_x"), (int, float)):
        return float(balance["center_x"])
    # layout_06_caution's original content group is centered around x=600;
    # its explicit offset is the renderer's way to bring that group to center.
    if scene.get("layout") == "layout_06_caution" and "content_offset_x" in scene:
        try:
            return 600.0 + float(scene.get("content_offset_x") or 0)
        except (TypeError, ValueError):
            return None
    return None


def _white_ratio(image: Image.Image, box: tuple[int, int, int, int]) -> float:
    sample = image.crop(box).convert("RGB").resize((64, 30))
    pixels = list(sample.get_flattened_data()) if hasattr(sample, "get_flattened_data") else list(sample.getdata())
    return sum(1 for red, green, blue in pixels if red >= 248 and green >= 248 and blue >= 248) / max(1, len(pixels))


def _black_edge_ratio(image: Image.Image, box: tuple[int, int, int, int]) -> float:
    sample = image.crop(box).convert("RGB").resize((64, 8))
    pixels = list(sample.get_flattened_data()) if hasattr(sample, "get_flattened_data") else list(sample.getdata())
    return sum(1 for red, green, blue in pixels if max(red, green, blue) <= 12) / max(1, len(pixels))


def _template_content_centroid_x(image: Image.Image) -> float | None:
    """template sceneの「背景白以外」の重心X。左右のvisual weightバランス確認用。"""
    sample = image.crop((0, 14, WIDTH, HEIGHT - SAFE_HEIGHT)).resize((480, 216), Image.BILINEAR)
    pixels = list(sample.getdata())
    width, height = sample.size
    total = 0.0
    weight = 0.0
    for y in range(height):
        row = y * width
        for x in range(width):
            red, green, blue = pixels[row + x]
            if red < 250 or green < 250 or blue < 250:
                point = 1.0 if (red < 244 or green < 244 or blue < 244) else 0.35
                total += (x + 0.5) / width * point
                weight += point
    if weight <= 0:
        return None
    return total / weight * WIDTH


def _declared_official_area_ratio(scene: dict[str, Any]) -> float | None:
    """Estimate the renderer slot size without judging the asset's content."""
    if not scene.get("official_asset"):
        return None
    boxes = {
        "layout_01_hero": (40, 140, 760, 800),
        "layout_03_visual_text": (50, 145, 830, 795),
        "layout_04_text_official": (1000, 235, 1810, 800),
        "layout_05_compare": (110, 360, 1810, 830),
        "layout_06_caution": (1120, 180, 1810, 840),
    }
    box = boxes.get(str(scene.get("layout") or ""))
    if box is None:
        return None
    width, height = max(0, box[2] - box[0]), max(0, box[3] - box[1])
    return (width * height) / (WIDTH * (HEIGHT - SAFE_HEIGHT))


def scene_visual_warnings(scene: dict[str, Any], path: Path) -> list[str]:
    """Collect conservative scene warnings; never turn visual heuristics into FAIL."""
    warnings: list[str] = []
    scene_id = int(scene.get("id", 0))
    center_x = declared_visual_center_x(scene)
    intentional_asymmetry = bool((scene.get("visual_balance") or {}).get("intentional_asymmetry", False)) if isinstance(scene.get("visual_balance"), dict) else False
    if center_x is not None and not intentional_asymmetry and (center_x < VISUAL_BALANCE_MIN_X or center_x > VISUAL_BALANCE_MAX_X):
        warnings.append(f"scene {scene_id:03d}: visual balance center x={center_x:.0f} (review; target {VISUAL_BALANCE_MIN_X}..{VISUAL_BALANCE_MAX_X})")

    animation = str(scene.get("animation") or "static")
    if animation in {"slow_pan", "horizontal_pan", "pan"} and not str(scene.get("animation_reason") or "").strip():
        warnings.append(f"scene {scene_id:03d}: horizontal pan has no declared animation_reason")
    official_ratio = _declared_official_area_ratio(scene)
    if official_ratio is not None and official_ratio < 0.25:
        warnings.append(f"scene {scene_id:03d}: official visual slot is small ({official_ratio * 100:.1f}%; review readability)")

    try:
        with Image.open(path) as opened:
            image = opened.convert("RGB")
            if image.size != (WIDTH, HEIGHT):
                return warnings
            render_mode = str(scene.get("render_mode") or "template")
            layout = str(scene.get("layout") or "")
            active = (0, 0, WIDTH, HEIGHT - SAFE_HEIGHT)
            left = _white_ratio(image, (0, 0, int(WIDTH * 0.20), HEIGHT - SAFE_HEIGHT))
            right = _white_ratio(image, (int(WIDTH * 0.80), 0, WIDTH, HEIGHT - SAFE_HEIGHT))
            middle = 1.0 - _white_ratio(image, (int(WIDTH * 0.35), 0, int(WIDTH * 0.65), HEIGHT - SAFE_HEIGHT))
            if render_mode in {"gpt_image", "hybrid"}:
                if left > 0.94 and middle > 0.12:
                    warnings.append(f"scene {scene_id:03d}: large white space on the left (review full-frame balance)")
                if right > 0.94 and middle > 0.12:
                    warnings.append(f"scene {scene_id:03d}: large white space on the right (review full-frame balance)")
                whole_white = _white_ratio(image, active)
                if whole_white > 0.40 and (left > 0.80 or right > 0.80):
                    warnings.append(f"scene {scene_id:03d}: opaque white area exceeds 40% (review intentional minimal design)")
            elif render_mode == "template":
                # 意図的な左右構図（GPT画像と2カラム設計）には適用しない。
                # 主対象は「一覧・注意・まとめ」系のcentered template。
                if layout in {"layout_02_list", "layout_06_caution", "layout_07_summary", "layout_08_section"}:
                    centroid = _template_content_centroid_x(image)
                    if centroid is not None and (
                        centroid < VISUAL_BALANCE_MIN_X or centroid > VISUAL_BALANCE_MAX_X
                    ) and not intentional_asymmetry:
                        warnings.append(
                            f"scene {scene_id:03d}: template content centroid x={centroid:.0f} off-center "
                            f"(target {VISUAL_BALANCE_MIN_X}..{VISUAL_BALANCE_MAX_X})"
                        )
            # Black bars are always suspicious in a 1920x1080 scene, but remain
            # a WARN because an intentional cinematic treatment is possible.
            if _black_edge_ratio(image, (0, 0, WIDTH, 8)) > 0.98 or _black_edge_ratio(image, (0, HEIGHT - 8, WIDTH, HEIGHT)) > 0.98:
                warnings.append(f"scene {scene_id:03d}: possible letterbox black edge")
            if _black_edge_ratio(image, (0, 0, 8, HEIGHT)) > 0.98 or _black_edge_ratio(image, (WIDTH - 8, 0, WIDTH, HEIGHT)) > 0.98:
                warnings.append(f"scene {scene_id:03d}: possible pillarbox black edge")
    except OSError:
        pass
    return warnings


def run_qa(
    data: dict[str, Any], final_scene_dir: Path, timing_path: Path, draft_path: Path,
    report_base: Path, audio_path: Path | None = None,
) -> dict[str, Any]:
    failures = unresolved_placeholders(data)
    warnings: list[str] = []
    scenes = data.get("scenes", [])
    timing = json.loads(timing_path.read_text(encoding="utf-8")) if timing_path.exists() else {"segments": []}
    postroll = data.get("postroll") or {}
    episode_dir = report_base.resolve().parent.parent
    cta_config_ref = postroll.get("cta_config") or "config/channel_cta.json"
    cta_config_path = Path(str(cta_config_ref))
    if not cta_config_path.is_absolute():
        cta_config_path = (
            (episode_dir / cta_config_path).resolve()
            if str(cta_config_ref).startswith(("work/", "assets/", "audio/"))
            else (ROOT / cta_config_path).resolve()
        )
    cta_config: dict[str, Any] = {}
    if cta_config_path.exists():
        try:
            loaded = json.loads(cta_config_path.read_text(encoding="utf-8"))
            cta_config = loaded if isinstance(loaded, dict) else {}
        except (OSError, json.JSONDecodeError):
            pass
    warnings.extend(linebreak_issues(data))
    warnings.extend(narration_item_count_issues(data))
    postroll_duration = float(postroll.get("duration_sec") or 0)
    if postroll_duration > 0:
        cta_screen = postroll.get("asset")
        if not cta_screen:
            failures.append("CTA: postroll asset（画面）が未設定")
        else:
            screen_path = Path(str(cta_screen))
            if not screen_path.is_absolute():
                screen_path = (episode_dir / screen_path).resolve()
            if not screen_path.exists():
                failures.append(f"CTA: 画面素材が存在しない: {screen_path.name}")
        audio_required = bool(cta_config.get("audio_required", True))
        cta_audio = postroll.get("cta_audio")
        if audio_required and not cta_audio:
            failures.append("CTA: audio_required=true だが cta_audio が未設定（画面だけのCTAは不可）")
        if cta_audio:
            audio_path_resolved = Path(str(cta_audio))
            if not audio_path_resolved.is_absolute():
                audio_path_resolved = (episode_dir / audio_path_resolved).resolve()
            if not audio_path_resolved.exists():
                failures.append(f"CTA: 音声素材が存在しない: {audio_path_resolved.name}")
            else:
                try:
                    with wave.open(str(audio_path_resolved), "rb") as wav_handle:
                        cta_duration = wav_handle.getnframes() / wav_handle.getframerate()
                    if cta_duration > postroll_duration + 0.05:
                        failures.append(
                            f"CTA: 音声（{cta_duration:.2f}s）がCTA尺（{postroll_duration:.2f}s）より長い"
                        )
                    if postroll_duration - cta_duration < 0.4:
                        warnings.append(
                            f"CTA: 余韻が短い（CTA尺{postroll_duration:.2f}s - 音声{cta_duration:.2f}s）"
                        )
                except (OSError, wave.Error) as exc:
                    failures.append(f"CTA: 音声が読めない: {cta_audio} ({exc})")
            config_hash = str(cta_config.get("content_hash") or "")
            postroll_hash = str(postroll.get("cta_content_hash") or "")
            if config_hash and postroll_hash and config_hash != postroll_hash:
                warnings.append("CTA: canonical CTA本文ハッシュ不一致（REVIEW候補）")
            elif config_hash and not postroll_hash:
                warnings.append("CTA: postrollにcta_content_hashが未設定")
    expected_duration = float(timing.get("duration", 0)) + postroll_duration
    scene_warning_map: dict[str, list[str]] = {}
    if len(timing.get("segments", [])) != len(data.get("narration_segments", [])):
        failures.append("audio segment count does not match narration segment count")
    for scene in scenes:
        path = final_scene_dir / f"scene_{int(scene['id']):03d}.png"
        if not path.exists():
            failures.append(f"missing final scene: {path.name}")
            continue
        try:
            with Image.open(path) as image:
                if image.size != (1920, 1080):
                    failures.append(f"{path.name}: {image.size} != 1920x1080")
                else:
                    scene_warnings = scene_visual_warnings(scene, path)
                    if scene_warnings:
                        scene_warning_map[f"scene_{int(scene['id']):03d}"] = scene_warnings
                        warnings.extend(scene_warnings)
        except OSError as exc:
            failures.append(f"{path.name}: invalid image ({exc})")
    for cue in data.get("subtitles", []):
        text = "".join(str(line) for line in cue.get("text_lines", []))
        if len(re.sub(r"\s+", "", text)) == 1:
            failures.append(f"{cue.get('id')}: one-character cue")
        for line in cue.get("text_lines", []):
            if estimated_width(str(line)) * float(cue.get("font_px") or 72) / 72.0 > 1800:
                failures.append(f"{cue.get('id')}: subtitle exceeds safe width")
    cue_segments = {int(cue["segment_id"]) for cue in data.get("subtitles", [])}
    narration_segments = {int(segment["id"]) for segment in data.get("narration_segments", [])}
    missing_cues = sorted(narration_segments - cue_segments)
    if missing_cues:
        failures.append(f"missing subtitle cues for segments: {missing_cues}")
    probe = _probe(draft_path)
    if draft_path.exists() and probe.get("error"):
        failures.append(f"ffprobe: {probe['error']}")
    if draft_path.exists() and probe:
        video = next((s for s in probe.get("streams", []) if s.get("codec_type") == "video"), {})
        audio_stream = next((s for s in probe.get("streams", []) if s.get("codec_type") == "audio"), {})
        if (video.get("width"), video.get("height")) != (1920, 1080):
            failures.append("draft video is not 1920x1080")
        if video and video.get("codec_name") != "h264":
            failures.append(f"draft video codec is not h264: {video.get('codec_name')}")
        if not audio_stream:
            failures.append("draft audio stream is missing")
        else:
            if audio_stream.get("codec_name") != "aac":
                failures.append(f"draft audio codec is not aac: {audio_stream.get('codec_name')}")
            if str(audio_stream.get("sample_rate")) != "48000":
                failures.append(f"draft audio sample rate is not 48000Hz: {audio_stream.get('sample_rate')}")
        if video.get("r_frame_rate") not in {"30/1", "30000/1001"}:
            warnings.append(f"unexpected frame rate: {video.get('r_frame_rate')}")
        if timing_path.exists():
            delta = abs(float(probe.get("format", {}).get("duration", 0)) - expected_duration)
            if delta > 0.5:
                warnings.append(f"audio/video duration delta: {delta:.3f}s")
        black = _black_frames(draft_path)
        if black:
            failures.extend(f"black frame interval: {item}" for item in black)
    if audio_path is not None:
        if not audio_path.exists():
            failures.append("narration audio is missing")
        else:
            silences = _long_silences(audio_path)
            if silences:
                warnings.extend(f"long silence: {item}" for item in silences)
    status = "FAIL" if failures else "WARN" if warnings else "PASS"
    result = {
        "status": status, "failures": failures, "warnings": warnings, "probe": probe,
        "scene_count": len(scenes), "subtitle_count": len(data.get("subtitles", [])), "postroll": postroll,
        "scene_visual_warnings": scene_warning_map,
        "expected_duration": round(expected_duration, 3),
    }
    report_base.parent.mkdir(parents=True, exist_ok=True)
    report_base.with_suffix(".json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase 2 QA", "", f"- status: {status}", f"- scenes: {len(scenes)}",
        f"- expected duration: {expected_duration:.3f}s", "", "## FAIL", "",
    ]
    lines.extend(f"- {item}" for item in failures or ["なし"])
    lines.extend(["", "## WARN", ""])
    lines.extend(f"- {item}" for item in warnings or ["なし"])
    report_base.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result
