# Subtitle preflight

Episode: 014_chiikawa_fleamarket_safety
Cues: 52
Safe width: 1800px (72px font measurement when available)

## FAIL

- SUB-003 seg 003: unnatural_japanese_line_break (9月2日の時点では、公式が確認 / していたのは、SNS投稿を受けて)
- SUB-003 seg 003: particle_or_auxiliary_orphan (9月2日の時点では、公式が確認 / していたのは、SNS投稿を受けて)
- SUB-048 seg 006: unnatural_japanese_line_break (ここでは、報道で伝えられた範囲として / 整理します。)
- SUB-007 seg 007: unnatural_japanese_line_break (ただし、フリマの出品者がその / 従業員だったのか、)
- なし

## WARN

- SUB-048: 2行の長さのバランスが悪い
- なし

## tts_reading_leakage

- result: PASS
- fail count: 0

## japanese_semantic_line_break

- policy: sentence meaning > bunsetsu integrity > modifier relation > visual balance > 72px
- long cues are split in time; font is not reduced to force a fit
- unnatural_japanese_line_break: 3
- word_split: 0
- conjugation_split: 0
- particle_or_auxiliary_orphan: 1
- orphan_particle_auxiliary: 1
- result: FAIL

## Summary

- result: FAIL
- fail count: 4
- warn count: 1
- cue text is read from episode.json; no character-count auto-splitting is performed
