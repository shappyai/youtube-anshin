# VOICEVOX pronunciation preflight

Episode: 012_phishing_message_safety
Engine: PASS
Speaker: 剣崎雌雄 / ノーマル (style_id=21)
Query count: 79/79
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

- seg 004 開く/開ける / engine: メエルヤ'/エスエムエ'スノ/リ'ン_クカラ/ハイラ'ズ、ジブンデ'/コオ_シキ'/ア'プリヤ/コオ_シキ'/サイトオ'/ヒラ'イテ/カクニン'/シマ'_ス
  context: メールやSMSのリンクから入らず、自分で公式アプリや公式サイトを開いて確認します。
- seg 005 今日 / engine: キョ'オワ、ツ'ウハン、タ_クハイ'、カ'アド、ケエタイリョ'オキン、コオテキナ'/オシラセノ'/イツ'ツノ/バ'メンデ、コノ'/カクニンテ'ジュンオ/_ツカイマ'_ス
  context: 今日は、通販、宅配、カード、携帯料金、公的なお知らせの5つの場面で、この確認手順を使います。
- seg 011 今日 / engine: コノ'/ママ'デワ/コオニュウ'/デキマセ'ン、キョオジュウニ'/カクニン'/_シテ'/クダサ'イ、ト'/カ'イテ/アレ'バ、イソ'イデ/シマイマ'_ス
  context: 「このままでは購入できません」「今日中に確認してください」と書いてあれば、急いでしまいます。
- seg 051 開く/開ける / engine: リョ'オキンミバライノ/バ'メンデモ、イソガ'サレルホド、イッタン'/トジ'テ/コオ_シキオ'/ジブンデ'/ヒラ'ク、コレデ'/カクニンノ'/イリグチオ'/トリモドセマ'_ス
  context: 料金未払いの場面でも、急がされるほど、いったん閉じて公式を自分で開く。これで確認の入口を取り戻せます。
- seg 058 開く/開ける / engine: タ'ダシ、ス'ベテノ/ギョオセエキ'カンノ/レンラクノ'/テジュンガ'/オナジトワ'/カギリマセ'ン、ココロア'タリノ/テツ'ズキガ/ア'ル/バアイワ'、ソノ'/ジ_チタイヤ'/キ'カンノ/コオ_シキ'/サイトオ'/ジブンデ'/ヒラ'イテ/カクニン'/シマ'_ス
  context: ただし、すべての行政機関の連絡の手順が同じとは限りません。心当たりの手続きがある場合は、その自治体や機関の公式サイトを自分で開いて確認します。
- seg 063 開く/開ける / engine: _フタツ'メ、ジブンデ'/コオ_シキ'/ア'プリヤ/コオ_シキ'/サイトオ'/ヒラ'ク
  context: 2つ目、自分で公式アプリや公式サイトを開く。

## contextual_pronunciation_audio_gate

辞書の読みが登録済みでも、文脈ごとの実音声audio_queryを別ゲートで確認する。
- result: PASS
- 本物 regression segments: 7
- 本物？ direct query: PASS
- e-Tax direct query: PASS

## Summary

- result: REVIEW
- approved matches: 22
- review items: 6
- dictionary mutation: none
