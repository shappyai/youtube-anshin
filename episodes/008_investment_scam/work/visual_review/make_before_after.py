# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw, ImageOps
base = r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/work/visual_review'
before_dir = base + '/before_render'
after_dir = base + '/../rendered_final_scenes'
targets = [2, 3, 5, 7, 9, 12, 14, 15, 17, 18]
TW, TH = 470, 264
GAP = 14
LABEL_H = 30
header = 56
width = 40 + (TW * 2) + GAP + 30
height = header + 40 + len(targets) * (TH + LABEL_H)
sheet = Image.new('RGB', (width, height), '#eef4f9')
draw = ImageDraw.Draw(sheet)
font = None
from PIL import ImageFont
try:
    font = ImageFont.truetype('C:/Windows/Fonts/YuGothB.ttc', 26)
except Exception:
    font = ImageFont.load_default()
small = ImageFont.truetype('C:/Windows/Fonts/YuGothB.ttc', 20) if font is not ImageFont.load_default() else font
draw.text((40, 18), 'Episode 008 Visual Gate v2 — Design Before/After（左: old / 右: new）', font=font, fill='#173a68')
y = header + 30
for i, sid in enumerate(targets):
    bp = before_dir + ('/scene_%03d.png' % sid)
    ap = after_dir + ('/scene_%03d.png' % sid)
    x0 = 40
    for src, x in ((bp, x0), (ap, x0 + TW + GAP)):
        im = Image.open(src).convert('RGB')
        thumb = ImageOps.fit(im, (TW, TH))
        sheet.paste(thumb, (x, y))
        draw.rectangle((x, y, x + TW, y + TH), outline='#9db8cc', width=2)
    draw.text((x0, y + TH + 6), 'SCENE-%03d' % sid, font=small, fill='#2f74bb')
    y += TH + LABEL_H
out = base + '/design_before_after.png'
sheet.save(out)
print('saved', out, sheet.size)
