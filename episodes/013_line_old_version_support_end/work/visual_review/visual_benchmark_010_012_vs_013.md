# Episode 013 Visual benchmark — Episode 010〜012との比較

確認日：2026-09-06  
対象：Episode 010 / 011 / 012 の承認済み接触シートと、Episode 013 Visual Gate v1.1接触シート  
参照：

- `episodes/010_myna_app_registration/work/visual_review/scene_contact_sheet_v2.png`
- `episodes/011_myna_insurance_scam_call/work/visual_review/draft_v2_contact_sheet.png`
- `episodes/012_phishing_message_safety/work/visual_review/scene_contact_sheet_v2.png`
- `episodes/013_line_old_version_support_end/work/visual_review/scene_contact_sheet_phase_b_template_v1_1.png`

## 採点方法

5点満点。正の指標は5点が良い。`template repetition`、`card density`、`large blank area`、`corporate slide feeling` は問題の強さで、1点が良く、5点が悪い。

| 指標 | 010 | 011 | 012 | 013 v1.1 | 判定の読み方 |
|---|---:|---:|---:|---:|---|
| visual variety | 4 | 4 | 5 | 1 | 人物・公式画面・図解・まとめの切替 |
| photographic / human scene ratio | 4 | 4 | 4 | 1 | 人物や生活場面が視聴の入口になる割合 |
| template repetition | 2 | 2 | 2 | 5 | 同じ背景・同じ構図の連続度（低いほど良い） |
| whitespace quality | 4 | 4 | 4 | 2 | 余白が読みやすさと主役のために機能しているか |
| hierarchy | 4 | 4 | 4 | 3 | 見出し・主情報・補足の優先順位 |
| card density | 2 | 2 | 2 | 4 | カードが多く説明資料に見える強さ（低いほど良い） |
| large blank area | 2 | 2 | 1 | 4 | 主役のない大きな空白の強さ（低いほど良い） |
| optical balance | 4 | 4 | 4 | 3 | 文字・人物・画面の重心と左右余白 |
| scene-to-scene change | 4 | 4 | 5 | 1 | 隣り合うsceneで視覚的に次の場面へ進む感覚 |
| senior readability | 4 | 4 | 4 | 4 | 50〜70代が大画面で主要情報を読めるか |
| YouTube-like visual quality | 4 | 4 | 5 | 2 | 放送・動画としての場面性とサムネイル縮小時の強さ |
| corporate slide feeling | 2 | 2 | 1 | 5 | PowerPoint／社内資料に見える強さ（低いほど良い） |

## 013 v1.1が明らかに弱く見える理由

1. **人物・生活場面がない**：冒頭の不安、確認する人、更新を判断する瞬間をすべてカードと記号で説明している。010〜012は最初と節目に人物や場面画像があり、視聴者が自分の状況に接続できる。
2. **同じ構図が長く続く**：section pill、中央見出し、淡いカード、下部の字幕帯が24sceneの大半で反復される。情報が正しくても、場面が進んでいないように見える。
3. **ケースA〜Dが結果ではなく表に見える**：4つの判断結果が同じsummary/list型に並び、視聴者の「自分はどこか」を探す分岐になっていない。
4. **数字の主役化が足りない**：14.6.3、14.4.6、15.0、8.0がカード内の小さな本文に埋もれ、今回確認する下限なのか、最新版推奨環境なのかの階層も弱い。
5. **実機sceneが未取得のまま同じ仮枠に見える**：CAPTURE_REQUIREDは正しいが、現行レイアウトでは8sceneが同じ中サイズの中立画面に見える。最終配置は今の段階で「実機画面が主役になる枠」として設計し直す必要がある。
6. **ベージュの連続で注意場面が常態化する**：警告・困ったときだけに使うべきamberが全体のベースに見え、安心して確認する番組の青・白・淡いgreenのリズムが失われている。

## 再設計で再利用する010〜012の長所

- 1scene 1 message。説明をカードに詰めず、見出し・数字・操作箇所のどれかを主役にする。
- Human / situation → clean explainer → real UI を交互に置く。人物sceneは不安を受け止める入口と、判断前の橋渡しに限定する。
- 正確な操作は実機・公式画面だけで示し、ImageGenには読めないスマホ画面や概念的な端末を使わせる。
- 青・白・淡いgreenを通常色にし、amberは「更新できない」「注意が必要」な分岐に限定する。
- 数字sceneでは数字をカードの本文に埋めず、画面の中心軸に大きく置く。

## Human gateで必ず問うこと

> Episode010〜012と並べたとき、Episode013だけが明らかに安っぽく見えないか？

Visual variety、story feel、senior readability、optical balanceを各4点以上、template repetitionとcorporate slide feelingを各2点以下として確認する。実機8sceneは、現時点では最終素材ではなくCAPTURE_REQUIREDのレイアウト確認として扱う。
