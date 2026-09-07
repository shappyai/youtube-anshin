# build_episode.py 設計メモ

## 目的

Episode 004以降は、企画・台本・字幕の人間確認が終わった episode.json を正本にして、再現できる工程を一つのコマンドへまとめる。Episode 003の実績と恒久ルールは `docs/episode003_retrospective.md` に記録する。

~~~powershell
python build_episode.py 003
~~~

Phase 2では、episode.jsonの検証、scene mode、GPT画像manifest、VOICEVOX差分生成、音声実測字幕、scene動画化、contact sheet、draft QA、copy-only finalizeまでを接続済みである。Episode 001〜003の完成動画はこのコマンドから上書きしない。

## 標準の処理順

1. topic research → sources → scriptを人間が確定する。
2. episode.jsonとsubtitleを確定し、schema、sources、scene mode、official assetsをpreflightする。
3. GPT画像manifestを作り、1scene=1枚の1920×1080 PNGを配置する。Episode 005以降は親Codexがsceneごとのassignmentへ分割し、依存関係のないsceneを1agent=1scene=1imageとして可能なら並列委譲する。
4. pronunciation preflightで疑わしい語だけREVIEWにし、人間承認後にsegment単位で確定する。
5. 親Codexが全GPT画像のcontact sheetを動画生成前に作り、人間がscene構成、余白、公式画面、視覚的重心を1回確認する。NG sceneだけを専用agentで再生成する。
6. `--continue`でscene、cache差分音声、実測タイムライン、52cue等の字幕、draft、QAを生成する。
7. draftを最後まで人間視聴し、必要箇所だけ`--rerender-scene`、`--regen-segment`、新しい`--output-name`で修正する。
8. 承認済みdraftを`--finalize`で再encodeせずfinalへcopyし、SHA-256等のFinal QAを記録する。
9. thumbnailとYouTube操作は本編buildの外で行う。

~~~text
episode.json
   │
   ├─ validation ── FAIL → stop
   ├─ pronunciation preflight ── REVIEW/FAIL → stop
   ├─ scene mode + scene render + official asset check ── FAIL → stop
   ├─ subtitle preflight ── FAIL → stop
   ├─ VOICEVOX per-segment WAV
   ├─ measured timeline
   ├─ captions / ffmpeg
   └─ contact sheet + QA → draft_auto_vN → human approval → copy-only final
~~~

## 停止条件と出力

- FAIL: 不正なJSON、欠落した公式素材、固有名詞の途中分割、安全幅超過など。終了コード1。
- REVIEW: VOICEVOXの読み、未確認の文脈依存語、または人間確認が必要な項目。終了コード2。
- PASS: 自動検査を通過。人間の画面・音声・公開前確認は残す。

preflightはレポートだけを更新し、config/voicevox_pronunciation.yaml を自動変更しない。辞書への登録は人間の試聴・承認後に別作業として行う。

## 人間に残す工程

- 企画・一次情報・台本の最終確定
- 実機画面、通知、生体認証、SMSなど再現性が必要な素材の録画
- VOICEVOXの REVIEW 候補の試聴と辞書登録判断
- contact sheetと完成候補の目視確認
- 個人情報・規約・公開範囲の最終確認

## Phase 2で実装済みの項目

1. build_episode.py のCLIと安全な出力ディレクトリ管理。
2. episode.json からのVOICEVOX segment生成・部分再生成・concat-only。
3. 実測WAVサンプル数に基づく字幕タイムコード生成。
4. 公式素材のslot/crop配置をlayoutごとに厳密化。
5. ffmpegのdraft生成と、既存QAのfact/language/visual/audio/privacy分類への接続。
6. dry-run、scene-only、tts-only、from-segment の再開オプション。
7. Episode 003を人間承認のもとで通し、ハイブリッド方式、差分生成、CTA、視覚QAの知見を記録した。

Episode 001/002の完成動画・実機素材・既存draftは、この設計コマンドから上書きしない。初回3本は「企画最終決定・実機録画・公開前確認」を人間が行う方針を維持する。

## GPT画像・Phase 2描画標準（2026-08-31）

- GPT画像は、人間が確認した1920×1080の完成背景を原則 `fit_mode=full_bleed` でそのまま画面全体に配置する。
- 文字の入れ方は `text_render_mode` で管理し、Episode 007以降の新規sceneは `imagegen_native`（ImageGenで背景と文字を同時生成）を既定とする。`pil_overlay`（旧 `codex` 相当）ではepisode.jsonで指定された日本語headline / support textだけを正確に後描画する。`no_text` は画像内に文字を入れない。公式引用・手順・URL・数字・PIN・長文は `pil_overlay` にし、ImageGen文字へ置き換えない。詳細は `docs/text_render_policy.md`。
- imagegen_native は生成後に文字QA（ `scripts/text_qa.py` ＋目視）を行い、PASSなら採用、FAILは1回だけ再生成、2回目FAILは生成画像を採用せずrenderer-nativeへ再設計する。生成画像＋大きな後乗せ文字のhybridは `NO_IMAGE_TEXT_HYBRID` により禁止する。
- 大きな白カードや別レイアウトの追加、LINE公式UIの生成は行わない。
- 文字が背景に埋もれる場合のscrim・影・outlineは文字の周囲に限定する。画面の左右に意図しない白い余白を追加しない。
- `cover_blur` は既定値にせず、アスペクト比不一致など明示的に必要な場合だけ使うfallbackとする。
- AI画像の下部180pxは字幕安全領域として扱い、Codexの文字レイヤーもImageGen生成文字も字幕帯と重ねない。
- 人物・説明用静止画の意味のない左右panは避け、原則 `static` または `very slow zoom` とする。
- 人間承認済み発音は、`App Store` → `アップストア`、1アクセント句、アクセント位置5（ア・ッ・プ・ス・ト・ア、トの後で下降）を標準辞書に登録する。
- `今ブラウン` → `いまブラウン` はsegment単位overrideのみとし、単独の「今」や文脈依存語「方」は共通辞書へ登録しない。
- `contextual_pronunciation_audio_gate` は恒久的な回帰ゲートとする。辞書のreading登録だけではPASSにせず、疑問文、助詞・助動詞が続く語、語尾が母音の語、引き伸ばされやすい語、ピッチ変更語について、実際の文全体をVOICEVOXへ`audio_query`し、モーラ数・余計な母音・フレーズ境界・疑問文フラグ・アクセント・母音長を確認する。`scripts/voicevox_preflight.py`が辞書確認とは別に実行し、失敗時はPhase Aを停止する。
- `human_audio_override` は文脈依存発音の人間修正版を扱う恒久的な上書き機構とする。`episode.json`の`human_audio_overrides`に承認済みWAV、SHA-256、対象narrationのSHA-256を記録し、保存先は`audio/human_approved/`とする。優先順位は`human_audio_override > pronunciation dictionary > automatic VOICEVOX generation`。overrideは音声再生成・cleanupの対象外とし、timelineは必ず記録済みWAVをreuseする。

## CTA・Human gate・計測標準（2026-08-31）

- 前Episode固有CTAは無条件に流用しない。通常は `channel_common_cta`（`config/channel_cta.json`）を `postroll` に指定する。標準は8〜10秒、static、新規ナレーションなし。
- Human gateは、原則としてテーマ・台本、scene contact sheet＋pronunciation REVIEW、draft全文視聴、thumbnail / publishの4回程度に整理する。重大な事実・発音・公式画面・プライバシーの問題は途中でSTOPする。
- `work/production_metrics.json`にstart time、Phase A完了、GPT画像数、pronunciation REVIEW数、draft版、human correction count、final version、finalize time、total制作時間を記録する。Episode 005以降は必要に応じて`subagent_count`、`parallel_task_groups`、`image_generation_agents`、`image_generation_parallel_batches`、`image_generation_calls`、`image_regeneration_calls`、`image_generation_elapsed_seconds`、`human_gate_count`、`human_correction_rounds`、`phase_a_minutes`、`phase_b_minutes`、`finalization_minutes`も記録し、未計測値は推測しない。
- 既存のdraft名を指定したbuildは停止し、`draft_auto_vN`の新しい名前を要求する。承認前draftとfinalは上書きしない。
- thumbnailは本編scene pipelineから分離する。
- Episode004/005を現在のPhase2で制作してから、実測メトリクスに基づいてPhase3を判断する。Episode004前に大規模な新自動化は行わない。
