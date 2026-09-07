# Episode 011 Final QA

確認日：2026-09-06  
対象：`output/final.mp4`  
判定：**PASS**

## Final artifact

- source: `output/draft_v2.mp4`
- method: copy-only、再エンコードなし
- byte-identical: **PASS**
- SHA-256: `45AB01EC1FF4F807FFF4ED7F42436FAFD2D00A24FD087BAA7436AF371C78AAB4`
- size: `21,501,533 bytes`
- duration: `251.800 seconds`（expected `251.795 seconds`）
- video: H.264 High / `1920×1080` / `30fps`
- audio: AAC / `48kHz` / mono

## Result

- decode / black frame / unexpected silence / av sync：PASS
- subtitles：39 cue、minimum56px以上、overflow0、3-line0、読み仮名漏出0
- fact / privacy / phone-number / CTA / SCENE-018 native text：PASS
- 重大な未確認事項：0

詳細版：`output/review/final_qa.md`
