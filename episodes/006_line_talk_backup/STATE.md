# Episode 006 State

- status: finalized
- human_approved: true
- human_approval_note: draft_v2・公開メタデータ人間承認済み。public公開は未承認
- phase: Phase B前半
- research_date: 2026-09-02
- title（候補・第一推奨）: 【LINE】トーク履歴、消えない？機種変更・故障の前に確認したい3つ
- slug: line_talk_backup

## Phase A 成果物・人間レビュー反映（2026-09-02）

- `brief.md` / `sources.md`（SRC-001〜013） / `script.md`（68ナレーションセグメント・想定約6分20秒） / `shotlist.md` / `episode.json`（schema検証0件・24 scene・68 segment・68 subtitle） / `publish.json`（metadata draft） / `media_manifest.csv` / `STATE.md`
- `work/subagents/006_line_talk_backup/`: research_report.md・title_analysis.md・script_review.md・fact_check.md・visual_plan.json
- `work/`: scene_mode_advisor.md・image_generation_manifest.md・scene_prompts/・pronunciation_candidates.md・phase_a_preflight.md・production_metrics.json
- 一次情報HTML13件: `local/web_check_006/`（2026-09-02取得）

## Phase B前半 成果物（2026-09-02）

- GPT画像5枚: `assets/generated_ai/scene_001.png` / `scene_003.png` / `scene_015.png` / `scene_019.png` / `scene_025.png`。原本を保持し、レビュー用1920×1080正規化copyを `work/phase_b_review/normalized_ai/` に作成。
- GPT画像contact sheet: `work/phase_b_review/gpt_image_contact_sheet.png`。全scene contact sheet: `work/phase_b_review/scene_contact_sheet.png`。
- Android実画面: LINE未インストールのため取得せず、SCENE-006 / 007 / 011 / 016を公式保存HTML由来引用カードへfallback。報告: `work/subagents/006_line_talk_backup/android_capture_report.md`。
- iPhone実画面: 未取得。SCENE-014を公式保存HTML由来引用カードへfallback。公式素材の出典・確認日・SHA: `work/subagents/006_line_talk_backup/iphone_official_report.md`、`media_manifest.csv`。
- 公式引用カード7枚: `assets/official/`。いずれも実在UIではなく、カード上に明記。
- 全24sceneの仮レンダー: `work/phase_b_review/rendered_final_scenes/`。rendered 24/24、render status PASS。
- CTA画面: `work/channel_cta.png`。`config/channel_cta.json` の共通CTAを使用し、CTA音声は未生成。
- pronunciation audio_query preflight: `work/phase_b_review/pronunciation_preflight.md`（68/68 query、REVIEW 5、辞書変更なし）。
- Human Gate記録: `work/phase_b_front_gate.md`（WAITING_FOR_HUMAN_REVIEW）。

## Fact Check（2026-09-02）

- FAIL: 0件／Phase A REVIEW 4件はcanonicalへ反映済み（詳細・履歴は `work/subagents/006_line_talk_backup/fact_check.md`）
- 最重要項目（標準バックアップの仕様・PIN 14日間・異なるOS・プレミアム・写真動画）はすべて一次情報で確認

## subtitles / schema QA

- schema（`episode_io.validate_episode`）: 0件
- subtitle preflight: PASS（fail 0 / warn 0）。PROTECTED_TERMSへEpisode 006用語（トーク履歴・標準バックアップ・自動バックアップ・プレミアムバックアップ・バックアップ・引き継ぎ・iCloud Drive・Google ドライブ・PINコード・メイン端末・セーフティネット等）を追加（scripts/subtitle_preflight.py）

## 次ゲート（人間レビュー）

1. scene contact sheet ＋ pronunciation REVIEW（Phase B前半。現在ここで停止）
2. Android/iPhone公式fallbackの可読性・実画面fallback継続可否
3. full draft
4. thumbnail / publish

## Phase B後半 成果物（2026-09-02）

- `work/phase_b_review/pronunciation_human_review.md`: 発音REVIEW 5件を人間確認用に一覧化（全5件「そのままでよい」の自動判定付き）。
- `work/phase_b_review/readability_review.md`: 公式fallback7sceneをPASS／CROP推奨／要人間確認で判定（全7scene CROP推奨）。SCENE-010は問題なし。
- `work/phase_b_review/readability_fix/`: 7sceneのレビュー用拡大版（約1.8〜2.0倍・静止1構図・実UIの再現なし・元素材のクロップのみ）＋`manifest.json`。
- `work/phase_b_review/ai_disclosure_candidate.md`: 概要欄用のAI素材開示文（1文）を提案。動画本体への追加はしない。
- canonical（`episode.json`等）は本工程では変更していない。差し替えは人間承認後に親Codexが行う。

## Phase B後半 次ゲート（人間確認）

1. pronunciation 5件の承認（`pronunciation_human_review.md`）
2. 可読性修正版7枚の確認（`readability_fix/`）と正式採用の可否
3. SCENE-010は変更不要のまま
4. full draft（本編VOICEVOX・字幕タイミング・video buildは人間承認後に開始）

## 本編生成（2026-09-02・人間承認後の工程）

- canonical反映: `episode.json` の `official_asset` 7sceneをreadability版へ更新。`shotlist.md`・`media_manifest.csv`も同期（元素材は保持）。AI開示文を説明欄へ1行追加（episode.json/publish.json同期済み）。
- VOICEVOX本編: 剣崎雌雄／ノーマル（speed 1.00/intonation 1.00/pitch 0.00）。**68/68生成**。総尺395.459秒（約6分35秒）＋CTA 12.56秒。
- 字幕: `work/audio_timing.json`（実測ベース）→ `work/captions_auto.srt/.ass`（68件・72px・字幕帯方式）。語中分割・句読点行頭・overflowなし（subtitle preflight PASS）。
- 仮レンダー: `output/draft_v1.mp4`（1920×1080・30fps・H.264・AAC 48kHz・全長407.93秒≒6分48秒・24scene＋CTA）。
- 自動QA: `phase2_qa` **PASS**（fail 0 / warn 0）。黒フレーム0・欠落0・無音0・字幕安全幅0。
- 発音5件の実音声: すべて意図した読みで生成（キョオ／ヒライテ・ヒラキマス／ホオ／タンジョオビ／キョオ）。試聴WAV `work/phase_b_review/audio/pronunciation_5seg_review.wav`。
- 人間レビュー用: `work/phase_b_review/human_review_checklist.md`（scene・時刻一覧）／`final_scene_contact_sheet.png`／`readability_adoption.md`。

## draft_v2（2026-09-03・人間レビュー修正）

- readability 7sceneの入れ子表示を解消（readability PNGを全面表示。`full_bleed_asset`）。二重タイトル・二重footerなし。
- PINの発音を「ピーアイエヌ」（アクセント6・ピー低→アイ上→エヌ高維持）へ統一。`config/voicevox_pronunciation.yaml` にEP006スコープで登録、`scripts/tts_voicevox.py` に `accent_on_phrase` を追加（他Episode無影響）。
- PIN 5seg（7/39/40/45/66）のみ再生成し、字幕タイミングを再同期（68件）。
- 出力: `output/draft_v2.mp4`（全長407.93秒≒6分48秒）。phase2_qa PASS。
- レビュー用: `work/draft_v2_review/readability_frames/`・`pin_pronunciation_report.md`・`pin_pronunciation_review.wav`・`change_summary.md`。

## 公開準備（2026-09-03・人間承認済みdraft_v2固定）

- draft_v2 人間レビュー: **PASS**（readability 7scene PASS・PIN発音 PASS・narration/subtitle/scene mapping PASS）
- 公開候補版: `output/final.mp4`（draft_v2のcopy-only・SHA一致をfinal_qaで確認。約6分48秒・1920×1080・30fps・H.264・AAC 48kHz）
- 推奨タイトル: 【LINE】機種変更の前に確認！トーク履歴を残すバックアップとPIN（候補3案をpublish.jsonへ反映）
- 概要欄: 完成版を `work/publish_review/final_metadata.txt` へ。AI開示文・チャンネルCTA・公式根拠8件（リンク疎通2026-09-03全200 OK）を含む
- チャプター: 8件（実測タイミング基準、`work/publish_review/final_chapters.txt`）
- サムネイル2案: `work/publish_review/thumbnail_a.png`（推奨）／`thumbnail_b.png`（1280×720・SCENE-001 GPT画像ベース）
- 公開前QA: `work/publish_review/pre_publish_qa.md` PASS（ISSUES 0）
- 人間レビュー: `work/publish_review/publish_review.md`
- public公開・予約公開・コメント・SNS告知は**未実施**（privateアップロードのみ2026-09-03実施）

## サムネイル確定（2026-09-03）

- 人間作成新案を正式採用: `assets/thumbnail/thumbnail.png`（1280×720・PNG）
- 経緯: 入力1672×941（16:9・crop不要）→ LANCZOSで1280×720最終化 → `work/publish_review/thumbnail_final.png` → `assets/thumbnail/thumbnail.png` へ反映
- バックアップ: 人間入力元を `assets/thumbnail/thumbnail_human_input.png` として保持
- 主文言・3要素（日時確認/自動バックアップ/PINコード）・人物・ブランド表示は変更なし
- publish.json: thumbnail=assets/thumbnail/thumbnail.png・thumbnail_status=approved
- final.mp4（SHA不変）・タイトル・概要欄・チャプター・AI開示は変更なし（この時点では公開処理未実施。2026-09-03にprivateアップロード実施）

## YouTube privateアップロード（2026-09-03 JST）

- uploaded_to_youtube: true
- visibility: private（publishAtなし・予約なし・unlisted/publicではない）
- youtube_video_id: DK0431L9TwA
- youtube_url: https://youtu.be/DK0431L9TwA
- upload date/time: 2026-09-03 06:06:48 JST（uploaded_at=2026-09-02T21:06:48Z）
- final.mp4 production complete（SHA不変・copy-only finalize）
- thumbnail approved / metadata approved（title・description・chapters・tags・category 22・language ja・made_for_kids false）
- AI開示: containsSyntheticMedia=true（YouTube側status更新・videos.update responseで検証。videos.listは本APIで同項目を省略する既知の挙動）
- HD / 1080p処理状況: **succeeded**（processingStatus=succeeded・fileDetails duration 408000ms）
- サムネイルアップロード: true
- human YouTube QA: **pending**（`work/publish_review/youtube_private_review.md`）
- 公開済み扱いにはしない（public昇格・予約は未承認）

## Phase B前半で行わないこと（未実施）

- VOICEVOX本編WAV生成・全編試聴・最終字幕タイミング
- video build・draft/final・thumbnail画像生成・YouTube操作
- 実アカウントでのLINEログイン、SMS認証、新規アカウント作成、実トーク取得

## CTA

- エンディングは `channel_common_cta`（`config/channel_cta.json`準拠・音声あり・duration_mode=audio_based）。新規CTAを作らない。「怖がらせる前に、確認する。」はCTAに含めない。

## 撮影媒体方針（Phase A確定・Phase B実績）

- LINEアプリ基本操作 → Android Emulatorまたは安全なテスト端末を優先。今回はLINE未インストールのため公式保存HTML由来引用カードで代替
- iPhone差分（iCloud Drive確認） → iPhone実機またはLINE公式資料。今回は公式保存HTML由来引用カードで代替
- 仕様の出典 → LINE公式保存HTML由来の引用カード（実在UIではない）
- 概念・安心 → GPT画像5枚（LINE UIのAI生成なし）
- 一覧・比較・注意・まとめ → Codexテンプレート

## YouTube publication
- youtube_upload: uploaded_private_verification_failed
- youtube_video_id: DK0431L9TwA
- youtube_url: https://youtu.be/DK0431L9TwA
- youtube_privacy: private
- youtube_scheduled_at: null
- youtube_scheduled_at_api: null
- thumbnail_uploaded: true
- uploaded_at: 2026-09-02T21:06:48Z
- youtube_channel_id: UCgVRceTJYO5KOrPX4w2jXZw
- youtube_publish_error: PublishError
- youtube_ai_disclosure: true
- youtube_ai_disclosure_updated_at: 2026-09-02T21:07:09Z
- youtube_ai_disclosure_verified: true
- youtube_ai_disclosure_verification: videos.update response; videos.list omitted containsSyntheticMedia
