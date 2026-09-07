# Episode 009 STATE

- Episode: 009 / `windows11_24h2_support`
- 現在地: **Episode 009 YouTube予約公開済み（非公開）**
- 状態: `SCHEDULED_PRIVATE`
- status: scheduled_private
- human_approved: true
- approved_draft: draft_v3
- 最終更新: 2026-09-05

## 完了

- Microsoft公式情報の調査と `sources.md` / `research.md` の作成
- `fact_check.md` の主要Fact判定（重大指摘0件）
- `episode.json`、`script.md`、`publish.json` の初版
- `scene_plan.json`、`shotlist.md` の作成
- Microsoft公式画面の個人情報を含まないcrop素材の準備
- Windows 11実機capture方法の設計（現PCはWindows 10のためblocked）
- 概念scene 3枚を生成し、`text_qa.py`のexact text自動判定3/3 PASS
- 19sceneを再レンダーし、contact sheet v1とscene quality reportを更新（17 OK / 2 WARN / 0 FAIL）
- semantic icon center、visual axis、panel alignment、subtitle safe areaの機械検査PASS
- SCENE-006 / 007 / 009のみを局所修正。公式UIを拡大し、step・highlight・日本語補助を追加
- `scene_contact_sheet_v2.png` と `scene_006_007_009_before_after.png` を作成
- Visual Gate v2の機械検査は19 OK / 0 WARN / 0 FAIL
- canonical参照0件を確認後、個人情報を含む一時原画 `assets/official/_source_tmp/devicenameandmodel.png` を削除
- Visual Gate v2は人間承認済み（19scene、19 OK / 0 WARN / 0 FAIL）
- Fact Check最終確認（FAIL 0 / REVIEW 0）
- VOICEVOX: 剣崎雌雄・ノーマル、52 narration segmentを生成（再利用0）
- 24H2 / 25H2 / 26H1は表示文字を維持し、TTSだけ読みを補正
- pronunciation preview（11語）とaudio_query/WAVを `work/phase_b_review/pronunciation/` に保存
- 字幕59 cueをVOICEVOX実測時間から生成。SRT/ASSのsubtitle preflightはPASS
- 共通CTA画面・音声を生成し、CTA全文表示QAはPASS
- `output/draft_v1.mp4` を生成し、decode・黒画面・無音・仕様・Visual Gate回帰QAはPASS
- 指定17代表フレームと `work/qa_frames_draft_v1/contact_sheet.png` を作成

## Phase B v2（発音のみ局所修正）

- draft_v1は上書きせず保持。字幕59 cue、Visual Gate v2の19scene、CTA画面・音声は変更なし。
- `方` は segment 001 / 011 の人を指す用法だけ `かた`、segment 006 / 038 は `ほう` のまま。`方` のglobal辞書登録はなし。
- `Windows`（16出現）、`Update`（7出現）、`ID`（segment 019）を承認済みのVOICEVOX読み・アクセントへ局所補正。最終的な発音差分は20segment、32segmentは再利用。
- 発音preview 5種と各audio_query JSONを `work/phase_b_review/pronunciation_fix_v2/` に保存。
- 実測音声から字幕タイミングを再構築し、字幕内容は変更なし。`output/draft_v2.mp4` を生成。
- draft_v2 QA: PASS（304.30秒、H.264 1920x1080 30fps、AAC 48kHz、decode / black / silence / Visual Gate v2 regression / official UI / privacy / CTA PASS）。
- `senior_readability=REVIEW`。発音previewとdraft_v2の全編人間確認が完了するまで、final・thumbnail・upload・schedule/public・End Screen設定へ進まない。

## Phase B v3（台本文言の局所修正）

- draft_v1 / draft_v2は上書きせず保持。人間レビューの2箇所だけ、発音overrideではなく台本文言そのものを変更。
- segment 006（約00:30）: 「三つ目、更新が表示されないときの考え方です。」→「三つ目は、更新が表示されないときに考えるポイントです。」
- segment 038（約03:29）: 「24H2の方は、まず25H2が表示されるかを確認してください。」→「24H2の場合は、まず25H2が表示されるかを確認してください。」
- VOICEVOXは変更した2segment（006 / 038）だけ再生成し、他50segmentをcache reuse。Windows / Update / ID / 24H2 / 25H2 / 26H1の発音QAはPASS。
- `script.md`、`episode.json` narration/display、SUB-006 / SUB-038を一致させ、字幕59cueを実測音声から再構築。minimum72px、font<56=0、overflow=0、3-line=0、TTS leakage=0。
- 実測尺: narration 289.880秒、CTA start 289.880秒、draft_v3 304.880秒。chapterはscene開始に合わせ `01:08 / 01:55 / 02:52 / 03:55 / 04:29`へ更新。
- Visual Gate v2の19scene、SCENE-006 / 007 / 009、CTA画面・音声は変更なし。contact sheet hash回帰0、PII temporary source / canonical reference 0。
- `ambiguous_kanji_pronunciation`で全52segmentをscan。変更後のnarration内「方」はsegment001（A / REVIEW）とsegment011（D / REWRITE候補）の2件で、今回は改稿せず一覧化。
- `output/draft_v3.mp4`と`work/draft_v3_qa.md`を作成。QAはPASS、`senior_readability=REVIEW`。

## Phase C — Final・公開メタデータ準備（2026-09-05）

- draft_v3は人間全編レビュー承認済み。`human_draft_approved=true`、`approved_draft=draft_v3`、`senior_readability=PASS`を記録。
- 非対象の「方」2件（segment001 / 011）は全編レビュー後に`APPROVED`へ解決。未解決発音0、`方`のglobal辞書登録なし。恒久ルール`ambiguous_方_avoidance`は維持。
- Microsoft公式Fact Watchを再確認。24H2 Home / Pro系の更新終了日2026-10-13、25H2、26H1、Windows 11全体ではないことを確認し、台本・動画は変更なし。
- `output/final.mp4`を`output/draft_v3.mp4`からcopy-onlyで作成。SHA-256一致、再エンコードなし。304.880秒、H.264 1920×1080 30fps、AAC 48kHz。
- Final QA: decode 0 / black 0 / unexpected silence 0 / visual regression 0 / subtitle regression 0 / privacy 0 / CTA regression 0 / pronunciation unresolved 0 / fact FAIL 0 / fact REVIEW 0。**PASS**。
- `publish.json`を選択タイトル、description、実測chapters、VOICEVOXクレジット、category_id=22、default_language=ja、made_for_kids=false、AI開示、End Screen予定、予約公開結果まで反映。
- `work/thumbnail_brief.md`、`work/analytics_plan.md`、`work/pre_publish_checklist.md`を作成。
- ユーザー提供サムネイルを `assets/thumbnail/thumbnail_source.png` に原本保存し、`assets/thumbnail/thumbnail.png` を1280×720へ最小crop・LANCZOS normalize。
- サムネイル25%確認版と `work/thumbnail_review/thumbnail_qa.json` を作成。主コピー、Fact Boundary、文字切れ、privacyをPASS。

## 公開後も未実施・要手動設定

- YouTube StudioのEnd Screen実設定（関連動画TBD＋チャンネル登録）

## Human Gate（履歴）

1. 台本とFact境界: 24H2の対象エディション、2026-10-13、25H2、26H1の説明を確認。
2. v2 contact sheetとbefore/afterで、SCENE-006 / 007 / 009の文字・構図・公式UIの可読性を確認。
3. 公開前にMicrosoft公式ページを再確認し、必要ならWindows 11実機captureへ差し替える。
4. draft_v3を最初から最後まで視聴し、24H2 / 25H2 / 26H1の聞き分け、速度、字幕、006→007→009の操作導線を確認する。
5. 約00:27.379（segment006）と約03:24.944（segment038）前後で、変更後の自然な文言と字幕同期を確認する。
6. `work/phase_b_review/pronunciation_fix_v2/` の5種previewとdraft_v3で、Windows / Update / ID / 24H2 / 25H2 / 26H1の読みを確認する。`ambiguous_kanji_pronunciation_v3.md`の非対象2件は今後の再発防止レビュー用に確認する。

## 停止位置

`senior_readability=PASS`。Final・サムネイル・publish dry-run・非公開アップロード・2026-09-09 19:00 JST予約・API検証まで完了。動画は予約時刻まで非公開。即時public化は行わない。End Screenの実設定のみYouTube Studioで要手動確認。

## YouTube publication
- youtube_upload: uploaded_scheduled
- youtube_video_id: NO4ZwXPvgA0
- youtube_url: https://youtu.be/NO4ZwXPvgA0
- youtube_privacy: private
- youtube_scheduled_at: 2026-09-09 19:00:00 JST
- youtube_scheduled_at_api: 2026-09-09T10:00:00Z
- thumbnail_uploaded: true
- uploaded_at: 2026-09-05T11:20:10Z
- youtube_channel_id: UCgVRceTJYO5KOrPX4w2jXZw
- publish_dry_run: PASS
- api_verify: PASS
- contains_synthetic_media: true
