# Episode 015 Phase B Visual Gate v3

- Overall: **HUMAN_REVIEW_REQUIRED**
- Revision: v2 → v3、SCENE-004 / 007 / 010の実Google UI入口capture差し替え
- Human Gate: 2（full draftと実画面可読性の確認待ち）

| Gate | Status | Detail |
|---|---|---|
| actual Google UI entry capture | PASS | 3/3。Security / 2SV / backup code entry / passkey entryを確認 |
| AI reconstruction of Google UI | PASS | 公式UIの生成画像は使用していない |
| backup code secret protection | PASS | コード一覧・コード数字・QRを開かず、rawにも保存していない |
| PII / device-name protection | PASS | メール、電話番号、アカウント名、プロフィール画像、端末名一覧なし |
| rendered scenes | PASS | 3/3が1920×1080。source imageはすべてPCブラウザ入口capture |
| source labels | PASS | 各sceneに実画面の入口ラベルとSRCを設定 |
| senior readability | REVIEW | 元画像とdraftをHumanが65歳以上向けの大きさで確認 |
| scene quality mechanical gate | REVIEW | 9 OK / 0 WARN / 3 FAIL。gradient背景の差分比較不能による既知の判定 |

## 対象素材

| Scene | raw capture dimensions | rendered scene SHA-256 |
|---|---:|---|
| 004 | 513×145 | `818D66E4DF34233086DA123AF32159A9AEEC63AA572D38BBB849C6534C369E4E` |
| 007 | 502×82 | `B57C222F6285082C1AB12487D8B4037A8204FAC61EC96FC3E520E10338D64B44` |
| 010 | 513×61 | `A61A5A3F1C56936E4E3380AC76C81EFFBCB08D4912F454C0AF9197CF70853961` |

詳細: `work/visual_revision_v3.md`、`work/scene_quality_report_v3.md`、`work/draft_contact_sheet_v3.png`。
