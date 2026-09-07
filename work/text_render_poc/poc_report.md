# text_render_mode 新フロー検証レポート

確認日: 2026-09-03

目的: Episode 007以降の標準である「ImageGenで背景＋文字を同時生成（imagegen_native）→ 文字QA → PASSならそのまま採用」が既存成果物へ影響せず成立することを、本番外サンドボックス1件で確認する。

## 実施内容

1. `work/text_render_poc/episode.json` に短い日本語2行のsceneを1件作成（`render_mode=gpt_image` / `text_render_mode=imagegen_native`・文言「のんびり、いこう。」「今日もいい一日を。」）
2. `scripts/build_image_generation_manifest.py` でmanifestを作成。prompt内に正確な日本語文言・行順・配置・文字スタイル・コントラスト・字幕帯確保・16:9を自動組み込み
3. manifestのpromptでImageGenを **1回だけ** 実行
4. `scripts/text_qa.py` で自動チェック＋親Codexの目視QAを実施 → **PASS**
5. `--mark SCENE-001:PASS` でmanifestのtext_qaを `passed` に記録
6. 本番rendererで採用フレームを生成し、PIL後乗せが行われていないことを確認

## 生成画像

| 項目 | 値 |
|---|---|
| output | `work/text_render_poc/assets/generated_ai/scene_001.png` |
| size | 1672×941（16:9相当） |
| file size | 2,119,383 bytes |
| SHA-256 | `BAAF6CFC9861450483890F413628AA315F5D2990C69641B69C573DB1F8093C49` |
| rendered | 1920×1080（LANCZOS正規化コピー） |

## 文字QA結果（12項目すべてPASS）

- 指定文言一致: 「のんびり、いこう。」「今日もいい一日を。」の2行が正確 ✓
- 誤字・脱字・余計な文字・文字化け・不自然な漢字置換: なし ✓
- 行順: 1行目→2行目の指定どおり ✓
- 文字切れ・画像端のはみ出し: なし ✓
- 人物・重要オブジェクトとの重なり: なし（空と丘の領域） ✓
- コントラスト: 紺文字＋白縁取りで十分 ✓
- スマホ縮小時の可読性: 大きな主見出しで可読 ✓
- 字幕帯（下180px）: 文字・コンテンツなし ✓

機械チェック（`scripts/text_qa.py`）: auto_fail=0。文言仕様の存在・prompt一致・画像配置・アスペクト比・サイズ・SHA-256全てPASS。

## 採用時の挙動

`render_episode_scenes` の出力は `ImageOps.fit(原本, 1920×1080)` と **byte一致**（PIL後乗せなし）。背景と文字が一体のまま採用され、`text_render_mode=imagegen_native` のsceneにはPILオーバーレイが適用されないことを確認。

## メモ（接触sheetレビュー時のWARN候補）

- 指定は「白文字＋紺縁取り」だったが、生成結果は「紺文字＋白縁取り」。コントラスト・可読性は十分で文字QAはPASSだが、スタイル指定の揺れとして記録（次回promptの記述順を厳密化するか、人間判断で許容）。
- 下部に広めの淡い空白帯がある。字幕帯（下180px）は空いており契約上は問題ないが、full-frame契約の「大きな空白」扱いとしてcontact sheetでWARN確認候補。

## 結論

`imagegen_native → QA → PASS → そのまま採用（後乗せなし）` の新フローが成立。本番Episode・既存動画・既存manifestへの変更はなし。API生成は検証用の1回のみ。
