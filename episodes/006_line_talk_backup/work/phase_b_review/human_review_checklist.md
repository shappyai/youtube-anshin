# Episode 006 仮レンダー 人間レビュー用チェックリスト

- draft: `output/draft_v1.mp4`（1920×1080・30fps・H.264・AAC 48kHz・全長 約6分48秒）
- 最終scene contact sheet: `work/phase_b_review/final_scene_contact_sheet.png`
- 発音5件の実音声QA: `work/phase_b_review/pronunciation_real_audio_qa.md`／試聴用WAV: `work/phase_b_review/audio/pronunciation_5seg_review.wav`
- readability採用一覧: `work/phase_b_review/readability_adoption.md`

## 確認ポイント（scene番号＋おおよその時刻）

| 時刻 | Scene | 確認内容 |
|---|---|---|
| 0:00 | SCENE-001 | 冒頭（GPT画像・見出し）。間延びしていないか |
| 0:19 | SCENE-002 | 今日確認する3つの一覧 |
| 1:45 | SCENE-006 | readability拡大版（バックアップ・引き継ぎ手順） |
| 2:03 | SCENE-007 | readability拡大版（今すぐバックアップ） |
| 2:28 | SCENE-010 | メイン端末だけ・文字だけ（3行表示のまま・崩れなしの確認） |
| 2:44 | SCENE-011 | readability拡大版（自動バックアップ） |
| 3:29 | SCENE-014 | readability拡大版（iCloud Drive） |
| 3:48 | SCENE-016 | readability拡大版（PIN）※実PIN非表示 |
| 4:55 | SCENE-020 | readability拡大版（同じOSのみ） |
| 5:24 | SCENE-022 | readability拡大版（写真・動画は対象外） |
| 5:58 | SCENE-024 | まとめ（冒頭と同一3項目） |
| 6:28 | SCENE-025 | クロージング（GPT画像） |
| 6:35〜6:48 | CTA | 共通CTA（音声あり） |

## 発音5件の実音声確認位置

| seg | 動画内 | 読み（query・実音声） |
|---|---:|---|
| 018 | 1:37〜1:44 | 今日 → きょう |
| 020 | 1:51〜1:57 | 開いて→ひらいて／開きます→ひらきます |
| 037 | 3:29〜3:36 | 方 → ほう |
| 047 | 4:30〜4:34 | 誕生日 → たんじょうび |
| 062 | 5:58〜6:02 | 今日 → きょう |

試聴用WAV（5件連結・0.6秒間隔）で5件をまとめて確認できます。

## 自動QA結果

- `phase2_qa`（draft_v1）: **PASS**（fail 0 / warn 0）。黒フレーム0・字幕安全幅0・scene欠落0・音声欠落0・長無音0・アスペクト正常。
- preflight: episode.json/sources/scenes/official assets/subtitles = PASS。pronunciation = REVIEW 5件（人間承認済みのfalse positive。本編実音声で確認済み）。
- GPT画像5枚は再来生なし・重複SHAなし（前工程から不変）。
