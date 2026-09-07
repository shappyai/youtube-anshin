# Short003 visual plan — Visual Redesign v5

## v5方針

- v4の3 core scenesを保ち、A1/A2の同一ImageGen asset重複と抽象usage rendererを廃止する。
- `shorts_micro_motion_for_motion_sake=FORBIDDEN`。意味のないzoom/panは使わず、公式画面、具体的な生活scene、意味のあるfocus cropをhard cutで切り替える。
- B1〜B3は音声cueに合わせ、マイナポータル→コンビニでの証明書取得→e-Taxを別々に見せる。画面を1枚の説明カードへ詰め込まない。
- 公式画面はデジタル庁公式プレスキットの実画像を使用する。ImageGenでは公式UIを再現しない。
- CTA専用slideは作らず、結論Visualの最後3秒だけ、実チャンネルアイコン180px＋「大人のデジタル安心室」を中央に表示する。

## Visual beat plan（v5実測）

| Beat | 範囲 | core | asset / mode | 役割 | motion |
|---|---:|---|---|---|---|
| A1 | 0.00–2.89秒 | A 冒頭 | `assets/imagegen_native_v2/normalized/scene_01_hook.png` / ImageGen-native | 人物＋問いのhook | hard cut static |
| B1 | 2.89–4.49秒 | B 行動 | `assets/official_v5/normalized/myna_app_home_official.png` / official image | デジタル庁公式のマイナアプリ画面 | hard cut static |
| B2 | 4.49–6.01秒 | B 行動 | `assets/imagegen_native_v5/normalized/convenience_certificate.png` / ImageGen-native | コンビニの複合機で証明書を扱う生活scene | hard cut static |
| B3 | 6.01–8.12秒 | B 行動 | `assets/imagegen_native_v5/normalized/etax_home.png` / ImageGen-native | 自宅でオンライン手続きを準備する生活scene | hard cut static |
| B4 | 8.12–13.63秒 | B 行動 | `assets/imagegen_native_v2/normalized/scene_03_health.png` / ImageGen-native | 医療機関・薬局で使える場合 | hard cut static |
| B5 | 13.63–18.59秒 | B 行動 | `assets/imagegen_native_v5/normalized/scene_03_health_focus.png` / meaningful crop | 端末による違いをfocus | hard cut static |
| C1 | 18.59–24.04秒 | C 結論 | `assets/imagegen_native_v2/normalized/scene_05_conclusion.png` / ImageGen-native | 実物カードが必要な場面 | hard cut static |
| C2 | 24.04–28.59秒 | C 結論 | 同conclusion＋lockup | 最後3秒だけCTA lockup | hard cut static |

## Official / ImageGen boundary

- B1は`episodes/002_myna_app/assets/official/official_screen_home.png`を正規化したもの。sourceはデジタル庁公式プレスキット（`https://services.digital.go.jp/mynaapp/communication-guidelines/`）。AI再構成ではない。
- B2/B3は文字なしのImageGen-native生活scene。証明書の紙、PC画面、スマホ画面には読める文字を入れていない。公式UI・ロゴ・QR・バーコードはない。
- B4/B5の医療利用は「対応する医療機関や薬局では」「使える場合も」という台本の条件付き表現を維持する。B5は端末差の字幕と合わせる意味のあるfocus crop。
- 公式画面に個人情報、ログイン情報、通知は入れていない。

## Audio / outputs

- 台本変更0、音声再生成0。`audio/narration_v4.wav`とv4の実時間cueを再利用する。
- CTA spoken canonicalは「次に困ったときのために、このチャンネルを登録しておいてください。」。`概要欄から`は追加しない。
- fake UI：0、official UI AI reconstruction：0、hybrid large-text overlay：0、privacy fail：0。
- 字幕はtarget80px / min64px / 最大2行。beat数はKPIではなく、具体性と可読性を優先する。
- Draft：`output/draft_v5.mp4`
- Render manifest：`work/render_manifest_v5.json`
- Contact sheet：`work/contact_sheet_v5.png`
- ImageGen prompts：`../work/imagegen_prompts_v5.md`
- Audio reuse：`work/v5_audio_reuse.md`
- Short003全体レビュー：`../work/batch_001_v5_timeline_review.md`
- サムネイル候補：`assets/thumbnail_candidate/first_frame_thumbnail_candidate.png`（確定未実施）
- final、publish、upload、scheduleは未実施。
