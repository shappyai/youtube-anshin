from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


EPISODE_DIR = Path(__file__).resolve().parents[1]
OUT = EPISODE_DIR / "assets" / "official" / "mhlw_warning_core_v1.png"
FONT = "C:/Windows/Fonts/YuGothB.ttc"


def draw_fitted_line(draw: ImageDraw.ImageDraw, text: str, box: tuple[int, int, int, int], max_size: int, min_size: int, fill: str) -> int:
    left, top, right, bottom = box
    for size in range(max_size, min_size - 1, -2):
        font = ImageFont.truetype(FONT, size)
        if draw.textlength(text, font=font) <= right - left:
            bbox = draw.textbbox((0, 0), text, font=font)
            y = top + max(0, (bottom - top - (bbox[3] - bbox[1])) // 2) - bbox[1]
            draw.text((left, y), text, font=font, fill=fill)
            return size
    raise RuntimeError(f"text does not fit: {text}")


canvas = Image.new("RGB", (1920, 1080), "#f1f8fd")
draw = ImageDraw.Draw(canvas)
draw.rectangle((0, 0, 1920, 14), fill="#2f74bb")
# Keep the bottom 180px clear for burned subtitles.
draw.rectangle((0, 900, 1920, 1080), fill="#f7fbfe")
draw.line((0, 900, 1920, 900), fill="#c8deed", width=3)
draw.rounded_rectangle((70, 54, 1850, 875), radius=36, fill="#ffffff", outline="#c8deed", width=5)
draw.rounded_rectangle((115, 92, 1805, 190), radius=24, fill="#eaf4ff")
draw_fitted_line(draw, "厚生労働省の公式注意喚起", (155, 111, 1765, 171), 68, 56, "#173a68")

# One screen = one core message. This is a faithful short display of the
# longer MHLW sentence recorded in sources.md; it is not an invented UI.
draw_fitted_line(draw, "電話やSMSで直接、", (150, 255, 1770, 395), 88, 64, "#173a68")
draw_fitted_line(draw, "健康保険証の利用登録を求めることはありません。", (150, 430, 1770, 650), 82, 64, "#173a68")
draw_fitted_line(draw, "出典：厚生労働省公式", (140, 804, 1780, 870), 56, 48, "#587187")
canvas.save(OUT, "PNG")
print(OUT)
