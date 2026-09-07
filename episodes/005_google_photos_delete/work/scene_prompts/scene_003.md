# Image Agent assignment — SCENE-003

- scene_id: SCENE-003
- output_path: `assets/generated_ai/scene_003.png`（この1ファイルのみ保存）
- purpose: 1/6セクション扉。バックアップ＝写真のコピーをGoogle側に預ける概念（見出し「1 / 6」はCodex後描画）
- contract: 1 Agent = 1 scene = 1 image。collage・storyboard・split panel・variantsは作らない。他sceneのpromptは見ない/受け取らない。

## Prompt（このpromptのみで生成する）

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy palette (soft blue, white clouds, gentle pastel). Strong visual hierarchy, one main message, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented logos, no unnecessary decoration. Scene direction: A soft storybook-style illustration. In the lower left, a smartphone silhouette with a plain blank screen; from it, several silhouettes of family photos flow upward as gentle ribbons of light into a small wooden storage chest resting on a cloud in the upper right (the concept of keeping a copy of your photos in a safe separate place). Sky has a calm blue-white gradient with fluffy clouds. Lower-left to center area is a quiet sky region for later Codex Japanese text (slightly light blue, not pure white). No text, no numbers, no logos, no brand names, no service names, no phone UI. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

## Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- presentation card layout
- Google Photos UI / app screen / phone UI
- real or invented logo (Google Photos, Google, Apple)
- fake screenshot
- tiny or garbled Japanese text, numbers, any readable text
- personal information
- content in the bottom 180px subtitle area

## Completion report

生成後、valid image、width / height、aspect ratio、file size、SHA-256を確認して親Codexへ返すこと。canonical file（episode.json等）は変更しない。
