# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
P = r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/episode.json'
d = json.load(open(P, encoding='utf-8'))
segs = d['narration_segments']
lines = []
lines.append('# Script — その投資広告、本物？LINEに誘導されたら確認したい3つ（Episode 008）')
lines.append('')
lines.append('制作メモ: Episode 002のホーム推薦実績（視聴4,718回・ホーム/ブラウジング流入約94%・平均視聴3:23・テレビ視聴約52.5%）を踏まえ、「社会的関心が高い × 50〜60代の自分事 × 具体的な困りごと × ホームで一瞬で意味がわかる」型の再現性を検証する。基準日: 2026-09-05。ナレーションは1文1segment（**63セグメント**・2026-09-05レビュー反映で句点分割）。**第一目標尺: 4:30〜5:30 + 共通CTA**（6分を超えない）。')
lines.append('')
lines.append('制作方針:')
lines.append('- problem-first: 冒頭0〜5秒で「広告→LINE誘導→本物?」、5〜15秒で「被害が増えている」、15〜25秒で「確認したい3つ」を一覧提示。')
lines.append('- 3つの確認は「行動の順番」: ①広告の有名人をそのまま信用しない ②LINEなどに誘導されたら一度止まる ③送金する前に登録と振込先を確認する。タイトル・冒頭・まとめで完全一致。')
lines.append('- 数字は集計範囲つきで1画面に集中（6,566件・約881億円・7割以上増・60代最多）。')
lines.append('- 事実と演出の分離: 実在UI・実在有名人を出さない。架空の広告・グループ画面は「イメージ」扱い。')
lines.append('- 安全規約: 「広告＝全部詐欺」「LINE自体が危険」と言わない。被害者を責める表現を使わない。')
lines.append('- 相談先は#9110・188・0570-050588（公式確認済み）。受付時間などの細部はナレーション/description。')
lines.append('')
sections = []
for s in segs:
    sec = s['section']
    if sec in ('はじめに',) and (not sections or sections[-1] != '## 0:00 はじめに（今日確認する3つ）'):
        sections.append('## 0:00 はじめに（今日確認する3つ）')
    elif sec == '1 / 3' and sections[-1] != '## 0:20 1 / 3 広告の有名人を、そのまま信用しない':
        sections.append('## 0:20 1 / 3 広告の有名人を、そのまま信用しない')
    elif sec == '2 / 3' and sections[-1] != '## 1:35 2 / 3 LINEなどに誘導されたら、一度止まる':
        sections.append('## 1:35 2 / 3 LINEなどに誘導されたら、一度止まる')
    elif sec == '3 / 3' and sections[-1] != '## 2:25 3 / 3 送金する前に、登録と振込先を確認する':
        sections.append('## 2:25 3 / 3 送金する前に、登録と振込先を確認する')
    elif sec == '困ったときは' and sections[-1] != '## 3:15 困ったときは（相談先）':
        sections.append('## 3:15 困ったときは（相談先）')
    elif sec == 'まとめ' and sections[-1] != '## 3:55 まとめ':
        sections.append('## 3:55 まとめ')
out = '\n'.join(lines) + '\n'
for sec in sections:
    out += '\n' + sec + '\n\n'
    for s in segs:
        if sections[sections.index(sec)] == sec and s['section'] in sec or (sec == '## 0:00 はじめに（今日確認する3つ）' and s['section'] == 'はじめに'):
            pass
out = out.replace('## 0:00 はじめに（今日確認する3つ）\n\n', '', 1) if False else out
# 単純化: セクションごとに書き出す
res = '\n'.join(lines) + '\n'
cur = None
for s in segs:
    sec = s['section']
    header = {'はじめに': '## 0:00 はじめに（今日確認する3つ）', '1 / 3': '## 0:20 1 / 3 広告の有名人を、そのまま信用しない', '2 / 3': '## 1:35 2 / 3 LINEなどに誘導されたら、一度止まる', '3 / 3': '## 2:25 3 / 3 送金する前に、登録と振込先を確認する', '困ったときは': '## 3:15 困ったときは（相談先）', 'まとめ': '## 3:55 まとめ'}[sec]
    if header != cur:
        res += '\n' + header + '\n\n'
        cur = header
    res += s['narration'] + '  \n'
res += '\n## 補足\n\n- 1文1segment（63セグメント）。字幕はepisode.jsonのサブタイトルcue（分割済み）を使用。\n- [SHOT-XX]タグはPhase Bで実機/公式captureが決まったsceneに付与（現状はscene番号と1:1対応）。\n- pronunciation REVIEW候補: SNS / LINE / FX / #9110 / 188 / 0570-050588 / 6,566件 / 881億円 / 4億4,000万円（Phase Bのaudio_queryで確認）。\n'
open(r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/script.md', 'w', encoding='utf-8').write(res)
print('script.md regenerated, segments=', len(segs))