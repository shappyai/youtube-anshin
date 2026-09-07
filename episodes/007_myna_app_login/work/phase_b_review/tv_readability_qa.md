# TV readability QA — Episode 007（2026-09-04）

- SCENE-004 overflow: right=0 bottom=0 PASS
- SCENE-005 overflow: right=0 bottom=0 PASS
- SCENE-008 overflow: right=0 bottom=0 PASS
- SCENE-009 overflow: right=0 bottom=0 PASS
- SCENE-012 overflow: right=0 bottom=0 PASS
- SCENE-015 overflow: right=0 bottom=0 PASS
- SCENE-018 overflow: right=0 bottom=0 PASS
- SCENE-019 overflow: right=0 bottom=0 PASS

- tv_text_size (Level-1 main font px): SCENE-004=68, SCENE-005=76, SCENE-008=72, SCENE-009=66, SCENE-012=96, SCENE-015=76, SCENE-018=72, SCENE-019=72
  - 基準: 64〜76px（012は「数字4桁」強調のため96px）。source系は24〜26pxに分離。
- SCENE-008 text_asset_overlap: panel_ink_ratio=0.00003 left_edge_ink=0 PASS
- SCENE-009 text_asset_overlap: panel_ink_ratio=0.00003 left_edge_ink=0 PASS

## Summary: overflow=PASS(all 8) / tv_text_size recorded / overlap=PASS
