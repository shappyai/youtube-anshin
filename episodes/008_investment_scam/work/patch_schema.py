# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
P = r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/episode.json'
d = json.load(open(P, encoding='utf-8'))
for sc in d['scenes']:
    if sc['id'] == 17 and not sc.get('main_message'):
        sc['main_message'] = '相談は、無料です。一人で悩まず、どうぞ'
    if sc['id'] == 18 and not sc.get('main_message'):
        sc['main_message'] = '送金する前に、この3つを'
d['publish']['description'] = '有名人が投資をすすめる広告を見て、LINEに案内されたら。お金を振り込む前に確認したい3つを、やさしく解説します（詳細はpublish.json）。'
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('patched:', [ (sc['id'], sc['main_message']) for sc in d['scenes'] if sc['id'] in (17, 18)])