# Shotlist — Episode 005 Googleフォト「削除」と「空き容量を増やす」の違い

方針: AndroidのGoogleフォト操作は **Android Emulator** を主役、iPhone（Apple「写真」アプリ・「最近削除した項目」）は **iPhone実機またはApple/Google公式ページ**、概念・安心・人物は **GPT画像**（GoogleフォトのUI・ロゴはAIで再現しない）、一覧・比較・チェック・まとめは **Codexテンプレート**。Phase B前半で取得できた実画面・公式ページcropを反映し、未取得の復元画面は推測で補わない。

Phase B前半時点で、GPT画像5枚は `assets/generated_ai/`（原本）と `work/phase_b_review/normalized_ai/`（1920×1080レビュー用）、Android撮影cropは `assets/captured/android/`、公式ページcropは `assets/official/` に置く。iPhone実機は未使用で、公式ページfallbackを採用する。

| Shot | Scene | Device | Render mode | 内容 | Asset / 画面表示 | 字幕安全領域 |
|---|---:|---|---|---|---|---|
| SHOT-01 | SCENE-004 | 保存済みGoogle公式ページ | official（公式） | 1 / 6 バックアップ確認。「バックアップが完了しました」の表示を確認 | `assets/official/google_photos_backup_android_crop.png`。公式ヘルプの該当本文をcrop。Android実機の個別写真詳細とは表現しない | 下180pxを空ける |
| SHOT-02 | SCENE-006 | Android Emulator | official（実画面） | 2 / 6 写真選択→ゴミ箱アイコン。sceneはタップ前で停止 | `assets/captured/android/delete_photo_trash_crop.png` 取得済み。自作ダミーのゴミ箱操作を中央crop。削除後画面は示さない | 下180pxを空ける |
| SHOT-03 | SCENE-008 | Android Emulator | official（実画面） | 2 / 6 ゴミ箱画面（保持期間の案内）。60日/30日の数字は実画面で確認 | `assets/captured/android/trash_days_crop.png` 取得済み。「ゴミ箱は空です」＋60日/30日の案内。アイテム表示は未取得 | 下180pxを空ける |
| SHOT-04 | SCENE-012 | Android Emulator | official（実画面） | 3 / 6 メニュー→「デバイスから削除」項目の表示 | `assets/captured/android/delete_from_device_crop.png` 取得済み。機種差の留保を字幕で明示 | 下180pxを空ける |
| SHOT-05 | SCENE-014 | Android Emulator | official（実画面） | 4 / 6 「このデバイスの空き容量を増やす」→対象確認→押す前で停止 | `assets/captured/android/free_up_space_crop.png` 取得済み。自作ダミー13.40 KB、実行ボタンは押していない | 下180pxを空ける |
| SHOT-06 | SCENE-018 | 保存済みGoogle/Apple公式ページ | official（公式） | 5 / 6 iPhone本体の写真とGoogleフォトにバックアップされた写真で、削除時の扱いが違うことを確認 | `assets/official/google_photos_delete_ios_crop.png` ＋ `assets/official/apple_guide_delete_photos_crop.png`。実機結果とは表現しない | 下180pxを空ける |
| SHOT-07 | SCENE-019 | 保存済みApple公式ページ | official（公式） | 5 / 6 「最近削除した項目」画面（30日保管の案内） | `assets/official/apple_recently_deleted_crop.png` 取得済み。viewport版のnull表示は不採用 | 下180pxを空ける |
| SHOT-08 | SCENE-022 | 保存済みGoogle公式ページ | official（公式手順） | 6 / 6 ゴミ箱→写真選択→「復元」まで。復元先は公式本文の範囲だけ説明 | `assets/official/google_photos_restore_android_steps_crop.png`。現行Google公式ヘルプの手順部分をcrop。Android実画面の完全再現ではない | 下180pxを空ける |
| — | SCENE-001 | GPT画像（生成済み） | gpt_image | 導入。写真整理に困るシニアの安心感 | `assets/generated_ai/scene_001.png` 原本検証済み（1672×941）。レビュー時に1920×1080へ正規化 | 下180pxを空ける |
| — | SCENE-002 | Codexテンプレート | template | 今日確認すること3項目の一覧 | `layout_02_list`。文字中心（1.バックアップ 2.削除と空き容量を増やすの違い 3.ゴミ箱からの復元） | 下180pxを空ける |
| — | SCENE-003 | GPT画像（生成済み） | gpt_image | 1 / 6 セクション扉。バックアップ=コピーをGoogleに預ける概念 | `assets/generated_ai/scene_003.png` 原本検証済み（1672×941）。レビュー時に1920×1080へ正規化 | 下180pxを空ける |
| — | SCENE-005 | Codexテンプレート | template | 2 / 6 セクション扉 | `layout_08_section`。「削除」を押すと、何が起きる？ | 下180pxを空ける |
| — | SCENE-007 | Codexテンプレート | template | 「何が消えるか」比較表の初出し（削除行をハイライト） | `layout_05_compare`。3操作×（スマホ本体/Googleフォト）。SCENE-011・015と同一レイアウト | 下180pxを空ける |
| — | SCENE-009 | Codexテンプレート | template | 「削除」前のひとこと確認（注意カード） | `layout_06_caution`。恐怖演出にしない | 下180pxを空ける |
| — | SCENE-010 | Codexテンプレート | template | 3 / 6 セクション扉 | `layout_08_section`。「デバイスから削除」とは？ | 下180pxを空ける |
| — | SCENE-011 | Codexテンプレート | template | 比較表の「デバイスから削除」行ハイライト | `layout_05_compare`（SCENE-007と同一）。スマホ本体:消える／Googleフォト:残る | 下180pxを空ける |
| — | SCENE-013 | GPT画像（生成済み） | gpt_image | 4 / 6 セクション扉。スマホ本体の容量が空く概念 | `assets/generated_ai/scene_013.png` 原本検証済み（1672×941）。字幕帯への一部重なりはWARNとして人間確認 | 下180pxを空ける |
| — | SCENE-015 | Codexテンプレート | template | 比較表の「空き容量を増やす」行ハイライト | `layout_05_compare`（SCENE-007と同一）。スマホ本体:消える／Googleフォト:残る | 下180pxを空ける |
| — | SCENE-016 | Codexテンプレート | template | スマホ本体の容量とGoogleアカウントの容量は別もの（2つの箱の図解） | `layout_03_visual_text` 相当の2ボックス図。templateで正確な日本語 | 下180pxを空ける |
| — | SCENE-017 | GPT画像（生成済み） | gpt_image | 5 / 6 セクション扉。iPhone本体の写真とGoogleフォトにバックアップされたコピーで、削除時の扱いが違う概念 | `assets/generated_ai/scene_017.png` 原本検証済み（1672×941）。1枚の写真からバックアップコピーへ流れる構図 | 下180pxを空ける |
| — | SCENE-020 | Codexテンプレート | template | 2つのゴミ箱の左右比較（Google 60日/30日 vs 最近削除した項目 30日） | `layout_05_compare`。別物であることを明示 | 下180pxを空ける |
| — | SCENE-021 | Codexテンプレート | template | 6 / 6 セクション扉。間違えて消しても復元できる | `layout_08_section`。ゴミ箱の説明はSCENE-008参照（重複しない） | 下180pxを空ける |
| — | SCENE-023 | Codexテンプレート | template | 消したことに気づいたら早めにゴミ箱確認（安心カード） | `layout_06_caution` | 下180pxを空ける |
| — | SCENE-024 | Codexテンプレート | template | まとめ4項目（seg 61〜64に同期して1件ずつ表示） | `layout_07_summary`＋summary_stagger。要点のみ | 下180pxを空ける |
| — | SCENE-025 | GPT画像（生成済み） | gpt_image | クロージング。家族と一緒に確認する安心の光景 | `assets/generated_ai/scene_025.png` 原本検証済み（1672×941）。レビュー時に1920×1080へ正規化 | 下180pxを空ける |
| — | CTA | Codexテンプレート | template | channel_common_cta（ナレーションなし・約10秒） | `work/channel_cta.png` Phase Bで作成。config/channel_cta.json準拠 | 下180pxを空ける |

## 公式素材の表示ルール

- Googleフォトの操作画面はAIで再現しない。AndroidはEmulator実画面（Phase B）、iPhoneは実機またはApple/Google公式ページのスクリーンショット（SRC-016/017等）を使用。
- 「デバイスから削除」「このデバイスの空き容量を増やす」等のメニュー名、60日/30日等の数字は、Codexテンプレートまたは実画面で正確に表示し、GPT画像では生成しない。
- テスト素材は個人写真・位置情報・実在のGoogleアカウント情報が映らない安全なものだけを使用（Emulatorのテストアカウント・ダミー画像）。

## 実機・媒体選択の根拠

- Googleフォトアプリ（Android）の操作 → 撮影媒体の選択ルールの「Android OS/Androidアプリ→Android Emulator」に該当。Emulatorを主役にする。
- iPhone固有のApple「写真」アプリ・「最近削除した項目」→ 「iPhone固有設定→iPhone」に該当。実機または公式ページを優先。
- 概念・安心・人物（導入・バックアップの概念・容量が空く概念・本体写真とバックアップコピーの扱い・クロージング）→ GPT画像（Phase 2標準の役割分担）。
- 一覧・比較・注意・まとめ → Codexテンプレート（正確な日本語を後描画）。
