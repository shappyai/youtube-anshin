# Episode 010 Phase C QC（Final / scheduled private）

- episode：010_myna_app_registration
- status：SCHEDULED_PRIVATE
- phase：Phase C
- checked：2026-09-06

## Automated and production checks

- [x] episode.json parse and scene definition：20 scenes、41 narration segments、44 subtitle cues
- [x] intro QA：registration_conversion_v1のmicro storyを反映。1 / 6開始はSCENE-004（25.347秒）、最初の実操作はSCENE-005（28.516秒）
- [x] required Phase A documents：brief、research、fact_check、script、shotlist、scene_plan、sources、publish
- [x] registration_conversion_v1 analytics plan：work/analytics_plan.md
- [x] primary-source links：sources.mdに記録
- [x] fact check：Fact error 0、REVIEW 2（FC-019、FC-020は更新・実機依存）
- [x] image generation manifest：3 scenes
- [x] scene render：20 / 20 PASS
- [x] scene quality：FAIL 0、WARN 3
- [x] ImageGen exact-text auto QA：FAIL 0
- [x] privacy QA：PASS
- [x] narration language：VOICEVOX narrationで「方」を避けた
- [x] Visual Gate v2：scene_contact_sheet_v2、intro_v1_v2_comparison、Fact FAIL 0を記録
- [x] Visual Gate v2：2026-09-05に人間承認
- [x] VOICEVOX：剣崎雌雄 / ノーマル、41 segment、最新修正はsegment 038のみ再生成、Engine PASS
- [x] subtitle preflight：44 cue、最小72px、FAIL 0 / WARN 0、tts_reading_leakage PASS
- [x] CTA preflight：Episode 010専用override、表示本文欠落・clipping 0、音声11.456秒
- [x] draft_v1：219.177秒、1920×1080、H.264/AAC、48kHz、draft QA FAIL 0 / WARN 0
- [x] draft_v2：219.486秒 expected（実ファイル約219.49秒）、1920×1080、H.264/AAC、48kHz、draft QA FAIL 0 / WARN 0
- [x] draft_v2 human full-watch：APPROVED、senior_readability=PASS
- [x] final.mp4：draft_v2からcopy-only、byte-identical、Final QA PASS
- [x] thumbnail：ChatGPT生成原本を受領。公開用1280×720、2MB以内、画像QA PASS
- [x] YouTube：private upload、thumbnail設定、2026-09-06 19:00 JST予約、API verify PASS
- [x] experiment QA：micro_story_intro PASS、reason_to_return_present PASS、duplicate_cta 0、midroll_cta 0
- [x] representative frames：21枚、contact sheet作成

## Latest fix QA

- [x] internal_episode_number_visible：0
- [x] internal_episode_number_spoken：0
- [x] 3:03付近 related_video_wording：PASS、subtitle_sync：PASS
- [x] 3:30付近 cta_visual_balance：PASS、cta_clipping：0、end_screen_reserved：PASS、subtitle_safe_area：PASS
- [x] draft_v1 regression：0
- [x] `internal_episode_id_not_viewer_facing`：PROPOSED（canonical化は人間判断待ち）

## Human confirmation required

- 実機と現在の公式画面のボタン名・順番
- NFC読み取り位置の機種差
- raw素材を含む個人情報の最終確認
- ImageGen native文字の完全一致とTV視認性（draft_v2全編承認済み）
- official UIと概念画像の区別
- Episode 002・007の回遊URL
- AI disclosureの最終判断
## Remaining human action

- FC-019：採用端末で現行アプリのボタン名・順番を実機照合（記録上のREVIEW）
- FC-020：Android公式対応機種一覧と採用端末を照合（記録上のREVIEW）
- YouTube Studioで関連動画「ログインできない？まず確認したい5つ」とチャンネル登録のEnd Screenを設定

## Publication result

- video ID：`rU5jlU7eq3I`
- privacy：`private`
- publishAt：`2026-09-06T10:00:00Z`（2026-09-06 19:00 JST）
- channel guard：`UCgVRceTJYO5KOrPX4w2jXZw` / 大人のデジタル安心室
- End Screen：YouTube Studioでの人間設定が必要。動画側の右40〜45% reservedは維持。
