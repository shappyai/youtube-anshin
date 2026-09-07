# Short001 real ChatGPT answer capture QA — v8

- 発見：YES
- canonical source：`shorts/work/ChatGPT Voice画面録画.MP4`
- 確認範囲：14.200〜17.000秒（元captureの12.8秒以降）
- 実際に表示された回答の冒頭：`もちろんです！キャベツだけでも、かなり簡単に作れます。`
- 料理名：`いちばん簡単「キャベツの塩昆布炒め」`
- 採用方法：元captureのpixelをcrop / resize。回答の書き直し・合成・UI改変は0。
- 動画内timestamp：20.256〜22.806秒（2.550秒）
- 見せる範囲：回答冒頭から料理名・材料が見える箇所。全文は読ませない。
- 字幕：`ちゃんと答えが返ってきた` の2行のみ。大きな説明見出しの後乗せなし。
- machine response audio：使用しない。Dictationの実録音声入力だけを使用。

## Required flags

| flag | result |
|---|---|
| real ChatGPT answer | PASS |
| crop / resize only | PASS |
| answer rewrite | 0 |
| fake UI | 0 |
| AI UI reconstruction | 0 |
| Voice / Dictation confusion | 0 |
