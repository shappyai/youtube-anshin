# Image Agent assignment — SCENE-019

- scene_id: SCENE-019
- image_prompt_id: IMG-004
- output_path: `assets/generated_ai/scene_019.png`（この1ファイルのみ保存）
- purpose: 5/5 扉。「OSをまたぐ機種変更」の概念。両OSの違いは色だけで暗示。headline「OSをまたぐ\n機種変更に注意」はCodex後描画
- contract: 1 Agent = 1 scene = 1 image。collage・storyboard・split panel・variantsは作らない。他sceneのpromptは見ない/受け取らない。

## Prompt（このpromptのみで生成する）

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy palette (soft blue and warm orange accents, gentle pastel). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. Scene direction: A soft illustration of two gentle island shapes in different colors (one cool blue, one warm orange) separated by water, connected by a simple curved wooden bridge. A small light at the center of the bridge marks a crossing. No smartphones, no device silhouettes, no logos, no brand marks. Keep the islands on the right to center; the left half is a quiet, slightly textured light wall for later Codex Japanese text (not pure white). No text, no numbers, no letters, no readable characters. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

## Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- iPhone/Android device illustrations, logos, or brand marks
- phone UI, chat bubbles, fake screenshot, QR code, phone-number-like or ID-like strings
- tiny or garbled Japanese text, numbers, or any readable text
- personal information
- content in the bottom 180px subtitle area

## Completion report

生成後、valid image、width / height、aspect ratio、file size、SHA-256を確認して親Codexへ返すこと。canonical file（episode.json等）は変更しない。
