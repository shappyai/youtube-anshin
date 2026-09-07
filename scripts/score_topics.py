from __future__ import annotations
import argparse, csv
from pathlib import Path

parser=argparse.ArgumentParser(); parser.add_argument('input_csv'); parser.add_argument('--output',default='ranked_topics.csv'); args=parser.parse_args()
rows=list(csv.DictReader(open(args.input_csv,encoding='utf-8-sig')))
required=['demand','competition_gap','evergreen','real_device','brand_fit']
for r in rows:
    vals=[]
    for k in required:
        try: vals.append(float(r.get(k,0)))
        except: vals.append(0)
    # demand 30%, gap 20%, evergreen 15%, demo 15%, brand 20%
    r['score']=round(vals[0]*0.30+vals[1]*0.20+vals[2]*0.15+vals[3]*0.15+vals[4]*0.20,2)
rows.sort(key=lambda r:float(r['score']),reverse=True)
fields=list(rows[0].keys()) if rows else ['topic','score']
with open(args.output,'w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
print(args.output)
