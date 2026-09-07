# Episode 011 STATE

更新日：2026-09-06

## Current state

- Episode: 011
- Topic: マイナ保険証を口実にした自動音声・電話詐欺
- Phase: C
- Status: `finalized`
- human_approved: true
- approved_draft: draft_v2
- senior_readability: PASS
- publication_state: SCHEDULED_PRIVATE_END_SCREEN_PENDING
- Selected title: `【マイナ保険証】「1番を押して」の電話、本物？まず確認したい3つ`
- Scene / narration / subtitle scale: 19 scenes / 39 narration segments / 39 subtitle cues
- Last completed: Visual Gate `APPROVED_WITH_2_FIXES` → SCENE-003修正 → Episode010実使用CTA照合 → SCENE-018 ImageGen-native修正 → segment 039修正 → VOICEVOX差し替え → 字幕 → draft_v2 → 機械QA → draft代表フレームcontact sheet → draft_v2全編人間承認 → thumbnail確定 → final copy-only → Final QA
- Stop condition: YouTube予約公開完了。残件はYouTube StudioのEnd Screen人間設定のみ。即時public化は行わない

## Gate result

- Fact FAIL: 0
- Fact REVIEW: 0
- Privacy FAIL: 0
- Template leakage: 0
- Tiny text: 0
- Overflow: 0
- Scene quality: 19/19 OK、WARN 0、FAIL 0
- Visual Gate: `APPROVED_WITH_2_FIXES`
- SCENE-003 fix: PASS。`assets/official/mhlw_warning_core_v1.png`へ核心1メッセージを整理し、電話・SMSで直接利用登録を求めない旨を大きく表示
- Official source legibility: PASS候補。核心文は64〜80px以上、出典は48px以上。人間の全編視聴で最終確認
- Subtitle safe area: PASS
- problem_scene: 4.885秒（segment 001実測）
- first_safe_action: 5.005秒開始（segment 002実測）
- official_answer: 8.389秒開始（segment 003実測）
- official source scene: 25.485秒開始（SCENE-003）
- three_actions_start: 19.461秒開始（segment 005実測）
- micro_story: PASS（視聴者を主人公にし、架空人物の体験談なし）
- Midroll CTA: 1回。68.822秒開始、音声6.496秒、75.518秒に本編へ復帰。上限7秒をPASS、疑似subscribe UIなし
- End CTA: Episode010 draft_v1実使用のregistration_conversion_v1を画面・音声・canonical textの3点で再利用。照合PASS
- Human full-watch: `APPROVED`（2026-09-06）
- Senior readability: `PASS`
- Final: `output/final.mp4`（draft_v2からcopy-only、byte-identical、SHA256 `45AB01EC1FF4F807FFF4ED7F42436FAFD2D00A24FD087BAA7436AF371C78AAB4`）
- Final QA: `PASS`（`output/review/final_qa.md`）
- Thumbnail: `HUMAN_SELECTED`（ユーザー提供画像を内容変更なしで1280×720へ正規化、QA PASS）
- Final fact check: 2026-09-06一次情報再確認、fact_error_count 0、privacy_error_count 0
- AI disclosure: `contains_synthetic_media=false`を明示。非写実的概念画の既存方針に沿い、API verify対象
- VOICEVOX pronunciation: PASS（39/39、REVIEW 0）
- Subtitle preflight: WARN（FAIL 0、WARN 8。文字サイズ縮小ではなく分割済み。人間確認対象）
- Draft QA: PASS。H.264 1920x1080 30fps / AAC 48kHz mono / 約251.800秒
- SCENE-018 ImageGen-native: PASS。生成2回（retry 1）、指定主文・補助文のexact text QA PASS、後付け文字0、pil_overlay fallback 0
- Viewer-facing brand promise scan: PASS。`怖がらせる前に、確認する。` の表示・ナレーション・字幕・CTA・概要欄・チャプター・現行scene画像への残存0。内部metadataのブランド定義は保持
- Story resolution: PASS。`迷ったら、その場で決めない` → `いったん止まって、公式から確認` → segment 039で確認後に手続きを進める流れを維持

## Created for Phase B

- `audio/voicevox_kenzaki/`（39 segment WAV、連結 narration 236.795秒。segment 039再生成、他38件再利用）
- `audio/voicevox_kenzaki/cta_registration_conversion_v1.wav`（Episode010実使用CTA、11.456秒）
- `captions.srt`
- `captions.ass`
- `output/draft_v1.mp4`
- `work/cta_registration_conversion_v1.json`
- `work/cta_registration_conversion_v1.png`
- `work/draft_v1_measurements.md`
- `work/phone_number_qa_v1.md`
- `work/phase_b_build_result.json`
- `work/draft_v1_qa.md`
- `work/qa_frames_draft_v1.json`
- `work/visual_review/draft_v1_contact_sheet_v2.png`
- `output/draft_v2.mp4`（SHA256: `45AB01EC1FF4F807FFF4ED7F42436FAFD2D00A24FD087BAA7436AF371C78AAB4`、probe 251.800秒）
- `work/visual_review/draft_v2_contact_sheet.png`
- `work/draft_v2_qa.md` / `work/draft_v2_qa.json`
- `work/phase_b_v2_build_result.json`
- `work/visual_review/scene_018_native_text_qa_v1.md`
- `work/visual_review/draft_v2_change_log.md`
- `work/visual_review/draft_v2_visual_qa_v1.md`
- `work/visual_review/brand_promise_scan_v2.md`
- `work/production_preflight_v2.md`

## Visual Gate fixes and source assets

- `assets/official/mhlw_warning_core_v1.png`：SCENE-003の可読性修正版
- `work/visual_review/scene_contact_sheet_v2.png`：修正後のscene contact sheet
- `work/visual_review/visual_gate_v2.md`：2点修正の記録
- `work/scene_quality_report_v2.md`：19 scenes / OK 19 / WARN 0 / FAIL 0
- Episode010実使用CTAのSHA・canonical textを`work/cta_registration_conversion_v1.json`に保持

## Registered CTA text

`スマホやパソコンの「これ、どうすればいい？」を、公式情報で分かりやすく確認しています。次に困ったときのために、チャンネル登録しておいてください。`

表示：`次に困ったときのために。` / `チャンネル登録しておいてください。`

## 登録者獲得実験 v2

- `registration_conversion_v2`
- story_intro：true
- reason_to_return_cta：true
- midroll_subscribe_cta：true（SCENE-019 / segment 013 / 実測6.496秒）
- comparison：Episode010。テーマ差があるため準実験として扱い、登録転換率とCTA前後のRetentionを併記する
- Episode010との差分：011のみ、最初の価値提供後に中盤CTAを1回追加。テーマ、3つの確認、公式情報、可読性は変更しない

## Human review checklist

- draft_v2を冒頭から最後まで視聴
- SCENE-003の核心文と出典の読みやすさを確認
- `0120-95-0178`、`#9110`、`110`、`5番`の表示と読み上げを確認
- VOICEVOXの固有名詞・略語・数字の発音を確認
- 中盤CTAが6.496秒以内で、前後の流れを妨げないことを確認
- Episode010と同じ終了CTAであること、右側reserved領域と疑似subscribe要素なしを確認
- 非写実的なAI概念画2sceneのAI disclosure要否を確認
- SCENE-018のImageGen-native文字が「迷ったら、／その場で決めない」「いったん止まって、／公式から確認」と読めることを確認
- `怖がらせる前に、確認する。` が視聴者向け音声・字幕・画面・概要欄・チャプターに出ていないことを確認

## Phase C finalized

- thumbnail generationは行わず、ユーザー提供サムネイルを採用
- `output/final.mp4`を確定
- YouTube scheduled uploadは`2026-09-11 19:00 JST`（API: `2026-09-11T10:00:00Z`）で完了。video ID: `kSln-2eJ6CU`
- upload_status: `uploaded_scheduled`
- YouTube StudioのEnd Screen（関連動画Episode004・チャンネル登録）は人間設定が必要

## Final records

- `work/human_review.json`
- `work/final_chapters_v1.md`
- `work/thumbnail_review/thumbnail_qa.md`
- `work/thumbnail_review/thumbnail_qa.json`
- `output/review/final_qa.md`
- `output/review/final_qa.json`
- `work/youtube_publish/upload_attempt.json`（verification PASS）
- `work/youtube_publish/ai_disclosure_attempt.json`（status-only、reupload false、verification PASS）

## YouTube publication
- youtube_upload: uploaded_scheduled
- youtube_video_id: kSln-2eJ6CU
- youtube_url: https://youtu.be/kSln-2eJ6CU
- youtube_privacy: private
- youtube_scheduled_at: 2026-09-11 19:00:00 JST
- youtube_scheduled_at_api: 2026-09-11T10:00:00Z
- thumbnail_uploaded: true
- uploaded_at: 2026-09-05T23:04:29Z
- youtube_channel_id: UCgVRceTJYO5KOrPX4w2jXZw
- youtube_ai_disclosure: false
- youtube_ai_disclosure_updated_at: 2026-09-05T23:05:48Z
- youtube_ai_disclosure_verified: true
- youtube_ai_disclosure_verification: videos.update response; videos.list omitted containsSyntheticMedia
