from __future__ import annotations
import argparse, csv, subprocess, shutil
from pathlib import Path
from _common import episode_path, load_yaml, ROOT

parser=argparse.ArgumentParser(); parser.add_argument('episode'); parser.add_argument('--no-subs',action='store_true'); args=parser.parse_args()
ep=episode_path(args.episode); cfg=load_yaml(ROOT/'config/production.yaml')['video']
raw=ep/'raw'; audio=ep/'audio'/'narration.mp3'; manifest=ep/'media_manifest.csv'; srt=ep/'captions.srt'
if not audio.exists(): raise SystemExit(f'Missing narration: {audio}')
files=[]
if manifest.exists():
    with manifest.open(encoding='utf-8-sig',newline='') as f:
        for row in csv.DictReader(f):
            if row.get('use','yes').lower() in ('yes','y','1','true'):
                p=raw/row.get('filename','')
                if p.exists(): files.append(p)
if not files:
    files=sorted([p for p in raw.iterdir() if p.suffix.lower() in ('.mp4','.mov','.mkv')])
if not files: raise SystemExit(f'No raw video clips in {raw}')
work=ep/'_build'; shutil.rmtree(work,ignore_errors=True); work.mkdir()
normalized=[]
for i,p in enumerate(files,1):
    out=work/f'norm_{i:03d}.mp4'
    vf=f"scale={cfg['width']}:{cfg['height']}:force_original_aspect_ratio=decrease,pad={cfg['width']}:{cfg['height']}:(ow-iw)/2:(oh-ih)/2,fps={cfg['fps']}"
    subprocess.run(['ffmpeg','-y','-i',str(p),'-an','-vf',vf,'-c:v',cfg['video_codec'],'-preset',cfg['preset'],'-crf',str(cfg['crf']),str(out)],check=True)
    normalized.append(out)
concat=work/'concat.txt'; concat.write_text('\n'.join([f"file '{p.name}'" for p in normalized]),encoding='utf-8')
visual=work/'visual.mp4'
subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',concat.name,'-c','copy',visual.name],cwd=work,check=True)
out=ep/'draft.mp4'
cmd=['ffmpeg','-y','-i',str(visual),'-i',str(audio)]
if srt.exists() and not args.no_subs:
    # ffmpeg subtitles filter needs escaped path on Windows; cwd to episode keeps it simple
    rel_visual=str(visual.resolve()); rel_audio=str(audio.resolve())
    cmd=['ffmpeg','-y','-i',rel_visual,'-i',rel_audio,'-vf',"subtitles='captions.srt':force_style='FontSize=26,Outline=2,Shadow=0,MarginV=45'",'-c:v',cfg['video_codec'],'-preset',cfg['preset'],'-crf',str(cfg['crf']),'-c:a',cfg['audio_codec'],'-b:a',cfg['audio_bitrate'],'-shortest','draft.mp4']
    subprocess.run(cmd,cwd=ep,check=True)
else:
    cmd += ['-c:v','copy','-c:a',cfg['audio_codec'],'-b:a',cfg['audio_bitrate'],'-shortest',str(out)]
    subprocess.run(cmd,check=True)
print(out)
