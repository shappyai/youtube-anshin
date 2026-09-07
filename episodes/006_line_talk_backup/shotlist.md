# Shot list

## Media decision（撮影前に決定・001で確定したルール）
- 企画時に「どの媒体が最も分かりやすく制作しやすいか」を先に決める:
  Webサービスの設定=PCブラウザ / Android OS・アプリ=Android Emulator /
  iPhone固有設定=iPhone / LINE等スマホアプリ=スマホ / 実機でなければ成立しない操作=実機
- 「スマホユーザー向けだから必ずスマホ撮影」はしない。

| ID | Device | Action | Expected screen | Privacy check | Filename |
|---|---|---|---|---|---|
| SHOT-01 | iPhone/Android |  |  |  | shot_01.mp4 |
# Shotlist — Episode 006 LINEのトーク履歴バックアップ

方針: LINEアプリの基本操作（バックアップ確認・自動バックアップ・PIN設定）は **Android Emulatorまたは安全なテスト端末** を優先したが、LINE未インストールのため **LINE公式保存HTML由来の手順引用カード** へfallback。iPhone差分（iCloud Drive確認）も公式保存HTML由来の引用カード、仕様の出典も **LINE公式ヘルプ**、概念・安心・人物は **GPT画像**（LINEの実際のUI・ロゴはAIで再現しない）、一覧・比較・チェック・まとめは **Codexテンプレート**。SCENE-018のPIN注意はSCENE-017へ統合し、sceneは24件。LINEの実画面はAI画像で作らない。

| Shot | Scene | Device | Render mode | 内容 | Asset / 画面表示 | 字幕安全領域 |
|---|---:|---|---|---|---|---|
| SHOT-01 | SCENE-006 | Android Emulator/テスト端末 | official（可読性拡大版・承認済み） | 2 / 5 設定→「バックアップ・引き継ぎ」の手順 | `work/phase_b_review/readability_fix/scene_006_readability.png`（元: `assets/official/line_backup_transfer_menu_fallback.png`） | 下180pxを空ける |
| SHOT-02 | SCENE-007 | Android Emulator/テスト端末 | official（可読性拡大版・承認済み） | 2 / 5 「トークのバックアップ」手順。「今すぐバックアップ」 | `work/phase_b_review/readability_fix/scene_007_readability.png`（元: `assets/official/line_talk_backup_datetime_fallback.png`） | 下180pxを空ける |
| SHOT-03 | SCENE-011 | Android Emulator/テスト端末 | official（可読性拡大版・承認済み） | 3 / 5 自動バックアップをオンにする手順 | `work/phase_b_review/readability_fix/scene_011_readability.png`（元: `assets/official/line_auto_backup_fallback.png`） | 下180pxを空ける |
| SHOT-04 | SCENE-014 | iPhone実機または公式資料 | official（可読性拡大版・承認済み） | 3 / 5 iPhone: iCloud Driveのオン確認 | `work/phase_b_review/readability_fix/scene_014_readability.png`（元: `assets/official/line_icloud_drive_crop.png`） | 下180pxを空ける |
| SHOT-05 | SCENE-016 | Android Emulator/テスト端末 | official（可読性拡大版・承認済み） | 4 / 5 バックアップ用PINコードの設定。6桁・事前登録 | `work/phase_b_review/readability_fix/scene_016_readability.png`（元: `assets/official/line_backup_pin_fallback.png`） | 下180pxを空ける |
| SHOT-06 | SCENE-020 | LINE公式ヘルプ | official（可読性拡大版・承認済み） | 5 / 5 標準バックアップは「同じOSに引き継ぐ場合にのみ利用できます」 | `work/phase_b_review/readability_fix/scene_020_readability.png`（元: `assets/official/line_standard_backup_same_os_crop.png`） | 下180pxを空ける |
| SHOT-07 | SCENE-022 | LINE公式ヘルプ | official（可読性拡大版・承認済み） | 5 / 5 標準バックアップでは画像・動画はバックアップ・復元されない（公式の本文） | `work/phase_b_review/readability_fix/scene_022_readability.png`（元: `assets/official/line_backup_trouble_media_crop.png`） | 下180pxを空ける |
| — | SCENE-001 | GPT画像 | gpt_image | 導入。機種変更・故障への不安と安心 | `assets/generated_ai/scene_001.png`（IMG-001・Phase Bで生成）。LINE UIを描かない | 下180pxを空ける |
| — | SCENE-002 | Codexテンプレート | template | 今日確認する3項目の一覧 | `layout_02_list`。①バックアップ日時 ②自動バックアップ ③PIN | 下180pxを空ける |
| — | SCENE-003 | GPT画像 | gpt_image | 1/5 扉。「引き継ぎ（手続き）とバックアップ（コピー）は別」の概念 | `assets/generated_ai/scene_003.png`（IMG-002・Phase Bで生成） | 下180pxを空ける |
| — | SCENE-004 | Codexテンプレート | template | 前・当日・後の3ステップ時系列図解 | `layout_03_visual_text`。前=バックアップ／当日=引き継ぎ／後=復元 | 下180pxを空ける |
| — | SCENE-005 | Codexテンプレート | template | 引き継ぎだけではトークは戻らない（両方の準備が必要） | `layout_05_compare`。端末内保存の事実・公式の「事前にバックアップが必要」 | 下180pxを空ける |
| — | SCENE-008 | Codexテンプレート | template | コピーがスマホの外に作られる概念 | `layout_03_visual_text`。クラウド保管のイメージ（公式UIなし） | 下180pxを空ける |
| — | SCENE-009 | Codexテンプレート | template | 保存先のOS別比較 | `layout_05_compare`。iPhone=iCloud Drive／Android=Google ドライブ（公式表記） | 下180pxを空ける |
| — | SCENE-010 | Codexテンプレート | template | 注意カード（メイン端末だけ・文字だけ） | `layout_06_caution`。写真・動画は後述 | 下180pxを空ける |
| — | SCENE-012 | Codexテンプレート | template | 自動バックアップの条件比較 | `layout_05_compare`。iPhone=5条件／Android=2条件（公式の条件表記） | 下180pxを空ける |
| — | SCENE-013 | Codexテンプレート | template | 注意カード（オフのままにしない） | `layout_06_caution`。失敗時は公式アカウントから通知 | 下180pxを空ける |
| — | SCENE-015 | GPT画像 | gpt_image | 4/5 扉。「コピーを守る鍵」の概念（PIN） | `assets/generated_ai/scene_015.png`（IMG-003・Phase Bで生成）。数字・PIN画面を描かない | 下180pxを空ける |
| — | SCENE-017 | Codexテンプレート | template | 直近14日間のセーフティネットとPINの注意（推測されやすい番号を避ける） | `layout_03_visual_text`。10回失敗は本編で扱わない | 下180pxを空ける |
| — | SCENE-019 | GPT画像 | gpt_image | 5/5 扉。「OSをまたぐ機種変更」の概念 | `assets/generated_ai/scene_019.png`（IMG-004・Phase Bで生成）。iPhone/Android実機・ロゴを描かない | 下180pxを空ける |
| — | SCENE-021 | Codexテンプレート | template | 同じOSと異なるOSの比較 | `layout_05_compare`。異なるOS=直近14日分まで | 下180pxを空ける |
| — | SCENE-023 | Codexテンプレート | template | 参考：プレミアムバックアップ（勧誘しない・解約注意のみ）＋引き継ぎ準備の案内 | `layout_03_visual_text`。公式ガイド参照の案内 | 下180pxを空ける |
| — | SCENE-024 | Codexテンプレート | template | まとめ3項目チェック（オープニングと同一内容・同一順） | `layout_07_summary`＋summary_stagger。①〜③ | 下180pxを空ける |
| — | SCENE-025 | GPT画像 | gpt_image | クロージング。あわてずに確認する安心の光景 | `assets/generated_ai/scene_025.png`（IMG-005・Phase Bで生成） | 下180pxを空ける |
| — | CTA | Codexテンプレート | template | channel_common_cta（音声あり・`config/channel_cta.json`準拠） | `work/channel_cta.png`（Phase Bで作成） | 下180pxを空ける |

## 公式素材の表示ルール

- LINEの操作画面はAIで再現しない。AndroidはEmulatorまたは安全なテスト端末の実画面を優先し、今回はLINE未インストールのため保存HTML由来の公式手順引用カードへfallback。iPhone差分も公式手順引用カードで代替し、仕様の出典はLINE公式ヘルプ（SRC-003/004/005/008）。
- 機能名（標準バックアップ・バックアップ用のPINコード・今すぐバックアップ・自動バックアップ・iCloud Drive・Google ドライブ・プレミアムバックアップ）は公式表記どおりに表示し、GPT画像では生成しない。
- テスト素材は実トーク・友だち一覧・通知・QRコード・LINE ID・電話番号・プロフィール写真が映らない安全なものだけを使用。

## 個人情報リスク（Phase Aで確定）

- LINE実画面はテストアカウントのみ。実在の会話・連絡先・通知内容を映さない（モザイク・見切らせ）。
- PINは値や入力欄の数字を映さない（設定導線の案内のみ）。
- iPhoneのiCloud設定はApple ID・メール等をモザイク。実機不可時はLINE公式資料（SRC-004）で代替。
- 公式手順引用カードは保存HTMLの公式文言をもとに作成し、実在UIではないこと、出典URLと確認日（2026-09-02）を画面・説明欄で明示。

## 実機・媒体選択の根拠

- LINEアプリの基本操作 → 媒体ルールの「LINE等スマホアプリ→スマホ」に該当。Android Emulatorまたは安全なテスト端末（LINEログイン・SMS認証の再現可否は人間が判断。不可能なら公式ヘルプ画面で代替）。
- iPhone固有のiCloud Drive設定 → 「iPhone固有設定→iPhone」に該当。実機または公式資料。
- 概念・安心・人物（導入・コピーの概念・PIN=鍵・OSまたぎ・クロージング）→ GPT画像5枚（人間確認後・Phase B）。
- 一覧・比較・注意・まとめ → Codexテンプレート（正確な日本語を後描画）。

## GPT画像の割当（1 Agent = 1 scene = 1 image）

- IMG-001 = SCENE-001（導入）・IMG-002 = SCENE-003（1/5扉）・IMG-003 = SCENE-015（4/5扉）・IMG-004 = SCENE-019（5/5扉）・IMG-005 = SCENE-025（クロージング）。詳細は `work/image_generation_manifest.md` と `work/scene_prompts/`。
