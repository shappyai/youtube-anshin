# Episode 008 Visual Gate v5 QA

実施日: 2026-09-05  
対象: 上部 semantic icon の可視グリフ中心だけを局所修正

人間Gate 2: **APPROVED（2026-09-05）**。以下のPhase Bでは、このv5を固定して使用した。

## 1. 変更範囲

- v4のユーザー提供背景、section pill、headline、support、panel/list、SCENE-005下部message panelは変更していない。
- imagegen_nativeの5scene（SCENE-001 / 004 / 006 / 008 / 013）は再生成していない。
- VOICEVOX、draft/final、thumbnail、YouTube操作は実施していない。
- v1〜v4の出力は上書きしていない。v5は別ディレクトリへ出力した。

## 2. 上部semantic iconのずれの原因

元のMaterial Symbols tint PNGは512×512の透明キャンバスで、可視グリフがキャンバス中央ではなくx=192付近に寄っていた。代表例の可視アルファbboxは次の通り。

| icon | source canvas | visible alpha bbox | visible center x | canvas centerとの差 |
|---|---:|---:|---:|---:|
| campaign_navy | 512px | (32,196)-(352,444) | 192 | -64px |
| account_balance_blue | 512px | (32,147)-(352,464) | 192 | -64px |
| warning_amber | 512px | (24,172)-(360,464) | 192 | -64px |
| forum_blue / forum_green | 512px | (32,160)-(352,463) | 192 | -64px |
| groups_amber | 512px | (0,224)-(384,416) | 192 | -64px |
| group_off_amber | 512px | (15,160)-(369,491) | 192 | -64px |
| verified_user_green | 512px | (64,161)-(320,479) | 192 | -64px |

従来の「512pxキャンバス全体を180pxへ縮小」では、この透明余白を含めて配置するため、可視グリフが意図した軸より約22.5px左へ見えていた。原因はSVG/PNGの意味やplate位置ではなく、元PNG内の透明余白と可視グリフbboxの不一致である。

## 3. v5の正規化方法

- 元のSVG/PNGは変更せず、alpha threshold=4で可視アルファbboxを検出。
- alpha bboxだけをtrimし、アスペクト比を維持したまま固定180×180pxの透明visual boxへcontain配置。
- visual boxの中心をplate中心（x=960）へ配置。
- 正規化キャッシュは `assets/icons/material_symbols_normalized/` に保存。元素材のライセンス・catalog定義は変更していない。

## 4. 最終render PNGのpixel/bbox QA

icon tintの最終render画素から可視グリフbboxを再計測した。plate中心は全対象でx=960px。

| scene | final visible glyph bbox | glyph center x | axis差 | glyph−plate差 | 判定 |
|---|---|---:|---:|---:|---|
| SCENE-002 campaign | (870,156)-(1050,294) | 960.0 | 0.0px | 0.0px | PASS |
| SCENE-005 account_balance | (870,116)-(1050,294) | 960.0 | 0.0px | 0.0px | PASS |
| SCENE-007 warning | (871,137)-(1049,293) | 960.0 | 0.0px | 0.0px | PASS |
| SCENE-009 forum | (870,120)-(1050,290) | 960.0 | 0.0px | 0.0px | PASS |
| SCENE-010 groups | (870,170)-(1050,260) | 960.0 | 0.0px | 0.0px | PASS |
| SCENE-011 group_off | (870,131)-(1050,298) | 960.0 | 0.0px | 0.0px | PASS |
| SCENE-012 forum | (870,135)-(1050,305) | 960.0 | 0.0px | 0.0px | PASS |
| SCENE-014 verified_user | (887,135)-(1032,314) | 959.5 | 0.5px | 0.5px | PASS |

QA threshold: `semantic_icon_visual_center` は axis差4px以下、glyph−plate差2px以下。v5の最大値はそれぞれ0.5px / 0.5pxで、PASS。

## 5. v4レイアウト保持確認

- SCENE-005の上部数字panelと下部message panel: v4から幅・center_xとも不変。panel regression=0。
- section pill: 全template 13sceneでx=90 / y=58を維持。`section_pill_anchor=PASS`。
- 背景: source SHA-256 `EA91E9714434E7DE2DF443886A44409A0BB81A622E4456B917CF04C8B44ED91F`、normalized SHA-256 `CA08D55D445F01B4030856BB39AF9F976DD4A5C92D202928B412838CEF354975`。v4から不変。
- native 5scene: v4/v5のSHA-256一致（SCENE-001 / 004 / 006 / 008 / 013）。

## 6. Visual Gate v5 mechanical QA

- scene_quality_report: **18 OK / 0 WARN / 0 FAIL**
- `semantic_icon_visual_center`: PASS
- `icon_plate_alignment`: PASS（最大中心差0px）
- `visual_axis_alignment`: PASS（最大差0px）
- `stacked_panel_alignment`: PASS（SCENE-005最大差0px）
- `section_pill_anchor`: PASS
- `tiny_text=0` / `overflow=0` / `text_asset_overlap=0` / `channel_name_in_scene=0`
- SCENE-005 panel regression=0 / background regression=0
- subtitle safe area: PASS（y=900〜1080）

## 7. v5成果物

- render: `work/rendered_final_scenes_v5/`
- contact sheet: `work/visual_review/scene_contact_sheet_v5.png`
- icon比較: `work/visual_review/icon_alignment_before_after.png`（左=v4、右=v5、SCENE-002/005/007/009/012/014）
- mechanical report: `work/visual_review/scene_quality_report_v5.json`

## 8. Phase B引き継ぎ

- draft QAでSCENE-007のsupport textに仮名途中分断が検出されたため、文言を変更せず意味の切れ目で改行を固定した。背景・icon・plate・headline・panel・imagegen_nativeは変更していない。
- `work/rendered_final_scenes_v5/`をdraft_v1の唯一のscene入力として使用した。代表フレームでもsemantic icon、背景、字幕安全帯、CTA reserved領域の回帰なし。

停止位置: **draft_v1完成。全編の人間視聴・thumbnail確定・YouTube操作は未実施**。
