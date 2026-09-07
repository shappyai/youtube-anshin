# GPT image generation manifest

Required images: 3

text_render_mode: imagegen_native = ImageGenで背景と文字を同時生成（QA必須）・pil_overlay = 背景のみ生成しPIL/HTMLで文字後乗せ・no_text = 画像内に文字なし。詳細は docs/text_render_policy.md。

## SCENE-001 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_001.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `static`
- text_qa: `pending`（retry=0）
- status: `image_required`

### Text spec（imagegen_native文字QAの正）

- headline: `Windows 11
このままで大丈夫？`
- support_text: `10月13日までに、確認すること`
- placement: calm low-detail area, upper-left preferred
- style: white Japanese type with dark blue outline, high contrast
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: Calm educational illustration for older Japanese viewers, one adult at home looking at a generic laptop with a mild concern turning into reassurance, soft blue and warm amber palette, abstract four-pane window-like shape without any trademark or logo, full-frame 16:9, clean composition with the bottom 180px left quiet for subtitles. Render exactly these two Japanese headline lines and no other readable text: Windows 11 / このままで大丈夫？. No real Windows UI, no Microsoft logo, no watermark, no extra symbols, no collage. Generation contract: render the declared Japanese text inside the image exactly as written (imagegen_native).

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

## SCENE-015 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_015.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- text_qa: `pending`（retry=0）
- status: `image_required`

### Text spec（imagegen_native文字QAの正）

- headline: `慌てて買い替えなくて大丈夫`
- support_text: `10月13日までに、まずバージョンと更新を確認`
- placement: calm low-detail area, upper-left preferred
- style: white Japanese type with dark blue outline, high contrast
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: Calm reassuring educational illustration for older Japanese viewers, an adult at home calmly checking a generic laptop beside a simple written checklist, hands relaxed, no shopping bags, no retail urgency, soft blue and pale amber palette, full-frame 16:9, bottom 180px quiet for subtitles. Render exactly one Japanese headline: 慌てて買い替えなくて大丈夫. No other readable text, no real Windows UI, no logo, no watermark, no collage, no fake warning badge. Generation contract: render the declared Japanese text inside the image exactly as written (imagegen_native).

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

## SCENE-019 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_019.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- text_qa: `pending`（retry=0）
- status: `image_required`

### Text spec（imagegen_native文字QAの正）

- headline: `まずバージョンを確認`
- support_text: `役に立ったら、チャンネル登録して、次回も一緒に確認しましょう。`
- placement: calm low-detail area, upper-left preferred
- style: white Japanese type with dark blue outline, high contrast
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: Warm reassuring educational illustration for older Japanese viewers, a calm adult checking a generic laptop settings page with a magnifying glass motif and a small support conversation cue, full-frame 16:9, soft blue and pale green palette, bottom 180px quiet for subtitles. Render exactly one Japanese headline: まずバージョンを確認. No other readable text, no real Windows UI, no Microsoft logo, no watermark, no collage. Generation contract: render the declared Japanese text inside the image exactly as written (imagegen_native).

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

