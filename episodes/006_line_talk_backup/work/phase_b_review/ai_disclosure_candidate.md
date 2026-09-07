# Episode 006 AI素材の開示（概要欄）

- date: 2026-09-02
- 現状: Episode 001〜005の説明欄にはAI素材の開示文はない（003／005は `contains_synthetic_media` をYouTube APIへ反映したのみ）。Episode 006の説明欄にも未追加。
- 前提: GPT画像5枚（写実的な人物イラスト）を使うため、概要欄に1回だけ開示する。
- 提案（1文）:

> この動画の人物・イラストの一部はAIで生成した画像を使用しています。

- メモ:
  - 今回は動画本体への追加表示はしない（概要欄のみ）。
  - `publish.json` の `contains_synthetic_media` は、人間がGPT画像5枚を確認したのち `true/false` を確定する（現時点は暫定false＋`ai_disclosure_review: REVIEW_REQUIRED`）。
