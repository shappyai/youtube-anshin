# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/fact_check.md'
t = open(P, encoding='utf-8').read()
# SRC ID 整合（episode.jsonにSRC-011 highrisk追加に伴い繰り下げ）
for old, new in [('SRC-014', 'SRC-015'), ('SRC-013', 'SRC-014'), ('SRC-012', 'SRC-013'), ('SRC-011', 'SRC-012')]:
    t = t.replace(old, new)
t = t.replace('※REVIEW-2表現修正済み', '※REVIEW-2表現修正済み・集計範囲（去年）も明記')
t = t.replace("| ((28,28), '広告やメッセージでの接触後、およそ9割がLINEに誘導', '警察庁令和7年確定値啓発資料p14/15「約9割」（SRC-005）※REVIEW-2表現修正済み・集計範囲（去年）も明記', 'PASS') |", "PLACEHOLDER")
open(P, 'w', encoding='utf-8').write(t)
print('fact_check SRC renumber ok')
