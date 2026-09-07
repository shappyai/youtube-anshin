# Image Agent assignment — SCENE-015

- scene_id: SCENE-015
- image_prompt_id: IMG-003
- output_path: `assets/generated_ai/scene_015.png`（この1ファイルのみ保存）
- purpose: 4/5 扉。「コピーを守る鍵」の概念（バックアップ用の暗証番号PIN）。headline「コピーを守る、\n鍵のようなもの」はCodex後描画
- contract: 1 Agent = 1 scene = 1 image。collage・storyboard・split panel・variantsは作らない。他sceneのpromptは見ない/受け取らない。

## Prompt（このpromptのみで生成する）

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, safe, reassuring palette (soft warm gold, gentle cream, light brown). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. Scene direction: A soft illustration of a large friendly brass key standing in front of a small wooden treasure chest that gently glows from inside, representing protecting a precious copy with a key. No keypad, no digits, no PIN screen, no phone, no UI. Keep the subject on the right; the left half is a quiet, slightly textured warm wall for later Codex Japanese text (not pure white). Warm lighting. No text, no numbers, no logos, no brand marks, no QR-code-like patterns. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

## Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- PIN entry screen, keypad, digits, or any numeric UI
- phone UI, chat bubbles, any real or invented logo (LINE, LYP, iCloud, Google)
- fake screenshot, QR code, phone-number-like or ID-like strings
- tiny or garbled Japanese text, numbers, or any readable text
- personal information
- content in the bottom 180px subtitle area

## Completion report

生成後、valid image、width / height、aspect ratio、file size、SHA-256を確認して親Codexへ返すこと。canonical file（episode.json等）は変更しない。
