# Episode 009 QC（Final / YouTube予約公開）

確認日: 2026-09-05

## Gate status

`SCHEDULED_PRIVATE`

## Final artifact QA

- `output/final.mp4`: draft_v3からcopy-only、byte-identical **PASS**
- SHA-256: `e4e181b9a264f00bae04673352bf88676c47982508fcfe6de4b73ad5c825fc70`
- 28,770,325 bytes / 304.880秒 / H.264 1920×1080 30fps / AAC 48kHz
- decode 0 / black 0 / unexpected narration silence 0
- visual regression 0 / subtitle regression 0 / privacy 0 / CTA regression 0
- pronunciation unresolved 0 / fact FAIL 0 / fact REVIEW 0
- `senior_readability=PASS`
- 詳細: `work/final_qa.md` / `work/final_qa.json`

## Fact / policy

- Fact重大指摘: 0件（`fact_check.md`）
- 主要事実の一次情報URL: あり
- Windows 11実機画面の誤用: なし（現PCはWindows 10、公式画面のみ採用）
- AIによる公式UI再現: なし
- 概念ImageGen scene: 3枚。`text_qa.py`のexact text自動判定は3/3 PASS。Visual Gate v2で人間承認済み
- Visual Gate v2: SCENE-006 / 007 / 009のみを局所修正。他sceneのPNGは上書きしていない
- thumbnail: ユーザー提供画像を正式採用。原本・公開用normalize・25%確認版・QAを保存
- thumbnail QA: 1280×720 / 16:9 / decode / text / edge / 25% readability / Fact Boundary / privacy PASS
- YouTube: `NO4ZwXPvgA0`へ非公開アップロード、サムネイル設定、2026-09-09 19:00 JST予約、API verify PASS
- AI開示: `contains_synthetic_media=true`をscheduled upload時に反映・検証

## Final Fact Watch

- Microsoft公式の24H2 / 25H2 / 26H1とエディション差を2026-09-05に再確認。`work/fact_watch_final.md`。
- Lifecycleページの終了時刻表示差は記録済み。release-healthの明示日付に基づき、動画の`2026年10月13日`は変更しない。

## Phase B results

- Visual Gate v2: 人間承認済み。19sceneを固定し、draftで回帰なし
- Fact Check最終: FAIL 0 / REVIEW 0
- VOICEVOX v3: 2 segment（006 / 038）regenerated / 50 reused、剣崎雌雄・ノーマル、speedScale 1.00 / intonationScale 1.00 / pitchScale 0.00
- narration: 52 segment、289.880秒（pause込みの実測タイムライン）
- script wording: segment006「考え方」→「考えるポイント」、segment038「24H2の方は」→「24H2の場合は」。発音overrideではなく台本文言を変更
- pronunciation QA v3: Windows / Update / ID / 24H2 / 25H2 / 26H1 PASS。`方` global dictionary entryなし
- subtitles: 59 cue、最小72px、subtitle preflight PASS（font below 56 = 0 / overflow = 0 / 3-line = 0 / protected term split = 0 / tts_reading_leakage = 0）
- CTA: `channel_common_cta`、画面15秒、音声11.563秒＋余韻3.437秒、`cta_full_text_visible = PASS`
- draft_v1: `output/draft_v1.mp4` は保持。上書きなし。
- draft_v2: `output/draft_v2.mp4`は保持。上書きなし。
- draft_v3: `output/draft_v3.mp4`、304.880秒、H.264 1920×1080 30fps、AAC 48kHz
- draft_v3 QA: PASS（decode returncode 0 / black frame 0 / unexpected silence 0 / scene 19 / subtitle 59 / Visual Gate v2 regression 0 / official UI PASS / privacy PASS / CTA PASS）
- chapter / scene timeline / CTA start: 実測音声に合わせ再計算。chapter `01:08 / 01:55 / 02:52 / 03:55 / 04:29`、CTA start `289.880s`
- representative frames: 指定17件を `work/qa_frames_draft_v1/` に保存

## Pronunciation-only v2

- `方`: segment 001 / 011 は `かた`、segment 006 / 038 は `ほう`。global辞書登録なし。
- `方`の局所指定: segment 001 / 011 は人を指すため `かた`、segment 006（考え方）/ 038（24H2の方）は `ほう`。
- `Windows`: segment 001, 002, 004, 005, 008, 009, 014, 020, 022, 023, 025, 037, 039, 047, 049, 050。読み `ウィンドオズ`、accent=5、語末ズ。
- `Update`: segment 005, 022, 023, 037, 039, 047, 050。読み `アップデエト`、accent=6、語末ト。
- `ID`: segment 019のみ。読み `アイディイ`（VOICEVOX上の表記）、accent=3、ディを核。表示字幕の `ID` は変更なし。
- 字幕表示文言（Windows / Windows Update / ID / 24H2 / 25H2 / 26H1）、Visual Gate v2、公式UI crop、CTAは変更なし。

## Script wording v3

- 恒久ルール `ambiguous_方_avoidance`を`AGENTS.md`へ追加。`ambiguous_kanji_pronunciation` preflightでscript.mdと全52 narration segmentをscan。
- 変更後のnarration内の「方」は2件: segment001（A / REVIEW）、segment011（D / REWRITE候補）。人間指摘の2箇所以外は改稿せず、一覧を`work/phase_b_review/ambiguous_kanji_pronunciation_v3.md`へ保存。
- target checks: segment006 / 038とも、旧文言消失・新文言のnarration/字幕一致をPASS。
- 字幕は新文言を反映し、SUB-006 / SUB-038を実測タイミングで再構築。非対象SUB-031-2は表示内容を変えず2行へ整形し、既存のoverflow候補を解消。

## Visual Gate checklist

|項目|結果|根拠|
|---|---|---|
|blank_white_slide|PASS|該当sceneなし|
|scene quality report v2|19 OK / 0 WARN / 0 FAIL|`scene_quality_report_v2.md`|
|tiny_text（44px未満）|PASS|templateの情報文字をrenderer規約で作成|
|headline|PASS|headlineは80px以上のlayoutを使用|
|SCENE-006 official_ui_legibility|PASS|「バージョン情報」focus crop＋操作step|
|SCENE-006 action_clarity|PASS|設定→システム→バージョン情報、highlight 1箇所|
|SCENE-007 version_field_legibility|PASS|公式crop＋「バージョン（例）」の別レイヤー|
|SCENE-007 privacy|PASS|device name / ID / product ID / serial / 個人名を非表示|
|SCENE-009 windows_update_legibility|PASS|公式button cropを右側へ拡大|
|SCENE-009 action_clarity|PASS|設定→Windows Update＋日本語補助ラベル|
|公式画面の可読性|PASS|v2 contact sheetと元画像を人間確認済み|
|個人情報|PASS|採用cropはPIIなし。個人情報を含む一時原画は2026-09-05に削除済み|
|semantic icon|PASS|visual center / plate alignmentの機械検査PASS|
|subtitle safe area|PASS|全sceneの下部180pxをrendererで確保|
|visual axis / panel alignment|PASS|v4/v5機械検査PASS|
|target scene visual balance|PASS|SCENE-006 / 007 / 009の公式UI占有率を改善|
|CTA reserved area|PASS|動画側は変更なし。YouTube Studioの実設定は未着手|

## 残る人間確認

- YouTube StudioでEnd Screen（関連動画TBD＋チャンネル登録）を人間設定する。
- 予約時刻前にYouTube Studio表示を最終確認する（動画は予約時刻まで非公開）。

## 停止位置

- `senior_readability=PASS`。Final、サムネイル、publish dry-run、非公開アップロード、予約、API verifyまで完了。
- 即時public化は未実施。End Screen実設定のみ未完了。
