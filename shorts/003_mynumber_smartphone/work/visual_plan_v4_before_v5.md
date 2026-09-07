# Short003 visual plan — Visual Redesign v4

## v4方針

- Draft v3の3 core scenes（冒頭 / 行動 / 結論）を8 visual beatsへ展開する。
- 「マイナポータル」「コンビニの証明書」「e-Tax」を大きな3カード説明にせず、短いsemantic cueとしてrenderer-nativeで各2〜3秒表示する。
- ImageGen-nativeの人物・生活画は再利用し、正確なサービス名だけをrendererで表示する。公式UIの再現は行わない。
- beatの目標変更間隔は2〜4秒。v4実測は8 beats、static hold >5秒は1、>7秒は0。
- CTA専用slideは作らず、結論Visualを維持した最後約3.2秒に、承認済みの実チャンネルアイコンと「大人のデジタル安心室」だけを表示する。

## Visual beat plan（実測）

| Beat | 範囲 | core | asset / mode | 役割 |
|---|---:|---|---|---|
| A1 | 0.00–4.02秒 | A 冒頭 | `scene_01_hook.png` / ImageGen-native | 人物＋問いのhook |
| A2 | 4.02–8.05秒 | A 冒頭 | 同hookのphone/card crop | スマホとカードへ寄る |
| B1 | 8.05–10.68秒 | B 行動 | `assets/renderer_v4/usage_cue_portal.png` / renderer-native | マイナポータルの短いcue |
| B2 | 10.68–13.32秒 | B 行動 | `usage_cue_certificate.png` / renderer-native | 証明書・e-Taxの短いcue |
| B3 | 13.32–15.95秒 | B 行動 | `scene_03_health.png` / ImageGen-native | 医療機関・薬局の利用例 |
| B4 | 15.95–18.59秒 | B 行動 | 同healthのclose crop | 条件付き利用へ寄る |
| C1 | 18.59–25.37秒 | C 結論 | `scene_05_conclusion.png` / ImageGen-native | 実物カードが必要な場面 |
| C2 | 25.37–28.59秒 | C 結論 | 同conclusion＋実チャンネルlockup | 条件付き結論とCTA |

## Usage cue boundary

- B1/B2は単一のgeneric smartphone＋generic cardの自作図解であり、マイナポータルやe-Taxの公式画面ではない。
- UIの細部・ロゴ・政府マーク・カード番号・氏名・顔写真は描かない。正確なサービス名は大きな説明カードにせず短いcueだけで示す。
- 保険証利用は対応する医療機関・薬局に限る条件付き表現を、ImageGen画とナレーションで維持する。

## CTA / 音声・字幕

- spoken canonicalは「次に困ったときのために、このチャンネルを登録しておいてください。」。
- 最終beatに実在の承認済み`local/channel/icon.png`と「大人のデジタル安心室」を表示する。登録ボタン・赤い登録UI・疑似subscribeは描画しない。
- 字幕はtarget80px / min64px / 最大2行。画像見出しと完全重複させない。

## QA / outputs

- fake UI：0、official UI AI reconstruction：0、privacy fail：0、hybrid large-text overlay：0。
- ImageGen-native 3 assetはv2から再利用。新規ImageGen call：0、再生成：0。renderer visual beat：2。
- Draft：`output/draft_v4.mp4`
- 音声：`audio/narration_v4.wav`（CTA segmentのみv4生成）
- Render manifest：`work/render_manifest_v4.json`
- Contact sheet：`work/contact_sheet_v4.png`
- Usage cue QA：`work/imagegen_text_qa_v4.md`（renderer境界も記録）
- Short003全体レビュー：`../work/batch_001_v4_timeline_review.md`
- サムネイル候補：`assets/thumbnail_candidate/first_frame_thumbnail_candidate.png`（確定未実施）
- final、publish、upload、scheduleは未実施。
