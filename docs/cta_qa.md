# CTA QA

共通CTAは`config/channel_cta.json`を正本とする。画面は`text.description`と`text.cta`から生成し、ナレーションは`narration_text`から生成する。

## `cta_full_text_visible`

`scripts/cta_preflight.py`で次を検査する。

- canonical本文の前半（説明文）と後半（CTA本文）が欠けずに描画される。
- missing suffix、clipping、crop、ellipsis、box overflowがない。
- テキストboxの全行が指定文字列を保持し、フォントは56px以上。
- CTA本文・パネル・説明文がEnd Screen reserved領域へ侵入しない。
- CTA画像は1920×1080である。

1文字でも欠けた場合はFAIL。フォントを小さくして押し込まず、意味の切れ目で改行し、左側のbox内で収める。
