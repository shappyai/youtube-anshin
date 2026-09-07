# Episode 013 sources

確認日: **2026-09-06**  
方針: LINE、Apple、Googleの一次情報を使用。各URLの本文を当日確認し、確認できた範囲を記録した。掲載内容はOS・アプリの更新で変わるため、公開前に再確認する。

| ID | 確認日 | URL | 何が確認できたか |
|---|---|---|---|
| SRC-001 | 2026-09-06 | https://help.line.me/line/smartphone?contentId=200002720&lang=ja | LINE公式のお知らせ。2026年11月上旬に、iOS／iPadOSのLINE 14.6.3未満、AndroidのLINE 14.4.6未満のサポートを終了予定。iOS／iPadOS 15.0以上・Android 8.0以上の場合の更新手順、OSまたはLINEを更新できない場合は動作環境を満たす別端末を検討する案内を確認。更新日2026年8月3日。 |
| SRC-002 | 2026-09-06 | https://help.line.me/line?contentId=10002433&lang=ja | LINEの利用環境。最新版の推奨環境はiOS 18.0以上、Android 11.0以上。動作環境としてiOS 15.0〜15.8.6はLINE 14.6.3まで、Android 8.0〜8.1はLINE 14.4.6まで等を確認。iOS／iPadOS 14.8.1以下、Android 7.1.2以下、LINE 13.20.0以下に関する注意も確認。 |
| SRC-003 | 2026-09-06 | https://help.line.me/line/smartphone?contentId=10002432&lang=ja | LINEバージョン確認手順。「ホーム → 設定 → LINEについて → 現在のバージョン」を確認する案内を確認。 |
| SRC-004 | 2026-09-06 | https://help.line.me/line/smartphone?contentId=20005476&lang=ja | LINEのインストール・更新ができない場合の公式対処。推奨環境の確認、iPhone／iPadの更新トラブル、AndroidのGoogle Play・空き容量・メーカー確認などを確認。 |
| SRC-005 | 2026-09-06 | https://support.apple.com/ja-jp/109065 | Apple公式。iPhone／iPadのOSバージョンは「設定 → 一般 → 情報」で確認する手順を確認。 |
| SRC-006 | 2026-09-06 | https://support.apple.com/ja-jp/102629 | Apple公式。App Store → アカウント → アプリのアップデート → 対象アプリの「アップデート」で手動更新する手順を確認。 |
| SRC-007 | 2026-09-06 | https://support.apple.com/ja-jp/guide/personal-safety/ips4930e3486/web | Apple公式。「設定 → 一般 → ソフトウェアアップデート」でiOS／iPadOSを確認・更新する手順を確認。 |
| SRC-008 | 2026-09-06 | https://support.google.com/android/answer/7680439?hl=ja | Google公式。Androidバージョンは「設定 → デバイス情報／タブレット情報 → Androidバージョン」で確認。OS更新は「設定 → システム → ソフトウェアアップデート」。更新時期は端末・メーカー・通信会社で異なることを確認。 |
| SRC-009 | 2026-09-06 | https://support.google.com/googleplay/answer/113412?hl=ja | Google Play公式。Google Play → プロフィール → アプリとデバイスの管理 → アップデート利用可能 → 対象アプリの「更新」で手動更新する手順を確認。 |
| SRC-010 | 2026-09-06 | https://help.line.me/line/smartphone?contentId=20023724&lang=ja | 機種変更前のLINE最新版・OS最新版・連絡先確認・トーク履歴バックアップ・アカウント引き継ぎの事前準備を確認。Episode 013では詳細操作を再説明しない。 |

## 一次情報で確認できなかったこと

- 11月上旬の具体的な実施日時は、確認時点の公式告知では未確定。
- 個々のiPhone機種、Androidメーカー・通信会社ごとの更新可否は一律に確定できない。
- 現在ストアで配信されているLINEの最新バージョン番号を、この動画の固定Factにはしない。

## 2026-09-06 capture/fact recheck

- SRC-001のLINE公式ページを再確認し、2026年11月上旬予定、iOS／iPadOSのLINE 14.6.3未満、AndroidのLINE 14.4.6未満という境界に変更がないことを確認した。
- 実画面の固定値としては、Android probeのLINE現在version `26.14.0`、Android version `16`、iPhoneのiOS `26.6.1`を記録した。これらは撮影端末の表示値であり、公式のサポート終了境界とは別の値である。
- [LINE公式のお知らせ](https://help.line.me/line/smartphone?contentId=200002720&lang=ja) に具体的な実施日はなく、動画内では「11月上旬の予定」とする。
