# Short002 ImageGen-native asset reuse record — Visual Redesign v3

- mode：built-in image_gen assets from v2を再利用
- new ImageGen call：0
- regeneration：0
- v3 major visuals：A / B / Cの3枚
- 共通制約：1080×1920へ正規化、人物・generic smartphone・短い見出しを一体生成済み。実在メール、企業ロゴ、URL、QR、個人情報、公式UI、精密な黒塗りUIは入れない。大見出しの後乗せは禁止。

## A / 冒頭

- asset：`assets/imagegen_native_v2/normalized/scene_01_hook.png`
- exact text：`このメール、` / `本物？`
- reuse reason：困った人物とgeneric smartphoneで、問いを最初のフレームから伝えられる。

## B / 行動

- asset：`assets/imagegen_native_v2/normalized/scene_02_mask.png`
- exact text：`個人情報は` / `まず隠す`
- reuse reason：個人情報を見せる前に隠す行動を、精密なUIなしで成立させられる。

## C / 結論

- asset：`assets/imagegen_native_v2/normalized/scene_05_official.png`
- exact text：`最後は` / `公式から確認`
- reuse reason：公式確認で落ち着く状況を人物Visualで示し、最後のCTAを同じ画面へ重ねられる。
