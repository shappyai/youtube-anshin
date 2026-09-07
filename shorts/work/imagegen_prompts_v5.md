# Shorts探索バッチ001 ImageGen prompts v5

確認日：2026-09-07（JST）

v5で新規生成したのはShort003の2sceneだけ。各sceneは1枚の完成した縦長画像として生成し、文字なしで採用した。公式UI、政府マーク、企業ロゴ、QRコード、バーコード、実在サービスの画面は生成していない。

## Short003 / convenience_certificate.png

```text
Create one photorealistic, natural full-frame vertical 9:16 lifestyle image for a Japanese explainer video. An older Japanese woman is standing at a generic convenience store multifunction copier, calmly handling a blank certificate-like sheet of paper. Show the woman, copier, and paper clearly with a warm, trustworthy everyday atmosphere. The paper must remain blank and unreadable. No words, no letters, no numerals, no logos, no brand marks, no QR codes, no barcodes, no government symbols, no real app interface, no fake official screen, no watermark. Single scene only, no collage, no split panel, no storyboard, no contact sheet. Text (verbatim): none.
```

採用先：`shorts/003_mynumber_smartphone/assets/imagegen_native_v5/normalized/convenience_certificate.png`

## Short003 / etax_home.png

```text
Create one photorealistic, natural full-frame vertical 9:16 lifestyle image for a Japanese explainer video. An older Japanese man is at home using a laptop with blank papers and a smartphone nearby, calmly preparing an online tax-related task. Make the everyday action immediately understandable without showing any readable interface. Laptop and papers must contain no readable text. No words, no letters, no numerals, no logos, no brand marks, no QR codes, no barcodes, no government symbols, no real app interface, no fake official screen, no watermark. Single scene only, no collage, no split panel, no storyboard, no contact sheet. Text (verbatim): none.
```

採用先：`shorts/003_mynumber_smartphone/assets/imagegen_native_v5/normalized/etax_home.png`

## QA記録

- 新規ImageGen call：2
- 再生成：0
- exact text QA：`PASS_NO_TEXT`
- visual QA：親Codexが生成結果を目視確認済み。文字・ロゴ・公式UI・コラージュなし。
- 既存v2 ImageGen-native完成画は再利用し、再生成していない。
- `NO_IMAGE_TEXT_HYBRID`：PASS。生成画像へ大見出しや説明カードを後乗せしていない。
