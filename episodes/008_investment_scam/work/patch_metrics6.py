# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
P = r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/work/production_metrics.json'
d = json.load(open(P, encoding='utf-8'))
d['visual_gate_v2'] = {
    'applied_at': '2026-09-05',
    'theme_profile': 'adult_digital_soft_background',
    'theme_config': 'config/visual_theme.json',
    'template_scenes_redesigned': 13,
    'imagegen_native_kept': 5,
    'qa_ok': 11, 'qa_warn': 7, 'qa_fail': 0,
    'blank_white_slide': 0,
    'headline_min_px': 83,
    'contact_sheet_v2': 'work/visual_review/scene_contact_sheet_v2.png',
    'before_after': 'work/visual_review/design_before_after.png',
    'permanent_rule': ['AGENTS.md', 'templates/scenes/README.md']
}
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('metrics v3 ok')