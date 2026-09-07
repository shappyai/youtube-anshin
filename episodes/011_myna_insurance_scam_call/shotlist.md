# Episode 011 Shotlist / Visual Plan

実機撮影は行わない。Device欄は、公式情報や概念画を扱う媒体の選択を記録したもの。音声はVOICEVOXで生成済みで、全編の人間視聴待ち。

冒頭は、電話が鳴る → 「1番を押してください」と言われる → 本物か迷う → 押さずに止まる → 公式結論、のmicro story。視聴者自身を主人公とし、架空人物の体験談は置かない。

| Scene | Device / medium | Use | Main visual | Safety / human check |
|---:|---|---|---|---|
| 001 | ImageGen（非写実） | 冒頭の着信イメージ | スマホを前に止まる高齢者 | 実音声・実在UI・番号なし、文字2行の一致 |
| 002 | template | 架空の電話文言 | dialpad icon＋短い表示 | 「再現イメージ」「実在の電話音声ではありません」 |
| 003 | PCブラウザで公式本文確認 | 厚労省の公式結論 | 確認済み本文のquote crop | UIのAI再現なし、原文一致、本文を大きく読む |
| 004 | template | 3つの行動一覧 | rounded list | 3項目以外を増やさない |
| 005 | template | 1 / 3扉 | block icon | amberを補助に限定 |
| 006 | template | 番号を押さない | block icon＋行動 | 「押した瞬間に必ず被害」と言わない |
| 007 | template | 電話を終える | caution layout | 恐怖演出を避ける |
| 019 | template | 中盤CTA / 登録理由 | verified_user icon＋静かな2行 | 公式確認後に1回だけ。疑似subscribe UIなし、5〜7秒 |
| 008 | template | 2 / 3扉 | lock icon | 暗証番号を画面に入力しない |
| 009 | template | 伝えない情報 | 5項目list | 情報文字44px未満なし |
| 010 | template | 情報を渡さない・用語整理 | lock icon | アプリ利用登録と保険証利用登録を混同しない |
| 011 | template | 3 / 3扉 | verified_user icon | 公式確認の意味を明確にする |
| 012 | template | 公式から確認 | verified_user icon | 相手の番号・SMSリンクを使わない |
| 013 | PCブラウザでデジタル庁公式確認 | 0120-95-0178 | 電話番号と5番・受付時間 | 数字QA、公開前に受付時間再確認 |
| 014 | PCブラウザで警察庁公式確認 | #9110 | 警察相談専用電話 | 緊急番号と説明しない |
| 015 | PCブラウザで警察庁公式確認 | 110と#9110の使い分け | warning icon＋用途 | 緊急時110、通常相談#9110 |
| 016 | template | すでに答えた場合 | 2カラム比較 | 押しただけと情報を伝えた場合を分ける |
| 017 | template | まとめ | 3行summary | 本編の3項目と一致 |
| 018 | ImageGen（非写実） | CTA前の安心感 | スマホを伏せて確認を選ぶ場面 | 右40〜45%をEnd Screen reserved、疑似登録要素なし |

## Background and layout

- Template：`config/visual_theme.json` の `adult_digital_soft_image_bg`
- Background：`assets/backgrounds/adult_digital_soft_v2.png` をcover＋LANCZOS、縦横比維持
- 下部180px：字幕安全領域。`captions.srt` / `captions.ass` はVOICEVOX実測タイムラインで生成済み。scene layoutは侵入させない
- ImageGen：1scene=1image、1920×1080へ正規化、collage・storyboard・split panel・fake official UI禁止
- Semantic icons：Material Symbols Rounded。rendererでalpha bbox trimとvisual center normalizationを適用
