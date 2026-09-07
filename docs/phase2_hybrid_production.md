# Phase 2 ハイブリッド制作フロー

Episode 003で通過確認した標準。正確なUI・公式素材を守りながら、template、official、gpt_imageをsceneごとに役割分担させる。Episode 005以降のサブエージェント委譲の詳細は `docs/subagent_orchestration.md` に記録する。

## 標準手順

1. topic research → sources → scriptを人間が確定する。
2. `episode.json` を作成し、subtitleを意味単位で確定してからsceneごとに `render_mode` を決める。未指定の既定は `template`。
3. `python scripts/scene_mode_advisor.py episodes/NNN_slug/episode.json` で推奨を確認する。推奨は元データを変更しない。
4. `python scripts/build_image_generation_manifest.py episodes/NNN_slug/episode.json` でGPT画像の指示書を作る。1scene=1 PNG、完成したfull-frame背景を要求し、`text_render_mode` に応じて文字の扱いを組み込み、親CodexがsceneごとのImage Agent assignmentへ分割する。
5. 依存関係のないGPT画像sceneは、親Codexが一意のoutput pathを割り当てたうえで、1agent=1scene=1imageとして可能なら並列生成する。各agentの結果を親Codexが統合QAし、`imagegen_native` のsceneは文字QA（`python scripts/text_qa.py episodes/NNN_slug/episode.json`）を行う。`python build_episode.py NNN --dry-run` でPhase Aの全ゲートを確認する。GPT画像は `assets/generated_ai/scene_NNN.png` に置き、1920×1080・PNG・下180px字幕安全領域を満たす。
6. pronunciation REVIEWは人が文脈内で聞いて判断し、承認したsegmentだけ `work/human_review.json` に記録する。辞書は自動変更しない。
7. GPT画像を含むcontact sheetを親Codex/Pythonで動画生成前に一度作り、人間が確認する。余白、公式画面サイズ、AI/template混在、視覚的重心を確認し、NG sceneだけを再生成する。
8. `python build_episode.py NNN --continue --output-name draft_auto_v1.mp4` でscene、差分音声、字幕、動画、QAを生成する。共通CTAを使う場合は `postroll.cta_profile=channel_common_cta` を指定する。
9. `draft_auto_v1.mp4` を最後まで視聴し、指摘があればsceneまたはsegmentだけ差分修正してv2、v3へ保存する。承認後に `human_review.json` の `video.draft_auto_vN: approved` を記録し、`python build_episode.py NNN --finalize` でcopy-only finalizeする。

`--rerender-scene 12` はscene 012だけ、`--regen-segment 34` は音声segment 034だけを再生成する。`--output-name draft_auto_v2.mp4` のように承認前draftを版管理し、既存のdraft/finalは上書きしない。既存のdraft名を指定したbuildは安全のため停止する。

## render_mode

- `template`: 一覧、比較、まとめ、正確な文字中心。
- `gpt_image`: 概念、注意喚起、章扉など視覚中心。公式UIやロゴを生成させない。
- `official`: 実画面、公式図、引用をそのまま見せる。
- `hybrid`: 既存の互換モード。生成画像を背景として残したまま大きな日本語を後乗せする用途は `NO_IMAGE_TEXT_HYBRID` により禁止し、新規sceneは imagegen-native完成画またはrenderer-nativeへ寄せる。

`gpt_image` は人間確認済みの完成背景を使用する意味で、Codexの再デザインではない。文字の入れ方は `text_render_mode` で管理し、**Episode 007以降の新規sceneは `imagegen_native` を既定**とする。

- `imagegen_native`: ImageGen内で背景と文字を同時生成。サムネイル、セクション扉、オープニング/クロージング、1〜2行の短いメッセージ画像向け。生成後は文字QA（指定文言一致・誤字脱字・文字化け・行順・文字切れ・はみ出し・重なり・コントラスト・縮小時可読性）を `scripts/text_qa.py` と目視で行い、PASSなら採用／FAILは1回だけ再生成／2回目FAILなら生成画像を採用せずrenderer-nativeへ再設計する。
- `pil_overlay`: template/official等のrenderer-native sceneで、PIL/HTML等により文字を正確に後描画（旧 `codex` 相当）。公式引用・操作手順・URL・数字・日付・PIN・長文・箇条書き・表は最初からこれを選ぶ。生成画像を背景として残したまま大きな文字を後乗せする用途は禁止する。大型白カード、AI画像の縮小、新レイアウト、画面半分の白塗りは禁止し、文字周囲の小さなscrim、shadow、outlineだけを許可する。
- `no_text`: 文字を一切入れない。背景・人物・イラストのみ。

`codex` / `image` は過去Episodeの後方互換別名（`codex`=`pil_overlay`、`image`=`imagegen_native`）。canonicalな定義は `docs/text_render_policy.md`。

### GPT画像の恒久契約

- manifest共通promptは「Generate exactly ONE standalone 16:9 image for this scene. Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes.」を含む。
- 背景はedge-to-edge full-frame。blank white half、large empty white area、presentation card layoutは明示的に必要なscene以外は禁止。
- fitの優先順は `full_bleed` → 軽微な比率差の `crop` → 明示指定時だけ `cover_blur`。
- 下部180pxは字幕安全領域。公式UI・サービスロゴ・政府マークはGPT画像へ生成させない。日本語の短い1〜2行は `imagegen_native` ではImageGenに正確な文言を生成させて文字QAし、長文・公式文言・数字類は `pil_overlay`（Codex/実在素材）で扱う。

### GPT画像のsubagent orchestration（Episode 005以降）

PoCのA→B→C逐次生成は、scene単独prompt、1scene=1image、自動保存、重複なし、contact sheet作成を検証した実行順であり、以後の並列化を禁止する制限ではない。依存関係のないGPT画像sceneは、原則としてImage Agentへ並列委譲する。

- 1 Image Agent = 1 scene = 1 image = 1 unique output path。
- 親Codexが起動前にscene ID、scene専用prompt、filename/pathを一意に予約する。
- 他sceneのprompt一覧・manifest全文・前scene画像をImage Agentへ渡さない。
- 同じsceneの重複割当、同じfilenameへの保存、複数sceneのprompt、collage、storyboard、split panel、grid、画像AIによるcontact sheetを禁止する。
- 複数候補が返っても、そのsceneの採用は1枚だけ。残りを別sceneに使わない。
- 各agentはvalid image、dimensions、aspect ratio、file size、SHA-256を確認し、親Codexへ結果を返す。canonical fileは直接編集しない。
- imagegen_native sceneのImage Agentは、生成後に担当sceneの文字を目視相当で確認し（指定文言一致・誤字・脱字・余計な文字・文字化け・行順・文字切れ・はみ出し・重なり・コントラスト・縮小時可読性）、結果を親Codexへ返す。親Codexは `scripts/text_qa.py` と併せて文字QAし、NGは1回だけ再生成、2回目NGは生成画像を採用せずrenderer-nativeへ再設計する。
- 7sceneなら最大7agentを候補とし、実行環境の制限があれば3+3+1などのbatchに分ける。依存sceneは並列化しない。

全agent完了後、親Codexがfilename、required scenes、重複hash、破損、scene内容、collage、blank white half、文字QA（imagegen_nativeのみ）、official UIのAI再現を一括確認する。contact sheetは親Codex/Pythonが作り、人間が1回確認する。NG sceneだけを再生成し、承認済みsceneは触らない。原本は保持し、1672×941等はrender時に1920×1080正規化copyを作る。

### AnimationとQA

- 既定は `static`。人物・説明画面の次候補は `very_slow_zoom` / `slow_zoom`。
- horizontal pan / `slow_pan` は意味のある演出と `animation_reason` がある場合だけ使う。
- scene QAはvisual balance、左右の巨大な空白、opaque white 40%以上、主ビジュアル25%未満、partial sharp AI、letterboxをWARN候補として記録する。WARNはFAILではなく、人間のcontact sheet確認へ回す。
- official sceneは全体画面を場所理解、zoom/cropを読ませる用途に使い、公式画面が小さすぎればWARNとする。

## 人間レビューの例

```json
{
  "pronunciation": {"approved_segments": [12, 18]},
  "video": {"draft_auto_v3": "approved"}
}
```

Phase AではREVIEW、WARN、FAIL、MISSINGが一つでも残ればbuildを停止する。Phase 2のvisual WARNは自動再配置をせず、draft reviewの確認候補として扱う。辞書は自動変更しない。

## Human review gate（Episode 005以降の標準）

承認は原則として次の4回程度に整理する。

1. Gate 1: theme / script / sources
2. Gate 2: scene contact sheet ＋ pronunciation REVIEW
3. Gate 3: draft動画を1回最後まで視聴
4. Gate 4: thumbnail / publish

contact sheetは動画生成前に必須。細かい中間承認を追加しない。

## CTA

前Episodeのtopic-specific CTAは無条件に流用しない。特別な理由がなければ `channel_common_cta`（`config/channel_cta.json`、標準ロゴ `local/channel/icon.png`、8〜10秒、static、新規ナレーションなし）を使う。

### CTA・End Screen標準（Episode 007 draft_v3で確定・恒久）
- End Screen背景動画には、チャンネル登録用として誤認されるチャンネルアイコン（ロゴ画像）・疑似登録アイコンを描画しない（draft_v4で確定）。実チャンネル登録要素はYouTube Studio側で配置する。CTA画面にはチャンネル名・説明・CTA本文・軽いブランド装飾のみ。
- 疑似subscribe（丸＋✓）は動画側に描画しない。登録ボタンはYouTube StudioのEnd Screen要素で実配置する。
- 右側40〜45%はEnd Screen reserved領域とし、装飾・ロゴ・本文・疑似アイコンを置かない。「次はこちら」等の案内ラベルは例外的に可（関連動画枠と被らせない・48px以上）。
- CTA文字は縮小で押し込まない。全文を自然な改行（「・」・句点等）で2行以内に配置し、56px以上（標準60px）。収まらない場合は `channel_cta.json` の panel / cta_box / cta_text_box を広げる。
- 装飾（水玉等）は左ブランド枠内・低opacity。表示のみの調整は表示文字列に限定し、canonical_text（ナレーション）は変更しない。hash一致ならCTA音声を再利用。

## finalizeと記録

人間承認済みdraftからfinalへの昇格はcopy-only。再encodeせず、draft/finalのSHA-256、duration、codec、resolution、fps、audio、decode error、black frame、subtitle焼き込み確認を `qc.md` 等へ残す。builderは `work/production_metrics.json` に自動取得できる制作時刻・画像数・REVIEW数・draft版を記録する。Episode 005以降は、可能ならsubagent数、並列task group、Image Agent数、画像生成call数・再生成数・経過秒、人間ゲート数、Phase A/B時間も記録し、未計測値は推測しない。

## 制作時間の目標

- 構成・scene mode判断: 20〜30分
- GPT画像生成・選定: 30〜45分
- 公式素材確認: 20〜30分
- 差分音声・字幕・動画build: 10〜20分
- 人間QA・修正: 30〜45分

段階目標はEpisode 005頃に2時間以内、Episode 010頃に90分前後。Episode 004/005の実測後にPhase 3を判断し、品質75〜80点の維持を時間短縮より優先する。
