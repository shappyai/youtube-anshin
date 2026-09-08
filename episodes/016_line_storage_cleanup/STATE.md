# Episode 016 state

- Episode: 016_line_storage_cleanup
- Topic: LINEが重い・容量が大きいと感じたときに、写真やトークを消す前に確認する3か所
- 基準日: 2026-09-08
- Phase: **Phase B / full draft生成済み、Human Gate 2待ち**
- status: in_review
- phase_a_human_gate: APPROVED WITH MINOR CHANGES
- human_approved: false
- upload_eligible: false
- title_status: 第一候補「【LINE】重くなった？写真を消す前に確認したい3か所」をPhase B仮使用。最終確定はHuman Gate 2
- viewer_facing_internal_brand_promise: 0
- 実画面capture: Human提供3枚を受領。正規化copyを作成し、個人情報QA PASS
- 削除操作: 未実施
- VOICEVOX生成: 完了。剣崎雌雄ノーマル、44セグメントを生成・再利用
- 字幕生成: 完了。実測タイミングの44 cue、SRT/ASSを生成
- scene・動画生成: 完了。13 scene + CTAのfull draftを生成
- thumbnail生成: 未実施
- YouTube操作: 未実施
- 共通CTA設定: 更新済み。新canonical textの音声・画像assetをPhase Bで生成
- full draft: `output/draft_auto_v4.mp4`、実尺280.2秒（本編267.743秒 + CTA12.456秒）
- draft SHA-256: `ACC541077A5F206CAAAAF6967D1BCFC4BF47461A0F546A95121991231E1969E8`

## Human Gate 1承認

- テーマ、3項目、安全境界: 承認
- viewer-facingから制作側の事情を削除
- キャッシュ説明を簡潔化
- 比喩表現を削除
- 第一候補タイトルを更新
- channel_common_ctaを現行文言へ更新

## Phase Aで完了

- AGENTS.mdとルートSTATE.mdを確認
- 既存LINE Episode 003、006、013を確認
- 2026-09-08時点のLINE公式ヘルプ・公式ガイドを再確認
- 競合の需要と見せ方を調査し、文章・構成・サムネイルをコピーしない方針を記録
- 「容量の内訳」「キャッシュ」「容量の大きいトーク」の3項目を選定
- キャッシュ、トーク履歴、写真、動画、ファイル、ボイスメッセージ、アルバムの違いと注意を整理
- タイトル候補4案を比較し、推奨3案を提示。最終タイトルは未決定
- brief.md、sources.md、script.md、shotlist.md、media_manifest.csv、episode.json、publish.jsonを作成
- Human Gate 1のminor changesをscript.md、episode.json、publish.json、brief.mdへ反映
- config/channel_cta.jsonのcanonical / narration / display / textを更新し、content_hashを再計算

## 公式情報の要点

- LINE公式は、キャッシュやトーク履歴データの蓄積が容量増加・動作の重さの要因になると案内
- ホーム → 設定 → トーク → データの削除から、キャッシュやトーク関連データを確認する入口を案内
- キャッシュ削除でもトーク履歴などは削除されないという案内がある
- 保存期間経過の写真・動画や、アプリ内の画像・動画・ボイスメッセージが利用できなくなる場合の注意もある
- トークごとのデータ削除では、容量の大きいトークルーム順に確認できる
- トーク内データやアルバム内容の削除は復元できないものがある

## 3項目

1. データの削除で容量の内訳を確認する
2. キャッシュを確認し、削除するならキャッシュだけにする
3. トークごとの容量順で大きいトークを確認する

## Phase B撮影素材確認

- Android EmulatorへのLINEアカウント作成・ログイン: 実施しない
- Human提供画像: `トーク.jpg`、`データの削除.jpg`、マスク済みの`トーク毎に削除.jpg`
- 正規化copy: `assets/normalized/`。EXIFを除去し、実画面のcropを作成
- 個人情報QA: 3枚とも、本人名・友だち名・グループ名・実トーク・写真・電話番号・メールアドレス・QRコード・通知内容は判読できない状態を確認
- LINE UI: 「トーク」の「データの削除」、「キャッシュ 369.7MB」、「トークごとにデータを削除」、マスク済み容量順の実画面を確認
- 削除操作: 実施しない

## Phase B実施結果

1. 正規化した3枚のHuman実画面と、視認性を優先した実画面cropをshotlistとepisode.jsonに反映した
2. VOICEVOX発音レビュー、音声、実時間字幕を完了した
3. scene contact sheet、full draft、QAを生成した
4. Human Gate 2で実画面・個人情報・音声・字幕・draftを確認する

## 自動QA結果

- production preflight: PASS（公式素材、字幕、発音、viewer-facing内部ブランド文言0）
- VOICEVOX pronunciation: PASS（approved 6、review 0、queries 44/44）
- subtitle preflight: PASS（44 cue、fail 0、warn 0）
- phase2 QA: PASS（13 scene、黒画面FAILなし、実尺280.2秒）
- viewer-facing text QA: PASS（内部ブランド文言0）
- scene quality report: 公式画面が白面中心のため共通グラデーションとの差分比較ができず、公式scene 6件が機械FAIL。代表フレームの目視では、実画面の見切れ・字幕帯侵入・制作側ラベル残存なしを確認した。

## 継続中の安全境界

**Human提供の設定画面だけを使用し、実データの削除操作、Android EmulatorへのLINEログイン、thumbnail生成、YouTube upload/publishは行わない。full draft完成後にHuman Gate 2で停止する。**
