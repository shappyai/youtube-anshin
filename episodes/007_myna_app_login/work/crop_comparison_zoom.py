# -*- coding: utf-8 -*-
"""比較画像の右半分（v3）下部を拡大して保存."""
from PIL import Image

src = Image.open(r"episodes/007_myna_app_login/work/phase_b_review/cta_v2_v3_comparison.png")
w, h = src.size
right = src.crop((w // 2, 0, w, h))
right.crop((int(right.width * 0.08), int(right.height * 0.55), int(right.width * 0.72), right.height)).save(
    r"episodes/007_myna_app_login/work/cta_v3_zoom.png")
print("saved")
