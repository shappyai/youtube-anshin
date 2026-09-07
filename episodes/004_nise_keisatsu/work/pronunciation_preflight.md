# VOICEVOX pronunciation preflight

Episode: 004_nise_keisatsu
Engine: PASS
Speaker: 剣崎雌雄 / ノーマル (style_id=21)
Query count: 72/72
Dictionary: config\voicevox_pronunciation.yaml

自動で pronunciation dictionary は変更していません。

## PASS

- seg 016 方 → かた（reading_overrides）
- seg 017 方 → かた（reading_overrides）
- seg 025 ＋ → プラス（reading_overrides）
- seg 027 ＋81 → プラスはちいち（reading_overrides）
- seg 040 ＃9110 → シャープきゅういちいちまる（reading_overrides）
- seg 057 方 → かた（reading_overrides）
- seg 060 方 → かた（reading_overrides）
- seg 071 ＃9110 → シャープきゅういちいちまる（reading_overrides）
- seg 071 188 → いちはちはち（reading_overrides）

## REVIEW

- seg 004 今日 / engine: キョ'オワ、マ'ズ、ナ'ニオ/カクニン'/スレ'バ/ヨ'イカ、オ'、ジュンバンニ'/セツメエ'/シマ'_ス
  context: 今日は、まず「何を確認すればよいか」を、順番に説明します。
- seg 016 上 / engine: ト'クニ、コト_シ'/カミハ'ンキノ/トオケエデワ'、ニセケエサツ'サギノ/ヒ'ガイワ、ナナジュウ'ダイノ/ホ'オガ/モット'モ/オ'オクナッテ/イマ'_ス
  context: 特に、今年上半期の統計では、ニセ警察詐欺の被害は、70代の方が最も多くなっています。
- seg 025 方 / engine: ツギ'ニ、タ'ス、カラ'/ハジマル'/コ_クサイデ'ンワノ/ミワケ'カタオ/カクニン'/シマ'_ス
  context: 次に、「＋」から始まる国際電話の見分け方を確認します。
- seg 030 下 / engine: サ'ラニ、ジツザイノ'/ケエサ_ツショノ'/バンゴ'オニ/ニセテ'、_シタ'/ヨン'ケタガ、ゼロイ'チ/イチゼ'ロ、ノ'/コ_クサイデンワバンゴ'オオ/_ツカウ'/ジレエモ'、メダ'ッテ/イマ'_ス
  context: さらに、実在の警察署の番号に似せて、下4桁が「0110」の国際電話番号を使う事例も、目立っています。
- seg 066 今日 / engine: キョ'オノ/マトメデ'_ス
  context: 今日のまとめです。
- seg 069 今日 / engine: ミッツ'、コ_クサイデ'ンワオ/トメル'/テツ'ズ_キカ、ブロ'ックノ/セッテエオ'、キョ'オノ/ウチニ'/タメシ'テ/ミマショ'オ
  context: 三つ、国際電話を止める手続きか、ブロックの設定を、今日のうちに試してみましょう。

## Summary

- result: REVIEW
- approved matches: 9
- review items: 6
- dictionary mutation: none

## 人間承認結果（2026-08-31・Phase B後半）

全72セグメントの読みを人間レビュー済み。承認内容はepisode.jsonのreading_overridesとwork/human_review.jsonへ反映済み。

### OVERRIDE_APPLIED（9項目・TTS入力のみ差し替え。表示字幕は原文のまま）

- seg 016 方 → かた（70代のかたが）
- seg 017 方 → かた（50代以上のかたが）
- seg 025 ＋ → プラス（「プラス」から始まる国際電話）
- seg 027 ＋81 → プラスはちいち（「プラスはちいち」は日本の番号です）
- seg 040 ＃9110 → シャープきゅういちいちまる
- seg 057 方 → かた（固定電話を使っているかたは）
- seg 060 方 → かた（手続きが難しいかたは）
- seg 071 ＃9110 → シャープきゅういちいちまる
- seg 071 188 → いちはちはち

### APPROVED（6項目・現状の読みで確定。overrideなし）

- seg 004 今日 → きょう（現状のまま）
- seg 016 上半期 → かみはんき（現状のまま）
- seg 025 見分け方 → みわけかた（現状のまま）
- seg 030 下4桁 → したよんけた／0110はゼロイチイチゼロの一桁読み（現状のまま。不自然なまとまり読みでないためoverride不要）
- seg 066 今日 → きょう（現状のまま）
- seg 069 今日 → きょう（現状のまま）

### 電話番号・記号の確定（表示とVOICEVOX入力は分離）

- 0120-210-364 → ゼロイチニイゼロ ニイイチゼロ サンロクヨン（一桁読みを採用・変更なし）
- 0110 → ゼロイチイチゼロ系の一桁読み（セグメント30・現状のまま）

### 方針の遵守

- 「方」「今」「上」「下」などの文脈依存語はglobal pronunciation dictionaryへ登録していない。適用はsegment overrideのみ。
- 既存の人間承認済み共通辞書（config/voicevox_pronunciation.yaml）は変更なし。
- 新規global dictionary entryの自動作成はなし。
- **unresolved REVIEW = 0**（production preflightのpronunciationゲートはPASS）。
