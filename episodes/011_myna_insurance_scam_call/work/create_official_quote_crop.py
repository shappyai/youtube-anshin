from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parents[1] / "assets" / "official" / "mhlw_warning_quote_crop_v1.png"
FONT = "C:/Windows/Fonts/YuGothB.ttc"


def fitted(draw, text, box, max_size, min_size, fill, max_lines=1):
    left, top, right, bottom = box
    for size in range(max_size, min_size - 1, -2):
        font = ImageFont.truetype(FONT, size)
        lines = []
        current = ""
        for char in text:
            candidate = current + char
            if current and draw.textlength(candidate, font=font) > right - left:
                lines.append(current)
                current = char
            else:
                current = candidate
        if current:
            lines.append(current)
        if len(lines) <= max_lines:
            line_height = size + 14
            total = line_height * len(lines)
            y = top + max(0, (bottom - top - total) // 2)
            for line in lines:
                draw.text((left, y), line, font=font, fill=fill)
                y += line_height
            return size, lines
    raise RuntimeError(f"text does not fit: {text}")


canvas = Image.new("RGB", (1400, 760), "#ffffff")
draw = ImageDraw.Draw(canvas)
draw.rounded_rectangle((4, 4, 1396, 756), radius=28, fill="#ffffff", outline="#c8deed", width=4)
draw.rounded_rectangle((38, 34, 1362, 116), radius=20, fill="#eef6fc")
fitted(draw, "厚生労働省の公式注意喚起", (70, 48, 1330, 102), 52, 44, "#173a68")
quote = "厚生労働省が、マイナンバーカードを健康保険証として使用いただくために、電話の音声案内やＳＭＳ（ショートメッセージサービス）などを用いて、直接、国民の皆様に対して、利用登録を要求することは一切ありません。"
fitted(draw, quote, (78, 154, 1322, 594), 54, 44, "#173a68", max_lines=5)
fitted(draw, "出典：厚生労働省公式", (78, 640, 1322, 708), 48, 44, "#587187")
canvas.save(OUT, "PNG")
print(OUT)
