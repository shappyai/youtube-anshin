from __future__ import annotations
import argparse, re, shutil
from pathlib import Path
from _common import ROOT

parser=argparse.ArgumentParser()
parser.add_argument('--number', type=int, required=True)
parser.add_argument('--slug', required=True)
parser.add_argument('--title', required=True)
args=parser.parse_args()

slug=re.sub(r'[^a-zA-Z0-9_-]+','_',args.slug).strip('_').lower()
ep=ROOT/'episodes'/f'{args.number:03d}_{slug}'
if ep.exists(): raise SystemExit(f'Already exists: {ep}')
for d in ['raw','audio','final','thumbnail']:
    (ep/d).mkdir(parents=True, exist_ok=True)
    (ep/d/'.gitkeep').write_text('',encoding='utf-8')

replacements={'{{NUMBER}}':f'{args.number:03d}','{{SLUG}}':slug,'{{TITLE}}':args.title}
for name in ['brief.md','sources.md','script.md','shotlist.md','publish.json']:
    src=ROOT/'templates'/name
    text=src.read_text(encoding='utf-8')
    for k,v in replacements.items(): text=text.replace(k,v)
    (ep/name).write_text(text,encoding='utf-8')
(ep/'media_manifest.csv').write_text('shot_id,filename,use,notes\n',encoding='utf-8-sig')
print(ep)
