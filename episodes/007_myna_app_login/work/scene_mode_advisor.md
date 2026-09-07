# Scene mode advisor — Episode 007

Visual Agent（`work/subagents/007_myna_app_login/visual_plan.json`）の推奨を親Codexが確認・統合した結果。Episode 007はマイナアプリの実画面・公式ページcropが主役。TV-first readability（Episode 002のテレビ視聴約52.5%）を全sceneに適用。GPT画像は概念のみ2枚に絞り、マイナアプリ/マイナポータルの実UI・ロゴ・政府マークをAIで生成しない。

| Scene | シーン目的 | Render mode | Device | 理由 |
|---|---|---|---:|---|
| SCENE-001 | オープニング（問題提示・結論） | template | template | layout_01_hero。大字テキストのみ・実UIなし。0〜5秒で困りごと |
| SCENE-002 | 一覧（5項目） | template | template | layout_02_list。冒頭の一覧（まとめSCENE-021と完全一致） |
| SCENE-003 | 1/5 扉（スマホ対応） | template | template | layout_08_section。imagegen_native（短い文言） |
| SCENE-004 | 1/5 動作環境（対応OS・NFC） | official | pc_browser | SHOT-01。全体2〜4秒→対応OS行を大きくcrop |
| SCENE-005 | 1/5 公式FAQ（通常モード・更新） | official | pc_browser | SHOT-02。シークレットモード記載をcrop |
| SCENE-006 | 1/5 注意（端末ロック必須） | template | template | layout_06_caution。公式の必須項目 |
| SCENE-007 | 2/5 扉（読み取りの概念） | gpt_image | gpt_image | IMG-001。スマホ（画面ぼかし）+カード（非表示）。UI・ロゴなし |
| SCENE-008 | 2/5 iPhone読み取り位置 | official | iphone実機→公式図解crop | SHOT-04。NFC実演は実機必須 |
| SCENE-009 | 2/5 Android読み取り位置 | official | android実機→公式図解crop | SHOT-05。機種により背面位置が違う |
| SCENE-010 | 2/5 注意（動かさない・ケース・金属等） | template | template | layout_06_caution。4つの注意を1画面に |
| SCENE-011 | 3/5 扉（暗証番号） | template | template | layout_08_section。imagegen_native |
| SCENE-012 | 3/5 暗証番号（数字4桁・顔/指紋） | official | pc_browser | SHOT-06。公式registerの案内をcrop。入力値は映さない |
| SCENE-013 | 3/5 注意（ロック・何度も試さない） | template | template | layout_06_caution。最重要の安全規約 |
| SCENE-014 | 4/5 扉（期限） | template | template | layout_08_section。imagegen_native |
| SCENE-015 | 4/5 カード有効期限 | official | pc_browser | SHOT-07。公式ページをcrop |
| SCENE-016 | 4/5 比較（カード期限/証明書期限） | template | template | layout_05_compare。「別もの」を視覚化 |
| SCENE-017 | 5/5 扉（それでもダメなら） | template | template | layout_08_section。imagegen_native |
| SCENE-018 | 5/5 障害・メンテナンス | official | pc_browser | SHOT-08。公式ページの存在を大きく |
| SCENE-019 | 5/5 再設定（コンビニ・窓口） | official | pc_browser | SHOT-09。条件付き案内（公式文言） |
| SCENE-020 | 5/5 窓口（フリーダイヤル・002案内） | template | template | 番号はpil_overlayの大きな文字。002案内1文 |
| SCENE-021 | まとめ（5項目） | template | template | layout_07_summary＋summary_stagger。冒頭と同一 |
| SCENE-022 | クロージング | gpt_image | gpt_image | IMG-002。安心の締め。短い文言をimagegen_native |
| CTA | 共通CTA | template | template | channel_common_cta（postroll・音声あり） |

## Count

- template: 12
- official: 8（公式Web crop 6・実機読み取り実演 2※取得できなければ公式図解cropへfallback）
- gpt_image: 2
- CTA: postroll（scene数に含めない）

## TV-first readability（Episode 007の正式QA項目）

- 見出し80〜140px級・補足48〜60px級・1画面1メッセージ。下部180px（y≥900）字幕帯を全sceneで空ける。
- 一覧・注意・比較（SCENE-002/010/016/021）は項目1行に短縮し行間を広げる（REVIEW→人間のcontact sheet確認）。
- 数字・公式名・電話番号（iOS 16.4・4桁・3回・10回目・5回目・0120-95-0178）はすべてpil_overlay（正確性優先）。
- officialは「全体2〜4秒→該当箇所を大きくcrop」の2段階。crop後に1920×1080 frameで読めることを実測。
- 色だけで区別しない（アイコン・形・番号を併用）。

## 判断メモ（2026-09-03・Episode 007用）

- マイナアプリ実画面（読み取り・暗証番号入力）はテストアカウント/テストカードのみ。実物カードの個人情報（マイナンバー・氏名・生年月日・住所・顔写真・カード表裏・暗証番号・QRコード）を映さない。「あとでモザイク」運用は禁止。
- GPT画像2枚はいずれも「マイナアプリ/マイナポータルの実UI・ロゴ・政府マーク・QRコード・番号風文字列を生成しない」契約。text_render_mode=imagegen_native（文字QA FAIL→1回再生成→2回目FAILはpil_overlayへfallback）。
- 実画面の導線・表示名はバージョン差があり得るため、SCENE-004/005/012等のsupport_textと説明欄に留保を記載。引用カードは実在UIではないことを明示。
- 読み取り実演（SCENE-008/009）はAndroid EmulatorではNFCが成立しないため実機必須。取得できない場合はjpki.go.jp等の公式図解cropへfallback（manifestに記録済み）。
- CTAは既存のchannel_common_cta固定（`config/channel_cta.json`準拠・音声あり）。「怖がらせる前に、確認する。」はCTAに含めない。

## fallback一覧

- SHOT-01/02/06/07/08/09（公式Web）: 公式保存HTML由来の引用カード→取得できれば実機/エミュレータ併用
- SHOT-04/05（読み取り実演）: iPhone/Android実機→jpki.go.jp等の公式図解crop・公式引用カード
- SHOT-03/クロージング（GPT）: 文字QA FAIL時はpil_overlay（背景+後描画文字）
