from __future__ import annotations
import argparse, os, subprocess, tempfile
from pathlib import Path
import requests
from dotenv import load_dotenv
from _common import episode_path, read_text, strip_markdown_for_speech, load_yaml, ROOT

load_dotenv(ROOT/'.env')
parser=argparse.ArgumentParser(); parser.add_argument('episode'); parser.add_argument('--model'); parser.add_argument('--voice'); parser.add_argument('--dry-run',action='store_true'); args=parser.parse_args()
ep=episode_path(args.episode)
cfg=load_yaml(ROOT/'config/production.yaml')['tts']
model=args.model or os.getenv(cfg['model_env']) or cfg['default_model']
voice=args.voice or os.getenv(cfg['voice_env']) or cfg['default_voice']
key=os.getenv('OPENAI_API_KEY')
text=strip_markdown_for_speech(read_text(ep/'script.md'))
max_chars=int(cfg.get('max_chars_per_chunk',1200))
chunks=[]; buf=''
for para in text.splitlines():
    candidate=(buf+'\n'+para).strip()
    if len(candidate)>max_chars and buf:
        chunks.append(buf); buf=para
    else: buf=candidate
if buf: chunks.append(buf)
print(f'model={model} voice={voice} chunks={len(chunks)} chars={len(text)}')
if args.dry_run: raise SystemExit(0)
if not key: raise SystemExit('OPENAI_API_KEY is not set. Copy .env.example to .env and set the key.')

audio_dir=ep/'audio'; audio_dir.mkdir(exist_ok=True)
parts=[]
for i,chunk in enumerate(chunks,1):
    p=audio_dir/f'part_{i:02d}.mp3'
    r=requests.post('https://api.openai.com/v1/audio/speech',headers={'Authorization':f'Bearer {key}','Content-Type':'application/json'},json={'model':model,'voice':voice,'input':chunk},timeout=180)
    if not r.ok:
        raise SystemExit(f'TTS failed {r.status_code}: {r.text[:1000]}')
    p.write_bytes(r.content); parts.append(p); print('wrote',p)
concat=audio_dir/'concat.txt'
concat.write_text('\n'.join([f"file '{p.name}'" for p in parts]),encoding='utf-8')
out=audio_dir/'narration.mp3'
subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',concat.name,'-c','copy',out.name],cwd=audio_dir,check=True)
print('wrote',out)
