# VOICEVOX pronunciation preflight

Episode: 013_line_old_version_support_end
Engine: PASS
Speaker: 剣崎雌雄 / ノーマル (style_id=21)
Query count: 74/74
Dictionary: config\voicevox_pronunciation.yaml

自動で pronunciation dictionary は変更していません。

## PASS

- seg 004 今日 → きょう（reading_overrides）
- seg 006 開く/開ける（human context approval）
- seg 007 上（human context approval）
- seg 023 開く/開ける（human context approval）
- seg 030 上（human context approval）
- seg 030 下（human context approval）
- seg 031 下（human context approval）
- seg 032 下（human context approval）
- seg 035 App Store → アップストア（pronunciation dictionary）
- seg 042 開きます → ひらきます（pronunciation dictionary）
- seg 044 開きます → ひらきます（pronunciation dictionary）
- seg 046 App Store → アップストア（pronunciation dictionary）
- seg 052 普段 → フダン（pronunciation dictionary）
- seg 053 App Store → アップストア（pronunciation dictionary）
- seg 069 今日 → きょう（reading_overrides）
- seg 073 上（human context approval）

## REVIEW

- なし

## contextual_pronunciation_audio_gate

辞書の読みが登録済みでも、文脈ごとの実音声audio_queryを別ゲートで確認する。
- result: PASS
- 本物 regression segments: 0
- 本物？ direct query: PASS
- e-Tax direct query: REVIEW

## Summary

- result: PASS
- approved matches: 16
- human-approved context items: 8
- review items: 0
- dictionary mutation: none

## Human approval

- result: HUMAN_APPROVED (8 context-specific items)
- approval record: work/pronunciation_human_approval_v3.md
- review pack: work/pronunciation_review_v3.wav
- audio regenerated: 0
- global dictionary additions: 0
