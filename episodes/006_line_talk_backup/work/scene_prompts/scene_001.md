# Image Agent assignment — SCENE-001

- scene_id: SCENE-001
- image_prompt_id: IMG-001
- output_path: `assets/generated_ai/scene_001.png`（この1ファイルのみ保存）
- purpose: 導入。機種変更・故障でLINEのトークが消えるのではという不安を、穏やかな光景で受け止める（安心を先に見せる）。headline「機種変更しても、\nトークは残る？」はCodex後描画
- contract: 1 Agent = 1 scene = 1 image。collage・storyboard・split panel・variantsは作らない。他sceneのpromptは見ない/受け取らない。

## Prompt（このpromptのみで生成する）

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, warm, reassuring palette (soft cream, warm beige, gentle light). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. Scene direction: A gentle realistic illustration of a Japanese man or woman in their 60s sitting on a sofa, looking at a smartphone with a calm, slightly thoughtful but not worried expression. The phone screen is overexposed and blurred so no UI is identifiable. Keep the person on the right half; the left half is a quiet, slightly textured warm wall with a plant and a small clock, reserved for later Codex Japanese text (not pure white). Warm natural light. No text, no numbers, no logos, no brand marks, no phone UI, no QR-code-like patterns, no ID-card-like text. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

## Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- LINE UI / chat bubbles / app screen / any phone UI
- real or invented logo (LINE, LYP, iCloud, Google)
- fake screenshot, QR code, phone-number-like or ID-like strings
- tiny or garbled Japanese text, numbers, or any readable text
- personal information
- content in the bottom 180px subtitle area

## Completion report

生成後、valid image、width / height、aspect ratio、file size、SHA-256を確認して親Codexへ返すこと。canonical file（episode.json等）は変更しない。
