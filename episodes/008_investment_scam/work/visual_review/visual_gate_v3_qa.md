# Episode 008 Visual Gate v3 QA

確認日: 2026-09-05  
テーマ: `adult_digital_soft_image_bg`  
対象: template 13 scene（SCENE-002/003/005/007/009/010/011/012/014/015/016/017/018）

## 背景asset

- 使用元: `episodes/008_investment_scam/assets/background.png`
- 使用元サイズ: 1672×941 / RGB
- 使用元SHA-256: `EA91E9714434E7DE2DF443886A44409A0BB81A622E4456B917CF04C8B44ED91F`
- 正規化copy: `assets/backgrounds/adult_digital_soft_v2.png`
- 正規化サイズ: 1920×1080 / RGB
- 正規化SHA-256: `CA08D55D445F01B4030856BB39AF9F976DD4A5C92D202928B412838CEF354975`
- 処理: 元画像を変更せず、縦横比維持のcover＋LANCZOSで正規化。背景は全画面に配置し、下部y=900〜1080はrendererの字幕安全帯で覆う。
- `background_asset_pending`: `false`

## Visual Gate判定

| 項目 | 結果 | 根拠 |
|---|---|---|
| template scene数 | 13 | `episode.json`の`render_mode=template` |
| imagegen_native | 5枚を維持 | SCENE-001/004/006/008/013。再生成なし・v2とのSHA-256一致 |
| 装飾の二重描画 | 0 | `overlay_decorations=false`。巨大circle、dots、leaf/wave、背景tint、大きな自動icon backingを無効化 |
| semantic icon plate | PASS | plate 214px / icon 180px。rendererが同じ(cx, cy)から描画し、中心差0px |
| 字幕安全領域 | PASS | y=900〜1080、背景assetに暗い字幕帯なし、renderer overlayのみ |
| background consistency | PASS | template 13 sceneが同一normalized assetを使用。native 5 sceneは対象外で変更なし |
| TV readability | PASS | Scene quality report: 18 OK / 0 WARN / 0 FAIL、template見出し最小83px |
| imagegen_native exact text | PASS候補 | 5 scene、`text_qa_v3`のauto_fail 0。既存目視PASS版を維持し、最終human Gate 2で確定 |
| tiny_text | 0 | 画像QA・配置確認で重大な44px未満情報文字なし |
| overflow | 0 | 全scene 1920×1080、見出し・カード・背景の画面外はみ出しなし |
| text_asset_overlap | 0 | 公式assetなしのtemplate構成、文字とsemantic icon/cardの配置確認PASS |
| icon_plate_misalignment | 0 | 全semantic icon plateの中心差0px |
| double_decoration | 0 | 画像内装飾へrendererの大きな背景装飾を重ねていない |
| blank_white_slide | 0 | image backgroundを意図的な背景として適用し、blank-slide警告0件 |

## Scene別の確認

- SCENE-002: ユーザー背景＋campaign semantic icon＋headline＋support。巨大circleなし。
- SCENE-007: ユーザー背景＋warning semantic icon＋小さなamber plate。背景全体のamber化なし。
- SCENE-009: ユーザー背景＋forum semantic icon＋小さなblue plate。巨大green/blue面なし。
- SCENE-012: ユーザー背景＋green forum icon＋細いgreen accent。別の大きなgreen背景なし。
- SCENE-005: 数字を一つの淡いpanelに集約し、追加motifなし。
- SCENE-015: 比較カードを維持し、見出しは85px級。カード外の追加装飾なし。
- SCENE-017/018: list cardはpale blue-white、薄い境界と軽いshadowで背景の雰囲気を残す。

## 出力

- contact sheet: `work/visual_review/scene_contact_sheet_v3.png`
- background before/after: `work/visual_review/background_before_after.png`
- mechanical report: `work/visual_review/scene_quality_report_v3.json`
- imagegen text report: `work/visual_review/text_qa_v3.md`（既存画像の再生成なし）
- reusable theme: `config/visual_theme.json` / profile `adult_digital_soft_image_bg`

本GateではVOICEVOX、draft.mp4、final.mp4、thumbnail、YouTube uploadを実施しない。最終採用はユーザーのcontact sheet確認後に行う。
