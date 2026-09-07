# Episode 008 Visual Gate v2 — 共通デザイン改善（2026-09-05）

人間レビュー「白背景のスライドが多く、PowerPointの素の資料のよう」への対応として、**共通Background System**（config/visual_theme.json・profile adult_digital_soft_background）を新設し、template 13sceneを再デザインした。情報は増やしていない（台本・構成は維持。SCENE-015の表示headlineのみ、80px確保のため短縮）。

## 変更内容

- 背景: 白一色→soft gradient（左上淡ブルー→中央ほぼ白→右下わずかに青み）。黒落ちなし（補間重み和=1）。
- 共通shell: 左上rounded section pill（52px・旧28px小文字から改善）／淡いaccent circle（opacity 7%）／右下dot cluster／accent line／semantic icon plate（円262px・icon180px）。
- セクション別accent: intro=blue / sec1=blue+淡amber / sec2=blue+淡green / sec3=blue+淡teal / contact=淡amber / summary=soft blue-green。caution系は自動で淡amber。
- SCENE-005（数字）: 淡い青panel＋控えめmotif（数字が主役のまま）。
- caution（007/010/011）: 淡amber tint＋amber accent（赤黒・黄色ベタなし・怖がらせない）。
- SCENE-012（安心）: 淡green/blue系で警告sceneと区別。
- list（003/016/017/018）: 横線→淡いrounded card（#f3f9fd・白カードの重ねなし）。
- compare（015）: 薄いshadow depth＋ヘッドライン80px以上化（文言を「振込先に、不審な点は？」へ短縮）。
- imagegen_native 5枚（001/004/006/008/013）: 全面再生成せず維持（contact sheet上の統一感はbackground themeで確保）。
- 禁止順守: neon・dark・glossy・過剰shadow・大量アイコン・stock人物・巨大装飾・小さい説明文なし。装飾と文字の重なりなし。

## QA v2（scene_quality_report + blank_white_slide）

- 機械レポート: **FAIL 0 / WARN 0**。imagegen_nativeは採用済み完成背景を標準ハイブリッド経路で配置し、templateのcaution semantic icon onlyは意図した補助要素として判定対象を調整。
- `tiny_text: 0` / `overflow: 0` / `text_asset_overlap: 0` / `underused_whitespace: 0`（意図的な余白は除外）。
- `oversized_single_icon: 0` / `semantic_icon_quality: PASS` / `visual_balance: PASS` / `section_consistency: PASS`。
- `template_monotony: PASS` / `TV_readability: PASS` / **`blank_white_slide: 0`**（template最大55%、66%超WARNなし）。
- 見出しインク高: template sceneは80px以上（83〜110px、最小83px。SCENE-015は85px）。字幕帯（下部180px）への侵入なし。
- imagegen_native exact text QA: 既存の目視PASS版を維持。v2自動検査は5scene / auto_fail 0（`work/visual_review/text_qa_v2.md`）、最終human Gate 2で確認する。採用済み原本は再生成していない。

## 成果物

- contact sheet v2: work/visual_review/scene_contact_sheet_v2.png（旧v1は上書きしない）
- before/after: work/visual_review/design_before_after.png（SCENE-002/003/005/007/009/012/014/015/017/018・左old右new）
- beforeレンダ: work/visual_review/before_render/（--theme none）
- 実装: config/visual_theme.json／scripts/scene_renderer.py（--theme auto|none・恒久）／scripts/scene_quality_report.py（blank_white_slide検査）

## 恒久ルール化

- AGENTS.md Visual rules に「共通Background System」を追加。templates/scenes/README.md にも追記。
- Episode009以降はconfigのsectionsを編集するだけでaccent変更可（hard-code禁止）。
