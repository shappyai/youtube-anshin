from __future__ import annotations
import argparse, subprocess, sys
parser=argparse.ArgumentParser(); parser.add_argument('episode'); parser.add_argument('--duration',type=float,default=600); args=parser.parse_args()
cmds=[
    [sys.executable,'scripts/check_sources.py',args.episode],
    [sys.executable,'scripts/make_captions.py',args.episode,'--duration',str(args.duration)],
    [sys.executable,'scripts/qc_episode.py',args.episode],
    [sys.executable,'scripts/youtube_metadata.py',args.episode],
]
for c in cmds:
    print('>', ' '.join(c)); r=subprocess.run(c)
    if r.returncode not in (0,1): raise SystemExit(r.returncode)
