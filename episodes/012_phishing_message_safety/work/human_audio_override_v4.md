# Episode 012 human audio override v4

確認日: 2026-09-06  
判定: `PASS`

ユーザーが修正した「これ、本物？」の音声を正本として採用した。音声内容は再生成せず、`human_audio_override` としてタイムラインへ組み込んだ。

| 項目 | 結果 |
|---|---|
| Segment | `030` |
| 対象文 | `これ、本物？` |
| canonical | `audio/human_approved/030.wav` |
| 元候補 | `audio/voicevox_kenzaki/segments/030.wav` |
| source | `human_audio_override` |
| SHA-256 | `7B534892A4AC893CC7F1D0D483B67A8A94E690353DB652EA16B0077C3F4C7106` |
| narration SHA-256 | `BF3FC7F9C9CA775F2AA5D26E1D2C343EC4AB1DE1E26D53F82D281918799C138B` |
| 音声 | mono / 24,000Hz / 152,320 frames |
| 元音声実測 | 6.346667秒（timeline 6.347秒） |
| timeline | 213.189–219.536秒、後続pause 0.12秒 |
| 自動再生成 | `false`。v4 build logでも `regenerated=[]` |
| 辞書との優先順位 | human audio overrideを辞書・自動生成より優先 |
| cleanup | `retain_during_cleanup=true` |

`output/draft_v4.mp4` と `output/final.mp4` の両方で同一音声を使用した。030以外の78 segmentは既存音声を再利用し、再生成は0件だった。
