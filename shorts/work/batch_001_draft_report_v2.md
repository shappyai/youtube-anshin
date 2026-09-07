# Shorts探索バッチ001 Visual Redesign Draft v2 report

- Visual Redesign：3本とも冒頭をImageGen-nativeへ変更
- 音声：既存VOICEVOX segment WAVを再利用。全音声の再生成なし
- 公式UI：ImageGenで生成していない。Short001はVoice実UIを使わずsemantic visualへ変更
- viewer-facing Short ID：0

| ID | duration | scene数 | ImageGen-native | real UI | first 3sec | visual QA | draft | thumbnail candidate |
|---|---:|---:|---:|---:|---|---|---|---|
| Short001 | 27.70秒 | 6 | 3 | 0 | 4/5 target | PASS_WITH_HUMAN_DRAFT_GATE | shorts/001_chatgpt_voice_input/output/draft_v2.mp4 | shorts/001_chatgpt_voice_input/assets/thumbnail_candidate/first_frame_thumbnail_candidate.png |
| Short002 | 30.98秒 | 6 | 3 | 0 | 4/5 target | PASS_WITH_HUMAN_DRAFT_GATE | shorts/002_ai_suspicious_message/output/draft_v2.mp4 | shorts/002_ai_suspicious_message/assets/thumbnail_candidate/first_frame_thumbnail_candidate.png |
| Short003 | 27.34秒 | 6 | 3 | 0 | 4/5 target | PASS_WITH_HUMAN_DRAFT_GATE | shorts/003_mynumber_smartphone/output/draft_v2.mp4 | shorts/003_mynumber_smartphone/assets/thumbnail_candidate/first_frame_thumbnail_candidate.png |

## 共通QA

- Fact FAIL：0
- fake UI：0
- official_ui_ai_reconstruction：0
- privacy_fail：0
- Shorts UI overlap：0
- hybrid_generated_image_large_text：0
- subtitle_overflow：0
- unexpected_silence：0
- ImageGen再生成：0 / renderer fallback：0
- CTA：3本共通版を各1回。音声は既存版を再利用

- Contact sheet：shorts/work/batch_001_draft_contact_sheet_v2.png
- 各Shortのwork/contact_sheet_v2.pngとwork/imagegen_text_qa_v2.mdも参照する。

Draft v2完成後は、final、thumbnail確定、upload、schedule、publishへ進まない。

Shorts探索バッチ001 Visual Redesign完了。3本ともImageGen-native冒頭へ変更しdraft_v2生成。人間Draft Gate待ち。
