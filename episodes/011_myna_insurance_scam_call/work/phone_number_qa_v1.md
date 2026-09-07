# Episode 011 phone-number QA

確認日：2026-09-06

## 対象

| 表示 | Scene / segment | 用途 | 機械確認 |
|---|---|---|---|
| `0120-95-0178` | SCENE-013 / segment 024、033 | マイナンバー総合フリーダイヤル | PASS |
| `#9110` | SCENE-014 / segment 027、028、035 | 警察相談専用電話 | PASS |
| `110` | SCENE-015 / segment 029、030、035 | 緊急時の警察通報 | PASS |
| `5番` | SCENE-013 / segment 025 | 健康保険証利用登録の問い合わせメニュー | PASS |

## 確認結果

- 表示字幕へ読み仮名・音声用表記が流出：0
- subtitle `tts_reading_leakage`：PASS
- VOICEVOX pronunciation preflight：PASS（39/39、REVIEW 0）
- 数字・記号を含む字幕cue：正本の表示文字列と一致
- 出典：デジタル庁・警察庁の確認済みURLを`source_or_prompt`と`sources.md`に保持

人間の全編視聴時に、`0120-95-0178`、`#9110`、`110`、`5番`の聞き取りを最終確認する。
