# Episode 012 QC status

確認日: 2026-09-06  
段階: Phase B final / YouTube scheduled  
状態: `UPLOADED_SCHEDULED`

| QA | 結果 | 記録 |
|---|---|---|
| JSON parse / episode manifest | PASS | 79 narration / 117 subtitle / 30 scene |
| Fact Check | PASS（FAIL 0） | `fact_check.md`。REVIEW 3件は公開前再確認へ送付 |
| Privacy design | PASS（FAIL 0） | 架空メッセージに実在URL・電話番号・氏名・QR・アカウント番号なし |
| ImageGen deterministic QA | PASS | 6/6配置、1920×1080、auto_fail 0 |
| ImageGen visual text QA | PASS | 指定見出し一致、余計な文字・公式UI・政府マークなしを目視確認 |
| Scene renderer | PASS | 30/30 rendered |
| Scene quality report Phase B | PASS | OK 31 / WARN 0 / FAIL 0。`visual_centroid_preflight` 7/7 PASS |
| Permanent visual policy | PASS | `oversized_checkmark_count=0` / `decorative_checkmark_as_main_visual=0` / `meaningless_filler_icon=0` |
| Official two-column balance | PASS | Phase B gateの対象7sceneすべてPASS。右visual weight最小31.71% / 重心x=1013.42〜1101.12 |
| Regression | PASS | 対象7scene以外の24sceneはv1 baselineとSHA-256一致。ImageGen章扉6sceneも未変更 |
| Long-form depth | PASS（机上） | `work/long_form_depth_gate.md`。人間確認待ち |
| Subtitle timing | PASS | 音声実尺から117 cue、72px、TTS reading leakage 0。意味境界4指標すべて0 |
| Audio / draft | PASS | VOICEVOX剣崎雌雄79 segment、`output/draft_v4.mp4` 585.40秒。030.wavは人間修正版override、再生成0件 |
| Human full watch | PASS | draft_v3全編確認済み、senior_readability=PASS。v4は030.wavの音声overrideのみ反映 |
| Final | PASS | `output/final.mp4`をdraft_v4からcopy-onlyで確定。SHA一致 |
| Thumbnail / upload | PASS | ユーザー提供サムネイルを内容変更なしで1280×720へ正規化。YouTube upload / schedule / metadata / thumbnail設定をAPI検証済み。End Screen設定はYouTube Studioの人間作業 |

## Final v4 gate（2026-09-06）

- `output/draft_v4.mp4` と `output/final.mp4` はともに585.400秒、47,642,598 bytes、H.264 1920×1080 30fps / AAC 48kHz mono。
- draft v4 / final SHA-256: `32933ED599E072DDF27FA7AF99756F4F78B15A3498DA0EA2071F44EC04660DD8`。copy-only、byte-identical、再エンコードなし。
- `segment030`「これ、本物？」は `audio/human_approved/030.wav` を正本として採用。SHA-256 `7B534892A4AC893CC7F1D0D483B67A8A94E690353DB652EA16B0077C3F4C7106`、実測6.346667秒、timeline 213.189–219.536秒。
- v4 audio logは `regenerated=[] reused=78 human_overrides=[30]`。human audio overrideは自動生成・辞書より優先し、cleanup時も保持する。
- subtitle 117 cue、72px基準 / 56px以上。semantic linebreak 4指標、overflow、3-line、TTS reading leakageはすべて0。
- e-Taxはイ・イ・タ・ッ・ク・ス、アクセントピーク「タ」、語中pause 0。SCENE-031とsegment080はタイムライン0件。
- 終了CTAは1回、15秒（音声11.456秒＋末尾3.544秒）。Episode011実使用CTAのcontent / visual / audio hashを再利用し、右40〜45%をEnd Screen予約領域として空けた。疑似subscribe UIなし。
- Fact FAIL 0 / Fact REVIEW 3 / Privacy FAIL 0。一次情報の最終再確認は `fact_check.md` と `sources.md` に記録。

## YouTube publication verification（2026-09-06）

- video ID: `CzTNLyAn1lY`（https://youtu.be/CzTNLyAn1lY）。承認済み`output/final.mp4`を再アップロードなしで登録。
- Channel guard: PASS。Channel ID `UCgVRceTJYO5KOrPX4w2jXZw`、チャンネル名「大人のデジタル安心室」を`channels.list(mine=true)`で確認。
- `privacyStatus=private`、`publishAt=2026-09-12T10:00:00Z`（2026-09-12 19:00 JST）、`madeForKids=false`、category `22`、language `ja`をAPIで確認。
- title / description / chapters / source URLs / thumbnail設定: PASS。`contains_synthetic_media=true`はupload時の`videos.update`応答で確認し、`videos.list`で省略されたowner-only項目であることを記録。
- End Screenは未設定。YouTube StudioでEpisode004を関連動画、チャンネル登録要素を人間が設定する。
- サムネイルは `work/thumbnail_qa.md` の人間提供画像を正式採用。原本`assets/thumbnail/thumbnail_source.png`、公開用`assets/thumbnail/thumbnail.png`（1280×720、2MiB以下、25% readability PASS）を保持。publish dry-run後に予約公開する。

## Phase B draft gate

- Visual Gate v2: `APPROVED_FOR_PHASE_B`（人間承認済み）。
- 対象SCENE-007 / 008 / 012 / 013 / 018 / 022 / 026: placeholder 0、neutral browser/phone 0、公式UI AI再現0、privacy PASS、公式文字TV可読性PASS。
- `work/visual_review/phase_b_visual_gate_final.md`: Overall PASS。
- `work/visual_review/scene_quality_report_phase_b_final.md`: OK 31 / WARN 0 / FAIL 0。
- `output/draft_v3.mp4`を人間が全編確認するまで、thumbnail、final、YouTube upload、schedule、End Screen設定へ進まない。

## Phase A stop（履歴）

人間のVisual Gate v2承認前は、VOICEVOX、字幕、draft、thumbnail、final、YouTube upload、schedule、End Screen設定へ進まない運用として停止していた。これはdraft_v3時点の履歴であり、現在は下記Final v4 gateへ更新済み。

## Phase B draft_v2（2026-09-06）

- 字幕は旧100 cueを意味単位で全件再構成し、119 cueへ更新。target 72px / minimum 56px、overflow 0、3-line 0、TTS reading leakage 0、`unnatural_japanese_line_break=0`、`word_split=0`、`conjugation_split=0`、`particle_or_auxiliary_orphan=0`。
- 恒久ルールは `scripts/japanese_subtitle_semantics.py`、`scripts/subtitle_phase_b_split.py`、`scripts/subtitle_preflight.py`、`templates/scenes/README.md` に追加。長い文は縮小せず、意味境界で時間方向へ分割する。
- SCENE-006 / 011 / 017 / 021 / 025は説明用semantic sceneとして再現ラベルを削除。全31sceneをscanし、`incorrect_reproduction_label=0`。
- SCENE-007は国民生活センター公式PDFの中途半端なcropを採用せず、同PDFの正確な短い引用＋出典ラベルへ変更。公式取得失敗時は抽出断片を表示しないfail-closed運用を恒久化。
- 発音辞書へ普段、何も、届け物、本物、カード会社、e-Taxを標準承認登録。実クエリ監査は `work/pronunciation_audio_audit_v2.md` / `.json` に保存し、6語すべてPASS。`カード会社` 4出現はaccent=3（ド）、e-Taxはinternal pause 0。
- 終了CTAはEpisode011 `output/final.mp4`の実使用postrollをsource of truthとして、canonical text・PNG・WAV・15秒・右40〜45%予約を再利用。CTA音声hash一致、再生成なし。中盤CTAもEpisode011 segment013とのhash一致を確認。
- Contact sheet：`output/review/scene_contact_sheet_v2.png`。Scene quality report：31 OK / WARN 0 / FAIL 0。
- `output/draft_v2.mp4`：実測597.13秒、SHA-256 `94A04D4D905E3736E3792DAC69C1CE2A1935F9D71C11A052951B74161ED48B8B`。人間の全編確認待ち。
- 再確認の時刻表：`work/human_review_points_v2.md`。thumbnail、final、upload、schedule、End Screen設定は未実施。

## Phase B draft_v3（2026-09-06・人間全編確認待ち）

- `『これ、本物？』` は対象文を直接 `audio_query` し、ホ／ン／モ／ノの4モーラ、疑問イントネーション、余分なオ行なし、語尾の不自然な引き伸ばしなしを確認した。`本物`の7出現すべてに `contextual_pronunciation_audio_gate` を適用し、辞書読みだけでPASSにしない回帰検査を残した。
- `e-Tax` は標準辞書を `イータックス`（イ・イ・タ・ッ・ク・ス、アクセント3＝タ、語中ポーズ0）へ更新し、`e-Taxのメールも、` の実文クエリを確認した。
- SCENE-031とsegment080を本編タイムラインから除外。SCENE-030（segments 076〜079）の直後にEpisode011実使用CTAをpostrollとして直接連結し、終了CTAは1回だけにした。
- 字幕は117 cue、72px基準／56px以上、`tts_reading_leakage=0`、`unnatural_japanese_line_break=0`、`word_split=0`、`conjugation_split=0`、`particle_or_auxiliary_orphan=0`。既存の日本語意味単位改行ルールを維持した。
- `output/review/scene_contact_sheet_v3.png`、`work/visual_review/scene_quality_report_draft_v3.md`、`work/subtitle_preflight_v3.md`、`work/pronunciation_audio_audit_v3.md`を保存。scene qualityは30 OK / WARN 0 / FAIL 0。
- `output/draft_v3.mp4`：実測585.55秒、SHA-256 `662804C23CD1FF6915CA65655671757A80118DD8E7EEC05F56627309EF9B1205`、Phase 2 QA PASS。人間の全編確認待ち。
- 再確認の時刻表：`work/human_review_points_v3.md`。thumbnail、final、upload、schedule、End Screen設定は未実施。
