# Episode 003 scene QA — Phase B前半

確認日: 2026-08-31  
対象: 18sceneの静止画合成のみ。音声・動画・サムネイルは未生成。

## Automated QA

| Check | Result | Detail |
|---|---|---|
| GPT画像の存在 | PASS | 8 / 8。`scene_001.png`、`003`、`007`、`010`、`013`、`014`、`016`、`018` |
| GPT画像の形式・解像度 | PASS | 全てPNG、1920×1080、Pillowで破損なしを確認 |
| GPT画像safe area | PASS | 下部180pxの可視コンテンツ警告なし |
| 18sceneレンダリング | PASS | 18 / 18、全て1920×1080、レンダーエラーなし |
| official asset / placeholder | PASS | 宣言済み公式素材の未配置・placeholderなし |
| headline overflow | PASS | 各render modeの既定テキスト領域で行数・幅・高さを確認 |
| subtitle safe area | PASS | AI入力preflightとtemplate/officialレンダラーの下180px帯を確認 |
| template fallback | PASS | GPT対象8sceneをtemplateへfallbackしていない |

## 人間確認が必要な項目

- GPT画像の意味・魅力・人物の自然さは未承認。特にSCENE-001、014、018を確認する。
- 公式画面の最終的な読みやすさは、フルサイズのSCENE-004、005、006、008、009、011、012で確認する。
- SCENE-004、011は全体像を理解する短時間表示、SCENE-005、006、008、009、012は説明対象を大きく見せる用途とした。
- 公式スクリーンショットとGPT画像・templateの色調差は許容範囲に収まっているが、番組全体としての最終判断は人間が行う。
- 日本語headline等はCodex後描画。GPT画像内の日本語・LINE UI・ロゴは使用していない。

## 出力

- Contact sheet: `scene_contact_sheet.png`
- 個別静止画: `rendered_scenes/scene_001.png`〜`scene_018.png`
- GPT画像preflight: `work/production_preflight_phase2.md` のGPT image assets = PASS

## 停止

このファイルはdraft build前の静止画レビュー記録。人間レビューで承認後、`build_episode.py 003 --continue`を実行済み。

## Build後追記

- 人間レビュー: 承認（約75/100）
- draft: `output/draft_auto_v1.mp4`を生成
- build QA: `output/review/build_qa.md`（WARN 0 / FAIL 0）
- final化、thumbnail、YouTube操作: 未実施
