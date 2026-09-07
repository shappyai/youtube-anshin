# GPT image generation manifest

Required images: 5

text_render_mode: imagegen_native = ImageGenで背景と文字を同時生成（QA必須）・pil_overlay = 背景のみ生成しPIL/HTMLで文字後乗せ・no_text = 画像内に文字なし。詳細は docs/text_render_policy.md。

## SCENE-001 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_001.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- text_qa: `pending`（retry=0）
- status: `image_required`

### Text spec（imagegen_native文字QAの正）

- headline: `11月に使えなくなる？`
- support_text: `全員ではありません。まず3つ確認`
- placement: calm low-detail area, upper-left preferred
- style: white Japanese type with dark blue outline, high contrast
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: Render exact Japanese text inside the image, in this order: line 1: "11月に使えなくなる？" and line 2: "全員ではありません。まず3つ確認". Spell it correctly: no typos, no missing characters, no extra characters, no mojibake, no unnatural kanji substitution. Preserve the declared line order and do not merge or reorder lines. Place the text in a calm, low-detail area, upper-left preferred. Use white Japanese type with a dark blue outline, high contrast, large and legible. The main headline must stay readable when the image is scaled down to a smartphone thumbnail. Do not clip the text, do not let it touch the image edges, and do not place it over the main subject or important objects. Keep the bottom 180 pixels (subtitle-safe area) free of text and content.

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

## SCENE-004 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_004.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- text_qa: `pending`（retry=0）
- status: `image_required`

### Text spec（imagegen_native文字QAの正）

- headline: `LINEのバージョンを確認`
- support_text: `まずアプリの数字を見る`
- placement: calm low-detail area, upper-left preferred
- style: white Japanese type with dark blue outline, high contrast
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: Render exact Japanese text inside the image, in this order: line 1: "LINEのバージョンを確認" and line 2: "まずアプリの数字を見る". Spell it correctly: no typos, no missing characters, no extra characters, no mojibake, no unnatural kanji substitution. Preserve the declared line order and do not merge or reorder lines. Place the text in a calm, low-detail area, upper-left preferred. Use white Japanese type with a dark blue outline, high contrast, large and legible. The main headline must stay readable when the image is scaled down to a smartphone thumbnail. Do not clip the text, do not let it touch the image edges, and do not place it over the main subject or important objects. Keep the bottom 180 pixels (subtitle-safe area) free of text and content.

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

## SCENE-008 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_008.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- text_qa: `pending`（retry=0）
- status: `image_required`

### Text spec（imagegen_native文字QAの正）

- headline: `スマホのOSを確認`
- support_text: `LINEとは別に見る`
- placement: calm low-detail area, upper-left preferred
- style: white Japanese type with dark blue outline, high contrast
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: Render exact Japanese text inside the image, in this order: line 1: "スマホのOSを確認" and line 2: "LINEとは別に見る". Spell it correctly: no typos, no missing characters, no extra characters, no mojibake, no unnatural kanji substitution. Preserve the declared line order and do not merge or reorder lines. Place the text in a calm, low-detail area, upper-left preferred. Use white Japanese type with a dark blue outline, high contrast, large and legible. The main headline must stay readable when the image is scaled down to a smartphone thumbnail. Do not clip the text, do not let it touch the image edges, and do not place it over the main subject or important objects. Keep the bottom 180 pixels (subtitle-safe area) free of text and content.

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

## SCENE-012 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_012.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- text_qa: `pending`（retry=0）
- status: `image_required`

### Text spec（imagegen_native文字QAの正）

- headline: `更新できるか確認`
- support_text: `3つ目は更新の可否`
- placement: calm low-detail area, upper-left preferred
- style: white Japanese type with dark blue outline, high contrast
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: Render exact Japanese text inside the image, in this order: line 1: "更新できるか確認" and line 2: "3つ目は更新の可否". Spell it correctly: no typos, no missing characters, no extra characters, no mojibake, no unnatural kanji substitution. Preserve the declared line order and do not merge or reorder lines. Place the text in a calm, low-detail area, upper-left preferred. Use white Japanese type with a dark blue outline, high contrast, large and legible. The main headline must stay readable when the image is scaled down to a smartphone thumbnail. Do not clip the text, do not let it touch the image edges, and do not place it over the main subject or important objects. Keep the bottom 180 pixels (subtitle-safe area) free of text and content.

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

## SCENE-022 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_022.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- text_qa: `pending`（retry=0）
- status: `image_required`

### Text spec（imagegen_native文字QAの正）

- headline: `買い替え前に確認`
- support_text: `LINE → OS → 次の手順`
- placement: calm low-detail area, upper-left preferred
- style: white Japanese type with dark blue outline, high contrast
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: Render exact Japanese text inside the image, in this order: line 1: "買い替え前に確認" and line 2: "LINE → OS → 次の手順". Spell it correctly: no typos, no missing characters, no extra characters, no mojibake, no unnatural kanji substitution. Preserve the declared line order and do not merge or reorder lines. Place the text in a calm, low-detail area, upper-left preferred. Use white Japanese type with a dark blue outline, high contrast, large and legible. The main headline must stay readable when the image is scaled down to a smartphone thumbnail. Do not clip the text, do not let it touch the image edges, and do not place it over the main subject or important objects. Keep the bottom 180 pixels (subtitle-safe area) free of text and content.

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

