# Phase 2 QA

- status: PASS
- scenes: 18
- expected duration: 336.804s

## FAIL

- なし

## WARN

- なし

## Phase B追加チェック

- video: H.264 / 1920x1080 / 30fps / AAC / 48kHz mono
- duration: 336.803s（expected 336.804s、delta 0.001s）
- narration: 63/63 WAV、segment timing 321.804s、欠落0
- subtitles: 122 cue、minimum 72px、3-line 0、overflow 0、semantic split 0
- visual source: `work/rendered_final_scenes_v5/` の18scene。background regression 0、native scene regression 0、semantic icon visual center PASS
- representative frames: `work/qa_frames_draft_v1/` の18scene＋CTA、19枚。contact sheetを目視確認済み
- senior readability: **REVIEW**（機械チェックPASS、全編人間視聴待ち）
