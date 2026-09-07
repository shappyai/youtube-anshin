# Episode 010 Thumbnail QA

- 確認日：2026-09-06
- 判定：**PASS**
- 原本：`assets/thumbnail/thumbnail_source.png`（1672×941、1,868,566 bytes）
- 公開用：`assets/thumbnail/thumbnail.png`（1280×720、1,147,245 bytes）
- 公開用SHA-256：`ffa2a968e3acf41b22220b17a2bfcaf2d4c1e5ab0539c3936884881b348b6860`
- 正規化：上下1px相当の比率調整とLANCZOS縮小のみ。文字・人物・構図・UIは変更していない。

## Visual checks

| 項目 | 結果 |
|---|---|
| 1280×720 / 16:9 | PASS |
| 2MB以内 | PASS |
| デコード | PASS |
| 指定コピー完全一致 | PASS |
| 文字切れ | 0 |
| 文字欠落 | 0 |
| 顔切れ | 0 |
| 25%縮小時の可読性 | PASS |
| watermark | 0 |
| viewer-facing内部Episode番号 | 0 |
| 公式サムネイルとの混同 | PASS（説明用ビジュアル） |

## Adopted copy

- マイナアプリ
- 最初に / 何する？
- 初めて使う人向け / やさしく解説

原本はユーザー指定のChatGPT生成画像。Codex/ImageGenによる再生成、文言変更、人物・UI変更は行っていない。
