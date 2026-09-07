# 大人のデジタル安心室 — YouTube Production OS

Codexを中心に、**企画 → 一次情報調査 → 台本 → 実機録画 → TTS → 字幕 → FFmpeg編集 → サムネ → QC → 公開 → 分析**を回すためのスターターリポジトリです。

## 最初にやること

### Windows PowerShell
```powershell
cd C:\path\to\youtube-anshin
if (!(Test-Path .git)) { git init }
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
python scripts\doctor.py
codex
```

### macOS / Linux
```bash
cd /path/to/youtube-anshin
[ -d .git ] || git init
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
python scripts/doctor.py
codex
```

Codexを起動したら最初にこれを依頼します。

```text
AGENTS.md と QUICKSTART.md を読んで、このプロジェクトの目的と現在の状態を確認して。
episodes/001_google_security を1本目として、sources.mdの一次情報を再確認し、script.mdとshotlist.mdを公開品質まで仕上げて。
ファイルを変更したら、何を変えたかと私が次にやる実機録画だけを簡潔に教えて。
```

## 重要
**最初から完全自動化しません。** まず3本を同じ型で完成させます。

人間に残すのは基本3つです。
1. 企画の最終決定
2. スマホ実機の画面録画
3. 完成動画の公開前確認

それ以外を順次Codexに寄せます。

## 主要コマンド
```bash
# 環境診断
python scripts/doctor.py

# 新しい動画フォルダ作成
python scripts/new_episode.py --number 2 --slug line_rumor --title "LINEの噂を公式情報と実機で検証"

# 一次情報ファイルを機械チェック
python scripts/check_sources.py episodes/001_google_security

# 仮字幕生成（TTS音声がまだなくても可）
python scripts/make_captions.py episodes/001_google_security --duration 600

# サムネ3案生成
python scripts/make_thumbnail.py episodes/001_google_security --text "Google 5項目"

# 自動QC
python scripts/qc_episode.py episodes/001_google_security

# TTS（OPENAI_API_KEY設定後）
python scripts/tts.py episodes/001_google_security

# 素材を置いた後に動画を組む
python scripts/build_video.py episodes/001_google_security

# 投稿用JSONを生成
python scripts/youtube_metadata.py episodes/001_google_security
```

## YouTube公開（安全なprivate / scheduledのみ）

完成動画を公開する前に、まずAPIを呼ばないdry-runを実行します。

```powershell
python scripts/publish_youtube.py 003 --private --dry-run
```

人間確認後の実upload、OAuth初期設定、チャンネル照合、予約、再試行は次を参照してください。

- `docs/youtube_publish_automation.md`
- `docs/youtube_oauth_setup.md`

このツールは即時public公開と動画削除を実装していません。標準サムネイル保存先は `episodes/NNN_slug/assets/thumbnail/thumbnail.png` です。

## OpenAI TTS
`gpt-4o-mini-tts` を `POST /v1/audio/speech` で呼びます。APIキーは `.env` に保存し、Gitには入れません。

```bash
cp .env.example .env
# .env の OPENAI_API_KEY= を自分のキーで埋める
```

## フォルダ
- `AGENTS.md` — Codexへの恒久ルール
- `config/` — チャンネル/制作設定
- `data/` — 競合・Analytics
- `episodes/` — 1動画1フォルダ
- `templates/` — 各ファイルの雛形
- `scripts/` — 自動化
- `tests/` — 最低限のテスト
- `docs/` — Excel調査資料

## 最初のゴール
**3本公開すること。** 管理画面を作ることではありません。
