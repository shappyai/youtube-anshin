# Episode013 iPhone capture report — 2026-09-06

## 結果

- iPhone capture: **3 / 3**
- 取得済み: `SCENE-009`, `SCENE-013`, `SCENE-015`
- SCENE-005: 実機captureから正式除外。公式事実rendererへ変更
- draft生成: **なし**

## 実測値

| Scene | 実画面で確認した結果 |
|---|---|
| SCENE-009 | `iOSバージョン 26.6.1` |
| SCENE-013 | LINEの横に **「開く」**。更新ボタンは表示されていない |
| SCENE-015 | `iOSは最新です`、`iOS 26.6.1` |

## 台本とのmenu差分

- SCENE-009は`設定 > 一般 > 情報`の実画面を確認した。
- SCENE-013はApp StoreのLINE検索結果で実表示を取得した。実画面が`開く`のため、台本・レンダーに`アップデート`ボタンを追加していない。
- SCENE-015は`設定 > 一般 > ソフトウェアアップデート`の実画面を確認した。

## privacy確認

- SCENE-009はiOSバージョン行だけをcropし、端末名・モデル・Apple Account・シリアル・IMEI・通知を除外した。
- SCENE-013はLINEの行だけをcropし、アカウント名・メール・購入履歴・通知を除外した。
- SCENE-015はソフトウェアアップデートの状態部分をcropし、個人情報・通知を除外した。
- fake UI: **0** / AI reconstruction: **0** / 架空の更新ボタン: **0**

## 成果物

- `assets/captures/iphone/iphone_scene009_ios_version.png`
- `assets/captures/iphone/iphone_scene013_line_update.png`
- `assets/captures/iphone/iphone_scene015_os_update.png`
