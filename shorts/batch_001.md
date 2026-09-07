# Shorts探索バッチ001

- 確認日：2026-09-07（JST）
- 対象：Short001〜Short003
- Phase：B Visual Redesign Draft v5 完了、Draft Gate待ち（Draft v4は約50/100でREJECT）
- ステータス：DRAFT_V5_GATE_PENDING
- 生成済み：v4音声再利用、v2 ImageGen-native画像再利用、Short003の具体的な新規生活scene 2枚、静止＋hard cut縦フレーム、Draft v5、コンタクトシート、サムネイル候補
- 生成していないもの：final、サムネイル確定、アップロード、予約公開

## バッチの狙い

Episodeとは別ラインで、短時間に問いを一つ解決する3本を探索する。Shortsから長尺へ展開できるテーマを、再生数だけでなく、一次情報の強さ、実機収録の負担、誤解の起きにくさで比較する。

共通の仮説指標は、3秒視聴率、平均視聴時間、完視聴率、保存・共有・コメントの質とする。具体的なしきい値は、公開後の同条件比較で決める。

## 3本の比較

| ID | 仮タイトル | 1本の問い | 需要・競合の観測 | 差別化 | Fact Gate | 長尺候補 |
|---|---|---|---|---|---|---|
| Short001 | ChatGPT、文字を打たなくていいんです | ChatGPTに話しかけて使える？ | 音声入力・音声モードの解説は存在するが、確認できた代表例は古い長尺中心。現行UIの差し替えリスクがある | 生活の一言を実際に話す。音声モードと音声入力を混同しない | REVIEW（現行UI・プラン差を収録前に確認） | 音声モードと音声入力を、実機・プライバシー設定付きで比較 |
| Short002 | 怪しいメール、AIに見せて大丈夫？ | 怪しいメールをAIへ相談するとき、何を先にする？ | フィッシング全般は大きな需要が見える一方、AI相談に絞ったShortsの確かな競合指標は今回の公開検索では取れなかった | AIを判定役にせず、個人情報を隠す→公式アプリ・公式サイトで確認の順にする | REVIEW（AIの位置づけを補助に限定） | 怪しいメールをAIに相談する安全な手順と、公式確認・相談先 |
| Short003 | マイナンバーカード、スマホに入れると何ができる？ | スマホのマイナンバーカードで何ができる？ | デジタル庁の公式動画・スマホ登録解説は強く、公式30秒動画は2026-01-22公開時点で約2,381万再生。便利さだけでは差別化しにくい | できることと同時に、iPhone/Android差・実物カードが必要な場面を短く示す | REVIEW（対応場所・OS差を収録前に確認） | iPhone/Android別の追加・削除・使える場所・実物カードの役割 |

## 最初のScript Gate候補

### 1. Short002を先に確認する

安全上の優先度が高い。AIを「詐欺判定機」と表現しないこと、個人情報を隠すこと、メール内リンクを開かず公式アプリまたはブックマークから確認することを、人間が一文ずつ確認する。実在メールの画面は使わず、抽象図解で始める。

### 2. Short001を確認する

現行のChatGPTアプリで音声アイコンの位置、音声モードとマイクによる音声入力の違い、プラン・アカウント・アプリ版による差を確認する。Phase Bでは個人情報のない生活例だけを実機で収録する。

### 3. Short003を確認する

「スマホだけで全てできる」と誤解されないかを確認する。iPhoneとAndroidの差を一つのShortに詰め込みすぎないか、使用例を3つに絞れるか、実物カードが必要な場面を最後まで読める大きさで表示できるかを確認する。

## Phase A完了記録

- 各Shortに市場確認、事実表、一次情報URL、台本、ナレーション区切り、映像設計がある
- short.json に探索仮説・指標・長尺候補・公開状態がある
- Fact Gateの重大な FAIL はなく、人間Script Gateで圧縮修正を承認した
- Phase Bで音声・縦フレーム・字幕・Draft v1を生成済み。Visual RedesignでImageGen-native画像を追加し、Draft v2を生成した。最終聴取とDraft Gateは未完了

## Draft v1実績

| ID | 実測尺 | scene数 | Fact FAIL | pronunciation | real UI数 | visual QA | Draft |
|---|---:|---:|---:|---|---:|---|---|
| Short001 | 27.70秒 | 6 | 0 | REVIEW（人間聴取待ち） | 1 | REVIEW（ログアウト画面にVoiceアイコンなし） | shorts/001_chatgpt_voice_input/output/draft_v1.mp4 |
| Short002 | 30.98秒 | 6 | 0 | REVIEW（人間聴取待ち） | 0 | PASS | shorts/002_ai_suspicious_message/output/draft_v1.mp4 |
| Short003 | 27.39秒 | 6 | 0 | REVIEW（人間聴取待ち） | 0 | PASS | shorts/003_mynumber_smartphone/output/draft_v1.mp4 |

共通CTAは3本とも同じ文面を1回使用し、音声WAVのSHA-256も一致した（A753E45DBCD6D1DCFE5C03360659EE34CB473F2249DF208BC53051C6BFBB4322）。字幕overflow 0、Shorts UI overlap 0、privacy_fail 0、unexpected_silence 0。Short001のVoice操作画面だけは、ログインを伴うため人間が確認してから置き換える。

Draft v1完成後は、final、thumbnail、upload、schedule、publishへ進まない。

## Visual Redesign Draft v2実績

| ID | 実測尺 | scene数 | ImageGen-native | real UI | first 3sec | visual QA | Draft v2 | thumbnail候補 |
|---|---:|---:|---:|---:|---|---|---|---|
| Short001 | 27.70秒 | 6 | 3 | 0 | 4/5 target | PASS_WITH_HUMAN_DRAFT_GATE | shorts/001_chatgpt_voice_input/output/draft_v2.mp4 | shorts/001_chatgpt_voice_input/assets/thumbnail_candidate/first_frame_thumbnail_candidate.png |
| Short002 | 30.98秒 | 6 | 3 | 0 | 4/5 target | PASS_WITH_HUMAN_DRAFT_GATE | shorts/002_ai_suspicious_message/output/draft_v2.mp4 | shorts/002_ai_suspicious_message/assets/thumbnail_candidate/first_frame_thumbnail_candidate.png |
| Short003 | 27.34秒 | 6 | 3 | 0 | 4/5 target | PASS_WITH_HUMAN_DRAFT_GATE | shorts/003_mynumber_smartphone/output/draft_v2.mp4 | shorts/003_mynumber_smartphone/assets/thumbnail_candidate/first_frame_thumbnail_candidate.png |

ImageGen-nativeの指定文言は3本とも3/3 PASS、再生成0、rendererでの大見出し後乗せ0。viewer-facing Short ID 0、fake UI 0、official UI AI再現0、privacy_fail 0、Shorts UI overlap 0、subtitle overflow 0、unexpected silence 0。Short001のVoice実UIは未取得のため、v2はsemantic visualへ切り替えた。

Draft v2完成後は、final、thumbnail確定、upload、schedule、publishへ進まない。

Shorts探索バッチ001 Visual Redesign完了。3本ともImageGen-native冒頭へ変更しdraft_v2生成。人間Draft Gate待ち。

## Visual Redesign Draft v3実績

Draft v2のHuman Draft Gate REJECT（ImageGen → 説明スライド → ImageGen → 説明スライドで、縦型の説明資料に見える）を受け、3本とも冒頭・行動・結論の3枚ストーリーへ変更した。説明用renderer sceneとCTA専用sceneは作らず、最後の結論VisualをCTAまで保持する。

| ID | 実測尺 | major visual | ImageGen | real UI | script変更segment | audio再生成segment | first3sec | PowerPoint feel | Fact | Draft v3 | thumbnail候補 |
|---|---:|---:|---:|---:|---:|---:|---|---|---:|---|---|
| Short001 | 26.95秒 | 3 | 3（v2再利用） | 0 | 1 | 1 | 4/5 REVIEW | 1/5 | 0 | shorts/001_chatgpt_voice_input/output/draft_v3.mp4 | shorts/001_chatgpt_voice_input/assets/thumbnail_candidate/first_frame_thumbnail_candidate.png |
| Short002 | 30.98秒 | 3 | 3（v2再利用） | 0 | 0 | 0 | 4/5 REVIEW | 1/5 | 0 | shorts/002_ai_suspicious_message/output/draft_v3.mp4 | shorts/002_ai_suspicious_message/assets/thumbnail_candidate/first_frame_thumbnail_candidate.png |
| Short003 | 27.34秒 | 3 | 3（v2再利用） | 0 | 0 | 0 | 4/5 REVIEW | 1/5 | 0 | shorts/003_mynumber_smartphone/output/draft_v3.mp4 | shorts/003_mynumber_smartphone/assets/thumbnail_candidate/first_frame_thumbnail_candidate.png |

### v3 QA

- dedicated CTA slide：0
- viewer-facing Short ID：0
- hybrid_generated_image_large_text：0
- fake UI：0
- official_ui_ai_reconstruction：0
- privacy_fail：0
- subtitle QA：3本とも64px未満なし、最大2行、overflow 0
- Shorts UI overlap：0
- headline_subtitle_duplicate：0
- renderer explanation scene：0
- full audio regeneration：0
- ImageGen新規call：0、再生成：0、v2完成画の再利用：9件
- Short001はVoice実UIが取得できないため、操作文言を一般化しsegment 03だけ差し替えた。Short002・003は台本と音声を変更していない。

Contact sheet：`shorts/work/batch_001_draft_contact_sheet_v3.png`

Draft v3完成後は、final、thumbnail確定、upload、schedule、publishへ進まない。

Shorts探索バッチ001 Visual Redesign v3完成。3枚ストーリー方式へ変更。人間Draft Gate待ち。

## Visual Redesign Draft v4実績

Draft v3のHuman Draft Gate REJECT（静止画を長く保持する説明資料感）を受け、3 core scenesを維持したまま各Shortを8 visual beatsへ再設計した。visual change targetは2〜4秒、static hold >7秒は0。CTA専用slideは作らず、結論Visualの最後約2〜3秒へ実チャンネルアイコン＋「大人のデジタル安心室」だけを表示した。

| ID | 実測尺 | core scenes | visual beats | mean beat interval | static >5s | static >7s | ImageGen | renderer beats | real UI | script変更 | audio再生成 | Draft v4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Short001 | 28.21秒 | 3 | 8 | 3.53秒 | 1 | 0 | 2 reuse | 0 | 3 + official ref 1 | 1 | 3 | shorts/001_chatgpt_voice_input/output/draft_v4.mp4 |
| Short002 | 32.24秒 | 3 | 8 | 4.03秒 | 0 | 0 | 2 reuse | 3 | 0 | 1 | 1 | shorts/002_ai_suspicious_message/output/draft_v4.mp4 |
| Short003 | 28.60秒 | 3 | 8 | 3.57秒 | 1 | 0 | 3 reuse | 2 | 0 | 1 | 1 | shorts/003_mynumber_smartphone/output/draft_v4.mp4 |

### v4 QA / review boundary

- Short001：ChatGPTの「ト」をaccent=3でquery確認。現行ChatGPTホーム実画面は使用済み。ライブVoiceセッションは`CAPTURE_REQUIRED`。
- Short002：privacy ImageGen画は不使用。generic documentで「氏名」「電話番号」「会員番号」「メールアドレス」の該当欄だけを`■■■■`でマスク。
- Short003：マイナポータル / 証明書・e-Taxは短いrenderer cueで表示し、3カード説明は不使用。
- CTA spoken canonical：`次に困ったときのために、このチャンネルを登録しておいてください。`
- 字幕：target80px、min64px、最大2行、overflow 0。fake UI 0、official UI AI reconstruction 0、privacy fail 0、pseudo subscribe UI 0。
- ImageGen新規call 0、再生成0。全音声再生成0。final、thumbnail確定、upload、publish、scheduleは未実施。
- 詳細タイムライン：`shorts/work/batch_001_v4_timeline_review.md`

Shorts探索バッチ001 Visual Redesign v4完成。
静止画スライドショー方式を廃止し、
Shorts-native visual beats方式へ変更。
人間Draft Gate待ち。

## Visual Redesign Draft v5実績

Draft v4のHuman Draft Gate（約50/100、微細zoom/panによる動き、Short003の抽象usage renderer）を受け、必要な箇所だけを修正した。v5は静止画を読みやすく保持し、意味のあるasset/state切替だけをhard cutで行う。

| ID | 実測尺 | core scenes | visual beats | mean static state | static >5s | ImageGen reuse / new | renderer beats | real UI / ref | official image | Draft v5 |
|---|---:|---:|---:|---:|---:|---|---:|---|---:|---|
| Short001 | 28.21秒 | 3 | 6 | 4.70秒 | 2 | 3 / 0 | 0 | 1 / 1 | 0 | shorts/001_chatgpt_voice_input/output/draft_v5.mp4 |
| Short002 | 32.24秒 | 3 | 7 | 4.61秒 | 0 | 3 / 0 | 3 | 0 / 0 | 0 | shorts/002_ai_suspicious_message/output/draft_v5.mp4 |
| Short003 | 28.60秒 | 3 | 8 | 3.57秒 | 2 | 4 / 2 | 0 | 0 / 0 | 1 | shorts/003_mynumber_smartphone/output/draft_v5.mp4 |

### v5適用内容

- `shorts_micro_motion_for_motion_sake=FORBIDDEN`。意味のないzoom、pan、micro motionは0。beat数はKPIにしない。
- Short001はA1/A2を統合。現行ChatGPT実画面、公式Voice参照、生活sceneを静止＋hard cutで使用。ライブVoice captureは`CAPTURE_REQUIRED`。
- Short002はA1/A2を統合。v4 approved privacy rendererの未マスク→一部マスク→全マスクを静止表示し、結論の人物・スマホfocusだけを意味のある別cropで用意。
- Short003はA1/A2を統合。デジタル庁公式マイナポータル画面→コンビニ証明書→e-Tax→医療利用→端末差→実物カードへ具体化。旧抽象usage rendererは不使用。
- CTAは3本とも専用slideなし。spoken canonicalは`次に困ったときのために、このチャンネルを登録しておいてください。`のまま、最後3秒だけ実チャンネルアイコン180px＋チャンネル名を中央表示。`概要欄から`は追加していない。
- 音声・台本の変更0、全音声再生成0。`audio/narration_v4.wav`を再利用。字幕はv4の実時間cueを再利用し、target80px / min64px / 最大2行。
- fake UI 0、official UI AI reconstruction 0、privacy fail 0、hybrid large-text overlay 0、Shorts UI overlap 0、viewer-facing internal brand promise 0。
- ImageGen新規callはShort003のコンビニ証明書sceneとe-Tax生活sceneの2枚だけ。再生成0。公式マイナポータル画面はデジタル庁公式素材。

### v5 outputs / gate

- Batch contact sheet：`shorts/work/batch_001_draft_contact_sheet_v5.png`
- Timeline review：`shorts/work/batch_001_v5_timeline_review.md`
- Report：`shorts/work/batch_001_draft_report_v5.md`
- 各Shortの`work/render_manifest_v5.json`、`work/v5_audio_reuse.md`、`work/draft_v5_qa.md`を生成済み。
- Human quality self-score：`68/100_REVIEW`。人間Draft Gate待ち。
- final、thumbnail確定、upload、publish、scheduleは未実施。

Shorts探索バッチ001 Visual Redesign v5完成。
不要なmicro motionを廃止。
CTA中央化・Short003利用例Visualを具体化。
人間Draft Gate待ち。
