# GPT image generation manifest

Required images: 1

text_render_mode: imagegen_native = ImageGenで背景と文字を同時生成（QA必須）・pil_overlay = 背景のみ生成しPIL/HTMLで文字後乗せ・no_text = 画像内に文字なし。詳細は docs/text_render_policy.md。

## SCENE-001 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_001.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `static`
- text_qa: `pending`（retry=0）
- status: `image_required`

### Text spec（imagegen_native文字QAの正）

- headline: `のんびり、いこう。`
- support_text: `今日もいい一日を。`
- placement: calm low-detail area, upper-left preferred
- style: white Japanese type with dark blue outline, high contrast
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: Render exact Japanese text inside the image, in this order: line 1: "のんびり、いこう。" and line 2: "今日もいい一日を。". Spell it correctly: no typos, no missing characters, no extra characters, no mojibake, no unnatural kanji substitution. Preserve the declared line order and do not merge or reorder lines. Place the text in a calm, low-detail area, upper-left preferred. Use white Japanese type with a dark blue outline, high contrast, large and legible. The main headline must stay readable when the image is scaled down to a smartphone thumbnail. Do not clip the text, do not let it touch the image edges, and do not place it over the main subject or important objects. Keep the bottom 180 pixels (subtitle-safe area) free of text and content.

### Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- presentation card layout unless explicitly required by the scene
- official UI or app screen
- real or invented government logo
- fake screenshot
- tiny or garbled Japanese text
- personal information
- content in the bottom 180px subtitle area

