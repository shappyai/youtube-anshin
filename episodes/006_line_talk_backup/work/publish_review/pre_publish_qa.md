# Episode 006 公開前QA（2026-09-03）

- status: PASS
- サムネイル確定済み: 人間新案を正式採用（`assets/thumbnail/thumbnail.png`・1280×720・PNG正常・文字/人物切れなし・一覧サイズで主見出し読取可）

## 確認結果
- final.mp4 size: 32140024 bytes
- final.mp4 duration: 408.0s (6:48) / 1920x1080 30fps h264 / aac 48kHz (ffprobe確認済み)
- title / description: episode.json と publish.json で同期
- chapters: 8件（すべて動画尺内）
- public text: TODO/draft/placeholder 語なし
- AI disclosure: 概要欄に1文あり
- channel CTA: 概要欄に1文あり
- source_urls: 8件・重複0。LINE公式 7件 / その他 1件（guide.line.me）
- link check: 8件すべてHTTP 200・リダイレクトなし（2026-09-03 HEAD確認）
- thumbnails: a/b とも 1280x720
- 公開設定候補: private / visibility=private / scheduled_at=None（未設定）
- category_id=22 made_for_kids=False default_language=ja
- AI disclosure review: REVIEW_REQUIRED（人間最終判断待ち）

## ISSUES
- なし

## 対象
- 公開候補: C:\Codex\260829_youtube-anshin\episodes\006_line_talk_backup\output\final.mp4
- thumbnail: C:\Codex\260829_youtube-anshin\episodes\006_line_talk_backup\work\publish_review\thumbnail_a.png（推奨） / C:\Codex\260829_youtube-anshin\episodes\006_line_talk_backup\work\publish_review\thumbnail_b.png
