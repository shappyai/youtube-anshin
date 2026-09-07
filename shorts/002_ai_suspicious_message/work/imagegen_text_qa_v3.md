# Short002 ImageGen-native文字QA v3

- 生成方式：v2のbuilt-in image_gen完成画を再利用
- 新規ImageGen call：0
- 画像内の大見出し：ImageGen-nativeで一体生成済み
- 後乗せ大見出し：0（NO_IMAGE_TEXT_HYBRID / visual_mode_exclusive）
- 再生成：0
- 目視再確認：指定文言、誤字、脱字、余計な文字、文字切れ、人物との重なり、縮小時可読性をPASS

## Major visual A / 冒頭

- asset：`assets/imagegen_native_v2/normalized/scene_01_hook.png`
- headline：`このメール、` / `本物？`
- text_render_mode：`imagegen_native`
- exact_text_qa：PASS
- vision_qa：PASS_REVALIDATED
- official_ui_ai_reconstruction：0
- hybrid_generated_image_large_text：0

## Major visual B / 行動

- asset：`assets/imagegen_native_v2/normalized/scene_02_mask.png`
- headline：`個人情報は` / `まず隠す`
- text_render_mode：`imagegen_native`
- exact_text_qa：PASS
- vision_qa：PASS_REVALIDATED
- official_ui_ai_reconstruction：0
- hybrid_generated_image_large_text：0

## Major visual C / 結論

- asset：`assets/imagegen_native_v2/normalized/scene_05_official.png`
- headline：`最後は` / `公式から確認`
- text_render_mode：`imagegen_native`
- exact_text_qa：PASS
- vision_qa：PASS_REVALIDATED
- official_ui_ai_reconstruction：0
- hybrid_generated_image_large_text：0

