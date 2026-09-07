# Episode013 pronunciation human approval v3

- Status: `HUMAN_APPROVED`
- Reviewed at: `2026-09-06`
- Review pack: `work/pronunciation_review_v3.wav`
- Review count: `8`
- Human result: `ALL OK`
- Audio regenerated: `0`
- Global dictionary additions: `0`
- Context-specific approvals: `8`

## 承認範囲

以下の8件は、`pronunciation_review_v3.wav`を人間が全件聴取し、自然な文脈で問題なしと確認した。承認はEpisode013の該当segment・該当語に限定する。`開く／開ける`、`上`、`下`は文脈依存のため、`config/voicevox_pronunciation.yaml`へ無条件登録しない。

| # | Segment | Scene | 対象語 | 判定 | audio |
|---:|---:|---|---|---|---|
| 1 | 006 | SCENE-002 | 開く／開ける | HUMAN_APPROVED | 既存segment audioをreuse |
| 2 | 007 | SCENE-003 | 上 | HUMAN_APPROVED | 既存segment audioをreuse |
| 3 | 023 | SCENE-009 | 開く／開ける | HUMAN_APPROVED | 既存segment audioをreuse |
| 4 | 030 | SCENE-011 | 上 | HUMAN_APPROVED | 既存segment audioをreuse |
| 5 | 030 | SCENE-011 | 下 | HUMAN_APPROVED | 既存segment audioをreuse |
| 6 | 031 | SCENE-011 | 下 | HUMAN_APPROVED | 既存segment audioをreuse |
| 7 | 032 | SCENE-011 | 下 | HUMAN_APPROVED | 既存segment audioをreuse |
| 8 | 073 | SCENE-024 | 上 | HUMAN_APPROVED | 既存segment audioをreuse |

## 優先順位と不変条件

- `human_audio_override`: なし
- human-approved dictionary: 既存設定を維持
- context-specific human approval: 上記8件のみ追加
- automatic VOICEVOX regeneration: 0
- 表示字幕: 数字・英字・漢字の表示を変更しない
- 古い `review=9` / `queries=0/74` reportはstaleとしてcanonical判定に使用しない

## Canonical result

- Query count: `74/74`
- REVIEW: `0`
- FAIL: `0`
- Human-approved: `8`
- `work/pronunciation_preflight.md`を最新canonical reportとして更新する。
