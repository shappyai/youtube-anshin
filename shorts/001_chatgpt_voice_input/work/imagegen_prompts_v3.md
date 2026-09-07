# Short001 ImageGen-native asset reuse record — Visual Redesign v3

- mode：built-in image_gen assets from v2を再利用
- new ImageGen call：0
- regeneration：0
- v3 major visuals：A / B / Cの3枚
- 共通制約：1080×1920へ正規化、人物・背景・generic smartphone・短い見出しを一体生成済み。公式ChatGPT UI、ロゴ、アカウント情報、履歴、個人情報は入れない。大見出しの後乗せは禁止。

## A / 冒頭

- asset：`assets/imagegen_native_v2/normalized/scene_01_hook.png`
- exact text：`ChatGPT` / `話すだけで使える？`
- reuse reason：冒頭フレームから日本人シニアとgeneric smartphone、問いが同時に見える。

## B / 行動

- asset：`assets/imagegen_native_v2/normalized/scene_04_life.png`
- exact text：`今日のごはん、` / `何を作れる？`
- reuse reason：冷蔵庫・卵・キャベツ・スマホで生活例が一枚で成立する。

## C / 結論

- asset：`assets/imagegen_native_v2/normalized/scene_06_summary.png`
- exact text：`まずは` / `話しかけるだけ`
- reuse reason：結論を強い人物Visualとして保持でき、最後のCTA字幕を同じ画面へ重ねられる。
