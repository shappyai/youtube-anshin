# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
from PIL import Image
p = r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/work/rendered_final_scenes/scene_003.png'
a = np.asarray(Image.open(p).convert('RGB'))[:900]
dark = (a[:,:,0]<105)&(a[:,:,1]<155)&(a[:,:,2]<215)
rowc = dark.sum(axis=1)
# 8本以上の行を範囲表示
ys = np.where(rowc >= 8)[0]
groups = []
if len(ys):
    s = ys[0]; prev = ys[0]
    for y in ys[1:]:
        if y - prev > 3:
            groups.append((int(s), int(prev)))
            s = y
        prev = y
    groups.append((int(s), int(prev)))
print('groups(y):', groups[:25])
# 特定行の暗ピクセルのx位置
for y in (60, 200, 450, 700, 850):
    xs = np.where(dark[y])[0]
    print('y=', y, 'count=', len(xs), 'xrange=', (int(xs.min()), int(xs.max())) if len(xs) else None)
# 中央部のサンプル色
for (x, y) in ((300, 500), (900, 500), (1500, 800), (500, 800), (960, 450)):
    print('px', x, y, a[y, x])