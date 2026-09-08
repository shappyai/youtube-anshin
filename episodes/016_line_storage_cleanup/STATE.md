# Episode 016 state

- Episode: 016_line_storage_cleanup
- Topic: LINEが重い・容量が大きいと感じたときに、写真やトークを消す前に確認する3か所
- 基準日: 2026-09-08
- Phase: **Phase B / 安全なLINE環境未準備のため停止**
- status: in_review
- phase_a_human_gate: APPROVED WITH MINOR CHANGES
- human_approved: false
- upload_eligible: false
- title_status: 第一候補「【LINE】重くなった？写真を消す前に確認したい3か所」をPhase B仮使用。最終確定はHuman Gate 2
- viewer_facing_internal_brand_promise: 0
- 実画面capture: 未実施
- 削除操作: 未実施
- VOICEVOX生成: 未実施
- 字幕生成: 未実施
- scene・動画生成: 未実施
- thumbnail生成: 未実施
- YouTube操作: 未実施
- 共通CTA設定: 更新済み。新canonical textの音声・画像assetは未生成

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

## Phase B環境確認

- Android SDKのemulator.exeは存在し、emulator-5554は起動済み
- 端末モデル: sdk_gphone64_x86_64
- Android: 16
- LINEパッケージ jp.naver.line.android: 未導入
- 現在画面: Chrome
- 判定: 安全な実LINE環境を確認できないため、実画面capture以降を停止
- 本番LINEへの切り替え: 実施しない
- 削除操作: 実施しない

## Phase B再開条件

1. 個人情報のないAndroid Emulatorまたはテスト用LINEアカウントを用意する
2. 現行LINE UIの入口・項目名・表示順を確認する
3. 削除ボタン直前までの実画面を取得する
4. 音声・字幕・scene・full draftを生成し、Human Gate 2で確認する

## 停止文

**Phase B停止。安全な実LINE環境が未準備のため、本番アカウントへ切り替えず、実画面capture・削除・音声・scene・full draftへ進まない。**
