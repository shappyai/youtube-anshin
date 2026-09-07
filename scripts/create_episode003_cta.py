"""Create the Episode 003 channel CTA from the current channel logo."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from scene_renderer import HEIGHT, SAFE_HEIGHT, WIDTH, draw_fitted  # noqa: E402


OUTPUT = ROOT / "episodes" / "003_line_renewal" / "output" / "review" / "cta_v3.png"
LOGO = ROOT / "local" / "channel" / "icon.png"


def centered(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str,
             max_size: int, min_size: int, fill: str, max_lines: int = 1) -> None:
    draw_fitted(draw, box, text, max_size, min_size, fill, max_lines, "center", 0.14)


def build() -> Path:
    if not LOGO.exists():
        raise FileNotFoundError(LOGO)

    canvas = Image.new("RGBA", (WIDTH, HEIGHT), "#f7fbfe")
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, WIDTH, 14), fill="#2f74bb")
    draw.rectangle((0, HEIGHT - SAFE_HEIGHT, WIDTH, HEIGHT), fill="#f7fbfe")
    draw.line((0, HEIGHT - SAFE_HEIGHT, WIDTH, HEIGHT - SAFE_HEIGHT), fill="#c8deed", width=3)

    # Episode 001's restrained end-card language: calm white field, blue/green
    # accents, centered text hierarchy, and no theme-specific app screen.
    draw.rounded_rectangle((90, 105, 1830, 860), radius=46, fill="#ffffff", outline="#d4e5f0", width=3)
    draw.ellipse((88, 160, 600, 672), fill="#eaf4ff")
    draw.ellipse((430, 510, 630, 710), fill="#eaf7ee")

    logo = Image.open(LOGO).convert("RGBA")
    logo.thumbnail((380, 380), Image.Resampling.LANCZOS)
    logo_x = 155 + (390 - logo.width) // 2
    logo_y = 205 + (390 - logo.height) // 2
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow.alpha_composite(logo, (logo_x + 8, logo_y + 10))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(logo, (logo_x, logo_y))

    draw = ImageDraw.Draw(canvas)
    centered(draw, (620, 165, 1730, 235), "やさしく・安全に・安心して", 44, 34, "#2f74bb")
    centered(draw, (585, 275, 1770, 395), "大人のデジタル安心室", 92, 68, "#173a68")
    centered(
        draw,
        (620, 435, 1770, 555),
        "スマホやパソコンを、もっと安全・快適に使うための情報をお届けします",
        50,
        38,
        "#587187",
        2,
    )

    cta_box = (650, 625, 1770, 755)
    draw.rounded_rectangle(cta_box, radius=28, fill="#eaf7ee", outline="#63a975", width=3)
    check_center = (710, 690)
    draw.ellipse((check_center[0] - 28, check_center[1] - 28, check_center[0] + 28, check_center[1] + 28), fill="#63a975")
    draw.line((check_center[0] - 14, check_center[1], check_center[0] - 2, check_center[1] + 13), fill="#ffffff", width=7)
    draw.line((check_center[0] - 2, check_center[1] + 13, check_center[0] + 20, check_center[1] - 16), fill="#ffffff", width=7)
    centered(draw, (760, 645, 1710, 735), "チャンネル登録・高評価もよろしくお願いします", 52, 40, "#3f8c58")
    centered(draw, (650, 795, 1770, 850), "怖がらせる前に、確認する。", 38, 30, "#2f74bb")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUTPUT, "PNG")
    return OUTPUT


if __name__ == "__main__":
    print(build())
