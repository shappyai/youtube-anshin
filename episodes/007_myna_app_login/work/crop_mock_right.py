# -*- coding: utf-8 -*-
from PIL import Image

src = Image.open(r"episodes/007_myna_app_login/work/phase_b_review/end_screen_mock_v3.png")
src.crop((1050, 0, 1920, 540)).save(r"episodes/007_myna_app_login/work/mock_v3_right_top.png")
src.crop((1500, 400, 1920, 960)).save(r"episodes/007_myna_app_login/work/mock_v3_right_bottom.png")
print("saved")
