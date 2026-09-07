# 大人のデジタル安心室 — Codex Instructions

## Goal
50〜70代を中心に、スマホ・詐欺・AIを難しい言葉なしで説明するYouTubeチャンネルを運営する。

## Brand promise
**怖がらせる前に、確認する。**

## Internal brand promise boundary（恒久ルール）
- `internal_brand_promise: "怖がらせる前に、確認する。"`
- `classification: INTERNAL_ONLY`
- `viewer_facing: FORBIDDEN`
- 完成動画のviewer-facing countは常に `0` とする。内部のブランド理念・企画書・制作メモ・QA記録に残ることは許可するが、scene表示文字、renderer text、ImageGen prompt/generated-text QA、字幕、ナレーション、CTA、thumbnail metadata、end card、overlay、descriptionの表示用metadataには入れない。
- `scripts/viewer_facing_text_qa.py` のQA rule `viewer_facing_internal_brand_promise` をEpisode/Shortsのproduction preflightとupload preflightで実行する。検出時はFAILとしてbuild/uploadを停止する。
- raster画像内の文字は既存のImageGen text QAとHuman Visual Gateで確認し、canonical text/metadataは上記スキャンで確認する。

## Priority
1. 正確性
2. 視聴者が実際に操作できる分かりやすさ
3. 独自性（実機・一次情報・自作図解）
4. 視聴維持・CTR

再生数のために1〜3を犠牲にしない。

## Research rules
- Apple / Google / LINE / デジタル庁 / 警察庁 / 通信会社など一次情報を最優先する。
- `sources.md` に **確認日 / URL / 何が確認できたか** を残す。
- 競合動画は「需要と見せ方」の研究にのみ使い、文章・構成をコピーしない。
- 一次情報で確認できないことは断定しない。「確認できませんでした」と書く。
- OS・アプリのバージョン差があり得る場合は明記する。

## Script rules
- 原則8〜15分。情報量が少ないのに引き延ばさない。
- 冒頭20秒以内に「結論」「この動画でやること」を伝える。
- 専門用語は直後に日常語で言い換える。
- 設定操作を見せる箇所には `[SHOT-01]` のようなタグを入れる。
- タイトル以上の恐怖を作らない。
- 「絶対」「100%」「全員」「漏れている」などは根拠がない限り使わない。
- `ambiguous_方_avoidance`（2026-09-05）: VOICEVOX narrationでは、自然な代替表現がある場合、漢字「方」を台本段階で避ける。特に「〜の方は」は「〜の場合は」「〜を使っている人は」「〜をお使いなら」、「考え方」は文脈に応じて「考え」「判断」「考えるポイント」、「やり方」は「手順」、「使い方」は「使う手順」「操作手順」、「確認したい方」は「確認したい人」、「こちらの方」は「こちら」へ自然に書き換える。固有名称・引用・公式UI文字、または書き換えると不自然／意味が変わる場合は例外とするが、VOICEVOX narrationに残す場合は `ambiguous_kanji_pronunciation` で SAFE / REWRITE / REVIEW を分類し、発音レビュー対象にする。

## Visual rules
- **共通Background System（恒久ルール・2026-09-05確定・Episode 008〜）**: template sceneは白一色禁止。`config/visual_theme.json` の `adult_digital_soft_background`（soft gradient・淡いcircle/dots/accent line・左上section pill〔44px以上〕・semantic icon plate・セクション別accent〔はじめに=blue／1=blue+淡amber／2=blue+淡green／3=blue+淡teal／困ったとき=淡amber／まとめ=soft blue-green〕・cautionは自動で淡amber・数字sceneは淡panel・listは淡rounded card・compareは薄いdepth）をレンダラー（HTML/CSS・Pillow）が自動適用する。適用順: template scene生成 → common background theme → semantic icon → text layout。Episodeごとのaccent変更はconfig/visual_theme.jsonのみ（hard-code禁止・再現性確保）。QA: `blank_white_slide`（コンテンツ領域ほぼ白画素率66%超WARN）をscene_quality_reportで検査。デザイン改善のために文字サイズ基準は緩めない。
- ユーザー提供の背景画像を採用するEpisodeでは、同じ設定ファイルの `adult_digital_soft_image_bg` を選び、`background_type=image`・`fit=cover`・縦横比維持・LANCZOS・`subtitle_safe_bottom_px=180`で全面配置する。元画像は保持し、正規化copyを再利用する。`overlay_decorations=false` とし、巨大circle・dots・leaf/wave・二重のicon backing・全体amber washは重ねない。section pill、意味アイコン、必要最小限のaccent line、字幕安全帯だけをrenderer/CSSが追加する。背景assetが無い場合は代替画像を作らず、`background_asset_pending=true`で停止する。
- 設定解説は実機画面または公式画面を優先する。
- 架空の設定画面をAIで生成し、本物のUIとして見せない。
- 個人情報が入る画面はテストアカウントを優先し、必要ならモザイクする。
- サムネ文字は2〜6語を基本とし、タイトル全文を繰り返さない。
- 単純記号（✓ / ! / ?）の自作バッジを使わず、sceneの意味に合う高品質semantic SVGアイコン（Material Symbols Rounded等・公式配布元・ライセンス記録）を淡いトーン円に150〜220pxで載せる。見出しより強くしない・画面の30%以上を占有しない・大型カード化しない。アイコンが画面面積の15%以上ならWARN（oversized_single_icon）。定義は `config/icon_catalog.json`・`templates/scenes/README.md`。
- **読めない情報は、ないのと同じ**（恒久ルール・2026-09-04確定）。主要視聴者を50〜60代中心・視力が弱い視聴者も想定と明記する。画面の情報文字は原則**44px以上**（main factは60px以上・headlineは80px以上・目安88〜120px・secondaryは52px以上）。44px未満の情報文字・URL長文・確認日・細かい注記・制作用ラベル（導入（問題提示・結論）等）は画面に出さず、sources.md / media_manifest / 説明欄 / local/web_check へ保持する。出典は「出典：マイナアプリ公式」等の短形のみ44px以上で表示。画面=結論・数字・操作箇所を大きく／ナレーション=条件・詳細・補足／概要欄=URL・source・詳細情報、の役割分担を原則とする。

## 撮影媒体の選択（shotlist作成前に決定する）
「スマホユーザー向けだから必ずスマホ撮影」とはしない。企画時に以下から最も分かりやすく制作しやすい媒体を選び、shotlistの Device 欄に記録する。
- Webサービスの設定 → PCブラウザを優先検討
- Android OS / Androidアプリ → Android Emulator
- iPhone固有設定 → iPhone
- LINE等スマホアプリ → スマホ
- 実機でなければ成立しない操作（生体認証・SMS受信・通知など）→ 実機

## 画面表示ルール（001で確定）
- **全体画面は「場所を理解させるため」だけに使い、原則2〜4秒。**
- 内容を読ませる箇所は必ず大きくクロップする（小さなスマホ画面全体を長時間表示しない）。
- 比較に意味がある場合のみ2カラム（2項目の左右比較）。
- 50〜70代でも読める文字サイズを最優先する。

## 字幕ルール（001で確定・2026-09-04補強）
- 全文字幕を表示する。
- タイミングは発話の実時間ベースで同期する（文字数按分は禁止。実尺から算出する）。
- 72px前後を基準とし、原則最大2行。**最小56px**（推奨60〜72px）。44px等への縮小は廃止。
- 下部の字幕専用帯に配置し、操作画面を字幕で覆わない。
- **長文cueは「小さくして収める」のではなく「時間方向に分割して大きく読む」**（恒久ルール）。1 narration segment に対し2つ以上の連続 subtitle display cue を許可（音声セグメントは分割しない・発話タイミングに沿って順に表示）。分割は句点・読点・意味の切れ目優先。語中・助詞のみ・protected term途中・「、」開始・不自然な途中切れは禁止。
- 3文字英字略語（NFC / PIN / API / URL 等・letter-by-letterで読む語）は**1文字目にアクセントピークを置かず、2文字目以降にイントネーションの山**を持たせる（恒久ルール・2026-09-04）。人間承認済み設定（NFC=エヌエフシー accent3・PIN=ピーアイエヌ accent6 等）は再利用。新規3文字略語は初回audio_queryでREVIEW（global辞書へ自動登録しない）。
- 音声用テキストと表示字幕は分離する。`narration`（または明示した`spoken_text`）はVOICEVOX入力、`subtitles.text_lines`（必要ならsegmentの`display_text`）は画面表示の正本とする。電話番号・URL・略語・数字・固有名詞の読み仮名を表示字幕へ流出させない。`tts_reading_leakage`で読み仮名流出と`display_text`不一致をFAIL検査する。

## CTA・End Screenルール（007 draft_v4で確定・恒久）
- **End Screen背景動画には、チャンネル登録用として誤認されるチャンネルアイコン（ロゴ画像）・疑似登録アイコンを描画しない**。実チャンネル登録要素はYouTube Studio側で配置する。CTA画面にはチャンネル名・説明・CTA本文・軽いブランド装飾のみを置く（draft_v4・人間指定）。
- **疑似subscribe（丸＋✓）を動画側に描画しない**。登録ボタンの実配置はYouTube StudioのEnd Screen要素で行う。
- **右側40〜45%はEnd Screen reserved領域**：装飾・ロゴ・本文・疑似アイコンを置かない。「次はこちら」等の案内ラベルは例外的に可（関連動画枠と被らせない・小さすぎない48px以上）。
- **CTA文字は縮小で押し込まない**：全文を自然な改行（「・」・句点等の意味の切れ目）で2行以内に収め、56px以上（標準60px）を維持。収まらない場合はボックスやカードを広げる。
- 背景装飾（水玉等）は左ブランド枠内に低opacityで配置し、reserved領域・文字と重ねない。
- 表示のみの調整（句点を省く等）は表示文字列に限定し、ナレーション（canonical_text）は変更しない。canonical hash一致ならCTA音声は再利用する。
- CTAのcanonical visual textは、`cta_full_text_visible`でmissing suffix・clipping・crop・ellipsis・box overflowを検査する。1文字でも本文が欠けた場合はFAILとし、フォント縮小ではなく自然な改行・左側boxの確保で修正する。

## セクション構成（基本フォーマット）
1. 冒頭で「今日は何を確認するか」を一覧表示
2. `1 / N` 形式のセクション見出し
3. 本編（説明対象UIの拡大表示）
4. まとめ
5. CTA

CTAの基本トーン: 「役に立ったら、チャンネル登録して、次回も一緒に確認しましょう。」（煽りすぎない）

## 標準ナレーター（001で確定）
- 標準: VOICEVOX「剣崎雌雄」（style: ノーマル / speedScale 1.00 / intonationScale 1.00 / pitchScale 0.00）
- 1文ずつ `audio_query → synthesis` で生成し、segment単位でWAV保存（後から1文だけ差し替え可能）
- 差し替え・再連結は `scripts/tts_voicevox_kenzaki.py --concat-only` で行う
- OpenAI TTSは削除せず、フォールバック/比較用として残す
- 発音調整は `config/voicevox_pronunciation.yaml` を継続利用。人間が聞いて気になった単語だけ追加し、勝手に大量登録しない
- 人間承認済みの音高形状を辞書へ登録する場合は、`/mora_data`後に適用する`pitch_shape`を1つのapproved設定として管理する。`low_high_plateau`は最初のmoraを低く、2mora目以降を同じ高いpitchにそろえ、連続する同一母音（例: `信用を`のオ・オ）はpitch差0とする。provenance（確認日・添付VOICEVOX手動調整）を必ず記録し、該当segmentだけ再生成する。
- クレジット: 本編で VOICEVOX 音声を使う場合は概要欄に「ナレーション：VOICEVOX:剣崎雌雄」を含める

## Episode outputs
各 `episodes/NNN_slug/` に以下を置く。
- `brief.md`
- `sources.md`
- `script.md`
- `shotlist.md`
- `media_manifest.csv`
- `audio/`
- `captions.srt`
- `draft.mp4` または `final/final.mp4`
- `thumbnail/`
- `publish.json`
- `qc.md`

## Automation policy
- 最初の3本は「実機録画・企画最終決定・公開前確認」を人間が行う。
- 再現できた工程だけ `scripts/` に自動化する。
- APIキー・OAuth秘密情報をリポジトリにコミットしない。
- 破壊的操作（素材削除、既存動画上書き）は明示依頼なしで行わない。

## YouTube publication standard
- 公開フローは `finalize → thumbnail確定 → publish dry-run → 人間確認 → privateまたはscheduled upload → API verify → STATE更新` の順にする。
- 公開対象は人間承認済みの `output/final.mp4` だけ。draft、未final、QA未PASS、SHA未記録の動画はuploadしない。
- 自動化で許可するYouTube公開状態は `private` と未来時刻の `scheduled` だけ。即時 `public`、privateからpublicへの自動昇格、動画削除は実装しない。
- OAuthは実際のチャンネル管理アカウントをブラウザで人間が選択し、パスワードを保存しない。`local/youtube/client_secret.json`、`token.json`、`*.json`はGit管理しない。
- 初回OAuth後は `channels.list(mine=true)` のChannel IDを人間承認して保存し、以後ID不一致なら停止する。表示名だけでチャンネルを選ばない。
- upload直後に動画IDを永続化し、thumbnail・予約・verifyの失敗時に再uploadしない。失敗は `--retry-thumbnail` / `--retry-schedule` の対象として個別に扱う。
- YouTube AI開示はpublish metadataの明示boolean `contains_synthetic_media` を `status.containsSyntheticMedia` へ対応させる。写実的なAI人物・実際には存在しない写実的sceneは人間確認の上でtrue、台本・タイトル・字幕補助や明らかな非写実イラストだけでは自動trueにしない。未設定はfalseに推測せず、AI disclosure reviewで停止する。
- 既存動画のAI開示変更は `videos.list(part=status) → 現在の更新可能statusを保持した videos.update(part=status) → videos.listでverify` の順にする。snippet、thumbnail、video ID、privacyStatus、publishAt、made-for-kidsを意図せず変更しない。専用更新でも `videos.insert` は呼ばない。
- 詳細手順と公式仕様は `docs/youtube_publish_automation.md`、初期設定は `docs/youtube_oauth_setup.md` を参照する。

## Phase 2 standard（Episode 003 retrospective）
- sceneはtemplate / official / gpt_imageを役割分担する。正確なUIは公式素材、概念・安心感・人物は人間確認済みGPT画像、一覧・チェックリスト・まとめはtemplateを優先する。
- GPT画像は1scene=1枚の完成した1920×1080 full-frame背景とし、collage、storyboard、contact sheet、split panel、巨大な白い空白を作らない。公式UI・ロゴ・政府マークは生成させない。
- 画像の文字は `text_render_mode` で管理する（詳細は **`docs/text_render_policy.md`**）。`imagegen_native`＝ImageGen内で背景と文字を同時生成（Episode 007以降の新規sceneの既定・サムネイル/セクション扉/1〜2行の短いメッセージ画像向け）。`pil_overlay`＝PIL/HTML等で文字を正確に後乗せ（公式引用・操作手順・URL・数字・日付・PIN・長文・箇条書き・表。旧`text_render_mode=codex`相当）。`no_text`＝画像内に文字を入れない。`codex`/`image`は後方互換別名として受け付ける。
- `NO_IMAGE_TEXT_HYBRID`（canonical name: `no_generated_image_large_text_overlay` / `visual_mode_exclusive`）を恒久ルールとする。`render_mode=gpt_image` / `hybrid` の生成画像へ、大きなheadline・説明カード・主要メッセージを後からPIL/HTMLで重ねない。生成画像sceneはImageGen-native完成画またはno-text完成画の一方、正確な後描画が必要なsceneはtemplate/official等のrenderer-nativeの一方で構成する。字幕・source label・section pill・小さな進行表示など、主役を変えない最小表示だけ例外とする。
- imagegen_nativeのフロー: 生成 → 文字QA（指定文言一致・誤字・脱字・余計な文字・文字化け・漢字置換・行順・文字切れ・端はみ出し・重要オブジェクトとの重なり・コントラスト・スマホ縮小時の可読性。機械は`scripts/text_qa.py`、目視相当は親Codex/Image Agentが担当）→ PASSなら採用／FAILは1回だけ再生成 → 2回目もFAILなら生成画像を採用せずrenderer-nativeへ再設計（3回以上回さない）。PIL renderer・フォント設定・文字サイズQA・linebreak QAは削除せず、renderer-nativeの正確性重視の役割として残す。
- animationはstaticを既定とし、人物・説明画面はvery slow zoomを優先する。意味のないhorizontal panは使わない。contact sheetは動画生成前に必須とする。
- `方`、単独の`今`など文脈依存語は共通VOICEVOX辞書へ登録しない。人間承認済みの`App Store`→`アップストア`（1句、accent 5）は既存辞書を壊さず再利用する。
- CTAは前Episode固有文言を無条件に流用せず、通常は`channel_common_cta`（`config/channel_cta.json`）を使う。承認前draftは上書きせず、finalizeは承認draftのcopy-onlyとする。
- QAの視覚バランス・左右余白・letterbox・公式画面サイズはWARN候補として記録し、最終判断は人間が行う。制作メトリクスは`work/production_metrics.json`へ残す。
- Episode 001/002/003の完成済みfinalは変更しない。Episode 004/005を現行Phase 2で制作後、実績に基づいてPhase 3を判断する。

## Subagent orchestration policy（Episode 005以降）

- 親Codexをオーケストレーターとし、独立して処理できる作業は、時短に寄与する場合に限りサブエージェントへ並列委譲してよい。並列化そのものを目的にサブエージェントを増やさない。
- 未完了の上流成果物に依存する作業は、上流が確定するまで開始しない。危険な変更、事実が曖昧な判断、公開範囲やプライバシーに関わる判断は人間ゲートに残す。
- サブエージェントは調査結果・レビュー・初稿などの成果物を返し、最終的なcanonical fileの反映は親Codexが行う。

### Canonical single-writer

以下をcanonical fileとして扱い、サブエージェントが同時に直接編集しない。

- `episode.json`
- `script.md`
- `shotlist.md`
- `publish.json`
- `STATE.md`
- `work/production_metrics.json`
- `config/*`
- 共通template
- final output

サブエージェントの成果物は、原則 `work/subagents/<episode_id>/`（または親Codexが指定した一意の`work/subagents/`配下）へ保存する。親Codexが内容を読み、矛盾を解消し、必要なcanonical fileへ単独で反映する。

### Phase Aの委譲

企画・一次情報・台本が未確定の段階では、次を可能なら並列化する。

- research: 一次情報、公的機関・公式ソース、数字・日付・制度、source candidates → `research_report.md`
- title/topic analysis: 視聴者向けの切り口、title candidates、thumbnail copy、過度な煽りの回避 → `title_analysis.md`
- structure/script reviewer: 6〜7分程度の構成、順序、重複、シニア向けの言葉 → `script_review.md`

research未確定の事実をtitle/topic analysisやstructure/script reviewerが断定してはならない。「要research確認」と記録する。

親Codexがresearchを統合してscriptと`episode.json`初版を作った後は、Fact Check（scriptとsourcesの突合）とVisual（script/shotlistからのscene plan）を並列化してよい。Visual Agentは`render_mode`、scene目的、visual focal point、text-safe area、animation recommendationを返すが、canonical `episode.json`は直接変更しない。

### GPT画像生成の委譲（Episode 005以降）

独立したGPT画像sceneは、原則としてImage Agentへ並列委譲してよい。必ず次の対応を守る。

- **1 Image Agent = 1 scene = 1 image = 1 unique output path**
- 親Codexが起動前にscene ID、担当prompt、出力filename/pathを一意に決める。
- 各Image Agentには担当sceneに必要な最小限の情報だけを渡し、他sceneのprompt一覧やmanifest全文を渡さない。
- 同じsceneの複数agentへの重複割当、同じfilenameへの保存、他sceneのprompt・画像の参照を禁止する。
- 1回の生成で複数候補が返っても、採用対象はそのsceneの1枚だけとし、残りを他sceneに割り当てない。
- collage、storyboard、split panel、grid、multi-scene prompt、画像AIによるcontact sheetを禁止する。variantsは明示依頼がある場合だけ作る。
- 生成後は各agentが画像破損、width/height、aspect ratio、file size、SHA-256を確認して親Codexへ返す。canonical fileは変更しない。
- imagegen_native sceneのImage Agentは、生成後に担当sceneの文字を目視相当で確認し（指定文言一致・誤字・脱字・余計な文字・文字化け・行順・文字切れ・はみ出し・重なり・コントラスト・縮小時可読性）、結果を親Codexへ返す。親Codexは`scripts/text_qa.py`と併せて文字QAし、NGは1回だけ再生成、2回目NGは生成画像を捨てて`text_render_mode=pil_overlay`のrenderer-native sceneへ再設計する（生成画像を背景として再利用しない。docs/text_render_policy.md）。

依存関係のないsceneは、実行環境の上限まで同時実行してよい。7sceneなら最大7 Image Agentを候補とし、同時実行数に制限がある場合は3+3+1などのbatchに分ける。scene間に依存がある場合は無理に並列化しない。PoCのA→B→C逐次実行はscene分離と保存の検証方法であり、Episode 005以降の並列化を禁止する根拠ではない。

全Image Agent完了後、親Codexがrequired scenes、filename、重複hash、破損、scene取り違え、collage、blank white half、readable generated text、official UIのAI再現を一括確認する。Codex/Pythonでcontact sheetを作り、人間がscene内容・重複・余白・読みやすさを確認する。NG sceneだけをそのscene専用agentで再生成し、承認済みsceneは再生成しない。1672×941等の原本は保持し、render時に1920×1080の正規化copyを作る。

### Phase Bの委譲

画像とsceneが揃った後は、Audio QA（pronunciation、数字、記号、固有名詞）、Visual QA（改行、重心、余白、旧Episode混入、公式画面の可読性）、Metadata（title、description、chapters、tags、source links、VOICEVOX credit、AI disclosure candidate）を可能なら並列化する。成果物は`work/subagents/<episode_id>/`へ返し、`publish.json`、global辞書、final outputは直接編集しない。YouTube uploadとfinalizationは常に単一writer・単一実行とする。

### Human Gateとmetrics

Episode 005以降の標準Human Gateは、原則として次の4回程度に整理する。

1. テーマ・台本
2. scene contact sheet ＋ pronunciation REVIEW
3. full draft
4. thumbnail / publish

重大なfact ambiguity、pronunciation不明、official UI確認、プライバシーや公開範囲の問題がある場合は途中でSTOPしてよい。

`work/production_metrics.json`には既存項目を維持したまま、必要に応じて`subagent_count`、`parallel_task_groups`、`image_generation_agents`、`image_generation_parallel_batches`、`image_generation_calls`、`image_regeneration_calls`、`image_generation_elapsed_seconds`、`human_gate_count`、`human_correction_rounds`、`phase_a_minutes`、`phase_b_minutes`、`finalization_minutes`を追加記録する。未計測値は推測せず`null`とする。

今回の変更はEpisode 005以降の運用方針と軽量な補助構造に限定し、Episode 005本体の作成、本番画像生成scriptの大規模新設、Episode 001〜004の成果物変更は行わない。

## 画像の文字レンダリング方針（Episode 007以降）

短い文字入り画像（サムネイル・セクション扉・オープニング/クロージング・1〜2行のキャッチコピー・感情＋短い見出し・クロージング前の概念scene）は、原則 **ImageGen内で背景と文字を同時生成（`imagegen_native`）** を正式な第一候補とする。**2026-09-03にEpisode 007 SCENE-003で実施したA/B比較（imagegen_native一体生成 vs Codex renderer文字後描画）で人間がCandidate Aを明確に採用**しており、以降の恒久ルールである（詳細・実績は `docs/text_render_policy.md`）。`NO_IMAGE_TEXT_HYBRID`により、生成画像を背景として残したまま大きな文字をCodex rendererで後乗せする構成は採用しない。文字QAに失敗した場合は1回目再生成→2回目で判断し、それでも品質が安定しないsceneは生成画像を捨ててrenderer-native（template/official + `pil_overlay`）へ再設計する（全sceneを巻き戻さない）。公式引用・操作手順・URL・数字・日付・PIN・長文・箇条書き・表・比較・CTA・正確なUI説明は引き続き`pil_overlay`/Codex renderer優先。`no_text`は文字を一切入れない画像専用。imagegen_nativeで文字を生成するsceneは必ずexact text QA（誤字・脱字・余計な文字・文字崩れ・漢字・句読点の完全一致）をPASSしたものだけ採用し、1文字でも誤ればFAIL。表示文字は原則 大見出し1〜2行＋補助0〜1行（総文字量30〜40文字程度以下を推奨）。「1/5」等の小さな進行表示はimagegen_nativeに無理に生成させず、必要ならsection pill・小さな進行表示としてCodex overlayで後付けしてよい（メインVisual+メイン見出し=imagegen_native／進行表示のみ最小overlay）。canonicalな定義・QA項目・retryルールは `docs/text_render_policy.md` に集約し、ここでは重複しない。Episode 001〜006の完成済み成果物は変更しない。

## Definition of done
公開候補は以下をすべて満たす。
- Fact / Language / Visual / Audio / Policy / Privacy の重大指摘が0件
- 主要な事実に一次情報URLがある
- 実機手順とナレーションが一致
- タイトル・サムネが内容以上に断定していない
- 説明欄に主要な根拠URLがある
