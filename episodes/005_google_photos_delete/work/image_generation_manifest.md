# GPT image generation manifest — Episode 005

Required images: 5

方針: 1 Image Agent = 1 scene = 1 image = 1 unique output path。GoogleフォトのUI・ロゴ・正確な日本語は生成しない。すべて `text_render_mode: codex`（文字はCodex後描画）・`fit_mode: full_bleed`。下部180pxは字幕安全領域。原本（1672×941等）は保持し、render時に1920×1080の正規化コピーを作る（人間確認後に生成開始）。

## SCENE-001 — gpt_image（導入）

- filename: `assets/generated_ai/scene_001.png`
- text_render_mode: `codex`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- status: `image_required`（未生成）

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, warm, trustworthy palette (cream, ivory, light brown). Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented logos, no unnecessary decoration. Scene direction: A realistic warm illustration of a Japanese woman in her 60s (gray hair, natural clothes) sitting on a sofa in a bright living room, looking at a smartphone in her hands with a gentle relieved smile. The phone screen is overexposed and blurred so no UI is identifiable. A few printed family photos lie on the coffee table in front. Keep the person on the right half; the left half is a quiet, slightly textured cream wall with a plant, reserved for later Codex Japanese text (not pure white). Warm natural light. No text, no numbers, no logos, no brand marks, no phone UI. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

### Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- presentation card layout unless explicitly required by the scene
- Google Photos UI / app screen / phone UI of any kind
- real or invented logo (Google Photos, Google, Apple)
- fake screenshot
- tiny or garbled Japanese text, numbers, or any readable text
- personal information
- content in the bottom 180px subtitle area

## SCENE-003 — gpt_image（1 / 6 セクション扉・バックアップ概念）

- filename: `assets/generated_ai/scene_003.png`
- text_render_mode: `codex`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- status: `image_required`（未生成）

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy palette (soft blue, white clouds, gentle pastel). Strong visual hierarchy, one main message, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented logos, no unnecessary decoration. Scene direction: A soft storybook-style illustration. In the lower left, a smartphone silhouette with a plain blank screen; from it, several silhouettes of family photos flow upward as gentle ribbons of light into a small wooden storage chest resting on a cloud in the upper right (the concept of keeping a copy of your photos in a safe separate place). Sky has a calm blue-white gradient with fluffy clouds. Lower-left to center area is a quiet sky region for later Codex Japanese text (slightly light blue, not pure white). No text, no numbers, no logos, no brand names, no service names, no phone UI. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

### Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- presentation card layout unless explicitly required by the scene
- Google Photos UI / app screen / phone UI
- real or invented logo (Google Photos, Google, Apple)
- fake screenshot
- tiny or garbled Japanese text, numbers, any readable text
- personal information
- content in the bottom 180px subtitle area

## SCENE-013 — gpt_image（4 / 6 セクション扉・容量が空く概念）

- filename: `assets/generated_ai/scene_013.png`
- text_render_mode: `codex`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- status: `image_required`（未生成）

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Clean, calm, reassuring palette (pale mint green, light blue, beige). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented logos, no unnecessary decoration. Scene direction: A clean, friendly illustration. On the right, a smartphone silhouette like a transparent glass case with a blank screen, inside which small boxes of photos change from being packed tight to being neatly emptied with soft light — the concept of device storage becoming free. On the left, a quiet, slightly textured wall in pale mint/white for later Codex Japanese text (not pure white). Keep the overall tone light and reassuring, no sense of danger. No text, no numbers, no logos, no brand marks, no phone UI. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

### Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- presentation card layout unless explicitly required by the scene
- Google Photos UI / app screen / phone UI
- real or invented logo (Google Photos, Google, Apple)
- fake screenshot
- tiny or garbled Japanese text, numbers, any readable text
- personal information
- content in the bottom 180px subtitle area

## SCENE-017 — gpt_image（5 / 6 セクション扉・本体写真とバックアップコピー）

- filename: `assets/generated_ai/scene_017.png`
- text_render_mode: `codex`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- status: `image_required`（未生成）

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy palette (soft blue-gray, gentle blue, warm wood tones). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented logos, no unnecessary decoration. Scene direction: A soft illustration showing a generic smartphone silhouette on the right with one family-photo card on it, and a gentle light ribbon creating a backup copy of the same photo card that flows toward a calm abstract cloud-shaped online storage symbol. Make the copy relationship clear: one photo on the phone, one backup copy flowing from it. Do not depict two independent photo libraries or two separate storage places. Place the subject on the right; the left half is a quiet, slightly textured blue-gray wall for later Codex Japanese text (not pure white). Do not draw any iPhone device illustration, any screen UI, any Apple logo, any Google Photos UI, any text, numbers, or brand marks. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

### Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- presentation card layout unless explicitly required by the scene
- iPhone device illustration, Apple UI, Apple logo, Google Photos UI
- two independent photo libraries or two separate storage places
- real or invented logo
- fake screenshot
- tiny or garbled Japanese text, numbers, any readable text
- personal information
- content in the bottom 180px subtitle area

## SCENE-025 — gpt_image（クロージング）

- filename: `assets/generated_ai/scene_025.png`
- text_render_mode: `codex`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- status: `image_required`（未生成）

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Warm, calm, reassuring palette (warm evening light, cozy home tones). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented logos, no unnecessary decoration. Scene direction: A warm realistic illustration of a Japanese couple in their 60s sitting side by side at a home dining table, both looking at one smartphone together with calm, reassured expressions and relaxed shoulders. The phone screen is slightly blurred so no UI is identifiable. Keep the couple on the right; the left half is a quiet wall with a small shelf (books, a teacup) for later Codex Japanese text (not pure white). Warm evening lighting, cozy, peaceful. No text, no numbers, no logos, no brand marks, no phone UI. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

### Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- presentation card layout unless explicitly required by the scene
- phone UI / app screen
- real or invented logo
- fake screenshot
- tiny or garbled Japanese text, numbers, any readable text
- personal information
- content in the bottom 180px subtitle area
