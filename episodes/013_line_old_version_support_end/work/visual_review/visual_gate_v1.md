# Episode 013 Visual Gate v1

- Episode: `013_line_old_version_support_end`
- 判定日: 2026-09-06
- 対象: Phase A / Visual Gate v1
- 判定: **CONDITIONAL PASS — 実機キャプチャ後の再確認待ち**

## Gate summary

| 確認項目 | 判定 | 根拠 |
|---|---|---|
| 24sceneのレンダリング | PASS | `scene_renderer.py`で24/24枚を生成。contact sheetを目視確認 |
| 共通背景システム | PASS | `adult_digital_soft_background`、section pill、淡いgradient、semantic icon plateを適用 |
| 文字の階層 | PASS | 見出しは80px以上、機械レポートの44px未満は0件 |
| 字幕安全帯 | PASS | subtitle-safe areaの機械チェックPASS。字幕は下部専用帯に配置 |
| アイコン | PASS | `verified_user` / `lock` / `support_agent` / `warning`を意味に合わせて使用。疑似登録アイコンなし |
| 白一色scene | PASS | `blank_white_slide` flagged scenes: 0 |
| 公式UIの正確性 | HOLD | 8sceneは実機キャプチャ予定。現在のneutral visual frameは撮影枠であり、公式画面ではない |
| 最終アップロード可否 | HOLD | 実機キャプチャ、発音レビュー、実尺、字幕同期の確認前 |

## Contact sheet review

`scene_contact_sheet_v1.png`と主要sceneの原寸画像を確認した。

- scene 001〜004: 冒頭の結論と「LINE → OS → 更新」の順序が一目で分かる。
- scene 005〜006: LINEのバージョン確認手順は左に大きく、右は実機差し替え用のneutral frame。架空UIの文字やロゴは入れていない。
- scene 007 / 011: iPhone・Androidの基準を左右カードで比較。比較に意味がある箇所だけ2カラムを使用。
- scene 009〜016: iPhoneとAndroidの操作を時間方向に分離。実機画面は各sceneで大きくcropする設計。
- scene 018〜020: ケースA〜Cを同じsummary構造で整理。ケースDはscene 021で独立させた。
- scene 022〜024: 買い替え前の確認順、機種変更時の準備、まとめの順で、CTAを本編途中に置いていない。
- 全scene: 重要な文字や操作領域が字幕帯と重ならない。contact sheet縮小時でも見出しの重心と色分けが崩れていない。

## Mechanical report

`scene_quality_report_v1.md` の機械判定は次のとおり。

- OK: 15scene
- WARN: 0scene
- FAIL: 9scene
- FAILの内訳: scene 003 / 005 / 006 / 009 / 010 / 013 / 014 / 015 / 016の `visual_centroid_preflight`。いずれも実機背景が未配置のため `background comparison unavailable` となった条件付きFAIL。
- `subtitle_safe_area`: PASS
- `background_consistency`: PASS
- `blank_white_slide`: 0scene
- `overflow`: 0
- `tiny_text`: 0
- `oversized_checkmark_count`: 0
- `decorative_checkmark_as_main_visual`: 0

この9sceneに架空の画面を入れて機械FAILを消すことはしない。実機撮影後、同じscene IDに実素材を配置して再レンダリングし、`visual_centroid_preflight`と公式画面の可読性を再確認する。

## Pending capture list

| Scene | Device | Capture focus | Status |
|---:|---|---|---|
| 005 | iPhone実機 | ホーム → 設定 → LINEについて → 現在のバージョン | CAPTURE_REQUIRED |
| 006 | Android実機 | ホーム → 設定 → LINEについて → 現在のバージョン | CAPTURE_REQUIRED |
| 009 | iPhone実機 | 設定 → 一般 → 情報 → iOSバージョン | CAPTURE_REQUIRED |
| 010 | Android実機 | 設定 → デバイス情報 → Androidバージョン | CAPTURE_REQUIRED |
| 013 | iPhone実機 | App Store → アカウント → LINEの更新 | CAPTURE_REQUIRED |
| 014 | Android実機 | Google Play → プロフィール → アプリとデバイスの管理 | CAPTURE_REQUIRED |
| 015 | iPhone実機 | 設定 → 一般 → ソフトウェアアップデート | CAPTURE_REQUIRED |
| 016 | Android実機 | 設定 → システム → ソフトウェアアップデート | CAPTURE_REQUIRED |

撮影時はテスト端末を使い、Apple ID・Googleアカウント・電話番号・個人名・通知内容が映らない状態にする。端末やOSの違いでメニュー名が変わる場合は、ナレーションを断定せず、画面に出た公式の項目名を優先する。

## Human gate decision

Phase AのVisual Gateとして、templateの構造・文字サイズ・背景・アイコン・字幕安全帯は進行可能と判断する。一方、実機キャプチャが未実施なので、Episode 013を公開候補へ進める判定ではない。人間承認後の状態は `APPROVED_WITH_3_FIXES → CAPTURE_REQUIRED` とする。

次のゲートは、8sceneの実機画面を差し替えた後の原寸可読性確認。その後に、VOICEVOX発音レビュー9件、実尺、字幕同期、thumbnail / publish reviewを行う。

## Human approval addendum — 2026-09-06

Human Gate: **APPROVED_WITH_3_FIXES**。

反映した修正:

1. 終了CTAを旧 `channel_common_cta` 指定から外し、Episode011 / 012で人間承認・実使用された `registration_conversion_v1` の音声・PNG・canonical textを再利用する設定へ変更。
2. SCENE-004 / 008 / 012のsemantic iconにscene別サイズ（plate 150px / glyph 96px）を設定し、番号と確認内容を第一階層にする。
3. SCENE-018の見出しを「ケースA　今回は対応不要」へ変更。直前のナレーションで、LINE・OSとも基準以上かつ必要な更新ができる条件を明記。長い見出しがsection pillと重ならない専用領域も設定した。

CTAの照合:

- audio SHA-256: `1D21F765F5606310CA08BC0264EC6ED0136F68F5A7DA07318B5018F1735FDBC9`
- visual SHA-256: `96EFB5195CD7F3D7121472A79F300AF19999108186D6B35C370EFA488185EAE0`
- duration: 15.000秒（audio 11.456秒 + tail 3.544秒）
- 中盤CTA: 0 / duplicate CTA: 0 / fake subscribe UI: 0

## Capture search result — 2026-09-06

- Episode 013に紐づく有効なiPhone／Android実機キャプチャは確認できなかった（0 / 8 scene）。
- `local/slot3_scene_013.png` と `local/slot4_scene013.png` は別案件のGoogle Play／マイナアプリ画面で、LINEの実機UIではないため採用しない。
- Phase Bの候補レンダーには8sceneのneutral frameが残るが、ドラフト動画には使用しない。実機素材が揃うまで `CAPTURE_REQUIRED` とする。
