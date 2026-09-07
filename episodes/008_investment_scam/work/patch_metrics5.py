# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
P = r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/work/production_metrics.json'
d = json.load(open(P, encoding='utf-8'))
d['scenes'] = {'total': 18, 'template': 13, 'gpt_image': 5, 'imagegen_native': 5, 'official_ui': 0, 'official_ui_planned': 1, 'icon_scenes': 8}
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('metrics scenes fixed')