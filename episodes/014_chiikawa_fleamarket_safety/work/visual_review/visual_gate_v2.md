# Episode 014 visual gate v2

確認日：2026-09-06

## 判定

- 機械QA：PASS（FAIL 0）
- scene quality report：OK 17 / WARN 1 / FAIL 0
- `hybrid_generated_image_large_text`：0
- `NO_IMAGE_TEXT_HYBRID`：違反0
- 人間の全編確認：未完了。draft_v2確認後に停止

## SCENE-005の変更

- 旧v1：`render_mode=gpt_image` + `text_render_mode=pil_overlay`。生成画像を背景にし、主要見出しをrendererで大きく後乗せする構成。
- 新v2：`render_mode=gpt_image` + `text_render_mode=imagegen_native`。ImageGen内で「残り1個」「どうする？」「架空の例」を完成画の一部として一体生成し、後から大きな文字を重ねていない。
- 新画像：`assets/generated_ai/scene_005.png`、1920×1080正規化済み、SHA-256 `9d9468204584228e986fcc1303b49f85cb43532c54953299c333802c423a8fa1`
- 目視確認：generic older adult、空のスマホ、無地の箱・抽象的な商品。ちいかわ等のキャラクター、ロゴ、実在UI、価格、出品者情報なし。

## 全scene確認

- 生成画像scene：2（SCENE-001 / SCENE-005）
- `imagegen_native`：2
- renderer-native：16
- 公式素材：4点。公式UIのAI再現なし
- character art：0
- oversized_checkmark：0
- midroll CTA：0 / end CTA：1
- blank_white_slide：0
- subtitle safe area：PASS
- SCENE-003の小文字proxyのみWARN。FAILへは扱わず、人間のTV視聴確認へ引き継ぐ。

## 恒久ルールの配置

- canonical：`docs/text_render_policy.md`
- 運用ルール：`AGENTS.md`
- schema/default validation：`scripts/episode_io.py`
- renderer fail-closed：`scripts/hybrid_scene_renderer.py`
- exact text retry：`scripts/text_qa.py`

生成画像sceneはImageGen-native完成画またはno-text完成画、正確な文字が必要なsceneはtemplate/official等のrenderer-nativeとする。2回目の文字QA FAIL後も、生成画像を再利用した大きな文字overlayへ戻さない。

## 確認素材

- contact sheet：`work/visual_review/scene_contact_sheet_v2.png`
- scene quality：`work/visual_review/scene_quality_report_v2.md`
