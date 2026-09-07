# Shorts制作ライン

## Episodeとの切り分け

ShortsはEpisodeとは別の企画・制作ラインとして管理する。ShortsのIDは Short001、Short002 のように採番し、将来Episodeへ展開しても番号は引き継がない。

現在のバッチ001はVisual Redesign Draft v5完成（Draft v4はHuman Draft Gateで約50/100のREJECT）、Short001〜003の人間Draft Gate待ち。公開状態はすべてNOT_UPLOADED。

各Shortの正本は、次のディレクトリに置く。

- shorts/001_chatgpt_voice_input/
- shorts/002_ai_suspicious_message/
- shorts/003_mynumber_smartphone/

## 共通仕様

- 画面比率：縦 1080×1920
- フレームレート：30fps
- 目標尺：27〜31秒、最大35秒
- 構成：冒頭（問い）→行動（生活場面）→結論の3 core scenes。各Shortは6〜8 visual beats、変更間隔の目標は2〜4秒。ナレーション1文ごとに説明sceneを増やさない
- 1本1問。タイトルと冒頭の問いを一致させる
- 字幕は原則2行以内。Shortsでは64px以上を最低目安、標準80pxを目標にする
- 字幕帯は下部のShorts UIと重ならない位置に固定する
- narration と表示字幕は分離する。読み仮名・VOICEVOX用の読みは表示字幕へ流出させない
- 設定画面は実機または公式画面を使い、架空UIを本物として見せない
- 個人情報・テストアカウントの情報を素材へ入れない
- CTA専用sceneは作らず、最後の結論Visualへ最後約2〜3秒のCTA字幕を重ねる。承認済み実チャンネルアイコン＋チャンネル名だけを添え、登録UIは描画しない
- 冒頭の1フレームから人物または生活状況と問いを見せる。fade in・チャンネル名・制作IDは置かない
- ImageGen-nativeは人物・背景・主役物・短い見出しが一枚で成立する完成画を優先する。大見出しの後乗せは禁止
- rendererは例外扱いとし、Shortsのつなぎやナレーション1文ごとの説明には使わない
- 今回は動画冒頭からサムネイル候補だけを生成し、サムネイル確定は行わない
- ナレーターはEpisode共通のVOICEVOX「剣崎雌雄」ノーマルを使う。ただしPhase Aでは音声生成を行わない

## Visual Redesign v5で適用したShortsルール

- `shorts_micro_motion_for_motion_sake`：`FORBIDDEN`。意味のないzoom、pan、105→110%の微細motionは使わない。
- visual stateの変更は、new asset、real/official UI、意味のあるcrop、privacy mask state、person→screen、before→afterなどのhard cutに限定する。beat数をKPIにしない。
- 静止画は2〜5秒を基本にし、50〜70代の読みやすさを優先する。字幕はtarget80px / min64px / 最大2行。
- CTAは専用slideなし。最後の結論Visualの最後3秒だけ、実チャンネルアイコン約180px＋チャンネル名を中央表示する。疑似subscribe UIは描画しない。
- Short001は現行ChatGPT実画面＋公式Voice参照画面を使い、ライブVoice captureは`CAPTURE_REQUIRED`のまま。Short002はprivacy maskの状態変化を静止表示する。
- Short003はデジタル庁公式マイナポータル画面→コンビニ証明書→e-Tax生活scene→医療利用→端末差→実物カードの具体的な順序にする。抽象usage rendererは使用しない。

## Phase A / Phase B

Phase Aで作成するものは、市場確認、一次情報の事実整理、台本、ナレーション区切り、映像設計までとする。各Shortの work/market_check.md、facts.md、sources.md、script.md、visual_plan.md が該当する。

人間のScript Gateで台本が承認されるまで、VOICEVOX、ImageGen、実機収録、動画書き出し、アップロード、公開は開始しない。承認後にPhase Bとして、実機画面の再確認、音声QA、字幕タイミング、素材QA、縦動画の書き出しを行う。

## 検証と公開

probe_metric は公開後に同条件で比較するための仮説指標であり、合格基準を先に断定しない。公開状態はPhase Aでは NOT_UPLOADED とする。

Fact Gateで REVIEW が残る場合は、人間が該当箇所を承認または修正してからScript Gateを通す。AIが詐欺を確定判定する、スマホだけで全てできる、どの利用者でも同じ画面が出る、といった過度な断定はしない。

## Visual Redesign v3で適用したShortsルール候補

- `visual_density_over_slide_count`：major visualは標準3〜4枚
- `shorts_no_narration_per_slide`：ナレーション1文ごとの説明スライド化をしない
- `shorts_no_dedicated_cta_slide`：専用CTA sceneを作らない
- `shorts_first_frame_hook_required`：最初の1フレームからhook visualを表示
- 人物・生活状況Visualを優先し、説明はナレーションと字幕へ置く
- rendererは例外。viewer-facing Short IDは常に0

## Visual Redesign v4で適用したShortsルール

- `shorts_core_scene_count`：3前後（冒頭 / 行動 / 結論）
- `shorts_visual_beats`：6〜8。今回は3本とも8 beats
- `static_hold_over_5sec`：原則WARN。今回の3本はShort001/003が1、Short002が0
- `static_hold_over_7sec`：FAIL。今回の3本とも0
- `visual_change_interval`：target 2〜4秒。beat内はslow crop / close cropで変化を保つ
- `shorts_slideshow_feel`：1/5 REVIEW、`shorts_native_feel`：4/5 REVIEW
- Short001は現行chatgpt.comの実画面＋公式Voice参照画面を使用。ライブVoiceセッションは`CAPTURE_REQUIRED`で、人間Draft Gateまで偽UIを追加しない
- Short002は拒否済みの人物privacy画を廃止し、該当欄だけ■■■■で隠すgeneric document rendererへ置換
- Short003の利用先は大きな3カードにせず、短いrenderer cueへ置換
- 共通CTAのspoken canonical：`次に困ったときのために、このチャンネルを登録しておいてください。`
- 変更audioは対象segmentだけ。ChatGPTの`ト`はglobal human-approved辞書へaccent=3で登録
