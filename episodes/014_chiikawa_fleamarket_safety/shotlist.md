# Episode 014 shotlist

| Scene | Segment | Device / medium | Visual | Asset / source | Animation | Checks |
|---|---:|---|---|---|---|---|
| SCENE-001 | 1 | ImageGen静止画 | 架空の高齢女性、スマホ、無地の箱・幾何学的なアクリル台 | `assets/generated_ai/scene_001.png`、ImageGen native | very slow zoom | 文字2行の完全一致、人物型キャラクター0、下部180px安全 |
| SCENE-002 | 2–3 | PCブラウザで公式PDF確認 | くら寿司9月2日公式発表の該当crop＋要点 | `official_kurasushi_sns_20260902.png` / SRC-002 | static | SNS投稿を受けた調査を維持、出典44px以上 |
| SCENE-003 | 4–5 | PCブラウザで公式PDF確認 | くら寿司9月5日公式発表の該当crop＋要点 | `official_kurasushi_cancel_20260905_v2.png` / SRC-001 | static | 従業員不正行為と9月6日中止を公式範囲で表示 |
| SCENE-004 | 6–7 | テンプレート図解 | 公式・報道・推測を分ける | 共有背景＋semantic icon `verified_user` | static | 出品者・商品の同一性を断定しない |
| SCENE-005 | 8 | ImageGen-native完成画 | 明示的な架空例。高齢者、スマホ、無地の箱。画像内に「残り1個／どうする？」 | `assets/generated_ai/scene_005.png`、ImageGen native | very slow zoom | 指定文字の完全一致、後付け大見出し0、キャラクター・ロゴ・UI0 |
| SCENE-006 | 9 | テンプレート一覧 | 販売時期／商品／アプリ内／評価／運営・188 | 共有背景、5項目リスト | static | 文字44px未満なし |
| SCENE-007 | 10 | テンプレート章扉 | 1 / 5 販売・配布の時期 | 共有背景＋`campaign` | static | 章番号・見出しを大きく |
| SCENE-008 | 11–14 | テンプレート図解 | 時期が合わない出品は確認する | 共有背景＋`campaign` | static | 「違法・盗品」と断定しない |
| SCENE-009 | 15 | テンプレート章扉 | 2 / 5 商品をよく確認 | 共有背景＋`verified_user` | static | 一般的な注意として提示 |
| SCENE-010 | 16 | PCブラウザで公式PDF確認 | 国民生活センター偽物注意喚起crop | `official_kokusen_fake_20250902.png` / SRC-004 | static | ちいかわ商品全般への一般化なし |
| SCENE-011 | 17–19 | テンプレート図解 | 購入前の質問ポイント | 共有背景＋`verified_user` | static | 実物・状態・付属品・入手経路 |
| SCENE-012 | 20 | テンプレート章扉 | 3 / 5 アプリの外へ出ない | 共有背景＋`forum` | static | LINE・銀行振込・別サイトを例示 |
| SCENE-013 | 21–24 | 左右比較テンプレート | アプリ内の決済・連絡／外部誘導 | 共有背景＋`payments` | static | 特定アプリUIを再現しない |
| SCENE-014 | 25 | テンプレート章扉 | 4 / 5 届く前に評価しない | 共有背景＋`verified_user` | static | 受取前評価を勧めない |
| SCENE-015 | 26–28 | PCブラウザで公式PDF確認 | 国民生活センター受取評価事例crop | `official_kokusen_receipt_20260305.png` / SRC-005/006 | static | 受け取る→確認→評価を大きく表示 |
| SCENE-016 | 29 | テンプレート章扉 | 5 / 5 困ったら運営・188 | 共有背景＋`support_agent` | static | 相談導線を穏やかに表示 |
| SCENE-017 | 30–33 | テンプレート注意・相談 | 取引相手→運営→188 | 共有背景＋`support_agent` | static | 実在電話番号以外の個人情報なし |
| SCENE-018 | 34–38 | テンプレートまとめ | 3行のまとめ。確認できなければ見送る | 共有背景、3項目リスト | static | 終了CTAはpostrollのみ |

## 画面媒体の決定

Web上の公式発表・公的資料はPCブラウザで確認し、PDFの該当箇所を大きくcropする。フリマの個別UIは撮影せず、一般化したテンプレート図解にする。ImageGenは概念・架空例のみで、公式UIやキャラクターを生成しない。
