# Episode 010 Visual Gate

- status：PASS_WITH_HUMAN_REVIEW
- confirmation date：2026-09-05
- contact sheet：scene_contact_sheet_v1.png

## Machine checks

- scene render：20 / 20 PASS
- scene quality：FAIL 0、WARN 3
- blank_white_slide：0 scene
- subtitle safe area：20 / 20 PASSまたはUNCHANGED
- background consistency：20 / 20 PASSまたはUNCHANGED
- semantic icon alignment：PASS
- ImageGen exact-text auto QA：auto_fail 0

## Visual review

- [x] 20 sceneをcontact sheetで確認し、collage・storyboard・split panel・大きな白い空白半分を確認しなかった
- [x] template sceneにadult_digital_soft_image_bgを適用した
- [x] ImageGen scene 001・017・020は1920x1080 full-frameで保存した
- [x] scene 017は文字なしの動作概念で、公式UIの代替にしていない
- [x] 公式UI sceneはデジタル庁の原画または原画cropで、AI生成UIを使用していない
- [x] scene 009・011・013・015・016・018は読む箇所をfocus cropにして、元の小さなスマホ全体表示を避けた
- [x] CTA疑似登録アイコン、チャンネルロゴ、End Screen reserved領域の装飾は追加していない

## WARN interpretation

- scene 001：ImageGen native背景の小文字帯proxy。大見出しは視認でき、本文の正確な情報を置いていないため、TV縮小時の人間確認を残す。
- scene 013・015：公式focus crop以外の淡い領域が多いというラスタ警告。原画の白面を意図的に保持し、操作説明の主役をfocus cropにしている。

## Human gate remaining

1. 現在の公式画面と採用実機でボタン名・順番を照合する。
2. 採用端末でNFC読み取り位置を確認し、機種依存として説明する。
3. 公式画面と概念画像が視聴者に混同されないことを確認する。
4. ImageGen文字の完全一致、端の切れ、TV縮小時の可読性を確認する。
5. 画面全体が長すぎず、字幕帯が操作箇所を覆わないことを確認する。
