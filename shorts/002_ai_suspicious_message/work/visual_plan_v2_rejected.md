# Short002 visual plan — Visual Redesign v2

## 共通

- canvas：1080×1920、30fps、縦
- target_duration：30秒（Draft v2実測30.98秒）
- draft_v2：output/draft_v2.mp4
- audio：既存VOICEVOX segment WAVを再利用。Visual変更のため全音声は再生成しない
- viewer_facing_short_id：0。動画フレームにShort002やチャンネル名を表示しない
- visual_rule：ImageGen-native画像は人物・背景・主要見出しの完成画。大見出しの後乗せは禁止。実在メール・ロゴ・URL・QR・個人情報・公式UIは使わない

## Scene / segment plan

| Segment | Scene | 時間目安 | render_mode | 内容・asset | 画面の主役 |
|---:|---:|---:|---|---|---|
| 01 | 01 | 0〜3.2秒 | imagegen_native | `assets/imagegen_native_v2/normalized/scene_01_hook.png` | シニア＋generic smartphone＋「このメール、 / 本物？」 |
| 02 | 02 | 3.2〜7.2秒 | imagegen_native | `assets/imagegen_native_v2/normalized/scene_02_mask.png` | 個人情報を覆う手＋「個人情報は / まず隠す」 |
| 03 | 03 | 7.2〜12.5秒 | renderer_native | assistant semantic visual | AIは整理・洗い出しの補助 |
| 04 | 04 | 12.5〜17秒 | renderer_native | warning semantic visual | AIだけで決めない |
| 05 | 05 | 17〜24.5秒 | renderer_native | 公式確認へ進むsemantic flow。実在サイトは再現しない | メール内リンクを開かず公式から確認 |
| 06 | 06 | 24.5〜27.5秒 | imagegen_native | `assets/imagegen_native_v2/normalized/scene_05_official.png` | 落ち着いて確認する人物＋「最後は / 公式から確認」 |
| 07 | 06 | 27.5〜30秒 | renderer_native | 共通CTA。疑似登録・チャンネルアイコンなし | CTAだけを表示 |

## ImageGen文字QA

- `imagegen_native`：3scene
- 指定文言一致：3/3 PASS
- 誤字・脱字・余計な文字・文字切れ：0
- 再生成：0回
- generated imageへの大見出し後乗せ：0（NO_IMAGE_TEXT_HYBRID）
- 実在メール、企業ロゴ、URL、QR、個人情報、公式UI：0
- 元画像はrootのassetに保持し、`normalized/`を動画とサムネイル候補へ使用する

## CTA / thumbnail

- CTAは共通renderer。spokenは`shorts/common_cta.md`の共通版を再利用
- CTAにsubscribe icon、チャンネルアイコン、Short002 IDを描画しない
- `assets/thumbnail_candidate/first_frame_thumbnail_candidate.png`は冒頭ImageGen-native画像の正規化copy。thumbnail確定は未実施
