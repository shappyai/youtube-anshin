# VOICEVOX pronunciation preflight

Episode: 014_chiikawa_fleamarket_safety
Engine: PASS
Speaker: 剣崎雌雄 / ノーマル (style_id=21)
Query count: 38/38
Dictionary: config\voicevox_pronunciation.yaml

自動で pronunciation dictionary は変更していません。

## PASS

- seg 001 ちいかわ → チイカワ（pronunciation dictionary）
- seg 004 ちいかわ → チイカワ（pronunciation dictionary）
- seg 006 フリマ → フリマ（pronunciation dictionary）
- seg 007 ちいかわ → チイカワ（pronunciation dictionary）
- seg 007 フリマ → フリマ（pronunciation dictionary）
- seg 016 フリマ → フリマ（pronunciation dictionary）
- seg 019 ちいかわ → チイカワ（pronunciation dictionary）
- seg 020 フリマ → フリマ（pronunciation dictionary）
- seg 022 フリマ → フリマ（pronunciation dictionary）
- seg 030 フリマ → フリマ（pronunciation dictionary）
- seg 031 188 → イチハチハチ（pronunciation dictionary）
- seg 032 188 → イチハチハチ（pronunciation dictionary）
- seg 036 188 → イチハチハチ（pronunciation dictionary）

## REVIEW

- seg 020 行う / engine: ミッツ'メワ、ケ'ッサイモ/レンラクモ'/フリマア'プリノ/ナ'カデ/オコナウ'/コト'デ_ス
  context: 3つ目は、決済も連絡もフリマアプリの中で行うことです。

## contextual_pronunciation_audio_gate

辞書の読みが登録済みでも、文脈ごとの実音声audio_queryを別ゲートで確認する。
- result: PASS
- 本物 regression segments: 0
- 本物？ direct query: PASS
- e-Tax direct query: REVIEW

## Summary

- result: REVIEW
- approved matches: 13
- review items: 1
- dictionary mutation: none
