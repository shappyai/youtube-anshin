# Episode 008 公開前チェックリスト（2026-09-05時点）

公開作業は、人間承認済みのfinalとサムネイルを対象に行う。YouTube upload・予約公開・サムネイル設定は完了し、End Screen実設定はYouTube Studioで人間が行う。

## 動画本体

- [x] `output/final.mp4` 作成（`draft_v3.mp4`からbyte-identical copy、再encodeなし）
- [x] Final QA PASS（decode error 0 / black frame 0 / unexpected silence 0）
- [x] Visual Gate v5 regression 0
- [x] 字幕 regression 0、v2のSRT/ASS/timingを再利用
- [ ] final.mp4をPCで通し視聴（映像・音声・字幕）
- [ ] final.mp4をスマホで通し視聴（文字の読みやすさ・音量）
- [x] `信用`・`今だけ`・`188`・`0570-050588`・CTA全文の最終人間確認（ユーザー承認済み）

## サムネイル

- [x] 原本保存: `assets/thumbnail/thumbnail_source.png`
- [x] 正式採用: `assets/thumbnail/thumbnail.png`
- [x] 1280×720、16:9、decode PASS
- [x] 25%版 `work/thumbnail_review/thumbnail_25.png` で大見出しを確認
- [x] 文字切れ・主要メッセージの小さすぎ・個人情報・口座番号・QRコード・実在著名人なし
- [x] A/B/C候補・imagegen_native再生成なし

## メタデータ

- [x] selected title: `【投資詐欺】その有名人、本物？LINEに誘導されたら確認したい3つ`
- [x] descriptionに主要根拠URL、確認日、VOICEVOXクレジットを含む
- [x] `contains_synthetic_media=true`（YouTube `videos.update` 応答で `containsSyntheticMedia=true` を確認）
- [x] privacy: private、publishAt: `2026-09-08T10:00:00Z`（2026-09-08 19:00 JST）
- [ ] 概要欄・チャプター・固定コメントを公開画面で人間確認

## 最新統計watch

- [x] 2026-09-05確認: 警察庁の最新掲載は「令和8年7月末・暫定値」
- [x] 「令和8年8月末・暫定値」の新規掲載なし
- [ ] 公開直前に再確認し、更新があれば本編を勝手に変更せず人間判断

根拠: [警察庁 統計ページ](https://www.npa.go.jp/publications/statistics/sousa/sagi.html)

## End Screen予定

- [ ] RELATED VIDEO: Episode004「【ニセ警察詐欺】『警察です』と電話が来たら？」
- [ ] SUBSCRIBE: チャンネル登録
- [ ] YouTube Studioで人間が実設定（動画側の焼き込み・疑似subscribeなし）

## YouTube upload・予約公開（2026-09-05）

- [x] 対象: `output/final.mp4`、SHA-256 `92166d59c228baff67ad32280899066ad050ff6c715646d773427ccba04f2854`
- [x] チャンネルID一致: `UCgVRceTJYO5KOrPX4w2jXZw`
- [x] YouTube video ID: `GryqJ70DCHs`
- [x] selected title・description・category・languageをAPIへ反映
- [x] `privacyStatus=private`、`selfDeclaredMadeForKids=false`
- [x] `containsSyntheticMedia=true`（status-only update、video ID不変、再アップロードなし）
- [x] `publishAt=2026-09-08T10:00:00Z`（2026-09-08 19:00 JST）をAPIで検証
- [x] サムネイル設定: `thumbnails.set`成功、`hasCustomThumbnail=true`
- [x] 重複アップロードなし
- [ ] YouTube StudioでEnd Screenを人間設定（RELATED VIDEO: Episode004／SUBSCRIBE: チャンネル登録）
- [ ] 公開後analytics確認

検証ログ: `work/youtube_publish/youtube_upload_log.md`。`videos.list`では`containsSyntheticMedia`が省略されたため、直前の`videos.update`応答を根拠に開示設定を確認した。
