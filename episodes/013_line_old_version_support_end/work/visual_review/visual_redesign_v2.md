# Episode013 Visual Redesign v2

status: `APPROVED_HUMAN_VISUAL_GATE`
approved_at: `2026-09-06`
contact_sheet: `work/visual_review/scene_contact_sheet_visual_redesign_v2.png`
benchmark: `work/visual_review/visual_benchmark_010_012_vs_013.md`

## 1. 旧版が弱く見えた原因

- 24sceneの大半が、淡いカード・中央見出し・同じ余白の組み合わせだった。
- 人物や生活場面がなく、実機画面も未配置だったため、視聴のリズムが「説明資料の連続」になった。
- CASE A〜Dが同じ表に見え、条件から次の行動へ進む流れが弱かった。
- 数字は読める一方、画面全体の重心と場面転換が単調で、Episode010〜012よりYouTube向けの完成感が低かった。

## 2. Episode010〜012から再利用した原則

- 人物・生活状況、整理図、公式画面、要点カードを交互に置く。
- 1scene 1メッセージにして、画面全体を長く読ませない。
- 数字・OS・更新順は大きく出し、条件の細部はナレーションへ分担する。
- 実機でしか成立しない説明は、実機キャプチャを大きく置く枠として先に設計する。
- 白一色を避け、共通Background Systemの淡い青・緑を基調にする。注意・ケースDだけ淡いamberを使う。
- CASE A〜Dは表ではなく「状況 → 次にすること」の分岐にする。

## 3. 構成数

| 役割 | scene | 数 | 状態 |
|---|---|---:|---|
| ImageGen-native | 001, 004, 008, 012, 022 | 5 | 1920×1080正規化済み・採用候補 |
| renderer native | 002, 003, 007, 011, 017〜021, 023, 024 | 11 | レンダー済み |
| real UI capture slot | 005, 006, 009, 010, 013〜016 | 8 | `CAPTURE_PENDING`。実機未配置 |

実機8sceneは、視聴者向け画面に`CAPTURE_PENDING`を表示せず、差し替え後に実画面が主役になる大きな枠だけを用意した。架空の設定画面・偽UI・AI生成の公式画面は使用していない。

## 4. レイアウトファミリーと反復上限

| レイアウトファミリー | scene | 最大連続 | 役割 |
|---|---|---:|---|
| imagegen_native | 001, 004, 008, 012, 022 | 1 | 人物＋生活状況＋短い見出し |
| opening_list | 002 | 1 | 今日確認する3つ |
| threshold_focus | 003, 007, 011 | 1 | 閾値・基準を数字中心で提示 |
| capture_focus | 005〜006, 009〜010, 013〜014 | 2 | LINE／OSの実機枠 |
| capture_focus_tall | 015〜016 | 2 | OS更新の縦長実機枠 |
| flow_focus | 017 | 1 | LINE → OS → LINE |
| case_result | 018〜021 | 4* | CASE A〜Dの分岐結果 |
| bridge_clean / summary_three | 023 / 024 | 1 | 機種変更前の案内／まとめ |

通常の同一レイアウト連続は最大2scene。CASE A〜Dの4連続だけは、ユーザー指定の分岐説明の例外として残し、green・blue・teal・amberの色、アイコン、条件、次の行動を変えている。人間Visual Gateでこの例外が「同じ表の連続」に見えないことを確認済み。

## 5. ImageGen-native QA

- 対象: SCENE-001 / 004 / 008 / 012 / 022
- 自動QA: 5/5配置、5/5サイズ・アスペクト比、`auto_fail=0`
- 目視相当レビュー: 指定見出し・補助文の一致、誤字・脱字・余計な文字なし、文字切れなし、人物との重なりなし、公式UI・ロゴなしを確認。
- SCENE-004とSCENE-022は初回生成で下部字幕安全帯へ文字が寄ったため、指定どおり各1回だけ再生成。2回目を採用した。
- 再生成回数: 2。3回目の生成・別sceneへの流用・renderer上の大見出し後乗せは行っていない。
- 自動のsafe-area検査はSCENE-008 / 012 / 022で背景の人物・机・床を検出したが、下部180pxに生成文字はない。背景画像の内容を消す加工は行わず、字幕帯は動画レンダー側で管理する。

詳細な機械レポート: `work/visual_review/text_qa_visual_redesign_v2.md` / `text_qa_visual_redesign_v2.json`

## 6. 視覚レビュー評価

人間Visual Gate承認時の評価。5点満点、反復・PowerPoint感だけは低いほど良い。

| 項目 | 評価 | 根拠 |
|---|---:|---|
| scene variety | 4/5 | 人物→数字→実機枠→流れ→分岐→まとめの切り替えがある |
| story / rhythm | 4/5 | 3つの確認項目とCASE A〜Dの結果が画面の役割として分かれる |
| senior readability | 4/5 | 閾値、OS基準、流れ、次の行動を大きく表示 |
| optical balance | 4/5 | ImageGenは左右非対称、rendererは数字・実機枠の重心を確保 |
| template repetition | 2/5 | 通常の同一layoutは最大2連続 |
| corporate PowerPoint feel | 2/5 | 人物sceneと状況分岐を追加。CASE A〜Dも同じ表の連続には見えない |
| YouTube finish | 4/5 | 010〜012と同じく、説明だけでなく場面転換を持たせた |

機械的なscene quality reportは24/24 OK、WARN 0、FAIL 0。subtitle safe area、背景一貫性、blank white slide、overflow、tiny text、decorative checkmarkはいずれも問題なし。実機8sceneの左右重心も8/8 PASS。

## 7. 変更範囲と未実施事項

- 変更: Episode013のvisual metadata、rendererのvisual variant、ImageGen-nativeのv2 asset、Visual Gate記録、接触シート。
- 未変更: `script.md`、VOICEVOX音声、字幕、facts、sources、CTA、実機録画、draft、final、thumbnail、publish、upload、schedule。
- draft / finalは、実機8sceneが未配置のため生成していない。

## 8. Human Visual Gate（APPROVED）

確認対象: `scene_contact_sheet_visual_redesign_v2.png`

Episode010〜012と並べて、次を人間が確認する。

1. Episode013だけ明らかに安っぽく見えないか。
2. CASE A〜Dが同じ表の繰り返しではなく、状況→次の行動として読めるか。
3. 実機8sceneの差し替え後も、実画面が小さくならず、字幕帯を覆わないか。
4. ImageGen-native 5sceneの文字が視聴サイズで読めるか。

判定: **APPROVED**。Episode010〜012と比較して明らかな品質低下なし。Visual Redesign v2をEpisode013のcanonical visualとして採用する。実機8scene取得前のため、draft/finalへは進めない。
