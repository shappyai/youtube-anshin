# Thumbnail pipeline

thumbnailは本編scene pipelineから分離する。GPT画像の本編full-frame契約をthumbnailへそのまま強制せず、thumbnail専用の人間レビューを行う。

## 生成方式（Episode 007以降）

サムネイルは **`imagegen_native`（ImageGenで人物/背景/文字を一体生成）を第一候補** とする。

1. ImageGenで人物/背景/文字を一体生成
2. 文字QA（指定文言一致・誤字脱字・文字化け・行順・文字切れ・はみ出し・文字と人物の干渉・コントラスト・スマホ縮小時の可読性）がPASSなら採用
3. FAILならpromptを調整して1回だけ再生成
4. それでもNGなら生成画像を再利用せず、renderer-onlyで再構成（`scripts/make_thumbnail.py` 等の既存PIL描画を継続利用）

制約（従来と同じ）:

- 大きな文字、スマホ縮小でも読める短い表現
- 1つの疑問、1つの主役、高コントラスト
- 50〜70代が一目でテーマを理解できること
- 公式UIを使う場合、架空UIを事実画面として見せないこと
- タイトル全文を詰め込まない。主見出しは2〜6語の短い表現、小さい補助文字を増やしすぎない

本編draftの人間承認・finalize後にthumbnailを確定し、YouTube upload・予約・公開は別の公開前確認で行う。
