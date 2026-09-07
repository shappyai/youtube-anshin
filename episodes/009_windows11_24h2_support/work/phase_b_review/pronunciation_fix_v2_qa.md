# Episode 009 pronunciation fix v2 QA

- status: **PASS**
- qa: `approved_pronunciation_match`

|語|出現segment数|segment IDs|判定|
|---|---:|---|---|
| 方 | 4 | 001, 006, 011, 038 | PASS |
| Windows | 16 | 001, 002, 004, 005, 008, 009, 014, 020, 022, 023, 025, 037, 039, 047, 049, 050 | PASS |
| Update | 7 | 005, 022, 023, 037, 039, 047, 050 | PASS |
| ID | 1 | 019 | PASS |

## Context rule: 方

- person: segment 001 / 011 → かた
- direction or comparison: segment 006 / 038 → ほう
- global 方 dictionary entry: none

## Approved patterns

- Windows: ウィンドオズ / accent=5（語末ズ）
- Update: アップデエト / accent=6（語末ト）
- ID: アイディイ / accent=3（ディ。表示はIDのまま）

## FAIL

- なし

