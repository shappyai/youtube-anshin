# VOICEVOX pronunciation preflight

Episode: 012_phishing_message_safety
Engine: REVIEW (offline)
Speaker: 剣崎雌雄 / ノーマル
Query count: 0/79
Dictionary: config\voicevox_pronunciation.yaml

自動で pronunciation dictionary は変更していません。

## PASS

- seg 002 本物 → ほんもの（pronunciation dictionary）
- seg 003 本物 → ほんもの（pronunciation dictionary）
- seg 008 本物 → ほんもの（pronunciation dictionary）
- seg 010 普段 → フダン（pronunciation dictionary）
- seg 012 普段 → フダン（pronunciation dictionary）
- seg 014 本物 → ほんもの（pronunciation dictionary）
- seg 015 開きます → ひらきます（pronunciation dictionary）
- seg 017 何も → ナニモ（pronunciation dictionary）
- seg 029 届け物 → とどけもの（pronunciation dictionary）
- seg 030 本物 → ほんもの（pronunciation dictionary）
- seg 030 本物 → ホンモノ / accent=4（segment accent_overrides）
- seg 034 カード会社 → カードがいしゃ（pronunciation dictionary）
- seg 036 ID → アイディイ（pronunciation dictionary）
- seg 038 カード会社 → カードがいしゃ（pronunciation dictionary）
- seg 039 開きます → ひらきます（pronunciation dictionary）
- seg 039 カード会社 → カードがいしゃ（pronunciation dictionary）
- seg 050 ID → アイディイ（pronunciation dictionary）
- seg 056 e-Tax → イータックス（pronunciation dictionary）
- seg 066 本物 → ほんもの（pronunciation dictionary）
- seg 069 ID → アイディイ（pronunciation dictionary）
- seg 071 カード会社 → カードがいしゃ（pronunciation dictionary）
- seg 079 本物 → ほんもの（pronunciation dictionary）

## REVIEW

- seg 030 contextual_pronunciation_audio_gate / engine: VOICEVOX /audio_query was not completed
  context: 辞書の読みだけでなく、実際の文脈audio_queryのモーラ・ピッチ・母音長を確認する回帰ゲート。
- seg 004 開く/開ける
  context: メールやSMSのリンクから入らず、自分で公式アプリや公式サイトを開いて確認します。
- seg 005 今日
  context: 今日は、通販、宅配、カード、携帯料金、公的なお知らせの5つの場面で、この確認手順を使います。
- seg 011 今日
  context: 「このままでは購入できません」「今日中に確認してください」と書いてあれば、急いでしまいます。
- seg 051 開く/開ける
  context: 料金未払いの場面でも、急がされるほど、いったん閉じて公式を自分で開く。これで確認の入口を取り戻せます。
- seg 058 開く/開ける
  context: ただし、すべての行政機関の連絡の手順が同じとは限りません。心当たりの手続きがある場合は、その自治体や機関の公式サイトを自分で開いて確認します。
- seg 063 開く/開ける
  context: 2つ目、自分で公式アプリや公式サイトを開く。

## contextual_pronunciation_audio_gate

辞書の読みが登録済みでも、文脈ごとの実音声audio_queryを別ゲートで確認する。
- result: REVIEW
- 本物 regression segments: 0
- 本物？ direct query: REVIEW
- e-Tax direct query: REVIEW
- failure: VOICEVOX /audio_query was not completed

## Summary

- result: REVIEW
- approved matches: 22
- review items: 7
- dictionary mutation: none
