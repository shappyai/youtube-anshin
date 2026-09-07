# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image
p = r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/work/rendered_final_scenes/scene_003.png'
im = Image.open(p).convert('RGB')
px = im.load()
samples = [(20, 200), (960, 140), (1900, 200), (20, 700), (960, 450), (1900, 800), (1810, 850)]
for (x, y) in samples:
    print('px', x, y, px[x, y])
w, h = im.size
near_white = 0
total = w * min(h - 180, 900)
for yy in range(0, min(h - 180, 900), 4):
    for xx in range(0, w, 4):
        r_, g_, b_ = px[xx, yy]
        if r_ >= 245 and g_ >= 245 and b_ >= 245:
            near_white += 1
print('near_white ratio:', round(near_white / (total / 16), 3))