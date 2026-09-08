# VOICEVOX pronunciation preflight

Episode: 016_line_storage_cleanup
Engine: PASS
Speaker: 剣崎雌雄 / ノーマル (style_id=21)
Query count: 44/44
Dictionary: config\voicevox_pronunciation.yaml

自動で pronunciation dictionary は変更していません。

## PASS

- seg 003 今日 → きょう（reading_overrides）
- seg 012 開きます → ひらきます（pronunciation dictionary）
- seg 016 何も → ナニモ（pronunciation dictionary）
- seg 023 何も → ナニモ（pronunciation dictionary）
- seg 030 開く → ひらく（reading_overrides）
- seg 038 今日 → きょう（reading_overrides）

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
- approved matches: 6
- human-approved context items: 0
- review items: 0
- dictionary mutation: none
