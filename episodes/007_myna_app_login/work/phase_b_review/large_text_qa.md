# 高可読性版（小文字廃止）QA — Episode 007（2026-09-04）

## tiny_text（情報文字の最小サイズ・構造値）
- SCENE-004: main 68px / secondary 52px / source「出典：マイナアプリ公式」44px / 小文字なし
- SCENE-005: main 76px / secondary 52px / source 44px / 小文字なし
- SCENE-008: main 76px / secondary 52px / source 44px / 小文字なし（2カラム）
- SCENE-009: main 66px / secondary 52px / source 44px / 小文字なし（2カラム）
- SCENE-012: main「数字4桁」96px / secondary 52px / source 44px / 小文字なし
- SCENE-015: main 76px / secondary 52px / source 44px / 小文字なし
- SCENE-018: main 72px / secondary 52px / source 44px / 小文字なし
- SCENE-019: main 72px / secondary 52px / source 44px / 小文字なし
- 判定: 情報文字の最小=44px（出典短形）≥ 基準44px → tiny_text=0 PASS

## unreadable_footer
- 対象8scene: 下部のURL全文・確認日・※注記・細かいsourceを全削除。残るのは「出典：○○公式」44pxのみ（y<=830・字幕帯外）。footerブランド名は非情報ブランドタグ（32px）。unreadable_footer=0 PASS

- SCENE-004 overflow: right=0 bottom=0 PASS
- SCENE-005 overflow: right=0 bottom=0 PASS
- SCENE-008 overflow: right=0 bottom=0 PASS
- SCENE-009 overflow: right=0 bottom=0 PASS
- SCENE-012 overflow: right=0 bottom=0 PASS
- SCENE-015 overflow: right=0 bottom=0 PASS
- SCENE-018 overflow: right=0 bottom=0 PASS
- SCENE-019 overflow: right=0 bottom=0 PASS
- SCENE-008 text_asset_overlap: left_edge_ink=0 PASS
- SCENE-009 text_asset_overlap: left_edge_ink=0 PASS

## Summary: tiny_text=0 / unreadable_footer=0 / overflow=PASS / overlap PASS / official facts unchanged / scene mapping PASS
