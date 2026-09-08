# Episode 016 Phase A QC

基準日: 2026-09-08  
状態: Phase B停止 / 安全なLINE環境未準備

## 実施済み

- 公式情報の再確認: PASS（sources.mdに確認日・URL・確認内容を記録）
- 既存LINE Episodeとの重複確認: PASS（Episode 003 / 006 / 013）
- 競合需要の整理: PASS（需要研究のみ。文章・構成・サムネイルは流用しない）
- 3項目の絞り込み: PASS
- Phase A成果物の作成: PASS
- viewer-facing内部文言の確認: PASS（publish.jsonのviewer_facing_internal_brand_promiseは0）
- Human Gate 1: APPROVED WITH MINOR CHANGES
- viewer-facing修正: PASS（制作側の事情・Episode 006言及をナレーション、字幕、sceneから除去）
- キャッシュ説明の簡潔化: PASS
- 共通CTA設定更新: PASS（canonical / narration / display / textを更新、hash再計算）

## 未実施

- LINE実画面の取得
- 実際の削除操作
- 音声、字幕、scene、動画、thumbnailの生成
- YouTube操作
- Phase B以降の機械QA・Human Gate

## Phase B環境確認

- Android SDKのemulator.exe: 存在
- emulator-5554: 起動済み
- Android: 16
- LINEパッケージ jp.naver.line.android: 未導入
- 現在画面: Chrome
- 判定: 安全な実LINE環境を確認できないため停止
- 本番LINEへの切り替え: なし
- 実データの削除: なし

## 重大な保留

- LINEのメニュー名・表示順は端末やアプリのバージョンで変わる可能性がある。実画面取得後に台本とshotlistを照合する。
- キャッシュ削除について、トーク履歴などは削除されないという公式案内と、保存期間経過メディアやアプリ内メディアへの注意を併記する必要がある。
- 安全なテスト環境が用意できない場合、本番LINEを使わず、架空UIも作らない。
- 安全なLINE環境が用意されるまで、実画面capture・VOICEVOX・字幕実時間化・scene・full draftへ進まない。
