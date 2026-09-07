# Visual Gate v1

ステータス：`PENDING_CONTACT_SHEET_AND_FULL_DRAFT_HUMAN_REVIEW`

## 機械・素材確認

- 必須scene：18
- ImageGen：2（SCENE-001 / SCENE-005）
- 公式visual：4（SCENE-002 / 003 / 010 / 015）
- template：12
- ちいかわ等のキャラクター artwork：0
- oversized_checkmark：0
- meaningless_filler_icon：0
- official UIをAI生成したscene：0
- 公式PDFの該当crop：4
- scene quality report：OK 17 / WARN 1 / FAIL 0
- draft_v1映像QA：PASS（黒画・尺差・音声ストリーム確認）

## ImageGen文字QA

- SCENE-001：retry 1回。指定2行と目視一致、文字の追加・欠落なし。採用画像は `assets/generated_ai/scene_001.png`。
- SCENE-005：画像内文字なし。後乗せ対象の落ち着いた背景、人物型キャラクター・ロゴ・実在UIなし。採用画像は `assets/generated_ai/scene_005.png`。

## 人間確認

- [ ] contact sheetでscene順・重複・余白・視線誘導を確認
- [ ] 公式資料の文字がTV視聴でも読めるか確認
- [ ] subtitle-safe bottom 180pxが守られているか確認
- [ ] SCENE-001 / 005の生成画像に権利上の類似キャラクターがないか確認
- [ ] 画面の主役が左へ偏りすぎていないか確認

## WARNメモ

- SCENE-002は公式資料cropの情報量が多く、機械検査でsmall-text proxy WARN。左側の要点文字は大きく配置済み。TV視聴での判読性は全編確認時に人間判定する。
