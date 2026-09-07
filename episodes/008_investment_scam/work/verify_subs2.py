# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open(r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/episode.json', encoding='utf-8'))
segs = {s['id']: s for s in d['narration_segments']}
by_seg = {}
for sub in d['subtitles']:
    by_seg.setdefault(sub['segment_id'], []).append(sub)
ok = True
for seg_id, subs in sorted(by_seg.items()):
    subs_sorted = sorted(subs, key=lambda x: x.get('display_order', 0))
    joined = ''.join(''.join(x['text_lines']) for x in subs_sorted)
    if joined.replace(' ', '') != segs[seg_id]['narration'].replace(' ', ''):
        ok = False
        print('MISMATCH seg', seg_id, '|', joined, '|', segs[seg_id]['narration'])
print('segment-level subtitle consistency:', 'PASS' if ok else 'FAIL', '(segments:', len(by_seg), ')')
