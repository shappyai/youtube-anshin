# YouTube公開自動化

このリポジトリの公開処理は、完成動画を安全にYouTubeへ登録するための補助機能です。即時の`public`公開は実装せず、許可する操作は`private`と将来時刻の`scheduled`だけです。引数を省略した場合も安全側の`private`になります。

実装: `scripts/publish_youtube.py`  
設定: `config/youtube_publish.json`  
OAuth設定手順: `docs/youtube_oauth_setup.md`

## 公式仕様の確認

確認日: 2026-08-31。仕様変更に備え、実upload前にもリンク先を再確認します。

- [YouTube Data API v3 概要](https://developers.google.com/youtube/v3)
- [`videos.insert`](https://developers.google.com/youtube/v3/docs/videos/insert): `snippet`と`status`を指定し、動画メディアを再開可能方式で登録します。アップロード対象は`output/final.mp4`だけです。未監査の新しいAPI projectではprivate制限がかかる場合があり、公式には監査で制限解除を申請する扱いです。
- [`videos.update`](https://developers.google.com/youtube/v3/docs/videos/update): 予約時は`status.privacyStatus=private`と将来の`status.publishAt`を送ります。`publishAt`は未公開private動画にのみ使え、過去時刻は即時公開として扱われ得るため、スクリプトは現在時刻以前を拒否します。
- [`thumbnails.set`](https://developers.google.com/youtube/v3/docs/thumbnails/set): upload後にPNG/JPEGサムネイルを設定します。2MiB超、破損、非対応形式は事前に停止します。
- [`videos` resource / limits](https://developers.google.com/youtube/v3/docs/videos): titleは100文字以内、descriptionは5,000 UTF-8 bytes以内、tags合計は500文字以内として、超過時は自動切り詰めせず停止します。
- [`channels.list`](https://developers.google.com/youtube/v3/docs/channels/list): `mine=true`でOAuth中のアカウントが所有するチャンネルを取得し、チャンネルIDを照合します。
- [`videos.list`](https://developers.google.com/youtube/v3/docs/videos/list): upload後に動画ID、title、privacyStatus、publishAtを再取得して検証します。
- [再開可能upload protocol](https://developers.google.com/youtube/v3/guides/using_resumable_upload_protocol) と [Python upload guide](https://developers.google.com/youtube/v3/guides/uploading_a_video): Google公式Python clientの`MediaFileUpload(..., resumable=True)`とchunk単位の`next_chunk()`を使います。
- [Installed app / desktop OAuth](https://developers.google.com/youtube/v3/guides/auth/installed-apps): ブラウザで人間がGoogleアカウントを選び、ローカルredirectで認証します。パスワードはスクリプトに保存しません。

## 実行モード

```powershell
# APIを呼ばずに全ローカルgateを確認
python scripts/publish_youtube.py 003 --private --dry-run

# 人間がdry-runを確認した後に、非公開で登録
python scripts/publish_youtube.py 003 --private

# 日本時間として解釈し、private登録後に予約
python scripts/publish_youtube.py 003 --schedule "2026-09-02 19:00"

# OAuth中のチャンネルを表示し、初回だけ人間承認済みIDを保存
python scripts/publish_youtube.py --verify-channel

# uploadなしでOAuth・access token・channel guardを確認
python scripts/publish_youtube.py --auth-check

# 失敗した後の対象だけを再試行（動画再uploadなし）
python scripts/publish_youtube.py 003 --retry-thumbnail
python scripts/publish_youtube.py 003 --retry-schedule "2026-09-02 19:00"
```

`--public`は常に次のエラーで停止します。publish.jsonにpublicが書かれていても、publicへ昇格する処理はありません。

```text
ERROR
Immediate public publishing is disabled by policy.
```

`--yes`は最終確認プロンプトを明示的に省略するときだけ使います。`--force-new-upload`は既存IDがある場合の新規動画作成を明示的に許可する特殊操作で、`--yes`も必須です。通常処理は既存IDがあれば二重uploadを拒否します。削除機能はありません。

## upload前のgate

通常処理では、まずOAuth healthと`channels.list`によるchannel guardを通過させます。その後、次のlocal gateを確認し、すべて通らない限り`videos.insert`へ進みません。

- `episodes/NNN_slug/output/final.mp4`が存在し、空でない。draftは対象外。
- `STATE.md`が`status: finalized`かつ`human_approved: true`。
- `work/human_review.json`に承認済み`draft_auto_*`が1つある。
- `output/review/final_qa.md`（または同等の記録）がPASSで、現在のfinal SHA-256を記録している。
- thumbnailが存在し、PNG/JPEGとして開け、2MiB以下である。
- title / description / tags / category / language / made-for-kidsが検証を通る。
- 予約時刻が現在のJSTより未来である。
- 過去の`youtube_video_id`や未解決の`upload_attempt.json`がない。

Episode 003の現行サムネイルは既存構成を尊重して候補を順に探し、現在は`episodes/003_line_renewal/output/thumbnail.png`を選びます。今後の標準保存先は次です。

```text
episodes/NNN_slug/assets/thumbnail/thumbnail.png
```

## metadataとdescription

`episode.json`の`publish`ブロックを基礎に、同じepisodeの`publish.json`があればそれを優先します。`selected_title`があればtitleに使用し、`description_file`が明示されていればそのファイルを使用します。description本文は大幅に書き換えず、欠けている場合だけ章立て、出典URL、VOICEVOXクレジットを末尾に補います。

送信する主な値は次のとおりです。

```text
snippet.title
snippet.description
snippet.tags
snippet.categoryId
snippet.defaultLanguage
status.privacyStatus=private
status.selfDeclaredMadeForKids
```

予約では最初の`videos.insert`をprivateで行った後、`videos.update(part=status)`で`publishAt`を設定します。更新時に`selfDeclaredMadeForKids`も含め、status部品の意図しない消失を避けます。

## AI使用開示（containsSyntheticMedia）

YouTube公式の[`videos` resource](https://developers.google.com/youtube/v3/docs/videos)では、`status.containsSyntheticMedia`を`videos.insert`または`videos.update`で設定できます。これは、写実的なAltered / Synthetic contentを含むことをチャンネル所有者が開示するための項目です。[YouTube Helpの生成AIコンテンツ開示](https://support.google.com/youtube/answer/14328491?hl=ja)では、実際には起きていない写実的なsceneなどは開示対象、台本・タイトル・サムネイル・字幕の補助や非写実的なイラストなどは通常の開示対象外と説明されています。

episode metadataでは、次の明示booleanを使用します。

```json
{
  "contains_synthetic_media": true
}
```

実装上は次のように対応します。

```text
contains_synthetic_media: true/false
        ↓
status.containsSyntheticMedia: true/false
```

AIを使ったという事実だけで自動的に`true`にはしません。写実的なAI人物・実際には存在しない写実的scene・現実の人物/場所/出来事の大幅なAI改変は`true`候補、台本生成・タイトル生成・caption生成・明らかなイラスト・軽微な補助編集は`false`候補です。判定できない場合はmetadata未設定のままにせず、公開前に`AI disclosure: REVIEW REQUIRED`で停止します。

Episode 003は、人間判断により`contains_synthetic_media: true`です。GPT画像で写実的なシニア人物と実在しない場面を使用しているため、YouTube APIでは`status.containsSyntheticMedia=true`へ反映します。

既存動画の開示だけを更新する場合は、次を使用します。

```powershell
python scripts/publish_youtube.py 003 --set-ai-disclosure true
```

このコマンドは、まず既存video IDを使って`videos.list(part=status)`を呼び、`privacyStatus`、`publishAt`、`selfDeclaredMadeForKids`などを表示・保存します。その後、現在存在する更新可能なstatus値を保持したbodyに`containsSyntheticMedia`だけを変更して`videos.update(part=status)`を呼びます。snippet、thumbnail、video ID、privacy、予約時刻は変更せず、`videos.insert`は呼びません。更新後も`videos.list(part=status)`で開示値と保持値を検証します。

APIのstatus応答で`containsSyntheticMedia`が返らない場合があります。その場合は、`videos.update`の成功レスポンスに含まれる`status.containsSyntheticMedia`を確認し、privacy・publishAt・madeForKidsなどは更新後の`videos.list`で確認します。どちらからも開示値を確認できない場合はPASSにせず停止します。確認経路は`youtube_ai_disclosure_verification`と`ai_disclosure_attempt.json`へ記録します。

dry-runでは次の表示を行い、APIを呼びません。

```text
AI DISCLOSURE DRY-RUN
Existing video ID: ...
Target AI disclosure: YES
videos.insert: NOT CALLED
OAuth/API: NOT CALLED (dry-run)
```

通常の新規private / scheduled uploadでも、metadataに明示された値を`videos.insert`のstatusへ含め、upload後の`videos.list`で一致確認します。metadataが未設定のepisodeは、`false`と推測せずreview requiredで停止します。

## OAuthとチャンネル照合

秘密ファイルは次に置きます。

```text
local/youtube/client_secret.json
local/youtube/token.json
local/youtube/channel_config.json
```

設定ファイルが要求するscopeは`youtube.upload`と`youtube.force-ssl`です。前者は動画登録、後者は予約更新・動画照合などの追加操作に使います。scopeを増やしたり、削除権限を追加したりはしません。

初回の`--verify-channel`で`channels.list(mine=true)`の実際のチャンネル名とIDを表示します。人間が承認した場合だけ、IDと名前を`channel_config.json`へ保存します。以後は表示名より優先してチャンネルIDを照合し、IDまたは承認済み名前が異なれば停止します。OAuth中のアカウントがテスト用アカウントなら、uploadを開始しません。

公開処理の開始時には`youtube_auth_preflight`を表示し、client type、tokenの存在、refresh tokenの有無、access token期限、refresh結果、error classを秘密値なしで確認します。既存`token.json`がある場合は、access tokenが期限切れまたは5分以内に期限切れとなる場合にrefreshを試します。refresh tokenがない、refreshが`invalid_grant`で失敗した、またはclient IDが不一致の場合はブラウザOAuthへ自動フォールバックせず停止します。ブラウザ再認証は、人間が明示的に`--force-reauth`を指定した場合だけ開始します。uploadを伴わない認証診断は`python scripts/publish_youtube.py --auth-check`で実行でき、`channels.list(part="id,snippet", mine=True)`とchannel guardまで確認します。詳細は[YouTube OAuth恒久運用](youtube_oauth.md)を参照してください。

Google Auth Platformの`Audience → Publishing status`はコードから推測しません。`Testing`ではtest userの認可とoffline accessのrefresh tokenが7日で期限切れになるため、長期運用では必要な確認後に`In production`へ変更することを推奨します。現在のstatusは人間がGoogle Cloud Consoleで確認します。

## 失敗時と再試行

upload開始前の失敗では公開状態を変更しません。`videos.insert`成功後は、API応答の動画IDを`upload_attempt.json`と`STATE.md`へ直ちに保存します。

- thumbnail失敗: `uploaded_private_thumbnail_failed`またはscheduled版を記録し、動画は削除せず`--retry-thumbnail`だけを許可します。
- 予約設定失敗: `uploaded_private_schedule_failed`を記録し、動画はprivateのまま、`--retry-schedule`だけを許可します。
- 検証失敗: IDを保持し、public化や再uploadは行わず停止します。
- `upload_attempt.json`がIDなしで開始中なら、サーバー側の成功有無を推測せず、新しいuploadを拒否します。

ログは`episodes/NNN_slug/work/youtube_publish/`に保存します。ログにはtoken、client secret、OAuthレスポンス本文を保存しません。

成功時の状態項目は次です。

```text
youtube_upload: uploaded_private | uploaded_scheduled
youtube_video_id
youtube_url
youtube_privacy
youtube_scheduled_at
youtube_scheduled_at_api
thumbnail_uploaded
uploaded_at
```

## quotaの目安

[公式quota calculator](https://developers.google.com/youtube/v3/determine_quota_cost)を2026-08-31に確認しました。既定値は、`videos.insert`が専用bucketで1日100 calls（1 call = 1 unit）、その他endpointの合計が1日10,000 unitsです。今回の主要endpointは次の値です。

| API | 公式quotaの目安 |
|---|---:|
| `channels.list` | 1 unit |
| `videos.insert` | 1 unit / 1日100 callsの専用bucket |
| `videos.update` | 50 units |
| `thumbnails.set` | 50 units |
| `videos.list` | 1 unit |

1本の通常private uploadは、チャンネル照合・insert・thumbnail・verifyで概ね4 callsです。scheduledは`videos.update`が加わります。quota値は変更され得るため、実運用前は公式表を再確認してください。無効なリクエストもquotaを消費します。

未監査projectでは、公式`videos.insert`仕様にあるprivate制限が適用される可能性があります。scheduled/publicがproject側で制限される場合も、スクリプトはpublicへfallbackせず、private状態で停止してStudioで人間が確認する運用にします。

## 標準フロー

```text
finalize
  ↓
thumbnail確定
  ↓
publish dry-run
  ↓
人間確認
  ↓
private または scheduled upload
  ↓
API verify
  ↓
STATE更新
```

動画upload自動化の実装時点ではEpisode 001〜003の再uploadを行っていません。今回のAI開示対応では、既存Episode 003の確認済みvideo IDに対してstatus-onlyの`videos.update`を実行し、`videos.insert`・thumbnail変更・snippet変更・公開状態変更は行っていません。
