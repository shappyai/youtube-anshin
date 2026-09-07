# Episode 005 Phase B前半 — iPhone / Official Asset QA

- 実施日: 2026-09-01
- 対象: SCENE-018 / SCENE-019
- 判定: **PASS（利用可能） / WARN 3件 / STOP なし**
- 追加作成: なし（既存の公式cropで要件を満たすため）
- canonical file: `episode.json` / `shotlist.md` / `media_manifest.csv` は変更していない

## 1. 利用判定

| Scene | 採用するファイル | 判定 | 確認内容 |
|---|---|---|---|
| SCENE-018 | `episodes/005_google_photos_delete/assets/official/google_photos_delete_ios_crop.png` + `apple_guide_delete_photos_crop.png` | PASS（2枚組） | Google公式の「写真や動画を削除する」とApple公式の「iPhoneで写真やビデオを削除する/非表示にする」を並べ、Googleフォト側とApple「写真」側で削除時の扱いが違うことを示せる。 |
| SCENE-019 | `episodes/005_google_photos_delete/assets/official/apple_recently_deleted_crop.png` | PASS | Apple公式ページの見出し、「最近削除した項目」、30日以内の復元、30日経過後の完全削除が同一crop内で読める。 |

上記はすべて「公式ヘルプページの画面」であり、iPhone実機の写真アプリ画面そのものではない。映像上では実機画面と誤認させず、Apple/Google公式ページ由来のfallbackとして扱う。

## 2. 公式ページ由来の確認

### Google公式（SCENE-018）

- 保存HTML: `local/web_check_005/gphoto_delete_ios.html`
- ページタイトル: `写真や動画を削除する - iPhone と iPad - Google フォト ヘルプ`
- source URL: https://support.google.com/photos/answer/6128858?co=GENIE.Platform%3DiOS&hl=ja
- 本文で確認できた内容:
  - バックアップ済みの写真・動画は削除後にゴミ箱に保持され、60日後に完全削除。
  - バックアップされていない写真・動画は30日後に完全削除。
  - Googleフォトから完全に削除しても、Appleの写真アプリの「最近削除した項目」フォルダには残る場合がある。
  - Googleフォトから削除した写真・動画の削除先として、バックアップがオンのiPhone/iPad等とGoogleフォトのアルバムが本文に列挙されている。
- `google_photos_delete_ios_crop.png` の画面上で読める主な文言は、タイトル、60日/30日の保持期間、削除前の注意事項。Apple側に残る「場合があります」の一文は保存HTML本文にはあるが、現在のcropには写っていない。

### Apple公式 iPhoneユーザガイド（SCENE-018）

- 保存HTML: `local/web_check_005/apple_guide_delete_photos.html`
- ページタイトル: `iPhoneで写真やビデオを削除する/非表示にする - Apple サポート (日本)`
- source URL: https://support.apple.com/ja-jp/guide/iphone/iphb4defbde9/26/ios/26
- 本文とcropで確認できた内容:
  - 写真アプリから削除した写真・ビデオは「最近削除した項目」に保存される。
  - iCloud写真を使用している場合、削除は他の対象デバイスにも及ぶ旨の説明がある。
  - 「最近削除した項目」に30日間保管され、その間は復元または完全削除できる旨が保存HTML本文にある。

### Apple Support（SCENE-019）

- 保存HTML: `local/web_check_005/apple_124460_recentlydeleted.html`
- ページタイトル: `iPhone、iPad、Mac、またはApple Vision Proで削除された写真を復元する方法 - Apple サポート (日本)`
- source URL: https://support.apple.com/ja-jp/124460
- 本文と `apple_recently_deleted_crop.png` で確認できた内容:
  - 削除した写真・ビデオは「最近削除した項目」アルバムに移動する。
  - アルバムの中身は30日間保管される。
  - 30日経過後は完全に削除され、取り戻せない。

## 3. 画像ファイル検査

全6ファイルをPNGとしてデコードできること、寸法、SHA-256、GPS系メタデータの有無を確認した。SHA-256は重複なし。

| ファイル | サイズ | 寸法 | 比率 | SHA-256 | 判定 |
|---|---:|---:|---:|---|---|
| `apple_guide_delete_photos_crop.png` | 45,867 bytes | 1000×563 | 1.776199 | `17B0AF4216902A5CFCD155BC2E9B5A45EC0193CC2442383D54573F9CD7345EDA` | decode OK |
| `apple_guide_delete_photos_viewport.png` | 66,005 bytes | 1440×810 | 1.777778 | `F90AC3B7EBA018533D62B7E9B3F171814621BCDF52A31149CACFE835150CE809` | decode OK / WARN |
| `apple_recently_deleted_crop.png` | 54,817 bytes | 1000×563 | 1.776199 | `70B3E567AB22F6123FD4D1A595A7D5650932010E9F2EBC2E7E0BF9B3341B519E` | decode OK |
| `apple_recently_deleted_viewport.png` | 77,343 bytes | 1440×810 | 1.777778 | `A85894FA2FBB522804F25F296077587C84233DB73ED49C30A4B8B742E365F652` | decode OK / WARN |
| `google_photos_delete_ios_crop.png` | 51,270 bytes | 900×506 | 1.778656 | `F944CA54F53C4A93B4DC82BFD5C2C697292273C131DEC86B7BCA23B95EE4A371` | decode OK |
| `google_photos_delete_ios_viewport.png` | 106,326 bytes | 1440×810 | 1.777778 | `D4BF18934FC9DEC9CCD7527522F7F18ED04C77F18A4F4F179FDF80FB491BAA34` | decode OK |

- すべて16:9に十分近い。cropはレンダー時に1920×1080へ正規化する前提で問題ない。
- PNGの画像プロパティ項目は各ファイル3件。GPS関連のExif項目は全ファイル0件。
- 画像の目視では、個人写真、氏名・メールアドレス等のアカウント情報、通知バナー、通知内容、地図、住所、GPS座標・位置情報は見当たらない。
- Apple画面の検索欄やGoogleヘルプの「ログイン」は一般的な公式サイトUIで、ログイン済みの個人アカウント情報は写っていない。
- AI生成画像・偽の設定UIは使用していない。見出し、本文、配色、公式サイトのUIが保存HTMLと対応している。

## 4. WARN / STOP

### WARN-01 — Apple recently-deleted viewport版は不採用

`apple_recently_deleted_viewport.png` の下端に、Appleページ内の画像が読み込めず `null` と表示される箇所がある。本文の公式文言は正常に読めるが、公開映像にはこのviewport版を使わず、該当箇所を含まない `apple_recently_deleted_crop.png` を使う。

### WARN-02 — SCENE-018のクロスアプリ関係はcrop単体では完結しない

Google公式cropにはGoogle側の削除・保持期間が、Apple公式cropにはApple側の「最近削除した項目」と30日保管が写っている。一方、Google公式本文にある「Googleフォトから完全に削除しても、Appleの写真アプリの『最近削除した項目』に残る場合があります」というクロスアプリの注意文は現在のGoogle cropには写っていない。

したがって、SCENE-018では2枚組と既存のナレーション/後描画テキストを一緒に使い、「残る場合があります」と条件付きで説明する。crop自体が実機での同一写真の動作結果を示す、と表現しない。

### WARN-03 — file:// のブラウザ表示確認は未実施

保存HTMLをアプリ内ブラウザで直接開く操作はローカル `file://` の安全ポリシーで拒否されたため、別ブラウザ等の回避は行わず、本文・タイトル・公式URLの静的確認と既存PNGの直接目視で判定した。HTML表示の追加確認が必要な場合は、公式ページの安全な実機/公式画面取得時に人間ゲートで再確認する。

### STOP

なし。SCENE-018/019とも、実機iPhoneが使えない場合の公式ページfallbackとして使用可能。ただし上記WARNを反映し、viewport版ではなくcrop版を採用する。

## 5. 変更記録

- 追加ファイル: なし
- 変更ファイル: `work/subagents/005_google_photos_delete/iphone_official_report.md` のみ
- `episode.json` / `shotlist.md` / `media_manifest.csv`: 変更なし
