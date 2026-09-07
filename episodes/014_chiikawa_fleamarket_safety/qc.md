# Episode 014 QC

## 現在の状態

- status：`UPLOADED_PRIVATE_VERIFIED`
- 制作モード：`TREND_FAST_TRACK_V2`
- STOP条件：private uploadと同じvideo IDのAPI検証まで完了。ここで停止
- thumbnail：`thumbnail/thumbnail.png`（ユーザー指定ファイル・YouTube設定済み）
- final：`output/final.mp4`（承認済み`draft_v2`からcopy-only）
- upload：`privacyStatus=private`で完了・API検証PASS
- schedule：未設定。public / unlisted / End Screenは未実施

## draft_v2 機械QA（承認前記録）

- `output/draft_v2.mp4`：PASS
- 実測構成尺：289.597秒（本編274.597秒＋終了CTA 15秒。Phase 2 probeは289.6秒）
- 速報パート：86.593秒（目標65〜90秒）
- 映像：1920×1080 / H.264 / 30fps
- 音声：AAC / 48kHz / mono
- 黒画：検出なし
- 長い無音：検出なし
- 音声・映像の期待尺差：許容範囲
- SHA-256：`379D265E899549B34D9AE69CD290E2FC9D948A11B204C4EB37729C7046FCF3BD`
- narration：38 segments
- subtitles：52 cues、subtitle preflight PASS（FAIL 0、WARN 0）
- Fact：重大なFAIL 0件。Tier B報道の表現と公式cropは全編人間確認待ち
- Pronunciation：対象の「ちいかわ」「フリマ」「188」は承認済み辞書でPASS。共通回帰ゲートの「行う」はREVIEW
- ImageGen：SCENE-001/005ともimagegen_native完成画、character art 0
- SCENE-005：旧 `gpt_image + pil_overlay` から、画像内に「残り1個／どうする？／架空の例」を一体生成した完成画へ変更
- `NO_IMAGE_TEXT_HYBRID`：Episode全体 `hybrid_generated_image_large_text=0`
- scene quality report：OK 17 / WARN 1 / FAIL 0（WARNはSCENE-003の小文字proxyのみ。`work/visual_review/scene_quality_report_v2.md`）
- contact sheet：[work/visual_review/scene_contact_sheet_v2.png](work/visual_review/scene_contact_sheet_v2.png)

## Final / private upload verification

- 人間確認：`output/draft_v2.mp4` 全編承認。senior readability PASS、発音レビューPASS。
- final：`output/final.mp4`。copy-only、承認済みdraft_v2とbyte-identical。
- final SHA-256：`379D265E899549B34D9AE69CD290E2FC9D948A11B204C4EB37729C7046FCF3BD`
- final尺：289.597秒。Final QA aggregate PASS（codec / duration / decode / black / silence / AV-syncはbyte-identicalなPhase 2 QA証拠を継承）。
- Fact：重大FAIL 0件。Pronunciation：PASS（seg020「行う」は実聴で自然、再生成・共通辞書登録なし）。
- Subtitle：52 cues、FAIL 0 / WARN 0。Visual：OK 17 / WARN 1 / FAIL 0、hybrid 0、character artwork 0、privacy PASS。
- thumbnail：`thumbnail/thumbnail.png`、1672×941、1,815,430 bytes、指定ファイルのSHA-256 `FDF0C3268221B1DAA4DE9C58CFD1192C9E4DCFEF82CF41DB5A92E9AB92CB03F3`。thumbnail設定PASS。
- title：`【ちいかわ転売問題】フリマで限定品を買う前に確認したい5つ`
- video ID：`2l0SI8VIh8A`（[YouTube](https://youtu.be/2l0SI8VIh8A)）。チャンネルID guard PASS：`UCgVRceTJYO5KOrPX4w2jXZw`。
- metadata照合：title / description / chapters / source URLs PASS。`privacyStatus=private`、`publishAt=null`、`madeForKids=false`、`categoryId=22`、`defaultLanguage=ja`。
- AI開示：`containsSyntheticMedia=true`。status-only `videos.update(part=status)`応答で確認。`videos.list`でowner-only項目が省略された点を記録。
- 再アップロード：なし（double upload 0）。
- schedule：`NOT_SET`。public / unlisted化なし。
- End Screen：`NOT_SET`。候補はEpisode012だが、YouTube Studio設定は行っていない。

## draft_v1 既往記録

- `output/draft_v1.mp4`：PASS
- 実測尺：249.210秒（本編234.213秒＋終了CTA 15秒）
- 速報パート：39.201秒（60秒以内）
- 映像：1920×1080 / H.264 / 30fps
- 音声：AAC / 48kHz / mono
- 黒画：検出なし
- 長い無音：検出なし
- 音声・映像の期待尺差：許容範囲
- SHA-256：`BDAB55A366EDD80A13774A6559617222F7120DBD2D52AD40254BB76EB309E37F`

## draft_v1 自動チェック記録

- episode schema：PASS
- subtitle preflight：PASS（39 cues、FAIL 0、WARN 0）
- tts_reading_leakage：PASS
- japanese_semantic_line_break：PASS（不自然な分割0）
- Fact：重大なFAIL 0件。Tier B報道の表現と公式cropは全編人間確認待ち
- Pronunciation：REVIEW 2件（「行う」の音声フレーズ確認、共通回帰ゲートのEpisode外対象確認）
- ImageGen SCENE-001：文字QA PASS、再生成1回。人物型キャラクター0を目視確認
- ImageGen SCENE-005：v1は生成画像＋大きな後付け文字のhybrid。人間全編確認でCHANGES_REQUIREDとなり、v2でImageGen-native完成画へ差し替え
- 公式素材：4点、PDFレンダー由来。個別UIのAI再現なし
- oversized_checkmark：0
- meaningless_filler_icon：0
- left_bias_fail：0（レンダー後に機械チェック）
- neutral_placeholder_final：0（公式素材は配置済み）
- midroll CTA：0
- end CTA：1（承認済みpostroll再利用）

## 人間確認が必要な項目

- 速報の事実・報道・SNS推測の切り分け
- VOICEVOX「ちいかわ」「フリマ」「188」および「くら寿司」「SNS」「LINE」「受取評価」の発音
- 全編の字幕同期、TV視聴時の可読性、公式cropの判読性
- ImageGen画像にキャラクター・ロゴ・実在UIがないこと
- SCENE-005がImageGen-native完成画で、generated image＋大きな後付け文字のhybridになっていないこと（恒久ルール適用済み）
- AI開示を含む公開前メタデータ

## 人間確認待ち

- 全編を視聴し、速報の事実境界、VOICEVOX発音、字幕同期、公式cropの判読性、生成画像の権利上の類似性を確認する。確認ポイントは `work/human_review_points_v2.md` に記録。
- 人間確認が終わるまで、thumbnail確定・`final/final.mp4`作成・upload・scheduleへ進まない。
