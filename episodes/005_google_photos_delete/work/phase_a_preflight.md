# Phase A preflight — Episode 005

確認日: 2026-09-01　基準: `episodes/005_google_photos_delete/` のcanonical file一式

| 項目 | 判定 | 備考 |
|---|---|---|
| schema | **PASS** | `episode_io.validate_episode` issues 0件（JSON構文・必須項目・subtitles 1:1・scene/subtitle整合） |
| sources | **PASS** | 一次情報20件（Googleフォト/Googleドライブ/Apple/Googleブログ）を2026-09-01に取得・保存（`local/web_check_005/`）。まとめサイト・二次記事不使用 |
| official facts | **PASS** | Fact Checkで最重要7項目すべて一次情報と一致（ゴミ箱60日/30日・端末同時削除・デバイスから削除両OS・空き容量の前提条件・30日保持・最近削除した項目30日・容量の区別） |
| script | **PASS** | 65ナレーションセグメント・想定6〜7分・1文1segment・冒頭20秒に結論・SHOTタグ8個 |
| fact check | **PASS** | FAIL 0件／REVIEW 3件（低優先度）→ 親Codexが全件反映済み（seg14/21/31/57・support_text整合） |
| subtitles | **PASS** | 字幕65件とsegments 1:1（意味単位・最大2行）。実尺タイミング・72px帯・改行QAはPhase B（実音声後）で実施 |
| scene mapping | **PASS** | 25 sceneがsegment 1〜65を重複・欠落なくカバー（Visual Agent planを親Codex統合・機械検証） |
| render modes | **PASS** | template 12 / official 8 / gpt_image 5＋CTA(postroll)。公式UIのAI再現なし |
| text provenance | **PASS** | 旧エピソード固有語（ニセ警察・国際電話・マイナ・LINE・App Store・セキュリティ等）のscene/ナレーション混入なし（script.mdの「App Store」は発音候補メモ内の注記のみ） |
| item count | **PASS** | シーン毎のitems件数とナレーションの整合（比較表3回・まとめ4項目） |
| pronunciation | **REVIEW可** | `work/pronunciation_candidates.md` に候補一覧。辞書は未変更（人間試聴後に承認分のみ登録） |
| gpt images | **NOT GENERATED** | 5枚すべて未生成（`assets/generated_ai/` 空）。manifest・scene_prompts準備済み |
| official/emulator/iphone素材 | **NOT CAPTURED** | `assets/emulator/`・`assets/iphone/` 空（Phase Bで取得・撮影）。production_preflightは素材揃うまでMISSINGで停止する想定 |

## 結論

Phase Aの必須項目はすべてPASS（またはREVIEW可・未生成として明示）。テーマ・台本・scene planの人間レビューを待って、次Phase（GPT画像生成・Emulator/iPhone撮影・VOICEVOX・video build）へ進める。
