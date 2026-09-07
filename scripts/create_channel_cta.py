"""Render the configurable channel-common CTA card.

The profile is intentionally separate from any episode asset.  It reuses the
approved channel logo and calm Episode 001/003 visual language without copying
topic-specific end-card text from an earlier episode.

Episode 005以降の仕様: CTAは画面とナレーションを同じcanonical本文から作る。
`config/channel_cta.json` の canonical_text / narration_text / display_text を
source of truthとし、音声付き（audio_required=true, duration_mode=audio_based）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "channel_cta.json"

import sys

SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from scene_renderer import HEIGHT, SAFE_HEIGHT, WIDTH, draw_fitted, fit_text_block  # noqa: E402


def _box(value: Any) -> tuple[int, int, int, int]:
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError(f"CTA box must contain four numbers: {value!r}")
    return tuple(int(item) for item in value)  # type: ignore[return-value]


def _point(value: Any) -> tuple[int, int]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"CTA point must contain two numbers: {value!r}")
    return int(value[0]), int(value[1])


def _path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def _centered(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str,
              max_size: int, min_size: int, fill: str, max_lines: int = 1) -> dict[str, Any]:
    return draw_fitted(draw, box, text, max_size, min_size, fill, max_lines, "center", 0.14)


def cta_text_metrics(config_path: Path = DEFAULT_CONFIG) -> dict[str, Any]:
    """Return deterministic layout metrics used by the CTA full-text QA."""
    config = load_config(config_path)
    text = config.get("text") or {}
    layout = config.get("layout") or {}
    draw = ImageDraw.Draw(Image.new("RGB", (WIDTH, HEIGHT)))
    specs = {
        "description": (str(text.get("description") or ""), _box(layout.get("description_box")), 60, 56, 3),
        "cta": (str(text.get("cta") or ""), _box(layout.get("cta_text_box")), 60, 56, 2),
    }
    result: dict[str, Any] = {}
    for name, (value, box, max_size, min_size, max_lines) in specs.items():
        font, size, lines, line_height = fit_text_block(
            draw, value, box[2] - box[0], box[3] - box[1], max_size, min_size, max_lines, 0.14
        )
        result[name] = {
            "text": value,
            "box": list(box),
            "font_size": size,
            "min_size": min_size,
            "max_lines": max_lines,
            "lines": lines,
            "line_height": line_height,
            "complete": "".join(lines).replace("\n", "") == value.replace("\n", ""),
        }
    return result


def load_config(config_path: Path = DEFAULT_CONFIG) -> dict[str, Any]:
    value = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("profile") != "channel_common_cta":
        raise ValueError("unsupported CTA profile")
    return value


def content_hash(config_path: Path = DEFAULT_CONFIG) -> str:
    config = load_config(config_path)
    text = str(config.get("canonical_text") or "")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def synthesize_cta_audio(
    config_path: Path = DEFAULT_CONFIG,
    engine_url: str = "http://127.0.0.1:50021",
    output_path: Path | None = None,
) -> dict[str, Any]:
    """Generate the common CTA narration with the same VOICEVOX voice as the main episode."""
    from voicevox_incremental import resolve_speaker, synthesize, wav_duration

    config = load_config(config_path)
    text = str(config.get("narration_text") or "")
    if not text:
        raise ValueError("channel_cta.json: narration_text が空です")
    output_path = output_path or (ROOT / "work" / "channel_cta_audio.wav")
    output_path = output_path.resolve()
    _uuid, style_id = resolve_speaker(engine_url, "剣崎雌雄", "ノーマル")
    synthesize(engine_url, text, style_id, output_path, episode_id="cta")
    return {
        "path": str(output_path),
        "duration": wav_duration(output_path),
        "text": text,
        "content_hash": content_hash(config_path),
        "style_id": style_id,
    }


def build_cta(config_path: Path = DEFAULT_CONFIG, output_path: Path | None = None) -> Path:
    config = load_config(config_path)
    colors = config.get("colors") or {}
    text = config.get("text") or {}
    layout = config.get("layout") or {}
    # End Screen背景ではチャンネルアイコンを描画しない（恒久ルール・2026-09-04）
    # チャンネル登録要素はYouTube Studio側で実配置するため。logo=null ならスキップ。
    logo_ref = config.get("logo")
    logo_path = _path(str(logo_ref)) if logo_ref else None
    if logo_ref and not logo_path.exists():
        raise FileNotFoundError(logo_path)
    output = output_path or (ROOT / "work" / "channel_cta.png")

    background = str(colors.get("background") or "#f7fbfe")
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), background)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, WIDTH, 14), fill=str(colors.get("top_bar") or "#2f74bb"))
    draw.rectangle((0, HEIGHT - SAFE_HEIGHT, WIDTH, HEIGHT), fill=background)
    draw.line((0, HEIGHT - SAFE_HEIGHT, WIDTH, HEIGHT - SAFE_HEIGHT), fill="#c8deed", width=3)

    panel = _box(layout.get("panel"))
    draw.rounded_rectangle(
        panel,
        radius=46,
        fill=str(colors.get("panel") or "#ffffff"),
        outline=str(colors.get("panel_outline") or "#d4e5f0"),
        width=3,
    )
    # 背景装飾（水玉）: YouTube End Screen用の右側reserved領域には置かず、
    # 左ブランド領域の中央（「デジタル」文字＝チャンネル名の背後）に低透明度で配置（2026-09-04・人間指定）。
    decor = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    dd = ImageDraw.Draw(decor)
    dd.ellipse((230, 360, 620, 750), fill=(234, 244, 255, 130))
    dd.ellipse((430, 430, 760, 760), fill=(234, 247, 238, 110))
    canvas.alpha_composite(decor)

    if logo_path is not None:
        logo_area = _box(layout.get("logo_area"))
        max_size = layout.get("logo_max") or [logo_area[2] - logo_area[0], logo_area[3] - logo_area[1]]
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((int(max_size[0]), int(max_size[1])), Image.Resampling.LANCZOS)
        logo_x = logo_area[0] + (logo_area[2] - logo_area[0] - logo.width) // 2
        logo_y = logo_area[1] + (logo_area[3] - logo_area[1] - logo.height) // 2
        shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        shadow.alpha_composite(logo, (logo_x + 8, logo_y + 10))
        canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(12)))
        canvas.alpha_composite(logo, (logo_x, logo_y))

    draw = ImageDraw.Draw(canvas)
    _centered(draw, _box(layout.get("channel_name_box")), str(text.get("channel_name") or ""), 92, 68, str(colors.get("ink") or "#173a68"))
    # CTAの情報本文も56px以上を維持し、全文を3行までで自然に表示する。
    _centered(draw, _box(layout.get("description_box")), str(text.get("description") or ""), 60, 56, str(colors.get("soft") or "#587187"), 3)

    # End Screen対応（2026-09-04・恒久）: 右側40〜45%を空け、関連動画・登録要素を自然に置ける構造。
    # 「次はこちら」ラベルは背景側の案内としてEnd Screen video領域の近くに置く（焼き込みなし）。
    next_label = config.get("next_label") if isinstance(config, dict) else None
    if next_label and next_label.get("text"):
        _centered(
            draw, _box(next_label.get("box")), str(next_label.get("text") or ""),
            48, 40, str(next_label.get("color") or "#587187"),
        )
    # 疑似subscribe（丸＋✓）は描画しない: 実公開時にYouTube Studio側の「チャンネル登録」End Screen要素を配置するため
    # （2026-09-04・人間指定）。本文とのoverlapもこれで解消。
    cta_box = _box(layout.get("cta_box"))
    draw.rounded_rectangle(
        cta_box,
        radius=28,
        fill=str(colors.get("green_fill") or "#eaf7ee"),
        outline=str(colors.get("green_outline") or "#63a975"),
        width=3,
    )
    # CTA本文は全文を自然な2行で表示（56px以上・60px標準・縮小で押し込まない）
    _centered(draw, _box(layout.get("cta_text_box")), str(text.get("cta") or ""), 60, 56, str(colors.get("green_text") or "#3f8c58"), 2)

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, "PNG")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(build_cta(args.config.resolve(), args.output.resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
