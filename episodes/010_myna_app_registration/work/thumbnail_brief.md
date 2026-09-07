# Episode 010 Thumbnail Brief

- status：**ChatGPT生成原本を受領・人間選択済み / 公開用QA PASS**
- updated：2026-09-06
- source_origin：ユーザー指定のChatGPT生成画像。Codex/ImageGenによる再生成はしていない。
- selected title：【マイナアプリ】登録方法は？初めて使う人が確認したい手順
- audience：50〜70代、特に65歳以上。TV表示でも一瞬で読める大きさを優先する。
- role：初めて使う人向けの利用登録動画だと、タイトルを読まなくても伝える。

## Adopted copy

- 上段：`マイナアプリ`
- 主見出し：`最初に` / `何する？`
- 補助：`初めて使う人向け` / `やさしく解説`
- 右側：スマートフォンを持って考える高齢男性
- 左〜中央：マイナアプリと実物カードを連想する説明用ビジュアル

## Visual direction

- 一般的なスマートフォンと実物カードを連想する説明用構図。公式UIや公式サムネイルではない。
- 公式UI、政府マーク、実在個人情報、QRコード、暗証番号そのものは扱わない。受領原本に含まれるカード風イラストは説明用として使用する。
- 背景はチャンネルの淡い安心感を維持し、警告色・恐怖表情・緊急バッジを主役にしない。
- 文字は大見出し1〜2行、2〜6語相当。タイトル全文を繰り返さない。

## Acceptance criteria

- `thumbnail_source.png` は受領原本、`thumbnail.png` は公開用正規化画像として保存する。
- `thumbnail.png` はPNGまたはJPEG、1280×720、16:9、2MB以内。
- 文字の完全一致、端の切れ、TV縮小時の可読性、Fact Boundary、privacyを人間確認する。
- 疑似登録ボタン、チャンネルアイコン、End Screen要素は描かない。実登録要素はYouTube Studio側で配置する。
- 公開用正規化：原本の上下1px相当の比率調整と1280×720への縮小のみ。文字・人物・UI・構図は変更しない。

受領原本は `assets/thumbnail/thumbnail_source.png`、公開用は `assets/thumbnail/thumbnail.png`。画像QAは `work/thumbnail_review/thumbnail_qa.json` に記録する。
