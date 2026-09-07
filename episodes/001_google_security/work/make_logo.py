# -*- coding: utf-8 -*-
"""チャンネル共通ロゴ（仮・ブランドニュートラル）: work/channel_logo.png を生成。
Googleロゴ・G・商標は含めない。後から画像を差し替え可能な外部ファイル。
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WORK = Path(__file__).resolve().parent


def main():
    S = 4
    img = Image.new("RGBA", (200 * S, 200 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([10, 10, 190 * S - 10, 190 * S - 10], radius=34 * S,
                        fill=(31, 42, 55, 255))
    pts = [
        (100 * S, 38 * S),
        (150 * S, 62 * S),
        (150 * S, 112 * S),
        (100 * S, 158 * S),
        (50 * S, 112 * S),
        (50 * S, 62 * S),
    ]
    d.polygon(pts, fill=(46, 109, 164, 255))
    d.line([(72 * S, 108 * S), (92 * S, 128 * S), (130 * S, 84 * S)],
           fill=(255, 255, 255, 255), width=12 * S, joint="curve")
    img = img.resize((200, 200), Image.LANCZOS)
    img.save(WORK / "channel_logo.png")
    print("work/channel_logo.png written (brand-neutral placeholder)")


if __name__ == "__main__":
    main()
