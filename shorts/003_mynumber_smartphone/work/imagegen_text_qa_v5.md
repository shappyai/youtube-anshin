# Short003 ImageGen / official / renderer QA v5

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
- sha256：`a4f879d31ea0987a28dabcdd0cae30eb02ac56f4e3eb3b4926262969164f47d1`

## `assets/imagegen_native_v5/normalized/convenience_certificate.png`

- text_render_mode：`imagegen_native`
- text：none
- exact_text_qa：PASS_NO_TEXT
- vision_qa：PASS_REVIEWED
- meaningful_crop：False
- sha256：`8d22bacf4f18a7f96cc8050d1a92472e08709e598464828a4aeebb688bde9436`

## `assets/imagegen_native_v5/normalized/etax_home.png`

- text_render_mode：`imagegen_native`
- text：none
- exact_text_qa：PASS_NO_TEXT
- vision_qa：PASS_REVIEWED
- meaningful_crop：False
- sha256：`9cc1adfc3de3f75a0bb175a6fc44ffb9b89ac1438147553898ec8e2fc1192850`

## `assets/imagegen_native_v2/normalized/scene_03_health.png`

- text_render_mode：`imagegen_native`
- text：ImageGen-native approved text retained
- exact_text_qa：PASS_REVALIDATED
- vision_qa：PASS_REUSED
- meaningful_crop：False
- sha256：`01f73abdef6215514dc608ce6d19835ac2d1ea9da7772b64a0aeeb947332db7d`

## `assets/imagegen_native_v5/normalized/scene_03_health_focus.png`

- text_render_mode：`imagegen_native`
- text：ImageGen-native approved text retained
- exact_text_qa：PASS_REVALIDATED
- vision_qa：PASS_REUSED
- meaningful_crop：True
- sha256：`8915e254b7263ae1d6614c237b7d0d0a4ee3cbdb206a5e0888f80b9d58107258`

## `assets/imagegen_native_v2/normalized/scene_05_conclusion.png`

- text_render_mode：`imagegen_native`
- text：ImageGen-native approved text retained
- exact_text_qa：PASS_REVALIDATED
- vision_qa：PASS_REUSED
- meaningful_crop：False
- sha256：`9e0a40e707bdbf0ea01e567cb795017d398041475630efb5f3f49f1d1a0fb465`

## Short003 concrete usage assets

- `myna_app_home_official.png`：デジタル庁公式プレスキットの実画面。source：https://services.digital.go.jp/mynaapp/communication-guidelines/
- `convenience_certificate.png` / `etax_home.png`：ImageGen-nativeの文字なし生活scene。公式UIを再現していない。
- B1/B2/B3を抽象rendererカードへ戻さない。字幕が説明し、画面は具体的な行動を示す。

