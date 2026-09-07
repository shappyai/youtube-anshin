# Image Agent assignment — SCENE-013

- scene_id: SCENE-013
- output_path: `assets/generated_ai/scene_013.png`（この1ファイルのみ保存）
- purpose: 4/6セクション扉。スマホ本体の容量が空く概念（見出し「4 / 6」はCodex後描画）
- contract: 1 Agent = 1 scene = 1 image。collage・storyboard・split panel・variantsは作らない。他sceneのpromptは見ない/受け取らない。

## Prompt（このpromptのみで生成する）

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Clean, calm, reassuring palette (pale mint green, light blue, beige). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented logos, no unnecessary decoration. Scene direction: A clean, friendly illustration. On the right, a smartphone silhouette like a transparent glass case with a blank screen, inside which small boxes of photos change from being packed tight to being neatly emptied with soft light — the concept of device storage becoming free. On the left, a quiet, slightly textured wall in pale mint/white for later Codex Japanese text (not pure white). Keep the overall tone light and reassuring, no sense of danger. No text, no numbers, no logos, no brand marks, no phone UI. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

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
