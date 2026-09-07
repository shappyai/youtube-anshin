# Short001 visual plan — Visual Redesign v5

## v5方針

- v4の3 core scenesを保ち、A1/A2の同一ImageGen asset重複を統合する。
- `shorts_micro_motion_for_motion_sake=FORBIDDEN`。zoom、pan、slow cropは使わず、asset切替だけをhard cutで行う。
- 静止画は字幕を読みやすくするため2〜5秒を基本に保持する。beat数を増やすためのcropは行わない。
- ChatGPTの実画面は現行ログアウト画面、Voiceは公式紹介ページの参照画面だけを使う。架空のVoiceセッションUIは作らない。
- CTA専用slideは作らず、結論Visualの最後3秒だけ、実チャンネルアイコン180px＋「大人のデジタル安心室」を中央に表示する。登録ボタン・疑似subscribeは描画しない。

## Visual beat plan（v5実測）

| Beat | 範囲 | core | asset / mode | 役割 | motion |
|---|---:|---|---|---|---|
| A1 | 0.00–3.31秒 | A 冒頭 | `assets/imagegen_native_v2/normalized/scene_01_hook.png` / ImageGen-native | 人物＋問いのhook | hard cut static |
| B1 | 3.31–8.22秒 | B 行動 | `assets/official_v5/normalized/chatgpt_home_current.png` / 現行実画面 | 現行chatgpt.comログアウト画面 | hard cut static |
| B2 | 8.22–13.14秒 | B 行動 | `assets/official_v5/normalized/voice_official_reference.png` / 公式参照 | Voice紹介ページ。ライブUIとは表示しない | hard cut static |
| B3 | 13.14–18.05秒 | B 行動 | `assets/imagegen_native_v2/normalized/scene_04_life.png` / ImageGen-native | 生活の質問を話しかける | hard cut static |
| C1 | 18.05–23.13秒 | C 結論 | `assets/imagegen_native_v2/normalized/scene_06_summary.png` / ImageGen-native | 「まずは話しかけるだけ」 | hard cut static |
| C2 | 23.13–28.21秒 | C 結論 | 同summary＋実チャンネルlockup | 最後3秒だけCTA lockup | hard cut static |

## Capture boundary / audio

- B1はAndroid emulator / Chromeで取得した現行chatgpt.comログアウト画面。B2はOpenAI公式Voice紹介ページの参照画面。
- ログイン後のライブVoiceセッション録画は未取得のため `CAPTURE_REQUIRED`。v5でも偽UIを追加しない。
- 台本変更0、音声再生成0。`audio/narration_v4.wav`とv4の実時間cueを再利用する。
- CTA spoken canonicalは「次に困ったときのために、このチャンネルを登録しておいてください。」。`概要欄から`は追加しない。

## QA / outputs

- fake UI：0、official UI AI reconstruction：0、hybrid large-text overlay：0、privacy fail：0。
- meaningful asset/state changeだけを使用。micro motion only：0、meaningless zoom：0、meaningless pan：0。
- 字幕はtarget80px / min64px / 最大2行。字幕帯は操作画面を覆わない。
- Draft：`output/draft_v5.mp4`
- Render manifest：`work/render_manifest_v5.json`
- Contact sheet：`work/contact_sheet_v5.png`
- Audio reuse：`work/v5_audio_reuse.md`
- Short001全体レビュー：`../work/batch_001_v5_timeline_review.md`
- サムネイル候補：`assets/thumbnail_candidate/first_frame_thumbnail_candidate.png`（確定未実施）
- final、publish、upload、scheduleは未実施。
