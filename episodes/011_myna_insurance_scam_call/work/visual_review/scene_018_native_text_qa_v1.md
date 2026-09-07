# SCENE-018 ImageGen-native text QA

確認日：2026-09-06

## 判定

`PASS`

- background_text_single_generation：PASS。背景・人物・スマートフォン・日本語文字を1枚のImageGen出力で生成
- imagegen_native：PASS
- post_text_overlay：0。PIL、ffmpeg drawtext、別文字layer、subtitle以外のheadlineなし
- ImageGen生成回数：2回（最終契約へ合わせた再生成1回）
- pil_overlay fallback：0
- exact text：PASS
- other readable text：0
- TV readability：PASS。主文を大きく、補助文をその下へ配置
- subtitle safe area：PASS。下部180pxに文字なし
- right reserved area：PASS。右40〜45%に文字なし

## 採用した文字

主文：

`迷ったら、`

`その場で決めない`

補助文：

`いったん止まって、`

`公式から確認`

上記以外の文字・ロゴ・番号・UI・ウォーターマークは確認されなかった。

## Asset

- raw：`work/imagegen_raw/scene_018_v2_native_source.png`
- normalized：`assets/generated_ai/scene_018.png`（1920×1080）
- 旧方式の背景は`work/archive/scene_018_pre_native.png`へ保持
