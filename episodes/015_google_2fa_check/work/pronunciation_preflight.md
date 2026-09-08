# VOICEVOX pronunciation preflight

Episode: 015_google_2fa_check
Engine: PASS
Speaker: 剣崎雌雄 / ノーマル (style_id=21)
Query count: 42/42
Dictionary: config\voicevox_pronunciation.yaml

自動で pronunciation dictionary は変更していません。

## PASS

- seg 004 今日 → きょう（reading_overrides）
- seg 009 開きます → ひらきます（pronunciation dictionary）
- seg 018 開きます → ひらきます（pronunciation dictionary）
- seg 030 開きます → ひらきます（pronunciation dictionary）
- seg 042 今日 → きょう（reading_overrides）

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
- approved matches: 5
- human-approved context items: 0
- review items: 0
- dictionary mutation: none
