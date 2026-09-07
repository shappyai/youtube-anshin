from __future__ import annotations
import argparse, json, re, subprocess
from pathlib import Path
from _common import episode_path, read_text

parser=argparse.ArgumentParser(); parser.add_argument('episode'); args=parser.parse_args(); ep=episode_path(args.episode)
issues=[]
req=['brief.md','sources.md','script.md','shotlist.md','media_manifest.csv']
for name in req:
    if not (ep/name).exists(): issues.append(('重大','File',f'必須ファイルなし: {name}'))
script=read_text(ep/'script.md'); sources=read_text(ep/'sources.md')
if len(re.findall(r'https?://',sources))<2: issues.append(('重大','Fact','一次情報URLが2件未満'))
for word in ['100%','全員漏れて','絶対安全','絶対に安全']:
    if word in script: issues.append(('重大','Language',f'強すぎる断定: {word}'))
if not re.search(r'\[SHOT-\d+\]',script): issues.append(('中','Visual','SHOTタグが台本にありません'))
if '確認日:' not in sources: issues.append(('重大','Fact','sources.mdに確認日がありません'))
if re.search(r'\bTODO\b|example\.com',script+sources,re.I): issues.append(('中','File','TODO/placeholderが残っています'))
# raw privacy reminder only; automated visual inspection is delegated to Codex/human
raw_count=len([p for p in (ep/'raw').glob('*') if p.is_file() and p.name!='.gitkeep'])
if raw_count==0: issues.append(('中','Visual','実機素材がまだありません'))
if not (ep/'audio'/'narration.mp3').exists(): issues.append(('軽微','Audio','narration.mp3 未生成'))

order={'重大':0,'中':1,'軽微':2}; issues.sort(key=lambda x:order[x[0]])
lines=['# QC Report','',f'Episode: {ep.name}','']
if not issues: lines += ['## Result','重大/中/軽微の自動検査指摘はありません。','']
else:
    lines += ['## Issues','|重要度|区分|内容|','|---|---|---|']+[f'|{a}|{b}|{c}|' for a,b,c in issues]+['']
lines += ['## Human checks still required','- 実機画面とナレーションが一致しているか','- メール・電話・住所・通知など個人情報が映っていないか','- タイトル/サムネが内容以上に恐怖を煽っていないか','- 音声の読み間違いがないか','']
(ep/'qc.md').write_text('\n'.join(lines),encoding='utf-8')
print(ep/'qc.md')
for i in issues: print(i)
raise SystemExit(1 if any(x[0]=='重大' for x in issues) else 0)
