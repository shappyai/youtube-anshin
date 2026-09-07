# Episode 005 Phase B前半 preflight

確認日: 2026-09-01（JST）  
対象: `episodes/005_google_photos_delete/`

## 判定

**STOP / 人間レビュー待ち**。Phase B前半の資産確認とレビュー用still生成までを完了した。WAV、実尺字幕、draft/final、thumbnail、YouTube操作には進んでいない。

| Gate | Status | 結果 |
|---|---|---|
| episode schema | PASS | `episode_io.validate_episode` 0件 |
| sources | PASS | 主要根拠URLあり、保存HTML20件 |
| scene/item mapping | PASS | 65 narration segments、25 scene、item count指摘なし |
| GPT image assets | REVIEW | 5/5、原本1672×941保持、review copy 1920×1080、SHA重複0。下180pxは一部視覚要素あり |
| official assets | FAIL | SCENE-022の`restore_from_trash.png`のみ未取得。SCENE-004/006はREVIEW、SCENE-008/012/014はPASS |
| still render | REVIEW | 24/25 sceneを1920×1080へrender。SCENE-022は未取得タイルでcontact sheetへ明示 |
| subtitles | FAIL | 12行が安全幅1800px超過。`subtitle_preflight.md`参照 |
| pronunciation/audio | STOP | 65/65 query確認、設定不一致0。seg046「お使いの方」は「ほう」になり、WAV 0件 |
| privacy | PASS | Androidは自作ダミーのみ。採用公式cropに個人情報・通知・GPSなし |

## 必須レビュー項目

- contact sheet: `scene_contact_sheet.png` / `gpt_image_contact_sheet.png`
- 音声: seg046の「方」を「かた」とするか人間試聴で承認。`右上`は既存辞書適用を確認する。
- Android: SCENE-004の「バックアップが完了しました」、SCENE-006の削除後、SCENE-022の復元画面を専用テストで再取得するか判断。
- 視覚: SCENE-020/025の「確認」改行、字幕12行の安全幅、GPT画像の下180px、公式cropの可読性。

## 次工程へ持ち越すもの

1. human review（contact sheet＋pronunciation）
2. 必要なAndroid再撮影と字幕改行修正
3. WAV生成・実尺字幕・draftは、人間承認後にのみ実施

## Phase B前半残課題処理結果（2026-09-01）

上段は残課題処理前のスナップショットであり、現在の判定は以下を正とする。

| Gate | Status | 現在の結果 |
|---|---|---|
| seg046 pronunciation | REVIEW（人間試聴のみ） | TTS入力は「次は、iPhoneをお使いのかたに、確認しておきたいことがあります。」。字幕表示は「お使いの方」のまま。短いpreview WAVのみ生成し、本編WAVは未生成。 |
| pronunciation preflight | PASS | 65/65 query、未解決 pronunciation REVIEW 0。文脈候補7件は同一話者の読みを機械確認済みで、global dictionaryは変更なし。 |
| subtitles / Japanese linebreak | PASS | 安全幅超過0、字幕preflight FAIL 0 / WARN 0、scene linebreak WARN 0、1文字孤立0。12字幕＋scene 020/025を修正。 |
| Android REVIEW 2用途 | PASS（fallback含む） | SCENE-004はUI文言差→個人情報のないGoogle公式crop、SCENE-006は操作対象が見えない→自作ダミーcaptureの局所crop。残存Android REVIEW 0。 |
| SCENE-022 | PASS（公式fallback） | Android再撮影は行わず、Google公式ヘルプの「コレクション→ゴミ箱→写真を選択→復元」をcrop＋Codex overlayで構成。期間は公式情報だけを使用。 |
| scene render | PASS | 25/25 scene、全て1920×1080。変更scene 004/020/022/025のみ再render、他21sceneはreuse。 |
| visual QA | PASS（WARN専用候補あり） | template leakage 0、visual centroidの機械WARN 0、official asset path/source PASS、narration item count 0。scene_quality_reportのWARN専用候補11件（意図的余白・小文字proxy等）はcontact sheetで一括確認する候補として記録。 |

## 今回の停止位置

seg046 preview試聴と`scene_contact_sheet_v2.png`／公式cropの最終可読性確認だけを人間レビュー対象として残す。本編VOICEVOX、final subtitle timing、video assemble、draft、thumbnail、YouTube操作には進まない。
