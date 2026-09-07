# Episode 011 Final QA

確認日：2026-09-06  
対象：`output/final.mp4`  
判定：**PASS**

## Final artifact

- source: `output/draft_v2.mp4`
- method: copy-only、再エンコードなし
- byte-identical: **PASS**
- SHA-256: `45AB01EC1FF4F807FFF4ED7F42436FAFD2D00A24FD087BAA7436AF371C78AAB4`
- size: `21,501,533 bytes`
- duration: `251.800 seconds`（expected `251.795 seconds`）
- video: H.264 High / `1920×1080` / `30fps`
- audio: AAC / `48kHz` / mono

## Required gates

| QA項目 | 結果 | 根拠 |
|---|---|---|
| decode error | PASS | vendor ffmpegでfinal.mp4をdecode、エラー0 |
| black frame | PASS | blackdetect該当区間0 |
| unexpected silence | PASS | narration WAVに想定外の長時間無音0。終端はCTA余韻 |
| av sync | PASS | 実測音声タイムライン・字幕・CTAとfinalの尺が一致 |
| subtitle | PASS | 39 cue、target72px、minimum56px以上、overflow0、3-line0、読み仮名漏出0 |
| subtitle balance | PASS | 既知のbalance WARN 8件は文字サイズを下げずに記録。blockingな指摘なし |
| fact boundary | PASS | 2026-09-06に一次情報を再確認。fact_error_count=0、重大な未確認事項0 |
| privacy | PASS | 個人情報・テストアカウント情報の流出0 |
| phone numbers | PASS | `0120-95-0178`、`#9110`、`110`、音声案内`5番`の表示・読み上げを確認 |
| micro story | PASS | problem_scene=4.885秒、first_safe_action=5.005秒、official_answer=8.389秒 |
| midroll CTA | PASS | 1回、68.822〜75.518秒、音声6.496秒、上限7秒以内、疑似subscribe UI0 |
| end CTA | PASS | Episode010実使用registration_conversion_v1とcanonical text・音声を照合。重複0 |
| SCENE-018 native text | PASS | exact text一致、生成2回（retry1）、post overlay0、pil_overlay fallback0 |
| scene quality | PASS | 19/19 OK、scene quality WARN0 |
| AI disclosure metadata | PASS | `contains_synthetic_media=false`を明示。非写実的概念画の既存方針に沿い、API verify対象として保持 |

## Viewer-facing scan

- 対象：Episode004 / Episode008 / Episode010 / Episode011の内部ID、タイトル、ナレーション、字幕、scene画像、CTA、概要欄、chapters。
- viewer-facing internal episode ID：`0`
- viewer-facing brand promise「怖がらせる前に、確認する。」：`0`
- CTA・End Screen候補は視聴者向けの内部IDを表示せず、YouTube Studio側の設定に限定する。

## Registration conversion v2

- story_intro：PASS
- reason_to_return_cta：PASS
- midroll_subscribe_cta：PASS（1回、6.496秒）
- comparison_episode：Episode010
- comparison_type：テーマ差を明記した準実験

## Thumbnail

- selected: `assets/thumbnail/thumbnail.png`
- source: `assets/thumbnail/thumbnail_source.png`
- 1280×720 / PNG / `1,129,358 bytes`
- clipping0 / text_error0 / face_obstruction0 / watermark0 / viewer-facing internal episode ID0
- 25%縮小確認：PASS
- 詳細：`work/thumbnail_review/thumbnail_qa.md`

## Chapter and publish boundary

- final実測タイムラインに基づくchaptersを`publish.json`へ反映。
- 詳細：`work/final_chapters_v1.md`
- titleはcanonical selected titleを維持。
- descriptionは公式根拠URL・VOICEVOXクレジット・更新可能性の注記を含む。
- privacyはprivate、予約日時は2026-09-11 19:00 JST（`2026-09-11T10:00:00Z`）。即時publicは不可。

## Upload guard

- 既存のYouTube video ID：なし
- upload attempt record：なし
- final SHA記録：上記のとおり
- 二重upload防止：publish scriptの既存ID・未解決attempt検出を通過
- End Screen：関連動画候補はEpisode004。関連動画とチャンネル登録要素はYouTube Studioで人間が設定する。動画側の自動設定は行わない。

機械QA原記録：`work/final_qa.json`  
サムネイルQA：`work/thumbnail_review/thumbnail_qa.json`
