# Short001 script — Draft v8（Dictation / 音声入力）

## 基本情報

- canonical title：ChatGPT、文字を打たなくても使える？
- feature_type：Dictation / 音声入力
- 1本の問い：ChatGPTで、文字を打たずに質問できる？
- v8変更点：元capture後半の実際の料理回答を追加。回答は書き直さず、画面のcrop / resizeだけで見せる
- 目標尺：30秒程度、上限30秒を目安
- scene構成：hook → 実際の音声入力 → 文字化の確認 → 送信 → 実際の回答 → 短い結論 → CTA
- ナレーター：VOICEVOX「剣崎雌雄」ノーマル
- 実画面：ユーザー提供のiPhone画面録画を正本にする。架空の画面は作らない

`narration` はVOICEVOXへ渡す文、`subtitle_display` は画面表示の正本。実録音声のsegment 03だけはユーザー提供captureの音声を使う。実回答sceneでは機械返答音声を使わず、回答画面を主役にする。表示字幕に読み仮名は入れない。

## セグメント

### 01｜Scene 01｜冒頭の問い

- shot_tag：なし
- narration：ChatGPT、文字を打つのが大変ですか。
- subtitle_display：
  - 「文字入力が大変？」
- visual：v7から再利用するImageGen-native hook。人物とスマホを見せ、実在サービスのUIは出さない
- intent：タイトルと同じ問いを最初に提示する

### 02｜Scene 02｜結論の先出し

- shot_tag：なし
- narration：音声入力なら、話した内容を文字にして送れます。
- subtitle_display：
  - 「話すだけで文字に」
- visual：ユーザーcaptureから切り出した、マイク入力中の実画面
- intent：音声入力の役割を一文で伝える

### 03｜Scene 03｜実際に話す

- shot_tag：[SHOT-01]
- narration：実録音声「冷蔵庫にキャベツがあります。簡単な料理を教えてください。」
- subtitle_display：
  - 「冷蔵庫にキャベツが」
  - 「あります。」
  - 「簡単な料理を」
  - 「教えてください。」
- visual：ユーザー提供の実画面。3.800〜12.800秒のマイク入力中→文字起こし中→質問文表示を9秒以内で表示する
- intent：話す → 文字になる、を実画面と実録音声で示す

### 04｜Scene 04｜文字を確認して送信

- shot_tag：[SHOT-02]
- narration：文字になったら、内容を確認して送信します。
- subtitle_display：
  - 「文字になったら確認」
- visual：同じ実画面の文字化後crop。質問文を読み取れる大きさで見せる
- intent：送信前に内容を確認する手順を伝える

### 05｜Scene 05｜実際の料理回答

- shot_tag：[SHOT-03]
- narration：料理の答えが返ってきました。
- subtitle_display：
  - 「ちゃんと答えが」
  - 「返ってきた」
- visual：元captureの14.200〜17.000秒から、実際に表示された回答の冒頭・料理名・材料が見える部分をcrop / resizeする。大きな説明見出しは後乗せしない
- intent：話した内容が文字になり、送信すると実際の回答が返る流れを、実ChatGPT画面で確認する
- constraint：回答の全文朗読、回答文の書き直し、回答内容の合成、UI改変はしない

### 06｜Scene 06｜短い結論

- shot_tag：なし
- narration：文字を打たずに、質問できました。
- subtitle_display：
  - 「質問できました。」
- visual：v7から再利用するImageGen-native conclusion。回答後は短く表示する
- intent：Dictationでできたことを一文にまとめる

### 07｜Scene 06｜共通CTA

- shot_tag：なし
- narration：次に困ったときのために、このチャンネルを登録しておいてください。
- subtitle_display：
  - 「次に困ったときのために」
  - 「このチャンネルを登録して」
  - 「おいてください。」
- visual：結論Visualに実チャンネルアイコン約180pxと「大人のデジタル安心室」を中央表示。登録ボタンや疑似subscribeは描画しない
- intent：共通CTAを最後に表示する

## Fact / production boundary

- 今回はDictation / 音声入力だけを扱う。話した音声を文字にし、送信前に確認し、実際のテキスト回答が返る流れを見せる。
- ユーザー提供captureの質問文「冷蔵庫にキャベツがあります。簡単な料理を教えてください。」をcanonicalな実例として使う。
- 元captureには、回答冒頭「もちろんです！キャベツだけでも、かなり簡単に作れます。」と、料理名「いちばん簡単『キャベツの塩昆布炒め』」が表示されている。動画では14.200〜17.000秒の実画面を使い、回答を改変しない。
- ChatGPTの返答音声は使わない。Voice / リアルタイム会話の紹介にしない。
- 実画面の上部にあるアカウント情報は選択区間に含めない。個人情報が見える素材は使用しない。
- OS・アプリ版・アカウントで画面が変わる可能性があるため、画面の位置を一般化して断定しない。
