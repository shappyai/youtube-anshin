# Episode013 iPhone capture request

既存のWindows側iPhone capture workflowはrepo内にないため、iPhone実機で次の3画面を撮影してください。SCENE-005のiPhone版LINE画面は正式に撮影対象から除外し、LINE公式の事実をrenderer-nativeで表示します。端末はテスト用アカウントを使い、撮影前に通知プレビュー・Apple Account表示・メール・電話番号・連絡先・シリアル番号・IMEIを隠してください。

共通:

- 画面全体は場所が分かる1枚、その後に重要行が読める大きなcropを用意する。
- 画面全体を長く見せ続けない。動画化する場合は全体2〜4秒→重要部分crop。
- 実際の画面に「アップデート」が表示されない場合、架空のボタンを作らない。実際の状態を保存し、sceneの説明は「更新の有無を確認します」に合わせる。
- 更新の実行、アカウント変更、購入、ログアウトなどの確定操作はしない。
- PNG、端末のスクリーンショット原寸を優先する。字幕用の下部180pxを残して保存する。

| Scene | 開く画面 | 撮る箇所 | 個人情報注意 | 期待ファイル名 |
|---|---|---|---|---|
| SCENE-009 | 設定 → 一般 → 情報 | `iOSバージョン`の行を大きくcrop | Apple Account、シリアル番号、IMEI、Wi-Fi名、通知を表示しない | `assets/captures/iphone/iphone_scene009_ios_version.png` |
| SCENE-013 | App Store → アカウント → アプリのアップデート → LINE | LINEの更新有無が分かる行をcrop | アカウント名、メール、購入履歴を表示しない。更新ボタンを捏造しない | `assets/captures/iphone/iphone_scene013_line_update.png` |
| SCENE-015 | 設定 → 一般 → ソフトウェアアップデート | OS更新の有無と画面名をcrop | Apple Account、端末名、通知、個人情報を表示しない | `assets/captures/iphone/iphone_scene015_os_update.png` |

## 撮影後のメモ

撮影した端末の実測値を、captureと一緒に次へ記録してください。

- iPhone機種名:
- iOSバージョン:
- LINE現在のバージョン:
- SCENE-013の更新表示: あり / なし
- SCENE-015のOS更新表示: あり / なし
- 実機画面と台本のメニュー名に差分: なし / あり（差分を記載）

## SCENE-005の扱い

- iPhone実機LINE画面は取得対象外。
- SCENE-005は`renderer_native + SRC-001`で、`14.6.3未満は11月上旬にサポート終了予定`だけを表示する。
- LINEの実際の設定画面をAI・テンプレートで再現しない。
