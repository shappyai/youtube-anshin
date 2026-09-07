# Episode 008 thumbnail QA

確認日: 2026-09-05

## 採用方針

- ユーザー提供画像を正式採用。
- imagegen_nativeによる再生成、別案、A/B/C候補は作成していない。
- 原本を `assets/thumbnail/thumbnail_source.png` として保持。
- 正式配置は `assets/thumbnail/thumbnail.png`。1672×941の原本を、内容を変えず1280×720へ正規化した。

## QA結果

| 項目 | 結果 |
|---|---|
| aspect ratio | PASS（1280×720、16:9） |
| decode | PASS |
| text typo | PASS（「その投資広告」「本物？」「LINEに誘導されたら」「注意」） |
| text clipping / edge clipping | PASS |
| 25% readability | PASS（320×180で大見出し2箇所を確認） |
| real celebrity | 0 |
| personal information / account number | 0 |
| QR code | 0 |
| LINE context | PASS（投資広告からLINEへ誘導されたら注意） |

## 内容確認

青系背景、黄色の「本物？」、スマホ、架空の投資広告イメージ、心配そうなシニア男性、下部の「LINEに誘導されたら 注意」を維持している。スマホ内の人物は generic silhouette で、実在著名人の写真・氏名はない。

## ハッシュ

- 原本: `8759ba8a8d7f4534d66c3227bd84164236ae4764648103afd7bfb2627b4100f2`
- 正式thumbnail: `f73ffff3b74414fe921104ac1e89605ee9ba3cb643c818130cdeb8010d3d923e`
- 25%版: `2dd5d0af00848bf1485c4ce32dd37e5411abf0771dbc5842042ea253c3f2a1e2`
