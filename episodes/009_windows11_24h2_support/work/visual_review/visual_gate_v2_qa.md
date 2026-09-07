# Episode 009 Visual Gate v2 QA

確認日: 2026-09-05

## 変更範囲

- 変更対象: SCENE-006 / SCENE-007 / SCENE-009のみ
- 非対象: SCENE-001〜005、SCENE-008、SCENE-010〜019、ImageGen 001 / 015 / 019、共通背景、台本、音声、字幕
- 再利用: `adult_digital_soft_image_bg`、Microsoft公式のPII-free素材

## 対象sceneの判定

|Scene|変更内容|判定|
|---|---|---|
|SCENE-006|左に「設定→システム→バージョン情報」のstep、右に拡大公式focus crop、highlight 1箇所|official_ui_legibility PASS / action_clarity PASS / visual_balance PASS / tiny_text 0|
|SCENE-007|公式「デバイスの仕様」cropと、UI外の「バージョン（例）24H2 / 25H2」説明欄|version_field_legibility PASS / privacy PASS / visual_balance PASS / tiny_text 0|
|SCENE-009|左に「設定→Windows Update」のstep、右に日本語補助ラベルと公式button crop、highlight 1箇所|windows_update_legibility PASS / action_clarity PASS / visual_balance PASS / tiny_text 0|

## 全体QA

- 19scene contact sheet v2: 作成済み
- before / after比較: 作成済み（左=v1、右=v2）
- scene quality report v2: 19 OK / 0 WARN / 0 FAIL
- `blank_white_slide`: 0
- `tiny_text`: 0
- `overflow`: 0
- `visual_axis_alignment`: PASS
- `stacked_panel_alignment`: PASS
- `subtitle_safe_area`: PASS（下部180px）
- `background_consistency`: PASS
- 公式UIのAI再現: なし

## Privacy

- canonicalな`episode.json`、`scene_plan.json`、`media_manifest.csv`に`_source_tmp`の参照はない。
- SCENE-006 / 007で採用したfocus cropは、device name、Device ID、Product ID、serial、個人名を含まない。
- 個人情報を含む一時原画 `assets/official/_source_tmp/devicenameandmodel.png` は、canonical参照0件を確認後、2026-09-05に削除済み。

## Human Gate

- 元画像サイズで、SCENE-006の「バージョン情報」、SCENE-007の「バージョン（例）」、SCENE-009の「更新プログラムのチェック」が一目で読めるか。
- SCENE-007の`24H2 / 25H2`が実UIの改変ではなく、UI外の説明用例示として理解できるか。
- 英語の`Check for updates`と日本語補助ラベルの意味が一致しているか。
- 006→007→009の「開く→見る→更新を確認」の流れが自然か。

## 停止位置

Episode 009 Visual Gate v2完成。SCENE-006 / 007 / 009の人間確認待ち。VOICEVOX、subtitles、draft、thumbnail、uploadへは進まない。
