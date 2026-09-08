# Episode 015 QC — full draft

- 状態: `FULL_DRAFT_V4_COMPLETE_WAITING_HUMAN_GATE_2`
- 確認日: 2026-09-08
- full draft: `output/draft_auto_v4.mp4`
- full draft SHA-256: `7AB436A319D66CC7EF27BA9A936CC6AC15AC0A725EBEFA7818AFC2C7131EDB5D`
- 実尺: 312.920秒（5分12.920秒、container probe）。音声timeline/QA基準は313.356秒（5分13.356秒）。
- 映像: 1920×1080 / H.264 / 30fps
- 音声: AAC / 48kHz / mono

## 自動QA

- Phase 2 production preflight: PASS
- Phase 2 QA: PASS（FAIL 0 / WARN 0）
- VOICEVOX pronunciation preflight: PASS、42/42 query、review 0
- Subtitle preflight: PASS、61 cue、FAIL 0 / WARN 0
- viewer-facing INTERNAL_ONLY文言QA: PASS、検出0
- バックアップコード数字の素材混入: 0（入口・存在確認のみ）
- scene renderer: 12枚生成済み。テンプレート9枚、実Google UI入口3枚。AI生成画像0枚
- scene quality report: `9 OK / 0 WARN / 3 FAIL`。3件は実Google UI入口の `layout_04_text_official` で、gradient背景には差分比較用の画像背景がないため `background comparison unavailable` となる既知の機械判定。実画面の内容・位置・プライバシーは別のvisual gateと目視で確認する。
- v4 contact sheet: `output/review/draft_contact_sheet_v4.png`（動画代表フレーム）
- 音声・字幕専用確認: `work/audio_subtitle_revision_v4.md`（section番号0件、compound語のaudio_query内breakなし）

## Human Gate確認事項

1. scene 004 / 007 / 010はHumanログイン済みPCブラウザの入口キャプチャへ差し替え済み。65歳以上でもUI名と入口が読めるか確認する。
2. PC表示のcrop、字幕の大きさ、1画面1メッセージが65歳以上でも読みやすいか確認する。
3. VOICEVOXの固有名詞・用語の発音と、冒頭30秒以内の対象・3項目の伝わり方を試聴する。
4. バックアップ コードの数字が、動画・字幕・静止画・raw素材のどこにも残っていないことを再確認する。
5. 内容確認が済むまで、thumbnail生成・YouTube upload・publish・finalizeは行わない。

詳細: `work/phase2_qa.md`、`work/production_preflight_v4.md`、`work/pronunciation_preflight_v4.md`、`work/subtitle_preflight_v4.md`、`work/viewer_facing_internal_brand_promise_v4.md`、`work/cta_preflight_v4.md`、`work/scene_quality_report_v4.md`、`work/audio_subtitle_revision_v4.md`
