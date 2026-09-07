# Short001 script — Draft v1

## 基本情報

- 仮タイトル：ChatGPT、文字を打たなくていいんです
- 1本の問い：ChatGPTに話しかけて使える？
- 人間Script Gate：APPROVED_WITH_COMPRESSION（2026-09-06）
- 目標尺：30秒（27〜31秒、最大35秒）
- scene目安：3 major visual（ナレーションセグメントとは分離。結論とCTAは3枚目に含める）
- 音声：VOICEVOX「剣崎雌雄」ノーマル
- 実機：iPhoneまたはAndroidを1台だけ。UI形状・位置は収録時の現在表示を正とする

narrationがVOICEVOXへ渡す読み上げ文、subtitle_displayが画面表示の正本。ChatGPTは読み上げで「チャットジーピーティー」とし、表示字幕では「ChatGPT」とする。時間は仮置きで、実音声生成後に発話の実時間で調整する。

## セグメント

### 01｜Scene 01｜0.0〜3.0秒｜フック

- shot_tag：なし
- narration：チャットジーピーティー、文字入力は大変ですか。
- subtitle_display：
  - 「文字入力は」
  - 「大変ですか？」
- visual：人物または抽象スマホの概念画。実在アプリ画面・ロゴ・生成文字は出さない
- intent：1本1問を最初の3秒で提示する

### 02｜Scene 02｜3.0〜6.0秒｜結論

- shot_tag：なし
- narration：音声モードなら、話しかけて使えます。
- subtitle_display：
  - 「音声モードなら」
  - 「話しかけて使える」
- visual：マイクと音声波形のsemantic icon。字幕帯と重ねない
- intent：最初の20秒を待たずに答えを示す

### 03｜Scene 03｜6.0〜10.0秒｜現在の入口

- shot_tag：なし
- narration：スマホに向かって、短い質問を話しかけてみます。
- subtitle_display：
  - 「スマホに向かって」
  - 「短い質問を話す」
- visual：ImageGen-nativeの生活場面。公式UI・架空UI・ボタン位置は出さない
- intent：UI操作を断定せず、スマホへ話しかける使い始めの動作を伝える

### 04｜Scene 04｜10.0〜18.0秒｜生活例

- shot_tag：[SHOT-02]
- narration：冷蔵庫に卵とキャベツがあります。何を作れますか。
- subtitle_display：
  - 「卵とキャベツで」
  - 「聞いてみる」
- visual：実機へ自作の生活質問を話す。個人情報のない文だけを使う
- intent：機能名ではなく、生活の一言で使い道を示す

### 05｜Scene 05｜18.0〜24.0秒｜応答

- shot_tag：[SHOT-03]
- narration：チャットジーピーティーが、質問に合わせて答え始めます。
- subtitle_display：
  - 「答え始める」
- visual：回答の開始だけを見せ、回答全文は読ませない。履歴・アカウント情報を映さない
- intent：音声で会話が始まることだけ確認する

### 06｜Scene 06｜24.0〜27.0秒｜まとめ

- shot_tag：なし
- narration：まずは、話しかけるだけです。
- subtitle_display：
  - 「まずは短い質問から」
- visual：テンプレートのsemantic microphone / conversation icon。登録ボタンや疑似登録アイコンは描画しない
- intent：Shortの答えを保存しやすい一文にする

### 07｜Scene 06｜27.0〜29.0秒｜次テーマ

- shot_tag：なし
- narration：次は、写真で聞く手順も確認します。
- subtitle_display：
  - 「次は写真で聞く」
- visual：写真入力を示す小さなsemantic image icon。大見出しにせず、CTAの前置きとして扱う
- intent：長尺候補への導線を短く残す

### 08｜Scene 06｜29.0〜31.0秒｜共通CTA

- shot_tag：なし
- narration：次に困ったときのために、このチャンネルを登録しておいてください。
- subtitle_display：
  - 「次に困ったときのために」
  - 「このチャンネルを登録」
- visual：左側のブランド枠だけを使う軽い装飾。右側のShorts UI領域を空ける
- intent：Shorts共通CTAを最後約3秒で表示する

## Fact / production boundary

- iOS・AndroidでVoice利用可、message barのVoice icon、マイク許可が必要な場合、VoiceとDictationが別という事実はfacts.mdに保持する。
- 「マイクを許可」は独立sceneにしない。実機収録中に表示された場合だけ、Scene 03の短い補足として扱う。
- UI形状・位置・表示名は収録時の実機を正とし、生成画像で公式UIを再現しない。
