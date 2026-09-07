# Episode013 capture device status — 2026-09-06

## 調査結果

- `adb.exe`: installed
- ADB version: `1.0.41 / 37.0.0-14910828`
- `adb devices -l`: `emulator-5554` / state `device`
- Android capture: **4 / 4**（SCENE-006 / 010 / 014 / 016）
- iPhone capture: **3 / 3**（SCENE-009 / 013 / 015）
- SCENE-005: iPhone実機LINE画面のcapture対象から正式除外。LINE公式の下限値だけをrenderer-nativeで表示
- missing real UI capture: **なし**

## Android実測

- emulator: `emulator-5554` / `sdk_gphone64_x86_64` / Android `16` / 1080x2424
- SCENE-006: `LINEについて > 現在のバージョン`、`26.14.0`。最終成果物は確認行だけをcrop
- SCENE-010: `Android バージョン` は `16`。端末識別情報を含む全体画面は不採用
- SCENE-014: Google PlayのLINE検索結果で、LINEの行は`インストール済`・`開く`。当初想定の`アプリとデバイスの管理`画面との差分を記録し、更新ボタンは作らない
- SCENE-016: `お使いのシステムは最新の状態です`。`アップデートを確認`ボタンも実画面で確認
- 台本との差分: 設定の実表示は `エミュレートされたデバイスについて`、システム内は `ソフトウェア アップデート`（空白あり）

## iPhone実測

- SCENE-009: `iOSバージョン 26.6.1`の行だけをcrop
- SCENE-013: App StoreのLINE行は実画面で`開く`。更新ボタンは作らない
- SCENE-015: `iOSは最新です`、`iOS 26.6.1`をcrop

## 既存workflowの確認

- repo内でEpisode013用のAndroid／iPhone capture workflowは確認できなかった。
- `scripts/capture_android.py`はEpisode001固定のためEpisode013のcaptureには流用していない。
- 今回はユーザー提供の実画面probeを確認し、指定sceneのprivacy cropとして保存した。

## 安全状態

- fake UI: `0`
- AI reconstruction of official UI: `0`
- 架空の更新ボタン: `0`
- neutral frameをdraftへ残す: `禁止`
- `output/draft_v1.mp4`: 未生成
- 最終cropにGoogle account、email、device ID、serial、IMEI、notificationを含めていない

## 次の状態

7つのreal UI captureとSCENE-005の公式事実rendererが揃った。Visual Gate v3の機械QAは24scene OK / 0 WARN / 0 FAIL。人間Visual Gate、発音レビュー、Fact/Privacy/Audio/Subtitle QAが終わるまでdraftは生成しない。
