# Episode 008 pronunciation review — Phase B

確認日: 2026-09-05  
Engine: VOICEVOX `剣崎雌雄 / ノーマル`（speed 1.00 / intonation 1.00 / pitch 0.00）

## 判定

- preview WAV: 12語・12ファイル生成済み
- 本編 audio_query: 63/63 query 完了
- 文脈REVIEW 4件: **PASS**（`上半期`=`カミハンキ`、`今日`=`キョオ`、`行う`=`オコナウ`はいずれも文脈上自然）
- 電話番号: segment単位 `reading_overrides` を適用し、`9110` は「きゅう いち いち まる」、`188` は「いち はち はち」として本編音声を生成
- 発音辞書の追加・変更: **なし**

## preview一覧

| surface | audio_query reading | accent summary | 本編扱い |
|---|---|---|---|
| SNS | エスエヌエス | エスエヌエス(5) | 採用 |
| LINE | ライン | ライン(3) | 採用 |
| FX | エフエックス | エフ(1) / エックス(1) | 採用 |
| #9110 | キュウセンヒャクジュウ | キュウセンヒャクジュウ(3) | 本編はreading_overridesへ切替 |
| 188 | ヒャクハチジュウハチ | ヒャク(2) / ハチジュウ(4) / ハチ(2) | 本編はreading_overridesへ切替 |
| 0570-050588 | ゼロゴオナナゼロゼロゴオゼロゴオハチハチ | 5句 | 表示・ナレーションとも読み上げ表記を採用 |
| 6,566件 | ロクセンゴヒャクロクジュウロッケン | 4句 | 採用 |
| 881億円 | ハッピャクハチジュウイチオクエン | 3句 | 採用 |
| 4億4,000万円 | ヨンオクヨンセンマンエン | 3句 | 採用 |
| 上（上半期） | カミハンキ | 文脈query | PASS |
| 今日 | キョオ | キョオ(1) | PASS |
| 行う | オコナウ | オコナウ(4) | PASS |

関連ファイル: `words.json`、`pronunciation_manifest.csv`、`pronunciation_review_all.wav`、`work/pronunciation_preflight.md`。
