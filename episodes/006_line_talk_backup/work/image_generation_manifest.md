# GPT image generation manifest — Episode 006

Required images: 5

方針: 1 Image Agent = 1 scene = 1 image = 1 unique output path。LINEの実際のUI・ロゴ・正確な日本語・QRコード・電話番号風の文字列は生成しない。すべて `text_render_mode: codex`（文字はCodex後描画）・`fit_mode: full_bleed`・`animation_default: very_slow_zoom`。下部180pxは字幕安全領域。原本（1672×941等）は保持し、render時に1920×1080の正規化コピーを作る。Phase B前半で5枚を生成・正規化・contact sheet化済み。人間レビュー待ち。

## SCENE-001 — gpt_image（導入）IMG-001

- filename: `assets/generated_ai/scene_001.png`
- purpose: 導入。機種変更・故障でLINEのトークが消えるのではという不安を、穏やかな光景で受け止める（安心を先に見せる）
- overlay text: headline「機種変更しても、\nトークは残る？」support「今のスマホで、3つのことを確認すれば、準備ができます。」（Codex後描画）
- status: `generated_review_pending`

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, warm, reassuring palette (soft cream, warm beige, gentle light). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. Scene direction: A gentle realistic illustration of a Japanese man or woman in their 60s sitting on a sofa, looking at a smartphone with a calm, slightly thoughtful but not worried expression. The phone screen is overexposed and blurred so no UI is identifiable. Keep the person on the right half; the left half is a quiet, slightly textured warm wall with a plant and a small clock, reserved for later Codex Japanese text (not pure white). Warm natural light. No text, no numbers, no logos, no brand marks, no phone UI, no QR-code-like patterns, no ID-card-like text. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

### Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- LINE UI / chat bubbles / app screen / any phone UI
- real or invented logo (LINE, LYP, iCloud, Google)
- fake screenshot, QR code, phone-number-like or ID-like strings
- tiny or garbled Japanese text, numbers, or any readable text
- personal information
- content in the bottom 180px subtitle area

## SCENE-003 — gpt_image（1/5 扉・二つの準備は別もの）IMG-002

- filename: `assets/generated_ai/scene_003.png`
- purpose: 「引き継ぎ（手続き）」と「バックアップ（コピー）」が別のものだという概念
- overlay text: headline「二つの準備は、\n別のもの」support「引き継ぎ＝手続き。バックアップ＝コピー。」（Codex後描画）
- status: `generated_review_pending`

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy palette (soft blue, gentle green, warm beige). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. Scene direction: A soft storybook-style illustration showing two different wooden storage chests standing side by side on a gentle path: one chest labeled by its shape as a "procedure/moving" chest with a small document-handover motif (no text), the other chest as a "copy" chest with a soft ribbon of light carrying small message-card silhouettes into it (no text). The two chests are clearly separate but equal, conveying two different preparations. Use simple shapes, no readable text, no letters, no digits. Keep the main subject on the right to center; the left half is a quiet, slightly textured wall for later Codex Japanese text (not pure white). No service logos, no brand marks, no phone UI, no chat bubbles. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

### Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- any real service name rendered as text (LINE, LINEアプリ表記) or logo
- phone UI, chat bubbles, QR code, phone-number-like or ID-like strings
- tiny or garbled Japanese text, numbers, or any readable text
- personal information
- content in the bottom 180px subtitle area

## SCENE-015 — gpt_image（4/5 扉・PIN=鍵）IMG-003

- filename: `assets/generated_ai/scene_015.png`
- purpose: 「コピーを守る鍵」の概念（バックアップ用の暗証番号PIN）
- overlay text: headline「コピーを守る、\n鍵のようなもの」support「三つ目の確認は、バックアップ用の暗証番号、PINコードです。」（Codex後描画）
- status: `generated_review_pending`

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, safe, reassuring palette (soft warm gold, gentle cream, light brown). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. Scene direction: A soft illustration of a large friendly brass key standing in front of a small wooden treasure chest that gently glows from inside, representing protecting a precious copy with a key. No keypad, no digits, no PIN screen, no phone, no UI. Keep the subject on the right; the left half is a quiet, slightly textured warm wall for later Codex Japanese text (not pure white). Warm lighting. No text, no numbers, no logos, no brand marks, no QR-code-like patterns. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

### Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- PIN entry screen, keypad, digits, or any numeric UI
- phone UI, chat bubbles, any real or invented logo (LINE, LYP, iCloud, Google)
- fake screenshot, QR code, phone-number-like or ID-like strings
- tiny or garbled Japanese text, numbers, or any readable text
- personal information
- content in the bottom 180px subtitle area

## SCENE-019 — gpt_image（5/5 扉・OSをまたぐ）IMG-004

- filename: `assets/generated_ai/scene_019.png`
- purpose: 「OSをまたぐ機種変更」の概念（両OSの違いは色だけで暗示）
- overlay text: headline「OSをまたぐ\n機種変更に注意」support「AndroidとiPhoneでは、引き継げる範囲が変わります。」（Codex後描画）
- status: `generated_review_pending`

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy palette (soft blue and warm orange accents, gentle pastel). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. Scene direction: A soft illustration of two gentle island shapes in different colors (one cool blue, one warm orange) separated by water, connected by a simple curved wooden bridge. A small light at the center of the bridge marks a crossing. No smartphones, no device silhouettes, no logos, no brand marks. Keep the islands on the right to center; the left half is a quiet, slightly textured light wall for later Codex Japanese text (not pure white). No text, no numbers, no letters, no readable characters. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

### Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- iPhone/Android device illustrations, logos, or brand marks
- phone UI, chat bubbles, fake screenshot, QR code, phone-number-like or ID-like strings
- tiny or garbled Japanese text, numbers, or any readable text
- personal information
- content in the bottom 180px subtitle area

## SCENE-025 — gpt_image（クロージング）IMG-005

- filename: `assets/generated_ai/scene_025.png`
- purpose: 「あわてずに確認する」安心のクロージング
- overlay text: headline「あわてずに、\n確認しましょう」support「今のスマホで、すぐに確認できます。」（Codex後描画）
- status: `generated_review_pending`

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Warm, calm, reassuring palette (warm evening light, cozy home tones). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. Scene direction: A warm realistic illustration of a Japanese couple in their 60s sitting side by side at a home dining table, both looking at one smartphone together with calm, reassured expressions and relaxed shoulders. The phone screen is slightly blurred so no UI is identifiable. Keep the couple on the right; the left half is a quiet wall with a small shelf (books, a teacup) for later Codex Japanese text (not pure white). Warm evening lighting, cozy, peaceful. No text, no numbers, no logos, no brand marks, no phone UI, no QR-code-like patterns. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

### Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- LINE UI / chat bubbles / app screen / any phone UI
- real or invented logo (LINE, LYP, iCloud, Google)
- fake screenshot, QR code, phone-number-like or ID-like strings
- tiny or garbled Japanese text, numbers, or any readable text
- personal information
- content in the bottom 180px subtitle area

## Phase B実績

- 生成Agent: 5（SCENE-001 / 003 / 015 / 019 / 025）。1 sceneにつき1枚、保存先も重複なし。
- 生成後の原本は `assets/generated_ai/` に保持。1672×941の3枚を含む。
- 正規化copyは `work/phase_b_review/normalized_ai/` に5枚、すべて1920×1080。下180pxは字幕帯として確保。
- `work/phase_b_review/gpt_image_contact_sheet.png` で、scene取り違え・重複・collage・split panel・大きな白抜き・生成文字の有無を人間確認する。
- AI開示は未確定。写実的な人物・sceneに該当するかを人間レビュー後に `publish.json` で決める。

| Scene | 原本 | 原本サイズ | 原本SHA-256 | 正規化copy |
|---:|---|---:|---|---|
| 001 | `assets/generated_ai/scene_001.png` | 1920×1080 | `e2d1862e3997e5e8c3768b20c4e0f45a520aeec42ffef0d8774b278ca584a079` | `work/phase_b_review/normalized_ai/scene_001.png` |
| 003 | `assets/generated_ai/scene_003.png` | 1672×941 | `ad4c2042b6e5a97a9d9a24ffd970dc56335bbdb94381725bef9fa83757680f17` | `work/phase_b_review/normalized_ai/scene_003.png` |
| 015 | `assets/generated_ai/scene_015.png` | 1672×941 | `c3bf62c709ced2d1cf41e1557c1412ab038294aca83eda3e6089ffb53e66c1a7` | `work/phase_b_review/normalized_ai/scene_015.png` |
| 019 | `assets/generated_ai/scene_019.png` | 1672×941 | `003907e0195a9cca6c0b2d04ab7fa14dc619629fe4300acae2c8a7fdcc0cff3b` | `work/phase_b_review/normalized_ai/scene_019.png` |
| 025 | `assets/generated_ai/scene_025.png` | 1920×1080 | `e1ad0a5e513440d863bfd69a8abd5e03aab6a73a08ea3cfa92f91e50a84e86cb` | `work/phase_b_review/normalized_ai/scene_025.png` |

## 投入ルール（Phase Bで適用）

- 1 Image Agent = 1 scene = 1 image = 1 unique output path（`assets/generated_ai/<scene_id>.png`）。
- 各Image Agentには担当sceneのpromptだけを渡す（manifest全文・他sceneのpromptを渡さない）。
- 生成後は各Agentがvalid image・width/height・aspect ratio・file size・SHA-256を確認して親Codexへ返す。canonical fileは変更しない。
- 全Agent完了後に親Codexが接触sheetを作成し、人間が内容・重複・余白・読みやすさを確認。NG sceneのみ再生成。
