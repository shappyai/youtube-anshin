# Image Agent assignment — SCENE-003

- scene_id: SCENE-003
- image_prompt_id: IMG-002
- output_path: `assets/generated_ai/scene_003.png`（この1ファイルのみ保存）
- purpose: 1/5 扉。「引き継ぎ（手続き）」と「バックアップ（コピー）」が別のものだという概念。headline「二つの準備は、\n別のもの」はCodex後描画
- contract: 1 Agent = 1 scene = 1 image。collage・storyboard・split panel・variantsは作らない。他sceneのpromptは見ない/受け取らない。

## Prompt（このpromptのみで生成する）

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy palette (soft blue, gentle green, warm beige). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. Scene direction: A soft storybook-style illustration showing two different wooden storage chests standing side by side on a gentle path: one chest conveys a "procedure/moving" idea with a small document-handover motif (no text), the other chest conveys a "copy" idea with a soft ribbon of light carrying small message-card silhouettes into it (no text). The two chests are clearly separate but equal, conveying two different preparations. Use simple shapes, no readable text, no letters, no digits. Keep the main subject on the right to center; the left half is a quiet, slightly textured wall for later Codex Japanese text (not pure white). No service logos, no brand marks, no phone UI, no chat bubbles. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

## Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- any real service name rendered as text (LINE, LINEアプリ表記) or logo
- phone UI, chat bubbles, QR code, phone-number-like or ID-like strings
- tiny or garbled Japanese text, numbers, or any readable text
- personal information
- content in the bottom 180px subtitle area

## Completion report

生成後、valid image、width / height、aspect ratio、file size、SHA-256を確認して親Codexへ返すこと。canonical file（episode.json等）は変更しない。
