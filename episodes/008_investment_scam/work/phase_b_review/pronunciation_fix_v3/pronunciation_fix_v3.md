# Episode 008 「信用」発音修正 v3

確認日: 2026-09-05  
入力: `output/draft_v2.mp4`  
出力: `output/draft_v3.mp4`

## 対象segment

Episode008の全63 narration segmentをscanし、「信用」を含む3件を抽出した。timestampはv3 audio_timingのsegment範囲。

| segment ID | narration全文 | timestamp |
|---:|---|---|
| 006 | 一つ、広告の有名人を、そのまま信用しない。 | 00:00:22.460–00:00:26.577（約0:26） |
| 011 | 広告の有名人を、そのまま信用しない、です。 | 00:00:41.187–00:00:45.325 |
| 059 | 一つ、広告の有名人を、そのまま信用しない。 | 00:04:57.747–00:05:01.864 |

## 旧設定との差

draft_v2で`accent=2`だけに依存していた旧挙動を廃止し、pitch shapeを含む1つの辞書entryへ統合した。新設定は`/mora_data`後に`pitch_shape: low_high_plateau`を適用するため、VOICEVOXのaccent再計算による後半下降を残さない。

## 新しいmora / pitch pattern

- 読み: `シンヨオ`（シ・ン・ヨ・オ）
- 形: `LOW → HIGH → HIGH → HIGH`
- 高い基準: 文脈ごとのaudio_queryの2モーラ目
- 低い値: 高い基準 - 0.45
- 2モーラ目以降: 同一pitch（QA tolerance 1e-6）
- `信用を`の検証queryでは、後続の`オ`も同じ高さにそろえ、O-O pitch delta = `0.0`

実測例: seg006 `[4.722651, 5.172651, 5.172651, 5.172651]`、seg011 `[4.717762, 5.167762, 5.167762, 5.167762]`、seg059 `[4.722651, 5.172651, 5.172651, 5.172651]`。

## dictionary更新

`config/voicevox_pronunciation.yaml`の`信用`を1件のapproved entryとして更新した。

- `reading: シンヨオ`
- `pitch_shape: low_high_plateau`
- `pitch_high_anchor_mora: 2`
- `pitch_low_delta: -0.45`
- `pitch_equalize_following_same_mora: true`
- provenance: `Episode008 human review / 2026-09-05 / attached VOICEVOX manual tuning`

検証用の`信用しない。`・`信用する。`・`信用を確認する。` queryは `context_queries.json` に保存した。

## 再生成と再利用

- regenerated: **3**（006 / 011 / 059）
- reused: **60**（その他のsegment。0570-050588のseg055もv2音声を維持）
- v2の字幕SRT/ASS、今だけ、188、0570-050588字幕、CTA、Visual Gate v5は変更していない。

## QA

- `approved_pitch_shape_match`: **PASS**（3/3）
- first mora low / second mora rise / later mora plateau: **PASS**
- `信用を` O-O pitch delta: **0.0**
- video: **PASS**（336.870秒、H.264 1920×1080 30fps、AAC 48kHz mono）
- decode error / black frame / unexpected silence: **0 / 0 / 0**
- visual regression: **0**（Visual Gate v5の18sceneを同一入力）
- subtitle regression: **0**（v2のSRT/ASS/timingとハッシュ一致）
- 既存修正: `今だけ`・`188=イチ、ハチ、ハチ`・`0570-050588`数字表示・CTA全文表示を維持

## 保存先

- preview WAV: `work/phase_b_review/pronunciation_fix_v3/previews/`
- pitch QA: `work/phase_b_review/pronunciation_fix_v3/approved_pitch_shape_match.json`
- context query: `work/phase_b_review/pronunciation_fix_v3/context_queries.json`
- v3 audio query: `work/draft_v3/voicevox_query_audit.json`
- 信用3件のquery抜粋: `work/phase_b_review/pronunciation_fix_v3/credit_audio_queries.json`
- v3 video: `output/draft_v3.mp4`
- representative frames: `work/qa_frames_draft_v3/`

人間が聞くtimestamp: **00:00:26 / 00:00:41–00:00:45 / 00:04:58–00:05:02**。機械QAはPASSだが、最終承認は人間試聴後に行う。
