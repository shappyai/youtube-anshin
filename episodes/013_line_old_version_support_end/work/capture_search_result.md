# Episode 013 real-device capture search result

確認日: 2026-09-06  
判定: **CAPTURE_REQUIRED**

Episode 013用の有効な実機キャプチャは、iPhone 0件・Android 0件（8scene中0件）だった。

対象scene:

- SCENE-005 / 006: LINEの現在のバージョン
- SCENE-009 / 010: iOS／Androidバージョン
- SCENE-013 / 014: App Store／Google PlayのLINE更新
- SCENE-015 / 016: iPhone／AndroidのOS更新

確認したが採用しなかった素材:

- `local/slot3_scene_013.png`
- `local/slot4_scene013.png`

上記はEpisode 013のLINE実機画面ではなく、別案件のGoogle Play／マイナアプリ画面であるため不採用。公式UIのAI再現や、別案件素材の流用で穴埋めはしていない。

停止条件:

- neutral frameを動画ドラフトへ残さない。
- `output/draft_v1.mp4` は生成しない。
- 実機素材が揃った後、同じscene IDへ配置し、Visual Gate v3とprivacy/readability QAを再実行する。

## Visual Redesign v2承認後の再調査（2026-09-06）

- ADBはインストール済みだが、`adb devices -l`の接続端末は0台。
- Android: 0 / 4（SCENE-006 / 010 / 014 / 016）。
- iPhone: 0 / 4（SCENE-005 / 009 / 013 / 015）。
- repo内にEpisode013用のiPhone capture workflowはなく、既存の`capture_android.py`はEpisode001固定のため流用しない。
- fake UI、AI reconstruction、別案件素材の流用はしていない。
- `work/capture_device_status_20260906.md`へ調査結果を保存。
- iPhoneの人間撮影指示を`work/capture_request_iphone.md`へ保存。
- capture不足のため、ここでPhase Bを停止。neutral frameをdraftへ残さず、`output/draft_v1.mp4`も生成しない。

## Android emulator接続後の実測（2026-09-06）

- `emulator-5554` / state `device` を確認。Android 16、1080x2424。
- SCENE-010とSCENE-016は実画面を確認してcrop保存。Android captureは2 / 4。
- LINE packageが端末にないため、SCENE-006とSCENE-014は取得不可。LINEを勝手にインストールせず、fake UI・AI reconstruction・架空の更新ボタンを使わない。
- SCENE-010の全体画面にはGoogle account、電話番号、IMEI、IP/MAC等が含まれるため、最終成果物にはAndroidバージョン行だけを保存。
- iPhone capture待ちとSCENE-006/014のLINE環境待ちを維持し、draftは生成しない。

## Current result after user-provided probes（2026-09-06）

- Android: **4 / 4**（SCENE-006 / 010 / 014 / 016）。SCENE-006はLINE `26.14.0`、SCENE-014はGoogle Playの実画面で`開く`。
- iPhone: **3 / 3**（SCENE-009 / 013 / 015）。SCENE-013はApp Storeの実画面で`開く`。
- SCENE-005: iPhone実機captureから正式除外し、LINE公式の下限値だけをrenderer-nativeで表示。
- real UI capture: **7 / 7**。fake UI、AI reconstruction、架空の更新ボタンは **0**。
- Visual Gate v3の機械QAは24scene OK / 0 WARN / 0 FAIL。人間確認と発音レビュー前のdraft生成は行わない。
