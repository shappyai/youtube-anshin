# Short001 visual plan — Draft v8（Dictation + real answer）

## 方針

- canonical title：`ChatGPT、文字を打たなくても使える？`
- feature：`Dictation / 音声入力`
- v7の読みやすい静止＋hard cutを維持し、元capture後半の実際のChatGPT回答を追加する。
- ChatGPT画面・回答文はユーザー提供captureのcrop・resizeのみ。架空UI、ImageGenによる公式UI再現、回答文の合成はしない。
- 回答sceneに大きな説明見出しを後乗せしない。短い字幕だけを下部の安全帯へ置く。
- 字幕はtarget80px / min64px / 最大2行。captureの画面を字幕帯で覆わないよう、実画面を上部plateへ配置する。
- CTAは結論Visualの最後3秒に実チャンネルアイコン約180pxと「大人のデジタル安心室」を中央表示する。疑似subscribeは描画しない。

## Visual beat plan

| Beat | audio segment | 役割 | asset / mode | state | motion |
|---|---:|---|---|---|---|
| A1 | 01 | hook | `assets/imagegen_native_v7/normalized/short001_dictation_hook.png` / ImageGen-native | 文字を打たなくても使える？ | hard cut static |
| B1 | 02 | 実画面への導入 | `assets/official_v8/normalized/dictation_intro_focus.png` / real capture crop | マイク入力中の実画面 | hard cut static |
| B2 | 03 | 実際に話す | `assets/official_v8/chatgpt_dictation_capture_source.mp4` / real capture sequence | 話す → 文字起こし中 → 質問文表示 | real_capture_natural |
| C1 | 04 | 文字を確認して送信 | `assets/official_v8/normalized/dictation_text_focus.png` / real capture crop | 質問文が文字になった状態 | hard cut static |
| E1 | 05 | 実際の回答 | `assets/official_v8/normalized/chatgpt_answer_focus.png` + source frame sequence / real capture | 回答冒頭 → 料理名・材料 | real_capture_natural |
| D1 | 06 | 短い結論 | `assets/imagegen_native_v7/normalized/short001_dictation_conclusion.png` / ImageGen-native | 文字を打たずに質問 | hard cut static |
| D2 | 07 | CTA | D1と同じasset＋実チャンネルlockup | CTA表示state | hard cut static |

## Capture boundary / audio

- source：`shorts/work/ChatGPT Voice画面録画.MP4`
- Dictation input：3.800〜12.800秒、9.000秒。ユーザー音声を採用する。
- 実回答：14.200〜17.000秒、2.800秒。画面はcrop / resizeのみで使い、動画内では約2.5〜4秒表示する。
- 実回答sceneでは機械返答音声を使わず、「料理の答えが返ってきました。」をVOICEVOXで短く説明する。
- 回答の全文、後半の評価dialog、元画面の個人情報は使用しない。
- capture音声には70Hz high-passと約−6.9dBの軽いレベル調整だけを適用し、強いdenoiseやgateは使わない。
- CTA spoken canonical：`次に困ったときのために、このチャンネルを登録しておいてください。`

## QA / outputs

- `real_dictation_ui=PASS`
- `real_chatgpt_answer=PASS`
- `fake_ui=0`
- `official_ui_ai_reconstruction=0`
- `voice_dictation_confusion=0`
- `privacy_fail=0`
- `subtitle_overflow=0`
- `Shorts UI overlap=0`
- `Fact FAIL=0`
- Draft：`output/draft_v8.mp4`
- Answer QA：`work/chatgpt_answer_capture_v8.md`
- Audio QA：`work/voice_capture_audio_qa_v8.md`
- Draft QA：`work/draft_v8_qa.md`
- 実測タイムライン：`work/render_manifest_v8.json`

final、upload、publish、scheduleは行わない。
