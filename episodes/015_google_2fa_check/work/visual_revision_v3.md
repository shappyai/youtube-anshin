# Episode 015 visual revision v3

- 確認日: 2026-09-08
- 対象: `output/draft_auto_v3.mp4`
- 状態: `HUMAN_GATE_2_PENDING`
- 方針: 場所の案内は実Google UI、個人情報・秘密情報が表示される先の説明は既存カード

## 実際に確認したGoogle UI

| Scene | 実画面で確認した入口 | raw capture | 内容上の制限 |
|---|---|---|---|
| 004 | `Google にログインする方法` → `2 段階認証プロセス` | `assets/captured/pc/scene_004_google_signin_2sv_entry.jpg` | 設定の入口のみ。メール・電話番号・アカウント名なし |
| 007 | `バックアップ コード` → `バックアップ コードの取得` | `assets/captured/pc/scene_007_google_backup_codes_entry.jpg` | コード一覧を開いていない。数字・QRなし |
| 010 | `パスキーとセキュリティ キー` → `2 件のパスキー` | `assets/captured/pc/scene_010_google_passkey_entry.jpg` | 入口のみ。端末名の一覧を開いていない |

いずれもHumanがログイン済みのテストアカウントを用意した状態で、Codexはログイン・パスワード入力・認証・設定変更を行っていない。

## v2 → v3変更箇所

1. SCENE-004: fallback quote cardを、実Google UIの「2 段階認証プロセス」入口captureへ差し替え。
2. SCENE-007: fallback quote cardを、実Google UIの「バックアップ コード」入口captureへ差し替え。コード本体は表示・保存していない。
3. SCENE-010: fallback quote cardを、実Google UIの「パスキーとセキュリティ キー」入口captureへ差し替え。端末名一覧は表示・保存していない。
4. 後段の説明カード、台本、VOICEVOX音声、実時間字幕、CTA本文は変更していない。
5. `draft_auto_v3.mp4`を再生成し、representative frame contact sheetを追加した。

## QA

- production preflight: PASS
- Phase 2 QA: PASS（FAIL 0 / WARN 0、12 scenes、61 subtitles）
- subtitle preflight: PASS（FAIL 0 / WARN 0）
- VOICEVOX pronunciation preflight: PASS（42/42 queries、review 0）
- viewer-facing text QA: PASS（検出 0）
- CTA preflight: PASS
- backup code digits in saved raw material: 0。Scene 007は入口だけを撮影し、コード一覧を開いていない。
- scene quality report: 9 OK / 0 WARN / 3 FAIL。SCENE-004/007/010のFAILは、gradient背景に対する `background comparison unavailable` という機械判定上の制約であり、実画面の欠落を示すものではない。Scene 010のnear-white判定も同じlayoutの大きな余白に対する機械候補である。
- render: 1920×1080 / H.264 / 30fps / AAC 48kHz mono
- 実尺: 318.740秒（5分18.740秒）

## Human Gate 2で確認する点

1. 元画像およびdraftで、3つの入口名が65歳以上にも読める大きさか。
2. Scene 004の時刻表示、Scene 010の「2 件のパスキー」表示が、今回の目的に対して不要な情報になっていないか。
3. Scene 007にバックアップコード本体がなく、Scene 010に端末名などがないこと。
4. 実Google UIの入口と、その後の説明カードの役割分担が自然か。

サムネイル生成、YouTube upload、publish、finalizeは未実施。
