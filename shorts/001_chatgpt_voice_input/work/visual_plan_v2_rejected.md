# Short001 visual plan — Visual Redesign v2

## 共通

- canvas：1080×1920、30fps、縦
- target_duration：30秒（Draft v2実測27.70秒）
- draft_v2：output/draft_v2.mp4
- audio：既存VOICEVOX segment WAVを再利用。Visual変更のため全音声は再生成しない
- viewer_facing_short_id：0。冒頭を含む動画フレームにShort001やチャンネル名を表示しない
- subtitle_safe_area：下部字幕帯。画像内の大見出し・人物の顔・スマホを隠さない
- visual_rule：ImageGen-native画像は人物・背景・主要見出しの完成画。大見出しの後乗せは禁止。公式UIは生成しない

## Scene / segment plan

| Segment | Scene | 時間目安 | render_mode | 内容・asset | 画面の主役 |
|---:|---:|---:|---|---|---|
| 01 | 01 | 0〜3秒 | imagegen_native | `assets/imagegen_native_v2/normalized/scene_01_hook.png` | 日本人シニア＋generic smartphone＋「ChatGPT / 話すだけで使える？」 |
| 02 | 02 | 3〜6秒 | renderer_native | microphone / conversation semantic visual | 音声モードの意味 |
| 03 | 03 | 6〜10秒 | renderer_native | Voice実UIは未取得のため、公式UIを再現せずsemantic visual | 音声モードを開く行動。実画面と誤認させない |
| 04 | 04 | 10〜18秒 | imagegen_native | `assets/imagegen_native_v2/normalized/scene_04_life.png` | 卵・キャベツ・generic smartphone＋「今日のごはん、 / 何を作れる？」 |
| 05 | 05 | 18〜24秒 | renderer_native | assistant semantic visual | 回答の開始。全文は見せない |
| 06 | 06 | 24〜27秒 | imagegen_native | `assets/imagegen_native_v2/normalized/scene_06_summary.png` | 納得する人物＋「まずは / 話しかけるだけ」 |
| 07 | 06 | 27〜29秒 | renderer_native | 写真入力を示すsemantic visual | 次テーマへの短い導線 |
| 08 | 06 | 29〜31秒 | renderer_native | 共通CTA。疑似登録・チャンネルアイコンなし | CTAだけを表示 |

## ImageGen文字QA

- `imagegen_native`：3scene
- 指定文言一致：3/3 PASS
- 誤字・脱字・余計な文字・文字切れ：0
- 再生成：0回
- generated imageへの大見出し後乗せ：0（NO_IMAGE_TEXT_HYBRID）
- 生成画像内の公式UI・OpenAI logo：0
- 元画像はrootのassetに保持し、`normalized/`を動画とサムネイル候補へ使用する

## Short001 Voice UI REVIEWの扱い

公開ログアウト画面ではVoiceアイコンを取得できなかった。v2ではfake UIで補わず、Segment 03をsemantic visualに変更した。Voiceの位置・表示名を実機画面で断定する場合は、final前に人間が確認する。現在のナレーションは「音声アイコンをタップします」を保持し、semantic visualは実UIの再現ではないことをDraft Gateで確認する。

## CTA / thumbnail

- CTAは共通renderer。spokenは`shorts/common_cta.md`の共通版を再利用
- CTAにsubscribe icon、チャンネルアイコン、Short001 IDを描画しない
- `assets/thumbnail_candidate/first_frame_thumbnail_candidate.png`は冒頭ImageGen-native画像の正規化copy。thumbnail確定は未実施
