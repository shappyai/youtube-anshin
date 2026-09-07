# Episode 006 iPhone / official asset report

確認日時: **2026-09-02（Asia/Tokyo）**

## 結論

- iPhone実機の取得は行わず、SCENE-014はLINE公式保存HTMLの文言を使った引用カードへfallbackした。
- Android EmulatorはLINE未インストールだったため、SCENE-006 / 007 / 011 / 016も同じ方式へfallbackした。
- SCENE-020 / 022は、当初の公式crop相当素材を保存HTML由来の引用カードとして再生成した。
- 7枚とも、実在UI・LINEロゴ・アカウント情報・Apple ID・メールアドレス・PIN実値を含まない。カード上にも「実際のLINE画面ではありません」と明記している。
- ローカル保存HTMLの直接ブラウザ表示・スクリーンショットは、アプリのローカルファイル保護で許可されなかったため、HTML本文を一次情報として確認し、引用カードで代替した。公式ページのURL・タイトル・確認日・引用元HTMLを `media_manifest.csv` に記録している。

## 公式素材一覧

| Scene | Asset | 公式ページタイトル | URL | 確認日 | 結果 |
|---:|---|---|---|---|---|
| 006 | `episodes/006_line_talk_backup/assets/official/line_backup_transfer_menu_fallback.png` | トーク履歴を標準バックアップするには？ | https://help.line.me/line/smartphone?contentId=20023473&lang=ja | 2026-09-02 | 公式手順引用カードfallback |
| 007 | `episodes/006_line_talk_backup/assets/official/line_talk_backup_datetime_fallback.png` | トーク履歴を標準バックアップするには？ | https://help.line.me/line/smartphone?contentId=20023473&lang=ja | 2026-09-02 | 公式手順引用カードfallback |
| 011 | `episodes/006_line_talk_backup/assets/official/line_auto_backup_fallback.png` | トーク履歴を標準バックアップするには？ | https://help.line.me/line/smartphone?contentId=20023473&lang=ja | 2026-09-02 | 公式手順引用カードfallback |
| 014 | `episodes/006_line_talk_backup/assets/official/line_icloud_drive_crop.png` | バックアップしたトークの復元方法 | https://help.line.me/line/smartphone/categoryId/20007890/3/pc?contentId=20007389&lang=ja | 2026-09-02 | iPhone実画面の公式手順引用カードfallback |
| 016 | `episodes/006_line_talk_backup/assets/official/line_backup_pin_fallback.png` | [バックアップ用のPINコード]とは？ | https://help.line.me/line/smartphone/pc?contentId=20020033&lang=ja | 2026-09-02 | 公式手順引用カードfallback |
| 020 | `episodes/006_line_talk_backup/assets/official/line_standard_backup_same_os_crop.png` | トーク履歴を標準バックアップするには？ | https://help.line.me/line/smartphone?contentId=20023473&lang=ja | 2026-09-02 | 公式文言引用カード |
| 022 | `episodes/006_line_talk_backup/assets/official/line_backup_trouble_media_crop.png` | トーク履歴のバックアップ（保存）や復元で問題が発生している場合 | https://help.line.me/line/smartphone?contentId=20020173&lang=ja | 2026-09-02 | 公式文言引用カード |

## 画像検証

カードはすべて **1680×515 px**。公式ページの導線記号は、読みやすさのため `⋅` を `・` に整形している。出典の正確なURLと保存HTMLのファイル名は `media_manifest.csv` に残した。

| Asset | bytes | SHA-256 |
|---|---:|---|
| `line_backup_transfer_menu_fallback.png` | 76090 | `66636f79855d0fbf624babc5262853951a9a600c0ddf491b14e96c6a0baca7d5` |
| `line_talk_backup_datetime_fallback.png` | 78328 | `f75a1c28d19c8e5483ef3840ffcb79d15b945026d91f098f095900de86c21451` |
| `line_auto_backup_fallback.png` | 75083 | `2035fabc4f5bddb24fe8d91a8e0e38780ffc44502e0ae674642a172b5dd7d827` |
| `line_icloud_drive_crop.png` | 74770 | `87f18e2e87a881b1ffb9ec5ead9bb9a41daebac98aea39076b7b6f354ff80ce1` |
| `line_backup_pin_fallback.png` | 78122 | `e2a3660ab3d09815ce7496adc051eafbae8e7286bef067ef88ea34f9759711ba` |
| `line_standard_backup_same_os_crop.png` | 75745 | `3d8034f9c2f3e554962d0160961c4389cc7a73ec573542a78671665b254dd310` |
| `line_backup_trouble_media_crop.png` | 83642 | `07fa29aa1ed1b7c9b864445d57f471636f1bd084a307ef046505a9c87d4787c8` |

## Human review items

- 「実際のLINE画面ではない」という注記が読めること。
- 引用カードの文字が、スマホ視聴時にも読めること。
- 実画面fallbackのまま公開するか、LINEが利用できる安全なテスト環境を用意して再取得するか。
