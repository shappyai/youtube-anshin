# Episode 005 Android Capture Report

Phase B前半のAndroid Capture Agent報告。確認日・撮影日は **2026-09-01（Asia/Tokyo）**。本ファイルはサブエージェント成果物であり、Episode 001〜004は変更していない。残課題の局所処理後のcanonical反映（episode.json、shotlist、media_manifest）は親Codex側で実施済み。

## 実行環境

- Device: `emulator-5556`
- Model: `sdk_gphone64_x86_64` / manufacturer: Google
- Android: 16 / API 36
- Display: 1080 x 2424 px
- Googleフォト package: `com.google.android.apps.photos`
- Googleフォト versionName: `7.8.0.697873850`（アプリ画面の表示は「バージョン 7.8」）
- Source: すべて `adb exec-out screencap -p` の実画面

## 安全性

- 個人写真・位置情報・通知・個人アカウントの利用／探索は行っていない。画面上に事前設定済みのテスト用アカウント表示が出たが、識別子は記録せず、素材のcrop対象から外した。
- `episode005_safe_dummy.png` はローカル生成した単色背景＋青い円のPNG（1600 x 900、EXIF/位置情報を付与していない）。端末には同名の自作ダミー1枚だけを追加した。
- 単発の「今すぐバックアップ」は自作ダミー1枚だけに実行した。グローバルのバックアップ設定はONにしていない。
- 通常削除の確認UIは自作ダミーに限って表示確認した。完全削除は行っていない。
- 最終的な「ゴミ箱に移動」後の状態は追加再試行せず、復元可能なアイテムの存在を推測していない。端末上の自作ダミーは片付けず、次工程の人間確認対象として残している。

## 6用途の判定

| 用途 | Scene | 素材 | 判定 | 確認内容・crop note |
|---|---|---|---|---|
| backup status | SCENE-004 | `assets/captured/android/backup_status.png`、補助 `backup_status_item.png` | **REVIEW** | 設定画面は「バックアップ」トグルOFFで、「バックアップが完了しました」は出なかった。補助画面では自作ダミーの「バックアップ済み（13 KB）」を確認。global完了表示としては使わない。crop: 設定の「バックアップ」行／補助画面の「バックアップ済み」。 |
| normal delete / trash icon | SCENE-006 | `assets/captured/android/delete_photo_trash.png` | **REVIEW** | 自作ダミーの実画面で下部の「ゴミ箱」アイコンを取得。確認ダイアログではGoogleアカウント・バックアップONの他デバイス・共有場所から削除する旨を確認したが、削除後の一連の反映までは未検証。crop: 下部右側の「ゴミ箱」。 |
| trash screen | SCENE-008 | `assets/captured/android/trash_days.png` | **PASS** | 現行UIの「ゴミ箱は空です」と、バックアップ済み60日／未バックアップ30日の保持案内を取得。アイテム表示ではなく保持期間確認用。crop: 「ゴミ箱」見出しと保持期間の文章。 |
| delete from device | SCENE-012 | `assets/captured/android/delete_from_device.png` | **PASS** | 詳細メニューに現行UIの「デバイスから削除」を確認。位置情報は未設定。crop: メニュー中央の「デバイスから削除」。 |
| free up space | SCENE-014 | `assets/captured/android/free_up_space.png` | **PASS** | 「このデバイスの空き容量を増やす」「安全にバックアップされています」「空き容量を13.40 KB増やす」を確認。実行ボタンは押していない。crop: 見出し、バックアップ済み説明、下部ボタン。 |
| restore | SCENE-022 | `assets/captured/android/restore_from_trash.png` | **NOT CAPTURED / STOP** | 安全な範囲で確認した時点のゴミ箱は空。自作ダミーの削除後に最終反映・復元ボタンを確認できる状態を再現できず、既存ライブラリを探す／追加の削除再試行／完全削除は行わない。推測代替なし。 |

## 素材台帳（SHA-256）

| scene_id | filename | source/device | app version | captured_at | privacy check | fact/UI notes | SHA-256 |
|---|---|---|---|---|---|---|---|
| SCENE-004 | `assets/captured/android/backup_status.png` | adb screencap / emulator-5556 | 7.8.0.697873850 | 2026-09-01T07:42:27+09:00 | PASS:識別子・写真なし | global backup is OFF。完了表示なし。 | `96A991D907F687D653EB37C7419D7E7E323C84BF309C64FBA3BF01D9A666DDB4` |
| SCENE-004 (補助) | `assets/captured/android/backup_status_item.png` | adb screencap / emulator-5556 | 7.8.0.697873850 | 2026-09-01T07:51:49+09:00 | PASS:自作ダミーのみ | 「バックアップ済み（13 KB）」、元の画質。global完了表示ではない。 | `0CEA89342BDDD9BC7FCC394280D820DFC94EC5E60B90DA627BCAE7F6FEB6B49E` |
| SCENE-006 | `assets/captured/android/delete_photo_trash.png` | adb screencap / emulator-5556 | 7.8.0.697873850 | 2026-09-01T07:45:05+09:00 | PASS:自作ダミーのみ | 下部「ゴミ箱」アイコン。 | `6D99D311B0F87B0C3007DC696454AB04FEC1D5763A6397FAA1C5AFF0425048EF` |
| SCENE-008 | `assets/captured/android/trash_days.png` | adb screencap / emulator-5556 | 7.8.0.697873850 | 2026-09-01T07:48:53+09:00 | PASS:写真・個人情報なし | 「ゴミ箱は空です」、60日／30日案内。 | `A1BEE7C7FEE1F0D6531208BF1C0DF32B2644DFB2451292D35B5627A592C3A901` |
| SCENE-012 | `assets/captured/android/delete_from_device.png` | adb screencap / emulator-5556 | 7.8.0.697873850 | 2026-09-01T07:37:43+09:00 | PASS:自作ダミーのファイル情報のみ | 「デバイスから削除」表示。位置情報なし。 | `C34E17FE3A1198CDDECC2768B2D7FF33A066B2D62F4EF927AA9E3EC8CBEFD8E8` |
| SCENE-014 | `assets/captured/android/free_up_space.png` | adb screencap / emulator-5556 | 7.8.0.697873850 | 2026-09-01T07:40:44+09:00 | PASS:自作ダミーのみ | バックアップ済み説明と13.40 KBの対象確認。実行前で停止。 | `5FE6D160A9DF5BC7BE5C1CEF517160C1A616D7954A383663A6203656F4CF8E11` |
| supplemental | `assets/captured/android/backup_settings_detail.png` | adb screencap / emulator-5556 | 7.8.0.697873850 | 2026-09-01T07:43:11+09:00 | PASS:識別子・写真なし | バックアップ設定画面のOFF表示。初回取得時の補助素材。 | `8A5AA82F77B22A05E636B9E47607FB2BA23974B7065494A0ECD765F1130884DB` |
| test input | `assets/captured/android/episode005_safe_dummy.png` | local generated, then pushed to emulator-5556 | N/A | 2026-09-01T07:24:10+09:00 | PASS:自作・位置情報なし | 1600 x 900、単色背景＋青い円。 | `BE3D0A48960808D701709E7B374675B1F535B82134D4439E5C204FE2874826D2` |

## STOP / WARN

1. SCENE-004: Phase Aの「バックアップが完了しました」は、globalバックアップOFFのため未取得。単発ダミーの「バックアップ済み」は別表示として扱う。
2. SCENE-006: 現行UIは通常削除が二段階確認で、削除後の状態は未検証。ダイアログの文言はPhase A facts（端末・Googleアカウント等にも及ぶ）と整合するが、実演素材としての最終フレームは未確定。
3. SCENE-008: 保持期間の公式文言は取得できたが、ゴミ箱内アイテムとの同時表示は未取得。
4. SCENE-022: `restore_from_trash.png` は未作成。復元ボタンを推測で生成・代替しない。

以上。次工程では、REVIEW項目を人間ゲートで承認し、特にSCENE-004の完了表示とSCENE-022の復元画面を安全な専用テスト環境で再取得するか判断する。

## Phase B前半残課題の局所処理（2026-09-01）

元のREVIEW 2用途を、次の分類で再評価した。

| Scene | 元の理由分類 | 局所処理 | 最終扱い |
|---|---|---|---|
| SCENE-004 | UI文言差（設定画面のグローバル完了表示が未取得。取得済みの個別写真「バックアップ済み」とは別文言） | 個人情報を含まない保存済みGoogle公式ヘルプから「バックアップが完了しました」の該当本文をcaptureし、見出し・完了表示・オフ表示だけをcrop | **PASS（公式fallback）**。Android実機の完了表示とは表現しない |
| SCENE-006 | 操作対象が見えない（元cropはタップ対象の下部操作部に限定） | 自作ダミーだけの安全な既存captureから「ゴミ箱」操作部を中央crop。sceneの目的をタップ前の対象確認に限定し、未検証の削除後状態は表示・断定しない | **PASS（局所crop）**。削除後画面の実演素材ではない |

分類対象外の未取得素材は、SCENE-022のAndroid実画面である。追加の削除再試行は行わず、現行Google公式ヘルプの手順fallbackへ切り替えた。
