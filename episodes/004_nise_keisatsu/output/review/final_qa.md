# Episode 004 final QA

確認日: 2026-08-31

## Finalization

- 人間最終レビュー: approved（draft_v3を全編再視聴・違和感なし）
- 承認対象: `output/draft_v3.mp4`
- finalize方式: 再encodeなしのcopy-only
- final: `output/final.mp4`
- YouTube upload / thumbnail / publish: 本レポート時点の状況をSTATE.mdに記録

## Identity

| File | SHA-256 |
|---|---|
| episodes/004_nise_keisatsu/output/draft_v3.mp4 | 2022F1BD549B60CAA6664BFDA22F92789DDA781FD35C6F3589E7155EACBFD6FE |
| episodes/004_nise_keisatsu/output/final.mp4 | 2022F1BD549B60CAA6664BFDA22F92789DDA781FD35C6F3589E7155EACBFD6FE |

- hash一致: 完全一致（copy-only finalize）

## Media probe（ffprobe）

- duration: 401.8s
- video: h264 1920x1080 30fps
- audio: aac 48000Hz
- size: 21,251,254 bytes

## Checks

- decode error: 0
- black frame: 0（blackdetect）
- 無音異常: 0
- scenes: 18 / subtitle cues: 72 / narration segments: 72
- CTA: channel_common_cta 10s（brand promiseなし）
- 最終QA status: **PASS**
