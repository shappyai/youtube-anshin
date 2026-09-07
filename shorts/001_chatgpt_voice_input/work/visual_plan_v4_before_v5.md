# Short001 visual plan — Visual Redesign v4

## v4方針

- Draft v3の3枚ストーリーは維持し、A 冒頭 / B 行動 / C 結論の3 core scenesを8 visual beatsへ展開する。
- beatの目標変更間隔は2〜4秒。v4実測は8 beats、static hold >5秒は1、>7秒は0。
- ImageGen-nativeは人物hookと結論の2資産だけを再利用し、rendererで大見出しを後乗せしない。
- 実在UIが必要な箇所は実画面または公式参照画面だけを使う。架空のChatGPT Voice UIは描かない。
- CTA専用slideは作らず、結論Visualを維持した最後約3.2秒に、承認済みの実チャンネルアイコンと「大人のデジタル安心室」だけを表示する。

## Visual beat plan（実測）

| Beat | 範囲 | core | asset / mode | 役割 |
|---|---:|---|---|---|
| A1 | 0.00–3.18秒 | A 冒頭 | `assets/imagegen_native_v2/normalized/scene_01_hook.png` / ImageGen-native | 人物＋問いのhook |
| A2 | 3.18–6.36秒 | A 冒頭 | 同hookのphone crop | スマホへ視線を寄せる |
| B1 | 6.36–9.29秒 | B 行動 | `assets/official_v4/normalized/chatgpt_home_current.png` / 現行実画面 | 現行chatgpt.comログアウト画面 |
| B2 | 9.29–12.21秒 | B 行動 | `assets/official_v4/normalized/voice_official_reference.png` / 公式参照 | Voice紹介ページ。ライブUIとは表示しない |
| B3 | 12.21–15.13秒 | B 行動 | `assets/official_v4/normalized/chatgpt_home_current.png` / 現行実画面 | 質問capture未取得時の実画面crop |
| B4 | 15.13–18.05秒 | B 行動 | 同ChatGPT実画面のclose crop | 回答capture未取得時の実画面crop |
| C1 | 18.05–25.00秒 | C 結論 | `scene_06_summary.png` / ImageGen-native | 「まずは話しかけるだけ」 |
| C2 | 25.00–28.21秒 | C 結論 | 同summary＋実チャンネルlockup | 結論を保持してCTA |

## 実UI / capture boundary

- B1/B3/B4はAndroid emulator / Chromeで取得した現行chatgpt.comのログアウト画面。アカウント・履歴・通知・個人情報は入れない。
- B2はOpenAI公式Voice紹介ページの参照画面であり、アプリ内のライブVoiceセッション画面として扱わない。
- ログイン後の実Voiceセッション（5〜10秒）は未取得。`CAPTURE_REQUIRED`として人間Draft Gateで追加要否を判断する。
- Voice画面がない状態を、生成画像や後描画UIで補完しない。

## 音声・字幕

- 表示は`ChatGPT`、VOICEVOX入力は`チャットジーピーティー`。
- 実audio_query/mora_dataを確認し、Short001のsegment 01 / 05は「ト」を3モーラ目のaccent=3として再生成する。
- CTAのspoken canonicalは「次に困ったときのために、このチャンネルを登録しておいてください。」。
- 字幕はtarget80px / min64px / 最大2行。画像内の見出しをそのまま反復しない。

## QA / outputs

- fake UI：0、official UI AI reconstruction：0、hybrid large-text overlay：0、privacy fail：0。
- ImageGen新規call：0、再生成：0。Short001のImageGen-native 2 assetはv2から再利用。B3/B4は実ChatGPT画面のcrop違い。
- Draft：`output/draft_v4.mp4`
- 音声：`audio/narration_v4.wav`（変更segmentのみv4生成）
- Render manifest：`work/render_manifest_v4.json`
- Contact sheet：`work/contact_sheet_v4.png`
- Pronunciation QA：`work/pronunciation_qa_v4.md` / `work/chatgpt_pronunciation_v4.json`
- Short001全体レビュー：`../work/batch_001_v4_timeline_review.md`
- サムネイル候補：`assets/thumbnail_candidate/first_frame_thumbnail_candidate.png`（確定未実施）
- final、publish、upload、scheduleは未実施。
