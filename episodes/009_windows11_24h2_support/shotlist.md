# Episode 009 shotlist（Phase A）

確認日: 2026-09-05

## 媒体の選択

Windowsの設定を説明するため、基本媒体は「PCのWindows Settings画面」とする。正確なUIはMicrosoft公式の画面素材を優先し、実機画面が必要な場面はWindows 11テストPCで再撮影できるよう `local/capture_windows_settings.ps1` を用意した。現在の制作PCはWindows 10 Pro 24H2なので、実機画面としては使用しない。

|SHOT|Scene|Device|映像・焦点|画面文字の扱い|音声範囲|動き|プライバシー|
|---|---:|---|---|---|---|---|---|
|SHOT-01|001|概念イラスト|Windows 11を確認する前の落ち着いた入口|ImageGenで短い見出しを生成、文字QA必須|1-3|static|人物・UI・ロゴを実在風にしない|
|SHOT-02|002|template|今日確認する3つ|Pillow overlay、headline 88px以上|4-6|static|個人情報なし|
|SHOT-03|003|template|24H2の対象範囲と日付|日付と対象エディションを大きく、出典は短形|7-11|static|個人情報なし|
|SHOT-04|004|template|スタート右クリックからの道順|3手順をカードで表示|12-14|static|個人情報なし|
|SHOT-05|005|template|エディション / 24H2 / 25H2|英数字tokenを分断しない|15-17|static|個人情報なし|
|SHOT-06|006|公式画面focus v2|左に「設定→システム→バージョン情報」のstep、右に大きな公式focus crop|右の「バージョン情報」だけをhighlight|18-19|very_slow_zoom|採用cropはID・名前・メールを含まない。arrowは1本|
|SHOT-07|007|公式画面focus v2|公式「デバイスの仕様」crop＋説明用の「バージョン（例）」欄|「バージョン（例）」だけをhighlight。実UIの値は改変しない|20-21|very_slow_zoom|値・ID・アカウントを映さない。説明欄はfake Windows UIではない|
|SHOT-08|008|template|2 / 3 Windows Update|セクション扉は正確なoverlay|22-23|static|個人情報なし|
|SHOT-09|009|公式画面focus v2|左に「設定→Windows Update」のstep、右に日本語補助ラベル＋公式「Check for updates」crop|右の更新確認箇所だけをhighlight|24-25|very_slow_zoom|採用素材に個人情報なし。UI文字は書き換えない|
|SHOT-10|010|template|25H2が表示されたら保存・再起動|手順を大きく表示|26-28|static|個人情報なし|
|SHOT-11|011|template|25H2が表示されないときの注意|blockアイコンをsemantic SVGで表示|29-33|static|個人情報なし|
|SHOT-12|012|template|3 / 3と26H1の位置づけ|26H1を既存PCの更新先として描かない|34-37|static|個人情報なし|
|SHOT-13|013|template|24H2は25H2を確認|淡いcompare／手順、矢印は説明用|38-40|static|個人情報なし|
|SHOT-14|014|template|公式サポート・メーカー・管理者へ相談|support_agentを使用|41-42|static|個人情報なし|
|SHOT-15|015|概念イラスト|慌てて買い替えず、まず確認|ImageGen native、短文の文字QA|43-46|very_slow_zoom|PC・人物を不安商法風にしない|
|SHOT-16|016|template|まずバージョン→Windows Update|2段階をcompareで正確に表示|47|static|個人情報なし|
|SHOT-17|017|template|まとめの導入|1つ目を大きく表示|48-49|static|個人情報なし|
|SHOT-18|018|template|2つ目・3つ目|まとめカード、最小56pxを維持|50-51|static|個人情報なし|
|SHOT-19|019|概念イラスト|まずバージョンを確認して相談へ|ImageGen native、短文の文字QA|52|very_slow_zoom|UI・ロゴ・人物の個人情報なし|

## 実機capture手順

1. Windows 11テストPCで `local/capture_windows_settings.ps1 -Page about` または `-Page update` を実行する。
2. 原画は `work/windows_capture/` に保存し、個人名、メール、デバイスID、プロダクトIDを確認する。
3. 必要な部分だけをcrop・マスキングし、`assets/official/`へコピーする。
4. `sources.md`、`media_manifest.csv`、`qc.md`に撮影日と採用範囲を追記する。

現在の制作PCでの実行結果は `blocked` とし、Windows 11の画面として採用しない。
