# Episode 003 QC

## Phase B draft status

- 基準日: 2026-08-31
- 公開候補ではなく、draft_auto_v1の最終人間レビュー待ち。
- 実機撮影: 不要（公式スクリーンショットで成立）
- 本編音声: 生成済み（52 segment、既存hash cacheを52件再利用）
- 本編動画: draft_auto_v1生成済み
- サムネイル: 未制作
- YouTube公開: 未実施

## Fact

- [x] トークタブ公式ページの更新日、15.16.0以上、順次公開、2タブ、友だちリスト導線、年代テスト、ブラウン注記を確認
- [x] ホームタブ公式ページの開始日、26.2.0以上、順次提供、アクティビティ、コンテンツ、友だち・通知・サービス・LINE NEWSを確認
- [x] 旧画面への復帰は、公式ページで確認できた範囲に限定した表現にした

## Language / Visual / Privacy / Policy

- [x] 冒頭20秒以内に結論「LINE公式のリニューアル」を提示
- [x] 「全員が同じ画面」「絶対」「戻せない」といった根拠のない断定を避けた
- [x] LINE UIは公式素材のみ。GPT画像のpromptに偽UI・ロゴ・小さい日本語を禁止
- [x] 個人の実機画面・通知・トーク履歴は使用しない
- [x] 公式素材11点を `asset_manifest.csv` に記録

## Automated gate

実行結果は `work/` の各レポートに保存した。

- episode schema: PASS
- sources: PASS
- subtitles: PASS（52 cue / FAIL 0 / WARN 0）
- pronunciation: PASS（人間承認反映後、remaining review=0）
- scenes: PASS
- scene modes: PASS（template 3 / official 7 / gpt_image 8 / hybrid 0）
- official assets: PASS（本編宣言9点、保存11点のうち予備2点）
- GPT image assets: PASS（8/8、PNG、1920×1080、破損なし）
- Phase 2 video QA: PASS（18scene、1920×1080、30fps、H.264/AAC）

レポート:

- `work/scene_mode_advisor.md`
- `work/image_generation_manifest.md`
- `work/subtitle_preflight.md`
- `work/pronunciation_preflight.md`
- `work/production_preflight.md`
- `work/production_preflight_phase2.md`

## Static scene review

- [x] `work/phase_b_review/scene_contact_sheet.png` を生成
- [x] 18 / 18 sceneを静止画合成
- [x] 自動QA: missing image 0、寸法違反0、placeholder 0、headline overflow 0、safe area警告0
- [x] 人間レビュー: 承認（約75/100）
- [ ] draft動画でGPT画像の表示時間、公式画面の実動画での可読性、テンポを人間確認

## Draft output

- draft: `output/draft_auto_v1.mp4`（290.800秒）
- review contact sheet: `output/review/scene_contact_sheet.png`
- build QA: `output/review/build_qa.md`
- phase 2 QA: `work/phase2_qa.md`（PASS）

## Stop condition

発音4件は承認済み。`draft_auto_v1.mp4`を人間が最後まで視聴するまで、`final.mp4`へのコピー、サムネイル作成、YouTube操作は行わない。

## Phase B v2 修正版（現行）

- 基準日: 2026-08-31
- `output/draft_auto_v1.mp4` は保存したまま。v2は別ファイルとして生成し、final化・サムネイル・YouTube操作は未実施。
- 人間確認済みの新GPT画像8枚（scene_001 / 003 / 007 / 010 / 013 / 014 / 016 / 018）を、すべてPNG・1920×1080・破損なしで使用。
- GPT sceneは同一画像の `full_bleed`。`cover_blur` は既定化していない。大きな白カードや二重layoutは追加せず、Codexの正確な日本語文字と局所scrimだけを重ねた。
- 指摘9時刻は、SCENE-001 / 003 / 007 / 010 / 013 / 014 / 015 / 016 / 018に対応。GPT sceneはフル画面化し、SCENE-015は実際の空き側だけsoft gradientで連続させた。
- 3:13のSCENE-014は横panを無効化し、staticに変更。
- seg_024は`今ブラウン`→`いまブラウン`のsegment overrideを維持。seg_043はApp Store辞書を適用して再生成。
- 本編VOICEVOX: 52 segment。最終差分buildはseg_043のみ再生成、51件をcache再利用。
- 字幕: episode.json確定の52 cueを維持。再分割なし。
- 動画: 18 content scene + Episode 002 CTA postroll 10.046秒。v1 290.800秒、v2 300.833秒（想定300.933秒との差0.100秒）。
- v2仕様: 1920×1080 / 30fps / H.264 / AAC 48kHz mono。
- QA: Phase A PASS、Phase 2 QA PASS。GPT画像、placeholder、字幕、黒フレーム、音声欠落のFAIL/WARNなし。
- 人間確認: v2を最後まで視聴し、9時刻の左右余白、3:13の静止、2:07・3:56の発音、CTAの表示時間を確認する。

成果物:

- `output/draft_auto_v2.mp4`
- `output/review/scene_contact_sheet_v2.png`
- `output/review/build_qa_v2.md`

v2確認が終わるまで、`final.mp4`は生成しない。

## Phase B v3 修正版（現行）

- 基準日: 2026-08-31
- v1 / v2は上書きせず保存。v3はSCENE-015の構図とpostroll CTAだけを変更。
- 3:32は実タイムライン上のSCENE-015（205.238–227.917秒）。旧レイアウトのコンテンツ群が左側で完結していたため、シンボル・headline・support・main messageを`content_offset_x=360`で右へ移動し、static化した。
- CTAはEpisode 002の`scene_034.png`を使用せず、`local/channel/icon.png`を正式ロゴとして用いた`output/review/cta_v3.png`へ差し替え。
- 新CTAは`大人のデジタル安心室`、既存bannerの正式表現、`チャンネル登録・高評価もよろしくお願いします`、ブランド文言`怖がらせる前に、確認する。`で構成。10.046秒、音声・CTA字幕なし。
- v2までのGPT画像full_bleed、cover_blur非default、SCENE-014 static、seg_024 / seg_043発音、App Store辞書、52字幕cue、official assetsは維持。
- VOICEVOX: 0 segment再生成、52件cache再利用。動画尺はv2と同じ300.833秒。
- QA: Phase A PASS、Phase 2 QA PASS。WARN/FAILなし。
- v3は人間最終レビュー済み。`draft_auto_v3.mp4`を承認し、copy-onlyでfinal化する。サムネイル・YouTube操作は未実施。

成果物:

- `output/draft_auto_v3.mp4`
- `output/review/cta_v3.png`
- `output/review/scene_015_v3.png`
- `output/review/scene_contact_sheet_v3.png`
- `output/review/build_qa_v3.md`

## Finalized status

- 承認対象: `output/draft_auto_v3.mp4`
- final: `output/final.mp4`
- finalize方式: 再encodeなしのファイルcopy
- 人間承認: 済み（2026-08-31）
- YouTube upload / thumbnail / publish: 未実施

最終QA: `output/review/final_qa.md`
