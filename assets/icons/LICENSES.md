# Icon asset licenses & provenance

## Library

- **Name**: Material Symbols Rounded（Google Fonts / Material Design Icons）
- **License**: Apache License 2.0
- **Official source**: https://github.com/google/material-design-icons （`symbols/web/<name>/materialsymbolsrounded/`）
- **Downloaded**: 2026-09-04（raw.githubusercontent.com の公式masterブランチから直接取得。第三者サイトの再配布SVGは不使用）

## Icons

| File (SVG source) | derived assets (tint PNG) | License | Source URL | Downloaded | Episode / Scene usage |
|---|---|---|---|---|---|
| login_wght700_48px.svg | login_navy.png | Apache 2.0 | https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/login/materialsymbolsrounded/login_wght700_48px.svg | 2026-09-04 | 007 / SCENE-001（ログインできない？） |
| lock_wght700_48px.svg | lock_blue.png | Apache 2.0 | https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/lock/materialsymbolsrounded/lock_wght700_48px.svg | 2026-09-04 | 007 / SCENE-006（端末ロック必須） |
| fingerprint_wght700_48px.svg | （未使用・catalog登録のみ） | Apache 2.0 | https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/fingerprint/materialsymbolsrounded/fingerprint_wght700_48px.svg | 2026-09-04 | 007 / catalog（生体認証） |
| contactless_wght700_48px.svg | contactless_blue.png | Apache 2.0 | https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/contactless/materialsymbolsrounded/contactless_wght700_48px.svg | 2026-09-04 | 007 / SCENE-010（読み取り注意） |
| block_wght700_48px.svg | block_amber.png | Apache 2.0 | https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/block/materialsymbolsrounded/block_wght700_48px.svg | 2026-09-04 | 007 / SCENE-013（何度も試さない） |
| support_agent_wght700_48px.svg | support_agent_green.png | Apache 2.0 | https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/support_agent/materialsymbolsrounded/support_agent_wght700_48px.svg | 2026-09-04 | 007 / SCENE-020（公式窓口相談） |

## Processing

- SVG → 512×512 transparent PNG: Edge headless（公式SVGを直接描画）。白背景は明度→アルファ変換で除去（antialiased edge保持）。
- tint: 単色アイコンをsceneトーン（navy #173a68 / blue #2f74bb / green #3f8c58 / amber #c07d1e）へ一色化。`assets/icons/material_symbols/<name>_<tone>.png`。
- 背景円（淡色 tone circle）はscene rendererの描画（ICON_CIRCLE）。アイコン本体とは別管理。
- 配布条件（Apache 2.0）: 著作権表示を本ファイルに保持。改変（tint・リサイズ）は同ライセンスで再利用可。
| dialpad_wght700_48px.svg | dialpad_blue.png | Apache 2.0 | https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/dialpad/materialsymbolsrounded/dialpad_wght700_48px.svg | 2026-09-04 | 007 / SCENE-012（暗証番号・数字4桁） |
| badge_wght700_48px.svg | badge_blue.png | Apache 2.0 | https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/badge/materialsymbolsrounded/badge_wght700_48px.svg | 2026-09-04 | 007 / SCENE-015（カード自体の期限） |
| construction_wght700_48px.svg | construction_blue.png | Apache 2.0 | https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/construction/materialsymbolsrounded/construction_wght700_48px.svg | 2026-09-04 | 007 / SCENE-018（障害・メンテナンス確認） |
| lock_reset_wght700_48px.svg | lock_reset_blue.png | Apache 2.0 | https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/lock_reset/materialsymbolsrounded/lock_reset_wght700_48px.svg | 2026-09-04 | 007 / SCENE-019（暗証番号の再設定） |
