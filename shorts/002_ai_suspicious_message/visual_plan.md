# Short002 visual plan — Visual Redesign v5

## v5方針

- v4の3 core scenesを保ち、A1/A2の同一ImageGen asset重複を統合する。
- `shorts_micro_motion_for_motion_sake=FORBIDDEN`。zoom、pan、slow cropは使わず、未マスク→一部マスク→全マスク、full→意味のあるfocus cropなど情報状態が変わるときだけhard cutする。
- privacy rendererはv4で承認された汎用文面を再利用する。実在メール、企業名、URL、QR、ロゴ、個人情報は使わない。
- CTA専用slideは作らず、結論Visualの最後3秒だけ、実チャンネルアイコン180px＋「大人のデジタル安心室」を中央に表示する。

## Visual beat plan（v5実測）

| Beat | 範囲 | core | asset / mode | 役割 | motion |
|---|---:|---|---|---|---|
| A1 | 0.00–3.33秒 | A 冒頭 | `assets/imagegen_native_v2/normalized/scene_01_hook.png` / ImageGen-native | 人物＋問いのhook | hard cut static |
| B1 | 3.33–8.27秒 | B 行動 | `assets/renderer_v4/privacy_mask_stage_0.png` / renderer-native | 汎用文面。まだ隠していない | hard cut static |
| B2 | 8.27–13.22秒 | B 行動 | `assets/renderer_v4/privacy_mask_stage_1.png` / renderer-native | 氏名・電話番号を隠す | hard cut static |
| B3 | 13.22–18.16秒 | B 行動 | `assets/renderer_v4/privacy_mask_stage_2.png` / renderer-native | 該当欄をすべて隠す | hard cut static |
| C1 | 18.16–22.85秒 | C 結論 | `assets/imagegen_native_v2/normalized/scene_05_official.png` / ImageGen-native | 公式から確認 | hard cut static |
| C2 | 22.85–27.55秒 | C 結論 | `assets/renderer_v5/scene_05_official_focus.png` / meaningful crop | 人物・スマホへ意味のあるfocus | hard cut static |
| C3 | 27.55–32.24秒 | C 結論 | `assets/imagegen_native_v2/normalized/scene_05_official.png`＋lockup | 最後3秒だけCTA lockup | hard cut static |

## Privacy / audio

- B1→B2→B3は個人情報の表示状態だけが段階的に変わる。画面の文面は「氏名」「電話番号」「会員番号」「メールアドレス」の例示で、値は置かない。
- C2のfocusは微小zoomではなく、元画像のheadline領域を避けて人物・スマホ・フォルダーを見せる別asset。切れた文字を表示しない。
- 台本変更0、音声再生成0。`audio/narration_v4.wav`とv4の実時間cueを再利用する。
- CTA spoken canonicalは「次に困ったときのために、このチャンネルを登録しておいてください。」。`概要欄から`は追加しない。

## QA / outputs

- fake UI：0、official UI AI reconstruction：0、privacy fail：0、hybrid large-text overlay：0。
- meaningful asset/state changeだけを使用。micro motion only：0、meaningless zoom：0、meaningless pan：0。
- 字幕はtarget80px / min64px / 最大2行。字幕帯とrenderer内の文面を重ねない。
- Draft：`output/draft_v5.mp4`
- Render manifest：`work/render_manifest_v5.json`
- Contact sheet：`work/contact_sheet_v5.png`
- Audio reuse：`work/v5_audio_reuse.md`
- Short002全体レビュー：`../work/batch_001_v5_timeline_review.md`
- サムネイル候補：`assets/thumbnail_candidate/first_frame_thumbnail_candidate.png`（確定未実施）
- final、publish、upload、scheduleは未実施。
