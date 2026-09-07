# Episode 004 — GPT Image Generation Manifest v2

## IMPORTANT: GENERATION PROTOCOL

This file is an orchestration index only.

**DO NOT send this entire file to the image generator.**

The image generator must receive **exactly ONE scene prompt per call**.

Generation sequence:

1. Open one scene prompt file from `scene_prompts/`.
2. Send ONLY that file's content to the image generator.
3. Generate exactly 1 image (`n=1`).
4. Save the result using the exact filename specified in that scene file.
5. Validate the output.
6. Only after that scene is saved, move to the next scene.

Never combine prompts from multiple scenes in one image-generation call.

## Queue

| Order | Scene | Prompt file | Output filename |
|---:|---|---|---|
| 1 | SCENE-001 | `scene_prompts/scene_001.md` | `scene_001.png` |
| 2 | SCENE-003 | `scene_prompts/scene_003.md` | `scene_003.png` |
| 3 | SCENE-006 | `scene_prompts/scene_006.md` | `scene_006.png` |
| 4 | SCENE-009 | `scene_prompts/scene_009.md` | `scene_009.png` |
| 5 | SCENE-012 | `scene_prompts/scene_012.md` | `scene_012.png` |
| 6 | SCENE-015 | `scene_prompts/scene_015.md` | `scene_015.png` |
| 7 | SCENE-018 | `scene_prompts/scene_018.md` | `scene_018.png` |

## Hard rules

- One tool call = one scene = one image.
- Never generate a collage, storyboard, contact sheet, grid, montage, split screen, or multi-panel image.
- Never generate 7 variants of one scene in place of the 7 requested scenes.
- Never pass more than one `scene_###.md` file to the image generator at once.
- Never infer another scene from this index.
- Each output must be a single continuous 16:9 composition.
- Exact target: 1920×1080 intent, PNG.
- `text_render_mode = codex`: do not generate readable Japanese text in the image.
- `fit_mode = full_bleed`: background must extend naturally edge-to-edge.
- The lower subtitle-safe region must remain visually continuous background, **not a white blank bar**.
- Text-safe zones are low-detail background regions, **not empty white canvas**.
- Official UI, police badges, government logos, arrest warrants, phone numbers, and fake screenshots are forbidden unless a scene prompt explicitly says otherwise.

## Output validation after every scene

Reject and regenerate the SAME scene if any of these occur:

- more than one panel / scene / frame
- scene labels such as `SCENE-001`
- a storyboard/contact sheet
- multiple unrelated compositions
- huge blank white half
- white presentation card occupying a large part of the frame
- readable generated text
- fake official UI
- phone numbers
- police badge or government logo
- important subject placed inside the lower subtitle-safe region

Do not proceed to the next scene until the current one passes.
