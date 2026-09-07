# Phase A preflight — Episode 007

確認日: 2026-09-03　基準: `episodes/007_myna_app_login/` のcanonical file一式（Analyticsパッチ反映済み）

| 項目 | 判定 | 備考 |
|---|---|---|
| schema | **PASS** | JSON構造検証OK（61 segments・61 subtitles・22 scenes・14 sources・postroll=channel_common_cta）。schema検証script（episode_io）はサンドボックスで実行不可のため、構造検証はPowerShell JSONパースで実施（Phase B開始時にepisode_io.validate_episodeを実行する） |
| sources | **PASS** | 一次情報14件（デジタル庁・マイナポータル・マイナンバーカード総合サイト・J-LIS・Apple/Google）。2026-08-30キャプチャ（local/web_check_002/）＋2026-09-03 web検索要約併用。まとめサイト・二次記事不使用。「未確認・要人間確認リスト」で数値系を明記 |
| official facts | **PASS（REVIEW 5）** | Fact Check: FAIL 0件／REVIEW 7件（ナレーション5・sceneテキスト1・description 1）。数値系（3回連続ロック・10回目/5回目の誕生日・3か月前・受付時間）はweb要約由来のため**撮影時に人間が公式ページ本文で最終確認**。REVIEW-2（発行日表記）・REVIEW-6（002タイトル表記）は反映済み |
| current branding | **PASS** | 正式名称は「マイナアプリ」で統一（旧名「マイナポータルアプリ」は本編テキストに出現なし・metadata/SRC/end_screen候補のみ）。ストア併記名は撮影時に実画面確認 |
| script | **PASS** | 61ナレーションセグメント・第一目標5:30〜6:15+CTA・1文1segment・冒頭20秒以内に結論＋5項目一覧・SHOT-01〜09 |
| fact check | **PASS（REVIEW 7）** | `work/subagents/007_myna_app_login/fact_check.md`。FAIL 0件。REVIEW7件は数値系要人間確認＋説明欄002タイトル（反映済み） |
| subtitles | **PASS** | 61字幕とナレーション1:1（行分割のみ・言い換え0件）。72px・最大2行・下部帯はPhase B字幕工程で確定（実尺タイミング） |
| scene mapping | **PASS** | 22 sceneがsegment 1〜61を重複・欠落なくカバー（visual_plan.jsonで突合済み） |
| render modes | **PASS** | template 12 / official 8（公式Web crop 6・実機読み取り実演 2※fallback可）/ gpt_image 2＋CTA。マイナアプリの実UIのAI再現なし |
| TV readability | **PASS（REVIEW 7）** | TV_READABILITYをQA項目に追加。全sceneで下180px字幕帯確保。一覧・注意・比較の文字量（scene 2/10/16/21）とsupport_text長（4/12/19/20）は人間のcontact sheet確認へ |
| text provenance | **PASS** | 旧Episode固有語（ニセ警察・国際電話・Googleフォト・LINE等）の混入なし。Analytics数値は本編に出現なし |
| item count | **PASS** | オープニング（seg 4〜10）とまとめ（seg 54〜61・scene 21）が同じ5項目・同じ順・同一文言。5項目一覧の表示は冒頭とまとめの2回のみ |
| linebreak QA | **PASS（Phase B確認）** | subtitle_preflightはPhase Bで実施予定（PROTECTED_TERMS候補: マイナアプリ・マイナポータル・マイナンバーカード・利用者証明用暗証番号・電子証明書・暗証番号・シークレットモード・プライベートブラウズ・フリーダイヤル・障害・メンテナンス・再設定・iPhone・Android・NFC・iOS） |
| pronunciation | **REVIEW可** | `work/pronunciation_candidates.md` に候補一覧（33件）。辞書は未変更（人間試聴後に承認分のみ登録） |
| privacy plan | **PASS** | 本物のマイナンバー・氏名・生年月日・住所・顔写真・カード表裏・暗証番号・QRコードを映さない（テストカード/完全隠しのみ）。実機アカウント情報はモザイク/見切らせ。visual_plan.jsonのpersonal_data_riskに全scene展開 |
| gpt images | **NOT GENERATED** | 2枚予定（scene 7・22）。manifestとpromptsは準備済み（`work/image_generation_manifest.md`・`work/scene_prompts/`）。Phase Bで1 Image Agent=1 scene=1 image |
| captures | **NOT STARTED** | SHOT-01〜09はmedia_manifest.csvに計画登録。実画面撮影はPhase B。公式Web cropの取得はPCブラウザ/保存HTML |

## Analyticsパッチ反映QA（ユーザー指定25項目）

| 項目 | 判定 | 備考 |
|---|---|---|
| title | PASS | 仮タイトル維持【マイナアプリ】ログインできない？まず確認したい5つ。SEO詰め込みなし |
| hook | PASS | 0〜5秒で困りごと→5〜15秒で「確認するのは5つ」→15〜25秒で一覧。チャンネル紹介・歴史・002の長い振り返りなし |
| 5-item consistency | PASS | 冒頭＝まとめ（同一5項目・同一順）。一覧表示は2回のみ |
| problem-first order | PASS | 困り方順（①スマホ対応②読み取り③暗証番号④期限⑤再設定・窓口）。読み取り開始約1:15・暗証番号開始約2:25（前半50%以内） |
| script length | PASS | 61 segments・目標5:30〜6:15+CTA（7分超を目標にしない） |
| scene mapping | PASS | 22 scene+CTA。1画面1メッセージ |
| TV readability plan | PASS（REVIEW→人間確認） | 大文字・1画面1メッセージ・大胆crop・下180px帯維持・色だけで区別しない |
| official UI plan | PASS | 全体2〜4秒→大きくcropの2段階。小さな全画面中央配置禁止。1920×1080 frameで確認 |
| privacy | PASS | 撮影禁止物の一覧をmanifest・visual_plan・shotlistに明記 |
| Episode 002 separation | PASS | 本編での002宣伝は終盤1文のみ。002の解説を繰り返さない |
| cross-link plan | PASS | 説明欄の002関連動画リンク構造（タイトル表記反映済み）。video IDはrepoに存在しないため公開時に人間確認（推測しない） |
| CTA | PASS | channel_common_cta固定+本編終盤にブリッジ1seg（「こうしたスマホの困りごとを、これからも、分かりやすく、確認していきます」） |
| linebreak | PASS（Phase B確認） | 禁則・保護語はPhase Bのsubtitle_preflightで機械QA |
| fact check | PASS（REVIEW 7） | FAIL 0件。数値系は撮影時人間確認 |

## 結論

Phase A必須項目はPASS（数値系REVIEWは撮影時最終確認へ繰り越し）。GPT画像・実画面撮影・VOICEVOX・字幕実尺・video build・thumbnail・YouTubeは**未実施**。次は人間レビュー（Gate 1: テーマ・台本・scene plan）。

## 2026-09-03 追記（数値REVIEW解消・imagegen_native A/Bテスト前）

| 項目 | 判定 | 備考 |
|---|---|---|
| official facts | **PASS（REVIEW 0）** | 数値系REVIEW 7件を公式ページ本文の直接取得で全解消（`local/web_check_007/` 21ファイル）。3回連続ロック・10回目/5回目の誕生日・3か月前・0120-95-0178受付時間・iPhone/Android読み取り位置・シークレットモード・障害ページ・コンビニ再設定のすべてを本文一致で確認。台本の独自表現（「カメラのあたり」等）は公式文言へ同期（SEG 21/22/24/42・scene 8/9） |
| fact check | **PASS（REVIEW 0）** | FAIL 0／REVIEW 0（解消済み・全61セグメントPASS）。詳細は `work/subagents/…/fact_check.md` セクション9 |
| gpt images | NOT GENERATED（A/B用の1枚のみ生成） | 下記A/Bテスト参照。SCENE-007/022のコンセプト画像は未生成のまま |

## imagegen_native A/Bテスト（2026-09-03・人間比較待ち）

対象scene: **SCENE-003（1/5 セクション扉「スマホが、対応しているか」）**。表示文言はepisode.jsonの正（headline「スマホが、対応しているか」2行・支援「まずは、端末とアプリの準備から。」1行）。

- Candidate A: imagegen_native（背景＋日本語文字を一体生成）→ `work/phase_b_review/ab_test_candidate_A.png`（原本1672×941・16:9・1920×1080正規化copyを比較画像に使用）
- Candidate B: 既存renderer（本番パイプライン、layout_08_section＋Codex文字後描画・Edgeレンダリング）→ `work/phase_b_review/ab_test_candidate_B.png`（1920×1080）
- 比較画像: `work/phase_b_review/imagegen_native_ab_test.png`（左A・右B・ラベルは画像外）
- QA: Aの文字完全一致（見出し2行＋補助1行を目視で確認・余計な文字なし）／TV readability（大見出し）／下部180px相当の安全領域に文字・オブジェクトなし（ピクセル検査・min 252）／公式UI・ロゴ・QR・個人情報なし／collageなし。Bは決定論的描画のため文字100%正確
- 生成時間: imagegen_native=約32.0秒（ツール実測wall clock）／renderer=22 scene一括で約52秒（B単体の実測なし→null。1sceneあたり約2.4秒相当）／imagegen_native再生成回数=0

**停止: A/Bの人間比較待ち**（残りのsection扉・SCENE-007/022・全scene render・VOICEVOX・draft・thumbnail・YouTubeは未実施）
