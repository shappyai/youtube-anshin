# VOICEVOX pronunciation preflight

Episode: 017_smartphone_battery_drain
Engine: PASS
Speaker: 剣崎雌雄 / ノーマル (style_id=21)
Query count: 34/34
Dictionary: config\voicevox_pronunciation.yaml

自動で pronunciation dictionary は変更していません。

## PASS

- seg 001 100% → ひゃくパーセント（reading_overrides）
- seg 003 iPhone → アイフォーン（reading_overrides）
- seg 004 今日 → きょう（reading_overrides）
- seg 008 iOS → アイオーエス（reading_overrides）
- seg 013 iPhone → アイフォーン（reading_overrides）
- seg 015 iOS → アイオーエス（reading_overrides）
- seg 017 開きます → ひらきます（pronunciation dictionary）
- seg 023 iPhone → アイフォーン（reading_overrides）
- seg 026 Apple → アップル（reading_overrides）
- seg 028 100% → ひゃくパーセント（reading_overrides）
- seg 033 iOS → アイオーエス（reading_overrides）
- seg 033 Apple → アップル（reading_overrides）
- seg 034 今日 → きょう（reading_overrides）

## REVIEW

- seg 001 方 / engine: サイキン'、ア'サワ/ヒャ_クパアセ'ントダッタノニ、ユウガタニワ'/ジュウデンガ'/カ'ナリ/ヘッテ'/イル'、ソンナ'/コトワアリマセ'ンカ
  context: 最近、朝は100%だったのに、夕方には充電がかなり減っている。そんなことはありませんか。
- seg 011 方 / engine: アプリゴトノ'/ショオサイニワ'、ガメンジョオ'、バックグラ'ウンド、ナ'ド、_ツカワレ'カタノ/テガ'カリガ/ヒョオジ'/サレマ'_ス、タンマツヤ'/ジョオキョオニヨッテ'、ケ'ンガイヤ/テエシ'ンゴオ、ツウチナ'ドガ/ヒョオジ'/サレル'/バアイモ'/アリマ'_ス
  context: アプリごとの詳細には、「画面上」「バックグラウンド」など、使われ方の手がかりが表示されます。端末や状況によって、圏外や低信号、通知などが表示される場合もあります。
- seg 011 上 / engine: アプリゴトノ'/ショオサイニワ'、ガメンジョオ'、バックグラ'ウンド、ナ'ド、_ツカワレ'カタノ/テガ'カリガ/ヒョオジ'/サレマ'_ス、タンマツヤ'/ジョオキョオニヨッテ'、ケ'ンガイヤ/テエシ'ンゴオ、ツウチナ'ドガ/ヒョオジ'/サレル'/バアイモ'/アリマ'_ス
  context: アプリごとの詳細には、「画面上」「バックグラウンド」など、使われ方の手がかりが表示されます。端末や状況によって、圏外や低信号、通知などが表示される場合もあります。
- seg 012 開く/開ける / engine: ガメンジョオ'、ガ'/タケ'レバ、ア'プリオ/ヒラ'イテ/ガメンニ'/ヒョオジ'/_シテ'/イタ'/ジカンガ'/ナガ'カッタ/カノオセエガ'/アリマ'_ス、バックグラ'ウンド、ワ'、ガメンニ'/ヒョオジ'/_シテ'/イナイ'/アイダノ'/ショ'リナドガ/ツズイテ'/イタ'/カノオセエオ'/シメシマ'_ス
  context: 「画面上」が長ければ、アプリを開いて画面に表示していた時間が長かった可能性があります。「バックグラウンド」は、画面に表示していない間の処理などが続いていた可能性を示します。
- seg 012 上 / engine: ガメンジョオ'、ガ'/タケ'レバ、ア'プリオ/ヒラ'イテ/ガメンニ'/ヒョオジ'/_シテ'/イタ'/ジカンガ'/ナガ'カッタ/カノオセエガ'/アリマ'_ス、バックグラ'ウンド、ワ'、ガメンニ'/ヒョオジ'/_シテ'/イナイ'/アイダノ'/ショ'リナドガ/ツズイテ'/イタ'/カノオセエオ'/シメシマ'_ス
  context: 「画面上」が長ければ、アプリを開いて画面に表示していた時間が長かった可能性があります。「バックグラウンド」は、画面に表示していない間の処理などが続いていた可能性を示します。
- seg 028 方 / engine: マトメデ'_ス、ア'サ/ヒャ_クパアセ'ントカラ/ユウガタニ'/カ'ナリ/ヘッタ'/ト'キワ、マ'ズ/サンカ'ショオ/カクニン'/シマ'_ス
  context: まとめです。朝100%から夕方にかなり減ったときは、まず3か所を確認します。

## contextual_pronunciation_audio_gate

辞書の読みが登録済みでも、文脈ごとの実音声audio_queryを別ゲートで確認する。
- result: PASS
- 本物 regression segments: 0
- 本物？ direct query: PASS
- e-Tax direct query: REVIEW

## Summary

- result: REVIEW
- approved matches: 13
- human-approved context items: 0
- review items: 6
- dictionary mutation: none
