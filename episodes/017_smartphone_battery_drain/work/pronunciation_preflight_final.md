# VOICEVOX pronunciation preflight

Episode: 017_smartphone_battery_drain
Engine: PASS
Speaker: 剣崎雌雄 / ノーマル (style_id=21)
Query count: 34/34
Dictionary: config\voicevox_pronunciation.yaml

自動で pronunciation dictionary は変更していません。

## PASS

- seg 001 100% → ひゃくパーセント（reading_overrides）
- seg 001 方（human context approval）
- seg 002 バッテリー → バッテリイ（pronunciation dictionary）
- seg 002 バッテリー → low_high_plateau（pitch shape / mora QA対象）
- seg 003 iPhone → アイフォーン（reading_overrides）
- seg 004 今日 → きょう（reading_overrides）
- seg 005 バッテリー → バッテリイ（pronunciation dictionary）
- seg 005 バッテリー → low_high_plateau（pitch shape / mora QA対象）
- seg 006 バッテリー → バッテリイ（pronunciation dictionary）
- seg 006 バッテリー → low_high_plateau（pitch shape / mora QA対象）
- seg 007 バッテリー → バッテリイ（pronunciation dictionary）
- seg 007 バッテリー → low_high_plateau（pitch shape / mora QA対象）
- seg 008 iOS → アイオーエス（reading_overrides）
- seg 011 方（human context approval）
- seg 011 上（human context approval）
- seg 012 開く/開ける（human context approval）
- seg 012 上（human context approval）
- seg 013 iPhone → アイフォーン（reading_overrides）
- seg 015 iOS → アイオーエス（reading_overrides）
- seg 017 開きます → ひらきます（pronunciation dictionary）
- seg 022 バッテリー → バッテリイ（pronunciation dictionary）
- seg 022 バッテリー → low_high_plateau（pitch shape / mora QA対象）
- seg 023 iPhone → アイフォーン（reading_overrides）
- seg 023 バッテリー → バッテリイ（pronunciation dictionary）
- seg 023 バッテリー → low_high_plateau（pitch shape / mora QA対象）
- seg 025 バッテリー → バッテリイ（pronunciation dictionary）
- seg 025 バッテリー → low_high_plateau（pitch shape / mora QA対象）
- seg 026 Apple → アップル（reading_overrides）
- seg 027 バッテリー → バッテリイ（pronunciation dictionary）
- seg 027 バッテリー → low_high_plateau（pitch shape / mora QA対象）
- seg 028 100% → ひゃくパーセント（reading_overrides）
- seg 028 方（human context approval）
- seg 029 バッテリー → バッテリイ（pronunciation dictionary）
- seg 029 バッテリー → low_high_plateau（pitch shape / mora QA対象）
- seg 031 バッテリー → バッテリイ（pronunciation dictionary）
- seg 031 バッテリー → low_high_plateau（pitch shape / mora QA対象）
- seg 033 iOS → アイオーエス（reading_overrides）
- seg 033 Apple → アップル（reading_overrides）
- seg 034 今日 → きょう（reading_overrides）

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
- approved matches: 39
- human-approved context items: 6
- review items: 0
- dictionary mutation: none

## Human approval

- result: HUMAN_APPROVED (6 context-specific items)
- approval record: work/human_review.json
- review pack: audio/voicevox_kenzaki_v2/narration_kenzaki_auto.wav
- audio regenerated: 0
- global dictionary additions: 0
