# Subtitle QA

字幕は画面表示の正本であり、VOICEVOXへ渡す発音用の読み仮名とは分離する。

## 必須検査

- 全文字幕であること。
- 発話の実時間に同期し、文字数按分でタイミングを決めないこと。
- フォントは56px未満にしない（標準は60〜72px）。
- 1 cueは最大2行。語中、助詞だけ、固有名詞、電話番号・URL・略語の途中で分割しない。
- segmentに`display_text`がある場合、連続する`subtitles.text_lines`を結合した表示文字列と完全一致すること。
- `reading_overrides`や`accent_overrides`の読み仮名が表示字幕へ流出していないこと（`tts_reading_leakage=0`）。

電話番号のように音声用表記と公式表示が異なる場合の例:

```json
{
  "spoken_text": "ゼロゴーナナゼロの、ゼロゴーゼロゴー、ハチハチ。",
  "display_text": "0570-050588"
}
```

`spoken_text`はVOICEVOXへ渡し、`display_text`は字幕へ表示する。数字の読みを字幕に表示しない。
