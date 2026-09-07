# Short001 capture audio QA — v7

- source：`shorts/work/ChatGPT Voice画面録画.MP4`
- selected interval：3.800〜12.800秒（9.000秒）
- capture audio use：YES
- machine response audio use：NO。今回の主題はDictationで、返答音声を聞かせる構成ではない。

## Before / after

| 項目 | before | after | 判定 |
|---|---:|---:|---|
| duration | 9.000s | 9.000s | PASS |
| RMS | -21.42 dBFS | -28.36 dBFS | natural level adjustment |
| peak | -0.96 dBFS | -7.93 dBFS | no clipping |
| clipped samples | 0 | 0 | PASS |
| near-silence ratio | 0.6305 | 0.6671 | speech / pause separation visible |

## Checks

- clipping：PASS。選択区間のbefore/afterともクリップ判定サンプル0。
- hum / hiss / sudden noise：PASS候補。静かな区間のRMSが低く、強い連続ノイズは音量計測上確認されない。
- intelligibility：PASS_WITH_HUMAN_LISTENING。話している区間と静かな区間が明確に分かれ、最終の自然さは人間Draft Gateで聴取する。
- user voice：captureの話者音声を残し、不自然なmuteや強いgateは行っていない。
- VOICEVOXとのバランス：captureだけを約−6.9dB下げ、VOICEVOXと同じ音量へ強制していない。
- processing：70Hz high-pass＋volume 0.45のみ。denoise、gate、強いcompressorは不使用。

## Decision

- capture音声をv7 draftへ採用する。実録音声の上にVOICEVOX narrationを重ねない。
- `audio/segments_manifest_v7.csv` と `audio/narration_v7.wav` に採用区間を記録した。
