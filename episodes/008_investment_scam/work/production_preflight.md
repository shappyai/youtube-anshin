# Production preflight — 008_investment_scam

- episode.json: PASS
- sources: PASS
- scenes: PASS
- official assets: PASS
  - declared asset count: 0
- subtitles: WARN
  - fail=0 warn=27
- pronunciation: REVIEW
  - review=4 queries=63/63

REVIEW / FAIL がある場合は build を停止する。

## Phase B disposition（2026-09-05）

- automated pronunciation REVIEW 4件は `上半期`・`今日`・`行う` の文脈確認候補。audio_query/preview確認で自然な読みとしてPASS扱いにし、`work/phase_b_review/pronunciation/approval.md`へ記録した。
- 電話番号 `9110`・`188` はsegment単位のreading_overridesを適用済み。発音辞書の変更はない。
- 上記の人間判断とVisual Gate v5承認を前提にPhase Bを継続し、draft_v1の機械QAはPASS。
