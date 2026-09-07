from __future__ import annotations
import argparse, json, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from _common import episode_path, find_font

parser=argparse.ArgumentParser(); parser.add_argument('episode'); parser.add_argument('--text',required=True); parser.add_argument('--font'); args=parser.parse_args()
ep=episode_path(args.episode); out=ep/'thumbnail'; out.mkdir(exist_ok=True)
font_path=args.font or find_font()
if not font_path: raise SystemExit('Japanese font not found. Use --font path/to/font')

W,H=1280,720
variants=[
    ((245,248,252),(23,50,77),(43,108,176),'公式確認'),
    ((250,250,250),(28,37,54),(183,121,31),'実機確認'),
    ((239,250,246),(28,65,52),(47,133,90),'一緒に確認'),
]
for i,(bg,fg,accent,badge) in enumerate(variants,1):
    im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
    fmain=ImageFont.truetype(font_path,116); fbadge=ImageFont.truetype(font_path,36); fsmall=ImageFont.truetype(font_path,44)
    d.rounded_rectangle((70,58,300,125),24,fill=accent); d.text((95,72),badge,font=fbadge,fill='white')
    # abstract phone card
    d.rounded_rectangle((790,90,1170,650),45,fill=(255,255,255),outline=accent,width=8)
    d.rounded_rectangle((850,180,1110,260),18,fill=accent)
    d.ellipse((885,350,1075,540),fill=(245,247,250),outline=accent,width=8)
    d.line((930,445,985,500,1045,390),fill=accent,width=18,joint='curve')
    wrapped='\n'.join(textwrap.wrap(args.text,width=7))
    d.multiline_text((70,190),wrapped,font=fmain,fill=fg,spacing=16)
    d.text((74,610),'大人のデジタル安心室',font=fsmall,fill=accent)
    p=out/f'thumb_{i:02d}.png'; im.save(p,quality=95)
    print(p)
