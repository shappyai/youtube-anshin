# Pronunciation fix v2

人間レビューに基づくv2発音確認。preview WAVとVOICEVOX audio_queryを保存。

- 本編63セグメント中、再生成は5件（006/011/031/052/059）、draft_v1音声の再利用は58件。
- 0570-050588（seg055）は人間承認済みのdraft_v1音声をそのまま再利用し、再合成していない。

| segment | target | status | effective text | accent summary |
|---:|---|---|---|---|
| 006 | 信用 | regenerated | 一つ、広告の有名人を、そのまま信用しない。 | シンヨオ accent=2 |
| 011 | 信用 | regenerated | 広告の有名人を、そのまま信用しない、です。 | シンヨオ accent=2 |
| 031 | 今だけ | regenerated | 「今だけ」「あなただけ」と、あせらせる言葉が来たら、いったん、止まりましょう。 | イマダケ accent=1 |
| 052 | 188 | regenerated | 消費者ホットラインは、イチ、ハチ、ハチ。 | イチ accent=2 / ハチ accent=2 / ハチ accent=2 |
| 055 | 0570-050588 | reused_from_draft_v1 | ゼロゴーナナゼロの、ゼロゴーゼロゴー、ハチハチ。 |  |
| 059 | 信用 | regenerated | 一つ、広告の有名人を、そのまま信用しない。 | シンヨオ accent=2 |

- 信用: seg 006/011/059すべて シンヨオ / accent=2。
- 今だけ: seg 031のみ イマダケ / accent=1。
- 188: seg 052はEpisode 004承認済みの イチ、ハチ、ハチ をreuse（Episode008では音声を再生成）。
- 0570-050588: seg 055音声はdraft_v1からreuse。

Preview directory: previews/
Audio query report: pronunciation_fix_v2.json
