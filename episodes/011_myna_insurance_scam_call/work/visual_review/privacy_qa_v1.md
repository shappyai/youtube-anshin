# Episode 011 Privacy QA v1

確認日：2026-09-06

| check | result | evidence |
|---|---|---|
| 実在の詐欺電話音声を使っていない | PASS | 音声はPhase B未生成。SCENE-002は「再現イメージ」「実在の電話音声ではありません」と表示。 |
| AIで実在の詐欺音声を再現していない | PASS | ImageGenは非写実的な概念画2sceneのみ。音声生成なし。 |
| 実在の相手先電話番号を詐欺演出に使っていない | PASS | 架空の電話文言sceneに番号なし。0120-95-0178は公式相談先として後半にのみ表示。 |
| 偽の厚労省ロゴ・政府マークを使っていない | PASS | 公式引用は確認済み本文のquote crop。ロゴ・政府UIの描き直しなし。 |
| 公式UIをAI生成していない | PASS | SCENE-001/018は非写実的概念画。SCENE-003は公式本文の正確な引用画像。 |
| 個人情報・マイナンバー・暗証番号・カード番号を素材に含めていない | PASS | template/AI/official assetを目視確認。実データなし。 |
| 疑似subscribe button・チャンネルアイコンを描画していない | PASS | SCENE-019とSCENE-018を確認。登録要素はYouTube Studio側に残す。 |
| End Screen reserved領域を侵食していない | PASS | SCENE-018右40〜45%を空け、SCENE-019はEnd Screen前の中盤scene。 |

## 集計

- Privacy FAIL：0
- PII leak：0
- fake official UI/logo：0
- real scam audio：0
- fake subscribe UI：0
