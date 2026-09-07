# Short003 visual plan — Visual Redesign v2

## 共通

- canvas：1080×1920、30fps、縦
- target_duration：30秒（Draft v2実測27.34秒）
- draft_v2：output/draft_v2.mp4
- audio：既存VOICEVOX segment WAVを再利用。Visual変更のため全音声は再生成しない
- viewer_facing_short_id：0。動画フレームにShort003やチャンネル名を表示しない
- visual_rule：ImageGen-native画像は人物・背景・主要見出しの完成画。大見出しの後乗せは禁止。公式UI、政府ロゴ、正確なカードデザイン、個人情報は使わない

## Scene / segment plan

| Segment | Scene | 時間目安 | render_mode | 内容・asset | 画面の主役 |
|---:|---:|---:|---|---|---|
| 01 | 01 | 0〜3秒 | imagegen_native | `assets/imagegen_native_v2/normalized/scene_01_hook.png` | シニア＋generic smartphone＋無地generic card＋「カードを / スマホに？」 |
| 02 | 02 | 3〜11秒 | renderer_native | 3つの利用例を時間に沿って表示 | マイナポータル・証明書・e-Tax |
| 03 | 03 | 11〜16秒 | imagegen_native | `assets/imagegen_native_v2/normalized/scene_03_health.png` | generic card＋病院・薬局の雰囲気＋「保険証として / 使える場合も」 |
| 04 | 04 | 16〜22秒 | renderer_native | iPhone / Androidのgeneric phone比較 | 端末差があること |
| 05 cue 1 | 05 | 22秒以降 | renderer_native | generic card semantic visual | 実物カードが必要な場面も |
| 05 cue 2 | 05 | 22秒以降 | imagegen_native | `assets/imagegen_native_v2/normalized/scene_05_conclusion.png` | smartphone＋無地generic card＋「スマホだけで / 全部ではない」 |
| 06 | 06 | まとめ後 | renderer_native | 共通CTA。疑似登録・チャンネルアイコンなし | CTAだけを表示 |

## ImageGen文字QA

- `imagegen_native`：3scene
- 指定文言一致：3/3 PASS
- 誤字・脱字・余計な文字・文字切れ：0
- 再生成：0回
- generated imageへの大見出し後乗せ：0（NO_IMAGE_TEXT_HYBRID）
- 個人番号、氏名、顔写真、政府ロゴ、正確なカードデザイン、公式UI：0
- 元画像はrootのassetに保持し、`normalized/`を動画とサムネイル候補へ使用する

## CTA / thumbnail

- CTAは共通renderer。spokenは`shorts/common_cta.md`の共通版を再利用
- CTAにsubscribe icon、チャンネルアイコン、Short003 IDを描画しない
- `assets/thumbnail_candidate/first_frame_thumbnail_candidate.png`は冒頭ImageGen-native画像の正規化copy。thumbnail確定は未実施
