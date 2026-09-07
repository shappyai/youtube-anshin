# Episode 009 pre-publish checklist

確認日: 2026-09-05  
現在地: **YouTube予約公開済み（非公開）**

## 完了

- [x] draft_v3の人間全編レビュー承認を記録
- [x] `human_draft_approved=true`
- [x] `senior_readability=PASS`
- [x] `approved_draft=draft_v3`
- [x] `output/final.mp4`をdraft_v3からcopy-onlyで作成
- [x] finalのSHA-256・サイズ・尺・映像／音声仕様を記録
- [x] H.264 1920×1080 30fps / AAC 48kHz
- [x] decode、黒画面、予期しない無音、Visual Gate v2回帰、字幕回帰、privacy、CTA回帰を確認
- [x] Fact Watch（24H2 / 25H2 / 26H1 / Windows 11全体ではない）をMicrosoft公式で再確認
- [x] `方`の残り2件を人間承認済みに変更し、未解決発音0を記録
- [x] `方`のglobal辞書登録がないことを確認
- [x] VOICEVOXクレジットをdescriptionに記載
- [x] measured timelineに基づくchaptersをpublish metadataへ反映
- [x] category_id=22 / default_language=ja / made_for_kids=falseを準備
- [x] End Screen予定（関連動画TBD / チャンネル登録）を記録
- [x] Episode 002 / 008比較のanalytics planを記録
- [x] ユーザー提供サムネイルを正式採用
- [x] 原本を `assets/thumbnail/thumbnail_source.png` に保存
- [x] 公開用サムネイルを1280×720 / 16:9へ最小crop・normalize
- [x] 25%縮小、文字、edge、Fact Boundary、privacy QA（PASS）

## 未完了・次の人間ゲート

- [x] `publish dry-run`（thumbnail確定後）
- [ ] YouTube StudioでEnd Screen（関連動画・チャンネル登録）を設定
- [x] OAuthアカウント・チャンネルIDを確認（承認済みIDと一致）
- [x] privateでアップロードし、2026-09-09 19:00 JSTを予約
- [x] API verify（video ID / title / privacyStatus / publishAt / AI disclosure）

## 停止確認

予約公開済み。video IDは `NO4ZwXPvgA0`、privacyStatusはprivate、publishAtは2026-09-09 19:00 JST。即時public化は実行していない。End ScreenはYouTube Studioでの手動設定待ち。
