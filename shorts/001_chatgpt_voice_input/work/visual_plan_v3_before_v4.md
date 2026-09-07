# Short001 visual plan — Visual Redesign v3

## v3方針

- Draft v2はHuman Draft GateでREJECT。淡い説明rendererの連続を廃止する。
- 3枚ストーリー：冒頭（問い）→行動（生活例）→結論（CTAを同じ画面へ重ねる）。
- canvas：1080×1920、30fps。Draft v3実測26.95秒（約27秒）。
- ImageGen-native完成画を3枚再利用。新規ImageGen call 0、再生成0。
- 画像内の人物・背景・スマホ・大見出しは完成画のまま使用し、大見出しの後乗せはしない。
- renderer説明scene 0、dedicated CTA slide 0。字幕だけを最下部230pxと右側UI領域を避けて表示する。
- 各major visualを105%→112%のゆっくりズーム。冒頭フレームから人物＋問いを表示し、fade in・ID・ロゴなし。

## Major visual plan

| Major visual | Segment | 実測範囲 | asset | ImageGen-nativeの主役 | CTA |
|---|---:|---:|---|---|---|
| A 冒頭 | 01–02 | 0.00–6.36秒 | `assets/imagegen_native_v2/normalized/scene_01_hook.png` | 日本人シニア＋generic smartphone＋「ChatGPT / 話すだけで使える？」 | なし |
| B 行動 | 03–05 | 6.43–18.05秒 | `assets/imagegen_native_v2/normalized/scene_04_life.png` | 冷蔵庫・卵・キャベツ・スマホ＋「今日のごはん、 / 何を作れる？」 | なし |
| C 結論 | 06–08 | 18.12–26.95秒 | `assets/imagegen_native_v2/normalized/scene_06_summary.png` | 話しかけて納得する人物＋「まずは / 話しかけるだけ」 | 最後のCTA字幕のみ |

字幕は画像内見出しの完全反復を避け、Aは「文字入力は／大変ですか？」、Bは「卵とキャベツで／聞いてみる」、Cは「まずは短い質問から」などナレーション補助に分担する。字幕は80px基準、64px未満へ縮小しない、最大2行。

## Voice UIの扱い

現行のログアウト画面ではVoiceアイコンを確認できなかったため、v3でも公式UIを生成・再現しない。旧「音声アイコンをタップします」は、UI依存を避けて「スマホに向かって、短い質問を話しかけてみます。」へ一般化し、segment 03だけVOICEVOXを差し替えた。他segmentは既存WAVを再利用する。

## QA / outputs

- Fact FAIL：0。VoiceとDictationを混同する説明は追加しない。
- real UI：0、fake UI：0、official_ui_ai_reconstruction：0、privacy_fail：0。
- headline_subtitle_duplicate：0、hybrid_generated_image_large_text：0、viewer-facing Short ID：0。
- subtitle_overflow：0、Shorts UI overlap：0、unexpected silence：0。
- pronunciation：REVIEW（segment 03差し替えを含め、人間聴取待ち）。
- Draft：`output/draft_v3.mp4`
- 音声：`audio/narration_v3.wav`
- Contact sheet：`work/contact_sheet_v3.png`
- ImageGen QA：`work/imagegen_text_qa_v3.md`
- サムネイル候補：`assets/thumbnail_candidate/first_frame_thumbnail_candidate.png`（確定未実施）
