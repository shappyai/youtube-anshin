# Codex prompt cookbook

このファイルは、毎回の依頼を短くするための実用プロンプト集です。Codexは必ず `AGENTS.md` を優先してください。

## A. 初回だけ — リポジトリ監査

```text
AGENTS.md、README.md、QUICKSTART.md、config/、scripts/、episodes/001_google_security を読んで。
このYouTube制作OSがWindows/macOSで動くか監査し、壊れているスクリプトがあればテスト付きで直して。
APIキーが必要な処理は実行せず、dry-runで確認して。
最後に「私が次にやること」を3つ以内で教えて。
```

## B. 1本目を仕上げる

```text
AGENTS.mdを守って episodes/001_google_security を公開候補まで進めて。
1) sources.mdを最新のGoogle公式情報で再確認
2) 事実に不足があれば一次情報を追加
3) script.mdを8〜12分で自然な日本語に修正
4) SHOTタグとshotlist.mdを同期
5) 私がスマホで撮る映像だけを撮影順にまとめる
競合動画の文章コピーは禁止。画面名称は撮影日時点で再確認する前提にして。
```

## C. 実機素材を置いた後

```text
episodes/001_google_security/raw/ を確認し、shotlist.mdと照合して。
ファイルを削除せず、media_manifest.csvを更新して、不足素材だけ列挙して。
不足がなければ、次にTTS→字幕→draft.mp4生成まで進められる状態にして。
```

## D. TTS・編集を実行

```text
001のscript.mdが承認済み、raw素材も揃った前提で進めて。
OPENAI_API_KEYの値自体は表示しないこと。
scripts/tts.py → make_captions.py → build_video.py を必要に応じて修正・実行し、draft.mp4を作成して。
失敗したら原因を直して再実行。素材そのものは破壊しない。
```

## E. 公開前レビュー

```text
001について sources.md / script.md / shotlist.md / captions.srt / draft.mp4 / publish.json をレビューして。
fact / language / visual / audio / policy / privacy に分け、重大・中・軽微でqc.mdを更新。
重大0件になるまで、自動修正できるものは修正して。
事実判断や見た目の好みだけ私に残して。
```

## F. サムネ・タイトル

```text
001の内容からタイトル5案とサムネ3案を作って。
競合の勝ち筋（危険、変更、誤解解消）は参考にしてよいが、内容以上に煽らない。
サムネ文字は2〜6語、タイトルと同文にしない。
既存thumbnailを上書きせず新しい案として出して。
```

## G. 2本目の企画

```text
data/competitors.csv、1本目のreview.md（あれば）、直近の公式情報を使って次候補を10件出して。
需要30%、競合余地20%、長寿命15%、実機の見せやすさ15%、ブランド適合20%で採点。
上位3件だけ理由を詳しく。競合タイトルの言い換えは禁止。
```

## H. 7日後の改善

```text
data/analytics/ にあるYouTube Studio CSVを読み、最新動画を過去動画と比較して。
CTR、最初30秒、平均視聴率、ブラウジング/検索、1000再生あたり登録の順で診断。
次の動画で検証する改善仮説は1個だけ選ぶ。複数同時に変えない。
review.mdと次候補CSVを作って。
```
