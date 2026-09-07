# 画像の文字レンダリング方針（Episode 007以降の標準）

確認日: 2026-09-03

この文書は画像への文字入れ方式の **canonical方針** である。他のドキュメントは詳細を重複させず、この文書を参照する。Episode 001〜006の完成済み成果物・manifestは変更しない。この方針は「今後生成する画像のdefault」であり、過去Episodeの再解釈や再生成を行わない。

2026-09-06にEpisode 014の人間確認で確定した恒久ルール `NO_IMAGE_TEXT_HYBRID`（canonical name: `no_generated_image_large_text_overlay` / `visual_mode_exclusive`）を追加する。生成画像を主役にするsceneは、ImageGen-native完成画またはno-text完成画として扱い、生成画像へ大きな見出し・説明カードを後から重ねない。renderer-native sceneはcommon background・公式素材・semantic icon・正確な文字をPIL/HTMLで構成する。sceneの主要visual modeはこのどちらか一方だけにする。

## 1. 標準フロー（旧 → 新）

旧方式（Episode 006まで）:

```text
背景画像を生成 → PIL/Codexで文字を後乗せ → QA
```

新方式（Episode 007以降の標準）:

```text
ImageGenで背景＋文字を同時生成（imagegen_native）
→ 文字QA
→ PASS : そのまま採用
→ FAIL : promptを調整して1回だけ再生成
→ 2回目もFAIL : その生成画像は採用せず、renderer-native sceneとして再設計
```

原則3回以上ImageGenを回さない（APIコスト・待ち時間・同じ文字崩れの繰り返し防止）。2回目の文字QA FAIL後に「絵だけ採用して後から大きな文字を重ねる」fallbackは禁止する。人間が再生成を明示しても、生成画像＋大きな後乗せ文字へ戻す例外は設けない。

## 2. text_render_mode

scene / generation manifest / image agent assignment は以下の3値で管理する。既存Episodeが使う `codex` / `image` は後方互換の別名として受け付ける（`codex` = `pil_overlay`、`image` = `imagegen_native`）。

| 値 | 意味 |
|---|---|
| `imagegen_native` | ImageGen内で背景と文字を同時生成する。**今後の新規sceneの既定** |
| `pil_overlay` | renderer-nativeのcommon background・公式素材・実画面へ、PIL / HTML / deterministic rendererで文字を正確に重ねる（旧`codex`相当）。生成画像背景への大きな文字overlayには使わない |
| `no_text` | 背景・人物・イラストのみ生成し、画像内に文字を入れない |

未指定の場合のdefaultは、今後の新規sceneでは原則 `imagegen_native` とする（既存Episodeは明示値があるため再解釈されない）。`templates/episode.example.json` や `scene_mode_advisor --fixture-output` は新規sceneに `imagegen_native` をセットする。

## 3. imagegen_native を使う対象（原則）

- YouTubeサムネイル
- セクション扉
- オープニング画像
- クロージング画像
- 短いキャッチコピー付き画像
- 1〜2行程度のタイトル画像
- 雰囲気・世界観と文字デザインの一体感が重要な画像
- 「のんびり、いこう。」「今日もいい一日を。」のような短いメッセージ画像

ImageGenへの指示には、文字を「後から追加する前提」にせず、以下を含める。

- 正確な日本語文言（sceneのheadline / support_textを正とする。promptへハードコードしない）
- 行数と行順
- 配置（余白のある場所）
- 大まかな文字サイズ
- 背景とのコントラスト
- 文字が人物・重要オブジェクトに重ならないこと
- 文字が画像端にはみ出さないこと
- 16:9 / 9:16 等の最終比率

## 4. pil_overlay を使う対象（最初から選択してよい）

- 公式情報の引用
- 操作手順
- UI説明
- URL
- 数字
- 日付
- PIN等の正確性が重要な表記
- 長文
- 箇条書き
- 表
- 1文字の誤りも許容できない情報
- 法的/注意事項
- 公式文言
- ImageGenが2回連続で文字QA FAILした画像

Episode 006のLINE公式手順引用カードのような素材は、今後もPIL/HTML等のdeterministic描画を使う。これをImageGen文字へ置き換えない。

## 5. ImageGen文字QA（imagegen_native生成後は最低限以下を確認）

Must:

- 指定文言と一致している
- 誤字なし
- 脱字なし
- 余計な文字なし
- 文字化けなし
- 不自然な漢字置換なし
- 行順正常
- 文字切れなし
- 画像端にはみ出していない
- 人物や重要オブジェクトと重なっていない
- 背景とのコントラスト十分
- スマホ縮小時でも主見出しが読める

OCR依存だけにせず、Image Agent / visionによる目視相当チェックも利用する。機械チェックは `scripts/text_qa.py`（文言仕様の存在・prompt一致・画像サイズ・破損・重複hash等）と親Codexの目視で行い、複雑なOCR基盤は作らない。

## 6. Retryルール

```text
1回目 FAIL → promptを調整して1回だけ再生成
2回目 FAIL → 生成画像を採用せず、common background等を使うrenderer-native sceneへ再設計
```

`scripts/text_qa.py --fail` がretry回数を数え、2回目FAILで `renderer_only_required` を返す。renderer-nativeへ変更する場合は、生成画像背景を使い回さず、common background・公式素材・deterministic rendererでsceneを作り直す。PIL renderer・フォント設定・文字サイズQA・linebreak QAは削除せず、renderer-nativeの正確性を担う。

## 7. ImageGen promptの組み立て

`scripts/build_image_generation_manifest.py` がsceneの文言を正としてpromptを組み立てる。例（イメージ）:

```text
青空と丘の背景。左上に日本語で正確に「のんびり、いこう。」
その下に「今日もいい一日を。」と表示。
白文字＋青系の縁取り。スマホ表示でも読みやすい大きさ。
文字は画像内で完全に収める。
```

## 8. サムネイル方針

YouTubeサムネイルも `imagegen_native` を第一候補とする。

1. ImageGenで人物/背景/文字を一体生成
2. 文字QA PASSなら採用
3. 1回だけ再生成
4. それでもNGなら生成画像を再利用せず、common background等のrenderer-nativeへ再設計（`scripts/make_thumbnail.py` 等の正確な文字描画は継続利用）

制約: タイトル全文を詰め込まない / 主見出しは短く（2〜6語） / 50〜70代でも読める文字サイズ / 文字と人物を干渉させない / 小さい補助文字を増やしすぎない。

## 9. 関連ファイル

- schema: `templates/episode.schema.json`（`scene.text_render_mode`）
- 検証・default: `scripts/episode_io.py`
- manifest: `scripts/build_image_generation_manifest.py`
- renderer: `scripts/hybrid_scene_renderer.py`
- advisor: `scripts/scene_mode_advisor.py`
- 文字QA: `scripts/text_qa.py`（新規）
- 運用ドキュメント: `docs/phase2_hybrid_production.md`, `docs/subagent_orchestration.md`, `docs/build_episode_plan.md`, `docs/thumbnail_pipeline.md`, `AGENTS.md`
- schema: `templates/episode.schema.json`（`scene.text_render_mode`）
- 検証・default: `scripts/episode_io.py`
- manifest: `scripts/build_image_generation_manifest.py`
- renderer: `scripts/hybrid_scene_renderer.py`
- advisor: `scripts/scene_mode_advisor.py`
- 文字QA: `scripts/text_qa.py`（新規）
- 運用ドキュメント: `docs/phase2_hybrid_production.md`, `docs/subagent_orchestration.md`, `docs/build_episode_plan.md`, `docs/thumbnail_pipeline.md`, `AGENTS.md`

## 10. A/B実績と恒久化（2026-09-03・Episode 007）

Episode 007 SCENE-003（セクション扉「スマホが、対応しているか」）で controlled A/B test を実施し、**人間が Candidate A（imagegen_native 背景＋短い日本語文字の一体生成）を明確に採用**した。理由: TV視聴で読みやすい／画面の完成度が高い／テンプレ感が少ない／文字とビジュアルの一体感／50〜70代向けでも落ち着いている／exact textもPASS。

### 恒久ルール（このA/B結果を基に確定）

1. **section扉 / concept title scene（短い見出しが主役）は imagegen_native を正式な第一候補**とする。対象: セクション扉・導入の概念scene・「まず確認すること」等の短いタイトルscene・感情＋短い見出し・クロージング前の概念scene。
2. **表示文字は短く**: 大見出し1〜2行＋補助0〜1行。総文字量30〜40文字程度以下を推奨（機械的上限ではなく読みやすさ優先）。長文・一覧・比較・手順・数字・公式仕様・注意・表・CTA・official screenshot上の補足は従来どおり Codex renderer / `pil_overlay` 優先。
3. **exact text QA 必須**: 誤字・脱字・余計な文字・文字崩れ・指定漢字・句読点の完全一致・readable Japanese・文字途中欠け・TV readability・subtitle safe area・no fake UI・no collage・no old episode leakage。1文字でも誤りがあればFAIL（「雰囲気が良いから許容」は禁止）。
4. **retry policy**: FAIL時は1回目再生成→2回目も不安定なら**そのsceneだけ** renderer-nativeへ再設計。生成画像を背景として残したまま`pil_overlay`するfallbackはしない。全sceneを巻き戻さない。
5. **小さな補助表示の例外**: 「1/5」等の小さな進行表示、section pill、source label、字幕は、sceneの主役を変えない範囲でCodex overlayを許可する。生成画像へ大きなheadline・説明カードを重ねることは許可しない。
6. **imagegen_native sceneのrender**: 基本full_bleed。巨大な白カードを重ねる・画像を小さな枠へ縮小する・文字を二重表示する・AI文字の上へ同じCodex文字を重ねる、を禁止。Codex後付けはsection pill・progress・小さなchapter indicator程度。`hybrid_scene_renderer.py` は template＋`imagegen_native` のsceneをfull-bleed配置（文字オーバーレイなし）で処理する。
7. **official UIは今後もAI生成禁止**（このルール変更で「AIで公式UIも作ってよい」ことにはならない）。実画面・Emulator・公式画像・official cropのみ。GPT画像の文字を official UI の代替にしない。
8. **人間レビューの考え方**: 「AI文字生成は危険だから禁止」でも「AI生成だから必ず高品質」でもなく、**実物の品質で判断**する。新しいscene type・文字量が多い場合はcontact sheet（`imagegen_native_text_contact_sheet.png`等）で人間確認。
9. **記録すべきmetrics**: `imagegen_native_text_scene_count`・`imagegen_native_text_regeneration_count`・`imagegen_native_text_fallback_count`・`exact_text_pass_count`・`exact_text_fail_count`・`hybrid_generated_image_large_text`（実測のみ・推測禁止）。`imagegen_native_text_fallback_count`は旧記録との互換用で、新規の2回目FAILはrenderer-native再設計として記録する。

### Episode 007 実績（この文書の基準として）

- A/B対象: SCENE-003（表示文言「スマホが、対応しているか」＋「まずは、端末とアプリの準備から。」）
- 成果物（削除しない）: `episodes/007_myna_app_login/work/phase_b_review/ab_test_candidate_A.png`（採用）／`ab_test_candidate_B.png`（比較履歴）／`imagegen_native_ab_test.png`（比較画像）
- Candidate A: 文字完全一致PASS・TV readability PASS・下部180px相当の安全領域クリア・no fake UI／生成約32秒・再生成0回
- Candidate B（Codex renderer・本番パイプライン）: 文字100%正確・見出し104px（テンプレート既定）
- 本ルールの旧記述（「日本語文字はAIで生成しない」等の絶対禁止）が残っているドキュメントは、このセクションを正として更新・解釈する。official UI禁止ルールは変更しない。

## 11. Internal brand promise のviewer-facing禁止（恒久）

```yaml
internal_brand_promise: "怖がらせる前に、確認する。"
classification: INTERNAL_ONLY
viewer_facing: FORBIDDEN
viewer_facing_internal_brand_promise: 0
```

上記の文言はブランド理念・内部企画・制作メモとしては保持できるが、完成動画のscene text、renderer text、ImageGen prompt/generated-text QAの表示仕様、字幕、ナレーション、CTA、thumbnail/end card、overlay、descriptionの表示用metadataへ出してはならない。`scripts/viewer_facing_text_qa.py` をEpisode/Shortsのpreflightとupload前に実行し、1件でも検出したらbuild/uploadを停止する。生成済みラスター内の文字は、既存のImageGen文字QAとHuman Visual Gateで併せて確認する。
