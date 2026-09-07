# YouTube OAuth恒久運用

この文書は、`scripts/publish_youtube.py`のOAuth動作と、再認証が必要になった場合の確認手順を記録します。対象のcanonical fileは次です。

```text
local/youtube/client_secret.json
local/youtube/token.json
```

## 現行実装の監査結果

2026-09-07に秘密値を表示しない方法で確認した結果、現在の`client_secret.json`はInstalled/Desktop型です。token.jsonにはrefresh tokenがあり、token.json側のclient IDとclient_secret.json側のclient IDは一致していました。現在のscopeは次の2つです。

- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube.force-ssl`

変更前の実装では、保存済みCredentialsを読み、`expired`のときにrefreshし、refresh失敗時はブラウザを開かず停止していました。一方、失敗は`RefreshError`という例外クラス名までしか記録せず、`invalid_grant`、`invalid_client`、network、timeoutの区別ができませんでした。また、token.jsonの保存は通常の直接書き込みで、refresh token保持とatomic writeがコード上で明示されていませんでした。

今回の実装では、次を固定しました。

- access tokenの期限切れ・5分以内の期限接近は、保存済みrefresh tokenで自動refreshする。
- 通常のpublish / auth-checkではブラウザを開かない。token.json未存在、refresh token未存在、refresh失敗時も停止する。
- `invalid_grant`、`invalid_client`、network、timeout、otherを分類する。`invalid_grant`は`AUTH_REAUTH_REQUIRED`として扱う。
- Googleのrefresh応答に新しいrefresh tokenが含まれない場合、古いrefresh tokenを必ず保持する。
- refresh成功後のtoken.json保存は、flush・fsync・close後にreplaceするatomic writeとする。refresh失敗時はcanonical token.jsonを変更しない。
- 新しいrefresh tokenが取得されたときだけ、直前のtoken.jsonを`local/youtube/backups/`へtimestamp付きで1世代保存する。
- token.jsonとclient_secret.jsonのclient IDが両方読める場合は比較し、不一致なら`AUTH_CLIENT_MISMATCH`で停止する。自動再認証や自動上書きはしない。
- OAuth診断は`work/youtube_auth/auth_check.json`、通常のupload前診断はepisodeごとの`work/youtube_publish/auth_preflight.json`へ、秘密値を除いて保存する。

## 認証診断

uploadを伴わない診断は次で実行します。

```powershell
python scripts/publish_youtube.py --auth-check
```

診断は次の順で実行します。

1. client_secret.jsonの存在・形式を確認
2. token.jsonとrefresh tokenを確認
3. access tokenが期限切れまたは期限間近なら自動refresh
4. `channels.list(part="id,snippet", mine=True)`をread-onlyで実行
5. 人間承認済みchannel guardを確認

成功時は、token値やclient secretを表示せず、`AUTH_HEALTH=PASS`と`upload: 0`を表示します。`channels.list`が成功しても、登録対象channelのguardが不一致または未承認なら失敗です。

失敗時の主な分類は次です。

| error_class | 扱い |
| --- | --- |
| `invalid_grant` | `AUTH_REAUTH_REQUIRED`。refresh tokenの期限切れ・失効を示す候補。ブラウザは自動起動しない |
| `invalid_client` | `AUTH_CLIENT_INVALID`。client secret / Google Cloud側設定を確認して停止 |
| `network` | `AUTH_NETWORK_ERROR`。通信を確認して停止 |
| `timeout` | `AUTH_TIMEOUT`。通信を確認して停止 |
| `other` | `AUTH_REFRESH_FAILED`。詳細を秘密値なしで診断して停止 |
| client ID不一致 | `AUTH_CLIENT_MISMATCH`。自動再認証しない |

`invalid_grant`の場合の明示再認証コマンドは次です。

```powershell
python scripts/publish_youtube.py --auth-check --force-reauth
```

`--force-reauth`を付けたときだけInstalledAppFlowを起動し、`access_type="offline"`と`prompt="consent"`を指定します。通常のrefreshでは`prompt="consent"`を使いません。再認証が成功して新しいrefresh tokenが取得できた場合だけ、既存tokenをbackupしてからcanonical token.jsonをatomicに更新します。

## Google Cloud側の恒久設定

コードからGoogle CloudのPublishing statusを推測することはできません。人間がGoogle Cloud Consoleで次を確認してください。

```text
Google Cloud Console
  → Google Auth Platform
  → Audience
  → Publishing status
```

`Testing`では、test userの認可が7日で期限切れになり、offline accessで取得したrefresh tokenも期限切れになります。長期運用では、必要な確認・verificationを満たしたうえで`In production`へ変更することを推奨します。現在のprojectがTestingかどうか、また変更の可否はこのリポジトリやコードから確認できないため、人間確認が必要です。

公式仕様:

- [Google Cloud Help — Manage App Audience](https://support.google.com/cloud/answer/15549945?hl=en): Testing / In productionと7日間の認可・refresh tokenの扱い
- [Google OAuth 2.0 — Web server applications](https://developers.google.com/identity/protocols/oauth2/web-server): `access_type=offline`、`prompt=consent`、access token refresh
- [Google OAuth 2.0 — Installed apps](https://developers.google.com/identity/protocols/oauth2/native-app): Desktop / installed appのOAuth

## upload前の順序

通常のprivate / scheduled uploadは、次の順序で進みます。

```text
OAuth health
  ↓
channels.list + channel guard
  ↓
metadata / final / thumbnail / human gate validation
  ↓
人間の最終確認
  ↓
videos.insert
```

OAuthが壊れている状態でresumable upload sessionを作成しません。`--auth-check`とこの作業ではupload、publish、scheduleを実行しません。

## 今回の失敗の原因候補

今回、変更前の実行ログから確定できたのは`RefreshError`までです。旧実装がGoogleのエラー内容を保存・分類していなかったため、今回の実errorが`invalid_grant`だったかは後追いで断定できません。

候補は、Testingによる短期失効、Google側でのrefresh token失効・取り消し、client設定不一致、または通信系エラーです。Google CloudのPublishing statusはコードから確認できないため、人間確認待ちです。次回の`--auth-check`では、秘密情報を出さずに分類結果を記録します。

