# GPT image generation manifest — Episode 007

Required images: 2

方針: 1 Image Agent = 1 scene = 1 image = 1 unique output path。マイナアプリ／マイナポータルの実UI・ロゴ・政府マーク・QRコード・番号風文字列は生成しない。両方とも `text_render_mode: imagegen_native`（背景と文字を同時生成）を既定とし、文字QA FAIL→1回だけ再生成→2回目もFAILなら `pil_overlay` へfallback（3回以上回さない）。原本（1672×941等）は保持し、render時に1920×1080の正規化copyを作る。下部180pxは字幕安全領域。Phase Bで生成する（Phase Aでは未生成）。

全scene共通の禁止事項:

- collage, storyboard, contact sheet, split panel, grid, 複数シーン
- 空白の白い半分・大きな空白キャンバス
- マイナアプリ/マイナポータルの実UI・アプリ画面・ロゴ・政府マーク・記章
- 実在のマイナンバーカード券面（氏名・住所・生年月日・顔写真・マイナンバー・QRコード風パターン・カード番号風文字列）
- 実在の電話番号・ID風の数字列
- 小さくて読めない日本語文字・文字化け・誤字
- 下部180px（1080pでy≥900）へのコンテンツ配置

## SCENE-007 — gpt_image（2/5 扉・カードを読み取る概念）IMG-001

- filename: `assets/generated_ai/scene_007.png`
- purpose: 「カードを読み取る」セクション扉。実際のUI・実演ではなく、スマホとカードの読み取り位置の概念を穏やかに示す
- overlay text: headline「カードを、読み取る」support「スマホとカードの、向きと場所。」（imagegen_nativeで同時生成。行数2行・配置は左半分の静かな余白）
- status: `not_generated`（Phase Bで生成）

### Prompt（Phase B Image Agent向け・要約）

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, reassuring, trustworthy palette (soft white, warm beige, gentle pink accents that echo the official app color without copying the logo). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area; the left 45% may be a quiet background area reserved for Japanese text but must remain a real background. Reserve the bottom 180 pixels as a subtitle-safe area (keep empty). Scene direction: A soft, storybook-style illustration of a smartphone (screen overexposed and blurred so no UI is identifiable) held slightly above a my number card (card details such as name, number, QR-like pattern not shown; show only a clean blank card silhouette with the chip area gently indicated). Tender light arcs/ripples between the upper-back area of the phone and the card suggest contactless reading (no text, no letters, no digits). Keep the objects on the right-center; the left half stays quiet for the Japanese text lines: line 1 "カードを、読み取る", line 2 "スマホとカードの、向きと場所。" Large, bold, highly readable Japanese text (approx 90-110px height for the headline), dark ink color with good contrast on the background, centered in the left text area, not overlapping the objects, fully inside the frame, no text cut off. No logos, no government marks, no QR-like patterns, no phone UI, no readable card data. Generation contract: this is one finished standalone scene image with the exact Japanese text rendered in-image; edge-to-edge; calm non-white background.

### Must not generate

- collage / storyboard / contact sheet / split panel / grid / multiple scenes
- blank white half / large empty white canvas
- real myna / myna portal app UI, logo, government mark, emblem
- readable card personal data (name, address, DOB, photo, my number, QR-like pattern, card-number-like strings)
- tiny or garbled Japanese text, typos, extra characters, wrong line order
- content inside the bottom 180px subtitle area

## SCENE-022 — gpt_image（クロージング・あわてずに確認しましょう）IMG-002

- filename: `assets/generated_ai/scene_022.png`
- purpose: クロージング。安心感で締め、まとめからCTAへつなぐ
- overlay text: headline「あわてずに、確認しましょう」support（省略。headlineのみ1行でも可）
- status: `not_generated`（Phase Bで生成）

### Prompt（Phase B Image Agent向け・要約）

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, warm, reassuring palette (soft cream, warm beige, gentle light). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half; the left half may be a quiet, slightly textured warm wall for Japanese text but must remain a real background. Reserve the bottom 180 pixels as a subtitle-safe area. Scene direction: A gentle realistic illustration of a Japanese man or woman in their 60s sitting comfortably, looking at a smartphone with a calm, settled expression (phone screen overexposed and blurred, no UI identifiable). Keep the person on the right half; the left half is quiet. Render the exact Japanese text in-image, large and bold (approx 90-110px): line 1 "あわてずに、", line 2 "確認しましょう" — dark ink with strong contrast, fully inside the frame, not overlapping the person, no text cut off. No logos, no government marks, no phone UI, no readable numbers. One finished standalone scene; edge-to-edge; calm non-white background.

### Must not generate

- collage / storyboard / contact sheet / split panel / grid / multiple scenes
- blank white half / large empty white canvas
- app UI / logo / government mark / QR-like patterns / number-like strings
- tiny or garbled Japanese text, typos, extra characters, wrong line order
- content inside the bottom 180px subtitle area

## Wave割当（Phase Bで実施）

- 2 Image Agents（1 agent = 1 scene = 1 image）を並列起動してよい（独立scene）。
- 各agentには担当sceneのprompt・output pathのみ渡す（他sceneのprompt・manifest全文は渡さない）。
- 生成後にwidth/height・aspect ratio・file size・SHA-256と、imagegen_native文字QA（指定文言一致・誤字・脱字・文字化け・行順・切れ・はみ出し・重なり・コントラスト・縮小時可読性）を確認して返す。NGは1回だけ再生成、2回目NGはpil_overlayへfallbackし、親CodexがPIL描画で文字を重ねる。

## 進捗（2026-09-03・画像生成サービス障害の影響）

- **SCENE-003（1/5扉）: 正式採用済み・生成完了**（A/B Candidate A。原本1672×941→`assets/generated_ai/scene_003.png` 1920×1080正規化。exact text PASS・安全領域PASS・再生成0回・fallback 0）
- **SCENE-011 / SCENE-014 / SCENE-017（section扉・imagegen_native）: 割当確定・生成待ち**。画像生成サービスの一時障害（HTTP 404）により未生成。復旧後に本manifestの表示文言で1 scene = 1 generation を実行する。
- **SCENE-007 / SCENE-022（concept画像・text-integrated指定あり）: 割当確定・生成待ち**（同上）。
- 生成時は上記各sceneのprompt（scene_prompts/）を1対1で使用し、他sceneのprompt・manifest全文を混在させない。complete後はexact text QA他（docs/text_render_policy.md セクション10）をPASSしたものだけ採用、FAIL時は1回再生成→2回目不安定なら該当sceneのみpil_overlayへfallback。

## SCENE-011 — gpt_image（3/5 扉・暗証番号で、止まる）IMG-003

- filename: `assets/generated_ai/scene_011.png`（予定）
- overlay text: headline「暗証番号で、止まる」support「使うのは、数字4桁。」
- text_render_mode: imagegen_native（文字QA FAIL→1回再生成→2回目FAILはpil_overlayへfallback）
- visual direction: やわらかい鍵/暗証番号パッドの概念（過去の実在UI・本物の番号・QRは生成しない）。白/ソフトブルー系・紺見出し・TV可読・下180px字幕帯
- status: `pending`（画像生成サービス復旧待ち）

## SCENE-014 — gpt_image（4/5 扉・カードと、証明書の期限）IMG-004

- filename: `assets/generated_ai/scene_014.png`（予定）
- overlay text: headline「カードと、証明書の期限」support「期限は、別もの。」
- text_render_mode: imagegen_native（同上）
- visual direction: カレンダーと2つの期限ブロックの概念（実在UI・日付・番号は生成しない）。白/ソフトブルー系
- status: `pending`

## SCENE-017 — gpt_image（5/5 扉・それでも、ダメなら）IMG-005

- filename: `assets/generated_ai/scene_017.png`（予定）
- overlay text: headline「それでも、ダメなら」support「再設定・メンテナンス・公式窓口。」
- text_render_mode: imagegen_native（同上）
- visual direction: 相談窓口/電話受話器の穏やかな概念（実在UI・電話番号・QRは生成しない）。白/ソフトブルー系
- status: `pending`
