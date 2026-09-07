# Episode 009 Phase B draft_v2 summary

確認日: 2026-09-05

## Scope

- draft_v1は上書きせず保持。
- 今回は発音・VOICEVOXだけを局所修正。字幕表示、Visual Gate v2、scene PNG、CTA画面・CTA音声は変更なし。
- 停止位置はdraft_v2とQAまで。final、thumbnail、upload、schedule/public、End Screen設定は未着手。

## 1. 方 segment / reading

| segment | 用法 | 読み |
|---:|---|---|
| 001 | Windows 11を使っている方（人） | かた |
| 006 | 考え方（方向・方法） | ほう |
| 011 | HomeやProの方（人・利用者） | かた |
| 038 | 24H2の方（比較・該当ケース） | ほう |

`方` のglobal辞書登録はなし。segment 001 / 006 / 011 / 038にcontext overrideを適用。

## 2. Windows occurrences / IDs

16 occurrences: segment 001, 002, 004, 005, 008, 009, 014, 020, 022, 023, 025, 037, 039, 047, 049, 050。

### Approved dictionary

- surface: `Windows`
- VOICEVOX reading: `ウィンドオズ`（自然な「ウィンドウズ」のエンジン用表記）
- accent: `5`（語末のズをピーク）
- status: approved / 2026-09-05 human review

## 3. Update occurrences / IDs

7 occurrences: segment 005, 022, 023, 037, 039, 047, 050。

### Approved dictionary

- surface: `Update`
- VOICEVOX reading: `アップデエト`（自然な「アップデート」のエンジン用表記）
- accent: `6`（語末のトをピーク）
- status: approved / 2026-09-05 human review

## 4. ID occurrences / IDs

1 occurrence: segment 019。

### Approved dictionary

- surface: `ID`
- VOICEVOX reading: `アイディイ`（エンジン上はア・イ・ディ・イ。表示字幕は `ID` のまま）
- accent: `3`（ディをピーク）
- status: approved / 2026-09-05 human review

## 5. Regenerated / reused

- 最終的な発音差分: 20 segments regenerated。
- regenerated IDs: 001, 002, 004, 005, 006, 008, 009, 011, 014, 019, 020, 022, 023, 025, 037, 038, 039, 047, 049, 050。
- 32 segments reused（既存WAVを再利用）。
- `方` の人用 `かた` は001 / 011、方向・比較用 `ほう` は006 / 038として反映。

## 6. Preview assets

`work/phase_b_review/pronunciation_fix_v2/` に以下を保存。

- `kata_context.wav` / `kata_context_audio_query.json`
- `windows_representative.wav` / `windows_representative_audio_query.json`
- `update_representative.wav` / `update_representative_audio_query.json`
- `id_representative.wav` / `id_representative_audio_query.json`
- `windows_update_phrase.wav` / `windows_update_phrase_audio_query.json`
- `pronunciation_fix_v2_all.wav`

## 7. Draft / subtitle / visual

- draft_v2: `output/draft_v2.mp4`
- draft_v2 duration: `304.30s`
- narration duration: `289.304s`（pause込み）
- video: H.264 / 1920x1080 / 30fps
- audio: AAC / 48kHz
- subtitles: 59 cues、minimum 72px、表示文言・改行・TTS leakageは変更なし
- Visual Gate v2: 19scene固定、SCENE-006 / 007 / 009を含むtarget-only回帰0
- CTA: 15.000s（音声11.563s + 余韻3.437s）、変更なし

## 8. QA

- pronunciation QA: PASS（`approved_pronunciation_match`、方 / Windows / Update / IDの全出現を確認）
- video QA: PASS
- decode error: 0
- black frame: 0
- unexpected silence: 0
- official UI regression: 0
- privacy: PASS。`assets/official/_source_tmp/devicenameandmodel.png` は削除済み、採用参照0。
- CTA: PASS
- senior_readability: REVIEW（人間の全編視聴・発音再確認待ち）

## 9. 人間再確認 timestamps（draft_v2）

以下は該当segmentの開始位置。各位置から前後10秒程度を含めて確認する。

|対象|segment|開始|
|---|---:|---:|
|方|001|00:00.000|
|Windows|001|00:00.000|
|方|006|00:27.379|
|Windows|002|00:09.981|
|Windows|004|00:20.995|
|Windows / Update|005|00:24.149|
|方|011|01:02.285|
|Windows|008|00:34.396|
|Windows|009|00:50.504|
|Windows|014|01:16.244|
|ID|019|01:38.695|
|Windows|020|01:44.360|
|Windows / Update|022|01:54.449|
|Windows / Update|023|01:57.401|
|Windows|025|02:03.789|
|Windows / Update|037|03:15.951|
|方|038|03:24.485|
|Windows / Update|039|03:32.376|
|Windows / Update|047|04:20.815|
|Windows|049|04:31.000|
|Windows / Update|050|04:34.699|

Episode 009 draft_v2完成。方 / Windows / Update / ID発音の人間再確認待ち
