# Short001 ImageGen / official / renderer QA v5

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
- sha256：`3ea6c9f12d65c9669f4e5cf4125cc2f168a5f6b041f6679f519f26a301884f62`

## `assets/imagegen_native_v2/normalized/scene_04_life.png`

- text_render_mode：`imagegen_native`
- text：ImageGen-native approved text retained
- exact_text_qa：PASS_REVALIDATED
- vision_qa：PASS_REUSED
- meaningful_crop：False
- sha256：`f2547bb0b9dd4674a7ac2e77f87c8db071f2ff374b80ec86a979ff0e1d03f50b`

## `assets/imagegen_native_v2/normalized/scene_06_summary.png`

- text_render_mode：`imagegen_native`
- text：ImageGen-native approved text retained
- exact_text_qa：PASS_REVALIDATED
- vision_qa：PASS_REUSED
- meaningful_crop：False
- sha256：`a7caa300f1f2fdca47785bfeb03eb1bd60112924c58b109397b22aa89767b0a4`

## Short001 capture boundary

- 現行chatgpt.comログアウト画面は実画面として使用。公式Voice紹介ページは参照画面として使用。
- ログイン後のライブVoiceセッションは `CAPTURE_REQUIRED`。偽UIは作成していない。

