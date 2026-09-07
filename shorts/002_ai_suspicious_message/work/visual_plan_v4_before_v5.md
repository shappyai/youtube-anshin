# Short002 visual plan — Visual Redesign v4

## v4方針

- Draft v3の3 core scenes（冒頭 / 行動 / 結論）を8 visual beatsへ展開する。
- v3の「スマホを隠す人物」privacy visualは採用しない。個人情報を隠す意味が一目で分かるrenderer-native generic documentへ置換する。
- 実在メール、企業名、URL、QR、ロゴ、アプリUI、実個人情報は使わない。
- beatの目標変更間隔は2〜4秒。v4実測は8 beats、static hold >5秒は0、>7秒は0。
- CTA専用slideは作らず、結論Visualを維持した最後約4.7秒の中で、最後のbeatだけ実チャンネルlockupを表示する。

## Visual beat plan（実測）

| Beat | 範囲 | core | asset / mode | 役割 |
|---|---:|---|---|---|
| A1 | 0.00–1.66秒 | A 冒頭 | `scene_01_hook.png` / ImageGen-native | 人物＋問いのhook |
| A2 | 1.66–3.33秒 | A 冒頭 | 同hookのphone crop | 迷いの対象へ寄る |
| B1 | 3.33–8.27秒 | B 行動 | `assets/renderer_v4/privacy_mask_stage_0.png` / renderer-native | 一般化した文面と欄を見せる |
| B2 | 8.27–13.22秒 | B 行動 | `privacy_mask_stage_1.png` / renderer-native | 氏名・電話番号だけを■■■■で隠す |
| B3 | 13.22–18.16秒 | B 行動 | `privacy_mask_stage_2.png` / renderer-native | 会員番号・メールも該当欄だけ隠す |
| C1 | 18.16–22.85秒 | C 結論 | `scene_05_official.png` / ImageGen-native | 公式確認へ戻る |
| C2 | 22.85–27.55秒 | C 結論 | 同officialのclose crop | 確認手順へ寄る |
| C3 | 27.55–32.24秒 | C 結論 | 同official＋実チャンネルlockup | 結論とCTA |

## Privacy visual boundary

- renderer画面は汎用の文面で、表示する文字は「氏名」「電話番号」「会員番号」「メールアドレス」の例示だけにする。
- 値そのものは置かず、該当領域を中立placeholderまたは`■■■■`で示す。B2/B3では隠す欄だけが変わる。
- 自作画面を実在メールや公式アプリの画面として見せない。AI生成した旧`scene_02_mask.png`はv4で不使用。
- 字幕帯とrenderer内の文面を重ねない。字幕は「名前や番号は／先に隠す」「AIは整理の補助」など短いcueに限定する。

## CTA / 音声・字幕

- spoken canonicalは「次に困ったときのために、このチャンネルを登録しておいてください。」。
- 最終beatに実在の承認済み`local/channel/icon.png`と「大人のデジタル安心室」を表示する。登録ボタン・赤い登録UI・疑似subscribeは描画しない。
- 字幕はtarget80px / min64px / 最大2行。画像見出しと完全重複させない。

## QA / outputs

- fake UI：0、official UI AI reconstruction：0、privacy fail：0、hybrid large-text overlay：0。
- ImageGen-native 2 assetはv2から再利用。新規ImageGen call：0、再生成：0。renderer visual beat：3。
- Draft：`output/draft_v4.mp4`
- 音声：`audio/narration_v4.wav`（CTA segmentのみv4生成）
- Render manifest：`work/render_manifest_v4.json`
- Contact sheet：`work/contact_sheet_v4.png`
- Privacy renderer QA：`work/imagegen_text_qa_v4.md`（renderer境界も記録）
- Short002全体レビュー：`../work/batch_001_v4_timeline_review.md`
- サムネイル候補：`assets/thumbnail_candidate/first_frame_thumbnail_candidate.png`（確定未実施）
- final、publish、upload、scheduleは未実施。
