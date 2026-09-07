# Episode 011 viewer-facing brand promise scan

確認日：2026-09-06

## Result

- `viewer_facing_brand_promise_count`：**0**
- status：**PASS**

## Checked viewer-facing surfaces

- `episode.json` の narration / display text / subtitle text / scene text / midroll CTA / ending / postroll display text
- `script.md` の現行台本本文
- `publish.json` の description / chapters / end CTA
- `captions.srt` / `captions.ass`
- `assets/scenes/` と `work/rendered_final_scenes/` の現行scene画像、およびdraft_v2代表フレーム

## Result detail

`怖がらせる前に、確認する。` は、segment 039、SUB-039、SCENE-018の後付け表示、CTA、概要欄、チャプター、現行のrendered sceneには残っていない。SCENE-018は `迷ったら、` / `その場で決めない` と `いったん止まって、` / `公式から確認` のみをImageGen内に表示する。

内部の `metadata.brand_promise` と制作ルール上のブランド定義は、視聴者向け出力ではないため保持した。
