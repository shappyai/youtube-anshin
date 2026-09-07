# Scene 022 prompt — IMG-002（クロージング・あわてずに確認しましょう）

- scene_id: 22
- output_path: assets/generated_ai/scene_022.png
- render_mode: gpt_image
- text_render_mode: imagegen_native（文字QA FAIL→1回再生成→2回目FAILはpil_overlayへfallback）
- overlay text（正とする文言）: headline「あわてずに、」「確認しましょう」（2行・左半分の静かな余白に配置）
- status: not_generated（Phase B）

## Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, warm, reassuring palette (soft cream, warm beige, gentle light). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half; the left half may be a quiet, slightly textured warm wall for Japanese text but must remain a real background. Reserve the bottom 180 pixels as a subtitle-safe area (keep empty). Scene direction: A gentle realistic illustration of a Japanese man or woman in their 60s sitting comfortably, looking at a smartphone with a calm, settled expression (phone screen overexposed and blurred, no UI identifiable). Keep the person on the right half; the left half is quiet. Render the exact Japanese text in-image, large and bold (approx 90-110px): line 1 "あわてずに、", line 2 "確認しましょう" — dark ink with strong contrast on the background, fully inside the frame, not overlapping the person, no text cut off, correct line order. No logos, no government marks, no phone UI, no readable numbers. Generation contract: one finished standalone scene image with the exact Japanese text rendered in-image; edge-to-edge; calm non-white background.

## Must not generate

- collage / storyboard / contact sheet / split panel / grid / multiple scenes
- blank white half / large empty white canvas
- app UI / logo / government mark / QR-like patterns / number-like strings
- tiny or garbled Japanese text, typos, extra characters, wrong line order, text cut off
- content inside the bottom 180px subtitle area

## 文字QA（生成後に確認）

指定文言一致「あわてずに、」「確認しましょう」／誤字・脱字・余計な文字／文字化け／行順／文字切れ・はみ出し／人物との重なり／コントラスト／スマホ縮小時の可読性
