# Episode 010 STATE

- episode_id：010
- slug：myna_app_registration
- current_phase：Phase C
- status: scheduled_private
- publication_state: SCHEDULED_PRIVATE
- human_approved: true
- approved_draft: draft_v2
- senior_readability: PASS
- production_decision：PRODUCTION GO
- selected_title：【マイナアプリ】登録方法は？初めて使う人が確認したい手順
- target_publish_date：2026-09-06 19:00 JST（private予約済み）
- experiment：registration_conversion_v1（story_intro=true / reason_to_return_cta=true / midroll_subscribe_cta=false）
- narration_segments：41
- scenes：20
- official_ui_scenes：6
- official_focus_crops：6
- imagegen_scenes：3
- fact_fail：0
- fact_review：2（FC-019、FC-020は更新・実機依存）
- privacy_qa：PASS（生成原画・公式原画の機械確認と人間確認済み）
- visual_qa：PASS
- visual_machine：FAIL 0 / WARN 3（scene_quality_report）
- intro_version：v2
- old_intro：12 segments / 486文字
- new_intro：6 segments / 146文字（core 5 segments / 129文字）
- first_1_6：SCENE-004 / segment 006
- first_action：SCENE-005 / segment 007
- intro_before_first_action：28.516秒（VOICEVOX実測。PASS）
- one_six_start：25.347秒
- subtitle_cues：44（最小72px）
- audio_main：204.486秒
- CTA：専用variant音声11.456秒＋余韻3.544秒＝15秒
- CTA画面：work/cta_registration_conversion_v1.png（共通設定は未変更）
- CTA音声：audio/voicevox_kenzaki/cta_registration_conversion_v1.wav
- draft_v1：219.177秒（比較用に保持）
- draft_v2：219.486秒 expected（registration_conversion_v1 CTAを含む。実ファイルの表示尺は約219.49秒）
- draft_v2 latest fix：segment 038、SCENE-019、CTA説明行のみ更新。first_action 28.516秒、20 scene、official focus crop 6件、CTA音声11.456秒は維持。
- final：output/final.mp4（draft_v2からcopy-only、byte-identical）
- final_duration：219.486秒 / 1920×1080 / H.264 30fps / AAC 48kHz mono
- final_filesize：20,017,692 bytes
- final_sha256：89BBDE65D864944B1E0940E077ADD8C3094997CBD44DCF26A286F0492D830374
- final_qa：PASS（decode 0 / black 0 / unexpected narration silence 0 / audio peak error 0 / av sync PASS）
- thumbnail_status：HUMAN_SELECTED（thumbnail QA PASS）
- thumbnail：assets/thumbnail/thumbnail.png（1280×720、1,147,245 bytes）
- thumbnail_qa：work/thumbnail_review/thumbnail_qa.json
- upload_status：UPLOADED_SCHEDULED
- contact_sheet：work/visual_review/scene_contact_sheet_v2.png
- draft_v2_contact_sheet：work/qa_frames_draft_v2/contact_sheet.png
- intro_comparison：work/visual_review/intro_v1_v2_comparison.png

## 完了

- 公式情報再確認
- Fact Check
- selected title確定
- 台本作成
- 冒頭30秒v2 core message QA
- scene設計
- 公式UI素材配置
- 概念画像生成・正規化
- sceneレンダー
- contact sheet v2作成
- Visual QA
- Visual Gate v2の人間承認
- VOICEVOX音声生成・実測タイミング確定
- 字幕生成・subtitle preflight
- 共通CTA画面・音声生成・CTA preflight
- Episode 010専用CTA override生成・CTA preflight
- draft_v1生成・draft QA
- draft_v1代表フレーム21枚の確認
- draft_v2生成・draft QA
- draft_v2代表フレーム21枚、3:03付近、CTA終盤の確認
- draft_v2全編人間確認（APPROVED）
- final.mp4 copy-only確定・Final QA PASS
- 公開description・chapters・thumbnail brief・受け入れ先を準備

## 公開前の残件

1. FC-019：採用端末で現行アプリのボタン名・順番を照合
2. FC-020：Android公式対応機種一覧と採用端末を照合
3. AI disclosureの最終判断
4. ChatGPT作成サムネイルの受領・人間選択・画像QA
5. YouTube Studioで関連動画とチャンネル登録のEnd Screenを設定

## v2変更

- SCENE-001〜003を問題・短い全体像・最低限の準備に限定し、SCENE-004で1 / 6、SCENE-005で実操作へ入る構成に変更。
- OS条件・NFCをSCENE-012へ、本人認証3ルートをSCENE-013へ移動。
- Episode 002と重複する旧アプリ刷新・既存利用者更新の2文を台本ナレーションから削除。Fact Checkと一次情報は保持。
- 公式UI 6 sceneとfocus crop 6件、common background、ImageGen 3枚は維持。
- segment 038の旧「エピソード007」誘導を「読み取れない、ログインできないときは、関連動画で確認してください。」へ変更し、表示も「ログインできないときは／関連動画で確認」へ変更した。
- CTA「次に困ったときのために」は説明ボックスを110px下げ、登録文言との意味ブロックを維持した。CTA音声は再利用した。
- `internal_episode_id_not_viewer_facing`を提案ルールとして記録。canonical化は人間判断待ち。

## Fact REVIEW 2件

- FC-015：公式案内でiPhoneとAndroidの読み取り位置差を確認済み。特定機種の位置指定は動画に含めない。
- FC-019：公開前に公式ページと採用端末で現行画面の文言・ボタン順を確認する。
- FC-020：公開前にAndroid公式案内と採用端末で機能名称・対応機種を確認する。

## Visual Gate v2

- visual_gate：work/visual_review/visual_gate_v2.md
- privacy_qa：work/visual_review/privacy_qa_v2.md
- machine_qa：FAIL 0 / WARN 3。WARNはcontact sheetで人間確認する。
- human_gate：2026-09-05 Visual Gate v2承認済み。2026-09-06 draft_v2全編視聴も承認済み。

## Experiment QA

- micro_story_intro：PASS
- problem_to_solution_clear：PASS
- reason_to_return_present：PASS
- duplicate_cta：0 / midroll_cta：0
- subscriber_conversion_rate：公開後に `subscribers_gained / unique_viewers` で計算
- subscribers_per_1000_unique_viewers：正式値×1000。unique viewers未取得時は暫定値を別記録
- registered / not subscribed比率：登録転換率とは呼ばず、別指標として記録
- senior_readability：PASS（draft_v2全編視聴承認）
- internal_episode_number_visible：0
- internal_episode_number_spoken：0
- related_video_wording：PASS
- subtitle_sync：PASS
- cta_visual_balance：PASS / cta_clipping：0 / end_screen_reserved：PASS / subtitle_safe_area：PASS
- draft_v1_regression：0

## Phase B以降

VOICEVOX、字幕、Episode 010専用CTA、draft_v2、finalize、Final QA、サムネイルQA、YouTube private予約まで実施済み。draft_v1は比較用に保持する。Fact REVIEW 2件は更新・実機依存の運用確認として記録する。

## YouTube publication
- youtube_upload: uploaded_scheduled
- youtube_video_id: rU5jlU7eq3I
- youtube_url: https://youtu.be/rU5jlU7eq3I
- youtube_privacy: private
- youtube_scheduled_at: 2026-09-06 19:00:00 JST
- youtube_scheduled_at_api: 2026-09-06T10:00:00Z
- thumbnail_uploaded: true
- uploaded_at: 2026-09-05T22:51:38Z
- youtube_channel_id: UCgVRceTJYO5KOrPX4w2jXZw
- youtube_ai_disclosure: true
- youtube_ai_disclosure_updated_at: 2026-09-05T22:52:43Z
- youtube_ai_disclosure_verified: true
- youtube_ai_disclosure_verification: videos.update response; videos.list omitted containsSyntheticMedia
