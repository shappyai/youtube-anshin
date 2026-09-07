# Shorts探索バッチ001 Visual Redesign v4 timeline review

Draft v4の人間確認用タイムライン。1文1sceneではなく、3 core scenesの中で8 visual beatsへ分割した。
字幕は実音声のsegment時間を正本にし、visual beat境界とは独立して表示する。

## Batch metrics

| ID | duration | beats | mean beat interval | max beat | >5 sec | >7 sec | slideshow | native feel |
|---|---:|---:|---:|---:|---:|---:|---|---|
| Short001 | 28.21秒 | 8 | 3.53秒 | 6.95秒 | 1 | 0 | 1/5_REVIEW | 4/5_REVIEW |
| Short002 | 32.24秒 | 8 | 4.03秒 | 4.94秒 | 0 | 0 | 1/5_REVIEW | 4/5_REVIEW |
| Short003 | 28.60秒 | 8 | 3.57秒 | 6.78秒 | 1 | 0 | 1/5_REVIEW | 4/5_REVIEW |

## CAPTURE_REQUIRED

- Short001は現行ChatGPTホームの実画面（B1/B3/B4）と公式Voice紹介ページ（B2）を使用した。ログイン後のライブVoiceセッション録画は未取得。
- v4 draftではChatGPT UIを描き足さず、公式画面の性質を内部manifestへ記録した。人間Draft Gateで、実Voice 5〜10秒キャプチャを追加するか判断する。

## Beat timeline

| ID | beat | time | core | mode | asset | purpose | motion | CTA / note |
|---|---:|---|---|---|---|---|---|---|
| Short001 | A1 | 0.00〜3.18秒 | A | imagegen | `assets/imagegen_native_v2/normalized/scene_01_hook.png` | person_hook | slow_crop |  |
| Short001 | A2 | 3.18〜6.36秒 | A | imagegen | `assets/imagegen_native_v2/normalized/scene_01_hook.png` | phone_crop | slow_crop_push_in |  |
| Short001 | B1 | 6.36〜9.29秒 | B | real_ui | `assets/official_v4/normalized/chatgpt_home_current.png` | current_public_chatgpt_home | slow_crop | 実画面 |
| Short001 | B2 | 9.29〜12.21秒 | B | official_reference | `assets/official_v4/normalized/voice_official_reference.png` | official_voice_reference_not_live_session | slow_crop | 公式参照 |
| Short001 | B3 | 12.21〜15.13秒 | B | real_ui | `assets/official_v4/normalized/chatgpt_home_current.png` | question_capture_pending | slow_crop | 実画面 |
| Short001 | B4 | 15.13〜18.05秒 | B | real_ui | `assets/official_v4/normalized/chatgpt_home_current.png` | response_capture_pending | slow_crop_push_in | 実画面 |
| Short001 | C1 | 18.05〜25.00秒 | C | imagegen | `assets/imagegen_native_v2/normalized/scene_06_summary.png` | conclusion | slow_crop |  |
| Short001 | C2 | 25.00〜28.21秒 | C | imagegen | `assets/imagegen_native_v2/normalized/scene_06_summary.png` | conclusion_cta | slow_crop_push_in | 実チャンネルアイコン＋チャンネル名のみ。pseudo subscribeなし |
| Short002 | A1 | 0.00〜1.66秒 | A | imagegen | `assets/imagegen_native_v2/normalized/scene_01_hook.png` | person_hook | slow_crop |  |
| Short002 | A2 | 1.66〜3.33秒 | A | imagegen | `assets/imagegen_native_v2/normalized/scene_01_hook.png` | phone_crop | slow_crop_push_in |  |
| Short002 | B1 | 3.33〜8.27秒 | B | renderer | `assets/renderer_v4/privacy_mask_stage_0.png` | generic_document_before_mask | slow_crop |  |
| Short002 | B2 | 8.27〜13.22秒 | B | renderer | `assets/renderer_v4/privacy_mask_stage_1.png` | name_and_phone_masked | slow_crop |  |
| Short002 | B3 | 13.22〜18.16秒 | B | renderer | `assets/renderer_v4/privacy_mask_stage_2.png` | all_pii_regions_masked | slow_crop_push_in |  |
| Short002 | C1 | 18.16〜22.85秒 | C | imagegen | `assets/imagegen_native_v2/normalized/scene_05_official.png` | official_confirmation | slow_crop |  |
| Short002 | C2 | 22.85〜27.55秒 | C | imagegen | `assets/imagegen_native_v2/normalized/scene_05_official.png` | official_confirmation_close | slow_crop_push_in |  |
| Short002 | C3 | 27.55〜32.24秒 | C | imagegen | `assets/imagegen_native_v2/normalized/scene_05_official.png` | conclusion_cta | slow_crop_push_in | 実チャンネルアイコン＋チャンネル名のみ。pseudo subscribeなし |
| Short003 | A1 | 0.00〜4.02秒 | A | imagegen | `assets/imagegen_native_v2/normalized/scene_01_hook.png` | person_hook | slow_crop |  |
| Short003 | A2 | 4.02〜8.05秒 | A | imagegen | `assets/imagegen_native_v2/normalized/scene_01_hook.png` | phone_card_crop | slow_crop_push_in |  |
| Short003 | B1 | 8.05〜10.68秒 | B | renderer | `assets/renderer_v4/usage_cue_portal.png` | mynaportal_usage_cue | slow_crop |  |
| Short003 | B2 | 10.68〜13.32秒 | B | renderer | `assets/renderer_v4/usage_cue_certificate.png` | certificate_etax_usage_cue | slow_crop |  |
| Short003 | B3 | 13.32〜15.95秒 | B | imagegen | `assets/imagegen_native_v2/normalized/scene_03_health.png` | healthcare_usage | slow_crop |  |
| Short003 | B4 | 15.95〜18.59秒 | B | imagegen | `assets/imagegen_native_v2/normalized/scene_03_health.png` | healthcare_usage_close | slow_crop_push_in |  |
| Short003 | C1 | 18.59〜25.37秒 | C | imagegen | `assets/imagegen_native_v2/normalized/scene_05_conclusion.png` | card_required_conclusion | slow_crop |  |
| Short003 | C2 | 25.37〜28.59秒 | C | imagegen | `assets/imagegen_native_v2/normalized/scene_05_conclusion.png` | conclusion_cta | slow_crop_push_in | 実チャンネルアイコン＋チャンネル名のみ。pseudo subscribeなし |

## Human review points

- 0〜3秒のhookが一目で伝わるか。
- Short001のB1/B2/B3/B4が、実UIと公式参照の違いを誤認させないか。ライブVoice captureは必要か。
- Short002のB1→B2→B3で、個人情報の該当部分だけが隠れて見えるか。
- Short003のusage cueが説明カード3枚の再来になっていないか。
- 全Shortの最後2〜3秒で、結論Visualと実チャンネルロックアップが自然か。
- ChatGPTの`ト`、CTAの速度、字幕の読みやすさを実音声で確認する。

final、thumbnail確定、upload、publish、scheduleは未実施。
