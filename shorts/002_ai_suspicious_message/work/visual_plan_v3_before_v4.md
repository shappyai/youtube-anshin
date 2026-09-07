# Short002 visual plan — Visual Redesign v3

## v3方針

- Draft v2はHuman Draft GateでREJECT。説明rendererの連続を廃止する。
- 3枚ストーリー：冒頭（問い）→行動（隠す・AIは補助）→結論（公式確認とCTA）。
- canvas：1080×1920、30fps。Draft v3実測30.98秒。
- ImageGen-native完成画を3枚再利用。新規ImageGen call 0、再生成0、音声変更0。
- 実在メール・企業ロゴ・URL・QR・個人情報・公式UIは使わない。AI生成で精密な黒塗りUIも作らない。
- renderer説明scene 0、dedicated CTA slide 0。字幕だけを最下部230pxと右側UI領域を避けて表示する。
- 各major visualを105%→112%のゆっくりズーム。冒頭フレームから人物＋問いを表示し、fade in・ID・ロゴなし。

## Major visual plan

| Major visual | Segment | 実測範囲 | asset | ImageGen-nativeの主役 | CTA |
|---|---:|---:|---|---|---|
| A 冒頭 | 01 | 0.00–3.33秒 | `assets/imagegen_native_v2/normalized/scene_01_hook.png` | 困った人物＋generic smartphone＋「このメール、 / 本物？」 | なし |
| B 行動 | 02–04 | 3.40–18.16秒 | `assets/imagegen_native_v2/normalized/scene_02_mask.png` | 個人情報を隠そうとする状況＋「個人情報は / まず隠す」 | なし |
| C 結論 | 05–07 | 18.23–30.98秒 | `assets/imagegen_native_v2/normalized/scene_05_official.png` | 公式確認で落ち着く人物＋「最後は / 公式から確認」 | 最後のCTA字幕のみ |

字幕は画像内見出しを完全反復せず、Aは「AIに聞く前に／一呼吸」、Bは「名前や番号は／先に隠す」「AIは整理の補助」などナレーション補助に分担する。字幕は80px基準、64px未満へ縮小しない、最大2行。

## Fact / privacy boundary

- AIを詐欺判定機にしない。「AIは補助。最後は公式から確認」を維持する。
- メール内リンクは開かず、公式アプリまたはブックマークした公式サイトから確認する説明はナレーションで伝える。
- Fact FAIL：0、fake UI：0、official_ui_ai_reconstruction：0、privacy_fail：0。
- headline_subtitle_duplicate：0、hybrid_generated_image_large_text：0、viewer-facing Short ID：0。
- subtitle_overflow：0、Shorts UI overlap：0、unexpected silence：0、pronunciation：REVIEW（人間聴取待ち）。

## outputs

- Draft：`output/draft_v3.mp4`
- 音声：`audio/narration_v3.wav`（既存segment WAVを全再利用）
- Contact sheet：`work/contact_sheet_v3.png`
- ImageGen QA：`work/imagegen_text_qa_v3.md`
- サムネイル候補：`assets/thumbnail_candidate/first_frame_thumbnail_candidate.png`（確定未実施）
