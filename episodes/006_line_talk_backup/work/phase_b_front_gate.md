# Episode 006 Phase B前半 Human Gate

- status: `WAITING_FOR_HUMAN_REVIEW`
- date: 2026-09-02（Asia/Tokyo）
- stop point: contact sheet・pronunciation review

## Automated checks

- canonical: schema 0件。narration 68、subtitles 68、scene 24。scene rangeはsegment 1〜68を重複・欠落なくカバー。
- human-review corrections: old CTA wording removed; backup-date wording updated; PIN 10-failure explanation removed from narration; SCENE-018 merged into SCENE-017; opening/summary item synced.
- GPT images: 5/5 generated, one scene/one image/one unique path, original retained. Duplicate SHA-256 0 groups. Review copies 1920×1080 with subtitle-safe bottom 180px.
- official assets: 7/7 present. Android 4 screens and iPhone 1 screen were not captured because the safe environment did not have LINE / iPhone capture; all use clearly labeled official saved-HTML excerpt cards.
- render: 24/24 scene renders PASS. `visual_qa.md` mechanical FAIL 0 / WARN 0.
- subtitles: `subtitle_preflight.md` PASS（fail 0 / warn 0）。
- pronunciation: VOICEVOX 剣崎雌雄・ノーマル、audio_query 68/68。REVIEW 5、dictionary mutation 0。
- privacy/policy: real account, SMS, real talk, personal information, PIN value, QR, and LINE UI recreation were not used.

## Human review required

1. `gpt_image_contact_sheet.png`で5枚のscene内容、重複、collage／split panel、生成文字、LINE UI・ロゴ混入、左右の重心、下180pxの帯を確認する。
2. `scene_contact_sheet.png`で24sceneの順序、scene 18を欠番にした意図、改行、公式カードの可読性、旧Episode混入がないことを確認する。
3. `pronunciation_preflight.md`のREVIEW 5件（seg 018/020/037/047/062）を意図した読みと照合する。必要なら次のゲートでpreview WAVを作る。共通辞書はこのゲートで変更しない。
4. Android/iPhoneの公式fallbackカードを公開候補に残すか、安全なLINEテスト環境を用意して実画面を再取得するか決める。
5. GPT画像5枚の見た目を踏まえ、YouTube AI disclosure `contains_synthetic_media` を人間承認後に確定する。

## Not started by design

- VOICEVOX本編WAV、CTA音声、実尺字幕、draft/final video、thumbnail、publish dry-run、YouTube upload。
