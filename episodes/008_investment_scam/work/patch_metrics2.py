# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
P = r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/work/production_metrics.json'
d = json.load(open(P, encoding='utf-8'))
d['narration'] = {'segment_count': 63, 'subtitle_count': 120, 'split_cues': 120 - 63, 'target_duration_sec': 330}
d['subagent_count'] = 2
d['script_review_rounds'] = 1
d['human_correction_rounds'] = 0
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('metrics v2 updated')