# Short002 script — Draft v1

## 基本情報

- 仮タイトル：怪しいメール、AIに見せて大丈夫？
- 1本の問い：怪しいメールをAIへ相談するとき、何を先にする？
- 人間Script Gate：APPROVED_WITH_COMPRESSION（2026-09-06）
- 目標尺：30秒（27〜31秒、最大35秒）
- scene目安：3 major visual（ナレーションセグメントとは分離。結論とCTAは3枚目に含める）
- 音声：VOICEVOX「剣崎雌雄」ノーマル
- 実在メール・企業ロゴ・実QR・fake app UI：すべて0

narrationがVOICEVOXへ渡す読み上げ文、subtitle_displayが画面表示の正本。AIは読み上げで「エーアイ」、QRコードは読み上げで「キューアールコード」とし、読み仮名を表示字幕へ流出させない。時間は仮置きで、実音声生成後に発話の実時間で調整する。

## セグメント

### 01｜Scene 01｜0.0〜3.2秒｜フック

- shot_tag：なし
- narration：このメール、本物かエーアイに聞きたいですよね。
- subtitle_display：
  - 「AIに聞く前に」
  - 「一呼吸」
- visual：抽象的な通知と迷う人物またはスマホ。実在メールのUI・企業ロゴ・送信者名は出さない
- intent：視聴者の自然な行動を問いにする

### 02｜Scene 02｜3.2〜7.2秒｜先に隠す

- shot_tag：[SHOT-01]
- narration：名前、住所、電話番号、会員番号などの個人情報は隠します。
- subtitle_display：
  - 「名前や番号は」
  - 「先に隠す」
- visual：抽象文面にマスク帯を置く。実在値、企業名、QRコード画像を使わない
- intent：AIへ見せる前の安全行動を先に置く

### 03｜Scene 03｜7.2〜12.5秒｜AIの役割

- shot_tag：[SHOT-02]
- narration：エーアイには、文面整理と怪しい点の洗い出しを手伝ってもらいます。
- subtitle_display：
  - 「AIは整理の補助」
  - 「怪しい点を洗い出す」
- visual：AIを判定機にしない意味図解。合否バッジや「安全」のスタンプは禁止
- intent：便利さを残しながら、役割を補助に限定する

### 04｜Scene 04｜12.5〜17.0秒｜最終判定ではない

- shot_tag：なし
- narration：エーアイが大丈夫と言っても、本物とは決めません。
- subtitle_display：
  - 「AIだけで決めない」
- visual：AIの吹き出しと公式確認の導線を別々に配置。AIの吹き出しを正解表示にしない
- intent：AIの回答を確定判定にしない

### 05｜Scene 05｜17.0〜24.5秒｜公式から確認

- shot_tag：[SHOT-03]
- narration：メールのリンクは開かず、公式アプリや、ブックマークした公式サイトから確認します。
- subtitle_display：
  - 「メールのリンクは開かない」
  - 「公式アプリから」
  - 「ブックマークから確認」
- visual：リンクアイコンから公式アプリ・ブックマークへ向かう抽象フロー。実在サイトを再現しない
- intent：警察庁の行動指針を実行順で見せる

### 06｜Scene 06｜24.5〜27.5秒｜まとめ

- shot_tag：[SHOT-04]
- narration：エーアイは補助。最後は公式から確認。
- subtitle_display：
  - 「AIは補助」
  - 「確認は公式へ」
- visual：マスク・AI補助・公式確認のsemantic icon。単純記号の自作バッジは使わない
- intent：順番を保存しやすい形で再提示する

### 07｜Scene 06｜27.5〜30.0秒｜共通CTA

- shot_tag：なし
- narration：次に困ったときのために、このチャンネルを登録しておいてください。
- subtitle_display：
  - 「次に困ったときのために」
  - 「このチャンネルを登録」
- visual：左側のブランド枠だけを使う軽い装飾。右側のShorts UI領域を空ける
- intent：Shorts共通CTAを最後約3秒で表示する

## Fact / production boundary

- AIがフィッシングを確定判定するとは言わない。
- 実在メール、企業ロゴ、URL、QRコード、個人情報を素材へ入れない。
- 被害後の相談先やData Controlsの詳細は、一次情報URL付きの長尺・概要欄へ分ける。
