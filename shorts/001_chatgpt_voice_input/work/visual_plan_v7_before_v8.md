# Short001 visual plan — Draft v7（Dictation）

## 方針

- canonical title：`ChatGPT、文字を打たなくても使える？`
- feature：`Dictation / 音声入力`
- v5の読みやすい静止＋hard cutを再利用し、今回の主役だけをユーザー提供の実録画へ差し替える。
- 実録画は、音声入力中の状態と文字化後の状態を別の情報stateとして見せる。意味のないzoom、pan、push-inは使わない。
- ChatGPT画面はユーザー提供captureのcrop・resizeのみ。架空UI、ImageGenによる公式UI再現、公式の音声会話紹介画面は使用しない。
- 字幕はtarget80px / min64px / 最大2行。captureの画面を字幕帯で覆わないよう、実画面を上部plateへ配置する。
- CTAは専用slideを追加せず、結論Visualの最後3秒に実チャンネルアイコン約180pxと「大人のデジタル安心室」を中央表示する。疑似subscribeは描画しない。

## Visual beat plan

| Beat | audio segment | 役割 | asset / mode | state | motion |
|---|---:|---|---|---|---|
| A1 | 01 | hook | `assets/imagegen_native_v7/normalized/short001_dictation_hook.png` / ImageGen-native | 「ChatGPT、文字を打たなくても使える？」 | hard cut static |
| B1 | 02 | 実画面への導入 | `assets/official_v7/normalized/dictation_intro_focus.png` / official capture crop | マイク入力中の実画面 | hard cut static |
| B2 | 03 | 実際に話す | `assets/official_v7/chatgpt_dictation_capture.mp4` / real capture sequence | 話す → 文字起こし中 | real_capture_natural |
| C1 | 04 | 文字を確認 | `assets/official_v7/normalized/dictation_text_focus.png` / official capture crop | 質問文が文字になった状態 | hard cut static |
| D1 | 05 | 結論 | `assets/imagegen_native_v7/normalized/short001_dictation_conclusion.png` / ImageGen-native | 「文字を打たずに質問」 | hard cut static |
| D2 | 06 | CTA | D1と同じasset＋実チャンネルlockup | CTA表示state | hard cut static |

## Capture boundary / audio

- source：`shorts/work/ChatGPT Voice画面録画.MP4`
- selected source interval：3.800〜12.800秒、9.000秒
- 3.800〜10.900秒：入力中の実画面を自然な録画フレームで表示
- 10.900〜11.800秒：文字起こし中の状態を表示
- 11.800〜12.800秒：文字化された質問文を表示
- capture音声を9秒使う。VOICEVOX narrationはcapture区間へ重ねない。
- capture音声には70Hz high-passと約−6.9dBの軽いレベル調整だけを適用し、強いdenoiseやgateは使わない。
- CTA spoken canonical：`次に困ったときのために、このチャンネルを登録しておいてください。`

## QA / outputs

- `real_dictation_ui=PASS`
- `fake_ui=0`
- `official_ui_ai_reconstruction=0`
- `voice_dictation_confusion=0`
- `privacy_fail=0`
- `subtitle_overflow=0`
- `Shorts UI overlap=0`
- `Fact FAIL=0`
- Draft：`output/draft_v7.mp4`
- Audio QA：`work/voice_capture_audio_qa.md`
- Draft QA：`work/draft_v7_qa.md`
- 実測タイムライン：`work/render_manifest_v7.json`

final、upload、publish、scheduleは行わない。
