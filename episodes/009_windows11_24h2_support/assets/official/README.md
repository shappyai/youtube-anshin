# Episode 009 公式画面素材

確認日: 2026-09-05

## 採用素材

- `about_header_official.png`: Microsoft Supportの「Windowsデバイスの情報を確認する」ページに掲載された「システム > バージョン情報」の見出し部分。個人情報を含む下部を採用していない。
- `about_specs_header_official.png`: 同ページの「デバイスの仕様」見出し部分。値・ID・アカウント情報は採用していない。
- `about_header_zoom_official.png` / `about_specs_zoom_official.png`: 上記の安全cropから余白をさらに減らし、公式見出しを読めるサイズにした拡大crop。
- `about_version_label_official.png`: 「システム >」の文字化け・HTML entity表示を画面に残さないため、「バージョン情報」の公式見出しだけを切り出した採用crop。
- `about_version_focus_official.png`: 上記の採用cropからさらに余白を減らしたVisual Gate v2用のfocus crop。公式文字は変更していない。
- `about_specs_focus_official.png`: 「デバイスの仕様」公式見出しを大きく見せるVisual Gate v2用のfocus crop。Windowsの仕様・バージョンの説明欄はrendererの別レイヤーで表示し、公式UIを書き換えない。
- `windows_update_official.png`: Microsoft Supportの「Windows 11の2025年更新プログラム」ページに掲載されたWindows Update画面。英語UIの実在画面をそのまま使用し、日本語の操作説明は別レイヤーで正確に表示する。
- `windows_update_check_button_official.png`: 上記の公式画面から、操作対象の「Check for updates」ボタン周辺だけを拡大cropしたもの。UIを描き直さず、公式原画を切り出している。

## 出典

- https://support.microsoft.com/ja-jp/windows/experience/find-information-about-your-windows-device
- https://support.microsoft.com/ja-jp/windows/deployment/updates-lifecycle/inside-this-update
- https://support.microsoft.com/ja-JP/Windows/Deployment/Updates-Lifecycle/install-windows-updates

## 実機capture

`local/capture_windows_settings.ps1` を使用する。現在の制作PCはWindows 10 Pro 24H2のため、同スクリプトは実画面を開かず `blocked` を記録する。Windows 11実機で実行した場合も、原画は `work/windows_capture/` にのみ保存し、個人情報を確認・マスキングしたcropだけを採用する。

`_source_tmp/` の原画は素材一覧・レンダリング・contact sheetで使用しない一時保管領域だった。canonical参照0件を確認し、2026-09-05に削除済み。
