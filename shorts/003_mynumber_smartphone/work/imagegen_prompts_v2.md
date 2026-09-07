# Short003 ImageGen-native prompt set v2

- 生成方式：built-in `image_gen`
- Use case：`photorealistic-natural`
- 共通指定：縦9:16、人物・背景・主要オブジェクト・短い見出しを一体生成。日本人シニア、自然な生活場面、スマホ表示時に読める濃紺の大見出し。カードは無地のgeneric cardとし、個人番号、氏名、顔写真、政府マーク、ロゴ、QR、公式UI、読める追加文字、透かし、collage、split panel、presentation slideを入れない。見出しは画面左上〜上中段、人物・重要物・右端Shorts UI・下20%と重ねない。

## Scene 01 — hook

人物：60代後半の日本人。generic smartphoneと完全に無地のgeneric cardを見比べ、「スマホに？」と考える。表情は好奇心程度で、カードへ公式デザインを入れない。

画像内の正確な文字（2行）：

```text
カードを
スマホに？
```

## Scene 03 — conditional health-insurance example

人物：60代後半の日本人。generic smartphoneと無地のgeneric cardを持ち、病院または薬局らしい明るい受付を背景にする。看板、ロゴ、施設名は描かず、「場合も」の条件を崩さない。

画像内の正確な文字（2行）：

```text
保険証として
使える場合も
```

## Scene 05 — conclusion

人物：65〜70歳程度の日本人。家庭の机でgeneric smartphoneと無地のgeneric cardを並べ、両方が必要になり得ることに納得する。カードは無地で、政府・個人情報・公式UIを入れない。

画像内の正確な文字（2行）：

```text
スマホだけで
全部ではない
```

