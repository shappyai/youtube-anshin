# Scene mode advisor — Episode 005

Visual Agent（`work/subagents/005_google_photos_delete/visual_plan.json`）の推奨を親Codexが確認・統合した結果。エピソード005はGoogleフォトの実画面が主役のため、実画面（Emulator/iPhone）とtemplateが中心、GPT画像は概念・安心のみ5枚に絞る。

| Scene | シーン目的 | Render mode | Device | 理由 |
|---|---:|---|---|---|
| SCENE-001 | 導入 | gpt_image | gpt_image | 人物・安心感。GoogleフォトUIは描かない |
| SCENE-002 | 一覧（3項目） | template | template | layout_02_list。文字中心 |
| SCENE-003 | 1/6 扉（バックアップ概念） | gpt_image | gpt_image | コピーを預ける概念。実UI不要 |
| SCENE-004 | 1/6 実演（バックアップ確認） | official | emulator | 実画面が主役。Emulatorで撮影 |
| SCENE-005 | 2/6 扉 | template | template | layout_08_section |
| SCENE-006 | 2/6 実演（削除操作） | official | emulator | 実画面が主役 |
| SCENE-007 | 2/6 比較表（削除行） | template | template | 「何が消えるか」表の初出し |
| SCENE-008 | 2/6 実演（ゴミ箱画面） | official | emulator | 実画面＋60/30日はCodex後描画 |
| SCENE-009 | 2/6 注意（削除前の確認） | template | template | layout_06_caution。恐怖演出なし |
| SCENE-010 | 3/6 扉 | template | template | layout_08_section |
| SCENE-011 | 3/6 比較表（デバイスから削除行） | template | template | Scene-007と同一レイアウト |
| SCENE-012 | 3/6 実演（メニュー表示） | official | emulator | 実画面でメニュー名を確認 |
| SCENE-013 | 4/6 扉（容量が空く概念） | gpt_image | gpt_image | 概念イラスト |
| SCENE-014 | 4/6 実演（空き容量を増やす） | official | emulator | 実画面が主役 |
| SCENE-015 | 4/6 比較表（空き容量を増やす行） | template | template | Scene-007と同一レイアウト |
| SCENE-016 | 4/6 容量の区別（2つの箱） | template | template | 正確な日本語を後描画 |
| SCENE-017 | 5/6 扉（本体写真とバックアップコピー） | gpt_image | gpt_image | iOS固有UIなし。本体写真からバックアップコピーへつながる概念 |
| SCENE-018 | 5/6 実演（2つの場所の関係） | official | iphone | 実機またはApple公式ページ |
| SCENE-019 | 5/6 実演（最近削除した項目） | official | iphone | 実機またはApple公式ページ |
| SCENE-020 | 5/6 比較（2つのゴミ箱） | template | template | layout_05_compare |
| SCENE-021 | 6/6 扉 | template | template | layout_08_section |
| SCENE-022 | 6/6 実演（復元） | official | emulator | 実画面が主役 |
| SCENE-023 | 6/6 注意（早めの確認） | template | template | layout_06_caution |
| SCENE-024 | まとめ（4項目） | template | template | layout_07_summary＋summary_stagger |
| SCENE-025 | クロージング | gpt_image | gpt_image | 家族の安心感 |
| CTA | 共通CTA | template | template | channel_common_cta（postroll・ナレーションなし） |

## Count

- template: 12
- official（実画面）: 8（Android Emulator 6 / iPhone実機or公式 2）
- gpt_image: 5
- CTA: postroll（scene数に含めない）

## 判断メモ（2026-09-01・Episode 005用）

- 「デバイスから削除」はiOSにも公式手順がある（2026-09-01）が、実機アプリのメニュー表示はバージョン差があり得るため、SCENE-012の字幕で「機種やアプリのバージョンによって違う場合があります」と留保し、Phase BのEmulatorで挙動確認する。
- GPT画像5枚はいずれも「GoogleフォトのUI・ロゴ・正確な日本語を生成しない」契約。公式画面の代替には使わない。
- 比較表はSCENE-007で3操作×2列の全体を初出しし、SCENE-011・015で同一レイアウト＋ハイライト行のみ変更（重複説明を防ぐ）。
- CTAは既存のchannel_common_cta固定。「怖がらせる前に、確認する。」はCTAに含めない。
