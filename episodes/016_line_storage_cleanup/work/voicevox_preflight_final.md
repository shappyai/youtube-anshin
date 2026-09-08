# VOICEVOX pronunciation preflight

Episode: 016_line_storage_cleanup
Engine: PASS
Speaker: 剣崎雌雄 / ノーマル (style_id=21)
Query count: 44/44
Dictionary: config\voicevox_pronunciation.yaml

自動で pronunciation dictionary は変更していません。

## PASS

- seg 003 今日 → きょう（reading_overrides）
- seg 005 キャッシュ → キャッシュ（pronunciation dictionary）
- seg 005 キャッシュ → low_high_plateau（pitch shape / mora QA対象）
- seg 010 キャッシュ → キャッシュ（pronunciation dictionary）
- seg 010 キャッシュ → low_high_plateau（pitch shape / mora QA対象）
- seg 012 開きます → ひらきます（pronunciation dictionary）
- seg 016 何も → ナニモ（pronunciation dictionary）
- seg 018 キャッシュ → キャッシュ（pronunciation dictionary）
- seg 018 キャッシュ → low_high_plateau（pitch shape / mora QA対象）
- seg 019 キャッシュ → キャッシュ（pronunciation dictionary）
- seg 019 キャッシュ → low_high_plateau（pitch shape / mora QA対象）
- seg 020 キャッシュ → キャッシュ（pronunciation dictionary）
- seg 020 キャッシュ → low_high_plateau（pitch shape / mora QA対象）
- seg 021 キャッシュ → キャッシュ（pronunciation dictionary）
- seg 021 キャッシュ → low_high_plateau（pitch shape / mora QA対象）
- seg 022 キャッシュ → キャッシュ（pronunciation dictionary）
- seg 022 キャッシュ → low_high_plateau（pitch shape / mora QA対象）
- seg 023 何も → ナニモ（pronunciation dictionary）
- seg 024 キャッシュ → キャッシュ（pronunciation dictionary）
- seg 024 キャッシュ → low_high_plateau（pitch shape / mora QA対象）
- seg 025 キャッシュ → キャッシュ（pronunciation dictionary）
- seg 025 キャッシュ → low_high_plateau（pitch shape / mora QA対象）
- seg 030 開く → ひらく（reading_overrides）
- seg 038 今日 → きょう（reading_overrides）
- seg 040 キャッシュ → キャッシュ（pronunciation dictionary）
- seg 040 キャッシュ → low_high_plateau（pitch shape / mora QA対象）
- seg 042 キャッシュ → キャッシュ（pronunciation dictionary）
- seg 042 キャッシュ → low_high_plateau（pitch shape / mora QA対象）

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
- approved matches: 28
- human-approved context items: 0
- review items: 0
- dictionary mutation: none
