# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open(r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/episode.json', encoding='utf-8'))
segs = {s['id']: s for s in d['narration_segments']}
ok = True
for sub in d['subtitles']:
    joined = ''.join(sub['text_lines'])
    seg = segs[sub['segment_id']]
    norm = lambda x: x.replace(' ', '')
    if norm(joined) != norm(seg['narration']):
        ok = False
        print('MISMATCH', sub['id'], '|', joined, '|', seg['narration'])
print('subtitle-narration consistency:', 'PASS' if ok else 'FAIL')
scene_ids = sorted({s['scene_id'] for s in d['narration_segments']})
print('scenes used:', scene_ids)
print('seg ids sequential:', [s['id'] for s in d['narration_segments']] == list(range(1, len(d['narration_segments']) + 1)))
