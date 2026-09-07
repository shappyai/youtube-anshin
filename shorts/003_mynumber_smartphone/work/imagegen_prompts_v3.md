# Short003 ImageGen-native asset reuse record — Visual Redesign v3

- mode：built-in image_gen assets from v2を再利用
- new ImageGen call：0
- regeneration：0
- v3 major visuals：A / B / Cの3枚
- 共通制約：1080×1920へ正規化、人物・generic smartphone・generic card・短い見出しを一体生成済み。カード番号、氏名、顔写真、政府ロゴ、正確なカードデザイン、公式UIは入れない。大見出しの後乗せは禁止。

## A / 冒頭

- asset：`assets/imagegen_native_v2/normalized/scene_01_hook.png`
- exact text：`カードを` / `スマホに？`
- reuse reason：generic cardとsmartphoneが最初のフレームから見え、問いを即時提示できる。

## B / 行動

- asset：`assets/imagegen_native_v2/normalized/scene_03_health.png`
- exact text：`保険証として` / `使える場合も`
- reuse reason：医療機関・薬局を想起する生活利用例を一枚で示せる。

## C / 結論

- asset：`assets/imagegen_native_v2/normalized/scene_05_conclusion.png`
- exact text：`スマホだけで` / `全部ではない`
- reuse reason：実物カードも必要という条件付き結論を、最後まで強いVisualで保持できる。
