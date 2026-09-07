# Episode 008 State

- status: finalized
- phase: Phase B完了（Visual Gate v5・draft_v3 human approved・final QA・thumbnail QA PASS）
- human_approved: true
- publication_status: YouTube uploaded・2026-09-08 19:00 JST scheduled
- research_date: 2026-09-05
- human_visual_approved: true
- visual_gate_version: v5
- audience_profile: 60代以上を中心に、特に65歳以上でも無理なく見聞きできる視聴者
- 公開予定: 2026-09-08（private/scheduledは人間判断）
- title（候補・第一推奨・selected）: 【投資詐欺】その有名人、本物？LINEに誘導されたら確認したい3つ
- slug: investment_scam

## 今回のテーマ選定Gate（2026-09-05記録）

- topic_score_trend: 5 / topic_score_age_fit: 5 / topic_score_channel_fit: 5 / topic_score_home_ctr: 4 / topic_score_competition: 3 / topic_score_practicality: 5
- selected_topic_reason: 2026-09-01国民生活センター発表＋警察庁7月末暫定値（前年比+75.6%/+88.6%）で社会的関心が高く、被害額60代最多で50〜60代の自分事。「その広告を見たときに何を確認するか」まで落とし込めるためselected。
- 注記: 2026-09-05時点で、警察庁が9月4日に掲載した「令和8年7月末暫定値」が最新。公開日前に8月末統計が新規公表された場合はpublish watchとして更新要否を人間判断する。

## Episode 002再現仮説

- 仮定: 「社会的関心 × 50〜60代の自分事 × 具体的な困りごと × ホームで一瞬で意味がわかる」が002の伸びの理由。
- 検証: 別ジャンル（投資詐欺）で同型を再現できるか。KPIは002実績（CTR 5.5%・平均視聴3:23・ホーム/ブラウジング94%）と比較。

## 一次情報（2026-09-05・公式本文を直接取得）

- local/web_check_008/ に保存済み（警察庁PDF×3・SOS47 HTML×2・金融庁HTML×5・国民生活センターHTML×3・消費者庁HTML・LINEヤフーHTML）。
- 主要数字: SNS型投資詐欺 令和8年7月末暫定値 6,566件（+75.6%）・881.2億円（+88.6%）／上半期 1日4.4億円・被害額60代最多／接触後LINE誘導 約9割（令和7年）／著名人画像無断使用広告は令和7年7月以降増加が顕著。
- 相談先: #9110・188・0570-050588（金融庁・投資詐欺ダイヤル・平日10-17時）。登録確認: search.fsa.go.jp。

## Phase A 成果物

- brief.md / sources.md（SRC-001〜018） / script.md（63ナレーションセグメント・1文1segment・4:30〜5:30+CTA目標） / shotlist.md / media_manifest.csv / episode.json（schema検証済み: 63 segment・122 subtitle cue・18 source・SCRIPT REVIEW反映済み） / publish.json（title candidates 5・selected・description・chapters・tags・固定コメントcandidate） / fact_check.md（FAIL 0・REVIEW 0） / STATE.md
- work/: production_metrics.json・pronunciation_candidates.md・visual_plan.md・scene_prompts/（IMG-001〜005）
- アイコン: Material Symbols Rounded 10種をGoogle公式配布元から取得しtint PNG化（assets/icons/material_symbols/）。config/icon_catalog.json にusage_episode_008を追加。
- GPT画像5枚（IMG-001〜005）とscene render: 下記「Visual Gate候補」参照。

## Visual Gate候補（Phase A実施分）

- imagegen_native 5枚: SCENE-001（hero）・SCENE-004/008/013（section扉）・SCENE-006（なりすまし広告概念）→ assets/generated_ai/scene_001/004/006/008/013.png
- template render: SCENE-002/003/005/007/009/010/011/012/014/015/016/017/018 → work/rendered_final_scenes/
- contact sheet: work/visual_review/scene_contact_sheet.png
- QA: tiny_text（<44px FAIL）・oversized_single_icon（15%以上WARN）・imagegen_native exact text・scene repetition・詐欺画面の実在誤認なし、を確認済み（結果はcontact sheet付属note）
- 未対応（Human Gate 2候補）: official UI（search.fsa.go.jp）capture可否 / サブタイトル実尺同期 / pronunciation REVIEW 11件

## Fact Check（2026-09-05・最終）

- **FAIL 0件 / REVIEW 0件**。SEG50の「やり取りの画面は消さずに残す」は警察庁SRC-018で確認。統計更新の継続確認は公開前watchとして別管理。ナレーション63/63 PASS（独立レビュー反映）。
- 禁止表現・被害者非難・特定人物言及なし。

## Human Gate（Phase B）

1. **テーマ・台本・visual plan** — Gate 1: 完了
2. **scene contact sheet ＋ pronunciation REVIEW** — Visual Gate v5: 人間承認済み。発音候補12語・文脈REVIEW4件は確認済み
3. **full draft** — `output/draft_v1.mp4` 機械QA PASS。全編人間視聴待ち
4. **thumbnail / publish** — 未着手。人間判断まで停止

## 停止位置（Phase B）

`draft_v1`まで完了。まだ行わない: 全編人間視聴の完了扱い・thumbnail確定・`final/final.mp4`・YouTube upload・End Screen実設定。公開日前の8月末統計確認はpublish watchとして残す。

## 補足

- CTAは config/channel_cta.json の channel_common_cta をそのまま再利用（新規CTAを作らない・ハッシュ一致）。
- End Screen: 右40〜45% reserved。チャンネルロゴ・名称・疑似登録アイコンを描画しない。RELATED VIDEO候補はEpisode 004（ニセ警察詐欺）をcandidateとし、公開前checklistで決定。
- Episode 001〜007の完成済み成果物は変更しない。

## Phase B draft_v2（2026-09-05）

- draft_v1人間全編レビューを反映し、`output/draft_v1.mp4`は保持したまま `output/draft_v2.mp4` を生成。
- Visual Gate v5の18sceneは再renderせず固定使用。変更は音声5segment（006/011/031/052/059）、seg055の字幕表示、CTA画面の局所レイアウトのみ。
- 発音: `信用`はseg006/011/059を `シンヨオ`・accent=2で統一、`今だけ`はseg031だけ `イマダケ`・accent=1、`188`はseg052を `イチ、ハチ、ハチ`で再生成。`0570-050588`のseg055音声はdraft_v1から再利用。
- 音声: 63segment中5件を再生成、58件を再利用。本編321.868秒。preview WAV／audio_query／判定表は `work/phase_b_review/pronunciation_fix_v2/`。
- 字幕: 121 cue。`0570-050588`は公式数字表示。tts_reading_leakage 0、below56px 0、3行0、overflow0。preflightはFAIL 0／非ブロッカーWARN 27。
- CTA: `work/channel_cta_v2.png`へ局所修正。説明文は56px・3行で `お届けします。`まで表示、CTA本文60px・2行、右40〜45% reserved、ロゴ／疑似登録アイコンなし。
- 動画QA: PASS。336.870秒、H.264 1920×1080 30fps、AAC 48kHz mono、デコード／黒画面／想定外の長時間無音のblocking指摘なし。代表フレームは `work/qa_frames_draft_v2/`。
- 人間再確認待ち: 発音4箇所（信用・今だけ・188・0570-050588）とCTA全文。finalize、thumbnail、`final/final.mp4`、YouTube upload、End Screen実設定は未実施。

## Phase B draft_v3（2026-09-05・信用の人間承認イントネーション再修正）

- `output/draft_v2.mp4`を入力に、Episode008内の「信用」全3segment（006 / 011 / 059）だけを再生成し、`output/draft_v3.mp4`を作成。draft_v1/v2は上書きしていない。
- 辞書は旧accent-only挙動を置き換え、`信用 → シンヨオ`の1 approved entryへ統合。`low_high_plateau`（シ低→ン高→ヨ高→オ高）を`/mora_data`後に適用し、連続するオ・オはpitch差0.0へ揃える。provenanceはEpisode008 human review・2026-09-05・添付VOICEVOX手動調整。
- context query（信用しない／信用する／信用を）を保存。各contextでfirst low・second rise・later plateau PASS、信用をのO-O pitch delta 0.0。
- 音声は再生成3件、draft_v2から60件をhash cache reuse。本編321.868秒。preview WAV・audio_query・pitch QAは `work/phase_b_review/pronunciation_fix_v3/`。
- 今だけ・188・0570-050588字幕・CTA全文・Visual Gate v5は変更なし。v2の字幕SRT/ASS/timingとハッシュ一致、subtitle regression 0。
- 動画QA: PASS。336.870秒、H.264 1920×1080 30fps、AAC 48kHz mono、decode error 0・black frame 0・unexpected silence 0・visual regression 0。
- 人間が聞くtimestamp: 約00:00:26、00:00:41〜00:00:45、00:04:58〜00:05:02。最終承認待ち。finalize、thumbnail、`final/final.mp4`、YouTube upload、End Screen実設定は未実施。

## Final・thumbnail確定（2026-09-05）

- draft_v3を人間承認済みとして確定し、`output/final.mp4`を`draft_v3.mp4`からbyte-identical copy（再encodeなし）で作成。SHA-256: `92166d59c228baff67ad32280899066ad050ff6c715646d773427ccba04f2854`。
- ユーザー提供サムネイルを正式採用。原本は`assets/thumbnail/thumbnail_source.png`、正式画像は`assets/thumbnail/thumbnail.png`（1280×720、16:9）。A/B/C候補・imagegen_native再生成なし。
- thumbnail QAはPASS。25%版は`work/thumbnail_review/thumbnail_25.png`。原本・正式画像のSHAとQAは`work/thumbnail_review/thumbnail_qa.json`に記録。
- metadataはselected title、descriptionの主要根拠URL、VOICEVOXクレジット、`contains_synthetic_media=true`を確認。AI開示の最終確定は公開時に人間判断。
- 警察庁の最新統計watchは2026-09-05時点で令和8年7月末・暫定値。令和8年8月末統計の新規掲載なし。公開直前に再確認する。
- End Screen予定はRELATED VIDEO: Episode004 ニセ警察詐欺、SUBSCRIBE: チャンネル登録。実設定は未実施。
- final QA: `work/final_qa.json` / `output/review/final_qa.md`。YouTube upload、schedule/public、thumbnail upload、End Screen実設定は未実施。


## Visual Gate v2（2026-09-05・人間レビュー反映）

- 人間レビュー「白背景のスライドが多く、PowerPointの素の資料のよう」を受け共通デザイン改善を実施。情報は増やしていない。
- **共通Background Systemを新設**: `config/visual_theme.json`（profile: adult_digital_soft_background）＝ 白一色禁止・soft gradient・左上section pill（52px）・淡いcircle/dots/accent line・semantic icon plate・セクション別accent（caution=淡amber・数字scene=淡panel・list=淡rounded card・compare=薄いdepth）。scene_renderer.pyへ自動適用（--theme auto|none）。恒久ルール化（AGENTS.md・templates/scenes/README.md）。
- template 13scene再render・SCENE-015ヘッドライン80px以上へ短縮・SCENE-005に淡panel。
- QA v2: **FAIL 0 / WARN 0・tiny_text 0・overflow 0・text_asset_overlap 0・underused_whitespace 0・blank_white_slide 0件（template最大55%）・見出し最小83px**。imagegen_native 5枚は標準ハイブリッド経路で採用済み完成背景を配置し、自動exact text QAはauto_fail 0（既存目視PASS版の最終確認はhuman Gate 2）。
- 成果物: `work/visual_review/scene_contact_sheet_v2.png`（旧は上書きしない）・`design_before_after.png`（10シーン比較）・`before_render/`（--theme none）。
- 次のゲート: Gate 2（contact sheet v2＋pronunciation REVIEW）→ Phase B（VOICEVOX・draft・thumbnail）。

## Visual Gate v3（2026-09-05・ユーザー提供背景版）

- ユーザー提供 `assets/background.png`（1672×941）を元画像として保持し、`assets/backgrounds/adult_digital_soft_v2.png`へ縦横比維持のcover＋LANCZOSで1920×1080正規化。Episodeの`visual_theme`を`adult_digital_soft_image_bg`へ変更。
- template 13sceneを`work/rendered_final_scenes_v3/`へ再render。画像内の既存装飾を優先し、巨大circle・dots・leaf/wave・背景tint・大きな自動icon backing・全体amber washを無効化。section pill・semantic icon・最小accent line・字幕安全帯だけを追加。
- icon plateは214px、iconは180px、中心差0px。listはpale blue-white card、SCENE-005は単一panel、SCENE-015は比較カード維持＋見出し85px級。
- QA: **18 OK / 0 WARN / 0 FAIL**。tiny_text 0 / overflow 0 / text_asset_overlap 0 / icon_plate_misalignment 0 / double_decoration 0 / blank_white_slide 0 / TV readability PASS / background consistency PASS / subtitle safe area PASS。
- native 5scene（SCENE-001/004/006/008/013）は再生成せず、v2出力とSHA-256一致。出力: `work/visual_review/scene_contact_sheet_v3.png` / `background_before_after.png` / `visual_gate_v3_qa.md`。
- 停止: ユーザーのcontact sheet確認待ち（Gate 2）。VOICEVOX、draft/final、thumbnail、YouTube操作は未実施。

## Visual Gate v4（2026-09-05・中央軸／section pill／不要文字の局所調整）

- v3のユーザー提供背景は変更せず、`adult_digital_soft_image_bg` を継続使用。元画像・normalized assetともSHA-256はv3記録から不変。
- template 13sceneから常設チャンネル名を削除。imagegen_native 5sceneは再生成せず、既存画像をそのまま維持。
- section pillは全template 13sceneを左上へ復帰（x=90 / y=58）。hero系semantic icon・plate・headline・support・panelは中央軸x=960へ整列。
- SCENE-005は数字panelと下部message panelを同じ幅1220px・center_x=960へ統一。SCENE-003/016/017/018のlist cardは左右150pxで中央配置、SCENE-015はカード幅790px・gap120px・pair center_x=960。
- QA: 18 OK / 0 WARN / 0 FAIL。tiny_text 0 / overflow 0 / text_asset_overlap 0 / channel_name_in_scene 0 / icon_plate_misalignment 0 / visual_axis_alignment PASS / stacked_panel_alignment PASS / section_pill_anchor PASS / subtitle_safe_area PASS / background_consistency PASS / TV_readability PASS。
- 出力: `work/rendered_final_scenes_v4/`、`work/visual_review/scene_contact_sheet_v4.png`、`work/visual_review/alignment_before_after.png`、`work/visual_review/visual_gate_v4_qa.md`、`work/visual_review/scene_quality_report_v4.json`。
- 停止位置: 人間Gate 2（v4 contact sheet＋pronunciation REVIEW）待ち。VOICEVOX、draft/final、thumbnail、YouTube操作は未実施。

## Visual Gate v5（2026-09-05・上部semantic icon可視グリフ中心の局所修正）

- v4の上部semantic iconだけを修正。元の512px PNGは透明余白を含み、可視グリフ中心x=192／キャンバス中心x=256（差-64px）だったため、全canvas縮小時に可視グリフが約22.5px左へずれていた。
- 元SVG/PNGは変更せず、alpha threshold=4で可視bboxをtrimし、アスペクト比を維持して180×180pxの固定visual boxへcontain配置。正規化cacheは `assets/icons/material_symbols_normalized/`。
- SCENE-002/005/007/009/010/011/012/014の最終render pixel/bboxを再計測。可視グリフのx軸差は最大0.5px、glyph−plate差は最大0.5pxで、`semantic_icon_visual_center` PASS（閾値4px／2px）。
- v4の背景、section pill（x=90 / y=58）、headline、support、panel/list、SCENE-005下部message panelは保持。background SHA-256は不変、native 5sceneはv4/v5 SHA-256一致。
- QA: **18 OK / 0 WARN / 0 FAIL**。tiny_text 0 / overflow 0 / text_asset_overlap 0 / channel_name_in_scene 0 / icon_plate_alignment PASS / visual_axis_alignment PASS / stacked_panel_alignment PASS / section_pill_anchor PASS / SCENE-005 panel regression 0 / background regression 0。
- 出力: `work/rendered_final_scenes_v5/`、`work/visual_review/scene_contact_sheet_v5.png`、`work/visual_review/icon_alignment_before_after.png`、`work/visual_review/visual_gate_v5_qa.md`、`work/visual_review/scene_quality_report_v5.json`。
- 停止位置: **人間Gate 2（上部semantic iconのvisual center最終確認）待ち**。VOICEVOX、draft/final、thumbnail、YouTube操作は未実施。

## Phase B開始（2026-09-05・Visual Gate v5人間承認）

- `human_visual_approved=true`、`visual_gate_version=v5`を確定。ユーザー提供背景、template 13scene、imagegen_native 5scene、section pill左上、本文中央軸、semantic icon visual center修正版、SCENE-005 panel整列、チャンネル名overlay削除、tiny_text 0、overflow 0、icon alignment PASSを固定し、明確な不具合以外のデザイン再変更は行わない。
- 視聴者想定を「50〜60代中心」から「60代以上を中心に、特に65歳以上でも無理なく見聞きできる」へ更新。文字を小さくしない、数字を聞き取りやすくする、専門語を詰め込まない、1画面1メッセージ、字幕原則60px以上をPhase B QAへ適用。
- Fact Check最終: **FAIL 0 / REVIEW 0**。SEG50の「やり取りの画面は消さずに残す」は警察庁SRC-018で確認。8月末統計の新規公表確認は公開前watchとして別管理。
- Phase Bの停止目標: VOICEVOX全segment、pronunciation QA、実測subtitle、Visual v5使用draft_v1、draft QA、代表フレームまで。final、thumbnail確定、YouTube upload、End Screen実設定は行わない。

## Phase B完了（2026-09-05・draft_v1）

- VOICEVOX「剣崎雌雄 / ノーマル」で63/63 segmentを生成。`audio/voicevox_kenzaki/narration_kenzaki_auto.wav` は実測321.804秒。CTAは11.563秒＋余韻3.437秒で15秒に整合。
- 字幕は122 cue。46 segmentを意味の切れ目で分割し、segment境界は実測WAV、分割cue境界はVOICEVOX `audio_query` mora durationで決定。最小72px、3行0、保護語/活用語の不自然分断0。
- Visual Gate v5の18sceneを入力に `output/draft_v1.mp4` を作成。実測336.803秒、H.264 1920x1080 30fps、AAC 48kHz。Phase 2 QAはPASS（FAIL 0 / WARN 0）。
- `work/qa_frames_draft_v1/` に18scene＋CTAの19代表フレームとcontact sheetを保存。背景・native scene・semantic iconの回帰なし。Scene 007のみ、文言を変えず意味の切れ目で改行する局所修正を反映。
- senior readability: **REVIEW**（機械QA PASS、全編の人間視聴待ち）。thumbnail確定、`final/final.mp4`、YouTube upload、End Screen実設定は未実施。

## YouTube publication
- youtube_upload: uploaded_scheduled
- youtube_video_id: GryqJ70DCHs
- youtube_url: https://youtu.be/GryqJ70DCHs
- youtube_privacy: private
- youtube_scheduled_at: 2026-09-08 19:00:00 JST
- youtube_scheduled_at_api: 2026-09-08T10:00:00Z
- thumbnail_uploaded: true
- uploaded_at: 2026-09-05T03:57:31Z
- youtube_channel_id: UCgVRceTJYO5KOrPX4w2jXZw
- youtube_schedule_verification: PASS（videos.list: publishAt=2026-09-08T10:00:00Z）
- youtube_thumbnail_verification: PASS（thumbnails.set・hasCustomThumbnail=true）
- youtube_metadata_verification: PASS（title・channel ID・privacyStatus）
- youtube_reupload: false
- youtube_ai_disclosure: true
- youtube_ai_disclosure_updated_at: 2026-09-05T04:00:24Z
- youtube_ai_disclosure_verified: true
- youtube_ai_disclosure_verification: videos.update response; videos.list omitted containsSyntheticMedia
