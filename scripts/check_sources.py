from __future__ import annotations
import argparse, re
from urllib.parse import urlparse
from _common import episode_path, read_text

parser=argparse.ArgumentParser(); parser.add_argument('episode'); parser.add_argument('--strict',action='store_true'); args=parser.parse_args()
ep=episode_path(args.episode); text=read_text(ep/'sources.md')
urls=re.findall(r'https?://[^\s)>]+', text)
issues=[]
if len(urls)<2: issues.append('一次情報URLが2件未満です')
for u in urls:
    if not urlparse(u).netloc: issues.append(f'不正URL: {u}')
if not re.search(r'確認日\s*:\s*20\d{2}-\d{2}-\d{2}', text): issues.append('確認日 YYYY-MM-DD がありません')
if args.strict and re.search(r'\bTODO\b|未確認|example\.com', text, re.I): issues.append('TODO/未確認/placeholderが残っています')
print(f'URLs: {len(urls)}')
for u in urls: print(' -',u)
if issues:
    print('\nIssues:'); [print(' -',x) for x in issues]; raise SystemExit(1)
print('\nOK: sources.md basic checks passed')
