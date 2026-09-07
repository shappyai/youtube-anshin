# Episode 005 State

- status: finalized
- human_approved: true
- phase: Phase 2 / Phase B前半
- research_date: 2026-09-01
- title: 【Googleフォト】写真を消して大丈夫？「削除」と「空き容量を増やす」の違い
- slug: google_photos_delete

## Phase A 成果物（2026-09-01）

- `brief.md` / `sources.md` / `script.md`（65ナレーションセグメント・想定6分〜7分） / `shotlist.md`（SHOT-01〜08＋25 scene） / `episode.json`（schema検証0件・25 scene） / `publish.json` / `media_manifest.csv` / `STATE.md`
- `work/subagents/005_google_photos_delete/`: research_report.md・title_analysis.md・script_review.md・fact_check.md・visual_plan.json
- `work/`: scene_mode_advisor.md・image_generation_manifest.md・scene_prompts/・pronunciation_candidates.md・phase_a_preflight.md・production_metrics.json
- 一次情報HTML21件: `local/web_check_005/`

## Phase B前半 成果物（2026-09-01）

- GPT画像5枚: `assets/generated_ai/scene_001.png`、`scene_003.png`、`scene_013.png`、`scene_017.png`、`scene_025.png`（原本検証済み）。レビュー用1920×1080正規化copy: `work/phase_b_review/normalized_ai/`
- Android実画面crop: `assets/captured/android/`。SCENE-004は公式fallback、SCENE-006は局所cropで解決、SCENE-008/012/014はPASS。SCENE-022はGoogle公式ヘルプfallbackで解決。
- iPhone実機は未使用。公式ページfallback crop: `assets/official/`（SCENE-018/019）。
- 実画面レビュー: `work/phase_b_review/rendered_scenes/`、`work/phase_b_review/scene_contact_sheet_v2.png`、`work/phase_b_review/gpt_image_contact_sheet.png`
- サブエージェントQA: `work/subagents/005_google_photos_delete/android_capture_report.md`、`audio_qa_report.md`、`iphone_official_report.md`、`visual_qa.md`

## Fact Check（2026-09-01）

- FAIL: 0件 / REVIEW: 3件（低優先度。修正反映済み: seg14 設定の画面／seg21 バックアップをオンにしている／seg31 基本的に／seg57 写真一覧に戻ってきます）
- 最重要7項目すべて一次情報で確認。過剰断定なし。

## 次ゲート（人間確認）

1. `scene_contact_sheet_v2.png`と発音レビュー（特にseg046 previewの「かた」）
2. 公式fallback cropの可読性と、SCENE-022の「ゴミ箱に残っている間は復元できる」というfact boundaryを確認
3. full draft
4. thumbnail / publish

## Phase B前半で行わないこと（完了済みとして記録）

- VOICEVOX本編WAV生成・試聴、最終字幕タイミング、video build、draft/final、thumbnail生成、YouTube操作は未実施。

## Phase B前半残課題処理（2026-09-01）

- seg046のみ`reading_overrides: {"方": "かた"}`を使用。global dictionaryは変更していない。preview WAVは`work/phase_b_review/audio/seg046_otsukai_no_kata_preview.wav`。
- pronunciation preflightは65/65 query、未解決 REVIEW 0。`work/pronunciation_preflight.md`と`work/subagents/005_google_photos_delete/audio_qa_report.md`を更新。
- 字幕12件とSCENE-020/025の改行を修正し、安全幅超過0・linebreak WARN 0。
- SCENE-022はAndroid再撮影ではなく、Google公式ヘルプの手順crop＋Codex overlay。`media_manifest.csv`にsource URL・capture date・crop noteを記録。
- renderは25/25。変更した004/020/022/025のみ再render、GPT画像5枚は再生成していない。contact sheet v2を更新。
- 現在は人間のpreview試聴とcontact sheet／公式crop可読性確認で停止中。

## Phase B後半（2026-09-02）

- seg046は人間承認済み（APPROVED_BY_HUMAN）として採用。TTS入力「お使いのかた」、字幕は「お使いの方」のまま。global辞書変更なし。
- SCENE-016/017の英字途中分断（Goo/gle、G/oogle）を修正。`scripts/scene_renderer.py`のwrapをASCII英数字token不可分に恒久化し、`scripts/phase2_qa.py`へASCII token／仮名（小書き仮名・長音符）分断検出、`scripts/subtitle_preflight.py`のPROTECTED_TERMSへGoogle系を追加。
- SCENE-025の「いっしょ」分断も検出・修正（明示改行）。修正対象sceneは016/017/025のみ再render、他はreuse（`work/rendered_final_scenes`）。
- Gate 2: `work/phase_b_gate2.md` PASS。contact sheet v3更新（`scene_contact_sheet_v3.png`）。
- VOICEVOX本編65件生成（剣崎雌雄ノーマル、1.00/1.00/0.00、総尺368.937秒）。2回目のビルドでは65件すべてreuse。
- subtitle timing 65件を実測durationから生成（`work/audio_timing.json`、`captions_auto.srt/.ass`）。
- draft assemble: `output/draft_v1.mp4` → SCENE-025修正後 `output/draft_v2.mp4`（1920×1080・30fps・H.264・AAC 48kHz・全長378.93秒・CTA 10秒）。
- 自動QA PASS: fail/warn 0、decode error 0、black frame 0、silence anomaly 0、narration 65/subtitle 65/scene 25。
- visual frame QA: `work/qa_frames/`（v1）と`work/qa_frames_v2/`（修正確認）。公式crop可読性・字幕帯干渉なしを目視確認。

## 次ゲート（人間全編視聴）

1. `output/draft_v3.mp4` を再確認（3:20 / 4:01 の「あく」、5:03 の表示、CTA音声、字幕同期、公式UI可読性）
2. full draft承認後: thumbnail / publish（finalizeは人間承認後にのみ）

## draft_v3（人間レビュー反映、2026-09-02）

- 約3:20 / 約4:01の「空く」（すく→あく）: seg37・seg44のみsegment override `空く→あく`。query kanaは「アク」を確認。字幕・表示テキストの「空く」は維持。
- pronunciation恒久対応: `config/voicevox_pronunciation.yaml`へ容量文脈限定フレーズ「で空くのは→であくのは」「空く容量が→あく容量が」を登録（単体「空く」のglobal登録なし）。`episode_io.py`の文脈候補に「空く」を追加（要調査の自動提案）。
- 約5:03（SCENE-020）: compareカードをtitle/body構造へ分解し、「60日（バックアップ済み）／30日（未バックアップ）」の自然な2行表示に修正。QA走査で検出したSCENE-007（ほ／か）・013（機能名途中分断）・019（30／日、され／ます）も局所修正。
- line-break QA拡張: wrapの括弧内不可分（開き括弧で改行を送り、括弧内を1単位に）、QA検出に括弧内改行・閉じ括弧行頭・保護語またぎ・数字と単位の分断を追加（`scripts/scene_renderer.py` / `scripts/phase2_qa.py` / `scripts/subtitle_preflight.py`）。
- CTA恒久仕様: `config/channel_cta.json`をsource of truth化（canonical_text / narration_text / display_text / audio_required / duration_mode=audio_based / trailing_seconds / content_hash）。「10秒静止画のみ」運用を終了。`create_channel_cta.py`に共通CTA音声生成を追加、`phase2_video.py`で本編直後にCTA音声を連結。
- CTA本文: 「大人のデジタル安心室では、スマホやパソコンを、もっと安全・快適に使うための情報をお届けします。チャンネル登録・高評価もよろしくお願いします。」（画面と音声が同一）。音声11.56秒＋余韻1.0秒＝CTA尺12.56秒。
- CTA QA追加（`phase2_qa.run_qa`）: 画面なしFAIL / 音声なしFAIL / 音声>尺 FAIL / content hash不一致REVIEW / 余韻不足WARN。
- `output/draft_v3.mp4`: 381.47秒（本編368.9＋CTA12.56）。H.264 1920×1080 30fps / AAC 48kHz。自動QA PASS（fail/warn 0、decode error 0、black frame 0、silence anomaly 0、65 narration / 65 subtitle / 25 scene、CTA音声あり）。
- draft_v1/v2は上書きせず履歴として残存。Episode 001〜004は無変更。

## 再確認ポイント（人間）

1. 約3:20（seg37）と約4:01（seg44）: 「あく」と聞こえるか
2. 約5:03（SCENE-020）: 「60日（バックアップ済み）／30日（未バックアップ）」の表示
3. CTA（6:08.9〜6:21.4）: 画面と音声の一致・余韻1秒
4. 全体: 字幕同期・公式crop可読性（前回指摘の再発なし）

## finalize（2026-09-02）

- `output/final.mp4`: `draft_v3.mp4`をbyte copy（再エンコードなし）。SHA256完全一致 `F52D20E3E5DF014A681EAD5AE8A3CE33F7654E9C55A366FA8428373DD102E597`。
- final QA PASS: decode error 0 / black frame 0 / silence anomaly 0 / 1920×1080 / 30fps / H.264 / AAC 48kHz / narration 65 / subtitle 65 / scene 25 / CTA音声あり・画面あり・canonical hash一致。
- CTA最終確認: canonical「大人のデジタル安心室では、…チャンネル登録・高評価もよろしくお願いします。」が画面・音声の同一source。音声11.56秒・尺12.56秒（余韻約1秒）。brand promise「怖がらせる前に、確認する。」は不採用。
- thumbnail: 人間指定の `assets/thumbnail/thumbnail.png`（1672×941、1.78MiB）を正式採用（approved）。publish.jsonのthumbnail参照を更新。
- publish metadata: タイトル確定（人間指定を維持）、descriptionに削除/デバイスから削除/空き容量/バックアップ/Android/iPhone差/ゴミ箱/公式sources/VOICEVOX creditを確認、chaptersを実尺へ更新（00:00 / 00:46 / 01:30 / 02:23 / 03:00 / 04:13 / 05:07 / 05:41）、contains_synthetic_media=true、made_for_kids=false、private・scheduled_at=null（未upload）。

## 現在の停止位置

- YouTube upload / schedule / 公開は未実施。thumbnail人間承認後に公開準備（dry-run→人間確認→private/scheduled・verify）へ進む。

## 現在の停止位置（thumbnail承認後）

- thumbnail = **ready**（人間指定ファイルを正式参照）。publish metadata = metadata_ready。
- 次はYouTube公開前確認（publish dry-run→人間確認→privateまたはscheduled upload→verify）のみ。

## YouTube publication
- youtube_upload: uploaded_scheduled
- youtube_video_id: T6XHnYt1XXc
- youtube_url: https://youtu.be/T6XHnYt1XXc
- youtube_privacy: private
- youtube_scheduled_at: 2026-09-08 19:00:00 JST
- youtube_scheduled_at_api: 2026-09-08T10:00:00Z
- thumbnail_uploaded: true
- uploaded_at: 2026-09-01T23:15:15Z
- youtube_channel_id: UCgVRceTJYO5KOrPX4w2jXZw
- youtube_publish_error: null
- youtube_ai_disclosure_verified: true
- youtube_ai_disclosure_source: videos.update response（videos.listはcontainsSyntheticMediaを返さないため。insert bodyにもtrueを送信済み）
- youtube_ai_disclosure: true
- youtube_ai_disclosure_updated_at: 2026-09-01T23:16:32Z
- youtube_ai_disclosure_verified: true
- youtube_ai_disclosure_verification: videos.update response; videos.list omitted containsSyntheticMedia
