# Episode 011 Thumbnail QA

確認日：2026-09-06  
判定：**PASS**

## 採用画像

- 原本：`assets/thumbnail/thumbnail_source.png`
- 公開用：`assets/thumbnail/thumbnail.png`
- 原本はユーザー提供画像。Codexによる新規生成・文言変更・人物や構図の変更は行っていない。
- 公開用画像は原本をLANCZOSで1280×720へリサイズし、PNGメタデータを持たないRGB画像として保存。

## 機械確認

| 項目 | 結果 |
|---|---|
| 公開用サイズ | 1280×720 |
| ファイル形式 | PNG |
| ファイルサイズ | 1,129,358 bytes（2MiB以下） |
| 破損 | 0 |
| 文字の欠落・切れ | 0 |
| 顔の欠落・遮蔽 | 0 |
| ウォーターマーク | 0 |
| 視聴者向けEpisode内部ID | 0 |

## 人間相当の縮小確認

`work/thumbnail_review/thumbnail_25.png`（320×180）を確認し、マイナ保険証、「1番を押して」、その電話、本物？、まず確認する3つの主要メッセージを判読できることを確認した。主要人物の顔、電話、マイナンバーカードの図解に不自然な欠落はない。

## SHA-256

- 原本：`3856F3FF36EBEF575B712E5DD5B5648773B77BDE215052E6F4E910A3F9739F96`
- 公開用：`A918228AFCCCB45EF3DE51832CC94781302B83C38B811083586A6B842C642830`

機械可読記録：`work/thumbnail_review/thumbnail_qa.json`
