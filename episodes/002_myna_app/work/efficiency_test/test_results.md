# Episode 002 efficiency test

実行日: 2026-08-31

## 入力

- episodes/002_myna_app/episode.json
- 既存のEpisode 002のscript / scene plan / subtitle plan / timeline plan / VOICEVOX manifest

既存の output/final.mp4、output/draft_v4.mp4、既存音声、既存字幕、公式素材は再生成・上書きしていない。

## 結果

| 検査 | 結果 |
|---|---|
| episode.json契約 | PASS |
| schema相当の参照検査 | PASS |
| scene renderer | PASS: 35 / 35 scene |
| 画像サイズ | PASS: 1920 x 1080 |
| 公式素材 | PASS: 欠落0、宣言22件 |
| contact sheet | PASS |
| VOICEVOX /audio_query | PASS: 80 / 80 |
| pronunciation dictionary | 変更なし |
| pronunciation preflight | REVIEW: 5件 |
| subtitle preflight | FAIL: 1件 / WARN: 2件 |
| production preflight | FAIL（字幕FAIL、発音REVIEWを検出） |
| pipeline unit tests | PASS: 4 tests |

## pronunciation preflight

人間承認済みの指定・辞書一致は7件をPASSとした。

REVIEW候補は、今日 が2件、文脈依存の 開く/開ける 系が3件。VOICEVOXの読みを取得したうえで、辞書の自動登録は行っていない。

## subtitle preflight

- FAIL: SUB-042 の2行目が72px実測で安全幅1800pxを超過。
- WARN: SUB-087 と SUB-092 は2行の長さのバランスが小さい。

既存Episode 002は字幕確認済みの完成版であるため、今回のテストでは字幕本文や動画を変更せず、次回の字幕確定時に確認すべき改善点として残した。

## renderer方式

HTML/CSSテンプレートを第一候補として実装し、Edge/ChromiumのヘッドレスPNG化を試行する。今回の環境ではEdgeのヘッドレス呼び出しが利用できなかったため、同じepisode.jsonをPillowフォールバックで35枚生成した。

出力:

- scene_001.png 〜 scene_035.png
- scene_contact_sheet.png
