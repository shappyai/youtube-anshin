# Episode 006 公開前レビュー（work/publish_review）

- date: 2026-09-03
- 公開候補動画: `output/final.mp4`（draft_v2のcopy-only・SHA一致確認済み。約6分48秒・1920×1080・30fps・H.264・AAC 48kHz）

## 確認してほしいこと（1ページ要約）

1. **タイトル（推奨）**: 【LINE】機種変更の前に確認！トーク履歴を残すバックアップとPIN
   - 前半で「機種変更の前に確認する動画」と分かる。検索語（LINE・機種変更・トーク履歴・バックアップ・PIN）を含む。煽りなし。
   - 候補B: 【LINE】トーク履歴、消えない？機種変更・故障の前に確認したい3つ（従来の問いかけ型）
   - 候補C: 【LINE】機種変更してもトークを残す。今のスマホで確認する3つ
2. **サムネイル**: **正式採用（2026-09-03）** ＝ 人間作成新案 `assets/thumbnail/thumbnail.png`（1280×720・PNG）。主見出し「機種変更しても、トークは残る？」＋補助バナー＋日時確認/自動バックアップ/PINコードの3要素＋ブランド表示。旧案 `thumbnail_a.png`／`thumbnail_b.png` はレビュー用として保持。
3. **概要欄**: `final_metadata.txt` に完成版。動画で分かること・公式根拠8件・バージョン留保・AI開示文・チャンネルCTA・VOICEVOXクレジットを含む。
4. **チャプター**: 8件（実測タイミング基準。`final_chapters.txt`）。
5. **公式リンク**: 8件すべて2026-09-03にHTTP 200・リダイレクトなしを確認（LINE公式7件＋LINEみんなの使い方ガイド1件）。
6. **AI開示**: 概要欄に承認済み1文を反映。containsSyntheticMediaは **true推奨**（写実的AI人物イラスト5枚を使用。YouTube側のONは人間確認後）。
7. **公開設定候補**: category 22・ja・kids=false・tags 8件・private（確認後にscheduled可）。即時public・uploadは未実施。

## 公開前QA

- `pre_publish_qa.md`: **PASS**（ISSUES 0）
  - final.mp4再生可能・1920×1080・約6:48・AAC音声・CTAあり（動画末尾）
  - サムネイル2案とも1280×720
  - タイトル・概要欄・チャプターが動画内容と一致（narration/scene実時刻ベース）
  - TODO/draft/placeholder語なし・実PIN・個人情報なし・URL重複なし

## 決定後に進むこと（この工程では実施しない）

1. タイトル・サムネイル・概要欄を人間が確定 → publish.jsonへ確定反映
2. サムネイルを `assets/thumbnail/thumbnail.png` へ確定コピー
3. AI開示（containsSyntheticMedia）を人間が最終決定
4. YouTube dry-run → private/scheduled upload → verify → STATE更新
