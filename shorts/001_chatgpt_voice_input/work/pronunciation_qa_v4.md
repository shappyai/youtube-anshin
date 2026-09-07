# Short001 pronunciation QA v4

- engine：VOICEVOX
- speaker：剣崎雌雄 / ノーマル
- speedScale：1.00
- intonationScale：1.00
- pitchScale：0.00
- audio regenerated segment count：3
- full audio regeneration：0
- audio policy：変更segmentだけv4 WAVを生成し、残りは既存WAVを再利用。
- human listening gate：REVIEW（Draft Gateで最終聴取）

## ChatGPT pronunciation

- 表示：`ChatGPT`。VOICEVOX入力：`チャットジーピーティー`。
- 実audio_query/mora_dataを確認し、「チャ・ッ・ト」の`ト`を3モーラ目のaccent核に設定（accent=3）。
- `config/voicevox_pronunciation.yaml`へ`human_approved: true` / `global: true`で登録し、Short001の全出現segmentへ適用。
- 修正版audio生成後のquery観測：

| segment | accent | ト pitch | status |
|---:|---:|---:|---|
| 1 | 3 | 5.0219 | PASS |
| 5 | 3 | 5.0285 | PASS |

- `work/chatgpt_pronunciation_v4.json`に観測値と対象segmentを保存。

| segment | narration | VOICEVOX kana | status |
|---:|---|---|---|
| 1 | チャットジーピーティー、文字入力は大変ですか。 | チャットジイピイティイモジニュウリョクワタイヘンデスカ | regenerated_v4_target_segment |
| 2 | 音声モードなら、話しかけて使えます。 | オンセエモオドナラハナシカケテツカエマス | reused_existing_segment_wav |
| 3 | スマホに向かって、短い質問を話しかけてみます。 | スマホニムカッテミジカイシツモンオハナシカケテミマス | reused_v3_segment_wav |
| 4 | 冷蔵庫に卵とキャベツがあります。何を作れますか。 | レエゾオコニタマゴトキャベツガアリマスナニオツクレマスカ | reused_existing_segment_wav |
| 5 | チャットジーピーティーが、質問に合わせて答え始めます。 | チャットジイピイティイガシツモンニアワセテコタエハジメマス | regenerated_v4_target_segment |
| 6 | まずは、話しかけるだけです。 | マズワハナシカケルダケデス | reused_existing_segment_wav |
| 7 | 次は、写真で聞く手順も確認します。 | ツギワシャシンデキクテジュンモカクニンシマス | reused_existing_segment_wav |
| 8 | 次に困ったときのために、このチャンネルを登録しておいてください。 | ツギニコマッタトキノタメニコノチャンネルオトオロクシテオイテクダサイ | regenerated_v4_target_segment |

固有名詞・CTAの速さ・句読点の間は、人間がDraft v4を聴くまで最終PASSにしない。
