# Episode 008 Visual Plan（2026-09-05・Phase A）

## 基本方針

- 1920×1080 / 30fps / 下部180px字幕安全領域 / TV視聴52.5%前提。
- 文字サイズ: headline ≥80px（目安88〜120）・main fact ≥60px・secondary ≥52px・出典短形 ≥44px・字幕60〜72px（最小56px）。
- 役割分担: 正確なUIは公式素材（今回は未取得のためテンプレート表記）／概念・安心感はGPT画像（imagegen_native）／一覧・数字・比較・注意・まとめはtemplate。
- animation: static既定。GPT画像scene（扉・概念）はvery_slow_zoomのみ。

## scene一覧と実装

| SCENE | layout | render_mode | text_render_mode | 主情報 | icon |
|---|---|---|---|---|---|
| 001 | layout_01_hero | gpt_image | imagegen_native | その投資広告、本物？ | — |
| 002 | layout_01_hero | template | pil_overlay | 高額な被害が、増えています | campaign(navy) |
| 003 | layout_02_list | template | pil_overlay | 今日確認する、3つ | — |
| 004 | layout_08_section | gpt_image | imagegen_native | 1/3扉 | — |
| 005 | layout_01_hero | template | pil_overlay | 6,566件・およそ881億円 | account_balance(blue) |
| 006 | layout_08_section | gpt_image | imagegen_native | 本人がすすめているとは限らない | — |
| 007 | layout_06_caution | template | pil_overlay | 必ずもうかる・あなただけ | warning(amber) |
| 008 | layout_08_section | gpt_image | imagegen_native | 2/3扉 | — |
| 009 | layout_01_hero | template | pil_overlay | LINE誘導はおよそ9割 | forum(blue) |
| 010 | layout_06_caution | template | pil_overlay | サクラがいることも | groups(amber) |
| 011 | layout_06_caution | template | pil_overlay | 相談しないでは詐欺のサイン | group_off(amber) |
| 012 | layout_03_visual_text | template | pil_overlay | LINEは危険ではありません | forum(green) |
| 013 | layout_08_section | gpt_image | imagegen_native | 3/3扉 | — |
| 014 | layout_01_hero | template | pil_overlay | 会社の登録を確認する | verified_user(green) |
| 015 | layout_05_compare | template | pil_overlay | 振込先の2チェック（比較） | — |
| 016 | layout_02_list | template | pil_overlay | まず送金しない・記録を残す・相談 | — |
| 017 | layout_02_list | template | pil_overlay | 相談先3つ（大きな番号） | — |
| 018 | layout_02_list | template | pil_overlay | まとめ | — |

## imagegen_native（IMG-001〜005）生成指示

各sceneのpromptは work/scene_prompts/scene_###.md に保存。共通の禁止事項:
- 実在の有名人・著名人・キャラクターを描かない（顔はシルエット・モザイク・後ろ姿）。
- 実在サービスのロゴ・UI・トーク画面を再現しない（LINE等の実在UI風にしない）。
- QRコード・口座番号・個人情報・政府マーク・警察/金融庁の実在画面を生成しない。
- 日本語の誤字禁止（exact text QA必須）。長文禁止（大見出し1〜2行＋補助0〜1行、30〜40字以内）。

## 進行pill（hybrid）

SCENE-004/008/013は「1/3」「2/3」「3/3」pillをCodex overlayで後付け（imagegen_nativeには生成させない。角丸semi-transparent・secondary 52px相当）。

## official UI（Phase B判断）

- SCENE-014候補: 金融庁「金融事業者一括検索機能」search.fsa.go.jp をPCブラウザcapture（全体2〜4秒→検索欄crop→説明に誘導）。未取得なら現行テンプレート（出典: 金融庁）で公開可。AIでUIを再現しない。

## QA項目（render後）

- tiny_text（<44px FAIL・<52px REVIEW）／unreadable_footer／oversized_single_icon（アイコン15%以上WARN）／1画面1メッセージ／scene repetition／imagegen_native exact text（誤字・脱字・余計な文字・漢字置換・行順・文字切れ）／詐欺画面が本物と誤認されない（「イメージ」ラベル含む）／不安をあおりすぎない（禁止表現なし）。
## 更新（2026-09-05・Visual Gate v2）

- 共通Background System（config/visual_theme.json・adult_digital_soft_background）を全template sceneへ自動適用（soft gradient・section pill・circle/dots/accent line・icon plate・セクション別accent・caution=amber・数字scene=panel・list=rounded card・compare=薄いdepth）。
- SCENE-015ヘッドラインを「振込先に、不審な点は？」へ短縮し80px以上を確保（85px）。
- imagegen_native 5枚は採用案のまま維持（全面再生成なし）。

### Visual Gate v2 QA記録

- tiny_text: 0 / overflow: 0 / text_asset_overlap: 0 / underused_whitespace: 0（意図的な余白は除外）。
- oversized_single_icon: 0 / semantic_icon_quality: PASS / visual_balance: PASS / section_consistency: PASS。
- template_monotony: PASS / TV_readability: PASS / blank_white_slide: 0（template scene最大55%、66%超WARNなし）。
- 機械レポートは `work/visual_review/scene_quality_report_v2.json` に保存（拡張子は既存運用に合わせたレポート形式）。標準ハイブリッド経路で全18sceneを再描画し、FAIL 0 / WARN 0。imagegen_native 5枚は完成背景をそのまま配置し、template側は共通themeを適用。
- imagegen_nativeは既存目視PASS版を維持。v2自動検査は5scene / auto_fail 0（`work/visual_review/text_qa_v2.md`）、最終human Gate 2で確認する。

## 更新（2026-09-05・Visual Gate v3／ユーザー提供背景）

- `episode.json.visual_theme`を`adult_digital_soft_image_bg`へ変更。`episodes/008_investment_scam/assets/background.png`を元画像として保持し、`assets/backgrounds/adult_digital_soft_v2.png`を共通normalized assetとして使用する。
- template 13sceneは背景画像を全面cover＋LANCZOSで適用。`overlay_decorations=false`により、巨大circle・dots・leaf/wave・背景tint・大きなicon backing・全体amber washを追加しない。section pillは画像内の左上装飾を避けて配置し、最小accent lineだけを残す。
- SCENE-002/007/009/012はsemantic icon plateを214px、iconを180pxへ統一し中心差0px。SCENE-005は単一数字panel、SCENE-015は比較カード＋見出し85px級、SCENE-016〜018はpale blue-white list cardを維持。
- native 5scene（001/004/006/008/013）は再生成せず、v2出力とSHA-256一致。v3出力は `work/rendered_final_scenes_v3/`、contact sheetは `work/visual_review/scene_contact_sheet_v3.png`、比較は `background_before_after.png`。

### Visual Gate v3 QA記録

- scene_quality_report: 18 OK / 0 WARN / 0 FAIL。tiny_text 0 / overflow 0 / text_asset_overlap 0 / icon_plate_misalignment 0 / double_decoration 0 / blank_white_slide 0。
- TV readability: PASS / background consistency: PASS / subtitle safe area: PASS（y=900〜1080）/ icon_plate_alignment: PASS（最大中心差0px）。
- 詳細: `work/visual_review/visual_gate_v3_qa.md` および `work/visual_review/scene_quality_report_v3.json`。停止位置はユーザーのGate 2確認待ちで、VOICEVOX・draft/final・thumbnail・YouTube操作は未実施。

## 更新（2026-09-05・Visual Gate v4／中央軸・section pill・不要文字）

- 背景画像とnormalized assetはv3から変更なし。template 13sceneのみrendererのoverlay layoutを局所修正し、imagegen_native 5sceneは再生成しない。
- template常設チャンネル名を削除。section pillは全13sceneで左上（x=90 / y=58）へ復帰し、中央軸をx=960へ統一。
- SCENE-005は数字panelとmessage panelを同幅・同centerへ整列。list（003/016/017/018）は左右margin150px、compare（015）は左右幅790px・gap120px・pair center960px。
- 新QA: `visual_axis_alignment` PASS（最大差0px、許容12px）／`stacked_panel_alignment` PASS（SCENE-005差0px）／`section_pill_anchor` PASS（x=90<300）／`repeated_channel_name` 0。
- v4出力: `work/rendered_final_scenes_v4/`、`work/visual_review/scene_contact_sheet_v4.png`、`work/visual_review/alignment_before_after.png`。停止位置は人間Gate 2確認待ち。

## 更新（2026-09-05・Visual Gate v5／semantic icon可視グリフ中心）

- v4の上部semantic iconの見た目のズレだけを対象とし、背景、section pill、headline、support、panel/list、native 5sceneは変更しない。
- 原因はMaterial Symbols tint PNGの透明キャンバス内で可視グリフがx=192、canvas中心がx=256だったこと。alpha bboxをtrimし、180×180pxの固定visual boxへアスペクト比を維持して再配置する正規化cacheを導入。
- final render PNGの可視tint画素を再計測し、SCENE-002/005/007/009/010/011/012/014のsemantic icon visual centerをx=960軸へ整列。最大axis差0.5px、plateとの差0.5px。
- v5成果物: `work/rendered_final_scenes_v5/`、`work/visual_review/scene_contact_sheet_v5.png`、`work/visual_review/icon_alignment_before_after.png`、`work/visual_review/visual_gate_v5_qa.md`、`work/visual_review/scene_quality_report_v5.json`。人間Gate 2は2026-09-05承認済み。Phase Bのdraft_v1へ固定使用。
