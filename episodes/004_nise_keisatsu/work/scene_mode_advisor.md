# Scene mode advisor

| Scene | Current | Recommended | Reason |
|---|---|---|---|
| SCENE-001 | gpt_image | gpt_image | 概念・注意・章扉を視覚中心で説明 |
| SCENE-002 | template | template | 一覧・比較・まとめはtemplate向き |
| SCENE-003 | gpt_image | gpt_image | 概念・注意・章扉を視覚中心で説明 |
| SCENE-004 | template | template | 一覧・比較・まとめはtemplate向き |
| SCENE-005 | template | gpt_image | 概念・注意・章扉を視覚中心で説明 |
| SCENE-006 | gpt_image | gpt_image | 概念・注意・章扉を視覚中心で説明 |
| SCENE-007 | template | template | 一覧・比較・まとめはtemplate向き |
| SCENE-008 | template | gpt_image | 概念・注意・章扉を視覚中心で説明 |
| SCENE-009 | gpt_image | gpt_image | 概念・注意・章扉を視覚中心で説明 |
| SCENE-010 | template | template | 一覧・比較・まとめはtemplate向き |
| SCENE-011 | template | gpt_image | 概念・注意・章扉を視覚中心で説明 |
| SCENE-012 | gpt_image | gpt_image | 概念・注意・章扉を視覚中心で説明 |
| SCENE-013 | official | hybrid | 見た目の主役が必要 / 公式素材を同時に提示 |
| SCENE-014 | template | template | 一覧・比較・まとめはtemplate向き |
| SCENE-015 | gpt_image | gpt_image | 概念・注意・章扉を視覚中心で説明 |
| SCENE-016 | template | gpt_image | 概念・注意・章扉を視覚中心で説明 |
| SCENE-017 | template | template | 公式性が必要だが素材未指定のため、捏造しないtemplateを使用 |
| SCENE-018 | gpt_image | gpt_image | 概念・注意・章扉を視覚中心で説明 |

## Count

- template: 6
- official: 0
- gpt_image: 11
- hybrid: 1

## 判断メモ（2026-08-31・Episode 004用）

advisorの推奨のうち、以下はあえて採用しない。理由は次のとおり。

- SCENE-005（手口の流れ）: 正確な犯行文言を文字で示す箇所のためtemplateを維持。GPT画像に正確な日本語を描かせない運用と整合。
- SCENE-008（末尾0110・75.5％）: 数字と事実の正確性が主役のためtemplateを維持。数字をGPTで描画しない。
- SCENE-011（番号偽装の注意）: 注意の文言が主役であり、`layout_06_caution` のtemplateに正確な文章を載せる方を優先。
- SCENE-013（国民生活センターの明言）: officialの公式発表ページを主役にする。hybridは背景と公式素材の合成が必要で、Phase Bの素材取得後に再検討する。
- SCENE-016（0120-210-364）: 実在の電話番号を正確に表示する必要があるためtemplateを維持。GPT画像に番号を生成させない。

最終のscene構成（episode.json反映済み）: template=10, official=1, gpt_image=7, hybrid=0。
