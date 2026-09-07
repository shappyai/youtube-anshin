# Short001 capture audio QA — v8

- source：`shorts/work/ChatGPT Voice画面録画.MP4`
- Dictation input audio：3.800〜12.800秒（9.000秒）を採用
- ChatGPT answer visual：14.200〜17.000秒。音声は追加しない
- capture audio use：YES（音声入力中のユーザー音声のみ）
- machine response audio use：NO。今回の主題はDictationで、回答画面のテキストを見せる。

## Before / after

| 項目 | before | after | 判定 |
|---|---:|---:|---|
| duration | 9.000s | 9.000s | PASS |
| RMS | -21.42 dBFS | -28.36 dBFS | natural level adjustment |
| peak | -0.96 dBFS | -7.93 dBFS | no clipping |
| clipped samples | 0 | 0 | PASS |
| near-silence ratio | 0.6305 | 0.6671 | speech / pause separation visible |

## Decision

- Dictation入力区間の実録音声をv8へ採用する。実回答sceneへVOICEVOXや機械返答音声を重ねない。
- 処理は70Hz high-passとvolume 0.45だけ。強いdenoise / gate / compressorは不使用。
- 最終的な聞き取りやすさは人間Draft Gateで確認する。
