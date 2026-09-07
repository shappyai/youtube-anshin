# Phase B前半 preflight — Episode 007（2026-09-03）

基準: A/B採用（SCENE-003 = imagegen_native一体生成）後の公式仕様・描画パイプライン。**画像生成サービスが一時障害（HTTP 404）のため、imagegen_native 6 scene中5 sceneが生成待ち**。それ以外の工程は完了。

| 項目 | 判定 | 備考 |
|---|---|---|
| fact check | PASS | FAIL 0 / REVIEW 0（公式本文直接確認で解消済み。61 segment） |
| official numeric facts | PASS | 3回連続ロック・10回目/5回目の誕生日・3か月前・0120-95-0178・受付時間・読み取り位置は lical/web_check_007/ の公式本文で確認 |
| imagegen_native text scenes | **REVIEW（1/4生成）** | SCENE-003 生成・採用／SCENE-011/014/017 生成待ち（サービス障害） |
| exact text | **PASS 1/1（2/6待ち）** | SCENE-003の指定文言（スマホが、/対応しているか・まずは端末とアプリの準備から。）を目視相当QAで完全一致。pending 5場面は復旧後に実施 |
| concept images | **REVIEW（0/2生成）** | SCENE-007/022 生成待ち（サービス障害） |
| duplicate SHA | PASS | assets 11ファイルで重複グループ0 |
| official assets | PASS（REVIEW：実機未取得） | 公式引用カード6枚＋公式読み取りイメージ入り2枚（計8・1920×1080）を本番パイプラインで反映。実機/Emulatorは未取得（安全な実機取得に時間をかけない方針） |
| privacy | PASS | 実物カード・マイナンバー・氏名等は一切不使用。公式イラスト/公式引用のみ。カードの個人情報を含む画像なし |
| pronunciation | REVIEW（8件） | VOICEVOX 剣崎雌雄/ノーマル（style_id=21）で61/61 audio_query実行。REVIEW 8件は全て文脈依存語（上・方・生・今日）の自動フラグで、エンジン読みは全て正しい（ウエ/ホオ/ハッコービ/ショーメイショ/キョオ）。辞書変更なし・segment override候補 |
| scene mapping | PASS（17/22描画） | segment 1〜61をカバーする22 sceneのうち、画像未生成5 scene（007/011/014/017/022）以外を描画。描画済み17 sceneでメッセージ・字幕帯・レイアウト矛盾なし |
| linebreak | PASS（subtitle） | episode.jsonの字幕61件とナレーションの一致を再検証済み（mismatch 0）。実尺タイミングは本編音声後に実施 |
| TV readability | PASS/REVIEW | 描画17 scene: 下180px安全領域クリア（active比≦0.08を全sceneで確認）。見出し：AI採用scene=A/Candidate（大見出し・高コントラスト）、template=104px、official引用カード=64px。縮小時・実TV距離の最終判定はcontact sheetの人間確認へ |
| template leakage | PASS | 旧Episode固有語なし。Analytics数値は本編に出さない方針を維持 |
| CTA | PASS | channel_common_cta固定（postroll）。新規CTAなし |

## 描画状況

- rendered 17/22（scene_001〜021のうち画像依存5 sceneを除く全点）。missing: scene_007/011/014/017/022（画像生成サービス復旧後に生成→再render）
- renderer: hybrid_scene_renderer（imagegen_native scene = full-bleed・文字オーバーレイなし、のルーティングを恒久化。template + imagegen_native をrender_ai_sceneへ）／Edge（HTML）エンジン
- contact sheet（部分）: `work/phase_b_review/scene_contact_sheet.png`／imagegen_native text contact sheet: `work/phase_b_review/imagegen_native_text_contact_sheet.png`（SCENE-003採用表示＋5 sceneはPENDINGラベル）

## 次アクション（人間レビュー待ち）

1. scene contact sheet＋imagegen_native text contact sheet：SCENE-003採用分・official引用カード8枚・templateの見た目を確認
2. pronunciation REVIEW 8件（文脈依存語フラグ）の試聴確認（REVIEW一覧は `work/phase_b_review/pronunciation_preflight.md`）
3. 画像生成サービス復旧後に SCENE-007/011/014/017/022 を生成（1 scene=1 generation）→ exact text QA → 再render → contact sheet更新
4. その後: 本編VOICEVOX生成・字幕実尺・draft へ

## Visual polish 最終QA（2026-09-04追記）

| 項目 | 判定 | 備考 |
|---|---|---|
| official facts | PASS | 公式本文直接確認済みの数値を維持（改変なし） |
| semantic icons | PASS | 9 scene（承認5＋追加4）。ライセンス記録済み（LICENSES.md）・意味一致 |
| imagegen text | **PASS 5/5** | SCENE-007/011/014/017/022 生成・exact text QA（目視・全文字一致）。再生成0・fallback0 |
| exact text | PASS 6/6 | 前回採用分1＋今回5（SCENE-003/007/011/014/017/022） |
| text/image overlap | **PASS** | SCENE-008: 0.35%・SCENE-009: 0.56%（閾値1%未満。2カラム固定で重なりゼロ） |
| scene text density | PASS（WARN 0） | 公式引用カードは引用2〜3行＋source 小（構造値）。詰め込みなし |
| TV readability | PASS/REVIEW | 全22scene・見出し中央・アイコン180px・引用54px以上。縮小時は人間確認（v4 sheet） |
| privacy | PASS | 実物カード・個人情報なし。公式イラスト/引用のみ |
| template leakage | PASS | 旧Episode固有語なし |
| duplicate composition | PASS（0） | imagegen 5枚は構図コピーなし（概念別）・重複SHA 0 |
| subtitle safe area | **PASS（22/22）** | 下180px帯に文字・オブジェクト侵入なし（機械計測） |
| scene mapping | PASS | 22 scene × 61 segment 対応を維持（text無変更） |
| render | **22/22** | 11枚polish再render＋11枚reuseで全scene完成 |

成果物: `scene_contact_sheet_v4.png`・`visual_polish_comparison.png`（OLD v3/NEW v4）・`visual_polish_qa.md`・`visual_polish_review.md`

**Phase B前半（Visual）は完了。残るは本編VOICEVOX生成・字幕実尺・draft 以降（人間のcontact sheet確認後に進める）**
