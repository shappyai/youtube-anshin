from __future__ import annotations
"""Create local dummy clips/audio to test the FFmpeg pipeline. Not for publishing."""
import argparse, subprocess
from _common import episode_path
parser=argparse.ArgumentParser(); parser.add_argument('episode'); args=parser.parse_args(); ep=episode_path(args.episode)
raw=ep/'raw'; raw.mkdir(exist_ok=True)
colors=['#eaf2f8','#e9f7ef','#fff7e6','#f5f7fa','#edf2f7']
for i,c in enumerate(colors,1):
    p=raw/f'shot_{i:02d}_demo.mp4'
    subprocess.run(['ffmpeg','-y','-f','lavfi','-i',f'color=c={c}:s=1920x1080:d=2:r=30','-c:v','libx264','-pix_fmt','yuv420p',str(p)],check=True)
# silent 8 sec narration placeholder
ad=ep/'audio'; ad.mkdir(exist_ok=True); out=ad/'narration.mp3'
subprocess.run(['ffmpeg','-y','-f','lavfi','-i','anullsrc=r=44100:cl=stereo','-t','8','-q:a','9','-acodec','libmp3lame',str(out)],check=True)
print('Demo assets created. DO NOT PUBLISH THEM.')
