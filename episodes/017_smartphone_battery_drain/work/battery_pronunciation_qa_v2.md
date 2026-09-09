# Episode017 バッテリー発音QA

- result: PASS
- 標準辞書の同一surface登録数: 1（期待値: 1）
- VOICEVOX実audio_query mora: バ・ッ・テ・リ・イ（5モーラ）
- accent: 4（表示上の最後の「リ」に対応する4モーラ目）
- pitch shape: low_high_plateau（「リ」を含む語末を高域で保持）
- 対象segment: 002, 005, 006, 007, 022, 023, 025, 027, 029, 031

## Segment別

| Segment | mora | accent | リ peak | 長音相当イも高域 | 判定 |
|---:|---|---:|---|---|---|
| 002 | バ・ッ・テ・リ・イ | 4 | PASS | PASS | PASS |
| 005 | バ・ッ・テ・リ・イ | 4 | PASS | PASS | PASS |
| 006 | バ・ッ・テ・リ・イ | 4 | PASS | PASS | PASS |
| 007 | バ・ッ・テ・リ・イ | 4 | PASS | PASS | PASS |
| 022 | バ・ッ・テ・リ・イ | 4 | PASS | PASS | PASS |
| 023 | バ・ッ・テ・リ・イ | 4 | PASS | PASS | PASS |
| 025 | バ・ッ・テ・リ・イ | 4 | PASS | PASS | PASS |
| 027 | バ・ッ・テ・リ・イ | 4 | PASS | PASS | PASS |
| 029 | バ・ッ・テ・リ・イ | 4 | PASS | PASS | PASS |
| 031 | バ・ッ・テ・リ・イ | 4 | PASS | PASS | PASS |

## 辞書登録

```yaml
surface: バッテリー
reading: バッテリー
engine_reading: バッテリイ
accent: 4
pitch_shape: low_high_plateau
human_approved: true
global: true
```

VOICEVOX audio_queryでは表記上の長音「ー」が末尾の「イ」として返る。4モーラ目の「リ」をaccent=4の核にし、low_high_plateauで5モーラ目まで高域を保持する。
