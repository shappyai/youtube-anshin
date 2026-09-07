# QUICKSTART — 1本目を作る

## 0. 事前確認
```bash
python scripts/doctor.py
```
`codex`, `git`, `python`, `ffmpeg` が見つかればOKです。

## 1. Codexでリサーチと台本を仕上げる
リポジトリ直下で `codex` を起動し、次を依頼します。

```text
AGENTS.mdを守って、episodes/001_google_security を1本目として完成させたい。
まずsources.mdのURLと2026年8月29日時点の公式情報を確認して、不足があれば一次情報を追加。
その後script.mdを8〜12分に整え、各実機操作に[SHOT-XX]を付け、shotlist.mdを更新して。
競合動画の文章はコピーしないで。
```

## 2. 自分で実機録画
Codexが更新した `shotlist.md` の順に録ります。

素材は `episodes/001_google_security/raw/` に入れます。
例：
- `shot_01_security_checkup.mp4`
- `shot_02_recovery.mp4`
- `shot_03_2step.mp4`

個人メールアドレスや通知が映らないようにしてください。

## 3. 素材検品をCodexに依頼
```text
raw/の動画をshotlist.mdと照合して、不足素材を一覧化して。
問題なければmedia_manifest.csvを更新して。
ファイルは削除しないで。
```

## 4. TTS
`.env` に `OPENAI_API_KEY` を入れたら：
```bash
python scripts/tts.py episodes/001_google_security
```
APIをまだ使わない場合は、この工程を後回しにしてもOKです。

## 5. 字幕
```bash
python scripts/make_captions.py episodes/001_google_security --duration 600
```
音声完成後は実尺に合わせてCodexに調整させます。

## 6. サムネ
```bash
python scripts/make_thumbnail.py episodes/001_google_security --text "Google 5項目"
```
`thumbnail/` に3案出ます。

## 7. 編集
`raw/` に素材、`audio/narration.mp3` ができたら：
```bash
python scripts/build_video.py episodes/001_google_security
```

## 8. QC
```bash
python scripts/qc_episode.py episodes/001_google_security
```
さらにCodexへ：
```text
qc.mdとdraft.mp4を確認し、fact / language / visual / audio / policy / privacy の重大指摘を0件にして。
自動修正できるものは直して。事実判断が必要なものは私に残して。
```

## 9. 投稿セット
```bash
python scripts/youtube_metadata.py episodes/001_google_security
```
`publish.json` を確認した後、自動化を使う場合も、まずAPIを呼ばないdry-runを実行します。
```powershell
python scripts/publish_youtube.py 003 --private --dry-run
```
実uploadは人間確認後にprivateまたはfuture scheduledだけを選びます。OAuth初期設定とgateは `docs/youtube_oauth_setup.md` / `docs/youtube_publish_automation.md` を参照してください。即時publicと削除は自動化していません。

## 10. 7日後
YouTube StudioからAnalytics CSVを `data/analytics/` に保存し、Codexへ：
```text
最新動画と過去動画を比較し、CTR・最初30秒・平均視聴率・流入元・登録転換を分析。
次の1本で検証する改善仮説を1個だけ決めて。
```
