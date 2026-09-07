# Episode 008 Visual Gate v4 QA

確認日: 2026-09-05

## 変更範囲

- v3の背景画像（`assets/backgrounds/adult_digital_soft_v2.png`）は変更せず、そのまま全面coverで使用。
- 元画像 `assets/background.png` とnormalized assetのSHA-256はv3記録と一致。
- template 13sceneを `work/rendered_final_scenes_v4/` へ再render。
- imagegen_native 5scene（SCENE-001/004/006/008/013）は再生成せず、既存画像をそのまま使用。
- templateの常設チャンネル名overlayを13sceneから削除。native画像に焼き込まれた文字は今回変更しない。
- 背景画像上のcircle・dots・leaf/wave等は追加せず、rendererが担当するのはsection pill・semantic icon・必要最小限のaccent line・字幕安全帯のみ。

## 配置QA

- section pill: template 13sceneを左上へ復帰。`x=90 / y=58`、`x<300`をPASS。
- template heroのsemantic icon: 共通center `x=960`。plateは直径214px、iconは180px、中心差0px。
- SCENE-002: 「はじめに」を左上へ戻し、campaign icon/plateを上部中央へ配置。headline/supportも中央軸へ整列。
- SCENE-005: 数字panel `(350,350)-(1570,690)` と下部message panel `(350,778)-(1570,898)` を同じ `center_x=960`・同じ幅1220pxへ整列。icon→数字→source/support→messageの縦階層を維持。
- SCENE-007: warning semantic icon/plate、headline、support、messageを中央軸へ維持。背景全体のamber washは追加しない。
- SCENE-009: forum icon/plate、数字headline、support、messageを中央軸へ整列。
- SCENE-012/014: semantic icon/plateとheadline/support/main messageを中央軸へ整列。
- SCENE-003/016/017/018: list cardの左右marginを `150px / 150px` で統一し、全体center `x=960`。section pillだけ左上。
- SCENE-015: headlineと左右カードを中央配置。カード幅790px、gap120px、pair center `x=960`。

## 機械QA

- scene_quality_report: **18 OK / 0 WARN / 0 FAIL**
- tiny_text: 0
- overflow: 0
- text_asset_overlap: 0
- channel_name_in_scene: 0（template renderer/template sourceに常設overlayなし）
- icon_plate_misalignment: 0（最大中心差0px、許容2px）
- visual_axis_alignment: **PASS**（最大差0px、許容12px）
- stacked_panel_alignment: **PASS**（SCENE-005最大差0px、許容12px）
- section_pill_anchor: **PASS**（template x=90px、基準x<300）
- subtitle_safe_area: **PASS**（y=900〜1080）
- background_consistency: **PASS**
- TV_readability: **PASS**
- blank_white_slide: 0（画像背景自身の白面はraw値として保持し、誤警告しない）

## Native文字QA

`text_qa_v4.md`: 5 imagegen_native scene / auto_fail=0。既存の人間確認対象を維持し、再生成・再文字入れは行っていない。

## 出力

- contact sheet: `scene_contact_sheet_v4.png`
- v3→v4整列比較: `alignment_before_after.png`（SCENE-002/005/007/009/012/015/017）
- mechanical report: `scene_quality_report_v4.json`

## 停止位置

Visual Gate v4まで。VOICEVOX、draft、thumbnail、final、uploadは未実施。次は人間Gate 2（v4 contact sheet＋pronunciation REVIEW）。
