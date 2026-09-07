from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parents[1] / "assets" / "official" / "mhlw_warning_quote_full_v1.png"
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
            line_height = size + 22
            total = line_height * len(lines)
            y = top + max(0, (bottom - top - total) // 2)
            for line in lines:
                draw.text((left, y), line, font=font, fill=fill)
                y += line_height
            return size, lines
    raise RuntimeError(f"text does not fit: {text}")


canvas = Image.new("RGB", (1920, 1080), "#f1f8fd")
draw = ImageDraw.Draw(canvas)
draw.rectangle((0, 0, 1920, 14), fill="#2f74bb")
draw.rectangle((0, 900, 1920, 1080), fill="#f7fbfe")
draw.line((0, 900, 1920, 900), fill="#c8deed", width=3)
draw.rounded_rectangle((70, 54, 1850, 875), radius=36, fill="#ffffff", outline="#c8deed", width=5)
draw.rounded_rectangle((115, 92, 1805, 190), radius=24, fill="#eaf4ff")
fitted(draw, "厚生労働省の公式注意喚起", (155, 111, 1765, 171), 68, 56, "#173a68")
quote = "厚生労働省が、マイナンバーカードを健康保険証として使用いただくために、電話の音声案内やＳＭＳ（ショートメッセージサービス）などを用いて、直接、国民の皆様に対して、利用登録を要求することは一切ありません。"
fitted(draw, quote, (140, 235, 1780, 775), 78, 60, "#173a68", max_lines=5)
fitted(draw, "出典：厚生労働省公式", (140, 812, 1780, 870), 56, 48, "#587187")
canvas.save(OUT, "PNG")
print(OUT)
