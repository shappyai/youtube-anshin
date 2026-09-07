# Episode 010 Privacy QA

- status：PASS（Phase A素材確認）
- confirmation date：2026-09-05
- scope：ImageGen raw・正規化画像・公式原画・公式crop・20 scene render・contact sheet

## Checks

- [x] 氏名・住所・電話番号・メールアドレスがない
- [x] 生年月日・顔写真・マイナンバー・カード番号・製造番号がない
- [x] 実データの暗証番号・QRコード・通知内の個人情報がない
- [x] scene 017は一般化したカード概念で、公式カードの再現や個人情報を含まない
- [x] ImageGen sceneは政府マーク・アプリロゴ・実在の設定画面を生成していない
- [x] 公式原画はAI生成ではなく、公式素材をそのまま使用している
- [x] scene renderとcontact sheetに、上記の禁止情報が追加されていない

公式画面内の入力欄、番号の例示、カード illustration は、操作説明用の一般化された表示として扱う。実機撮影に切り替える場合は、テスト端末・テストカードを使い、raw素材を再確認する。

## Human gate remaining

公開前に、採用する実機・カード・通知設定画面を人間が再確認する。個人情報が1つでも入る場合は、その素材を採用せず差し替える。
