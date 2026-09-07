# Phase A preflight — Episode 006

確認日: 2026-09-02　基準: `episodes/006_line_talk_backup/` のcanonical file一式

> Phase A人間レビュー後およびPhase B前半の実績を追記した。以下の旧行に残る69 segment／25 scene／未生成の記述は、Phase A時点の履歴であり、現行canonicalは68 segment／24 scene。最新の停止点は末尾の「Phase B前半 update」を参照。

| 項目 | 判定 | 備考 |
|---|---|---|
| schema | **PASS** | `episode_io.validate_episode` issues 0件（現行: 68 segments・68 subtitles・24 scenes・13 sources） |
| sources | **PASS** | 一次情報13件（LINEヘルプセンター・LINEみんなの使い方ガイド）を2026-09-02に取得・保存（`local/web_check_006/`）。まとめサイト・二次記事不使用 |
| official facts | **PASS** | Fact Checkで指定9項目すべて一次情報と一致（標準バックアップ・保存先・自動バックアップ・PIN・14日間の現行性・OS条件差・写真動画・プレミアム・引き継ぎとの違い） |
| script | **PASS** | 現行68ナレーションセグメント・想定約6分20秒・1文1segment・冒頭20秒に結論・SHOTタグ7個 |
| fact check | **PASS** | FAIL 0件／Phase A REVIEW 4件をcanonicalへ反映（自動バックアップ限定・標準バックアップ限定・iCloud Drive表記・公式表記） |
| subtitles | **PASS** | 現行字幕68件とsegments 1:1。subtitle_preflight fail 0 / warn 0（72px・安全幅1800px・最大2行・保護語またぎ・単独助詞・バランス）。実尺タイミングは本編音声後に実施 |
| scene mapping | **PASS** | 現行24 sceneがsegment 1〜68を重複・欠落なくカバー（scene 18はscene 17へ統合） |
| render modes | **PASS** | 現行 template 12 / official 7（公式引用カード）/ gpt_image 5＋CTA(postroll)。LINEの実UIのAI再現なし |
| text provenance | **PASS** | 旧エピソード固有語（ニセ警察・国際電話・マイナ・Googleフォト・App Store等）のscene/ナレーション混入なし |
| item count | **PASS** | オープニング3項目（seg 4〜7）とまとめ3項目（scene 24・seg 63〜66）が同一文面・同一順。各sceneのitems件数とナレーション整合 |
| linebreak QA | **PASS** | subtitle_preflight PASS。PROTECTED_TERMSへEpisode 006用語を追加（scripts/subtitle_preflight.py） |
| pronunciation | **REVIEW可** | `work/pronunciation_candidates.md` に候補一覧。辞書は未変更（人間試聴後に承認分のみ登録） |
| personal-data plan | **PASS** | shotlist・visual_planにテストアカウント限定・実トーク/友だち一覧/通知/QR/LINE ID/電話番号/プロフィール写真の非表示・PINの値非表示・iCloudモザイクを明記 |
| gpt images | **REVIEW** | 5枚生成済み。原本は`assets/generated_ai/`、1920×1080正規化copyとcontact sheetは`work/phase_b_review/`。人間レビュー待ち |
| captures | **OFFICIAL FALLBACK** | AndroidはLINE未インストール、iPhone実機未取得。7枚の公式保存HTML由来引用カードを`assets/official/`に作成。実在UIではない |

## 結論

Phase Aの必須項目は修正反映済み。Phase B前半では、GPT画像5枚・公式引用カード7枚・全24scene仮レンダー・pronunciation audio_query preflightまで完了し、contact sheet・pronunciationの人間レビューで停止する。

## Phase B前半 update（2026-09-02）

- GPT画像: 5/5生成、重複SHAなし、原本保持。正規化copyは5/5・1920×1080・下180px字幕帯確保。
- 公式素材: 7/7 ready。Android実画面4枚とiPhone実画面1枚は取得せず、保存HTML由来の引用カードにfallback。出典・タイトル・確認日・引用元HTML・SHAは`media_manifest.csv`と`work/subagents/006_line_talk_backup/iphone_official_report.md`に記録。
- render: 24/24 PASS。`work/phase_b_review/scene_contact_sheet.png`と`gpt_image_contact_sheet.png`を作成。
- pronunciation: VOICEVOX 剣崎雌雄／ノーマル（style_id=21）で68/68 audio_query。REVIEW 5、辞書変更なし。
- 未実施: VOICEVOX本編WAV、最終字幕タイミング、video build、thumbnail、YouTube操作。
