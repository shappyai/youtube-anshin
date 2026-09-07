# Short001 script — Draft v7（Dictation / 音声入力）

## 基本情報

- canonical title：ChatGPT、文字を打たなくても使える？
- feature_type：Dictation / 音声入力
- 1本の問い：ChatGPTで、文字を打たずに質問できる？
- 目標尺：30秒以内
- scene構成：hook → 実際の音声入力 → 文字化の確認 → 結論 → CTA
- ナレーター：VOICEVOX「剣崎雌雄」ノーマル
- 実画面：ユーザー提供のiPhone画面録画を正本にする。架空の画面は作らない

`narration` はVOICEVOXへ渡す文、`subtitle_display` は画面表示の正本。実録音声のsegment 03だけは、ユーザー提供captureの音声を使う。表示字幕に読み仮名は入れない。

## セグメント

### 01｜Scene 01｜冒頭の問い

- shot_tag：なし
- narration：ChatGPT、文字を打つのが大変ですか。
- subtitle_display：
  - 「文字入力が大変？」
- visual：新規ImageGen-native hook。人物とスマホを見せ、実在サービスのUIは出さない
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
- visual：ユーザー提供の実画面。マイク入力中から文字起こし後までを9秒以内で表示する
- intent：話す → 文字になる、を実画面と実録音声で示す

### 04｜Scene 04｜文字を確認する

- shot_tag：[SHOT-02]
- narration：文字になったら、内容を確認して送信します。
- subtitle_display：
  - 「文字になったら確認」
- visual：同じ実画面の文字化後のcrop。質問文を読み取れる大きさで見せる
- intent：送信前に内容を確認する手順を伝える

### 05｜Scene 05｜まとめ

- shot_tag：なし
- narration：文字を打たずに、質問できました。
- subtitle_display：
  - 「文字を打たずに質問」
- visual：新規ImageGen-native conclusion。公式UIやロゴは生成しない
- intent：今回の答えを短く保存しやすい一文にする

### 06｜Scene 05｜共通CTA

- shot_tag：なし
- narration：次に困ったときのために、このチャンネルを登録しておいてください。
- subtitle_display：
  - 「次に困ったときのために」
  - 「このチャンネルを登録して」
  - 「おいてください。」
- visual：結論Visualに実チャンネルアイコン約180pxと「大人のデジタル安心室」を中央表示。登録ボタンや疑似subscribeは描画しない
- intent：共通CTAを最後に表示する

## Fact / production boundary

- 今回はDictation / 音声入力だけを扱う。話した音声を文字にし、送信前に確認できることを見せる。
- ユーザー提供captureの質問文「冷蔵庫にキャベツがあります。簡単な料理を教えてください。」をcanonicalな実例として使う。
- ChatGPTの返答全文は使わない。返答の正確性をShort001の主題にしない。
- 実画面の上部にあるアカウント情報は選択区間に含めない。個人情報が見える素材は使用しない。
- OS・アプリ版・アカウントで画面が変わる可能性があるため、画面の位置を一般化して断定しない。
