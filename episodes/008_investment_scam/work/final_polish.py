# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
P = r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/episode.json'
d = json.load(open(P, encoding='utf-8'))

# (A) sources に fsa highrisk を SRC-011 として追加し、後続を繰り下げ（sources.mdと整合）
srcs = d['sources']
new_srcs = []
inserted = False
for s in srcs:
    if s['source_id'] == 'SRC-011' and not inserted:
        new_srcs.append({
            'source_id': 'SRC-011',
            'url': 'https://www.fsa.go.jp/ordinary/chuui/highrisk.html',
            'title': '無登録業者との取引は要注意！！～無登録業者との取引は高リスク～',
            'organization': '金融庁',
            'verified_at': '2026-09-05',
            'claim': 'SOS47もリンクする無登録業者注意ページ。無登録での金融商品取引業・暗号資産交換業は違法である旨。HTML本文を直接取得し確認（fsa_highrisk.html）。'
        })
        inserted = True
    sid = int(s['source_id'].split('-')[1])
    if sid >= 11:
        s['source_id'] = 'SRC-' + str(sid + 1).zfill(3)
    new_srcs.append(s)
# SRC-011 (kokusen) が highrisk に変わったので、kokusen news は SRC-012 になる（ループで+1済み）
d['sources'] = new_srcs
print('sources ids:', [s['source_id'] for s in d['sources']])

# (B) ナレーション微修正（集計範囲・初出言い換え）
fixes = {
  '警察庁のまとめでは、SNS型投資詐欺は、今年7月末までの暫定値で、6,566件です。':
    '警察庁のまとめでは、SNS型投資詐欺、つまりSNSの広告などを入口にした投資詐欺は、今年7月末までの暫定値で、6,566件です。',
  '被害額は、60代が、最も多いという、報告もあります。':
    '今年の上半期では、被害額は、60代が、最も多いという、報告もあります。',
  '広告やメッセージでの接触後、およそ9割が、LINEに、誘導されています。':
    '警察庁の去年のまとめでは、広告やメッセージでの接触後、およそ9割が、LINEに、誘導されています。',
  '株やFX、暗号資産の取引を、日本で行う会社は、国の登録が、必要です。':
    '株やFX、暗号資産、いわゆる仮想通貨の取引を、日本で行う会社は、国の登録が、必要です。',
}
for s in d['narration_segments']:
    if s['narration'] in fixes:
        s['narration'] = fixes[s['narration']]

# (C) 字幕を全再生成（。、単位・1cue最大2行・行長22字上限）
def unitize(t):
    units, cur = [], ''
    for ch in t:
        cur += ch
        if ch in '。、':
            units.append(cur); cur = ''
    if cur: units.append(cur)
    return units
def cues_for(t):
    units = unitize(t)
    cues, buf, ln = [], [], 0
    for u in units:
        if buf and (len(buf) >= 2 or ln + len(u) > 22):
            cues.append(buf); buf, ln = [], 0
        buf.append(u); ln += len(u)
    if buf: cues.append(buf)
    return cues if cues else [[t]]
segs = d['narration_segments']
subs = []
for s in segs:
    base = 'SUB-' + str(s['id']).zfill(3)
    cues = cues_for(s['narration'])
    ids = []
    for i, c in enumerate(cues):
        sid = base if len(cues) == 1 else base + '-' + str(i + 1)
        ids.append(sid)
        subs.append({'id': sid, 'text_lines': c, 'segment_id': s['id'], 'display_order': i})
    s['subtitle_ids'] = ids
d['subtitles'] = subs
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('segments=', len(segs), 'subtitles=', len(subs))
over = [(x['id'], x['text_lines']) for x in subs if any(len(l) > 23 for l in x['text_lines'])]
print('lines >23 chars:', over)
