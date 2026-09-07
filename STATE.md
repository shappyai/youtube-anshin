# Project state

- Phase: 0 → 1（1〜3本で制作型を固定する段階）
- Channel: 大人のデジタル安心室
- Brand: 怖がらせる前に、確認する。
- Current episode: `012_phishing_message_safety`
- 001 sources: Google公式ヘルプ8ページを2026-08-29に本文確認済み（URL 6294825 は「不正使用されたアカウントを保護する」ページと判明、デバイス確認専用ページ 3067630 を追加）
- 001 script: v0.2（想定尺 約10分・冒頭20秒結論・SHOTタグ5個）
- 001 shotlist: v0.2（台本と同期、画面名称の当日確認リスト付き）
- 001 publish.json: 章立て・公式URL8件・タイトル案4件を同期済み
- 001 raw: SHOT-01（37秒）・SHOT-02（44秒）・SHOT-02B（40秒・再設定用メール）・SHOT-03（24秒）・SHOT-04（27秒）・SHOT-05（82秒メタデータ）を全6素材日本語UIで撮影済み（2026-08-29）。script.md/shotlist.md 対比で素材不足なし → 「C. 撮影後」へ進める状態
- 001 空テイク・旧テイク（19KB など）は raw/ にバックアップ名で残置（削除していない）
- 001 draft: `output/draft.mp4` 生成済み（410.1秒・1920x1080 h264・aac・字幕焼き込み・モザイク済み・TTS=6分50秒 gpt-4o-mini-tts/coral）。モザイク済み中間材は work/、素材rawは不変
- 001 draft_v2: `output/draft_v2.mp4` 生成済み（502.5秒・8:22・冒頭5項目カード＋各セクション見出し＋左情報パネル/右スマホ画面・要点テロップ方式・逐文TTS＋実測字幕同期・2:10相当のChromeメニュー除去済み）。v1は残置
- 001 draft_v3: `output/draft_v3.mp4` 生成済み（509.7秒・8:30・全字幕焼き込み（ASS・下部帯・Yu Gothic・スマホと非重複）・スマホ中央寄せ・見出し完全中央・冒頭ビジュアル（intro_visual.png）・エンディングCTA＋CTAナレーション追加・ナレーション/間/音量はv2維持）。未公開。レイアウトのテンプレート化は人間合格まで保留
- 001 draft_v4: `output/draft_v4.mp4` 生成済み（518.8秒・8:39・冒頭はユーザー提供 intro_visual_v4.png（イメージ注記付き）・字幕は52px太字+縁3+濃ネイビー帯 y890-1080・まとめは実タイミングで5画面＋締めに切替・エンドカード約9.6秒＋フェードアウト）。v1〜v3・raw・work は不変。未公開
- 001 draft_v5: `output/draft_v5.mp4` 生成済み（518.8秒・字幕は{\an5\pos(960,985)}で帯内縦中央固定・描画幅ベースで28本を自然2行化＋1本をイベント分割・冒頭画像はy0-890に収め字幕帯と分離・エンドカードはチャンネルロゴ（work/channel_logo_google.png・差し替え可）を使用）。未公開
- 001 draft_v6: `output/draft_v6.mp4` 生成済み（518.9秒・字幕は禁則処理（行頭句読点禁止・語途中禁止）＋安全幅1550px・2行化37本＋イベント分割3件・本編は説明連動のズーム（計11区間・1.3〜1.7倍）＋青枠ハイライト（11区間））。未公開
- 001 draft_v7: `output/draft_v7.mp4` 生成済み（513.8秒・スマホ全体表示を維持し、左右余白に拡大インセット（角丸カード・青枠・シャドウ・11区間）＋スマホ側青枠ハイライト・字幕62px（帯900-1080・縦中央990）・1:55の過剰説明（「再設定」の意味解説）を削除して音声/タイムラインを再構築・エンドカードはロゴ拡大＋名称テキスト重複削除）。未公開
- 001 draft_v8: `output/draft_v8.mp4` 生成済み（513.6秒・8:34・インセット全撤去・スマホ常時全体表示・視線誘導はタップリップル（青系・0.9秒）＋短時間青枠のみ・字幕72px（帯y885-1080・縦中央{\an5\pos(960,980)}・最大幅1780px・2行化＋イベント分割・禁則処理維持）・字幕タイミングはPCM実測（24000Hzサンプル数）ベースで再構築（work/retime_v8.py → timeline_v8.json → captions_v8.srt/.ass）・音声は narration_v6.mp3（513.644秒）と完全同期）。v7以前・raw・work は不変。未公開
- 001 v8補足: 字幕ズレ原因は旧タイムライン（ビットレート推定尺の累積誤差・秒丸め）と実音声の乖離。v8は各TTSユニット/無音/CTAをPCM f32le 24000Hzへデコードしサンプル数で時刻を決定。ハイライト/リップルのキャンバス座標（スマホ設置オフセット770,12加算）も修正済み
- 001 draft_v9: `output/draft_v9.mp4` 生成済み（513.6秒・8:34・映像構図を全面変更：青枠/リップル全撤去・構図は「全体画面(full)/1項目の大きな切り抜き(crop)/2項目の左右2カラム(two)」の3種のみ・モザイク済み work/s0X_*.png から説明対象UIを切り抜いて映像領域に拡大配置・字幕/音声はv8を完全維持（captions_v8.ass・narration_v6.mp3）・work/build_v9.py 実装）。v8以前・raw・work は不変。未公開
- 001 VOICEVOX採用: ナレーションを VOICEVOX「剣崎雌雄」（style_id=21 ノーマル・speed 1.00/intonation 1.00/pitch 0.00・1文ずつ生成）へ暫定→本採用。segment 001〜079.wav + segments_manifest.csv + narration_kenzaki_final.wav（396.77秒＋エンドカード無音8秒＝404.77秒）。発音辞書 config/voicevox_pronunciation.yaml（開けます→ひらけます／セキュリティ→セキュリティー／Gmail→ジーメール／再設定用 2句・再改定1句等・方向4語）
- 001 draft_v10: `output/draft_v10.mp4` 生成済み（404.77秒・6:45・v9の映像デザイン継承＋VOICEVOX実タイムラインへ全面再配置・全体画面2〜4秒ルール適用・字幕 captions_v10.ass を実尺で再計算・work/build_v10.py）。v9以前・raw・work・OpenAI音声は不変
- 001 最終採用: draft_v10 を人間確認し **85/100** で1本目の完成版として採用（2026-08-30）
- 001 final: `output/final.mp4`（draft_v10 の単純コピー・SHA256一致 E33363E3F2ED1EE68B92209331D7668AD63F7A3CBE20387392E75476C671B2DC）
- 001 publish準備: タイトル候補5案・推奨1案・概要欄・チャプター（VOICEVOX実タイムライン）・固定コメント・publish.json（visibility: private）・pre_publish_checklist.md を作成（publish/ 配下）。サムネイルは人間指定の final/thumbnail.png をそのまま使用（自働生成案は work/discarded_thumbs/ に退避・未採用）
- 001 capture: `scripts/capture_android.py` 実装済み（固定環境向け最小版）。座標は capture_coords.json、プライバシー対象は privacy_mosaic_targets.json に記録
- 環境: Python 3.14.3（C:\Users\user\AppData\Local\Programs\Python\Python314）・ffmpeg 8.1.1（winget）。PyYAML 未導入のため doctor.py 等の yaml 依存スクリプトは要 pip install pyyaml
- TTS: 本編は VOICEVOX 剣崎雌雄（standard）に決定。OpenAI TTS（gpt-4o-mini-tts）はフォールバック/比較用として残置（削除しない）
- Final video: `episodes/001_google_security/output/final.mp4`（draft_v10 のコピー・85/100採用）
- Thumbnail: `final/thumbnail.png`（人間指定・採用・生成物は使わない）
- 標準ナレーター: VOICEVOX 剣崎雌雄（ノーマル・speed 1.00 / intonation 1.00 / pitch 0.00・1文ずつ生成・segment単位WAV・1文差し替え可能）→ AGENTS.md に反映
- 映像制作ルール確定（全体画面2〜4秒・読ませるUIは拡大・字幕72px下部帯・媒体選択工程など）→ AGENTS.md / templates/ に反映
- 002_myna_app 編集完了: `output/draft_v4.mp4` 生成、映像・字幕・テンポは人間レビュー承認済み（映像80/100、テンポOK、字幕OK）
- 002_myna_app 最終発音修正: `開けない → ひらけない` を人間承認済みの完全一致辞書として追加し、segment 047のみ再生成。`方 → かた`、`後から → あとから`、App Store「アップストア」は維持
- 002_myna_app final: `output/final.mp4` はdraft_v4のSHA256一致コピーとして確定。status: 公開準備完了（YouTube未アップロード・未公開）

## Next action
Episode012: YouTube予約公開済み。動画ID `CzTNLyAn1lY`の`privacyStatus=private`・2026-09-12 19:00 JST予約をAPI検証済み。次はYouTube StudioでEnd Screen（Episode004関連動画・チャンネル登録）を人間設定する。

## Episode 005 — Phase A（2026-09-01）

- Episode 005 `google_photos_delete`「【Googleフォト】写真を消して大丈夫？「削除」と「空き容量を増やす」の違い」のPhase Aを完了（詳細は `episodes/005_google_photos_delete/STATE.md`）。
- 一次情報20件を2026-09-01に取得・保存（`local/web_check_005/`）・Fact Check FAIL 0件。
- canonical: brief / sources / script（65セグメント・6〜7分） / shotlist / episode.json（25 scene・schema検証0件） / publish.json / media_manifest.csv / STATE.md。
- subagents 5体（research/title/structure → fact_check/visual の2並列グループ）。成果物は `work/subagents/005_google_photos_delete/`。
- GPT画像5枚のmanifest・scene prompts準備済み（未生成）。Emulator/iPhone素材は未撮影。VOICEVOX・動画・YouTubeは未実施。
- 次アクション: 人間がテーマ・台本・scene planをレビュー（Gate 1）。承認後に画像生成（1 Agent=1 scene=1 image・5並列）とPhase B撮影へ。


## Episode 008 — Visual Gate v3（2026-09-05）

- ユーザー提供 `episodes/008_investment_scam/assets/background.png` を元画像として保持し、`assets/backgrounds/adult_digital_soft_v2.png`へcover＋LANCZOSで正規化。Episode008のtemplate 13sceneへ共通適用する再利用プロファイル `adult_digital_soft_image_bg` を `config/visual_theme.json` に追加。
- v2を上書きせず `episodes/008_investment_scam/work/rendered_final_scenes_v3/`へ再render。native 5sceneは再生成せずv2とSHA-256一致。巨大circle/dots/leaf/wave/background tint/大きな自動icon backing/全体amber washは無効化。
- QA: 18 OK / 0 WARN / 0 FAIL。tiny_text 0 / overflow 0 / text_asset_overlap 0 / icon_plate_misalignment 0 / double_decoration 0 / blank_white_slide 0 / TV readability PASS / background consistency PASS / subtitle safe area PASS。
- 成果物: `episodes/008_investment_scam/work/visual_review/scene_contact_sheet_v3.png`・`background_before_after.png`・`visual_gate_v3_qa.md`。停止位置はユーザーのGate 2確認待ち。VOICEVOX・draft/final・thumbnail・YouTube操作は未実施。


## Episode 008 — Phase A（2026-09-05）

- Episode 008「【投資詐欺】その有名人、本物？LINEに誘導されたら確認したい3つ」のPhase Aを完了（詳細は `episodes/008_investment_scam/STATE.md`）。
- テーマ選定Gate 7軸（trend 5 / age_fit 5 / channel_fit 5 / home_ctr 4 / competition 3 / practicality 5）を記録。公開予定 2026-09-08。
- 一次情報は2026-09-05に公式本文を直接取得（`local/web_check_008/`: 警察庁PDF3・SOS47/金融庁/国民生活センター/消費者庁/LINEヤフーHTML12）。主要数字: SNS型投資詐欺 令和8年7月末暫定値 6,566件（+75.6%）・881.2億円（+88.6%）／上半期1日4.4億円・被害額60代最多／接触後LINE誘導約9割／著名人画像無断使用広告は令和7年7月以降増加顕著。
- canonical一式作成: brief / sources（SRC-001〜017） / script（51セグメント・4:30〜5:30+CTA目標） / shotlist / media_manifest / episode.json（51seg・59sub・18scene・14source・schema検証PASS） / publish.json / fact_check（FAIL 0・REVIEW 2） / STATE。
- Visual Gate候補: imagegen_native 5枚（hero1＋section扉3＋概念1）生成・exact text目視QA PASS。template 13シーン描画。scene_quality_report OK 9/WARN 9/FAIL 0（WARNはcontact sheet人間確認候補）。contact sheet: `episodes/008_investment_scam/work/visual_review/scene_contact_sheet.png`。
- Material Symbols Rounded 10種を公式配布元から取得してtint PNG化し `config/icon_catalog.json` にusage_episode_008を追加。
- 次アクション: 人間がテーマ・台本・visual plan・contact sheetをレビュー（Gate 1）。承認後にPhase B（pronunciation REVIEW 11件→full VOICEVOX→draft→thumbnail→publish）。


## Episode 008 — Visual Gate v2（2026-09-05）

- 人間レビュー（白背景・素の資料感）に対応し、**共通Background System**（`config/visual_theme.json` profile `adult_digital_soft_background`・恒久ルール化）を新設。soft gradient＋section pill＋淡いcircle/dots/accent line＋icon plate＋セクション別accentをrenderer（Pillow/HTML CSS）へ自動適用。白一色禁止。
- template 13scene再render・SCENE-005淡panel・compareヘッドライン80px以上（85px）・listはrounded card・QAにblank_white_slide検査追加。
- QA v2: FAIL 0 / WARN 0・tiny_text 0・overflow 0・text_asset_overlap 0・underused_whitespace 0・**blank_white_slide 0件**。
- 成果物: `episodes/008_investment_scam/work/visual_review/scene_contact_sheet_v2.png`・`design_before_after.png`（10シーン比較）・before_render/（--theme none）。
- 停止: 人間のcontact sheet v2確認待ち（Gate 2→Phase B）。

## Episode 008 — Visual Gate v4（2026-09-05）

- v3のユーザー提供背景を変更せず、template 13sceneへ中央軸・section pill左上・panel整列の局所修正を適用。imagegen_native 5sceneは再生成せず保持。
- 常設チャンネル名overlayをtemplate 13sceneから削除。section pillはx=90 / y=58へ復帰し、hero/icon/plate/headline/support/panelの主要軸をx=960へ統一。
- QA: 18 OK / 0 WARN / 0 FAIL。tiny_text 0 / overflow 0 / text_asset_overlap 0 / channel_name_in_scene 0 / icon_plate_misalignment 0 / visual_axis_alignment PASS / stacked_panel_alignment PASS / section_pill_anchor PASS / subtitle_safe_area PASS / background_consistency PASS / TV_readability PASS。
- 成果物: `episodes/008_investment_scam/work/visual_review/scene_contact_sheet_v4.png`、`alignment_before_after.png`、`visual_gate_v4_qa.md`、`scene_quality_report_v4.json`。次は人間Gate 2。VOICEVOX・draft/final・thumbnail・YouTube操作は未実施。

## Episode 008 — Visual Gate v5（2026-09-05・上部semantic icon可視グリフ中心）

- v4の上部semantic iconの見た目のズレだけを修正。元PNGの可視alpha bbox中心x=192と512pxキャンバス中心x=256の差（-64px）が原因で、全canvas縮小時に約22.5px左へ見えていた。
- 元SVG/PNGは保持し、alpha bbox trim＋アスペクト比維持＋180×180px固定visual boxへの再センタリングを実施。v4の背景、section pill、text/panel/list、SCENE-005下部panel、native 5sceneは不変。
- 最終render pixel/bbox QAでsemantic iconのaxis差最大0.5px、glyph−plate差最大0.5px。`semantic_icon_visual_center`、`icon_plate_alignment`、`visual_axis_alignment`、`stacked_panel_alignment`、`section_pill_anchor`はすべてPASS。18 OK / 0 WARN / 0 FAIL。
- 出力: `episodes/008_investment_scam/work/visual_review/scene_contact_sheet_v5.png`、`icon_alignment_before_after.png`、`visual_gate_v5_qa.md`、`scene_quality_report_v5.json`。停止位置は人間Gate 2の最終確認待ち。VOICEVOX・draft/final・thumbnail・YouTube操作は未実施。

## Episode 008 — Phase B draft_v1（2026-09-05）

- Visual Gate v5を人間承認済みとして固定。Fact CheckはFAIL 0 / REVIEW 0（公開日前の8月末統計確認はwatch）。
- VOICEVOX「剣崎雌雄 / ノーマル」で本編63/63 segmentを生成。実測ナレーション321.804秒、CTA11.563秒＋余韻3.437秒。
- 字幕122 cue（分割segment46）。実測WAVをsegment境界に使用し、split cueはVOICEVOX audio_queryのmora durationで同期。最小72px・3行0・overflow0・semantic split0。
- `episodes/008_investment_scam/output/draft_v1.mp4` を作成。336.803秒、H.264 1920x1080 30fps、AAC 48kHz。Phase 2 QA PASS。
- 代表フレーム19枚（18scene＋CTA）とcontact sheetを `episodes/008_investment_scam/work/qa_frames_draft_v1/` に保存。senior readabilityは機械PASS・全編人間視聴REVIEW。
- 停止: thumbnail確定、`final/final.mp4`、YouTube upload、End Screen実設定。

## Episode 008 — Phase B draft_v2（2026-09-05）

- draft_v1人間全編レビューを局所反映し、`episodes/008_investment_scam/output/draft_v2.mp4`を生成。draft_v1は上書きしていない。
- Visual Gate v5の18sceneを固定使用。音声はseg006/011/031/052/059の5件のみ再生成、58件を再利用。`信用`は3箇所を `シンヨオ`・accent=2、`今だけ`はseg031だけaccent=1、`188`は `イチ、ハチ、ハチ`。seg055の0570音声はv1維持。
- 字幕は121 cueへ更新し、0570-050588を公式数字で表示。tts_reading_leakage 0、below56px 0、3行0、overflow0。CTAは全文 `お届けします。` まで表示（56px・3行、右reserved維持）。
- 動画QA PASS: 336.870秒、H.264 1920×1080 30fps、AAC 48kHz mono。代表フレームと発音previewを保存済み。人間再確認後にfinalizeへ進む。
- 停止: 全編人間再確認待ち、thumbnail確定、`final/final.mp4`、YouTube upload、End Screen実設定。

## Episode 008 — Phase B draft_v3（2026-09-05・信用prosody局所修正）

- `episodes/008_investment_scam/output/draft_v2.mp4`から、全63segmentをscanして「信用」を含むseg006 / 011 / 059の3件だけを再生成。60件はdraft_v2のhash cacheを再利用。
- `信用`の辞書を1 approved entryへ更新し、`シンヨオ`をLOW→HIGH→HIGH→HIGHのplateauへ調整。`信用を`のcontext queryでは連続オ・オのpitch差0.0。`approved_pitch_shape_match`は3/3 PASS。
- draft_v2の今だけ・188・0570-050588字幕・CTA・Visual Gate v5を維持。SRT/ASS/timingはv2とハッシュ一致でsubtitle regression 0。
- `episodes/008_investment_scam/output/draft_v3.mp4`を生成。336.870秒、H.264 1920×1080 30fps、AAC 48kHz mono。Phase 2 QA PASS、decode/black/silence 0。
- preview・context query・pitch QA・代表フレームを保存済み。人間が聞くtimestampは約00:00:26、00:00:41〜00:00:45、00:04:58〜00:05:02。
- 停止: 人間承認イントネーション「信用」の最終確認待ち。final、thumbnail、YouTube upload、End Screen実設定は未実施。

## Episode 008 — Final・thumbnail確定（2026-09-05）

- draft_v3を人間承認済みとして、`episodes/008_investment_scam/output/final.mp4`をcopy-onlyで確定。draft_v3とSHA-256一致、再encodeなし。Final QA PASS。
- ユーザー提供thumbnailを正式採用。原本は`episodes/008_investment_scam/assets/thumbnail/thumbnail_source.png`、正式画像は`episodes/008_investment_scam/assets/thumbnail/thumbnail.png`（1280×720、16:9）。25%版とQAは`episodes/008_investment_scam/work/thumbnail_review/`。
- selected title、descriptionの主要根拠URL、VOICEVOXクレジット、`contains_synthetic_media=true`をmetadataで確認。AI開示の最終確定は公開時に人間判断。
- 2026-09-05の警察庁統計watchでは、最新掲載は令和8年7月末・暫定値で、令和8年8月末統計の新規掲載なし。公開直前に再確認する。
- End Screen予定はRELATED VIDEO: Episode004 ニセ警察詐欺、SUBSCRIBE: チャンネル登録。実設定は未実施。
- 停止: YouTube upload、schedule/public、thumbnail upload、End Screen実設定は未実施。公開準備完了・YouTubeアップロード待ち。

## Episode 008 — YouTube予約公開（2026-09-05）

- `episodes/008_investment_scam/output/final.mp4`を承認済みチャンネルID `UCgVRceTJYO5KOrPX4w2jXZw`へ非公開アップロード。video ID: `GryqJ70DCHs`。
- `privacyStatus=private`、`publishAt=2026-09-08T10:00:00Z`（2026-09-08 19:00 JST）、`selfDeclaredMadeForKids=false`をAPIで確認。
- 正式サムネイルの設定、selected title・descriptionの反映、AI開示`containsSyntheticMedia=true`（videos.update応答）を確認。重複再アップロードなし。
- End ScreenはYouTube Studioで人間設定するまで未完了。予定はEpisode004関連動画＋チャンネル登録。

## Episode 008 — YouTube予約公開（2026-09-05）

- `output/final.mp4`をチャンネルID `UCgVRceTJYO5KOrPX4w2jXZw`へ非公開アップロード。video ID: `GryqJ70DCHs`、SHA-256一致。
- `privacyStatus=private`、`selfDeclaredMadeForKids=false`、selected title・description・thumbnailを反映。
- 予約時刻: `2026-09-08T10:00:00Z`（2026-09-08 19:00 JST）。videos.listでvideo ID・channel ID・title・privacy・publishAtを検証し、**PASS**。
- サムネイルは`thumbnails.set`成功、`hasCustomThumbnail=true`を確認。AI開示はstatus-only update応答で`containsSyntheticMedia=true`を確認。
- 初回検証の項目省略はログへ記録し、同じ動画ID・同じ予約時刻を再検証。再アップロードなし。
- End Screenは未設定。YouTube StudioでEpisode004関連動画＋チャンネル登録を人間が設定する。
- 最終ログ: `episodes/008_investment_scam/work/youtube_publish/youtube_upload_log.md`。

## Episode 009 — Phase A / Visual Gate（2026-09-05）

- `episodes/009_windows11_24h2_support/`に、Windows 11 version 24H2のサポート終了と一般ユーザーの確認手順をまとめたPhase A成果物を作成。
- Microsoft公式情報を基に、Home / Pro等の24H2更新終了日、25H2の段階提供、26H1の位置づけを`research.md` / `fact_check.md` / `sources.md`へ記録。
- `episode.json`、`script.md`、`shotlist.md`、`scene_plan.json`、`publish.json`を作成。公式UI 3scene、template 13scene、ImageGen概念3sceneを構成。
- 19sceneを再レンダーし、`work/visual_review/scene_contact_sheet_v1.png`を更新。scene quality reportは17 OK / 2 WARN / 0 FAIL、ImageGen文字QAは3/3 PASS。
- 状態: `VISUAL_GATE_WAITING_HUMAN`。音声、字幕、draft、thumbnail、YouTube uploadは未実施。

## Episode 009 — Visual Gate v2（2026-09-05）

- SCENE-006 / 007 / 009のみを局所修正。SCENE-006は「設定→システム→バージョン情報」と公式focus crop、SCENE-007は「Windowsの仕様」と説明用のバージョン例欄、SCENE-009は「設定→Windows Update」と日本語補助ラベル＋公式ボタンcropへ変更。
- SCENE-001〜005、008、010〜019、ImageGen 001 / 015 / 019、共通背景、台本、音声、字幕は変更していない。
- `episodes/009_windows11_24h2_support/work/visual_review/scene_contact_sheet_v2.png` と `scene_006_007_009_before_after.png` を作成。
- Visual Gate v2 QA: 19 OK / 0 WARN / 0 FAIL。対象3sceneのaction clarity・official UI legibility・privacyを確認。
- 状態: `VISUAL_GATE_V2_WAITING_HUMAN`。人間確認後までVOICEVOX、字幕、draft、thumbnail、YouTube uploadへ進まない。

## Episode 009 — Phase B draft_v1（2026-09-05）

- Visual Gate v2は人間承認済みとして確定。19scene、19 OK / 0 WARN / 0 FAIL。
- Fact Check最終: FAIL 0 / REVIEW 0。Microsoft公式情報と台本を再突合済み。
- VOICEVOX「剣崎雌雄」ノーマルで52segmentを生成。再利用0、narration実測289.357秒。
- 24H2 / 25H2 / 26H1のTTS読みを補正し、表示字幕には英数字表記を維持。必須11語の発音previewを作成。
- 実測音声から字幕59 cueを生成。minimum subtitle font 72px、subtitle preflight PASS。
- `episodes/009_windows11_24h2_support/output/draft_v1.mp4`を生成。304.36秒、H.264 1920x1080 30fps、AAC 48kHz。
- draft QA PASS（decode / black frame / unexpected silence / official UI / privacy / Visual Gate v2 regression）。指定17scene + CTAの代表フレームとcontact sheetを保存。
- 状態: `DRAFT_V1_WAITING_HUMAN`。senior_readabilityはREVIEW。人間の全編視聴・発音試聴が完了するまでfinal、thumbnail、YouTube upload、schedule/public、End Screen実設定へ進まない。

## Episode 009 — Phase B draft_v2（2026-09-05）

- draft_v1は保持したまま、発音のみを局所修正。`方`の文脈読み、`Windows`、`Update`、`ID`の承認済みVOICEVOX読みを反映。
- 最終的に20segmentを再生成、32segmentを再利用。字幕59 cue、Visual Gate v2の19scene、公式UI crop、CTAは変更なし。
- `episodes/009_windows11_24h2_support/output/draft_v2.mp4`を生成。304.30秒、H.264 1920x1080 30fps、AAC 48kHz。
- 発音QA、decode、black frame、unexpected silence、Visual Gate v2 regression、official UI、privacy、CTAはPASS。`senior_readability=REVIEW`。
- 状態: `DRAFT_V2_WAITING_HUMAN`。方 / Windows / Update / IDの発音とdraft_v2全編の人間再確認待ち。final、thumbnail、YouTube upload、schedule/public、End Screen実設定へは進まない。

## Episode 009 — Phase B draft_v3（2026-09-05）

- draft_v1 / draft_v2を保持したまま、draft_v2の人間レビューで指摘された2箇所だけ台本文言を変更。segment006「考え方」→「考えるポイント」、segment038「24H2の方は」→「24H2の場合は」。
- `ambiguous_方_avoidance`を`AGENTS.md`へ追加し、`ambiguous_kanji_pronunciation`でscript.mdと全52 narration segmentをscan。変更後のnarration内「方」はsegment001（A / REVIEW）とsegment011（D / REWRITE候補）の2件で、今回は一覧化のみ。
- VOICEVOXは006 / 038の2segmentだけ再生成、他50segmentを再利用。Windows / Update / ID / 24H2 / 25H2 / 26H1の発音QAはPASS。`方`のglobal dictionary登録はなし。
- 字幕59cueを新文言・実測音声へ同期。minimum72px、font<56=0、overflow=0、3-line=0、TTS leakage=0。scene timeline / chapter / CTA startも再計算。
- `episodes/009_windows11_24h2_support/output/draft_v3.mp4`を生成。304.880秒、H.264 1920x1080 30fps、AAC 48kHz。
- QA PASS: decode error 0 / black frame 0 / unexpected narration silence 0 / Visual Gate v2 regression 0 / official UI PASS / privacy PASS / CTA PASS。Visual Gate v2のsceneとCTAは変更なし。
- 状態: `DRAFT_V3_WAITING_HUMAN`。`senior_readability=REVIEW`。人間のdraft_v3全編視聴と、約00:27.379 / 約03:24.944の変更箇所再確認待ち。final、thumbnail、upload、schedule/public、End Screen実設定へは進まない。

## Episode 009 — final・公開メタデータ準備（2026-09-05）

- draft_v3の人間全編レビューを最終承認として記録。`human_draft_approved=true`、`approved_draft=draft_v3`、`senior_readability=PASS`。
- 非対象の「方」2件をAPPROVEDへ解決。未解決発音0、`方`のglobal辞書登録なし。`ambiguous_方_avoidance`は恒久ルールとして維持。
- Microsoft公式Fact Watch PASS。24H2 Home / Pro系の2026-10-13、25H2、26H1、Windows 11全体ではないことを再確認。日付表示差は`episodes/009_windows11_24h2_support/work/fact_watch_final.md`へ記録し、台本・動画は変更なし。
- `episodes/009_windows11_24h2_support/output/final.mp4`をdraft_v3からcopy-onlyで確定。SHA-256一致、再エンコードなし。304.880秒、H.264 1920×1080 30fps、AAC 48kHz。
- Final QA PASS: decode / black / unexpected silence / visual regression / subtitle regression / privacy / CTA regression / pronunciation unresolved / fact FAIL / fact REVIEWはすべて0。
- `publish.json`、thumbnail brief、analytics plan、pre-publish checklistを準備。category_id=22、default_language=ja、made_for_kids=false、AI開示候補、End Screen予定を記録。
- 状態: `FINAL_WAITING_THUMBNAIL`。これは制作履歴上の記録であり、現在の状態は下記の予約公開記録を参照。

## Episode 009 — YouTube予約公開（2026-09-05）

- ユーザー提供サムネイルを正式採用し、原本保存・1280×720 normalize・25% readability QAをPASS。
- `output/final.mp4`を承認済みチャンネルID `UCgVRceTJYO5KOrPX4w2jXZw`へ非公開アップロード。video ID: `NO4ZwXPvgA0`。
- `privacyStatus=private`、`publishAt=2026-09-09T10:00:00Z`（2026-09-09 19:00 JST）、`selfDeclaredMadeForKids=false`をAPIで確認。
- selected title・description・サムネイルを反映し、AI開示`containsSyntheticMedia=true`を反映・API検証PASS。重複再アップロードなし。
- End ScreenはYouTube Studioで人間が設定するまで未完了。即時public化は行っていない。

## Episode 011 — Phase B draft_v1（2026-09-06）

- テーマ：マイナ保険証を口実にした自動音声・電話詐欺。
- Visual Gate v1を`APPROVED_WITH_2_FIXES`として反映。SCENE-003の核心1メッセージを`assets/official/mhlw_warning_core_v1.png`へ整理し、Episode010のdraft_v1実使用`registration_conversion_v1` CTAを画面・音声・canonical textで照合して再利用。
- VOICEVOX「剣崎雌雄 / ノーマル」39 segmentを生成。音声実測239.611秒。発音preflightは39/39、REVIEW 0。
- 冒頭実測：first safe action 5.005秒、official answer 8.389秒、3つの行動一覧19.461秒。各設定値を`episodes/011_myna_insurance_scam_call/work/draft_v1_measurements.md`へ記録。
- 中盤CTAは1回のみ。68.822秒開始、音声6.496秒、75.518秒に本編復帰。7秒上限PASS、疑似subscribe UI 0。
- 字幕39 cue、`captions.srt` / `captions.ass`、TTS reading leakage 0、subtitle preflightはFAIL 0 / WARN 8。
- `episodes/011_myna_insurance_scam_call/output/draft_v1.mp4`を生成。254.610秒、H.264 1920×1080 30fps、AAC 48kHz mono。Phase B QA PASS。代表20フレームのcontact sheetを保存。
- 状態：`DRAFT_V1_COMPLETE_WAITING_HUMAN_REVIEW`。人間の全編視聴とAI disclosure要否確認まで、thumbnail、final、YouTube upload、scheduleへ進まない。

## Episode 011 — Phase B draft_v2（2026-09-06）

- draft_v1の人間確認で指定された2点だけを反映。SCENE-018を背景・人物・主文・補助文のImageGen-native 1枚へ変更し、segment 039から視聴者向けブランドプロミス文言を削除。
- SCENE-018はImageGenを2回実行（retry 1）。`迷ったら、` / `その場で決めない`、`いったん止まって、` / `公式から確認` のexact text QA PASS。後付け文字0、pil_overlay fallback 0。
- viewer-facing brand promise scanは0件。内部metadataのブランド定義は保持。story resolution、冒頭の安全行動、厚労省の公式結論、3つの確認、中盤CTA、Episode010実使用の終了CTAは維持。
- VOICEVOXはsegment 039のみ再生成、他38 segmentを再利用。main narration 236.795秒。字幕39 cue、TTS reading leakage 0、電話番号QA PASS。
- `episodes/011_myna_insurance_scam_call/output/draft_v2.mp4`を生成。probe 251.800秒、H.264 1920×1080 30fps、AAC 48kHz mono、SHA256 `45AB01EC1FF4F807FFF4ED7F42436FAFD2D00A24FD087BAA7436AF371C78AAB4`。Phase B QA PASS。
- 代表20フレームのcontact sheetを`episodes/011_myna_insurance_scam_call/work/visual_review/draft_v2_contact_sheet.png`へ保存。
- 状態：`DRAFT_V2_COMPLETE_WAITING_HUMAN_REVIEW`。人間の全編視聴とAI disclosure要否確認まで、thumbnail、final、YouTube upload、scheduleへ進まない。

## Episode 011 — Final・thumbnail確定（2026-09-06）

- draft_v2の全編視聴を人間承認済みとして`work/human_review.json`へ記録。`senior_readability=PASS`。
- ユーザー提供サムネイルを正式採用。原本は`episodes/011_myna_insurance_scam_call/assets/thumbnail/thumbnail_source.png`、公開用は`assets/thumbnail/thumbnail.png`（内容変更なし、1280×720、1,129,358 bytes）。サムネイルQA PASS。
- `episodes/011_myna_insurance_scam_call/output/final.mp4`をdraft_v2からcopy-onlyで確定。SHA-256 `45AB01EC1FF4F807FFF4ED7F42436FAFD2D00A24FD087BAA7436AF371C78AAB4`、byte-identical、再encodeなし。
- Final QA PASS。decode / black frame / unexpected silence / av sync / subtitle / fact boundary / privacy / CTA / SCENE-018 native textを確認。
- 2026-09-06に厚生労働省・デジタル庁・警察庁の一次情報を再確認。主要事実の未確認0、privacy error 0。記録は`episodes/011_myna_insurance_scam_call/sources.md`。
- final実測タイムラインに基づくchaptersを`publish.json`へ反映。selected titleは変更していない。
- `contains_synthetic_media=false`を明示。非写実的概念画の既存方針に沿い、upload後のAPI verify対象とする。
- 予約目標：privateで2026-09-11 19:00 JST（`2026-09-11T10:00:00Z`）。即時public化は行わない。
- End ScreenはEpisode004を関連動画候補とし、関連動画・チャンネル登録要素はYouTube Studioで人間が設定する。動画側の疑似subscribe要素・自動設定は行わない。
- 状態：`FINAL_PENDING_SCHEDULED_UPLOAD`。YouTube upload / scheduleはpublish dry-run後に実行する。

## Episode 011 — YouTube予約公開（2026-09-06）

- 承認済み`episodes/011_myna_insurance_scam_call/output/final.mp4`を、承認済みチャンネルID `UCgVRceTJYO5KOrPX4w2jXZw`へ非公開で登録。video ID: `kSln-2eJ6CU`。
- `privacyStatus=private`、`publishAt=2026-09-11T10:00:00Z`（2026-09-11 19:00 JST）、`selfDeclaredMadeForKids=false`をAPIで確認。
- selected title・description・実測chapters・正式サムネイルを反映。サムネイル設定とmetadata / schedule検証はPASS。
- `containsSyntheticMedia=false`をstatus-onlyで再確認。`videos.insert`は追加で呼ばず、video ID不変、reupload=false、AI開示検証PASS。
- 既存video ID・upload attemptの重複防止を通過。最終記録は`episodes/011_myna_insurance_scam_call/work/youtube_publish/`。
- End Screenは未設定。YouTube StudioでEpisode004を関連動画、チャンネル登録要素を人間が設定する。

## Episode 012 — Phase A / Visual Gate（2026-09-06）

- `episodes/012_phishing_message_safety/`に、SMS・メールのリンクを使わず公式側から確認する長尺企画を正式検討し、Phase A成果物を作成。
- 一次情報を2026-09-06に確認。Case 1は国民生活センターの80歳代相談例、Case 2〜5は日本郵便・フィッシング対策協議会・JCB・ソフトバンク・国税庁・消費者庁等の注意喚起をもとにした架空の再現として整理。Fact Check FAIL 0 / REVIEW 3、Privacy FAIL 0。
- 80 segment・3,473字、5ケース＋共通3手順＋押した後の内容別対応。`long_form_watchtime_v1`の推定尺は約10分50秒。AVDを最重要指標としてEpisode 002 / 010 / 011と比較する。
- 31scene（template 25 / ImageGen 6）を共通背景 `adult_digital_soft_image_bg`でrender。接触シート、ImageGen文字QA、scene quality reportを保存。公式UIはAI生成せず、7scene slots（5 source groups）をPhase B用に未配置で保持。
- 状態: `PHASE_A_COMPLETE_WAITING_HUMAN_REVIEW`。VOICEVOX、字幕、draft、thumbnail生成、final、YouTube upload、schedule、End Screen実設定は未実施。
- 2026-09-10 JSTのApple Event後、iPhone・安全設定・詐欺対策に大きな影響があれば、公開順と公式リンクを人間が見直す。制作は停止しない。

## Episode 012 — Visual Gate v2（2026-09-06）

- Human Visual Gate v1は`REJECTED_WITH_COMMON_RENDERER_FIX`。原因は、公式素材未配置の`layout_04_text_official`が意味のない大きなチェックマークへfallbackし、視覚重心を左へ寄せていた共通renderer回帰。
- `scripts/scene_renderer.py`、`templates/scenes/layout_04_text_official.html`、`templates/scenes/styles.css`を修正し、左の短い要点＋右のneutral browser/phone frameへ統一。7scene（007 / 008 / 012 / 013 / 018 / 022 / 026）から巨大✓と意味のないfiller iconを除去。
- `templates/scenes/README.md`と`config/icon_catalog.json`へ`no_oversized_decorative_checkmark`、`no_meaningless_filler_icon`、icon size policy、official two-column、`visual_centroid_preflight`を恒久ルールとして追加。
- QAは31 OK / 0 WARN / 0 FAIL。`oversized_checkmark_count=0`、`decorative_checkmark_as_main_visual=0`、`meaningless_filler_icon=0`、`left_bias_fail=0`、`tiny_text=0`、`overflow=0`。公式7sceneの重心xは892.93〜965.22、右weight最小38.27%。
- 対象7scene以外の24sceneはv1 baselineとSHA-256一致。ImageGen章扉SCENE-001 / 005 / 010 / 016 / 020 / 024は未変更。
- 成果物: `episodes/012_phishing_message_safety/work/visual_review/scene_contact_sheet_v2.png`、`visual_gate_v2.md`、`scene_quality_report_v2.md`。状態: `PHASE_A_VISUAL_GATE_V2_WAITING_HUMAN_REVIEW`。
- VOICEVOX、字幕、draft、final、thumbnail、YouTube upload、schedule、End Screen設定は未実施。次は人間のv2確認。

## Episode 012 — Phase B draft_v1（2026-09-06）

- ユーザーがVisual Gate v2を`APPROVED_FOR_PHASE_B`として承認。SCENE-007 / 008 / 012 / 013 / 018 / 022 / 026のneutral browser/phone frameを、公式公開資料クロップまたは意味図解へ置換。
- 公式採用：SCENE-007 国民生活センター、SCENE-008 自分で公式アプリを開く意味図解、SCENE-012 フィッシング対策協議会、SCENE-013 安全な3入口の意味図解、SCENE-018 JCB、SCENE-022 ソフトバンク、SCENE-026 国税庁。placeholder 0、neutral frame 0、公式UI AI再現0、privacy PASS、公式文字TV可読性PASS。
- VOICEVOX「剣崎雌雄」80 segmentを生成・連結。字幕100 cue、72px、TTS reading leakage 0。`captions.srt`を配置。
- `episodes/012_phishing_message_safety/output/draft_v1.mp4`を生成。実尺595.56秒（9分55秒）、Phase 2 QA PASS。`output/review/scene_contact_sheet.png`とPhase B visual gate reportを保存。
- Fact Check FAIL 0 / REVIEW 3。長尺目標9〜11分に対して実尺は範囲内。
- 状態：`DRAFT_V1_COMPLETE_WAITING_HUMAN_REVIEW`。人間の全編確認とAI disclosure確認まで、thumbnail、final、YouTube upload、schedule、End Screen設定へは進まない。

## Episode 012 — Phase B draft_v2（2026-09-06）

- draft_v1の人間指摘を反映し、`episodes/012_phishing_message_safety/output/draft_v2.mp4`を生成。実測597.13秒、SHA-256 `94A04D4D905E3736E3792DAC69C1CE2A1935F9D71C11A052951B74161ED48B8B`、Phase 2 QA PASS。
- 字幕は119 cueへ全件再構成。target72px / minimum56px、overflow 0、3-line 0、`unnatural_japanese_line_break=0`、`word_split=0`、`conjugation_split=0`、`particle_or_auxiliary_orphan=0`、TTS reading leakage 0。
- 説明用SCENE-006 / 011 / 017 / 021 / 025の再現ラベルを削除。SCENE-007は国民生活センター公式PDFの正確な短い引用＋出典へ差し替え、公式取得失敗時のfail-closed policyを恒久化。
- 普段、何も、届け物、本物、カード会社、e-Taxを標準承認辞書へ登録し、実クエリ監査PASS。`カード会社`全4出現はドaccent、e-Taxは語中pauseなし。
- Episode011実使用finalをsource of truthとして、終了CTAのcanonical text・画面・音声・15秒・右40〜45%予約を一致させて再利用。中盤CTAもEpisode011と一致。
- Contact sheet：`episodes/012_phishing_message_safety/output/review/scene_contact_sheet_v2.png`。人間再確認ポイント：`episodes/012_phishing_message_safety/work/human_review_points_v2.md`。
- 状態：`DRAFT_V2_COMPLETE_WAITING_HUMAN_REVIEW`。thumbnail、final、YouTube upload、schedule、End Screen設定は未実施。

## Episode 012 — Phase B draft_v3（2026-09-06・人間全編確認待ち）

- draft_v2の人間再確認で指定された3点だけを反映し、`episodes/012_phishing_message_safety/output/draft_v3.mp4`を生成。実測585.55秒、SHA-256 `662804C23CD1FF6915CA65655671757A80118DD8E7EEC05F56627309EF9B1205`、Phase 2 QA PASS。
- 『これ、本物？』は直接audio_queryした4モーラ（ホ・ン・モ・ノ）と疑問ピッチを確認。`本物`全7出現のcontextual pronunciation audio gateをPASSし、e-Taxはイータックス（アクセント3＝タ、語中ポーズ0）へ標準辞書更新して実文クエリを確認。
- SCENE-031とsegment080を本編タイムラインから除外。SCENE-030（segments 076〜079）からEpisode011実使用CTAへ直接連結し、終了CTAは1回だけ。79 narration / 117 subtitle cue / 30 scene。
- `episodes/012_phishing_message_safety/work/human_review_points_v3.md`を保存。thumbnail、final、YouTube upload、schedule、End Screen設定は未実施。状態：`DRAFT_V3_COMPLETE_WAITING_HUMAN_REVIEW`。

## Episode 012 — Phase B draft_v4 / final（2026-09-06）

- ユーザー修正版「これ、本物？」の `030.wav` をhuman audio overrideの正本として採用。`audio/human_approved/030.wav` と元候補のSHA-256は `7B534892A4AC893CC7F1D0D483B67A8A94E690353DB652EA16B0077C3F4C7106` で一致し、narration SHA・timeline・保持方針は `episodes/012_phishing_message_safety/work/human_audio_override_v4.json` に記録。
- `human_audio_override > pronunciation dictionary > automatic VOICEVOX generation` を適用し、030の再生成なし。v4 build logは `regenerated=[] reused=78 human_overrides=[30]`、自動再生成0件。e-Taxのアクセントピーク「タ」、語中pause 0、SCENE-031 / segment080除外、117字幕cue、semantic QA 0件を維持。
- `episodes/012_phishing_message_safety/output/draft_v4.mp4` は585.400秒、SHA-256 `32933ED599E072DDF27FA7AF99756F4F78B15A3498DA0EA2071F44EC04660DD8`、Phase 2 QA PASS。人間全編確認・senior_readability=PASSを記録。
- `episodes/012_phishing_message_safety/output/final.mp4`をdraft_v4からcopy-onlyで確定。47,642,598 bytes、SHA-256はdraft_v4と一致。Final QAは `episodes/012_phishing_message_safety/work/final_qa.md`、状態は `UPLOADED_SCHEDULED`。
- ユーザー提供サムネイルを内容変更なしで正式採用し、1280×720へ正規化。サムネイル設定・YouTube upload・予約時刻・metadataをAPI検証済み。

## Episode 012 — YouTube予約公開（2026-09-06）

- 承認済み`episodes/012_phishing_message_safety/output/final.mp4`を、承認済みチャンネルID `UCgVRceTJYO5KOrPX4w2jXZw`へ非公開で登録。video ID: `CzTNLyAn1lY`（[YouTube](https://youtu.be/CzTNLyAn1lY)）。
- `privacyStatus=private`、`publishAt=2026-09-12T10:00:00Z`（2026-09-12 19:00 JST）、`selfDeclaredMadeForKids=false`をAPIで確認。即時public化は行わない。
- final SHA-256 `32933ED599E072DDF27FA7AF99756F4F78B15A3498DA0EA2071F44EC04660DD8`、サムネイル設定、title / description / chapters / source URLsの照合はPASS。再アップロードなし。
- `contains_synthetic_media=true`をupload時のstatus更新応答で確認。`videos.list`では当該owner-only項目が省略されたため、値の検証元を記録した。
- End Screenは未設定。YouTube StudioでEpisode004を関連動画、チャンネル登録要素を人間が設定する。動画側の疑似subscribe要素・自動設定は行わない。

## Episode 014 — Phase B draft_v2（2026-09-06）

- draft_v1の人間全編確認は`CHANGES_REQUIRED`。SCENE-005の生成画像＋大きな後乗せ文字を廃止し、ImageGen-native完成画へ差し替え。「残り1個」「どうする？」「架空の例」を画像内に一体生成し、キャラクター・ロゴ・実在UIは含めていない。
- `NO_IMAGE_TEXT_HYBRID`（canonical name: `no_generated_image_large_text_overlay` / `visual_mode_exclusive`）を`AGENTS.md`、`docs/text_render_policy.md`、validator、rendererへ恒久化。全Episode scanで`hybrid_generated_image_large_text=0`。
- ちいかわニュースを公式9月2日・9月5日発表、報道、確認できない同一性の順に補強。速報パート86.593秒、主要事実のFact FAIL 0件。出典は`episodes/014_chiikawa_fleamarket_safety/sources.md`と`fact_check.md`。
- 「ちいかわ」＝チイカワ（ワにaccent 4）、「フリマ」＝フリマ（マにaccent 3）、「188」＝イチハチハチを承認辞書へ登録。188の既存global entryはなく、v1は先回りした`spoken_text`が原因で辞書適用を bypass していた。対象発音はPASS、一般語「行う」の共通回帰ゲートのみREVIEW。
- VOICEVOX 38 segment、字幕52 cue。`episodes/014_chiikawa_fleamarket_safety/output/draft_v2.mp4`を生成（289.597秒、H.264 1920×1080 30fps、AAC 48kHz mono、SHA-256 `379D265E899549B34D9AE69CD290E2FC9D948A11B204C4EB37729C7046FCF3BD`）。Phase 2 QA PASS。
- scene quality reportは17 OK / 1 WARN / 0 FAIL。contact sheetは`episodes/014_chiikawa_fleamarket_safety/work/visual_review/scene_contact_sheet_v2.png`、人間確認ポイントは`episodes/014_chiikawa_fleamarket_safety/work/human_review_points_v2.md`。
- 状態：`DRAFT_V2_READY_HUMAN_REVIEW`。人間の全編確認待ち。thumbnail、final、YouTube upload、scheduleは未実施。

## Episode 014 — Final・指定サムネイル付きYouTube非公開アップロード（2026-09-06）

- 人間承認済み`episodes/014_chiikawa_fleamarket_safety/output/draft_v2.mp4`をcopy-onlyで`output/final.mp4`へ確定。289.597秒、24,583,308 bytes、SHA-256 `379D265E899549B34D9AE69CD290E2FC9D948A11B204C4EB37729C7046FCF3BD`。Final QA aggregate PASS。
- ユーザー指定の現行サムネイル`episodes/014_chiikawa_fleamarket_safety/thumbnail/thumbnail.png`（1672×941、1,815,430 bytes、SHA-256 `FDF0C3268221B1DAA4DE9C58CFD1192C9E4DCFEF82CF41DB5A92E9AB92CB03F3`）を設定。thumbnail API検証PASS。
- title `【ちいかわ転売問題】フリマで限定品を買う前に確認したい5つ`を、承認済み`final.mp4`からvideo ID `2l0SI8VIh8A`として1回だけ登録（[YouTube](https://youtu.be/2l0SI8VIh8A)）。channel guard PASS：`UCgVRceTJYO5KOrPX4w2jXZw`。
- API検証：title / description / chapters / source URLs PASS、`privacyStatus=private`、`publishAt=null`、`selfDeclaredMadeForKids=false`、`categoryId=22`、`defaultLanguage=ja`。`containsSyntheticMedia=true`はstatus-only `videos.update`応答で確認。
- 再アップロードなし（double upload 0）。予約・public化・unlisted化・End Screen設定は未実施。End Screen候補はEpisode012だが、Studio側設定は行っていない。
