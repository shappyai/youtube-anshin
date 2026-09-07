# Episode 009 Final Fact Watch

確認日: 2026-09-05（JST）  
判定: **PASS / 台本・動画の変更なし**

公開準備前のMicrosoft公式情報を再確認した。重要な事実の変更や、動画を止める重大な矛盾は確認されなかった。

| 確認項目 | Microsoft公式で確認した内容 | 判定 |
|---|---|---|
| Windows 11 24H2 Home / Pro系 | 24H2はHome、Pro、Pro Education、Pro for Workstationsで2026-10-13に更新終了。 | PASS |
| Windows 11全体の終了ではない | 25H2と26H1が別のサポート対象バージョンとして掲載され、エディション・サービスチャネルにより終了日が異なる。 | PASS |
| 25H2 | 24H2 Home / Proの管理されていない端末には25H2が提供され、設定 > Windows Update > 更新プログラムの確認で確認できる。 | PASS |
| 26H1 | 次世代ハードウェア向けの限定的なリリース。既存端末への機能更新としてWindows Updateから提供されるものではない。 | PASS |

## 日付表示の取り扱い

Home and ProのLifecycleページには、24H2の終了時刻が `10/14/2026 6:59:59 AM` と表示される箇所がある。一方、同ページは日付をPTで表示すると説明しており、Microsoftのリリース正常性ページの本文と、Windows 11の現在のバージョン表は、利用者向けの更新終了日を明示的に `2026-10-13` としている。25H2・26H1も同じ表で確認できるため、本動画では公式の更新終了日として `2026年10月13日` を維持する。

この表示差は記録したうえで、アップロード直前には再度公式ページを確認する。公開日時やサポート時刻を動画内で断定する変更は行わない。

## 参照した一次情報

- [Windows 11 リリース情報](https://learn.microsoft.com/ja-jp/windows/release-health/windows11-release-information) — 24H2 / 25H2 / 26H1の更新終了日、エディション別の表、26H1の位置づけ。
- [サポートされているバージョンの Windows クライアント](https://learn.microsoft.com/ja-jp/windows/release-health/supported-versions-windows-client) — Home / Pro系とEnterprise / Education系の終了日の違い。
- [Windows 11 バージョン 24H2 の既知の問題と通知](https://learn.microsoft.com/ja-jp/windows/release-health/status-windows-11-24h2) — 24H2 Home / Proの2026-10-13、25H2提供、Windows Updateでの確認。
- [Windows 11、IT担当者向けのバージョン26H1](https://learn.microsoft.com/ja-jp/windows/whats-new/windows-11-version-26h1) — 26H1は既存端末向けの機能更新ではなく、Windows Updateから提供されないこと。
- [Windows 11 ホーム アンド プロ - Microsoft Lifecycle](https://learn.microsoft.com/ja-jp/lifecycle/products/windows-11-home-and-pro) — 対象エディションとLifecycle上の終了時刻表示。上記の日付表示差を記録するため参照。

## 変更判断

- `episode.json`、`script.md`、`captions.srt`、`output/draft_v3.mp4`は変更しない。
- `2026年10月13日`、24H2 Home / Pro系、25H2、26H1の説明は維持する。
- 25H2が表示されないことを故障・買い替え必須とは扱わない。
