# Short003 visual plan — Visual Redesign v3

## v3方針

- Draft v2はHuman Draft GateでREJECT。細かな説明rendererの連続を廃止する。
- 3枚ストーリー：冒頭（問い）→行動（生活利用と条件）→結論（実物カードの条件とCTA）。
- canvas：1080×1920、30fps。Draft v3実測27.34秒。
- ImageGen-native完成画を3枚再利用。新規ImageGen call 0、再生成0、音声変更0。
- renderer説明scene 0、dedicated CTA slide 0。字幕だけを最下部230pxと右側UI領域を避けて表示する。
- 各major visualを105%→112%のゆっくりズーム。冒頭フレームから人物＋問いを表示し、fade in・ID・ロゴなし。

## Major visual plan

| Major visual | Segment | 実測範囲 | asset | ImageGen-nativeの主役 | CTA |
|---|---:|---:|---|---|---|
| A 冒頭 | 01–02 | 0.00–8.05秒 | `assets/imagegen_native_v2/normalized/scene_01_hook.png` | 人物＋generic smartphone＋generic card＋「カードを / スマホに？」 | なし |
| B 行動 | 03–04 | 8.12–18.59秒 | `assets/imagegen_native_v2/normalized/scene_03_health.png` | 医療機関・薬局を想起する人物＋generic card＋「保険証として / 使える場合も」 | なし |
| C 結論 | 05–06 | 18.66–27.34秒 | `assets/imagegen_native_v2/normalized/scene_05_conclusion.png` | smartphone＋generic card＋「スマホだけで / 全部ではない」 | 最後のCTA字幕のみ |

字幕は画像内見出しを完全反復せず、Aは「スマホに入れると／何ができる？」、Bは「医療機関や薬局で／使えることも」、Cは「実物カードが／必要な場面も」などナレーション補助に分担する。字幕は80px基準、64px未満へ縮小しない、最大2行。

## Fact / privacy boundary

- マイナポータル、コンビニ証明書、e-Tax、iPhone / Android差は独立Visualにせず、ナレーション＋字幕で扱う。
- 「スマホだけで全部できる」「実物カードは不要」とは言わない。保険証利用も対応する医療機関・薬局に限る条件付き表現を維持する。
- generic cardは番号・氏名・写真・政府ロゴ・正確なカードデザインを含まない。
- Fact FAIL：0、fake UI：0、official_ui_ai_reconstruction：0、privacy_fail：0。
- headline_subtitle_duplicate：0、hybrid_generated_image_large_text：0、viewer-facing Short ID：0。
- subtitle_overflow：0、Shorts UI overlap：0、unexpected silence：0、pronunciation：REVIEW（人間聴取待ち）。

## outputs

- Draft：`output/draft_v3.mp4`
- 音声：`audio/narration_v3.wav`（既存segment WAVを全再利用）
- Contact sheet：`work/contact_sheet_v3.png`
- ImageGen QA：`work/imagegen_text_qa_v3.md`
- サムネイル候補：`assets/thumbnail_candidate/first_frame_thumbnail_candidate.png`（確定未実施）
