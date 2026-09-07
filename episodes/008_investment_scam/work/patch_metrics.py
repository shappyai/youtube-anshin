# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
P = r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/work/production_metrics.json'
d = json.load(open(P, encoding='utf-8'))
d['subagent_count'] = 1
d['parallel_task_groups'] = 0
d['image_generation_agents'] = 0
d['image_generation_parallel_batches'] = 0
d['image_generation_calls'] = 5
d['image_regeneration_calls'] = 0
d['image_generation_elapsed_seconds'] = None
d['scene_render'] = {'rendered': 18, 'ok': 9, 'warn': 9, 'fail': 0, 'contact_sheet': 'work/visual_review/scene_contact_sheet.png'}
d['vision_text_qa'] = {'imagegen_native_scenes': 5, 'result': 'PASS（目視確認・誤字なし・実在人物なし）', 'final_judge': '人間Gate 2で確定'}
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('metrics updated')
