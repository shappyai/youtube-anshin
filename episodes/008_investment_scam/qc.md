# Episode 008 QC — draft_v1

確認日: 2026-09-05  
対象: `output/draft_v1.mp4`  
判定: **draft_v1 PASS／全編人間視聴待ち**

## Gate結果

| 項目 | 判定 | 根拠 |
|---|---|---|
| Fact | PASS | `fact_check.md`: FAIL 0 / REVIEW 0。公開日前の統計更新はwatchとして残置 |
| Language | PASS | VOICEVOX audio_query 63/63。文脈REVIEW 4件は確認済み。電話番号はsegment override適用 |
| Visual | PASS | Visual Gate v5の18scene、Phase 2 QA FAIL 0 / WARN 0。代表フレーム19枚を確認 |
| Audio | PASS | 本編321.804秒・CTA11.563秒。AAC 48kHzへ連結。全編の聞き取りは人間確認待ち |
| Subtitle | PASS | 122 cue、最小72px、3行0、overflow0、semantic split0。実測タイミング |
| Policy | REVIEW | `contains_synthetic_media=true` は候補として保持。AI開示の最終確定は公開前の人間判断 |
| Privacy | PASS | 実在著名人・個人情報を使用せず、公式UIの架空再現なし。金融庁公式UI captureは未使用 |
| Senior readability | REVIEW | 機械QA PASS。60代以上、特に65歳以上を想定した全編視聴を待つ |

## 動画仕様

- `output/draft_v1.mp4`: 336.803秒、H.264、1920×1080、30/1fps、AAC、48kHz、mono
- expected duration: 336.804秒、delta: 0.001秒
- SHA-256: `57953b5e788c8dbc0efa4713eca90c8daafe6f8940d2261f73c3e31724179313`
- narration WAV: `audio/voicevox_kenzaki/narration_kenzaki_auto.wav`、剣崎雌雄／ノーマル、speed 1.00／intonation 1.00／pitch 0.00
- CTA: `work/channel_cta.png`＋`audio/voicevox_kenzaki/cta_channel_common.wav`。画面15秒、音声11.563秒、余韻3.437秒。右40〜45%はEnd Screen reserved

## 冒頭25秒チェック

- 0.000秒からSCENE-001「その投資広告、本物？」を表示。
- `LINEに案内されたら。` は3.391秒から字幕表示。
- 7.480秒からSCENE-003「今日確認する、3つ」を表示。
- 13.487〜22.160秒で「確認したい3つ」「この3つ」をナレーション。
- 数字の本編提示は49.659秒からで、冒頭の結論提示後。

## 未実施・停止

- 全編の人間視聴による最終承認
- thumbnail候補の確定
- `final/final.mp4` の作成
- YouTube upload、公開、End Screen実設定

## draft_v2 — draft_v1人間全編レビュー反映（2026-09-05）

対象: `output/draft_v2.mp4`。draft_v1は上書きせず、Visual Gate v5の18sceneを固定して音声・字幕・CTAだけを局所更新した。

| 人間指摘 | 対応 | 結果 |
|---|---|---|
| 「信用」の抑揚 | seg006 / 011 / 059を再生成。共通辞書 `シンヨオ`・accent=2を人間承認済み設定として登録 | 3件すべて適用 |
| 「今だけ」の抑揚 | seg031だけに `イマダケ`・accent=1を適用。「今」はglobal登録しない | phrase限定 |
| 188の読み | seg052をEpisode004承認値 `イチ、ハチ、ハチ` で再生成 | 3語に分離 |
| 0570-050588 | seg055のdraft_v1音声を再利用。字幕表示のみ公式数字へ更新 | `0570-050588` |
| CTA末尾の欠落 | CTA画面を局所再配置し、説明文を3行・56pxで全文表示 | `お届けします。`まで表示 |

音声は本編63セグメント中5件（006/011/031/052/059）のみ再生成し、58件はdraft_v1 WAVを再利用した。発音preview WAVとaudio_queryは `work/phase_b_review/pronunciation_fix_v2/` に保存した。

### draft_v2 QA

- 動画: **PASS**。336.870秒、H.264、1920×1080、30fps、AAC、48kHz mono。デコードエラー0、黒画面0、想定外の長時間無音0。
- Visual Gate v5: **回帰0**。入力は `work/rendered_final_scenes_v5/` の18scene固定。CTA画面だけ `work/channel_cta_v2.png` に更新。
- 字幕: blocking failure 0。121 cue、below56px 0、3行 0、overflow 0、`tts_reading_leakage` 0。preflightの既存WARN 27件は短いcue・行バランス・cue数に関する非ブロッカー。
- 電話番号字幕: `0570-050588` を公式数字で表示（00:04:43.341〜00:04:47.021）。音声はdraft_v1から変更なし。
- CTA: `cta_full_text_visible=PASS`、説明文56px・3行、CTA本文60px・2行、クリッピング0、右側reserved開始x=1090を維持。ロゴ・疑似登録アイコンなし。
- 人間再確認フレーム: `work/qa_frames_draft_v2/contact_sheet.png`（0:26 / 2:45 / 4:32 / 4:44 / CTA 5:27付近）。

機械QAはPASSだが、「信用」「今だけ」「188」「0570-050588」とCTA全文の人間再確認は未完了。次工程は人間確認後のfinalizeであり、thumbnail確定・`final/final.mp4`・YouTube upload・End Screen実設定は行っていない。

## draft_v3 — 「信用」発音の人間承認形状反映（2026-09-05）

入力 `output/draft_v2.mp4`から、全63 narration segmentをscanして「信用」を含むseg006 / 011 / 059だけを再生成した。draft_v1/v2、Visual Gate v5、今だけ・188・0570-050588字幕・CTAは変更していない。

- dictionary: `信用 → シンヨオ`の1 approved entryへ統合。`low_high_plateau`（シ低→ン高→ヨ高→オ高）を`/mora_data`後に適用し、`信用を`の後続オも同値化。
- pitch QA: `approved_pitch_shape_match=PASS`（3/3）。first mora low、second mora rise、later mora plateauはすべてPASS。context queryのO-O pitch deltaは0.0。
- audio: regenerated=3（006/011/059）、reused=60。剣崎雌雄／ノーマル、本編321.868秒。
- subtitle regression: 0。draft_v2のSRT/ASS/timingを完全再利用（現行canonicalは121 cue、0570-050588数字表示）。
- CTA: v2承認済み画面・音声を再利用、`cta_full_text_visible=PASS`、`お届けします。`まで表示。
- video QA: **PASS**。336.870秒、H.264 1920×1080 30fps、AAC 48kHz mono、decode error 0／black frame 0／unexpected silence 0／Visual Gate v5 regression 0。
- pitch report: `work/phase_b_review/pronunciation_fix_v3/pronunciation_fix_v3.md`
- representative frames: `work/qa_frames_draft_v3/contact_sheet.png`

機械QAはPASS。人間が聞くtimestampは約00:00:26、00:00:41〜00:00:45、00:04:58〜00:05:02。ここで「信用」の最終承認を待ち、finalize・thumbnail・`final/final.mp4`・YouTube upload・End Screen実設定へは進んでいない。

## Final・thumbnail（2026-09-05）

ユーザー提供の今回の画像を正式サムネイルとして採用した。imagegen_native再生成・別案・A/B/C候補は作成していない。

- 原本: `assets/thumbnail/thumbnail_source.png`（1672×941、SHA-256 `8759ba8a8d7f4534d66c3227bd84164236ae4764648103afd7bfb2627b4100f2`）
- 正式thumbnail: `assets/thumbnail/thumbnail.png`（1280×720、16:9、SHA-256 `f73ffff3b74414fe921104ac1e89605ee9ba3cb643c818130cdeb8010d3d923e`）
- 25%確認: `work/thumbnail_review/thumbnail_25.png`（320×180、readability PASS）
- thumbnail QA: **PASS**。decode、文字誤り、文字切れ、edge clipping、25%可読性、実在著名人、個人情報、口座番号、QRコードを確認。LINEは「投資広告からLINEへ誘導されたら注意」の文脈を維持。
- final: `output/final.mp4`（`draft_v3.mp4`からbyte-identical copy、再encodeなし）
- final SHA-256: `92166d59c228baff67ad32280899066ad050ff6c715646d773427ccba04f2854`
- final QA: **PASS**。336.870秒、H.264 1920×1080 30fps、AAC 48kHz mono、decode error 0、black frame 0、unexpected silence 0、Visual Gate v5 regression 0、subtitle regression 0。
- metadata: selected title、descriptionの主要根拠URL、VOICEVOXクレジット、`contains_synthetic_media=true`を確認。AI開示の最終確定は公開時に人間確認。
- 最新統計watch: 2026-09-05時点で警察庁の最新掲載は令和8年7月末・暫定値。令和8年8月末統計の新規掲載なし。公開直前に再確認する。
- End Screen予定: RELATED VIDEOはEpisode004 ニセ警察詐欺、SUBSCRIBEはチャンネル登録。実設定はYouTube Studioで人間が行う。

YouTube upload、schedule/public、thumbnail upload、End Screen実設定は未実施。

## YouTube upload・予約公開（2026-09-05）

- 対象: `output/final.mp4`。SHA-256 `92166d59c228baff67ad32280899066ad050ff6c715646d773427ccba04f2854`を事前確認。
- チャンネルID: `UCgVRceTJYO5KOrPX4w2jXZw`。video ID: `GryqJ70DCHs`。別動画の重複アップロードなし。
- タイトル・description・category・language: **PASS**。`privacyStatus=private`、`selfDeclaredMadeForKids=false`: **PASS**。
- 予約: `publishAt=2026-09-08T10:00:00Z`（2026-09-08 19:00 JST）: **PASS**（videos.listで検証）。即時公開は未実施。
- サムネイル: `thumbnails.set` **PASS**、APIの`hasCustomThumbnail=true`を確認。
- AI開示: `containsSyntheticMedia=true`をstatus-only update応答で確認。動画ID不変、再アップロードなし。後続のvideos.listでは当該項目が省略されたため、検証ログに根拠を記録。
- 初回検証はYouTube APIの項目省略で停止したが、同じ予約時刻の再検証を行い、最終状態を**uploaded_scheduled / PASS**へ確定。
- End Screen: 未設定。YouTube StudioでEpisode004関連動画＋チャンネル登録を人間が設定する。

関連ログ: `work/youtube_publish/upload_attempt.json`、`work/youtube_publish/youtube_upload_log.md`。
