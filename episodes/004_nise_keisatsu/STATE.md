# Episode 004 State

- status: scheduled
- human_approved: true
- finalized: true
- approved_draft: `output/draft_v3.mp4`
- final: `output/final.mp4`
- finalization_method: copy-only; no re-encode
- finalized_at: 2026-08-31
- youtube_upload: completed
- thumbnail: uploaded（人間承認済み `final/thumbnail.png` を標準パス `assets/thumbnail/thumbnail.png` へ配置・thumbnails.set成功）
- publish: metadata_verified

## 最終QA（2026-08-31）

- final SHA256: `2022F1BD549B60CAA6664BFDA22F92789DDA781FD35C6F3589E7155EACBFD6FE`
- draft_v3 SHA256: `2022F1BD549B60CAA6664BFDA22F92789DDA781FD35C6F3589E7155EACBFD6FE`（完全一致）
- duration: 401.8s（ナレーション391.8s＋CTA 10s）
- H.264 1920x1080 30fps / AAC 48kHz
- decode error: 0 / black frame: 0 / 無音異常: 0
- scenes: 18 / subtitle cues: 72 / narration segments: 72
- contains_synthetic_media: true / made_for_kids: false

## Production metrics

- start_time: 2026-08-31T20:59:47+09:00
- phase_a_completed: 2026-08-31
- phase_b_front_half_completed: 2026-08-31
- gpt_image_count: 7
- pronunciation_review_count: 10（unresolved 0）
- draft_versions: [draft_v1.mp4, draft_v2.mp4, draft_v3.mp4]
- human_correction_rounds: 2（round1: draft_v1→v2 SCENE-013可読性 / round2: draft_v2→v3 全編レビュー反映）
- human_correction_count: 0（finalize回）
- final_version: final.mp4
- finalize_time: 2026-08-31T22:30:00+09:00
- youtube_upload_completed_at: 2026-08-31T14:08:22Z
- youtube_thumbnail_status: uploaded
- youtube_metadata_verify_status: verified
- total_production_minutes: null（人間が補足）

2026-09-04 19:00 JST（2026-09-04T10:00:00Z）に自動公開予定（scheduled private）。

## YouTube publication
- youtube_video_id: rHLCF8WcOkU
- youtube_url: https://youtu.be/rHLCF8WcOkU
- youtube_privacy: private
- youtube_scheduled_at: 2026-09-04 19:00:00 JST
- youtube_scheduled_at_api: 2026-09-04T10:00:00Z
- thumbnail_uploaded: true
- uploaded_at: 2026-08-31T14:08:22Z
- youtube_channel_id: UCgVRceTJYO5KOrPX4w2jXZw
- youtube_publish_at_jst: 2026-09-04 19:00
- youtube_publish_at_utc: 2026-09-04T10:00:00Z
- youtube_ai_disclosure: true
- youtube_ai_disclosure_verified: true（videos.insertのstatusにcontainsSyntheticMedia=true設定。videos.listではAPI仕様上省略されるため、YouTube Studioで最終確認を推奨）
- made_for_kids: false
- metadata_verify_note: videos.list(part=snippet,status)でtitle/description/tags/categoryId/defaultLanguage/privacyStatus/publishAt/thumbnailsを確認済み
