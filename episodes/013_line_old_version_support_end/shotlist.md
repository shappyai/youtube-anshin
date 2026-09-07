# Episode 013 shotlist

Phase Aで撮影媒体を決定済み。LINEはスマホアプリのため、iPhone実機とAndroid Emulator（`emulator-5554`）を使う。今回の確認画面では、実際の端末に表示されるメニュー名と更新可否を優先して撮影する。

## 共通撮影ルール

- テストアカウントを使用し、個人の友だち名、プロフィール写真、トーク、通知、電話番号、メールアドレスを表示しない。
- 画面全体は場所を理解させるため2〜4秒だけ。数字や操作箇所は大きくcropする。
- iPhoneとAndroidを左右に小さく並べず、iPhoneとAndroidを時間方向に分けて表示する。
- 実機の画面名・数字が公式手順と違う場合は、その場で撮影を止め、`sources.md`とFact Checkを更新する。
- 公式UIをAI画像やテンプレートで置き換えない。Phase Aのcontact sheetはneutral visual frameを使用し、Phase Bで実画面に差し替える。
- 字幕安全帯は画面下部180px。画面内の情報文字は原則44px以上、主要数字は60px以上を確保する。

## 撮影カット

| Tag | Device | Scene | 見せる内容 | 画面の扱い | Phase B状態 |
|---|---|---|---|---|---|
| SHOT-01 | Android Emulator | 006 | LINE → ホーム → 設定 → LINEについて → 現在のバージョン | `現在のバージョン 26.14.0`を大きくcrop | CAPTURED |
| SHOT-02 | iPhone実機 | 009 | 設定 → 一般 → 情報 → iOSバージョン | `iOSバージョン 26.6.1`をcrop。Apple Account等は表示しない | CAPTURED |
| SHOT-03 | Android Emulator | 010 | 設定 → デバイス情報等 → Androidバージョン | `Androidバージョン 16`をcrop。端末識別情報は隠す | CAPTURED |
| SHOT-04 | iPhone実機 | 013 | App Store → LINE | 実画面の`開く`をそのままcrop。更新ボタンは捏造しない | CAPTURED |
| SHOT-05 | Android Emulator | 014 | Google Play → LINE検索結果 | 実画面の`インストール済`・`開く`をそのままcrop。想定メニューとの差分を記録 | CAPTURED |
| SHOT-06 | iPhone実機 | 015 | 設定 → 一般 → ソフトウェアアップデート | `iOSは最新です`をcrop。個人情報は表示しない | CAPTURED |
| SHOT-07 | Android Emulator | 016 | 設定 → システム → ソフトウェア アップデート | `お使いのシステムは最新の状態です`をcrop | CAPTURED |

## 公式UI scene一覧

実画面の7scene: `SCENE-006`, `SCENE-009`, `SCENE-010`, `SCENE-013`, `SCENE-014`, `SCENE-015`, `SCENE-016`。  
`SCENE-005`はiPhone実機captureから正式除外し、`renderer_native + SRC-001`の公式事実sceneとする。同じshot tagを左右に小さく並べる構成にはしない。

## 非撮影scene

`SCENE-001〜004`, `SCENE-005`, `SCENE-007〜008`, `SCENE-011〜012`, `SCENE-017〜024` は、共通Background Systemを適用したrenderer/template scene。SCENE-005はLINE公式の下限値だけをPIL/HTMLの文字として表示し、LINE画面を再現しない。その他の正確な数字、判断、ケース分岐もPIL/HTMLの文字として表示し、AI画像は使わない。

## Phase B撮影後チェック

1. 実機のOS・LINEバージョンを記録し、台本の閾値と混同していないか確認する。
2. 「現在のバージョン」「iOSバージョン」「Androidバージョン」をそれぞれ1画面1確認ポイントで撮る。
3. Store画面のアカウント名・メールアドレス・購入履歴をモザイクまたは非表示にする。
4. 公式ページの手順と実機画面の差分を`work/`へ記録する。
5. 画面が読めない場合は撮り直し、全体画面を長く見せて補わない。

## 2026-09-06 capture search result（履歴）

- 当時の検索時点では、有効なEpisode 013用のiPhone／Android実機キャプチャは、作業領域と添付素材から確認できなかった（0 / 8 scene）。
- `local/slot3_scene_013.png` と `local/slot4_scene013.png` はEpisode 013のLINE実機画面ではなく、別案件のGoogle Play／マイナアプリ画面のため使用不可。
- 当時は8sceneを `CAPTURE_REQUIRED` のまま保持し、架空UI・中立フレームをドラフトへ残さない判断だった。

## 2026-09-06 current capture result

- Androidは`SCENE-006/010/014/016`の4 / 4、iPhoneは`SCENE-009/013/015`の3 / 3を採用。
- SCENE-005は実機capture対象から正式除外し、公式事実rendererへ変更。
- SCENE-013/014のストア表示は実際には`開く`。更新ボタンは作らない。
- 実画面7sceneとSCENE-005 rendererを反映したVisual Gate v3の機械QAは24scene OK / 0 WARN / 0 FAIL。人間確認前のdraft生成は禁止。
