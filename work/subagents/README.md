# subagent成果物置き場

Episode 005以降、サブエージェントの調査・レビュー・初稿は、canonical fileを直接編集せず、この配下へ保存する。

## 保存ルール

- 親Codexが先にEpisode単位の一意な出力先を決める。標準は `work/subagents/<episode_id>/`。
- `episode.json`、`script.md`、`shotlist.md`、`publish.json`、`STATE.md`、`work/production_metrics.json`、`config/*`、共通template、final outputはサブエージェントが直接変更しない。
- 同じファイルを複数agentが同時に書かない。
- 成果物は親Codexが読み、矛盾を解消してからcanonical fileへ反映する。

## 推奨成果物

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

各成果物には、可能な範囲で次を含める。

- conclusion
- PASS / REVIEW / FAIL
- findings
- source/reference
- recommended change
- confidence

## Image Agent

GPT画像sceneは、親Codexがscene ID、scene専用prompt、unique output pathを事前に割り当てる。

**1 Image Agent = 1 scene = 1 image = 1 unique output path**

Image Agentには他sceneのpromptやmanifest全文を渡さない。担当sceneの画像生成、保存、valid image、width / height、aspect ratio、file size、SHA-256を確認して結果を返す。`text_render_mode=imagegen_native` のsceneは、生成画像の文字を目視相当で確認し（指定文言一致・誤字・脱字・余計な文字・文字化け・行順・文字切れ・はみ出し・重なり・コントラスト・縮小時可読性）、結果も返す。文字QAのcanonicalルールは `docs/text_render_policy.md`。contact sheetは親Codex/Pythonが作り、画像AIには作らせない。NG sceneだけ専用agentで1回再生成し、2回目NGは`pil_overlay`へfallbackする。

## 注意

依存関係のある作業は上流確定前に開始しない。YouTube upload、finalization、公開範囲やプライバシーに関わる判断は単一writer・人間ゲートで扱う。
