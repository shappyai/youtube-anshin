# Episode 009 draft_v2 pipeline notes

確認日: 2026-09-05  
目的: `draft_v1.mp4` を、発音差分だけで `draft_v2.mp4` に再構成する安全な経路を記録する。  
制約: この調査ではcanonicalファイルを編集しない。映像、字幕本文、scene asset、CTA画面は変更しない。

## 1. 結論

次回は、canonical `episode.json` を直接更新する既存driverではなく、隔離stageを使う。

1. `episode.json` を `work/subagents/episode009_phase_b2/<run>/episode_draft_v2.json` へコピーする。
2. canonicalのVOICEVOX segment WAVと `voicevox_segment_state.json` を同じrunへコピーする。
3. 候補JSONでは発音差分だけを変更し、`subtitles`、`scenes`、`postroll`、表示文字列は不変を確認する。
4. `voicevox_incremental.generate_incremental()` を一度だけ呼び、`audio_dir` と `work_dir` はrun配下にする。
5. run側の実測 `audio_timing.json` を使い、字幕本文を変えずtimecodeだけ再計算する。
6. `phase2_video.build_video()` をrun側の音声・ASS・出力へ向け、canonical scene assetは読み取り専用で参照する。
7. vendor FFmpegを明示して `phase2_qa.run_qa()` を実行する。
8. PASS後にだけrun側の `draft_v2.mp4` をEpisodeの `output/draft_v2.mp4` へ新規コピーする。`draft_v1.mp4` は上書きしない。

scene renderer、CTA builder、canonical字幕生成、Episode全体build driverは呼ばない。

## 2. 調査した既存経路と役割

| ファイル / 関数 | 役割 | draft_v2での扱い |
|---|---|---|
| `scripts/voicevox_incremental.py:52` `segment_hash()` | narration、effective text、segment override、active辞書、話者・速度からhashを作る | 発音差分の選別に使う |
| `scripts/voicevox_incremental.py:138` `generate_incremental()` | hash一致WAVをreuseし、不一致だけsynthesis。連結音声とtimingも出力 | runの`audio_dir`/`work_dir`で一度だけ呼ぶ |
| `scripts/tts_voicevox.py:210` `apply_pronunciation_overrides()` | approved辞書をaudio_queryへ適用 | 現行configを読み取り、重複登録しない |
| `scripts/tts_voicevox.py:266` `apply_segment_accent_overrides()` | 1 segmentだけの文脈依存補正 | `方`などに限定して候補JSONで使う |
| `scripts/tts_voicevox.py:295` `apply_pronunciation_pitch_patterns()` | mora_data後のapproved pitch shape適用 | synthesis経路で自動適用 |
| `scripts/build_subtitle_cue_timing.py:47` `build_measurements()` | cueごとのVOICEVOX mora duration測定 | run側で再計測 |
| `scripts/build_subtitle_timeline.py:99` `build_from_files()` | timingからSRT/ASS作成 | 本文不変、run側でtimecodeのみ再生成 |
| `scripts/phase2_video.py:68` `build_video()` | scene、音声、ASS、CTAをFFmpegでdraft化 | read-only scene + run側入力で使用 |
| `scripts/phase2_qa.py:475` `run_qa()` | schema、scene、subtitle、CTA、probe、黒画面、無音を検査 | run側candidate/timing/draftで実行 |
| `work/phase_b_review/run_draft_qa.py` | vendor FFmpegでprobeする既存補助 | v1固定なのでv2へそのまま使わない |

## 3. 現在の入力と対象ID

- narration: 52 segments
- subtitles: 59 cues
- scenes: 19
- v1: `episodes/009_windows11_24h2_support/output/draft_v1.mp4`
- timing: `episodes/009_windows11_24h2_support/work/audio_timing.json`
- state: `episodes/009_windows11_24h2_support/work/voicevox_segment_state.json`
- query audit: `episodes/009_windows11_24h2_support/work/voicevox_query_audit.json`
- scene asset: `episodes/009_windows11_24h2_support/assets/scenes/scene_001.png`〜`scene_019.png`

全文scan:

| 表記 | segment ID | 文脈上の注意 |
|---|---|---|
| `方` | 001, 006, 011, 038 | 001は人を指す「かた」。006の「考え方」は既存の自然な「かた」。011は利用者を指す「かた」。038は「24H2のほう」という対象側の意味で無条件置換しない |
| `Windows` | 001, 002, 004, 005, 008, 009, 014, 020, 022, 023, 025, 037, 039, 047, 049, 050 | `Windows Update`内も含む |
| `Update` | 005, 022, 023, 037, 039, 047, 050 | 7件すべてWindowsと同一segment |
| `ID` | 019 | 表示は`ID`のまま、読みだけ補正 |

現行 `config/voicevox_pronunciation.yaml` には、重複せず使うapproved設定がある。

- `Windows`: reading `ウィンドオズ`, accent 5、語末「ズ」peak
- `Update`: reading `アップデエト`, accent 6、語末「ト」peak
- `ID`: reading `アイディイ`, accent 3、`ディ` peak
- scope: `標準辞書（Episode009 human review）` / provenance: `Episode009 human review` / date: `2026-09-05`

この補助作業ではconfigを編集していない。次回も辞書を追加せず、既存configを読み取る。

## 4. 隔離stageの準備

PythonはプロジェクトSTATEに記録されたものを使い、FFmpegはrepo内vendorを明示する。

```powershell
$ROOT = 'C:\Codex\260829_youtube-anshin'
$EP = Join-Path $ROOT 'episodes\009_windows11_24h2_support'
$PY = 'C:\Users\user\AppData\Local\Programs\Python\Python314\python.exe'
$FFMPEG = Join-Path $ROOT 'work\vendor\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
$STAGE_ROOT = Join-Path $EP 'work\subagents\episode009_phase_b2'
$RUN = Join-Path $STAGE_ROOT ('run_' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
if (Test-Path -LiteralPath $RUN) { throw "run already exists: $RUN" }
New-Item -ItemType Directory -Force -Path (Join-Path $RUN 'work'), (Join-Path $RUN 'audio\voicevox_kenzaki\segments'), (Join-Path $RUN 'output') | Out-Null
Copy-Item -LiteralPath (Join-Path $EP 'episode.json') -Destination (Join-Path $RUN 'episode_draft_v2.json')
Copy-Item -LiteralPath (Join-Path $EP 'work\voicevox_segment_state.json') -Destination (Join-Path $RUN 'work\voicevox_segment_state.json')
Get-ChildItem -LiteralPath (Join-Path $EP 'audio\voicevox_kenzaki\segments') -Filter '*.wav' -File | Copy-Item -Destination (Join-Path $RUN 'audio\voicevox_kenzaki\segments')
Copy-Item -LiteralPath (Join-Path $EP 'work\channel_cta.png') -Destination (Join-Path $RUN 'work\channel_cta.png')
Copy-Item -LiteralPath (Join-Path $EP 'audio\voicevox_kenzaki\cta_channel_common.wav') -Destination (Join-Path $RUN 'audio\voicevox_kenzaki\cta_channel_common.wav')
$canonicalEpisodeHash = (Get-FileHash (Join-Path $EP 'episode.json') -Algorithm SHA256).Hash
```

stateと全segment WAVをrunへコピーすることがcache reuseの前提。candidateのepisode JSONだけを発音差分用に編集し、canonical `episode.json`、config、scene asset、既存captionsは書き換えない。

## 5. candidate JSONの変更範囲

RUN\episode_draft_v2.jsonだけを候補として編集する。変更は発音フィールドに限定する。

- segment 001: reading_overrides["方"] = "かた"
- Windows / Update / ID: 既存approved configを使うため、candidateに重複する辞書や表示文字列を追加しない
- subtitlesのtext_lines、font_px、cue ID、segment_idは不変
- scenes、official_asset、render_mode、animation、scene画像は不変
- postroll、CTA asset、CTA audioは不変

候補生成後、canonicalとcandidateのnarration本文、display_text、subtitles、scenes、postrollを比較し、差分が発音フィールド以外にあれば停止する。

episodes/009_windows11_24h2_support/work/phase_b_review/build_episode009_phase_b.pyは固定されたcanonical episode.jsonを直接writeし、字幕・postroll・statusも更新する。今回の条件では使わない。

## 6. VOICEVOX incremental regeneration

voicevox_incremental.pyにはCLI entry pointがない。generate_incremental()をPythonから直接呼ぶ。

呼び出し引数は次の対応にする。

- data: run側のepisode_draft_v2.jsonをload_json()で読む
- episode_dir: canonical Episode dir（default audio dirの基準以外に書かない）
- work_dir: RUN/work
- engine_url: http://127.0.0.1:50021
- audio_dir: RUN/audio/voicevox_kenzaki

成功時の出力はrun側のvoicevox_segment_state.json、audio_timing.json、voicevox_query_audit.json、narration_kenzaki_auto.wav。

### cache判定

- run側にv1のstateと全segment WAVをコピーしておく。これがreuseの前提。
- segment_hash()はnarration、effective text、reading override、active pronunciation dictionary、話者、speed、intonation、pitchを含む。
- display_textはhashに参加しないため、表示字幕を変えない限り音声cacheを汚さない。
- force_segmentを全対象へループ適用しない。hash差分を一度のgenerate_incremental()で選別する。

実行前にVOICEVOXのversionとspeakers endpointを確認し、話者IDを固定値で決めない。resolve_speaker(engine_url, "剣崎雌雄", "ノーマル")でstyle IDを解決する。speed / intonation / pitchは1.00 / 1.00 / 0.00。

### dry-run

本生成前に同じcandidate、同じcopied state、同じrun audio cacheでdry_run=Trueを実行する。

- plannedが意図した発音差分だけであること
- skippedにそれ以外が入ること
- 予想外のplannedが出たら、辞書scopeまたはstate世代差を確認して停止すること
- 再生成件数を手計算で決め打ちしないこと

今回のscanではWindows 16件、ID 1件がunique対象。Update 7件はすべてWindowsと同一segmentで、方のsegment 001もWindows対象と重なる。正本はdry-runのplanned/skipped。

## 7. audio_timingと字幕

発音変更でWAV尺が変わる可能性があるため、audio_timing.jsonはrun側で必ず再構築する。generate_incremental()がsegmentごとの実測WAV duration、pause_after、start_sec、end_secを計算する。

続けてscripts/build_subtitle_cue_timing.pyをcandidateへ向けて実行し、run側work/subtitle_cue_timing.jsonへ59 cueのVOICEVOX mora durationを出す。

build_subtitle_timeline.build_from_files(data, RUN/work/audio_timing.json, RUN/work/captions.srt, RUN/work/captions.ass, RUN/work/subtitle_cue_timing.json)を呼ぶ。

ここで変えるのはtimecodeだけ。cue ID、text_lines、font_px、segment紐付け、59 cueの本文はcanonicalと一致させる。run側のSRT/ASSを使い、canonical captionsを上書きしない。

生成後はscripts/subtitle_preflight.pyをcandidateへ向け、59 cue、最小72px、overflow 0、3-line 0、tts_reading_leakage 0を確認する。FAILならdraftへ進まない。

## 8. phase2_videoでdraft_v2を組み立てる

phase2_video.build_video()は相対postroll assetの解決にwork_dir.parentを使う。candidateのpostroll.assetがwork/channel_cta.pngのままでも解決できるよう、CTA画面はRUN/work/channel_cta.pngへコピーし、work_dir=RUN/workで呼ぶ。

scene assetはcanonicalの次を読み取り専用で参照する。

episodes/009_windows11_24h2_support/assets/scenes/

phase2_video.pyは各scene PNGを読むだけで、scene画像自体は変更しない。clip、concat、visual中間動画はすべてrun側に出す。

### vendor FFmpeg

system ffmpeg / ffprobeがPATHから見つからない場合があるため、repo内の次を明示する。

C:\Codex\260829_youtube-anshin\work\vendor\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe

build_video呼び出し前にphase2_video._ffmpeg_executableを次のようにpatchする。

    import phase2_video
    phase2_video._ffmpeg_executable = lambda: str(FFMPEG)
    video = phase2_video.build_video(
        data=data,
        final_scene_dir=EP / "assets" / "scenes",
        timing_path=RUN / "work" / "audio_timing.json",
        audio_path=RUN / "audio" / "voicevox_kenzaki" / "narration_kenzaki_auto.wav",
        ass_path=RUN / "work" / "captions.ass",
        work_dir=RUN / "work",
        output_path=RUN / "output" / "draft_v2.mp4",
        cta_audio_path=RUN / "audio" / "voicevox_kenzaki" / "cta_channel_common.wav",
        cta_trailing=3.4373333333,
    )
    assert video["status"] == "PASS", video

output/draft_v2.mp4が既に存在する場合は停止し、draft_v1.mp4は入力として読むだけにする。

## 9. QA runnerの使い方

### 既存helperの注意

work/phase_b_review/run_draft_qa.pyは、EPがcanonical Episode固定、draftがoutput/draft_v1.mp4固定、reportがdraft_v1_qa固定である。そのままv2へ使わない。同helperのvendor probe処理をrun側の一時driverへコピーし、パスだけv2 stageへ置き換える。canonical helper自体は編集しない。

### phase2_qa.run_qa()

phase2_qa._ffmpeg_executableをvendor pathへpatchし、phase2_qa._probeには既存run_draft_qa.pyのvendor ffmpeg probe関数を渡す。引数は次の対応にする。

    qa = phase2_qa.run_qa(
        data=data,
        final_scene_dir=EP / "assets" / "scenes",
        timing_path=RUN / "work" / "audio_timing.json",
        draft_path=RUN / "output" / "draft_v2.mp4",
        report_base=RUN / "work" / "draft_v2_qa",
        audio_path=RUN / "audio" / "voicevox_kenzaki" / "narration_kenzaki_auto.wav",
    )

report_baseをRUN/work/draft_v2_qaにするのが重要。phase2_qaはreport baseの親の親をEpisode dirとしてCTA相対pathを解決するため、RUN/work/phase_b_review/draft_v2_qaに置くとwork/work/channel_cta.pngを探して誤判定する。

期待するQA項目:

- candidate schema: PASS
- scene count: 19
- subtitle count: 59
- video: H.264 / 1920x1080 / 30fps
- audio: AAC / 48000Hz
- decode returncode: 0
- black frame: 0
- unexpected long silence: 0
- CTA asset/audio: PASS
- scene visual warningの増加: 0

発音固有の確認はrun側voicevox_query_audit.jsonを使う。voicevox_pitch_qa.pyは現在のapproved pitch-shape entry向けなので、Windows / Update / IDの最終peakはquery auditのmora列を人間承認設定と照合し、方はexpected_reading()のsegment overrideがかたになっていることを確認する。

## 10. 実行してはいけない経路

- work/phase_b_review/build_episode009_phase_b.py: canonical episode.jsonを直接writeし、字幕・postroll・statusも更新する。
- build_episode.py: scene render、canonical work、audio、subtitle、metricsをまとめて扱うため、発音だけの隔離再構成には広すぎる。
- v1固定のrun_draft_qa.pyをパス変更なしで実行すること。v1を再QAするだけになる。
- render_episode_scenes()、build_cta()をdraft_v2の発音差分作業で呼ぶこと。scene/CTAを再生成する必要はない。
- force_segmentを対象全件へ機械的にループすること。hash判定を壊し、regenerated/reused報告を不正確にする。
- canonical captions.srt / captions.assを上書きすること。run側でtimecodeを作る。

## 11. 最終コピー前の不変条件

QA PASS後、次を確認してからだけ新規draftをコピーする。

    $afterEpisodeHash = (Get-FileHash (Join-Path $EP 'episode.json') -Algorithm SHA256).Hash
    if ($canonicalEpisodeHash -ne $afterEpisodeHash) { throw 'canonical episode.json changed' }
    if (Test-Path -LiteralPath (Join-Path $EP 'output\\draft_v2.mp4')) { throw 'draft_v2 already exists; do not overwrite' }
    $stageDraft = Join-Path $RUN 'output\\draft_v2.mp4'
    if (-not (Test-Path -LiteralPath $stageDraft)) { throw 'stage draft missing' }
    Copy-Item -LiteralPath $stageDraft -Destination (Join-Path $EP 'output\\draft_v2.mp4')

このコピーは将来のdraft_v2作成時だけ実行する。今回の補助作業では実行していない。

## 12. まとめ

安全なcanonical単一writer経路:

candidate episode（発音だけ） → copied state/WAV cache → generate_incremental(one call) → run audio_timing → run subtitle timecode only → phase2_video(vendor FFmpeg、read-only scenes) → phase2_qa(vendor probe、run report) → PASS後にdraft_v2新規copy

映像、字幕本文、scene asset、CTA画面を変更する処理はこの経路に含めない。発音差分の実際の再生成件数は、current configとcopied stateを用いたdry-runのplanned / skippedを正本とする。
