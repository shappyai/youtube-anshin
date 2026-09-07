# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/fact_check.md'
t = open(P, encoding='utf-8').read()
t = t.replace('（SRC-012/012）', '（SRC-012/013）')
t = t.replace('（SRC-013/013）', '（SRC-013）')
t = t.replace('（SRC-014/014）', '（SRC-014）')
t = t.replace('（40行: 日本で行う会社は国の登録が必要）', '')
t = t.replace('（48行: 詐欺かも→送金しない）', '')
t = t.replace('株やFX、暗号資産の取引は国の登録が必要（', '株やFX、暗号資産（仮想通貨）の取引は国の登録が必要（')
open(P, 'w', encoding='utf-8').write(t)
print('fact_check cleaned')
