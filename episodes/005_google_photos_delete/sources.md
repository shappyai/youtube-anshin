# Episode 005 sources

確認日: **2026-09-01**

調査方針: Googleフォト公式ヘルプ・Googleアカウント/Google One/Googleドライブ公式ヘルプ・Apple Support公式・Google公式ブログの一次情報のみを使用。まとめサイト・個人ブログ・SEO記事・ニュース二次記事は事実確認に使用していない。各URLの本文を当日ダウンロードして確認した。取得済みHTMLは `local/web_check_005/` に保存（20件）。

## 主要ソース

| ID | 確認日 | URL | 何が確認できたか |
|---|---|---|---|
| SRC-001 | 2026-09-01 | https://support.google.com/photos/answer/6128858?co=GENIE.Platform%3DAndroid&hl=ja | Googleフォト「写真や動画を削除する（Android）」。バックアップ済み写真・動画は削除後ゴミ箱に保持され60日後に完全削除、バックアップ済みでないものは30日後に完全削除。「重要: Googleフォトアプリから削除するとデバイスからも同じ写真・動画が削除される。バックアップ対象はバックアップがオンになっているすべてのデバイスから削除。アプリからのみ削除するにはまずバックアップをオフにする。」「デバイスから削除」手順（その他アイコン→デバイスから削除）。削除ページのヒント「一部の写真は削除すると容量を節約。どれくらい増えるか示されることがある」。 |
| SRC-002 | 2026-09-01 | https://support.google.com/photos/answer/6128858?co=GENIE.Platform%3DiOS&hl=ja | Googleフォト「写真や動画を削除する（iPhone/iPad）」。iOS版にも「デバイスから削除」手順が記載（2026-09-01現在）。ヒント「iPhoneまたはiPadのGoogleフォトから写真や動画を完全に削除しても、Appleの写真アプリの［最近削除した項目］フォルダには残る場合があります。」 |
| SRC-003 | 2026-09-01 | https://support.google.com/photos/answer/6128858?co=GENIE.Platform%3DDesktop&hl=ja | Googleフォト「写真や動画を削除する（パソコン/Web）」。ゴミ箱を空にする手順、完全削除手順（photos.google.com）。 |
| SRC-004 | 2026-09-01 | https://support.google.com/photos/answer/6128858?co=GENIE.Platform%3DDesktop&hl=en | Delete photos & videos (Desktop, en)。英語公式文「Backed up photos and videos you delete will stay in your trash for 60 days before they're permanently deleted forever. If the photos and videos aren't backed up, they'll be permanently deleted after 30 days. Photos and videos that were permanently deleted can't be restored.」 |
| SRC-005 | 2026-09-01 | https://support.google.com/photos/answer/6128843?co=GENIE.Platform%3DAndroid&hl=ja | Googleフォト「デバイスの空き容量を増やす（Android）」。実行前条件「Googleフォトに写真を安全にバックアップした後に…削除すれば、デバイスの空き容量を増やせます」「写真を削除する前に、必ずバックアップを取ってください」。手順（プロフィール写真またはイニシャル→このデバイスの空き容量を増やす→空き容量を[x]増やす）。注記「過去30日以内にデバイスに保存した写真や動画は、デバイスに保持される場合があります。写真や動画は、Googleフォトライブラリにバックアップとして残ります。」削除後もGoogleフォトアプリやphotos.google.comで表示可能。 |
| SRC-006 | 2026-09-01 | https://support.google.com/photos/answer/6128843?co=GENIE.Platform%3DiOS&hl=ja | Googleフォト「デバイスの空き容量を増やす（iPhone/iPad）」。iOS版の手順（プロフィール→このデバイスの空き容量を増やす→デバイスから[x]個のアイテムを削除→削除）。「30日以上経過した写真や動画は、デバイスから削除しても、Googleフォトライブラリにバックアップとして残ります。」実行後に「iPhoneまたはiPadの写真アプリを開きます（Googleフォトアプリではありません）。［最近削除した項目］を開き、同じ写真と動画を削除します」と公式案内。 |
| SRC-007 | 2026-09-01 | https://support.google.com/photos/answer/6193313?co=GENIE.Platform%3DAndroid&hl=ja | Googleフォト「写真や動画をバックアップする（Android）」。現行の設定項目名は「バックアップ」（プロフィール写真またはイニシャル→フォトの設定→バックアップ）。「アイテムのバックアップが完了すると、ステータスには「バックアップが完了しました」と表示されます。バックアップステータスがオフの場合「バックアップがオフになっています」。」 |
| SRC-008 | 2026-09-01 | https://support.google.com/photos/answer/6193313?co=GENIE.Platform%3DiOS&hl=ja | Googleフォト「写真や動画をバックアップする（iPhone/iPad）」。iOSの設定パス（右上のプロフィール写真またはイニシャル→Googleフォトの設定→バックアップ）、iOSの写真アクセス許可手順。 |
| SRC-009 | 2026-09-01 | https://support.google.com/photos/answer/10100180?hl=ja | Googleフォト「Google フォト ストレージ使用量」。各Googleアカウント最大15GB、Gmail/ドライブ/フォトで共有。2021年6月1日以降のアップロードから計上。 |
| SRC-010 | 2026-09-01 | https://support.google.com/photos/answer/10100180?hl=en | Storage usage in Google Photos (en)。英語版の同内容（trash 60日など）。 |
| SRC-011 | 2026-09-01 | https://support.google.com/photos/answer/9284827?hl=ja | Googleフォト「ストレージを管理する（パソコン）」。保存容量にカウントされないアイテムの一覧、削除で容量を節約するヒント。 |
| SRC-012 | 2026-09-01 | https://support.google.com/photos/answer/9284827?co=GENIE.Platform%3DAndroid&hl=ja | Googleフォト「ストレージを管理する（Android）」。設定パス（プロフィール→フォトの設定→バックアップ→ストレージを管理）。2021年6月1日より前に保存容量の節約画質（旧称「高画質」）またはエクスプレス画質でバックアップした写真・動画はアカウント容量にカウントされない。 |
| SRC-013 | 2026-09-01 | https://support.google.com/photos/answer/9284827?co=GENIE.Platform%3DiOS&hl=ja | Googleフォト「ストレージを管理する（iPhone/iPad）」。iOSの設定パス（プロフィール→Googleフォトの設定アイコン→バックアップ→ストレージを管理）。 |
| SRC-014 | 2026-09-01 | https://support.google.com/photos/answer/9284827?hl=en | Manage your storage (en)。英語版（what doesn't count toward storage）。 |
| SRC-015 | 2026-09-01 | https://support.google.com/drive/answer/6374270?hl=ja | Googleドライブ公式ヘルプ「ドライブ、Gmail、フォトの保存容量を管理する」。ゴミ箱と迷惑メールフォルダを空にすることが空き容量を増やす最も迅速な方法。「これらのフォルダ内のアイテムは、完全に削除するまで保存容量の上限の対象としてカウントされます。」複数ファイル削除時は容量反映に最長48〜72時間かかることがある。 |
| SRC-016 | 2026-09-01 | https://support.apple.com/ja-jp/124460 | Apple Support「iPhone、iPad、Mac、またはApple Vision Proで削除された写真を復元する方法」。写真やビデオを削除すると「最近削除した項目」アルバムに移動し、30日間保管。30日経過後は完全に削除され取り戻せない。復元手順。 |
| SRC-017 | 2026-09-01 | https://support.apple.com/ja-jp/guide/iphone/iphb4defbde9/26/ios/26 | Apple「iPhoneユーザガイド: iPhoneで写真やビデオを削除する/非表示にする」。削除した写真・ビデオは完全に削除されるまで「最近削除した項目」コレクションに30日間保管。その間復元または完全削除できる。「iCloud写真を使用している場合は、削除するか非表示にした写真がすべてのデバイスでも削除されるか非表示になります。」 |
| SRC-018 | 2026-09-01 | https://blog.google/intl/ja-jp/products/connect-communicate/2020_11_storage-policies-update/ | Google公式ブログ「Googleアカウントのストレージポリシー変更について」（2020-11-12公開）。2021年6月1日以降にGoogleフォトへアップロードされる新しい写真・動画はすべてアカウントの無料15GBストレージまたはGoogle Oneの追加容量に計上。それ以前の高画質分は対象外。当時は「バックアップと同期」という名称だった。 |
| SRC-019 | 2026-09-01 | https://blog.google/products-and-platforms/products/photos/storage-changes/ | Updating Google Photos' storage policy to build for the future（2020-11-11公開・英語）。同発表の英語版。 |
| SRC-020 | 2026-09-01 | https://support.apple.com/ja-jp/guide/iphone/welcome/ios | Apple iPhoneユーザガイド（目次）。削除トピックの本文はSRC-017で取得済み（このURLはガイド目次へのリダイレクト。参考のみ）。 |
| SRC-021 | 2026-09-01 | https://support.google.com/photos/answer/9343482?co=GENIE.Platform%3DAndroid&hl=ja | Googleフォト「最近削除した写真や動画を復元する（Android）」。削除した写真や動画がゴミ箱に残っている場合の復元可否、手順（コレクション→ゴミ箱→写真を長押し→復元）、復元先、バックアップ有無による60日/30日条件を確認。保存HTMLは `local/web_check_005/gphoto_restore_android.html`、該当手順cropはSCENE-022で使用。 |

## 重要事実と台本での言い方

### A. 通常の「削除」で何が起きるか

- バックアップ済みの写真・動画は、削除後ゴミ箱に保持され、**60日後**に完全削除。バックアップ済みでないものは**30日後**に完全削除（SRC-001/004）。
- Googleフォトアプリから削除すると、**端末からも同じ写真が削除される**。バックアップ対象なら「バックアップがオンになっているすべてのデバイス」から削除（SRC-001の「重要」文言）。
- クラウドだけを消して端末に残すには、まずスマートフォンでバックアップをオフにしてから削除する（SRC-001/002）。
- iPhoneでは、Googleフォトから「完全に削除」しても、Apple「写真」アプリの「最近削除した項目」に**残る場合があります**（SRC-002のヒント文言。「場合があります」を必ず付ける）。

### B. 「デバイスから削除」

- Googleフォトのクラウド側には残し、その端末のローカルコピーだけを削除する操作（SRC-001の手順から）。
- Android・iPhone/iPadの両方について、現行の公式ヘルプに手順が記載されている（2026-09-01時点。SRC-001/002）。実機アプリのメニュー表示はバージョン差があり得るため「機種やアプリのバージョンによって違う場合があります」と留保する。
- この操作ではGoogleアカウントの容量は増えない（クラウド側の写真は消えない。A・Cの公式文言と整合）。逆の説明はしない。

### C. 「このデバイスの空き容量を増やす」

- 実行前条件は「バックアップ済み」。「Googleフォトに写真を安全にバックアップした後にデバイスから写真を削除すれば、デバイスの空き容量を増やせます」「写真を削除する前に、必ずバックアップを取ってください」（SRC-005/006）。
- メニューの場所は両OS共通「プロフィール写真またはイニシャル→このデバイスの空き容量を増やす」（SRC-005/006）。
- 実行しても、Googleフォト（クラウド）には残る。削除後もGoogleフォトアプリやphotos.google.comで表示可能（SRC-005/006）。
- Androidは「過去30日以内に保存した写真・動画はデバイスに保持される場合があります」、iOSは「30日以上経過した写真・動画」が対象（SRC-005/006）。
- iOSでは実行後、Apple「写真」アプリ（Googleフォトアプリではない）の「最近削除した項目」から同じ写真・動画を削除する、と公式が案内（SRC-006）。

### D. iPhone: Googleフォトのゴミ箱とApple「最近削除した項目」

- Apple公式: 「最近削除した項目」は**30日間**保管され、30日経過後は完全削除（SRC-016/017。2026-09-01現在の公式値）。
- Googleフォトのゴミ箱（60日/30日）とApple「最近削除した項目」（30日）は別物。Google公式も「最近削除した項目」に残る場合がある、と明記（SRC-002）。
- iCloud写真オン時は、Apple「写真」アプリでの削除がすべてのApple端末に及ぶ（SRC-017）。

### E. Googleアカウントの容量（クラウド）とスマホ本体の容量

- 「空き容量を増やす」はスマホ本体の空き容量を増やす操作で、Googleアカウントのクラウド容量は減らない（クラウド側には残る。SRC-005/006）。
- Googleアカウントの容量を空けるには、Googleフォト上で削除→ゴミ箱から完全削除まで必要。ゴミ箱内アイテムは「完全に削除するまで保存容量の上限の対象としてカウント」（SRC-015。ドライブ公式ヘルプのGmail/ドライブ/フォト共通説明）。
- 2021年6月1日以降にアップロードした写真・動画はGoogleアカウントの無料15GBに計上。それ以前に「保存容量の節約画質（旧称: 高画質）」でバックアップした分は現在もカウントされない（SRC-009/012/018/019）。
- 複数ファイル削除時の容量反映は最長48〜72時間かかることがある（SRC-015）。

### バックアップの確認方法

- 現行の設定項目名は「バックアップ」。パスは Android: 「右上のプロフィール写真またはイニシャル→フォトの設定→バックアップ」／iOS: 「→Googleフォトの設定→バックアップ」（SRC-007/008）。
- 完了表示: 「バックアップが完了しました」／オフ時: 「バックアップがオフになっています」（SRC-007）。

## 未確認事項（「確認できませんでした」）

- iOS版Googleフォトアプリの実機UIで「デバイスから削除」メニューが確実に表示されるか（公式ヘルプには手順あり。実機確認はPhase B）。
- 「空き容量を増やす」実行後の端末容量の反映タイミング・機種差（公式は「場合があります」のみ）。
- ゴミ箱「いっぱい」表示のしきい値（件数・容量）。
- 「フォトのゴミ箱内アイテムが容量にカウントされる」というフォト単独ページでの明示文（ドライブ公式ヘルプでは確認済み）。
- 容量表示48〜72時間のフォト単独での公表（ドライブ公式ヘルプの文言のみ）。
- 「バックアップと同期」→「バックアップ」への名称変更時期の公式発表。
- iCloud写真＋Googleフォト両方オンの組み合わせ挙動の公式説明。
- 容量にカウントされない「一部のGoogle Pixelデバイス」の2026年時点の対象機種一覧。
- Googleフォトの「完全に削除」がApple側「最近削除した項目」に残る条件。

## 参照しなかった情報

- まとめサイト・個人ブログ・SEO記事・ニュース二次記事は事実確認に使用していない。
- 競合動画の調査は本エピソードでは行っていない。
