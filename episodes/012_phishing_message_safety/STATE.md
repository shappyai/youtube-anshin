# Episode 012 state

- Episode: `012_phishing_message_safety`
- status: finalized
- human_approved: true
- Title candidate selected: `【詐欺メール】本物そっくりでも見分けなくていい？安全に確認する5つの場面`
- Status: `UPLOADED_SCHEDULED`
- Phase A completed: 2026-09-06
- Experiment: `long_form_watchtime_v1`
- Theme: SMS・メールのリンクを使わず、自分で公式アプリ・公式サイトを開いて確認する共通手順
- Target: 50〜70代、特に65歳以上とTV視聴。怖がらせる前に、確認する。

## Phase A result

- Narration: 80 segments / 3,473 characters / estimated 650 seconds（約10分50秒、VOICEVOX実測前）
- Scenes: 31（template 25 / ImageGen concept 6）
- Official visual slots: 7 scene slots planned（5 source groups）/ 0 captured in Phase A
- ImageGen adopted assets: 6 / generation calls: 12（同じ主人公への統一置換5回を含む）/ text QA retry: 0 / exact headline QA: PASS
- Contact sheet v1: `work/visual_review/scene_contact_sheet_v1.png`（履歴）
- Human Visual Gate v1: `REJECTED_WITH_COMMON_RENDERER_FIX`。layout_04_text_officialの公式素材未配置fallbackが大きなチェックマークを描き、視覚重心を左へ寄せていたため、Episode固有hackではなく共通renderer / visual policyを修正。
- Contact sheet v2: `work/visual_review/scene_contact_sheet_v2.png`
- Renderer QA v2: 31 OK / 0 WARN / 0 FAIL。`oversized_checkmark_count=0` / `decorative_checkmark_as_main_visual=0` / `meaningless_filler_icon=0` / `left_bias_fail=0` / `tiny_text=0` / `overflow=0`。
- `visual_centroid_preflight`: 公式7sceneを7/7 PASS。重心x=892.93〜965.22、右visual weight最小38.27%。
- Regression: 対象7scene以外の24sceneはv1 baselineとSHA-256一致。ImageGen章扉SCENE-001 / 005 / 010 / 016 / 020 / 024は未変更。
- Fact Check: FAIL 0 / REVIEW 3
- Privacy: FAIL 0 / REVIEW 0
- Long-form depth gate: PASS（机上設計、人間確認待ち）
- Core answer: 20秒以内に「リンクから入らず、自分で公式を開く」
- Mid CTA: segment 030、1回、7秒以内の設計
- AVD target: 8〜12分動画として、まず5分30秒以上を観測基準にし、Episode 002 / 010 / 011と同公開後日数で比較する。成功判定はAVD・総再生時間・冒頭30秒維持を人間が決める。

## Human gate（Phase A完了）

人間が `brief.md`、`script.md`、`sources.md`、`fact_check.md`、`scene_plan.json`、`work/visual_review/scene_contact_sheet_v2.png`、`work/visual_review/visual_gate_v2.md`を確認し、`APPROVED_FOR_PHASE_B`を承認済み。確認項目は、5ケースの区別、公式7scene slots（5 source groups）の採用範囲、完成素材への置換、ImageGen 6枚の採用、TV縮小時の可読性、公開時のAI開示、Apple Event後の公開順。

## Not started by policy（Phase A履歴）

- VOICEVOX音声: 未生成
- `captions.srt` / `captions.ass`: 未生成
- draft / final video: 未生成
- thumbnail画像: 未生成（brief only）
- YouTube upload / schedule / End Screen実設定: 未実施

## Phase B draft_v1（2026-09-06）

- Visual Gate v2: `APPROVED_FOR_PHASE_B`。SCENE-007 / 008 / 012 / 013 / 018 / 022 / 026のneutral browser/phone frameを、公式公開資料クロップまたは意味図解へ置換。
- 公式採用：SCENE-007 国民生活センター、SCENE-008 自分で公式アプリを開く意味図解、SCENE-012 フィッシング対策協議会、SCENE-013 安全な3入口の意味図解、SCENE-018 JCB、SCENE-022 ソフトバンク、SCENE-026 国税庁。公式資料は大きく表示し、個人情報は含めない。
- Phase B visual gate: placeholder 0 / neutral browser 0 / neutral phone 0 / official UI AI reconstruction 0 / privacy PASS / official text TV readability PASS / visual balance PASS。
- Renderer quality: 31 OK / 0 WARN / 0 FAIL。`oversized_checkmark=0`、`meaningless_filler_icon=0`。
- VOICEVOX「剣崎雌雄」80 segmentを生成・連結。字幕100 cue、72px、TTS reading leakage 0。`captions.srt`を配置。
- `output/draft_v1.mp4`: 595.56秒（9分55秒）、Phase 2 QA PASS。contact sheetは`output/review/scene_contact_sheet.png`。
- Fact Check: FAIL 0 / REVIEW 3。長尺目標9〜11分に対して実尺9分55秒で範囲内。
- 状態: `DRAFT_V1_COMPLETE_WAITING_HUMAN_REVIEW`。人間の全編確認とAI disclosure確認まで、thumbnail、final、YouTube upload、schedule、End Screen設定へは進まない。

## Phase B draft_v2（2026-09-06）

- `output/draft_v2.mp4`を、draft_v1の人間指摘（字幕改行、再現ラベル、公式素材、発音、Episode011 CTA不一致）を反映して再構成。実測597.13秒、SHA-256 `94A04D4D905E3736E3792DAC69C1CE2A1935F9D71C11A052951B74161ED48B8B`、Phase 2 QA PASS。
- 字幕119 cue、target72px / minimum56px、overflow 0、3-line 0、TTS reading leakage 0、意味境界4指標すべて0。恒久ルールは `scripts/japanese_subtitle_semantics.py`、`scripts/subtitle_phase_b_split.py`、`scripts/subtitle_preflight.py`、`templates/scenes/README.md`へ追加。
- 説明用SCENE-006 / 011 / 017 / 021 / 025から再現ラベルを削除。SCENE-007は国民生活センター公式PDFの正確な短い引用へ差し替え、取得失敗時に抽出断片を表示しないpolicyを追加。
- 普段、何も、届け物、本物、カード会社、e-Taxを標準承認辞書へ登録。実クエリ監査PASS、カード会社4出現はドaccent、e-Taxは語中pauseなし。
- 終了CTAはEpisode011実使用postrollのcanonical text・PNG・WAV・15秒・右40〜45%予約を一致させて再利用。中盤CTAのEpisode011との一致も確認。
- Contact sheet：`output/review/scene_contact_sheet_v2.png`。人間再確認ポイント：`work/human_review_points_v2.md`。thumbnail、final、upload、schedule、End Screen設定は未実施。
- 状態：`DRAFT_V2_COMPLETE_WAITING_HUMAN_REVIEW`。人間の全編確認とAI disclosure確認まで公開工程へ進まない。

## Phase B draft_v3（2026-09-06・人間全編確認待ち）

- draft_v2の人間再確認で指定された3点だけを反映し、`output/draft_v3.mp4`を生成。実測585.55秒、SHA-256 `662804C23CD1FF6915CA65655671757A80118DD8E7EEC05F56627309EF9B1205`、Phase 2 QA PASS。
- 『これ、本物？』は対象文を直接audio_queryし、ホ／ン／モ／ノの4モーラ、疑問ピッチ、余分な母音なしを確認。`本物`の全7出現に`contextual_pronunciation_audio_gate`を適用し、辞書読みだけでPASSにしない回帰検査を保存。
- `e-Tax`は標準辞書をイータックス（イ・イ・タ・ッ・ク・ス、アクセント3＝タ、語中ポーズ0）へ更新し、`e-Taxのメールも、`の実文クエリを確認。
- SCENE-031とsegment080を本編タイムラインから除外。SCENE-030（segments 076〜079）の直後へEpisode011実使用CTAをpostrollとして直接連結し、終了CTAは1回だけにした。音声・画面・設定のSHA-256はEpisode011実使用値と一致。
- 79 narration / 117 subtitle cue / 30 scene。字幕72px基準・56px以上、既存の日本語意味単位改行ルールを維持し、semantic QA・TTS reading leakageはすべて0。
- 人間再確認時刻表：`work/human_review_points_v3.md`。thumbnail、final、upload、schedule、End Screen設定は未実施。状態：`DRAFT_V3_COMPLETE_WAITING_HUMAN_REVIEW`。

## Phase B draft_v4 / final（2026-09-06）

- ユーザーが修正した `audio/voicevox_kenzaki/segments/030.wav` を一意に確認し、同一SHAの `audio/human_approved/030.wav` をhuman audio overrideの正本として採用。対象文は「これ、本物？」、音声SHA-256は `7B534892A4AC893CC7F1D0D483B67A8A94E690353DB652EA16B0077C3F4C7106`。
- overrideは `human_audio_override > pronunciation dictionary > automatic VOICEVOX generation` の優先順位で処理。030は再生成せず、6.346667秒をtimeline 213.189–219.536秒へreuse。overrideのSHA・narration SHA・保持方針は `work/human_audio_override_v4.json` / `.md` に記録。
- `output/draft_v4.mp4`を作成。v4 build logは `regenerated=[] reused=78 human_overrides=[30]`、自動再生成0件、Phase 2 QA PASS。実測585.400秒、SHA-256 `32933ED599E072DDF27FA7AF99756F4F78B15A3498DA0EA2071F44EC04660DD8`。
- draft_v3、最初のv4 build、旧音声候補は保持。e-Taxはイ・イ・タ・ッ・ク・ス、アクセントピーク「タ」、語中pause 0を維持。字幕117 cue、72px基準／56px以上、semantic metrics・overflow・3-line・TTS leakageはすべて0。
- 人間全編確認とsenior_readabilityをPASSとして記録し、`output/final.mp4`をdraft_v4からcopy-onlyで確定。finalは585.400秒、47,642,598 bytes、SHA-256はdraft_v4と一致。`work/final_qa.md` と `qc.md` に最終QAを保存。
- ユーザー提供サムネイルを内容変更なしで正式採用し、1280×720へ正規化。YouTube upload、schedule、metadata、サムネイル設定はAPI検証済み。End Screen設定はYouTube Studioの人間作業として未実施。状態：`UPLOADED_SCHEDULED`。

## YouTube publication
- youtube_upload: uploaded_scheduled
- youtube_video_id: CzTNLyAn1lY
- youtube_url: https://youtu.be/CzTNLyAn1lY
- youtube_privacy: private
- youtube_scheduled_at: 2026-09-12 19:00:00 JST
- youtube_scheduled_at_api: 2026-09-12T10:00:00Z
- thumbnail_uploaded: true
- uploaded_at: 2026-09-06T09:14:01Z
- youtube_channel_id: UCgVRceTJYO5KOrPX4w2jXZw
