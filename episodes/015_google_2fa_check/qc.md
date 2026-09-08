# Episode 015 QC — scheduled upload

- 状態: `UPLOADED_SCHEDULED`
- 確認日: 2026-09-08
- approved draft: `output/draft_auto_v4.mp4`
- final: `output/final.mp4`
- finalize方式: copy-only（再encodeなし）
- SHA-256: `7AB436A319D66CC7EF27BA9A936CC6AC15AC0A725EBEFA7818AFC2C7131EDB5D`
- thumbnail: `assets/thumbnail/thumbnail.png`（ChatGPT生成・Human承認済み・YouTube設定済み）
- 実尺: 312.918秒（5分12.918秒、final container probe）。音声timeline/QA基準は313.356秒（5分13.356秒）。
- 映像: 1920×1080 / H.264 / 30fps
- 音声: AAC / 48kHz / mono
- Human Gate 2: APPROVED（映像・音声・字幕）

## 自動QA

- Phase 2 production preflight: PASS
- Final production preflight: PASS（episode.json、sources、scenes、official assets、subtitles、pronunciation、viewer-facing INTERNAL_ONLY）
- Phase 2 QA: PASS（FAIL 0 / WARN 0）
- Final QA: PASS（SHA一致、decode error 0、black frame 0、unexpected silence 0、audio clipping 0）
- Publish preflight dry-run: PASS（final / Human approval / final QA / metadata確認、privacy=PRIVATE、OAuth/API未呼出し）
- OAuth health: PASS（refresh token、YouTube API auth）
- Channel guard: PASS（UCgVRceTJYO5KOrPX4w2jXZw）
- Duplicate guard: PASS（upload前の既存video IDなし、reupload false）
- Scheduled upload/API verify: PASS（video ID、title、description、privacyStatus、publishAt、thumbnail設定）
- VOICEVOX pronunciation preflight: PASS、42/42 query、review 0
- Subtitle preflight: PASS、61 cue、FAIL 0 / WARN 0
- viewer-facing INTERNAL_ONLY文言QA: PASS、検出0
- バックアップコード数字の素材混入: 0（入口・存在確認のみ）
- scene renderer: 12枚生成済み。テンプレート9枚、実Google UI入口3枚。AI生成画像0枚
- scene quality report: `9 OK / 0 WARN / 3 FAIL`。3件は実Google UI入口の `layout_04_text_official` で、gradient背景には差分比較用の画像背景がないため `background comparison unavailable` となる既知の機械判定。SCENE-010はnear-white率72%も検出。Human Gate 2で映像を承認済みだが、機械判定結果は記録として残す。
- v4 contact sheet: `output/review/draft_contact_sheet_v4.png`（動画代表フレーム）
- 音声・字幕専用確認: `work/audio_subtitle_revision_v4.md`（section番号0件、`セキュリティー`・`なにで本人確認`・compound語のaudio_query内breakなし）

## Human Gate 2

Human Gate 2: **APPROVED**（映像・音声・字幕）。

## YouTube publication

- video ID: `f_6347guKso`
- publishAt: `2026-09-08 19:00:00 JST`（`2026-09-08T10:00:00Z`）
- privacyStatus: `private`
- thumbnail: `PASS（thumbnails.set）`
- metadata: `PASS（title・description・channel ID・privacyStatus・publishAt）`
- End Screen: 未設定（YouTube Studioで人間設定）
- 固定コメント: 未投稿（自動化なし・人間作業）

詳細: `output/review/final_qa.md`、`output/review/final_qa.json`、`work/youtube_publish/auth_preflight.json`、`work/youtube_publish/dry_run.json`、`work/youtube_publish/upload_attempt.json`、`work/youtube_publish/youtube_upload_log.md`、`work/phase2_qa.md`、`work/production_preflight_phase2.md`、`work/production_preflight_v4.md`、`work/production_preflight_final.md`、`work/pronunciation_preflight_v4.md`、`work/subtitle_preflight_v4.md`、`work/viewer_facing_internal_brand_promise_v4.md`、`work/viewer_facing_internal_brand_promise_final.md`、`work/cta_preflight_v4.md`、`work/cta_preflight_final.md`、`work/scene_quality_report_v4.md`、`work/audio_subtitle_revision_v4.md`
