# Episode 014 pronunciation audit v2

確認日：2026-09-06
エンジン：VOICEVOX / 剣崎雌雄 ノーマル（style_id=21）

## 対象語

| 表示 | TTS入力・辞書 | 確認結果 |
|---|---|---|
| ちいかわ | チイカワ、accent=4（ワ） | PASS。モーラはチ・イ・カ・ワ |
| フリマ | フリマ、accent=3（マ） | PASS。モーラはフ・リ・マ |
| 188 | イチハチハチ（text_replacement） | PASS。表示字幕は188のまま |

## 188の回帰確認

- 既存の標準辞書をEpisode014着手前に確認した時点で、surface=`188`のapproved global entryは未登録だった。
- v1では`spoken_text`を先回りして「いちはちはち」に置き換えていたため、surface=`188`に対する辞書処理を通らなかった。辞書ロードの回帰ではない。
- v2ではcanonicalの表示文字列を188に戻し、標準辞書のapproved `text_replacement`でTTS入力だけを「イチハチハチ」にした。
- 整数読み「ひゃくはちじゅうはち」と、誤った「イチワチワチ」は採用していない。

## 辞書のprovenance

- `config/voicevox_pronunciation.yaml`
- 3項目とも `status: approved`、`human_approved: true`、日付 `2026-09-06`
- 「ちいかわ」「フリマ」はVOICEVOX `audio_query`のモーラ列と語末アクセントを確認。
- 「188」は表示文字と音声入力を分離し、3か所（segment 31 / 32 / 36）で同じ読みを使用。

## ゲート結果

- pronunciation preflight：38/38 query、対象13 matches PASS
- `tts_reading_leakage`：PASS
- 共通回帰ゲート：e-Tax direct queryはEpisode014対象外、`行う`は一般文脈のREVIEW 1件
- 人間の全編確認で、対象語と「行う」の実音声を確認する。

