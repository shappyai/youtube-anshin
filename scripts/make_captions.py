from __future__ import annotations
import argparse, re
from pathlib import Path
from _common import episode_path, read_text, strip_markdown_for_speech, load_yaml, ROOT

parser=argparse.ArgumentParser(); parser.add_argument('episode'); parser.add_argument('--duration',type=float,default=600); args=parser.parse_args()
ep=episode_path(args.episode)
text=strip_markdown_for_speech(read_text(ep/'script.md'))
# sentence-ish chunks
parts=[]
for para in text.splitlines():
    for s in re.split(r'(?<=[。！？!?])', para):
        s=s.strip()
        if s: parts.append(s)
if not parts: raise SystemExit('No script text found')
weights=[max(len(p),6) for p in parts]; total=sum(weights); cursor=0.0

def ts(sec):
    ms=int(round((sec-int(sec))*1000)); s=int(sec)%60; m=(int(sec)//60)%60; h=int(sec)//3600
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

lines=[]
for idx,(p,w) in enumerate(zip(parts,weights),1):
    dur=max(1.2,args.duration*w/total); start=cursor; end=min(args.duration,cursor+dur); cursor=end
    lines += [str(idx), f'{ts(start)} --> {ts(end)}', p, '']
(ep/'captions.srt').write_text('\n'.join(lines),encoding='utf-8')
print(f'Wrote {ep/"captions.srt"}: {len(parts)} captions / target {args.duration:.1f}s')
