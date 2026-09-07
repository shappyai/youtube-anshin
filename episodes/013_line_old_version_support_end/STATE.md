# Episode 013 state

- Episode: `013_line_old_version_support_end`
- Topic: LINE旧バージョン・古いOSのサポート終了予定を、3つの確認手順とケース分岐で説明
- 基準日: 2026-09-06
- Phase: **Phase B / FINALIZED**
- Summary: **FINAL QA PASS / YouTube scheduled upload complete**
- status: finalized
- human_approved: true
- final_path: `output/final.mp4`
- final_qa: PASS (`output/review/final_qa.md`)
- final_sha256: `C9EFCABCD1888337E0E1707F045D14176097121B1CDA07C1B4BB78846D3E60F5`
- upload_eligible: true
- thumbnail_status: HUMAN_APPROVED_EXISTING_ASSET
- viewer_facing_internal_brand_promise: 0
- midroll_cta_count: 0
- end_cta_count: 1
- Selected title: `【LINE】11月に使えなくなる？今のスマホで確認したい3つ`

## 完了

- LINE公式、Apple公式、Google公式を再確認
- brief / research / sources / fact_check / script / shotlist / media_manifest / episode.json / scene_plan / publish.jsonを作成
- 6〜8分のduration_depth_gateを実施しPASS
- Visual Redesign v2を24sceneで生成し、`scene_contact_sheet_visual_redesign_v2.png`を作成。2026-09-06に人間Visual Gate APPROVED
- ImageGen-native 5sceneは承認済みassetとしてreuse。renderer-native 12scene、real UI capture 7sceneの構成をcanonical化
- 人間承認済みの3点を反映: registration_conversion_v1 CTA、SCENE-004/008/012のicon縮小、SCENE-018「ケースA 今回は対応不要」
- LINE公式ページを2026-09-06に再確認。11月上旬予定、対象LINEバージョン、OS下限、最新版推奨環境に変更なし
- Android SCENE-006/010/014/016、iPhone SCENE-009/013/015を実画面cropとして採用。SCENE-005はiPhone実機撮影を正式除外し、LINE公式事実だけのrenderer-nativeへ変更
- 機械品質: Visual Gate v3は24scene OK / 0 WARN / 0 FAIL。公式素材の重心・字幕安全帯・背景整合もPASS
- Human Visual Gate v3を2026-09-06に承認。現在の24scene構成を正式採用し、65+ / TV可読性だけはdraft Human Gateで再確認する
- F-011「11月上旬の具体的実施日は未確定」を既知のFact boundaryとして人間承認。動画では「11月上旬にサポート終了予定」までに制限し、具体日・確定済み表現は使わない
- 共通Background System、44px未満情報文字なし、見出し80px以上、字幕72px設計を反映
- iPhone／Androidを時間方向に切り替える実機キャプチャ計画を作成
- Android emulator（emulator-5554）でSCENE-010/016を実画面capture。個人情報を含む端末情報画面は採用せず、Androidバージョン行とOS更新状態だけをcrop
- 公式UIのAI再現なし、fake UI 0、ImageGen-native scene 5（人間承認済みreuse）
- 中盤CTAなし、registration_conversion_v1の15秒postrollを1回だけreuse
- VOICEVOX剣崎雌雄で74segmentを実測生成（本編405.874秒）、audio_timingとquery auditを保存
- VOICEVOX実測に基づくcaptions.srt / captions.assを生成。subtitle preflightはFAIL 0 / WARN 0
- Phase B機械QAを再実行。Phase 2 QA、subtitle preflight、CTA preflight、ImageGen文字QA、公式素材検証、production preflightはPASS。production preflightはVOICEVOX query 74/74、発音REVIEW 0、CTAはregistration_conversion_v1を1回だけ使用
- 既存audioを再生成せず、REVIEW 8件の全文segment音声を1秒無音で連結したHuman Review Packを作成（`work/pronunciation_review_v3.md` / `work/pronunciation_review_v3.wav` / 67.053秒）
- 発音8件を人間が全件聴取し、ALL OKとして`HUMAN_APPROVED`。Episode013のsegment-specific context approvalのみを記録し、共通辞書追加0・既存audio再生成0（`work/pronunciation_human_approval_v3.md`）
- `output/draft_v1.mp4`を2026-09-07に生成。本編405.874秒、postroll15.000秒、全体420.870秒。既存74音声を全件reuseし、音声再生成0。Phase 2 QA PASS
- Human Draft GateはAPPROVED_WITH_ONE_FIX。SCENE-024のviewer-facing内部ブランド文言だけを「今日の3つを確認」へ差し替え、音声・字幕・ImageGen・実機captureは変更しないまま`output/draft_v2.mp4`を再構成
- `output/final.mp4`は承認済み`draft_v2.mp4`のcopy-only finalize。Final QA PASS（decode error 0 / black frame 0 / unexpected silence 0 / AV sync PASS / clipping 0 / 1920x1080）
- `work/human_review_points_draft_v1.md`に全編Draft Gateの実測時刻を記録

## Counts

- narration segments: 74（VOICEVOX実測生成済み）
- narration duration: 405.874秒（postroll前）
- narration characters: 2486（episode.jsonの`phase_a.character_count`を正本とする）
- scenes: 24
- official UI scenes: 7（実機キャプチャ CAPTURED 7 / 7。Android 4 / 4、iPhone 3 / 3。SCENE-005は公式事実renderer）
- ImageGen scenes: 5（approved reuse）
- renderer-native visual scenes: 12
- template runtime scenes: 12
- official quote / threshold scenes: 0（テンプレート上の正確なテキストで表示）
- fact FAIL: 0
- fact REVIEW: 0
- fact HUMAN_APPROVED_REVIEW: 1（F-011）
- subtitle preflight: PASS（fail=0 / warn=0）
- pronunciation preflight: PASS（query 74/74 / REVIEW 0 / human-approved 8。共通辞書追加なし）
- draft_v1: PASS（本編405.874秒 / postroll15.000秒 / 全体420.870秒 / scene24 / subtitle74）
- core answer: 約10〜15秒見込み
- first check action: 約22〜25秒見込み

## YouTube非公開アップロード前

- draft Human Gateでの65+ / TV可読性・SCENE-005事実表示・SCENE-013/014の`開く`表示の再確認
- Fact / Privacy / Audio / Subtitleの全編最終人間確認（機械QAはPASS）
- YouTube非公開アップロード＋2026-09-13 19:00 JST公開予約
- End Screen設定

## 人間確認ポイント

1. draft Human Gateで、7つの実画面が65+ / TV視聴でも読めることを確認
2. 実機表示とF-011／台本の一致。SCENE-013/014の実表示「開く」を更新ボタンに置き換えない
3. 2026-09-10 Apple Event後の公開順
4. 公開前のLINE公式ページ再確認

停止文: **Final QA PASS。指定サムネイルを使ったYouTube非公開アップロード＋2026-09-13 19:00 JST公開予約済み。End Screenは未実施。**

## YouTube publication
- youtube_upload: uploaded_scheduled
- youtube_video_id: F5TMUaHrGDo
- youtube_url: https://youtu.be/F5TMUaHrGDo
- youtube_privacy: private
- youtube_scheduled_at: 2026-09-13 19:00:00 JST
- youtube_scheduled_at_api: 2026-09-13T10:00:00Z
- thumbnail_uploaded: true
- uploaded_at: 2026-09-06T16:11:33Z
- youtube_channel_id: UCgVRceTJYO5KOrPX4w2jXZw
