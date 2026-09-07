# Episode 012 YouTube auth preflight

- credential path: `C:\Codex\260829_youtube-anshin\local\youtube\token.json`
- token exists: `true`
- refresh token present: `true`
- expiry before test: `2026-09-05T23:51:11Z` / expired: `true`
- scopes: `youtube.upload`, `youtube.force-ssl`（010/011の公開経路と一致）
- token last write: `2026-09-06 08:05:47 JST`。Episode011の最終AI開示確認直後で、012開始時の更新ではない。
- restricted run refresh: `TransportError`
- real-network read-only refresh: `PASS`
- credentials valid after refresh: `true`
- `channels.list(mine=true)`: `PASS`
- channel guard: `PASS`（`大人のデジタル安心室` / `UCgVRceTJYO5KOrPX4w2jXZw`）
- re-auth performed: `false`
- token deleted: `false`
- read-only testによるtoken上書き: `false`

## Cause

`get_youtube_service()`は既存tokenを読み込み、期限切れならrefreshを試していた。しかしrefresh例外を握りつぶし、`credentials = None`としてブラウザOAuthへ自動フォールバックしていた。今回の最初の012実行では、通常sandboxのネットワーク制限によりrefreshが`TransportError`となり、この分岐に入った。

既存tokenがある場合はrefresh失敗で停止し、ブラウザ再認証は明示的な`--force-reauth`指定時だけ開始するよう`publish_youtube.py`を修正した。今回の実ネットワークrefreshとAPI単体確認では既存tokenが正常に復旧できたため、再OAuthは行わない。
