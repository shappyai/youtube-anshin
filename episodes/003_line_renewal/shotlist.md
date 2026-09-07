# Shotlist — Episode 003 LINEの画面リニューアル

方針: 実機撮影なし。正確なLINE画面はLINE公式スクリーンショットを使用し、GPT画像は概念説明だけに使う。公式スクリーンショットの表示名・写真は素材に含まれるサンプル表示であり、個人の実機情報は撮影しない。

| Shot | Scene | Device | Render mode | 内容 | Asset / 画面表示 | 字幕安全領域 |
|---|---:|---|---|---|---|---|
| SHOT-01 | 001 | 生成画像（ChatGPT画像生成後） | gpt_image | 画面が変わって戸惑う導入。「故障ではありません」を先に提示 | `assets/generated_ai/scene_001.png` 未生成。LINE UI・ロゴは生成しない | 下180pxを空ける |
| SHOT-02 | 002 | Codexテンプレート | template | 今日確認する4項目 | 文字中心の一覧。公式UIなし | 下180pxを空ける |
| SHOT-03 | 003 | 生成画像（ChatGPT画像生成後） | gpt_image | 1 / 5 セクション扉。「友だちはどこ？」 | `assets/generated_ai/scene_003.png` 未生成。抽象的な入口とスマホのみ | 下180pxを空ける |
| SHOT-04 | 004 | PCブラウザ（LINE公式ページ素材） | official | 新トークタブ全体を場所理解用に表示 | `chat_new_overview.png` | 内容を読む箇所は公式画像を大きく表示 |
| SHOT-05 | 005 | PCブラウザ（LINE公式ページ素材） | official | 「トーク」「友だち」の2タブを拡大 | `chat_new_tabs.png` の上部クロップ | タブ名を字幕で覆わない |
| SHOT-06 | 006 | PCブラウザ（LINE公式ページ素材） | official | 「友だち」をタップして切り替える | `chat_tabs_switch_1.png` / `chat_tabs_switch_2.png` 上部クロップ | 赤枠を含む公式画像を改変しない |
| SHOT-07 | 007 | Codexテンプレート | template | 2 / 5 セクション扉 | 文字中心の見出し | 下180pxを空ける |
| SHOT-08 | 008 | PCブラウザ（LINE公式ページ素材） | official | プラスメニューの機能 | `chat_plus_menu.png`。iOS / Android差もナレーションで説明 | 公式画面の文字を読ませる |
| SHOT-09 | 009 | PCブラウザ（LINE公式ページ素材） | official | ブラウン案内は現在表示されないことを補足 | `chat_brown_historical.png` のブラウン周辺クロップ。歴史的画面と明記 | 当時の画面であることを画面外テキストで補足 |
| SHOT-10 | 010 | 生成画像（ChatGPT画像生成後） | gpt_image | 3 / 5 セクション扉。ホームで見る場所 | `assets/generated_ai/scene_010.png` 未生成。家の入口を抽象表現 | 下180pxを空ける |
| SHOT-11 | 011 | PCブラウザ（LINE公式ページ素材） | official | ホームの全体像 | `home_new_overview.png` | 全体画面は場所理解用に短時間 |
| SHOT-12 | 012 | PCブラウザ（LINE公式ページ素材） | official | アクティビティとコンテンツ | `home_activity_content.png` / `home_activity_detail.jpeg` | 2画面比較。字幕帯は別にする |
| SHOT-13 | 013 | 生成画像（ChatGPT画像生成後） | gpt_image | 4 / 5 セクション扉。人によって違う | `assets/generated_ai/scene_013.png` 未生成。段階的な表示を抽象化 | 下180pxを空ける |
| SHOT-14 | 014 | 生成画像（ChatGPT画像生成後） | gpt_image | 同じアプリでも表示時期が違う概念 | `assets/generated_ai/scene_014.png` 未生成。2台の抽象スマホ | LINE UI・正確な文字は生成しない |
| SHOT-15 | 015 | Codexテンプレート | template | 旧画面への復帰・特別設定について確認できた範囲 | 公式案内に基づく注意画面。断定は避ける | 下180pxを空ける |
| SHOT-16 | 016 | 生成画像（ChatGPT画像生成後） | gpt_image | 5 / 5 セクション扉。今やること | `assets/generated_ai/scene_016.png` 未生成。空のチェック項目 | 下180pxを空ける |
| SHOT-17 | 017 | Codexテンプレート | template | 更新・トーク・ホームの3項目 | 数字付きのまとめ | 下180pxを空ける |
| SHOT-18 | 018 | 生成画像（ChatGPT画像生成後） | gpt_image | まとめとCTA。入口を確認する安心感 | `assets/generated_ai/scene_018.png` 未生成。人物とスマホの抽象画 | 下180pxを空ける |

## 公式素材の表示ルール

- `chat_new_overview.png` は全体の場所を理解させる短い表示にする。
- `chat_new_tabs.png`、`chat_tabs_switch_1.png`、`chat_tabs_switch_2.png` はタブ部分をクロップし、大きく読ませる。
- `chat_brown_historical.png` は現在の必須案内と誤解しないよう、「リニューアル当時の画面」と画面外で明記する。
- ホームの内容は、友だち・通知・サービス一覧と、LINE NEWSなどのコンテンツを分けて表示する。
