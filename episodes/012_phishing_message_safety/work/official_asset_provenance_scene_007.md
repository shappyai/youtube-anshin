# SCENE-007 公式素材の根拠確認

確認日：2026-09-06

## 根本原因

旧 `assets/official/scene_007_nlc_keyphrase.png` は、国民生活センター公式PDF
`assets/official/_source/nlc_shinsen550.pdf` の実ページから切り出した画像だった。OCRや生成文章、取得失敗時のfallbackではない。

ただし、切り出し範囲が箇条書きの途中から始まる短い横長cropだったため、画面上では「記載されているURLにはアクセスせず、」だけが前後の文脈なしで見えた。公式素材としての出所は正しかったが、表示範囲の選定が不適切で、ナレーションと画面の日本語として不自然に見える原因になった。

## 採用したasset

旧cropは採用せず、同じ一次情報のPDFで確認できる一文を、意味が完結する短い引用として再構成した。

- scene：SCENE-007
- asset：`official_asset.kind=quote`
- 採用本文：`記載されているURLにはアクセスせず、事前にブックマークした正規サイトのURLや、正規のアプリからアクセスしましょう。`
- 出典表示：`出典：国民生活センター`
- source URL：`https://www.kokusen.go.jp/mimamori/pdf/shinsen550.pdf`
- provenance：`exact_quote_from_official_pdf`
- status：`exact_quote_verified`
- 採用判断：公式PDFの箇条書き本文と照合済み。言い換え・要約・OCR fallbackは使用しない。

表示は公式ページの不完全な画面らしく見せるのではなく、出典付きの正確なquote cardとした。原PDFと取得時のrenderは `assets/official/_source/` に保持し、採用assetの記録は `sources.md` と `media_manifest.csv` に残している。

表示上は意味の切れ目で4行に固定し、改行を除いた表示本文は上記の採用本文およびPDF本文と一致する。改行は表示専用で、引用本文の変更ではない。

## 取得失敗時の恒久ルール

`official_capture_failed` の場合はfail closedとし、抽出途中の文字・OCR・部分画像を公式素材として描画しない。復旧の優先順位は、同じ公式URLからの再取得、同じ一次情報の別表示、完全一致の短い引用＋出典、公式として見せないsemantic sceneの順とする。

詳細は `docs/official_capture_failure_policy.md` および `templates/scenes/README.md` の恒久ルールを参照。
