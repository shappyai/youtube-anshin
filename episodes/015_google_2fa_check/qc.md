# Episode 015 QC — full draft

- 状態: `FULL_DRAFT_COMPLETE_WAITING_HUMAN_GATE`
- 確認日: 2026-09-08
- full draft: `output/draft_auto_v2.mp4`
- full draft SHA-256: `c11d2a2333d1b5acce813db09ba6fe43fb5755e27ccfc30849612faaea51c9c8`
- 実尺: 318.740秒（5分18.740秒）
- 映像: 1920×1080 / H.264 / 30fps
- 音声: AAC / 48kHz / mono

## 自動QA

- Phase 2 production preflight: PASS
- Phase 2 QA: PASS（FAIL 0 / WARN 0）
- VOICEVOX pronunciation preflight: PASS、42/42 query、review 0
- Subtitle preflight: PASS、61 cue、FAIL 0 / WARN 0
- viewer-facing INTERNAL_ONLY文言QA: PASS、検出0
- バックアップコード数字の素材混入: 0（入口・存在確認のみ）
- scene renderer: 12枚生成済み。テンプレート9枚、公式UI名fallback 3枚。AI生成画像0枚
- scene quality report: 3件FAIL（公式UIのquote fallbackは背景比較の基準を持たず、blank/centroid判定が機械的にFAIL）。実アカウント画面へ差し替えるか、fallbackを採用するかHuman Gateで確認する。

## Human Gate確認事項

1. 個別のGoogleアカウント設定画面は未capture。scene 004 / 007 / 010は、Google公式ヘルプで確認した正式UI名のfallbackカードであり、実アカウント画面ではない。認証済みテストセッションの実画面へ差し替えるか確認する。
2. PC表示のcrop、字幕の大きさ、1画面1メッセージが65歳以上でも読みやすいか確認する。
3. VOICEVOXの固有名詞・用語の発音と、冒頭30秒以内の対象・3項目の伝わり方を試聴する。
4. バックアップ コードの数字が、動画・字幕・静止画・raw素材のどこにも残っていないことを再確認する。
5. 内容確認が済むまで、thumbnail生成・YouTube upload・publish・finalizeは行わない。

詳細: `work/phase2_qa.md`、`work/pronunciation_preflight.md`、`work/subtitle_preflight.md`、`work/scene_quality_report.md`
