# Short001 ImageGen / official / renderer QA v4

- v2 ImageGen-native完成画：再利用。新規ImageGen call：0、再生成：0。
- 画像生成で公式UI・ChatGPT UI・ロゴを再現していない。
- Short002の旧privacy ImageGen sceneは拒否済みのため使用していない。
- NO_IMAGE_TEXT_HYBRID：PASS。大見出しの後乗せはなく、字幕と小さな実チャンネルロックアップだけを許可。

## `assets/imagegen_native_v2/normalized/scene_01_hook.png`

- ImageGen-native文字：['ChatGPT', '話すだけで使える？']
- exact_text_qa：PASS_REVALIDATED
- sha256：`3ea6c9f12d65c9669f4e5cf4125cc2f168a5f6b041f6679f519f26a301884f62`

## `assets/imagegen_native_v2/normalized/scene_06_summary.png`

- ImageGen-native文字：['まずは', '話しかけるだけ']
- exact_text_qa：PASS_REVALIDATED
- sha256：`a7caa300f1f2fdca47785bfeb03eb1bd60112924c58b109397b22aa89767b0a4`

## Short001 capture boundary

- `chatgpt_home_current.png`：現行chatgpt.comのログアウト画面を使った実画面（B1/B3/B4）。
- `voice_official_reference.png`：公式Voice紹介ページの参照画面。アプリ内の実Voiceセッションとしては表示しない。
- 実Voiceセッション録画：CAPTURE_REQUIRED（v4 draftは偽UIを使わず現状の公式素材までで停止）。

