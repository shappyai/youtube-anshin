# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
P = r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/work/production_metrics.json'
d = json.load(open(P, encoding='utf-8'))
d['narration'] = {'segment_count': 63, 'subtitle_count': 122, 'split_cues': 122 - 63, 'target_duration_sec': 330}
d['sources'] = {'primary_urls': 17, 'episode_json_sources': 15, 'saved_files': 15, 'direct_fetch_success': True}
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('metrics final ok')