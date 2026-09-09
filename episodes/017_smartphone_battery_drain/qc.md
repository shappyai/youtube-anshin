# Episode 017 QC

## 最終判定

- 判定: **UPLOADED_PRIVATE_HUMAN_APPROVED**
- 対象: Human Gate 2修正後の実画面拡大、発音辞書反映、音声、字幕、scene、full draft v2、copy-only final
- 基準日: 2026-09-09
- Human Gate 1: **APPROVED WITH MINOR CHANGES**
- Human Gate 2: **APPROVED**。`draft_auto_v2.mp4`をHumanが全編確認し、映像・実iPhone画面・字幕・音声・発音を承認
- Phase Bの完了条件: Human提供iPhone 12 mini／iOS 26.6.1の画面を受領し、正規化crop、発音修正音声、字幕、scene、full draft v2、個人情報QAを実施済み。バッテリー発音は標準辞書・mora QA PASS、夕方・使われ方・画面上・開いて・バックグラウンド・iPhone・iOS・AppleもHuman Gate 2で承認済み

## 確認結果

| 項目 | 判定 | 確認内容 |
|---|---|---|
| Fact | PASS_WITH_SCREEN_SYNC | Apple公式を主根拠に、使用状況・画面・バッテリー状態を紐付けた。撮影時点でApple公式を再確認し、iPhone 12 miniの実表示へ同期。 |
| Language | PASS_WITH_MINOR_CHANGES | 65歳以上を想定し、確認と変更を分離。バッテリー状態は最大容量・注意表示を中心にし、専門用語を実機確認後に補足する。 |
| Visual | PASS_WITH_HUMAN_CONTACT_SHEET_REVIEW | Human提供の実OS画面から正規化cropを作成。実画面メインを9 sceneへ拡大し、汎用盾・チェック表示を除去。15 sceneとv2 draft contact sheetを目視確認し、アプリ名が見える使用状況rawはviewer-facingに使用しない。 |
| Audio | PASS_HUMAN_APPROVED | VOICEVOXを1文単位で34セグメント管理。「バッテリー」含む10セグメントを再生成し、mora QA（バ・ッ・テ・リ・イ、accent=4、語末高域）と標準辞書登録はPASS。夕方・使われ方・画面上・開いて・バックグラウンド・iPhone・iOS・AppleはHuman Gate 2で承認済み。 |
| Policy | PASS | 位置情報、通知、バックグラウンド通信、5G、強制終了の一律オフ推奨を含めない。Human提供サムネイルを使用し、YouTubeはprivate uploadのみ実施。公開予約・公開は行わない。 |
| Privacy | PASS_WITH_RESTRICTIONS | raw screenshotsはsource保管。production assetにはアプリ名を避けたcropのみ使用し、Apple Account・メールアドレス・電話番号・端末名・通知・位置情報履歴・個人的な利用状況・シリアル番号を残さない。raw screenshots/はcommit対象外。 |
| Subtitle | PASS | 34 cueを実音声タイミングから生成。60px、最大2行、subtitle preflight fail=0 / warn=0。 |
| Draft | PASS | `output/draft_auto_v2.mp4`。321.13秒、1920×1080、30fps、Phase 2 QA failures=0 / warnings=0。旧v1は保持。 |

## Human提供画面の確認結果

1. Human提供端末: iPhone 12 mini / iOS 26.6.1。
2. 「バッテリー」画面: 「1日の使用状況」「すべてのバッテリー使用状況を表示」「バッテリーの状態と充電」。
3. 「バッテリー使用状況」画面: グラフ、「画面オン」「画面オフ」。アプリ一覧はrawに個人利用が推測できる名前があるため使用しない。
4. アプリ詳細: 「アクティビティ」「画面上」「バックグラウンド」を確認できるcropを使用。
5. 「画面表示と明るさ」画面: 「明るさ」「自動ロック 5分」を確認。iPhone 12 miniに「常に画面オン」は表示されないため、viewer-facingでは一般化しない。
6. バッテリー状態: 「バッテリーの状態と充電」「最大容量 100%」「ピークパフォーマンス性能」を確認。「サービス」は表示されていないため、条件付き説明にする。

## 禁止事項チェック

- 節電のために設定を片っ端から変更: **該当なし**
- 位置情報・通知・バックグラウンド通信の一律オフ: **該当なし**
- 5Gを切れば必ず改善という断定: **該当なし**
- 強制終了の常用案内: **該当なし**
- バッテリー残量や最大容量だけで交換必須と断定: **該当なし**
- 怪しい節電アプリの紹介: **該当なし**
- 内部用ブランド文言のviewer-facing混入: **0件**

## v2修正内容

- 発音: `config/voicevox_pronunciation.yaml`へ標準辞書として`バッテリー`を1件登録。VOICEVOX実audio_queryの5モーラ「バ・ッ・テ・リ・イ」を確認し、4モーラ目「リ」にaccent=4、`low_high_plateau`を適用。
- 再生成segment: 002、005、006、007、022、023、025、027、029、031。音声尺はv1と同じ308.681秒。
- Visual: SCENE-001、003、004、005、006、007、008、009、010、011、012、013、014をv2化。うちSCENE-004/005/006/007/009/010/011/013/014は実画面メイン。SCENE-002/015は一覧として維持。実画面slot幅は840px（43.8%）から1270px（66.1%）へ拡大。
- 字幕: v2音声から再計算し、34 cue。音声尺が変わらなかったため字幕内容・タイムコードはv1と同一SHA。字幕帯はy=900以降、実画面slotはbottom=895pxで重ならない。
- CTA: `config/channel_cta.json`をcanonicalとし、Episode016の`channel_common_cta`音声・visualをcopy/reuse。文言の新規生成なし。

## 実施済みQA

- episode/schema、sources、scenes、official assets: **PASS**
- viewer-facing内部ブランド文言検査: **PASS / count 0**
- CTA canonical preflight v2: **PASS**。`config/channel_cta.json`の文言・Episode016再利用音声・visualを使用
- production preflight final: **PASS**。episode/schema、sources、scenes、official assets、subtitle、pronunciation（34/34、review=0）、viewer-facing INTERNAL_ONLYを確認
- phase2 QA final: **PASS**。failures=0 / warnings=0。scene quality final: **PASS**（15/15）。video decode: **PASS**
- visual revision QA v2: **PASS**。実画面9 scene、slot幅66.1%、字幕帯重なりなし、AI Apple UIなし、汎用盾・チェック0件
- 実尺: 本編音声 308.681秒。CTA音声 11.456秒＋末尾1秒を含むdraft v2 321.137秒（probe表示321.13秒）
- サムネイル: **Human提供画像を使用**。Codexによる生成なし。YouTube設定済み
- YouTube操作: **private upload済み**。公開予約・公開・End Screen・固定コメントは未実施

## Human Gate 2確認結果

1. `バッテリー`全出現で最後の「リ」が語末の高域として聞こえること（表示字幕は「バッテリー」のまま）: **承認済み**
2. v2実画面メインsceneの重要文字がテレビ視聴でも確認でき、字幕帯に覆われていないこと: **承認済み**
3. `画面上`、`開いて`、`夕方`、`使われ方`、`バックグラウンド`、`iPhone`、`iOS`、`Apple`の発音: **承認済み**
4. app listを除いた正規化cropとdraftに個人情報がないこと: **承認済み**
5. バッテリー状態の説明が「最大容量」「サービス等の注意表示」に留まり、数字だけで交換必須・故障と断定していないこと: **承認済み**
6. CTA本文・音声がcanonicalと一致し、右側のEnd Screen予約領域を侵食していないこと: **承認済み**

## Final QA / finalize

- `output/draft_auto_v2.mp4`を再エンコードせず、copy-onlyで`output/final.mp4`を作成。
- draft/final SHA-256: `76BC6321AB21A2C520E92F7743FBDFE4707FF7820A1A488046899119AE5978D5`（一致）。
- Final QA: **PASS**。SHA一致、動画デコード、黒画面、無音、クリッピング、AV尺一致、1920×1080、30fps、H.264/AACを確認。
- pronunciation preflight: **PASS**（queries 34/34、review 0）。`バッテリー`標準辞書登録は維持。
- subtitle preflight: **PASS**（34 cue、fail 0、warn 0）。
- CTA canonical preflight: **PASS**。`config/channel_cta.json`とEpisode016再利用素材を使用。
- viewer-facing INTERNAL_ONLY QA: **PASS**（count 0）。
- privacy QA: **PASS**。Human提供の正規化実画面のみをproductionへ使用し、raw screenshotsは未追跡。
- publish preflight: **PASS**（upload前private dry-run）。
- YouTube upload: **uploaded_private**。video ID `XjAf_B77EtE`、privacy `private`、publishAt未設定。API再確認は**PASS**。
- サムネイル: Human提供画像を`episodes/017_smartphone_battery_drain/assets/thumbnail/thumbnail.png`へ配置し、YouTube設定済み。
- YouTubeのschedule、publish、End Screen、固定コメント設定: **未実施**。
