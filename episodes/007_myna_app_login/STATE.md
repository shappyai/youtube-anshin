# Episode 007 State

- status: finalized
- human_approved: true
- phase: Phase A
- research_date: 2026-09-03
- title（候補・第一推奨）: 【マイナアプリ】ログインできない？まず確認したい5つ
- slug: myna_app_login
- analytics_patch_applied: true（2026-09-03・Episode 002 Analyticsを踏まえた改善を反映）

## 企画の結論

「マイナアプリでログインできない」を一つの原因として扱わず、視聴者が実際に止まる順番（困り方順）で5つ確認する:

1. **スマホが対応しているか**（iOS 16.4以上／Android 11以降＋NFC・端末ロック必須・アプリ最新版・通常モード）
2. **カードを読み取れない場合**（背面上部をぴったり・iPhoneは本体上部・動かさない・ケース/金属机/充電ケーブル注意）
3. **暗証番号で止まる場合**（ログインで使うのは数字4桁・3回連続でロック・何度も試さない・顔/指紋も可）
4. **カードや電子証明書の期限**（カード=10回目の誕生日・証明書=5回目の誕生日・別もの・更新は3か月前から）
5. **それでもダメなら**（障害・メンテナンス確認→再設定（コンビニはもう一つの番号が必要・窓口）→マイナンバー総合フリーダイヤル 0120-95-0178）

## Analyticsパッチ（Episode 002実績反映・2026-09-03）

- Episode 002実績: 視聴4,718回・総再生108.2時間・登録+9・CTR 5.5%・平均視聴3:23・ブラウジング/ホーム流入94-97%・**テレビ視聴約52.5%**（本編に出さない）
- 尺: 5:30〜6:15+CTA（7分超を目標にしない）／GPT画像: 2枚／scene: 22+CTA
- 冒頭20秒を強化（問題→5項目→一覧）・5項目は困り方順・読み取り/暗証番号を前半50%以内・TV-first readabilityをQA項目化・002との相互導線パッケージ準備・固定コメントcandidate・CTAは共通固定＋ブリッジ1seg

## 一次情報（2026-09-03）

- 重要ページの当日再取得はネットワーク制限で失敗（`local/web_check_007/` は0件）。2026-08-30キャプチャ（`local/web_check_002/`）＋2026-09-03 web検索による公式サイト要約を併用（SRC-001〜014）。
- **数値系（3回連続ロック・10回目/5回目の誕生日・更新3か月前・フリーダイヤル受付時間・対応OS/読み取り位置）は撮影時に人間が公式ページ本文で最終確認**（sources.mdの「未確認・要人間確認リスト」・Fact Check REVIEWに吸収）。

## Phase A 成果物

- `brief.md`（Analytics仮説・KPIチェックリスト含む）／`sources.md`（SRC-001〜014）／`script.md`（61ナレーションセグメント・5:30〜6:15目標）／`shotlist.md`（※planはmedia_manifest.csvとvisual_plan.jsonに集約）／`episode.json`（schema検証: PowerShell JSONパースPASS・61 segment・61 subtitle・22 scene・14 source。episode_io.validate_episodeはサンドボックスで実行不可のためPhase B開始時に実施）／`publish.json`（metadata draft・相互導線・固定コメント・KPIチェックリスト）／`media_manifest.csv`（SHOT-01〜09計画）／`STATE.md`
- `work/subagents/007_myna_app_login/`: research_report.md（親Codex補完セクション6含む）・title_analysis.md・script_review.md・fact_check.md・visual_plan.json
- `work/`: scene_mode_advisor.md・image_generation_manifest.md・scene_prompts/scene_007.md・scene_022.md・pronunciation_candidates.md・phase_a_preflight.md・production_metrics.json
- 成果物の配置はEpisode 005/006の慣例に従い、agent成果物は`work/subagents/007_myna_app_login/`、上記`work/`配下は`episodes/007_myna_app_login/work/`に置いた（ユーザー指定の「work/」はエピソード別workディレクトリとして解釈）

## Fact Check（2026-09-03）

- **FAIL 0件 / REVIEW 7件**（ナレーション5・sceneテキスト1・publish.description 1）／PASS 54件（ナレーション56・scene/SRC系）
- REVIEWは数値系の「要人間確認」（3回・10回目/5回目・3か月前・受付時間）と説明欄の002タイトル表記。REVIEW-2（発行日表記）・REVIEW-6（002正式タイトル表記）は反映済み。残り5件は撮影時Human Gate
- 5項目の一貫性（冒頭＝まとめ）PASS・字幕61件ナレーションと完全一致・禁止表現・旧002仕様流用なし

## Human Gate（次のゲート）

1. **テーマ・台本・scene planの人間レビュー（ここで停止中）** — Gate 1: テーマ・台本・scene plan
2. scene contact sheet＋pronunciation REVIEW（Phase B前半）
3. full draft（Phase B後半）
4. thumbnail / publish（Phase B後半）

## 停止位置（Phase A）

まだ行わない: GPT画像生成（manifest/prompts準備済み）・Android/iPhone撮影・カード撮影・VOICEVOX本編・video build・thumbnail生成・YouTube操作。

## 補足

- 002相互リンク: Episode 002のvideo ID/URLはrepo内（publish.json・STATE等）に存在しないため**推測しない**。公開時に人間が確認して説明欄「マイナアプリの変更点はこちら」リンク・終了画面（002を第一候補）を設定。002側への007導線追加は007公開後のHuman Publish Checklistに記録。
- 固定コメントはcandidateのみ（自動投稿しない）。
- CTAは `config/channel_cta.json` の `channel_common_cta` をそのまま使用（新規CTAを作らない）。「怖がらせる前に、確認する。」はCTAに含めない。

## 数値REVIEW解消（2026-09-03・公式本文直接取得）

- ユーザー指示により、web検索要約ではなく公式ページ本文の直接取得で数値系REVIEWを解消。`local/web_check_007/` に21ファイル保存（有効19）。
- 確認済み: ロック回数（利用者証明用=連続3回・署名用=5回・自動解除なし・jpki_faq_digital_id.html）／カード=18歳以上発行から10回目の誕生日・電子証明書=年齢問わず5回目・更新3か月前から市区町村窓口（digital_expiration_date.html）／0120-95-0178平日9:30〜20:00・土日祝9:30〜17:30（kojinbango_contact_tel.html）／iPhone背面上部をぴったり・動かさず待つ・Android背面の読み取り位置・ケース/金属机/ケーブル注意（mynaapp_scan_mynumbercard・jpki_iphonefaq.pdf）／シークレットモード→通常モード・EDZ207（FAQ記事）／障害・メンテナンスページ（myna_info_index.html）／コンビニ再設定（jpki_reset_kiosk.html）。動作環境・利用登録もpagedata本文一致。
- 台本を公式文言へ同期（SEG 21/22/24/42・scene 8/9・SUB同期。字幕61件とナレーションの一致を再検証OK）。Fact Check: **FAIL 0 / REVIEW 0（全解消）**。
- sources.md / fact_check.md / phase_a_preflight.md / production_metrics.json を同期。

## imagegen_native A/Bテスト（2026-09-03・人間比較待ちで停止）

- 対象: **SCENE-003（1/5 セクション扉）**。表示文言: 「スマホが、対応しているか」+「まずは、端末とアプリの準備から。」
- Candidate A（imagegen_native・背景＋文字一体生成）: `work/phase_b_review/ab_test_candidate_A.png`（原本1672×941・16:9・文字完全一致・下部安全領域OK・公式UI/ロゴなし。生成約32秒・再生成0回）
- Candidate B（既存renderer・文字後描画・本番パイプライン）: `work/phase_b_review/ab_test_candidate_B.png`（1920×1080・文字100%正確・見出し104px）
- 比較画像: `work/phase_b_review/imagegen_native_ab_test.png`（左A・右B・ラベルは画像外）
- 停止: **A/Bの人間比較待ち**。A承認→残りsection扉もimagegen_native／B承認→Episode 007は従来方式（一般ルール化はしない）。SCENE-007/022のコンセプト画像・全scene render・VOICEVOX・draft・thumbnail・YouTubeは未実施。

## Phase B前半（2026-09-03・画像生成サービス障害により一部保留）

### 恒久ルール反映（A/B結果）
- AGENTS.md「画像の文字レンダリング方針」: imagegen_native（背景＋短い日本語文字一体生成）をsection扉・concept title sceneの正式第一候補へ。exact text QA必須（1文字でも誤ればFAIL）・fallbackは該当sceneのみ（1回再生成→2回目不安定ならcodex renderer）・進行pillはCodex後付け可（hybrid）・表示文字は大見出し1〜2行＋補助0〜1行（30〜40文字以下推奨）。
- docs/text_render_policy.md: セクション10「A/B実績と恒久化」を追記（人間がCandidate Aを採用した2026-09-03実績・棲み分け・QA・fallback・hybrid・metrics記録項目）。
- docs/episode003_retrospective.md: 旧「正確な日本語はCodexで後描画する」を新ルールへ更新。
- scripts/hybrid_scene_renderer.py: template＋imagegen_native のsceneをfull-bleed配置（文字オーバーレイなし）するルーティングを追加。
- official UIのAI生成禁止・Codex renderer優先行（一覧・比較・手順・数字・長文・公式仕様・注意・表・CTA）は維持。

### Episode 007 成果物（Phase B前半）
- SCENE-003: Candidate A正式採用 → `assets/generated_ai/scene_003.png`（1920×1080正規化）。A/B比較成果物は保持（ab_test_candidate_A/B.png・imagegen_native_ab_test.png）。
- official引用カード8枚: `assets/official/quote_*.png`（SCENE-004/005/008/009/012/015/018/019）＋公式読み取りイラスト2点。episode.jsonのofficial_asset/full_bleed_assetへ反映。media_manifest.csv更新。
- pronunciation preflight: VOICEVOX 剣崎雌雄/ノーマル 61/61 audio_query（`work/phase_b_review/pronunciation_preflight.md`）。REVIEW 8件＝文脈依存語（上・方・生・今日）の自動フラグ・エンジン読みは全て正しい。辞書変更なし。
- render: 17/22 scene（`work/rendered_final_scenes/`）。missing: SCENE-007/011/014/017/022（画像生成サービス障害により未生成）。
- QA: 描画17 scene 1920×1080・下180px安全領域クリア（active比≦0.08）／assets 11件で重複SHA 0／字幕61件とナレーション一致0件。
- contact sheets: `work/phase_b_review/scene_contact_sheet.png`・`work/phase_b_review/imagegen_native_text_contact_sheet.png`（SCENE-003採用＋5枚はPENDINGラベル）。
- preflight: `work/phase_b_review/production_preflight.md`。metrics: `work/production_metrics.json` 更新。

### ブロッカー（外部要因）
- 画像生成サービスが一時障害（image_gen 呼び出しが HTTP 404）。親Codex・サブエージェントとも確認。SCENE-007/011/014/017/022（imagegen_native text 4枚＋concept 2枚）は生成待ち。復旧後に1 scene=1 generationで生成→exact text QA→再render→contact sheet更新。

### 停止位置
今回実施しない: 本編VOICEVOX wav生成・字幕final timing・draft video・final・thumbnail・YouTube upload。次は人間レビュー（scene contact sheet＋imagegen_native text contact sheet＋pronunciation 8件）→画像サービス復旧後の残り5 scene生成。

## Visual局所修正（2026-09-04・人間レビュー反映）

人間レビューの指摘（SCENE-001/020の緑チェック過大・SCENE-006/010/013の黄色「!」の野暮ったさ）を反映し、**5sceneのみ再render**（他17sceneはreuse）。

- SCENE-001: 巨大緑チェックカード廃止→「ログインできない？」見出しを中央主役に、小さな緑丸バッジをsymbol-rowで上部補助。
- SCENE-020: 巨大チェック廃止→青「相談」バッジ（窓口・相談の案内ニュアンス）＋見出し主役。
- SCENE-006/010/013: 巨大黄色「!」カード廃止→小さなクリーム「!」バッジ＋「注意」ラベル＋中央テキスト。
- 共通template: hero/visual_text/cautionを「見出し主役＋補助バッジ」へ更新（HTMLテンプレート・styles.css・PILフォールバックの両パス。layout_08_section等の単一シンボルも小型化）。折返しは text-wrap: balance＋幅調整＋ASCII token不可分（20:00等を分断しない）で改善。
- QA: oversized_single_icon 5/5 PASS（バッジ最大108px＝画面の5.6%×10%・閾値15%未満）。text/字幕/fact/ナレーション・item countは無変更。
- 成果物: `work/rendered_final_scenes/scene_001/006/010/013/020.png`（更新）・`work/phase_b_review/scene_contact_sheet_v2.png`・`work/phase_b_review/icon_fix_comparison.png`。
- 恒久ルール: `templates/scenes/README.md`（単一アイコン補助要素・oversized_single_icon定義）・`AGENTS.md` Visual rules・`scene_renderer.py`（wrap ASCII token保護拡張・draw_badge導入）。
- 次は人間Visual確認（contact sheet v2・icon_fix_comparison）。本編VOICEVOX・draft・thumbnail・YouTubeは未実施。

## semantic SVG icon版（2026-09-04・人間レビュー反映）

人間レビュー「小さな丸バッジ＋!/✓はサイズは解消したが見た目がダサい・UIバッジ感が強い」を受け、**Material Symbols Rounded（Google公式・Apache License 2.0）を導入**し、問題の5sceneを再デザインした。旧・丸バッジ版は `work/phase_b_review/icon_badge_v1/` に退避（比較用に保持）。

- SCENE-001: loginアイコン（navy）・淡い青灰円 / 見出し「ログインできない？」主役
- SCENE-006: lockアイコン（blue）・淡いブルー円 / 見出し主役
- SCENE-010: contactlessアイコン（blue）・淡いブルー円 / 見出し主役
- SCENE-013: blockアイコン（amber）・淡いベージュ円 / 見出し主役（恐怖の赤×なし）
- SCENE-020: support_agentアイコン（green）・淡いミント円 / 見出し主役
- 実装: sceneデータの `icon_name`/`icon_tone` → `draw_icon_stage`（PIL）・`semantic_icon_html`（HTML）。fallbackは従来バッジ。背景円はICON_CIRCLE/toneクラス。150〜220px（目安180px）・画面面積15%未満。
- アセット: `assets/icons/material_symbols/`（SVG 6点＋tint PNG 5点）・`assets/icons/LICENSES.md`（provenance）・`config/icon_catalog.json`（意味→アイコン）。media_manifest.csvにICON-001〜005追記。
- 恒久ルール: `templates/scenes/README.md`（semantic SVG基準へ更新）・`AGENTS.md`（Visual rules更新）。
- QA: oversized_single_icon維持（面積比15%・semantic icon=1.6% PASS）／semantic_icon_quality automated PASS＋人間目視REVIEW。
- contact sheet v3: `work/phase_b_review/scene_contact_sheet_v3.png`／比較画像: `work/phase_b_review/semantic_icon_comparison.png`（OLD=丸バッジ / NEW=semantic icon）。
- 次は人間Visual比較（semantic_icon_comparison・contact sheet v3）。本編VOICEVOX・draft・thumbnail・YouTube・画像生成待ち5scene（007/011/014/017/022）は未実施のまま。

## Visual polish（2026-09-04・人間レビュー反映 第2弾）

- semantic SVG icon版（SCENE-001/006/010/013/020）は人間正式承認。以降のルールとして確定。
- Visual polish review（subagent）で全22sceneを分類: KEEP 6／OFFICIAL KEEP 6／IMAGEGEN 5（生成待ち）／ICON IMPROVE 2（任意）／LAYOUT FIX 3（008/009必須・021軽微）。レポート: `work/subagents/007_myna_app_login/visual_polish_review.md`
- **SCENE-008/009**: 左テキストカラム（x≤1010）＋右公式イラストパネル（x≥1060）の2カラムに再設計。text_asset_overlap QA PASS（0.35%/0.56% < 1%）。「iPhoneは本体の上部／Androidは背面の読み取り位置」が一瞬で伝わる構成。
- **SCENE-012/015/018/019**: 公式引用カードに semantic icon 追加（dialpad/badge/construction/lock_reset・blue）。出典・確認日・注記は折返し対応で見切れなし。
- **SCENE-004/005**: 引用・出典の視覚整理（公式文言は不変）。**SCENE-002/016**: soft_gradient背景を適用し「白すぎ」を改善。**SCENE-021**: まとめ行間を詰めて字幕帯（y≥900）侵入を解消。
- **imagegen_native 5scene**（007/011/014/017/022）: サービス復旧後に生成・exact text QA 5/5 PASS（目視確認済み）→ assets/generated_ai/ へ1920×1080正規化配置。**22/22 render完了**（11枚polish・11枚reuse）。
- stub整理: 未参照確認の上、404-stub SVG 6・白背景中間PNG 6 を削除（公式SVG・tint PNG・LICENSES.md は保持）。
- contact sheet v4: `work/phase_b_review/scene_contact_sheet_v4.png` ／比較画像: `work/phase_b_review/visual_polish_comparison.png`（OLD=v3退避版 / NEW）／QA: `work/phase_b_review/visual_polish_qa.md`
- 次は人間による最終contact sheet確認（v4）。本編VOICEVOX・字幕実尺・draft・thumbnail・YouTubeは未実施。

## 最終Visual調整（TV可読性・2026-09-04 人間レビュー反映 第3弾）

- 人間レビュー「TV視聴では本文が小さい・余白より文字を大きく」を受け、対象8scene（004/005/008/009/012/015/018/019）を**3階層構造**で再設計: Level1＝視聴者が覚える要点（66〜96px・本文も最大）／Level2＝公式の短い根拠（48〜56px・文節改行）／Level3＝出典・確認日（24〜26px・下部に分離。完全URLは画面非表示としmanifest/sources/descriptionに保持）。
- **SCENE-005 / 015 の overflow を解消**（wrap未適用で引用が右端へはみ出していた。文節単位分割 wrap_jp を導入し、overflow 最終0を機械検査で確認）。
- SCENE-004: L1「対応OS：iOS 16.4以上／Android 11以降＋NFC」68px／008: L1「iPhoneは、本体の上部」72px・2カラム維持／009: L1「Androidは、本体の背面の読み取り位置」66px・2カラム統一／012: 「数字4桁」96px強調＋dialpad icon／018: 72px／019: 72px。
- QA（tv_readability_qa.md）: overflow 8/8 PASS（right/bottom 0）・text_asset_overlap PASS（左端ストリップ侵入0・INK tol25）・tv_text_size 記録・underused_whitespace WARN 0。
- 比較画像: `work/phase_b_review/tv_text_readability_comparison.png`（OLD=v4退避版 / NEW）／contact sheet v5: `work/phase_b_review/scene_contact_sheet_v5.png`（22/22）。
- publish checklist: 終了画面の今後の標準として「関連動画1本＋チャンネル登録1個」（Episode 007→002・002→007は公開後・人間操作）を publish.json に記録。
- 次は人間による contact sheet v5 確認（50%/25%縮小で main message が判別できるか等）。本編VOICEVOX・字幕実尺・draft・thumbnail・YouTubeは未実施。

## 大文字・高可読性版（2026-09-04 人間レビュー反映 第4弾・最終Visual）

- 恒久ルール: 「**読めない情報は、ないのと同じ**」。主要視聴者を50〜60代中心・視力が弱い視聴者も想定と明記し、情報文字は原則44px未満を画面に出さない（main fact 60px以上・headline 80px以上・secondary 52px以上・source表記は44px以上）。AGENTS.mdとtemplates/scenes/README.mdへ反映。
- 対象8scene（004/005/008/009/012/015/018/019）をカードv4へ再設計: 下部の小さいURL全文・確認日・※注記・細かいsourceを**全削除**（provenanceはsources.md/media_manifest/publish description/local/web_checkへ保持）。出典は「出典：マイナアプリ公式」等の短形44pxのみ表示。L1 66〜96px・L2 52px以上・pill 44px。
- production memoの混入を解消: SCENE-001/013/020のmain_message（「導入（問題提示・結論）」「注意（最重要）」「案内（窓口・002案内）」）を視聴者向け文へ置換し、旧値はepisode.jsonのproduction_noteフィールドへ退避。SCENE-020の「（2026年9月時点・要再確認）」を削除。
- template基準: eyebrow/section-pill 28→44px・footerブランド 25→32px・行頭番号/チェック丸 40→44pxに引き上げ（templates/scenes/styles.css）。
- QA（large_text_qa.md）: tiny_text=0・unreadable_footer=0・overflow=0（機械検査right/bottom）・text_asset_overlap PASS・official facts無変更・scene mapping PASS。
- render: 16 scene 再render（template 7＋official 8＋compare 1）・6 scene reuse（imagegen_native系）。
- contact sheet v6: `work/phase_b_review/scene_contact_sheet_v6.png` ／比較: `work/phase_b_review/large_text_comparison.png`（OLD=小文字あり / NEW）／25%縮小確認: `work/phase_b_review/large_text_25pct_check.png`。
- 終了画面方針（関連動画1本＋登録1個・002相互導線）は維持（publish checklist・既存YouTube動画は変更しない）。
- 次は人間による contact sheet v6 と 25%縮小の確認。本編VOICEVOX・字幕実尺・draft・thumbnail・YouTubeは未実施。

## Phase B後半（2026-09-04・Visual Gate 人間承認済み）

- **Visual Gate**: fact PASS／visual/semantic icons/imagegen_native/TV readability=APPROVED_BY_HUMAN／tiny_text 0／overflow 0／privacy PASS／scene mapping PASS。`human_visual_approved=true` をSTATE/metricsに記録。
- **VOICEVOX本編**: 61/61 生成（剣崎雌雄・ノーマル・speed1.00/intonation1.00/pitch0.00）。narration 385.471s。音声は hash/selective 管理（再ビルド時 61 再利用）。
- **字幕実尺**: audio_timing 実測ベース。長文 cue は2行化のため cue単位フォント（60/52/44px・{\fs}）を適用し、ナレーション一致0・幅超過0・下180px帯内。
- **CTA**: channel_common_cta（canonical・音声再利用 11.563s・postroll 12.56s・hash一致）。
- **draft**: `output/draft_v1.mp4`（398.0s・1920×1080・30fps・H.264・AAC 48kHz）。QA: **WARN 2（仮名分断の予測。SCENE-006 headline・020 main_message・実フレームでは分断なし確認）/ FAIL 0**（decode 0・black 0・silence 0・subtitle 61・scene 22・CTA あり）。
- **representative frames**: `work/qa_frames_draft_v1/`（SCENE-001/003/005/007/008/009/011/012/014/015/017/018/019/020/022＋CTA）。Visual regression 確認済み（semantic icon版・imagegen_native版・2カラム版・大文字版に戻っていない）。
- **End Screen**: 焼き込みなし。mock= `work/phase_b_review/end_screen_mock.png`（CTA背景＋関連動画枠＋登録枠の重なり確認用）。方針: 関連動画1本（Episode 002候補）＋登録1個・YouTube Studio で実設定。
- **pronunciation REVIEW 8件**: `work/phase_b_review/pronunciation_review_targets.md` に timestamp 確定（1:49〜5:50）・human_review=pending。音声は自然な読みで生成（0120-95-0178 は1桁読み）。
- 冒頭25秒: ナレーション冒頭（ログインできない→5つ一覧）を維持。本題開始が遅れていないことを draft 視聴で確認。
- **次: 人間の全編視聴（draft_v1.mp4）**。final・thumbnail・YouTube upload・End Screen実設定・Episode 002設定変更は未実施。

## draft_v2（2026-09-04・人間全編レビュー反映）

- **発音修正**（5 segment 再生成・他56はhash reuse）: NFC=エヌエフシー（accent 3・尾高。1文字目集中読みの解消。3文字英字略語の恒久ルールをAGENTS.md・docs/pronunciation_workflow.mdに反映）／PIN=ピーアイエヌ（accent 6・Episode 006 approved の scope を007へ拡張して再利用）／上→うえ（seg 26・segment override）／方→かた（seg 32/40・分context override）。preview WAV+queryは `work/phase_b_review/pronunciation_fix_v2/`。
- **字幕**（恒久ルール化）: 「小さくして収める」→「時間方向に分割して大きく読む」。44/52px cue を廃止し、seg 12/16/20/47 を 1 narration→2 display cue に意味分割（句点・読点優先）。全 display cue 65・最小フォント 60px・56px未満0・幅超過0・ナレーション一致0。AGENTS.md・subtitle_preflight（font<56 FAIL・幅をfont換算）へ反映。
- **CTA（End Screen対応）**: 現デザイン（淡い青・ロゴ・チャンネル名・説明・緑CTA）を維持しつつ LEFT55%（ロゴ・名前・説明・CTA）＋RIGHT45%（関連動画枠・登録枠の空間）へ。右上に「次はこちら」ラベル（背景側・焼き込みなし）。postroll 12.56→15.0s（audio 11.56 + trailing 3.44）。mock A/B: `end_screen_mock_v2_A.png` / `_B.png`。
- **draft_v2**: `output/draft_v2.mp4`（400.4s・1920x1080・30fps・H.264・AAC48k）。QA WARN2（仮名単語途中分断の予測・実フレームで分断なし）/ FAIL 0。代表フレーム `work/qa_frames_draft_v2/`（字幕60px・新CTAを確認）。
- **次: 人間の再確認**（発音①〜⑤・字幕1:25/4:55・CTA/End Screen）。final・thumbnail・YouTube・End Screen実設定・002変更は未実施。

## draft_v3（2026-09-04・CTA/End Screen局所修正）

- **修正方針**: 終了画面のみ局所修正（人間レビュー反映）。本編22scene・発音・字幕・ナレーションは変更しない。
- **疑似subscribe削除**: 動画側の疑似登録アイコン（丸＋✓）を廃止。登録ボタンはYouTube StudioのEnd Screen要素で実配置する（恒久ルール化）。
- **水玉装飾**: 左ブランド枠中央（「デジタル」文字背後の低opacity）のみ。右reserved領域（x>=1090）は装飾・本文・疑似アイコン0（「次はこちら」ラベルのみ）。
- **CTA本文**: 「チャンネル登録・／高評価もよろしくお願いします」を自然な2行（「・」で改行）・60pxで表示（表示のみ句点省略・ナレーション不変）。footer band [138,714,1032,890] をカード下部に新設し、文字の途中切れ・overlap・はみ出しを解消。config/channel_cta.json に反映（panel/description_box/cta_box/cta_text_box）。
- **draft_v3**: output/draft_v3.mp4（400.4s・1920x1080・30fps・H.264・AAC48k・SHA256 40171870...）。CTA音声reuse 11.563s・postroll 15.0s（trailing 3.44）維持。QA: WARN2（既知の仮名分断予測・実フレームで問題なし）/ FAIL 0。
- **回帰確認**: 代表scene 15枚がdraft_v2とSHA同一（CTAのみ差替え）。代表フレーム work/qa_frames_draft_v3/。
- **成果物**: work/phase_b_review/cta_v2_v3_comparison.png（v2/v3比較）・work/phase_b_review/end_screen_mock_v3.png（関連動画枠＝右中・登録枠＝右下。次はこちらと非重なり）。
- **恒久ルール反映**: AGENTS.md「CTA・End Screenルール」・docs/phase2_hybrid_production.md（疑似subscribe禁止・reserved領域・縮小禁止・自然改行・装飾最小限）。
- **次: 人間のCTA/End Screen最終確認**（draft_v3 CTA・mock）。final・thumbnail・YouTube・End Screen実設定・002変更は未実施。

## draft_v4（2026-09-04・CTA左上アイコン削除）

- **修正内容**: 終了画面（約6:33以降）左上のチャンネルアイコン（ロゴ画像）を削除。理由: チャンネル登録用アイコンはYouTube Studio側で実配置するため、動画背景側に描画しない（恒久ルール化）。
- **削除実装**: config/channel_cta.json の logo を null 化し、create_channel_cta.py は logo が無い場合に描画をスキップ（logo_area は維持・別アイコンは追加しない。空いた左上は水玉装飾のみの余白として活かす）。
- **維持**: チャンネル名・説明文・CTA本文（2行60px）・淡いブルー背景・水玉左位置・次はこちら・右reserved・CTA音声11.563s・postroll 15.0s。疑似subscribe削除・text overlap 0・CTA全文表示も維持。
- **QA**: channel icon in CTA 0（logo_area 彩度0）・fake subscribe 0・CTA text 2行60px（L2≈840px）・reserved（x>=1090）foreign 0・bubble left rows 354 / right 0。本編scene 15枚はdraft_v3とSHA同一（回帰PASS）。QA status WARN（既知の仮名分断予測2のみ）/ FAIL 0。
- **draft_v4**: output/draft_v4.mp4（400.4s・1920x1080・30fps・H.264・AAC48k・SHA256 FCE921CD...）。black 0・decode error 0・silenceはCTA余韻3.50sのみ（設計どおり）。
- **成果物**: work/qa_frames_draft_v4/cta.png（t=386.9s）・work/phase_b_review/cta_v3_v4_comparison.png（LEFT=v3 / RIGHT=v4）。
- **恒久ルール反映**: AGENTS.md・docs/phase2_hybrid_production.md に「End Screen背景にはチャンネルアイコン・疑似登録アイコンを描画しない」を追加。
- **次: 人間のCTA左上アイコン削除の最終確認**。final・thumbnail・YouTube・End Screen実設定・002変更は未実施。

## draft_v5 → final・公開準備（2026-09-04）

- **CTA最終修正**: 約6:33以降のCTAからチャンネル名「大人のデジタル安心室」テキストも削除（ロゴ・疑似subscribe削除に続く第3弾。channel name ink=0・削除位置に別要素なし）。残す: 淡いブルー背景・左側水玉・説明文（カード中央へ軽く移動）・CTA本文2行60px・「次はこちら」・右reserved・CTA音声11.563s・postroll 15s。config/channel_cta.json の channel_name を空にし、description_box を [150,555,1020,695] へ軽く調整。
- **draft_v5**: output/draft_v5.mp4（400.4s・19,909,566 bytes・1920x1080・H.264・AAC48k・SHA256 80AD0194...）。QA: status WARN（既知の仮名分断予測2のみ）/ FAIL 0。decode error 0・black 0・silence はCTA余韻のみ。本編scene 15枚はdraft_v4とSHA同一（本編・音声・字幕の完全reuse）。
- **final**: output/final.mp4 = draft_v5 と byte-identical copy（SHA一致: 80AD0194...）。再encodeなし。
- **確定サムネイル**（人間確定・添付画像＝output/thumbnail.png 1672x941 16:9）: assets/thumbnail/thumbnail.png へコピーのみ（SHA一致 16A4DD89...・decode正常・文字切れなし・破損なし）。25%確認: work/thumbnail_review/thumbnail_25.png。新しい候補は生成しない。
- **metadata**: title=【マイナアプリ】ログインできない？まず確認したい5つ／description は既存（fact check/sources.md由来・スマホ対応/カード読み取り/PIN/期限/障害メンテ/再設定/公式サポート・official URL 8件・ナレーション：VOICEVOX:剣崎雌雄）／made_for_kids=false／containsSyntheticMedia=true・ai_disclosure_review=REVIEW_REQUIRED（公開時に人間確認で停止）。
- **End Screen 予定**: 007=RELATED Episode 002（「【マイナアプリ】マイナポータルアプリはどう変わった？今やること3つ」・video IDはrepoに無いため公開時人間確認）＋SUBSCRIBE登録要素。007公開後に002のEnd Screenへ007追加（人間操作・API変更しない）。
- **公開予定**: 2026-09-04 本日。YouTube upload・public化・End Screen実設定・002変更は未実施（人間操作による）。
- **次: 人間の YouTube publish（private/scheduled）・AI開示レビュー・End Screen実設定・002更新**。

## YouTube publication
- youtube_upload: uploaded_private
- youtube_video_id: CAb0b7n0ByY
- youtube_url: https://youtu.be/CAb0b7n0ByY
- youtube_privacy: private
- youtube_scheduled_at: null
- youtube_scheduled_at_api: null
- thumbnail_uploaded: true
- uploaded_at: 2026-09-04T12:47:52Z
- youtube_channel_id: UCgVRceTJYO5KOrPX4w2jXZw
- youtube_made_for_kids: false
- youtube_duration: PT6M41S（400.4s）
- youtube_upload_status: processed
- youtube_verification: PASS（title / privacy / madeForKids / thumbnail / channelId / description / duration 確認済み）
- youtube_ai_disclosure: true
- youtube_ai_disclosure_updated_at: 2026-09-04T12:49:47Z
- youtube_ai_disclosure_verified: true
- youtube_ai_disclosure_verification: videos.update response; videos.list omitted containsSyntheticMedia
- youtube_note: videos.list(part=status) は containsSyntheticMedia を返さない仕様のため、既存フォールバック（videos.update 応答）で verified。二重uploadなし・public化なし・End Screen実設定なし。
