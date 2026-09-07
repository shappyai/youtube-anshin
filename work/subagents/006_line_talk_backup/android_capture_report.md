# Episode 006 Android / LINE Capture Report

status: `fallback_recommended`

確認日時: **2026-09-02（Asia/Tokyo）**

担当範囲: SCENE-006 / SCENE-007 / SCENE-011 / SCENE-016 のAndroid実画面素材のみ。

## 実行環境

- ADB device: `emulator-5556`（接続状態 `device`）
- Model: `sdk_gphone64_x86_64`
- Android: `16` / API `36`
- Display: `1080x2424 px`
- LINE package: **未インストール**（`jp.naver.line.android` を確認できず）
- ローカルAPK/AAB: **リポジトリ内に該当ファイルなし**

## 判定

安全なAndroid Emulator自体は接続されていたが、LINEが利用できる状態ではなかった。Playストアからの追加導入、ログイン、SMS認証、新規アカウント作成、実アカウント情報の使用には進まなかった。したがって、指定4画面を実画面として取得する安全な経路がなく、ここで中止した。

| Scene / Shot | 指定ファイル | 結果 | 理由 |
|---|---|---|---|
| SCENE-006 / SHOT-01 | `episodes/006_line_talk_backup/assets/captured/android/backup_transfer_menu.png` | **NOT CAPTURED** | LINE未インストール |
| SCENE-007 / SHOT-02 | `episodes/006_line_talk_backup/assets/captured/android/talk_backup_datetime.png` | **NOT CAPTURED** | LINE未インストール。前回日時や「今すぐバックアップ」を推測しない |
| SCENE-011 / SHOT-03 | `episodes/006_line_talk_backup/assets/captured/android/auto_backup_toggle.png` | **NOT CAPTURED** | LINE未インストール。自動バックアップ設定を推測しない |
| SCENE-016 / SHOT-05 | `episodes/006_line_talk_backup/assets/captured/android/backup_pin_setting.png` | **NOT CAPTURED** | LINE未インストール。PIN値・入力欄を作成／表示しない |

## プライバシー・安全確認

- 実トーク、友だち名、家族名、電話番号、LINE ID、QRコード、通知内容、プロフィール写真、メール、実PIN、SMS認証コードにはアクセスしていない。
- 既存の `local/web_check_006/line_*.html` は架空UIの代替になるため使用していない。
- AI生成画像、合成スクリーンショット、モック画面、既存画面の別用途流用は行っていない。
- 指定4ファイルは作成していないため、寸法・比率・ファイルサイズ・SHA-256は該当なし（画像なし）。
- 短い全体画面および読ませる項目のcropも未取得。

## Canonical file保全

指定されたcanonical fileは変更していない。確認した取得前SHA-256は以下のとおりで、作業後にも再確認する対象とした。

| File | SHA-256（取得前） |
|---|---|
| `episodes/006_line_talk_backup/episode.json` | `4B931AB8BB0600595E6111087E6DC4F6999B695A2285920977DC1C55583F0819` |
| `episodes/006_line_talk_backup/script.md` | `918DC0D3CDAB336788B48E428C645DF05F6AECB055310EC3D0FC50ADB9629FCB` |
| `episodes/006_line_talk_backup/shotlist.md` | `99054F19CDBEC3E5105BD068816E3ED2706834872BFA7A862EFB61E9F7EC357A` |
| `episodes/006_line_talk_backup/publish.json` | `18F2E142B5733788E1A8B438513D1AB84A7E6F078D36FA7BDB0E9EF352D80542` |
| `episodes/006_line_talk_backup/STATE.md` | `BEC18D171DDC38792AD46D6BEAEA3853680A0699CB4BCB9184425F11E5837E61` |
| `episodes/006_line_talk_backup/work/production_metrics.json` | `48D17C0500D4BC5279F0502D259FD8256A66F3F091596C985C6AE48679DD8AC9` |

## 次工程への推奨

LINEの安全な撮影専用テストアカウントがログイン済みの実機またはEmulatorを人間が用意できた時点で、4画面を再取得する。用意できるまでは、4 sceneとも `fallback_recommended` として扱い、正確なUIを推測で補わない。
