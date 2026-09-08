# Episode015 音声・字幕修正 v4 専用確認

確認日: 2026-09-08

## A. セクション番号

- viewer-facing対象（`script.md`、`episode.json`、`publish.json`、`captions.srt`、`captions.ass`）を確認。
- `1 / 3`、`2 / 3`、`3 / 3`、`1/3`、`2/3`、`3/3` の残存数: **0**。
- SEG-007 / 016 / 026、字幕SUB-008 / 021 / 038、section headingは、それぞれ `1` / `2` / `3` に統一。
- 内部scene IDは変更していない。

## B. 「セキュリティ」の読み

- TTS入力で適用されたsegment: SEG-008、030、039。
- TTS入力は `セキュリティー`。表示字幕・表示UIの `セキュリティ` は変更していない。

## C. 「何で本人確認」の読み

- SEG-010だけに `reading_overrides` を設定。
- 表示字幕・canonical narrationは `何で本人確認` のまま。
- VOICEVOX入力は `なにで本人確認`。
- 共通辞書へ単独の `何で` は登録していない。

## D. 「バックアップ コード」のaudio_query

対象segment: SEG-017、018、020、024、025。

| segment | audio_query内のengine mora列 | compound内のpause / phrase break |
|---:|---|---|
| 017 | `バックアップコオドワ` | compound全体が1 accent phrase。内部breakなし（phrase後のpauseは「は」の前） |
| 018 | `バックアップコオド` | compound全体が1 accent phrase。内部breakなし（phrase後のpause） |
| 020 | `バックアップコオドワ` | compound全体が1 accent phrase。内部breakなし |
| 024 | `バックアップコオドワ` | compound全体が1 accent phrase。内部breakなし（phrase後のpauseは「は」の前） |
| 025 | `バックアップコオドオ` | compound全体が1 accent phrase。内部breakなし |

VOICEVOXの長音はengine上で `コード` が `コオド` と表現される。`pause_mora` があるsegmentでも、compoundの後ろにあるもので、`バックアップ` と `コード` の間にはない。アクセント形は変更していない。

## E. 「セキュリティ キー」のaudio_query

対象segment: SEG-030、039。

| segment | audio_query内のengine mora列 | compound内のpause / phrase break |
|---:|---|---|
| 030 | `セキュリティイキイ` | compound全体が1 accent phrase。内部breakなし（phrase後のpause） |
| 039 | `セキュリティイキイ` | compound全体が1 accent phrase。内部breakなし |

VOICEVOXの長音はengine上で `セキュリティーキー` が `セキュリティイキイ` と表現される。アクセント位置は変更していない。

## 再計算

- main narration audio timing: `300.356秒`
- full draftのQA基準timeline: `313.356秒`
- container probe: `312.920秒`（30fps/AAC mux後の実ファイル表示値）
- 変更segment以降を実音声尺から再計算し、字幕61 cueを再生成した。
