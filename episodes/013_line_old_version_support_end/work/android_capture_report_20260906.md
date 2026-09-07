# Episode013 Android capture report — 2026-09-06

## 結果

- Android capture: **4 / 4**
- 取得済み: `SCENE-006`, `SCENE-010`, `SCENE-014`, `SCENE-016`
- 保存先: `assets/captures/android/`
- draft生成: **なし**
- iPhone capture: **3 / 3**（SCENE-005は正式除外し、公式事実rendererへ変更）

## 実測値

| 項目 | 実画面で確認した結果 |
|---|---|
| LINE現在version | **26.14.0**（SCENE-006 `LINEについて > 現在のバージョン`） |
| Android version | **16**（SCENE-010） |
| Google PlayのLINE更新表示 | **なし**。LINEの行に実際に表示されたのは **「開く」**。更新ボタンは捏造していない（SCENE-014） |
| OS更新表示 | **あり**。`お使いのシステムは最新の状態です`。実画面には`アップデートを確認`ボタンも表示（SCENE-016） |

## 台本とのmenu差分

- SCENE-006は、実画面で`LINEについて`と`現在のバージョン`を確認できた。表示されたLINE versionは`26.14.0`。
- SCENE-010の設定トップに表示された端末情報入口は `エミュレートされたデバイスについて`。台本の「デバイス情報」は機種差を含む一般化表現として扱う。
- SCENE-014は、当初想定の`Google Play > アプリとデバイスの管理`画面ではなく、Google PlayのLINE検索結果画面で取得された実画面。LINEの行には`インストール済`と`開く`が表示されていた。台本は「更新が表示されるかを確認」に合わせ、更新ボタンを追加しない。
- SCENE-016のシステム内表示は `ソフトウェア アップデート`（空白あり）。台本の`ソフトウェアアップデート`と表記差がある。
- OS更新画面の実タイトルは `お使いのシステムは最新の状態です`。表示されていたAndroid versionは`16`。

## privacy確認

- SCENE-006の最終PNGは`LINEについて / 現在のバージョン / 26.14.0`の確認部分だけで、ステータスバー・通知・アカウント・メール・電話番号・device ID・serial・IMEIを含まない。
- SCENE-010の最終PNGは`Android バージョン / 16`の行だけで、Google account、電話番号、IMEI、IP/MAC、通知、device ID、serialを含まない。
- SCENE-014の最終PNGはLINEの検索結果行だけで、Google account、メール、通知、device ID、serial、IMEIを含まない。
- SCENE-016の最終PNGはステータスバーとナビゲーションバーを除いた更新状態部分だけで、account、email、device ID、serial、IMEI、通知を含まない。
- fake UI: **0** / AI reconstruction: **0** / 架空の更新ボタン: **0**

## 成果物

- `assets/captures/android/android_scene006_line_version.png`
- `assets/captures/android/android_scene010_android_version.png`
- `assets/captures/android/android_scene014_line_update.png`
- `assets/captures/android/android_scene016_os_update.png`

Android 4/4を取得し、追加のAndroid撮影はここで停止する。SCENE-005はiPhoneの実機LINE画面を捏造せず、LINE公式の事実だけをrendererで表示する。Visual Gate v3の機械QAは完了したが、人間Visual Gateと発音レビュー完了前のdraft生成は行わない。
