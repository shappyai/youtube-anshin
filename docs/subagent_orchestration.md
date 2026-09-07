# Episode 005以降のsubagent orchestration方針

## 目的と範囲

親Codexをオーケストレーターとして、独立作業を必要に応じてサブエージェントへ委譲し、制作時間を短縮する。canonical fileの競合編集を防ぎ、親Codexの統合と人間の最終判断を残す。

この文書はEpisode 005以降の運用方針であり、Episode 005本体の作成や既存Episode 001〜004の成果物変更を行うものではない。本番画像生成scriptの大規模新設もこの方針の範囲外とする。

## 1. 基本原則

- 独立タスクは、時短に実効性がある場合に限り並列委譲する。
- 上流の未完成成果物に依存するタスクは、依存先が確定するまで開始しない。
- 並列化のためだけにサブエージェントを作らない。
- サブエージェントは findings / artifacts / draft を返し、最終canonical mutationは行わない。
- 親Codexが成果物を読み、矛盾を解消し、canonical fileへ単独で反映する。
- 事実が曖昧なもの、危険な変更、プライバシー、公開範囲、公式画面の最終判断は人間ゲートに残す。

## 2. canonical single-writer

複数サブエージェントが同時に直接編集してはならない対象:

- `episode.json`
- `script.md`
- `shotlist.md`
- `publish.json`
- `STATE.md`
- `work/production_metrics.json`
- `config/*`
- 共通template
- final output

サブエージェント成果物の標準保存先は `work/subagents/<episode_id>/` とする。親Codexがepisode単位の一意な出力先を先に作り、次のようなファイルを置く。

```text
work/subagents/<episode_id>/
  research_report.md
  title_analysis.md
  script_review.md
  fact_check.md
  visual_plan.json
  pronunciation_review.md
  visual_qa.md
  metadata_draft.json
```

各成果物は、原則として次の形式にする。

- conclusion
- PASS / REVIEW / FAIL
- findings
- source/reference
- recommended change
- confidence

## 3. Phase A — 企画と初稿前

research未確定の事実を、title/topic analysisやstructure/script reviewerが独自に断定してはならない。必要な箇所は「要research確認」と記録する。

| Agent | 役割 | 出力 |
|---|---|---|
| Research Agent | 最新一次情報、公的機関・公式ソース、数字・日付・制度、source candidates | `research_report.md` |
| Title/Topic Agent | 視聴者向けの切り口、title candidates、thumbnail copy、過度な煽り回避 | `title_analysis.md` |
| Structure/Script Agent | 6〜7分程度の構成、話の順番、重複・冗長、シニア向けの言葉 | `script_review.md` |

親Codexがresearch結果を統合し、scriptと`episode.json`初版を作成する。この統合前にFact Checkや最終Visual planを開始しない。

## 4. Phase A — 初稿後

親Codexがresearchを反映したscript / sources / `episode.json`初版を作った後、次を並列化できる。

- Fact Check Agent: numerical claims、dates、official wording、overly strong claims、unsupported claims、source mismatch → `fact_check.md`
- Visual Agent: `render_mode`、official/template/gpt_image、scene purpose、visual focal point、text-safe area、animation recommendation → `visual_plan.json`

Visual Agentはcanonical `episode.json`を直接変更しない。

## 5. GPT画像生成 — 独立sceneの並列運用

### 正式方針

PoCではA→B→Cを逐次実行し、scene単独prompt、1scene=1image、自動保存、duplicateなし、contact sheet自動生成を確認した。この逐次順序はsceneの分離を検証するための方法であり、Episode 005以降の並列化を禁止する制限ではない。

依存関係のないGPT画像sceneは、原則としてImage Agentへ並列委譲する。必須契約は次のとおり。

**1 Image Agent = 1 scene = 1 image = 1 unique output path**

### 起動前のassignment

親Codexが各agentに次だけを渡す。

- scene_id
- 一意のoutput filename/path
- scene purpose
- scene専用image prompt
- `text_render_mode`（`imagegen_native` / `pil_overlay` / `no_text`）と、`imagegen_native` の場合は正確な日本語文言（headline / support_text）・行数・配置・文字サイズ・コントラスト・余白・最終比率
- visual style
- prohibited content
- safe area
- `1scene = 1image`契約

他sceneのprompt一覧、manifest全文、前sceneの画像は渡さない。親Codexが起動前にsceneとoutput pathを一意に予約し、各agentは割り当てられた1ファイル以外を書き込まない。

### 並列数

依存関係のないsceneは、実行環境の同時実行上限まで並列化する。GPT画像が7sceneなら最大7 Image Agentを候補とし、上限がある場合は3+3+1などのbatchでよい。sceneが別sceneの結果に依存する場合は、その依存関係を優先して並列化しない。

### 禁止事項

- 1agentへ複数sceneを渡す
- 1agentが複数sceneを生成する
- 同じsceneを複数agentへ重複割当する
- 複数agentが同じfilenameへ保存する
- 他agentのpromptや前scene画像を参照する
- collage、storyboard、split panel、gridを作る
- 複数sceneのpromptを同じ画像生成callへ渡す
- image AIにcontact sheetを作らせる
- 明示依頼のないvariantsを作る

画像生成機能が1回に複数候補を返す場合でも、担当sceneの採用画像は1枚だけとする。残り候補を別sceneへ割り当てず、必要なら破棄する。

### Agent完了条件と親QA

各Image Agentは担当sceneについて、image generation、local save、valid image、width / height、aspect ratio、file size、SHA-256を確認し、結果を親Codexへ返す。`imagegen_native` のsceneは、生成画像の文字を目視相当で確認し（指定文言一致・誤字・脱字・余計な文字・文字化け・漢字置換・行順・文字切れ・端はみ出し・重要オブジェクトとの重なり・コントラスト・スマホ縮小時の可読性）、その結果も返す。canonical `episode.json`などは変更しない。

全agent完了後、親Codexが次を一括確認する。

- required scenes N/N
- filenameとscene IDの一致
- duplicate hashなし
- image破損なし
- scene取り違えなし
- collageなし
- blank white halfなし
- imagegen_native以外のsceneに読める生成文字がないこと（pil_overlay / no_text）
- imagegen_nativeのsceneは文字QA（指定文言一致・誤字脱字・文字化け・行順・文字切れ・はみ出し・重なり・コントラスト・縮小時可読性）を `scripts/text_qa.py` と目視で確認
- official UI・ロゴ・政府マークのAI再現なし

1672×941等の原本はそのまま保持し、render時に1920×1080の正規化copyを作る。原本を上書きしない。

### Contact sheetと再生成

全画像完了後、親Codex/Pythonがcontact sheetを1回作る。image AIには作らせない。人間はcontact sheetを1回確認し、scene内容、重複、blank white half、collage、text-safe area、50〜70代向けの見やすさ、official UIの誤生成、imagegen_nativeの文字（指定文言一致・誤字・可読性）、`NO_IMAGE_TEXT_HYBRID`違反がないことを確認する。

NG sceneだけ、そのscene専用のImage Agentを1回だけ再実行する（prompt調整）。imagegen_nativeの文字QAが2回連続FAILしたsceneは、生成画像を採用せず、template/official等のrenderer-native sceneへ再設計する。生成画像を背景として残したままPIL/HTMLで大きな文字を後乗せするfallbackは禁止する。承認済みsceneや全画像を再生成しない。再生成回数・renderer-native再設計はmetricsへ記録する。

## 6. Phase B — 画像・scene確定後

画像とsceneが揃った後、次は可能なら並列化する。

| Agent | 役割 | 出力 |
|---|---|---|
| Audio QA Agent | pronunciation候補、多義語、電話番号、数字、記号、proper noun | `pronunciation_review.md` |
| Visual QA Agent | 日本語改行、1文字孤立、左右重心、oversized blank area、旧Episode混入、official screenshot readability、item count mismatch | `visual_qa.md` |
| Metadata Agent | title、description、chapters、tags、source links、VOICEVOX credit、AI disclosure candidate | `metadata_draft.json` |

Audio QAはglobal dictionaryを自動変更しない。Metadata Agentは`publish.json`を直接編集しない。YouTube uploadとfinalizationは常に単一writer・単一実行とする。

## 7. Human Gate

Episode 005以降の標準は、原則として次の4回程度とする。

1. テーマ・台本
2. scene contact sheet ＋ pronunciation REVIEW
3. full draft
4. thumbnail / publish

重大なfact ambiguity、pronunciation不明、official UI確認、プライバシー、公開範囲の問題がある場合は、ゲートを増やしてSTOPしてよい。

## 8. Metrics

既存metricsを壊さず、次を必要に応じて追加する。

- `subagent_count`
- `parallel_task_groups`
- `image_generation_agents`
- `image_generation_parallel_batches`
- `image_generation_calls`
- `image_regeneration_calls`
- `image_generation_elapsed_seconds`
- `human_gate_count`
- `human_correction_rounds`
- `phase_a_minutes`
- `phase_b_minutes`
- `finalization_minutes`

未計測値は`null`とする。Episode 004以前の値を推測して埋めない。目的は逐次生成と並列生成の制作時間、再生成回数、human gate数を比較できるようにすることである。
