# Short001 pronunciation QA v3

- engine：VOICEVOX
- speaker：剣崎雌雄 / ノーマル
- speedScale：1.00
- intonationScale：1.00
- pitchScale：0.00
- script changed segment count：1
- audio regenerated segment count：1
- full audio regeneration：0
- human listening gate：REVIEW

実UI依存の文言を一般化。segment 03のみVOICEVOXを差し替え、他segmentは既存WAVを再利用。

| segment | narration | VOICEVOX kana | status |
|---:|---|---|---|
| 1 | チャットジーピーティー、文字入力は大変ですか。 | チャットジイピイティイモジニュウリョクワタイヘンデスカ | reused_existing_segment_wav |
| 2 | 音声モードなら、話しかけて使えます。 | オンセエモオドナラハナシカケテツカエマス | reused_existing_segment_wav |
| 3 | スマホに向かって、短い質問を話しかけてみます。 | スマホニムカッテミジカイシツモンオハナシカケテミマス | regenerated_v3_target_segment |
| 4 | 冷蔵庫に卵とキャベツがあります。何を作れますか。 | レエゾオコニタマゴトキャベツガアリマスナニオツクレマスカ | reused_existing_segment_wav |
| 5 | チャットジーピーティーが、質問に合わせて答え始めます。 | チャットジイピイティイガシツモンニアワセテコタエハジメマス | reused_existing_segment_wav |
| 6 | まずは、話しかけるだけです。 | マズワハナシカケルダケデス | reused_existing_segment_wav |
| 7 | 次は、写真で聞く手順も確認します。 | ツギワシャシンデキクテジュンモカクニンシマス | reused_existing_segment_wav |
| 8 | 困ったときのために、登録しておいてください。 | コマッタトキノタメニトオロクシテオイテクダサイ | reused_existing_segment_wav |

固有名詞・略語・句読点の間・CTAの速さは、人間が聴くまで最終PASSにしない。
