# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image
p = r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/work/rendered_final_scenes/scene_003.png'
im = Image.open(p).convert('RGB')
print('size', im.size)
# 上半分を縦に潰して俯瞰（背景の様子を見る）
small = im.resize((480, 270))
small.save(r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/work/visual_review/diag_scene003_small.png')
# 左端の縦1ラインの色
px = im.load()
for y in (0, 50, 100, 200, 368, 500, 700, 838, 899):
    print('y', y, 'x=20:', px[20, y], 'x=960:', px[960, y], 'x=1900:', px[1900, y])