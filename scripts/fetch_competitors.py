from __future__ import annotations
"""Optional YouTube Data API helper.

Input CSV must contain a `channel_id` column. Existing human-curated competitor DB does
not require this script; use it after you have collected channel IDs.
"""
import argparse, csv, os, requests
from pathlib import Path
from dotenv import load_dotenv
from _common import ROOT
load_dotenv(ROOT/'.env')
parser=argparse.ArgumentParser(); parser.add_argument('input_csv'); parser.add_argument('--output',default='data/competitors_api.csv'); args=parser.parse_args()
key=os.getenv('YOUTUBE_API_KEY')
if not key: raise SystemExit('YOUTUBE_API_KEY not set in .env')
rows=list(csv.DictReader(open(args.input_csv,encoding='utf-8-sig')))
ids=[r['channel_id'] for r in rows if r.get('channel_id')]
if not ids: raise SystemExit('No channel_id values')
out=[]
for i in range(0,len(ids),50):
    params={'part':'snippet,statistics','id':','.join(ids[i:i+50]),'key':key}
    r=requests.get('https://www.googleapis.com/youtube/v3/channels',params=params,timeout=60); r.raise_for_status()
    for item in r.json().get('items',[]):
        st=item.get('statistics',{}); sn=item.get('snippet',{})
        out.append({'channel_id':item['id'],'title':sn.get('title'),'subscribers':st.get('subscriberCount'),'views':st.get('viewCount'),'videos':st.get('videoCount')})
p=ROOT/args.output; p.parent.mkdir(parents=True,exist_ok=True)
with p.open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['channel_id','title','subscribers','views','videos']); w.writeheader(); w.writerows(out)
print(p)
