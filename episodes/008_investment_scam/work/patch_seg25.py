# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
P = r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/episode.json'
d = json.load(open(P, encoding='utf-8'))
for s in d['narration_segments']:
    if s['id'] == 25:
        s['narration'] = '広告やメッセージでの接触後、およそ9割が、LINEに、誘導されています。'
for sub in d['subtitles']:
    if sub['id'] == 'SUB-025':
        sub['text_lines'] = ['広告やメッセージでの接触後、', 'およそ9割が、LINEに、誘導されています。']
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('patched ok; seg25 =', [s['narration'] for s in d['narration_segments'] if s['id']==25][0])