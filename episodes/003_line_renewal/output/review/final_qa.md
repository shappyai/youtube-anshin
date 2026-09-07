# Episode 003 final QA

確認日: 2026-08-31

## Finalization

- 人間最終レビュー: approved
- 承認対象: `output/draft_auto_v3.mp4`
- finalize方式: 再encodeなしのcopy-only
- final: `output/final.mp4`
- YouTube upload / thumbnail / publish: 未実施

## Identity

| File | SHA-256 |
|---|---|
| draft_auto_v3.mp4 | `AF4323F3364832CDE784EDE9F717A0D26AD45E1F285182D8F807C51DCEAE4788` |
| final.mp4 | `AF4323F3364832CDE784EDE9F717A0D26AD45E1F285182D8F807C51DCEAE4788` |

一致: PASS

## Media QA

- duration: 300.833333 sec
- video: H.264 / 1920×1080 / 30 fps
- audio: AAC / 48,000 Hz / mono
- audio present: PASS
- decode errors: 0
- black frame intervals: 0
- subtitle: videoへ焼き込み済み。subtitle streamなし、字幕表示中の実フレームを確認
- draft_auto_v1 / draft_auto_v2 / draft_auto_v3: すべて保持

## State

- episode state: finalized / human approved
- `STATE.md`: 更新済み
- `publish.json`: `finalized_human_approved`
