# Scene 007 prompt — IMG-001（2/5 扉・カードを読み取る概念）

- scene_id: 7
- output_path: assets/generated_ai/scene_007.png
- render_mode: gpt_image
- text_render_mode: imagegen_native（文字QA FAIL→1回再生成→2回目FAILはpil_overlayへfallback）
- overlay text（正とする文言）: headline「カードを、読み取る」support「スマホとカードの、向きと場所。」（2行・左半分の静かな余白に配置）
- status: not_generated（Phase B）

## Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, reassuring, trustworthy palette (soft white, warm beige, gentle pink accents that echo the official app color without copying the logo). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area; the left 45% may be a quiet background area reserved for Japanese text but must remain a real background. Reserve the bottom 180 pixels as a subtitle-safe area (keep empty). Scene direction: A soft, storybook-style illustration of a smartphone (screen overexposed and blurred so no UI is identifiable) held slightly above a my number card (card details such as name, number, QR-like pattern not shown; show only a clean blank card silhouette with the chip area gently indicated). Tender light arcs/ripples between the upper-back area of the phone and the card suggest contactless reading (no text, no letters, no digits). Keep the objects on the right-center; the left half stays quiet. Render the exact Japanese text in-image: line 1 "カードを、読み取る", line 2 "スマホとカードの、向きと場所。" Large, bold, highly readable Japanese text (approx 90-110px height for the headline), dark ink color with strong contrast, placed in the quiet left text area, not overlapping the objects, fully inside the frame, no text cut off, correct line order. No logos, no government marks, no QR-like patterns, no phone UI, no readable card data. Generation contract: one finished standalone scene image with the exact Japanese text rendered in-image; edge-to-edge; calm non-white background.

## Must not generate

- collage / storyboard / contact sheet / split panel / grid / multiple scenes
- blank white half / large empty white canvas
- real myna app / myna portal app UI, logo, government mark, emblem
- readable card personal data (name, address, DOB, photo, my number, QR-like pattern, card-number-like strings)
- tiny or garbled Japanese text, typos, extra characters, wrong line order, text cut off
- content inside the bottom 180px subtitle area

## 文字QA（生成後に確認）

指定文言一致「カードを、読み取る」「スマホとカードの、向きと場所。」／誤字・脱字・余計な文字／文字化け／行順／文字切れ・はみ出し／重要オブジェクトとの重なり／コントラスト／スマホ縮小時の可読性
