# GPT image generation manifest

Required images: 6

text_render_mode: imagegen_native = ImageGenで背景と文字を同時生成（QA必須）・pil_overlay = 背景のみ生成しPIL/HTMLで文字後乗せ・no_text = 画像内に文字なし。詳細は docs/text_render_policy.md。

## SCENE-001 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_001.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- text_qa: `pending`（retry=0）
- status: `image_required`

### Text spec（imagegen_native文字QAの正）

- headline: `リンクから入らない`
- support_text: `公式を自分で開く`
- placement: calm low-detail area, upper-left preferred
- style: white Japanese type with dark blue outline, high contrast
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: Render exact Japanese text inside the image, in this order: line 1: "リンクから入らない" and line 2: "公式を自分で開く". Spell it correctly: no typos, no missing characters, no extra characters, no mojibake, no unnatural kanji substitution. Preserve the declared line order and do not merge or reorder lines. Place the text in a calm, low-detail area, upper-left preferred. Use white Japanese type with a dark blue outline, high contrast, large and legible. The main headline must stay readable when the image is scaled down to a smartphone thumbnail. Do not clip the text, do not let it touch the image edges, and do not place it over the main subject or important objects. Keep the bottom 180 pixels (subtitle-safe area) free of text and content.

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

## SCENE-005 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_005.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- text_qa: `pending`（retry=0）
- status: `image_required`

### Text spec（imagegen_native文字QAの正）

- headline: `支払い方法の更新`
- support_text: `1 / 5　通販・普段使うアプリ`
- placement: calm low-detail area, upper-left preferred
- style: white Japanese type with dark blue outline, high contrast
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: Render exact Japanese text inside the image, in this order: line 1: "支払い方法の更新" and line 2: "1 / 5　通販・普段使うアプリ". Spell it correctly: no typos, no missing characters, no extra characters, no mojibake, no unnatural kanji substitution. Preserve the declared line order and do not merge or reorder lines. Place the text in a calm, low-detail area, upper-left preferred. Use white Japanese type with a dark blue outline, high contrast, large and legible. The main headline must stay readable when the image is scaled down to a smartphone thumbnail. Do not clip the text, do not let it touch the image edges, and do not place it over the main subject or important objects. Keep the bottom 180 pixels (subtitle-safe area) free of text and content.

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

## SCENE-010 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_010.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- text_qa: `pending`（retry=0）
- status: `image_required`

### Text spec（imagegen_native文字QAの正）

- headline: `再配達のお願い`
- support_text: `2 / 5　宅配・SMS`
- placement: calm low-detail area, upper-left preferred
- style: white Japanese type with dark blue outline, high contrast
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: Render exact Japanese text inside the image, in this order: line 1: "再配達のお願い" and line 2: "2 / 5　宅配・SMS". Spell it correctly: no typos, no missing characters, no extra characters, no mojibake, no unnatural kanji substitution. Preserve the declared line order and do not merge or reorder lines. Place the text in a calm, low-detail area, upper-left preferred. Use white Japanese type with a dark blue outline, high contrast, large and legible. The main headline must stay readable when the image is scaled down to a smartphone thumbnail. Do not clip the text, do not let it touch the image edges, and do not place it over the main subject or important objects. Keep the bottom 180 pixels (subtitle-safe area) free of text and content.

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

## SCENE-016 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_016.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- text_qa: `pending`（retry=0）
- status: `image_required`

### Text spec（imagegen_native文字QAの正）

- headline: `カードの利用確認`
- support_text: `3 / 5　通知が本物でも、入口は自分で`
- placement: calm low-detail area, upper-left preferred
- style: white Japanese type with dark blue outline, high contrast
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: Render exact Japanese text inside the image, in this order: line 1: "カードの利用確認" and line 2: "3 / 5　通知が本物でも、入口は自分で". Spell it correctly: no typos, no missing characters, no extra characters, no mojibake, no unnatural kanji substitution. Preserve the declared line order and do not merge or reorder lines. Place the text in a calm, low-detail area, upper-left preferred. Use white Japanese type with a dark blue outline, high contrast, large and legible. The main headline must stay readable when the image is scaled down to a smartphone thumbnail. Do not clip the text, do not let it touch the image edges, and do not place it over the main subject or important objects. Keep the bottom 180 pixels (subtitle-safe area) free of text and content.

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

## SCENE-020 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_020.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- text_qa: `pending`（retry=0）
- status: `image_required`

### Text spec（imagegen_native文字QAの正）

- headline: `料金が未払いです`
- support_text: `4 / 5　携帯会社・通信料金`
- placement: calm low-detail area, upper-left preferred
- style: white Japanese type with dark blue outline, high contrast
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: Render exact Japanese text inside the image, in this order: line 1: "料金が未払いです" and line 2: "4 / 5　携帯会社・通信料金". Spell it correctly: no typos, no missing characters, no extra characters, no mojibake, no unnatural kanji substitution. Preserve the declared line order and do not merge or reorder lines. Place the text in a calm, low-detail area, upper-left preferred. Use white Japanese type with a dark blue outline, high contrast, large and legible. The main headline must stay readable when the image is scaled down to a smartphone thumbnail. Do not clip the text, do not let it touch the image edges, and do not place it over the main subject or important objects. Keep the bottom 180 pixels (subtitle-safe area) free of text and content.

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

## SCENE-024 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_024.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- text_qa: `pending`（retry=0）
- status: `image_required`

### Text spec（imagegen_native文字QAの正）

- headline: `公的なお知らせ`
- support_text: `5 / 5　役所・公的機関を装う連絡`
- placement: calm low-detail area, upper-left preferred
- style: white Japanese type with dark blue outline, high contrast
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: Render exact Japanese text inside the image, in this order: line 1: "公的なお知らせ" and line 2: "5 / 5　役所・公的機関を装う連絡". Spell it correctly: no typos, no missing characters, no extra characters, no mojibake, no unnatural kanji substitution. Preserve the declared line order and do not merge or reorder lines. Place the text in a calm, low-detail area, upper-left preferred. Use white Japanese type with a dark blue outline, high contrast, large and legible. The main headline must stay readable when the image is scaled down to a smartphone thumbnail. Do not clip the text, do not let it touch the image edges, and do not place it over the main subject or important objects. Keep the bottom 180 pixels (subtitle-safe area) free of text and content.

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

