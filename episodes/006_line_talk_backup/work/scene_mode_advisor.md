# Scene mode advisor — Episode 006

Visual Agent（`work/subagents/006_line_talk_backup/visual_plan.json`）の推奨を親Codexが確認・統合した結果。Episode 006はLINE公式手順と公式仕様が主役。Android Emulator/iPhoneの実画面は優先確認したが取得条件を満たさず、保存HTML由来の公式手順引用カードへfallbackした。GPT画像は概念・安心のみ5枚に絞り、LINEのUI・ロゴはAIで生成しない。PINの注意はSCENE-017へ統合し、sceneは24件。

| Scene | シーン目的 | Render mode | Device | 理由 |
|---|---:|---|---|
| SCENE-001 | 導入 | gpt_image | gpt_image | 人物・安心感（IMG-001）。LINE UIは描かない |
| SCENE-002 | 一覧（3項目） | template | template | layout_02_list。文字中心 |
| SCENE-003 | 1/5 扉（引き継ぎとバックアップは別） | gpt_image | gpt_image | 概念イラスト（IMG-002） |
| SCENE-004 | 1/5 時系列（前・当日・後） | template | template | 正確な日本語を後描画 |
| SCENE-005 | 1/5 両方の準備が必要 | template | template | layout_05_compare |
| SCENE-006 | 2/5 手順引用（設定→バックアップ・引き継ぎ） | official | android_emulator→official fallback | SHOT-01。LINE未インストールのため公式引用カード |
| SCENE-007 | 2/5 手順引用（バックアップ日時・今すぐ） | official | android_emulator→official fallback | SHOT-02。LINE未インストールのため公式引用カード |
| SCENE-008 | 2/5 概念（コピーが外に作られる） | template | template | クラウド保管のイメージ。公式UIなし |
| SCENE-009 | 2/5 保存先比較（iCloud Drive / Google ドライブ） | template | template | layout_05_compare。公式表記 |
| SCENE-010 | 2/5 注意（メイン端末だけ・文字だけ） | template | template | layout_06_caution |
| SCENE-011 | 3/5 手順引用（自動バックアップ設定） | official | android_emulator→official fallback | SHOT-03。LINE未インストールのため公式引用カード |
| SCENE-012 | 3/5 条件比較（iPhone5条件/Android2条件） | template | template | layout_05_compare。公式表記 |
| SCENE-013 | 3/5 注意（オフのままにしない） | template | template | layout_06_caution |
| SCENE-014 | 3/5 手順引用（iPhone: iCloud Drive確認） | official | iphone→official fallback | SHOT-04。実機未取得のため公式引用カード |
| SCENE-015 | 4/5 扉（PIN=鍵） | gpt_image | gpt_image | 概念イラスト（IMG-003）。数字・PIN画面なし |
| SCENE-016 | 4/5 手順引用（PIN設定） | official | android_emulator→official fallback | SHOT-05。LINE未インストールのため公式引用カード。値は映さない |
| SCENE-017 | 4/5 概念＋注意（直近14日間のセーフティネット／推測されやすい番号を避ける） | template | template | layout_03_visual_text。10回失敗は本編で扱わない |
| SCENE-019 | 5/5 扉（OSをまたぐ） | gpt_image | gpt_image | 概念イラスト（IMG-004）。実機・ロゴなし |
| SCENE-020 | 5/5 公式文言引用（同じOSのみ） | official | line_official | SHOT-06。保存HTML由来の引用カード |
| SCENE-021 | 5/5 比較（同じOS/異なるOS） | template | template | layout_05_compare |
| SCENE-022 | 5/5 公式文言引用（写真動画は対象外） | official | line_official | SHOT-07。保存HTML由来の引用カード |
| SCENE-023 | 5/5 参考（プレミアムバックアップ・引き継ぎ準備） | template | template | 勧誘しない。解約注意のみ |
| SCENE-024 | まとめ（3項目チェック） | template | template | layout_07_summary＋summary_stagger。オープニングと同一 |
| SCENE-025 | クロージング | gpt_image | gpt_image | 人物・安心感（IMG-005） |
| CTA | 共通CTA | template | template | channel_common_cta（postroll・音声あり） |

## Count

- template: 12
- official: 7（Android実画面fallback 4・iPhone実画面fallback 1・LINE公式文言引用 2）
- gpt_image: 5
- CTA: postroll（scene数に含めない）

## 判断メモ（2026-09-02・Episode 006用）

- LINE実画面を取得できる場合はテストアカウントのみ（実トーク・友だち一覧・通知・QRコード・LINE ID・電話番号・プロフィール写真を映さない）。今回は実画面を使わず、PINは値・入力欄の数字を映さない公式引用カードにした。
- GPT画像5枚はいずれも「LINEのUI・ロゴ・正確な日本語を生成しない」契約。公式画面の代替には使わない。
- 実画面の導線・表示名はバージョン差があり得るため、SCENE-006/007のsupport_textと説明欄に「機種やバージョンで表示が違う場合があります」の留保を記載。引用カードは実在UIではないことを明示。
- 比較表はSCENE-009（保存先）・SCENE-012（自動条件）・SCENE-021（OSまたぎ）の3種。同じテンプレートレイアウトを使い分ける。
- CTAは既存のchannel_common_cta固定（`config/channel_cta.json`準拠・音声あり）。「怖がらせる前に、確認する。」はCTAに含めない。
