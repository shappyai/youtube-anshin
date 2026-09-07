# Episode 009 Phase B summary

確認日: 2026-09-05

## Gate

- Visual Gate: v2 / 人間承認済み
- 対象scene: 19
- Phase B status: `draft_v1_waiting_human`
- 次の停止位置: draft_v1全編視聴・発音・シニア向け視認性の人間確認

## Fact Check

- FAIL: 0
- REVIEW: 0
- 根拠: `fact_check.md` の Phase B final gate。主要事実はMicrosoft公式情報と突合済み。

## VOICEVOX

- 話者: VOICEVOX「剣崎雌雄」/ ノーマル
- 設定: speedScale 1.00 / intonationScale 1.00 / pitchScale 0.00
- narration: 52 segment
- generated: 52
- reused: 0
- narration総尺: 289.357秒（pause込み）
- 音声: `audio/voicevox_kenzaki/narration_kenzaki_auto.wav`

### pronunciation review

必須11語のaudio_queryと試聴用WAVを作成した。`pronunciation_preflight.md` の機械判定は、承認済み補正17件、文脈依存の人間確認9件、エンジンエラー0件。辞書の自動変更は行っていない。

- `24H2`: にじゅうよん、エイチ、ツー
- `25H2`: にじゅうご、エイチ、ツー
- `26H1`: にじゅうろく、エイチ、ワン
- その他の試聴対象: Windows 11 / Windows / Microsoft / Home / Pro / Windows Update / 10月13日 / 2026年
- 試聴用音声: `work/phase_b_review/pronunciation/pronunciation_review_all.wav`

## Subtitles / timeline

- subtitle cue: 59
- narration segmentを意味単位で分割したsegment: 7
- minimum subtitle font: 72px
- `font_below_56`: 0
- `overflow`: 0
- `3_line`: 0
- `protected_term_split`: 0
- `tts_reading_leakage`: 0
- 出力: `captions.srt` / `captions.ass`

## CTA / draft

- CTA profile: `channel_common_cta`
- CTA visual: 15.000秒
- CTA audio: 11.563秒 + 3.437秒の余韻
- CTA全文表示: PASS
- draft: `output/draft_v1.mp4`
- draft尺: 304.36秒
- video: H.264 / 1920x1080 / 30fps
- audio: AAC / 48kHz

## QA

- decode error: 0
- black frame: 0
- unexpected silence: 0
- scene count: 19
- Visual Gate v2 regression: 0
- official UI integrity: PASS
- privacy: PASS
- draft QA: PASS
- report: `work/draft_v1_qa.md`

## Representative frames

指定された17scene + CTAを `work/qa_frames_draft_v1/` に抽出し、contact sheetを作成した。

- contact sheet: `work/qa_frames_draft_v1/contact_sheet.png`
- frame report: `work/qa_frames_draft_v1.json`

## 人間が確認するtimestamp

以下はdraft中央付近の確認目安。全編視聴を優先し、必要な箇所を前後10秒程度戻して確認する。

|対象|目安|
|---|---:|
|SCENE-001|00:10.540|
|SCENE-002|00:26.342|
|SCENE-003|00:49.798|
|SCENE-004|01:13.968|
|SCENE-006|01:39.187|
|SCENE-007|01:49.458|
|SCENE-008|01:57.798|
|SCENE-009|02:07.706|
|SCENE-010|02:21.031|
|SCENE-011|02:39.904|
|SCENE-012|03:08.302|
|SCENE-013|03:33.411|
|SCENE-015|04:07.842|
|SCENE-017|04:31.709|
|SCENE-018|04:39.746|
|SCENE-019|04:47.049|
|CTA|04:56.857|

### 特に確認する点

- SCENE-006: 「設定 → システム → バージョン情報」と公式画面の対応。
- SCENE-007: 「Windowsの仕様 → バージョン」と、`24H2 / 25H2` の例示レイヤーの区別。公式画面内の「デバイスの仕様」がテレビ表示でも読めるか。
- SCENE-009: 英語の `Check for updates` と日本語補助「更新プログラムのチェック」の対応。
- 24H2 / 25H2 / 26H1の読み分け、設定手順の速度、字幕の自然さ。
- ImageGen nativeのSCENE-001 / 015 / 019の文字と縮小時可読性。
- CTA右側reserved領域に本文や装飾が侵入していないこと。

## Senior readability

`REVIEW`。機械的な字幕・レイアウト・コントラスト検査はPASSだが、65歳以上を想定した実際のテレビ／YouTube縮小表示での全編視聴は未完了。人間確認後にPASSまたは修正内容を記録する。

## 未実施

- final/final.mp4
- thumbnail
- publish dry-run / OAuth / YouTube upload
- schedule / public
- End Screen実設定

Episode 009 draft_v1完成。人間の全編視聴待ち
