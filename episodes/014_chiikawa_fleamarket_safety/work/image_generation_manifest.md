# GPT image generation manifest

Required images: 2

text_render_mode: imagegen_native = ImageGenで背景と文字を同時生成（QA必須）・pil_overlay = renderer-native背景へ正確な文字を後描画・no_text = 画像内に文字なし。生成画像＋大きな後乗せ文字は `NO_IMAGE_TEXT_HYBRID` により禁止。詳細は docs/text_render_policy.md。

## SCENE-001 — gpt_image / text_render_mode=imagegen_native

- filename: `scene_001.png`
- text_render_mode: `imagegen_native`
- fit_mode: `full_bleed`
- animation_default: `very_slow_zoom`
- text_qa: `PASS`（retry=1）
- status: `adopted_for_draft_v2`

### Text spec（imagegen_native文字QAの正）

- headline: `限定品を買う前に確認`
- support_text: `フリマで見つけたときの5つ`
- placement: upper-left quiet area, away from the person and merchandise
- style: large dark-blue Japanese type with a soft white outline, exact text, calm educational style
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: A calm, trustworthy editorial illustration for older Japanese viewers: a generic Japanese older adult at home carefully looking at a smartphone beside a plain unbranded gift box and a small generic acrylic merchandise item. No recognizable characters, no Chiikawa, no Hachiware, no Usagi, no mascots, no logos, no app UI, no readable labels. Soft blue and warm cream interior, realistic but clearly generic, subject on the right and a painted background on the left for exact Japanese headline text. Full-frame 16:9, no collage, no split panel, reserve the bottom 180 pixels for subtitles. Generation contract: render the declared Japanese text inside the image exactly as written (imagegen_native).

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
- text_qa: `PASS`（retry=0）
- status: `adopted_for_draft_v2`

### Text spec（imagegen_native文字QAの正）

- headline: `残り1個
どうする？`
- support_text: `架空の例`
- placement: upper-left painted background, integrated into the finished scene
- style: large dark-navy Japanese type; exact two-line headline with one short supporting line, high contrast and smartphone-readable
- aspect_ratio: 16:9

### Prompt

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy white, blue and green palette. Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented government logos, no unnecessary decoration. Scene direction: One finished standalone 16:9 image for a clearly fictional example in a calm Japanese YouTube educational video for viewers aged 50 to 70. A generic older Japanese adult on the right thoughtfully holds a blank smartphone at home beside one plain unbranded gift box and one generic small abstract acrylic-style merchandise item. The background continues naturally to every edge; do not make a collage, storyboard, split panel, grid, screenshot, blank white half, or large white card. Integrate the following exact Japanese text into the upper-left painted background as part of the finished image, with no later renderer text overlay: headline on two lines exactly "残り1個" then "どうする？"; one small supporting line exactly "架空の例". Render only those exact words and no other readable text. Use large dark-navy type, strong contrast, full visibility, safe margins, and reserve the bottom 180 pixels for subtitles. No Chiikawa, Hachiware, Usagi, mascots, character-like merchandise, human silhouette printed on merchandise, logos, watermark, official UI, marketplace UI, price, seller name, QR code, sign, label, or caption. Generation contract: render the declared Japanese text inside the image exactly as written (imagegen_native).

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

