# Episode 008 subtitle QA — draft_v1

確認日: 2026-09-05

## 判定

- **機械QA: PASS**
- cue数: 122（narration 63 segment）
- 複数cueへ分割したsegment: 46（追加cue 59）
- 分割方法: 各segmentの境界は実測 narration WAV、segment内のcue境界はVOICEVOX `audio_query` のmora duration

## 可読性・禁則

| 項目 | 結果 |
|---|---:|
| 最小font_px（ASS既定値） | 72px |
| 56px未満 | 0 |
| 3行cue | 0 |
| 安全幅超過 | 0 |
| 固有名詞・保護語の途中分割 | 0 |
| 活用語の不自然分断 | 0 |
| scene側の禁則・語途中分断 | 0 |
| segment内cueの重なり | 0 |
| segment内cueの不要な隙間 | 0 |

`subtitle_preflight.md` の27件のWARN（短い行・cue数上限）は、56px未満や意味分断ではないため記録のみとした。字幕を小さくして押し込む調整は行っていない。

## 代表的な実時間境界

- `SUB-001-1`: 0.000–3.391秒「有名人が、／投資をすすめる広告を見て、」
- `SUB-001-2`: 3.391–5.024秒「LINEに案内されたら。」
- `SUB-004-1`: 13.487–16.122秒「今回は、／お金を振り込む前に、」
- `SUB-004-2`: 16.122–19.385秒「確認したい3つだけ、／やさしく見ていきます。」

成果物: `captions.srt`、`captions.ass`、`work/subtitle_cue_timing.json`、`work/subtitle_qa_draft_v1.json`。
