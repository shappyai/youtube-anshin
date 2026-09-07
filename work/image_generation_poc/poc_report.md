# 画像生成フロー PoC レポート

確認日: 2026-08-31  
対象: Episode 005以降の画像生成運用の検証  
本番Episode 001〜004: 変更なし

## 判定

**SUCCESS**

今回の1回の依頼から、Codex内でSCENE-A、SCENE-B、SCENE-Cをそれぞれ独立した画像生成呼び出しとして順番に実行し、各scene 1枚を採用保存し、AI生成ではないcontact sheetまで自動作成できた。

## 操作・生成回数

- user interaction count: 1回（今回の依頼のみ）
- image generation call count: 3回
- 実行順: SCENE-A → SCENE-B → SCENE-C
- generator mode: ChatGPT/Codexの組み込み画像生成機能（built-in imagegen）
- API usage: none
- estimated additional API cost: 0
- ブラウザ自動操作・スクリーンスクレイピング: なし

各呼び出しは1scene分のプロンプトだけを渡した。3sceneを1回にまとめる呼び出し、候補画像を別sceneへ割り当てる処理、前sceneの画像やプロンプトの再利用は行っていない。

## Sceneごとの結果

### SCENE-A

- generation result: 明るい日本の家庭で、60〜70代の日本人女性が右側でスマートフォンを落ち着いて確認する1枚
- 人物・スマートフォンの位置: 右側中心
- 不安や恐怖の表現: なし
- generator returned candidates per call: 1
- adopted images count: 1
- output: `scene_a.png`

### SCENE-B

- generation result: 右側の抽象的な地球儀と、点線・弧でつながる1つの汎用的な受話器を描いた1枚
- 人物: なし
- 国名・国旗・電話番号・警察マーク・文字: なし
- generator returned candidates per call: 1
- adopted images count: 1
- output: `scene_b.png`

### SCENE-C

- generation result: 右側に汎用電話、虫眼鏡、緑のチェックマークを自然に配置した1枚
- 人物: なし
- 電話番号・読み取れる文字・UI・書類・警察バッジ: なし
- generator returned candidates per call: 1
- adopted images count: 1
- output: `scene_c.png`

## 保存結果

local save succeeded: **yes**

| scene | output path | valid image | width | height | aspect ratio | file size | SHA-256 |
|---|---|---:|---:|---:|---:|---:|---|
| A | `work/image_generation_poc/scene_a.png` | yes | 1672 | 941 | 1.776833 | 1,694,259 bytes | `482e98fc5ed768bed4750f4c44cd2200123911c3bbfa1a3083778f1c83086f23` |
| B | `work/image_generation_poc/scene_b.png` | yes | 1672 | 941 | 1.776833 | 1,811,981 bytes | `9a23bd527303c274d4866534f7cadd0a8428f50a6689a4aae4a52f4839fbcfd1` |
| C | `work/image_generation_poc/scene_c.png` | yes | 1672 | 941 | 1.776833 | 1,374,381 bytes | `4598d89065fc2cb6235474ca3a3d73098e9e9e639e03f96631f8e09032f7ad13` |

- adopted images count: 3（A/B/C各1枚）
- duplicate hash check: **no duplicate**（SHA-256のユニーク数 3/3）
- 1920×1080への正規化: 今回は実施せず。生成原本の1672×941をそのまま保存した
- 3sceneが別内容か: **yes**。Aはシニア女性、Bは地球儀と受話器、Cは電話・虫眼鏡・チェックマークで内容が分離している

## Contact sheet

- contact sheet result: **success**
- output: `work/image_generation_poc/contact_sheet.png`
- layout: A/B/Cを横3列
- scene label: 画像の上側にある別帯へローカル処理で描画
- contact sheet size: 1920×432
- contact sheet file size: 794,078 bytes
- contact sheet valid image: yes
- 作成方法: Codex/Pythonによる後処理。画像生成AIにはcontact sheetを作らせていない

## 手動介入

- 生成、採用保存、検証、contact sheet作成までにsceneごとの追加操作は不要だった
- 最終的な採用可否は、運用上はcontact sheetを人間が確認するゲートとして残す
- 今回のPoCでは、追加の人間操作を要求せず、確認用contact sheetを生成するところまで確認した

## Episode 005以降での実用性

この方式は、Episode 005以降の「1回の依頼 → sceneごとの独立生成 → 各scene 1枚保存 → contact sheetだけ人間確認」という運用に**実用化できそう**である。特に、3回の生成を順番に分離しても、ユーザー側の追加操作は発生しなかった。

残る課題:

1. 生成結果の内容確認と採用判断は、人間がcontact sheetで行う必要がある
2. 生成サイズが毎回1920×1080になる保証は今回確認していないため、本番では後段の正規化方針を決める
3. 生成失敗、保存失敗、既存ファイルがある場合のtimestamp付き出力先、再実行時の採用管理は本番設計で定義する
4. 実際のEpisode 005では、sceneごとのプロンプトを台本・shotlistから安全に分離する仕組みを別途検討する

## 結論

画像生成＋自動保存＋contact sheetまで成功。今回はPoCのみで、本番Episodeや本番自動化コードへの組み込みは行っていない。
