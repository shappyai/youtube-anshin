# YouTube OAuth初期設定（初心者向け）

この手順は、YouTubeチャンネル「大人のデジタル安心室」を管理しているGoogleアカウントで、初回だけ行います。パスワードをリポジトリやスクリプトへ入力・保存することはありません。ブラウザのGoogleログイン画面で人間がアカウントを選びます。

## 1. Google Cloudで準備

1. [Google Cloud Console](https://console.cloud.google.com/)で既存projectを選ぶか、新しいprojectを作成します。
2. API Libraryで **YouTube Data API v3** を有効にします。
3. OAuth consent screenを設定します。画面の案内に従ってアプリ名、連絡先、必要なscope、必要ならテストユーザーを設定してください。
4. OAuth Client IDを作成し、Application typeは **Desktop app** を選びます。
5. client secret JSONをダウンロードします。

詳細は[YouTube Data APIの認証ガイド](https://developers.google.com/youtube/v3/guides/authentication)と[Installed app / desktop OAuth](https://developers.google.com/youtube/v3/guides/auth/installed-apps)を参照してください。

## 2. 秘密ファイルを配置

リポジトリ直下で、次の場所へファイルを置きます。

```text
local/youtube/client_secret.json
```

この場所はGit対象外です。`client_secret.json`の中身をチャット、ログ、issue、commitへ貼り付けないでください。

## 3. Python依存をインストール

仮想環境を有効にしたPowerShellで実行します。

```powershell
python -m pip install -r requirements-youtube.txt
```

このprojectでは、公式Python clientのほか、OAuth、画像検証に必要な依存だけを指定しています。

## 4. チャンネルを一度確認

```powershell
python scripts/publish_youtube.py --verify-channel --force-reauth
```

初回は`--force-reauth`を明示してブラウザを開きます。テスト用ではなく、実際に「大人のデジタル安心室」を管理しているGoogleアカウントを選びます。画面とコンソールに表示されたチャンネル名・Channel IDを人間が確認してください。承認すると、次が作成されます。

```text
local/youtube/channel_config.json
```

このファイルには承認済みChannel IDとチャンネル名だけを保存します。OAuth tokenは別に保存され、どちらもGit管理しません。

## 5. 初回upload前の確認

まず、APIを呼ばないdry-runを実行します。

```powershell
python scripts/publish_youtube.py 003 --private --dry-run
```

タイトル、descriptionのbyte数、tags、finalのSHA-256、thumbnail、privacy、予定されるAPI requestが表示されます。dry-runはOAuthを開始せず、動画をuploadしません。

人間が内容を確認した後だけ、非公開uploadを実行します。

```powershell
python scripts/publish_youtube.py 003 --private
```

実行時には最終確認が表示され、既定では`N`で停止します。`--yes`を付けた場合だけ、この確認を省略できます。

## 保存されるファイル

```text
local/youtube/client_secret.json  # Google Cloudから取得。秘密。
local/youtube/token.json          # 初回OAuth後のrefresh token。秘密。
local/youtube/channel_config.json # 人間承認済みChannel ID。秘密情報は含めない。
```

tokenは次回以降のrefreshに使います。token失効、scope変更、別アカウントで認証したい場合は、必要に応じて次のように再認証します。

```powershell
python scripts/publish_youtube.py --auth-check --force-reauth
```

通常の状態確認はuploadを行わない次のコマンドです。

```powershell
python scripts/publish_youtube.py --auth-check
```

通常のpublishや`--auth-check`でブラウザは自動起動しません。access tokenの期限切れはrefresh tokenで自動更新し、refresh tokenが失効している場合だけ`--force-reauth`を人間が明示します。詳細は[YouTube OAuth恒久運用](youtube_oauth.md)を参照してください。

## よくある停止理由

- `OAuth client secret is missing`: `client_secret.json`を指定場所へ置く。
- `client libraries are not installed`: `requirements-youtube.txt`をインストールする。
- `Channel ID is not approved yet`: `--verify-channel`で表示内容を人間確認して保存する。
- `channel ID mismatch`: 別Googleアカウント、別チャンネルでログインしていないか確認する。自動で上書きしない。
- `AUTH_REAUTH_REQUIRED`: refresh tokenが期限切れまたは失効している可能性がある。Google Auth PlatformのPublishing statusを確認し、人間確認後に`python scripts/publish_youtube.py --auth-check --force-reauth`を実行する。
- `AUTH_CLIENT_MISMATCH`: token.jsonとclient_secret.jsonが別OAuth client。ファイルを混ぜず、Google Cloud側のclientを人間が確認する。自動再認証しない。
- `Final QA` / `human approved` gate: final化と人間承認記録を先に完了する。
- `Thumbnail missing`: 標準保存先`episodes/NNN_slug/assets/thumbnail/thumbnail.png`へ配置する。Episode 003は既存`output/thumbnail.png`も候補として扱う。
- 未監査projectによるprivate制限: 公式仕様を確認し、必要な監査やStudioでの人間操作を行う。publicへの自動fallbackはしない。

## セキュリティ上の注意

- パスワード、client secret、access token、refresh tokenをスクリプト引数に渡さない。
- `local/youtube/*.json`をcommitしない。
- ログにはOAuth内容を保存しない。
- 即時public、動画削除、privateからpublicへの自動昇格はこのツールにない。
- 実upload前に必ずdry-runと完成動画を人間が確認する。
