# Short002 ImageGen / official / renderer QA v5

- `shorts_micro_motion_for_motion_sake`：FORBIDDEN。ImageGen assetは静止表示し、意味のないzoom/panを付けていない。
- `NO_IMAGE_TEXT_HYBRID`：PASS。生成画像へ大見出し・説明カードを後乗せしていない。字幕とCTAの最小表示だけをrenderer overlayとして許可。
- 公式UI・マイナポータル画面・ChatGPT画面・ロゴをImageGenで再現していない。
- 新規ImageGen call：2（Short003のコンビニ証明書scene、e-Tax生活scene）、再生成：0。

## `assets/imagegen_native_v2/normalized/scene_01_hook.png`

- text_render_mode：`imagegen_native`
- text：ImageGen-native approved text retained
- exact_text_qa：PASS_REVALIDATED
- vision_qa：PASS_REUSED
- meaningful_crop：False
- sha256：`a3ebe0f10d85dcdae4135df728fc41a0b43f5484d7ff9260110f7137a82e0b85`

## `assets/imagegen_native_v2/normalized/scene_05_official.png`

- text_render_mode：`imagegen_native`
- text：ImageGen-native approved text retained
- exact_text_qa：PASS_REVALIDATED
- vision_qa：PASS_REUSED
- meaningful_crop：False
- sha256：`9b710d3a5878d219335461a090b07a623834feebc08ee73231c5e5638c1a88d6`

## `assets/renderer_v5/scene_05_official_focus.png`

- text_render_mode：`imagegen_native`
- text：ImageGen-native approved text retained
- exact_text_qa：PASS_REVALIDATED
- vision_qa：PASS_REUSED
- meaningful_crop：True
- sha256：`7938af25b6ebcc13dcdcb4db546edb1849c5d3fbdf3b80181a3ccd7651a93c8b`

