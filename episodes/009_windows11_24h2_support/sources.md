# Episode 009 sources

確認日: 2026-09-05（公開前に再確認）

一次情報を優先し、二次記事・競合動画は根拠として使用していない。ページの内容は更新される可能性があるため、公開前に日付・対象エディション・25H2の提供状況を再確認する。

|ID|組織 / URL|確認できたこと|使用箇所|
|---|---|---|---|
|SRC-001|Microsoft Learn / [Windows client supported versions](https://learn.microsoft.com/ja-jp/windows/release-health/supported-versions-windows-client)|Windows 11 24H2はHome / Pro / Pro Education / Pro for Workstationsで2026-10-13まで。25H2は2027-10-12まで。エディションにより期間が異なる。|基礎事実、タイトル、台本|
|SRC-002|Microsoft Learn / [Windows 11 version 24H2 known issues](https://learn.microsoft.com/ja-jp/windows/release-health/status-windows-11-24h2)|Home / Proの24H2の更新終了日、終了後に通常の更新・サポートが受けられないこと、対象機器には25H2が自動提供されること、Windows Update確認手順。|基礎事実、25H2|
|SRC-003|Microsoft Learn / [Windows 11 release information](https://learn.microsoft.com/ja-jp/windows/release-health/windows11-release-information)|年1回の機能更新、Home / Pro等24か月、Enterprise / Education 36か月のサポート区分、24H2以降の終了日。|エディション差、説明|
|SRC-004|Microsoft Learn / [Windows 11 version 26H1](https://learn.microsoft.com/ja-jp/windows/whats-new/windows-11-version-26h1)|26H1は一部の新しい機器向けの特別なリリース。既存PCへのWindows Update提供やインプレース更新の対象ではない。|26H1の補足|
|SRC-005|Microsoft Support / [Windows 11 2025 update](https://support.microsoft.com/ja-jp/windows/deployment/updates-lifecycle/inside-this-update)|Windows 11 2025 updateの案内と、設定のWindows Updateから確認する考え方。|更新画面|
|SRC-006|Microsoft Support / [Install Windows updates](https://support.microsoft.com/ja-JP/Windows/Deployment/Updates-Lifecycle/install-windows-updates)|スタート > 設定 > Windows Update > 更新プログラムの確認、利用可能時のダウンロードとインストール、再起動の案内。|操作手順|
|SRC-007|Microsoft Support / [Find information about your Windows device](https://support.microsoft.com/ja-jp/windows/experience/find-information-about-your-windows-device)|スタートを右クリック > 設定 > システム > バージョン情報、Windowsの仕様でエディションとバージョンを確認する場所。|バージョン確認、公式画面|
|SRC-008|Microsoft Support / [Windows 11 version 26H1 update history](https://support.microsoft.com/ja-JP/servicing/os/windows-11/2026/02/windows-11-version-26h1-update-history)|設定 > システム > バージョン情報でVersionを確認する手順。|バージョン確認|
|SRC-009|Windows Experience Blog / [How to get the Windows 11 2025 update](https://blogs.windows.com/windowsexperience/2025/09/30/how-to-get-the-windows-11-2025-update/)|25H2は段階的に提供され、対象機器でもアプリ・ドライバー互換性の確認により提供時期が異なる。|表示されない場合|
|SRC-010|Microsoft Support / [Safeguard holds](https://support.microsoft.com/en-us/servicing/os/windows/2021/09/kb5006965-how-to-check-information-about-safeguard-holds-affecting-your-device)|既知の問題から保護するため機能更新の提供を一時保留する仕組み。準備ができるまで待つ旨の案内。|セーフガードホールド|
|SRC-011|Microsoft Learn / [Windows 11 version 25H2 status](https://learn.microsoft.com/ja-jp/windows/release-health/status-windows-11-25h2)|対象機器へ段階的に提供され、Windows Updateで確認できる。セーフガードホールドにより待つ場合がある。|25H2の説明|

## 公式画面素材

- `assets/official/windows_update_official.png`: SRC-005 / SRC-006に掲載された実在のWindows Update画面を保存。英語UIのため、日本語の操作文は後工程の正確なoverlayで表示する。
- `assets/official/windows_update_check_button_official.png`: 上記公式画面から「Check for updates」ボタン周辺を拡大cropし、操作対象を読めるサイズにしたもの。
- `assets/official/about_header_official.png`: SRC-007の公式画面から、「システム > バージョン情報」の見出しだけを安全にcrop。
- `assets/official/about_specs_header_official.png`: SRC-007の公式画面から、「デバイスの仕様」の見出しだけを安全にcrop。
- `assets/official/about_header_zoom_official.png` / `assets/official/about_specs_zoom_official.png`: 上記の安全cropを拡大して表示用にしたもの。
- `assets/official/about_version_label_official.png`: SRC-007の公式画面から「バージョン情報」見出しだけを採用した表示用crop。
- Windows 11実機captureは `local/capture_windows_settings.ps1` で設計したが、現在の制作PCはWindows 10 Pro 24H2のため実行結果はblocked。実機captureをPhase Aで使用していない。

## Final Fact Watch（2026-09-05）

公開準備前にMicrosoft公式ページを再確認した。Windows 11 24H2のHome / Pro / Pro Education / Pro for Workstationsは `2026-10-13` に更新終了、25H2は `2027-10-12`、26H1は `2028-03-14` と、Microsoftの[Windows 11 リリース情報](https://learn.microsoft.com/ja-jp/windows/release-health/windows11-release-information)および[サポートされているバージョンのWindowsクライアント](https://learn.microsoft.com/ja-jp/windows/release-health/supported-versions-windows-client)で確認した。[24H2の状態ページ](https://learn.microsoft.com/ja-jp/windows/release-health/status-windows-11-24h2)にもHome / Proの2026-10-13、25H2の提供、Windows Updateでの確認が明記されている。

26H1は[Microsoftの説明](https://learn.microsoft.com/ja-jp/windows/whats-new/windows-11-version-26h1)どおり、選択された新しい機器にプレインストールされる限定的なリリースで、既存端末へのWindows Updateによる機能更新ではない。したがって「Windows 11全体が10月13日に終了する」とは扱わず、台本・動画は変更しない。

なお、[Home and ProのLifecycleページ](https://learn.microsoft.com/ja-jp/lifecycle/products/windows-11-home-and-pro)には24H2の終了時刻が `10/14/2026 6:59:59 AM` と表示される箇所がある。同ページのPT表示説明と、更新終了日を日付で明示する上記2ページの記載差は公開前確認事項として記録したが、利用者向けの暦日としては複数のrelease-health表・本文が一致する `2026-10-13` を採用する。
