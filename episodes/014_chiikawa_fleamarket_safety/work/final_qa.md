# Episode014 final QA

- status: PASS
- human-approved source: `output/draft_v2.mp4`
- final: `output/final.mp4`
- finalization: copy-only
- byte-identical to approved draft: PASS
- final SHA-256: `379D265E899549B34D9AE69CD290E2FC9D948A11B204C4EB37729C7046FCF3BD`
- duration: 289.597 seconds (probe 289.6 seconds)
- resolution: 1920x1080
- frame rate: 30fps
- video codec: H.264
- audio codec: AAC / 48kHz / mono
- decode errors: 0
- black frames: 0
- unexpected silence: 0
- AV sync: PASS

Codec, duration, decode, black-frame, silence, and AV-sync evidence is inherited from `work/phase2_qa_v2.json` because the final file is byte-identical to the approved draft. The local copy-only checker also confirmed SHA-256 equality; its separate ffprobe/ffmpeg availability warning does not change the byte-identical Phase 2 result.
