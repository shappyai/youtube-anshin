from __future__ import annotations
import argparse, json, re
from _common import episode_path, read_text

parser=argparse.ArgumentParser(); parser.add_argument('episode'); args=parser.parse_args(); ep=episode_path(args.episode)
brief=read_text(ep/'brief.md'); script=read_text(ep/'script.md'); sources=read_text(ep/'sources.md')
urls=[]
for u in re.findall(r'https?://[^\s)>]+',sources):
    u=u.rstrip('.,')
    if u not in urls: urls.append(u)
# derive chapter titles from markdown H2 sections
chap=[]
for line in script.splitlines():
    m=re.match(r'^##\s+(?:(\d+):(\d+)\s+)?(.+)',line)
    if m:
        if m.group(1): chap.append(f'{m.group(1)}:{m.group(2)} {m.group(3)}')

data={
 'title_candidates':[],
 'selected_title':'',
 'description':'大人のデジタル安心室です。\n\nこの動画では、公式情報と実機を確認しながら分かりやすく説明します。\n\n【確認した公式情報】\n'+'\n'.join(f'- {u}' for u in urls)+'\n\n※画面や名称はアップデートで変わることがあります。',
 'chapters':chap,
 'pinned_comment':'分かりにくかった画面や、次に確認してほしいテーマがあればコメントで教えてください。',
 'source_urls':urls,
 'thumbnail_text':[]
}
# preserve existing title candidates
p=ep/'publish.json'
if p.exists():
    try:
        old=json.loads(p.read_text(encoding='utf-8')); data['title_candidates']=old.get('title_candidates',[]); data['thumbnail_text']=old.get('thumbnail_text',[])
    except Exception: pass
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(p)
