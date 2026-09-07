# Episode 011 Phase B draft_v1 measurements

確認日：2026-09-06

## 冒頭の実測

| 確認項目 | 根拠 | 実測 | 判定 |
|---|---|---:|---|
| problem scene | segment 001 speech | 0.000〜4.885秒 | PASS |
| first safe action | segment 002開始 | 5.005秒 | PASS（12秒以内） |
| official answer | segment 003開始 | 8.389秒 | PASS（15秒以内） |
| official source scene | SCENE-003 / segment 006開始 | 25.485秒 | PASS |
| 3つの行動一覧 | segment 005 / SCENE-004開始 | 19.461秒 | PASS（35秒以内） |

VOICEVOXのsegment WAV尺に、各segmentの`pause_after`を加えた連結タイムラインを正本とする。字幕も同じタイムラインから生成した。

## 中盤CTA

- 挿入回数：1回
- 対象：SCENE-019 / segment 013
- 開始：68.822秒
- 音声終了：75.318秒
- 本編復帰：75.518秒（pause 0.200秒を含む）
- 音声実測：6.496秒
- 上限：7.000秒
- 判定：PASS
- 疑似subscribe UI：0

## 終了CTA

- 開始：239.611秒
- CTA枠：15.000秒
- Episode010実使用CTA音声：11.456秒
- 音声後の余白：3.544秒
- canonical text：`スマホやパソコンの「これ、どうすればいい？」を、公式情報で分かりやすく確認しています。次に困ったときのために、チャンネル登録しておいてください。`
- 判定：Episode010 draft_v1実使用の画面・音声・文言を再利用してPASS

## draft_v1仕様

- 本編音声：239.611秒
- 期待全体尺：254.611秒
- FFmpeg probe実測：254.610秒
- 映像：H.264 / 1920×1080 / 30fps
- 音声：AAC / 48kHz / mono
- scene：19
- narration：39 segment
- subtitles：39 cue
- 出力：`output/draft_v1.mp4`

## 人間確認待ち

全編視聴で、発音・数字の聞き取り、SCENE-003の視認性、字幕同期、CTAの流れ、非写実AI概念画のAI disclosure要否を確認する。thumbnail、final、upload、scheduleはこの確認後に進める。
