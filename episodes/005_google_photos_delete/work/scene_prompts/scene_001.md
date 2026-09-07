# Image Agent assignment — SCENE-001

- scene_id: SCENE-001
- output_path: `assets/generated_ai/scene_001.png`（この1ファイルのみ保存）
- purpose: 導入。写真整理に困るシニアの安心感（headline「写真を消す前に、確認すること」はCodex後描画）
- contract: 1 Agent = 1 scene = 1 image。collage・storyboard・split panel・variantsは作らない。他sceneのpromptは見ない/受け取らない。

## Prompt（このpromptのみで生成する）

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, warm, trustworthy palette (cream, ivory, light brown). Strong visual hierarchy, one main message, one large focal point, readable on a smartphone, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout unless explicitly required by this scene. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented logos, no unnecessary decoration. Scene direction: A realistic warm illustration of a Japanese woman in her 60s (gray hair, natural clothes) sitting on a sofa in a bright living room, looking at a smartphone in her hands with a gentle relieved smile. The phone screen is overexposed and blurred so no UI is identifiable. A few printed family photos lie on the coffee table in front. Keep the person on the right half; the left half is a quiet, slightly textured cream wall with a plant, reserved for later Codex Japanese text (not pure white). Warm natural light. No text, no numbers, no logos, no brand marks, no phone UI. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

## Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- presentation card layout
- Google Photos UI / app screen / any phone UI
- real or invented logo (Google Photos, Google, Apple)
- fake screenshot
- tiny or garbled Japanese text, numbers, or any readable text
- personal information
- content in the bottom 180px subtitle area

## Completion report

生成後、valid image、width / height、aspect ratio、file size、SHA-256を確認して親Codexへ返すこと。canonical file（episode.json等）は変更しない。
