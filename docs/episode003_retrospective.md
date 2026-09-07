# Episode 003 制作振り返りとPhase 2標準

作成日: 2026-08-31  
対象: `episodes/003_line_renewal/`  
目的: Episode 004以降で、Episode 003と同じ試行錯誤を繰り返さない。

## 1. retrospectiveの位置づけ

この文書は、Episode 003の実制作・人間レビュー・差分修正・finalizeで確認したルールを、今後のdocs、templates、schema、renderer、QA、production workflowへ戻すための記録である。Episode 001/002/003の完成動画は変更しない。

## 2. Episode 003の実績

- content scenes: 18
- narration: 52 segment
- subtitles: 52 cue
- gpt_image: 8
- official: 7
- template: 3
- 実機撮影: 不要
- final duration: 300.833秒（約300.8秒）
- final: human approved
- finalize: copy-only
- `draft_auto_v3.mp4` と `final.mp4` のSHA-256: `AF4323F3364832CDE784EDE9F717A0D26AD45E1F285182D8F807C51DCEAE4788`

Phase 2ハイブリッド方式が、1本の完成動画を人間承認・copy-only finalizeまで通過した実績として扱う。

## 3. ハイブリッド方式は継続

全部template、全部GPT imageのどちらかに固定しない。

- template: 箇条書き、3ステップ、チェックリスト、簡単なまとめ、正確な文字主体
- official: アプリUI、Web画面、公式FAQ、ストア、設定画面、正確な事実を見せる場面
- gpt_image: 冒頭、概念説明、安心感、比喩、人物、章の切り替え、感情的な理解の補助

sceneごとに「正確さを読ませるか、意味を感じてもらうか」を先に決める。

## 4. GPT画像で起きた二重レイアウト

旧方式ではGPT画像側に文字用の左半分を空け、さらにCodex側で大きな文字カードを追加した。その結果、主役が端へ寄り、白い空間が巨大になり、AI画像が細い飾りに見え、PowerPoint的な見え方になった。

今後はGPT画像の構図とCodexレイアウトを二重に設計しない。

## 5. GPT画像はfull-frame完成背景

GPT画像そのものを1920×1080の画面全体として成立させる。manifest共通promptには、full-frame、edge-to-edge background、no blank half、no large empty white area、no presentation card layout、no collage、no storyboard、no contact sheet、no split screen unless explicitly requiredを含める。

文字を置く領域は真っ白なキャンバスではなく、端まで続く静かな背景とする。

## 6. 1scene = 1image

画像生成manifestは、1回の生成依頼につき1sceneだけを要求する。8sceneまとめ、storyboard、contact sheet、collage、4×2 grid、multiple panelsは作らない。出力契約はmanifestの`prompt_contract=one_scene_full_frame_v1`と`asset_contract.one_scene_per_image=true`に記録する。

## 7. generated AI assetの条件

原則は、1920×1080、PNG、16:9、full-frame、1sceneのみ、下部180pxの字幕安全領域を意識、公式UIをAI生成しない、ロゴやサービス画面を偽造しない、小さい文字を生成しない、である。日本語の入れ方は docs/text_render_policy.md の恒久ルールに従い、短い見出しが主役のsection扉・concept title sceneは imagegen_native（背景＋短い日本語文字の一体生成）を第一候補とし、一覧・比較・手順・数字・長文・公式仕様・注意・表・CTA・official screenshot上の補足はCodex renderer（pil_overlay）で正確に後描画する（2026-09-03のEpisode 007 A/B実績で確定。詳細は docs/text_render_policy.md セクション10）。

## 8. gpt_image rendererの意味

`render_mode=gpt_image`は、human review済みの完成背景画像を使用するという意味であり、Codexが再デザインする指示ではない。標準処理は次のとおり。

```text
GPT image → full bleed → 必要な日本語text overlay → subtitle
```

## 9. text_render_mode=codex

`text_render_mode=codex`は、episode.jsonで指定した文字だけをCodexが追加する意味である。大型白カード、AI画像の縮小、新しいレイアウト、画面半分の白塗り、AI画像のtemplate card化は禁止する。必要な場合も、文字周囲のshadow、outline、小さな半透明scrimに限定する。

注記（2026-09-03）: Episode 007以降はこの方式は `text_render_mode=pil_overlay` の後方互換別名として扱う。`codex` / `image` は従来Episode用の別名で、新規sceneの標準は画像の文字レンダリング方針 `docs/text_render_policy.md`（`imagegen_native` 既定）に従う。

## 10. GPT画像のfit priority

1. exact 1920×1080: `full_bleed`
2. 軽微なaspect ratio差: `crop`
3. 最終手段: `cover_blur`

`cover_blur`はschema・config・rendererで明示指定した場合だけ使うfallbackであり、defaultにはしない。

## 11. 視覚的重心QA

SCENE-015では、右側をgradientで埋めても主役・情報全体が左側に偏って見えた。背景が埋まっていることだけでPASSにしない。

sceneの`visual_balance_center_x`または`visual_balance.center_x`を任意指定でき、rendererが既知のレイアウトは保守的な推定値を使う。画面中心x=960に対し、x=650未満またはx=1270超をWARN候補とする。誤検出の可能性があるためFAILにはしない。

## 12. 余白QA

左右どちらかの巨大な空白、opaque white area 40%以上、main visual占有率25%未満、sharp GPT imageが画面の一部にしか表示されない状態、letterboxをWARN候補にする。ただし意図したminimal designは人間が許可できる。自動WARNは再配置の命令ではなく、contact sheetで確認する候補である。

## 13. Animationの標準

人物・説明用静止画は`static`を第一候補、動きを足す場合は`very_slow_zoom`または`slow_zoom`を第二候補とする。horizontal pan / `slow_pan`はdefaultでは使わない。横長画像を順番に見せるなど、意味のある演出の場合だけ`animation_reason`を記録して使う。

## 14. official scene

公式UIは今後もAI生成しない。公式画像を使用する。全体画面は場所を理解させるため、zoom/cropは内容を読ませるため、というEpisode 001〜003の原則を維持する。公式スクリーンショットが小さすぎる場合はWARNとし、contact sheetと元画像で人間が読む。

## 15. pronunciation：文脈依存語

`方`や`今`はグローバル辞書へ登録しない。`方`は「驚いた方」「考え方」「探し方」では`かた`、「一方で」では`いっぽうで`のように文脈で変わる。Episode 003の「今ブラウン」はsegment overrideで`いまブラウン`とし、単独の「今」は登録しない。

## 16. 人間承認済みVOICEVOX辞書

Episode 003で次を正式追加済み。

- 表記: `App Store`
- 読み: `アップストア`
- アクセント句: 1句
- モーラ: 6
- accent: 5
- ピッチ: 「ト」の後で下降

`config/voicevox_pronunciation.yaml`に1件だけ登録し、重複登録しない。今後はこの項目を自動PASS対象とする。

## 17. pronunciation workflow

標準順序は、`/audio_query`、承認済み辞書との比較、suspiciousな候補だけREVIEW、人間承認、必要segmentだけoverride、差分VOICEVOX生成、である。AIの推測だけでglobal dictionaryへ新規登録しない。

## 18. VOICEVOX差分生成

Episode 003では52segmentのうち、最終修正で必要なsegmentだけを再生成し、ほぼ全てをcache再利用できた。今後も台本全体を毎回再生成せず、音声query・辞書・segment内容のhashが変わったものだけを作り直す。

## 19. 字幕

52 narrationと52 subtitleで成立した。自然な意味単位なら1 narration = 1 subtitleでよく、細かく分割することを目的にしない。文字数だけの再分割、1文字cue、助詞だけのcue、動詞活用の分断、固有名詞の分断は禁止する。タイムコードは音声実測から作る。

## 20. CTAの重要な学び

Episode 003初期にはEpisode 002固有の「慌てて消す前に、まず確認する」を流用し、テーマに合わなかった。前Episode固有CTAを無条件に流用しない。

## 21. チャンネル共通CTA

Episode 003 v3で人間承認された共通CTAを標準候補とする。ロゴは`local/channel/icon.png`、文言は次のとおり。

- `やさしく・安全に・安心して`
- `大人のデジタル安心室`
- `スマホやパソコンを、もっと安全・快適に使うための情報をお届けします`
- `チャンネル登録・高評価もよろしくお願いします`
- `怖がらせる前に、確認する。`

表示は約8〜10秒、原則static、新しいナレーションなしとする。

## 22. CTA template化

共通CTAは`channel_common_cta`プロファイルとして`config/channel_cta.json`と`templates/channel_cta/`で管理する。layout、logo path、text、durationを設定可能にし、Episode003の`cta_v3.png`へ直接依存しない。通常は`postroll.cta_profile=channel_common_cta`を利用する。

## 23. CTAのロゴ

標準ロゴは`local/channel/icon.png`。ロゴ更新時にepisode固有コードを直す必要がないよう、CTA configから参照する。新しいロゴを勝手にデザインしない。

## 24. Human review gate

承認工程は次の5つに固定し、これ以上細かく増やさない。

1. Gate 1: script / sources
2. Gate 2: pronunciation REVIEWのみ
3. Gate 3: scene contact sheet
4. Gate 4: draft動画を1回最後まで視聴
5. Gate 5: finalize

## 25. contact sheet

contact sheetは動画生成前に必須とする。scene構成、余白、公式画像サイズ、AI/template混在、視覚的重心を音声生成・動画生成前に確認できる。最終判断は人間が行う。

## 26. draft versioning

承認前draftは`draft_auto_v1.mp4`、`draft_auto_v2.mp4`、`draft_auto_v3.mp4`のように保存し、上書きしない。Episode 003で比較が容易だったため、同じ版管理を標準化する。

## 27. 修正は局所差分

人間が指摘したscene、segment、CTAだけを修正する。1箇所の修正で全scene、全VOICEVOX、全字幕、全rendererを作り直さない。`--rerender-scene`、`--regen-segment`、新しい`--output-name`を優先する。

## 28. finalize

人間承認済みdraftが1つだけ存在する場合、finalizeはcopy-onlyとする。再encode、音声再生成、字幕再分割、scene再配置を行わず、draftとfinalのSHA-256一致を確認する。既存finalがある場合は上書き拒否する。

## 29. Final QA

final QAではSHA-256、duration、codec、resolution、fps、audio、decode error、black frame、subtitle焼き込み確認を記録する。`scripts/final_qa.py`はこの記録を機械化し、subtitle焼き込みの最終目視だけは人間に残す。

## 30. Episode 004以降の理想フロー

```text
topic research
↓
sources
↓
episode.json
↓
subtitle finalization
↓
scene mode advisor
↓
official assets
↓
GPT manifest
↓
pronunciation preflight
↓
GPT images
↓
scene contact sheet
↓
human visual review
↓
build --continue
↓
draft_auto_v1
↓
human full-video review
↓
必要箇所だけ差分修正
↓
approved draft
↓
copy-only finalize
↓
thumbnail
↓
YouTube
```

## 31. 目標Human intervention

人間が積極的に見る工程は、テーマ・台本、pronunciation REVIEW、contact sheet、draft、thumbnailを原則とする。一次情報・実機素材・公開範囲など、正確性とプライバシーに関わる最終判断は引き続き人間が行う。

## 32. 今後の改善タイミング

Episode 004制作前に大規模な新自動化は行わない。まず現在のPhase 2方式でEpisode 004とEpisode 005を制作し、制作時間、修正回数、GPT画像枚数、人間レビュー回数を比較してPhase 3を判断する。

## 33. production metrics

Episode 004以降は`work/production_metrics.json`またはepisodeのSTATEへ、start time、Phase A完了、GPT image count、pronunciation REVIEW count、draft v1完成、human correction count、final version number、finalize time、total制作時間を記録する。Episode 005以降は必要に応じてsubagent数、並列task group、Image Agent数、画像生成call数・再生成数・経過秒、人間ゲート数、Phase A/B時間も追加する。builderは自動記録できる項目を追記し、人間修正回数などは手動で補う。未記録の値は推測で埋めない。

## 34. Thumbnail

thumbnailは本編scene pipelineと分離する。本編GPT画像のfull-frameルールをそのままthumbnailへ強制しないが、大きな文字、スマホ縮小でも読める1つの疑問、1つの主役、高コントラスト、50〜70代に分かりやすい構成を維持する。公式UIを使う場合、架空UIを事実画面として見せない。

## 35. 更新対象

今回、docs、templates、schemaのdefault、renderer、QA、production workflowを更新した。主な更新先は`docs/phase2_hybrid_production.md`、`docs/build_episode_plan.md`、`AGENTS.md`、`templates/episode.schema.json`、`templates/episode.example.json`、`templates/scenes/README.md`、`config/channel.yaml`、`config/channel_cta.json`、`templates/channel_cta/`、GPT manifest、pronunciation docs、STATE templateである。

## 36. 完成済みEpisodeは変更禁止

Episode 001 final、Episode 002 final、Episode 003 finalは変更しない。Episode003の`final.mp4`はhuman approved済みであり、再encode・再finalizeしない。今回の恒久化作業は制作基盤と文書だけに限定する。

## 37. 最終状態

Episode003の知見をPhase 2標準制作フローへ反映する準備が完了した。Episode004のテーマ選定・台本作成はこの作業では開始しない。

## 38. Episode 004の記録（2026-08-31・画像生成自動化の残課題）

Episode 004ではGPT画像7枚を人間が1枚ずつ手動生成した。以下をPhase 3改善の材料として記録する。

- 1ファイルに複数sceneのpromptをまとめるとcollage化が発生しやすい。scene単独promptなら成功する。
- 人間の生成操作が7回必要で、制作効率の面ではNGだった。2026-08-31の画像生成PoCで、1回の依頼からscene単独の生成、自動保存、重複確認、contact sheet作成までを確認した。PoC自体はA→B→Cの逐次実行だったが、これは検証上の順序であり、Episode 005以降は依存関係のないsceneを「1 Image Agent = 1 scene = 1 image = 1 unique output path」で並列委譲する方針へ更新する。
- 今回のフェーズでは上記の自動化は実装しない（Episode 004完成を優先）。
- 補足: 人間生成画像の解像度は1672x941（16:9）だった。原本は変更せず、検証・レンダリング用にLANCZOS拡大の1920x1080正規化コピーを`episodes/004_nise_keisatsu/work/phase_b_review/normalized_ai/`へ置いた。再出力による差し替えはいつでも可能。
