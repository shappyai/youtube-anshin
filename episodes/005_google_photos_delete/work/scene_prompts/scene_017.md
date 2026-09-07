# Image Agent assignment — SCENE-017

- scene_id: SCENE-017
- output_path: `assets/generated_ai/scene_017.png`（この1ファイルのみ保存）
- purpose: 5/6セクション扉。本体にある写真からGoogleフォトへバックアップコピーが作られ、削除時の扱いが違う概念（見出し「5 / 6」はCodex後描画。Apple/Google UI・ロゴは生成しない）
- contract: 1 Agent = 1 scene = 1 image。collage・storyboard・split panel・variantsは作らない。他sceneのpromptは見ない/受け取らない。

## Prompt（このpromptのみで生成する）

Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes. Create an edge-to-edge full-frame background for a 1920x1080 Japanese YouTube educational video for viewers aged 50 to 70. Calm, trustworthy palette (soft blue-gray, gentle blue, warm wood tones). Strong visual hierarchy, one large focal point, uncluttered. Do not leave a blank white half or a large empty white area. A text area may be quiet, but it must remain a real background that continues to the screen edges. No presentation card layout. Reserve the bottom 180 pixels as a subtitle-safe area. No tiny text, no fake official UI, no invented logos, no unnecessary decoration. Scene direction: A soft illustration showing a generic smartphone silhouette on the right with one family-photo card on it, and a gentle light ribbon creating a backup copy of the same photo card that flows toward a calm abstract cloud-shaped online storage symbol. Make the copy relationship clear: one photo on the phone, one backup copy flowing from it. Do not depict two independent photo libraries or two separate storage places. Place the subject on the right; the left half is a quiet, slightly textured blue-gray wall for later Codex Japanese text (not pure white). Do not draw any iPhone device illustration, any screen UI, any Apple logo, any Google Photos UI, any text, numbers, or brand marks. Generation contract: this is one finished standalone scene background; keep the visual edge-to-edge and use a calm, non-white-empty background for any later Codex text.

## Must not generate

- collage, storyboard, contact sheet, split panel, grid, or multiple scenes in one image
- blank white half or large empty white canvas
- presentation card layout
- iPhone device illustration, Apple UI, Apple logo, Google Photos UI
- two independent photo libraries or two separate storage places
- real or invented logo
- fake screenshot
- tiny or garbled Japanese text, numbers, any readable text
- personal information
- content in the bottom 180px subtitle area

## Completion report

生成後、valid image、width / height、aspect ratio、file size、SHA-256を確認して親Codexへ返すこと。canonical file（episode.json等）は変更しない。
