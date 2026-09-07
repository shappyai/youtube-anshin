# Episode 011 draft_v2 visual QA

確認日：2026-09-06

## Result

- status：`PASS_WITH_HUMAN_REVIEW`
- 代表フレーム：20枚
- contact sheet：`draft_v2_contact_sheet.png`
- scene quality：19 scenes / FAIL 0 / WARN 0
- 解像度：全scene 1920×1080

## SCENE-018

- `render_mode`：`gpt_image`
- `text_render_mode`：`imagegen_native`
- 1枚のImageGen出力に背景・人物・主文・補助文を含めた。
- 主文は `迷ったら、` / `その場で決めない` と一致。
- 補助文は `いったん止まって、` / `公式から確認` と一致。
- 文字QA：PASS。余計な文字・文字切れ・文字化けなし。
- post text overlay：0
- pil_overlay fallback：0
- 下部字幕安全帯：確保
- 右側End Screen reserved領域：確保

## Viewer-facing scan

- `怖がらせる前に、確認する。`：視聴者向け0件
- 内部metadataのブランド定義：保持
- story resolution：`迷ったら、その場で決めない` → `いったん止まって、公式から確認` → 確認後に手続きを進める、でPASS

## Other checks

- SCENE-003公式核心：既存修正版を継続使用
- 中盤CTA：1回、音声6.496秒、7秒上限PASS
- 終了CTA：Episode010実使用 `registration_conversion_v1` と照合PASS
- 電話番号：`0120-95-0178` / `#9110` / `110` / `5番` の機械QA PASS
- 字幕：39 cue、TTS reading leakage 0、FAIL 0
- 人間確認：発音、字幕の読みやすさ、SCENE-018 native文字、AI disclosure要否を全編で確認する
