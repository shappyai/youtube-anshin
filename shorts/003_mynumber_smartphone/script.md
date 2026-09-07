# Short003 script — Draft v1

## 基本情報

- 仮タイトル：マイナンバーカード、スマホに入れると何ができる？
- 1本の問い：スマホのマイナンバーカードで何ができる？
- 人間Script Gate：APPROVED_WITH_COMPRESSION（2026-09-06）
- 目標尺：30秒（27〜31秒、最大35秒）
- scene目安：3 major visual（ナレーションセグメントとは分離。結論とCTAは3枚目に含める）
- 音声：VOICEVOX「剣崎雌雄」ノーマル
- 実機：原則renderer。実機を使う場合はiPhoneまたはAndroidを1台だけ

narrationがVOICEVOXへ渡す読み上げ文、subtitle_displayが画面表示の正本。e-Taxはナレーションで「イータックス」と読み、表示字幕では「e-Tax」とする。時間は仮置きで、実音声生成後に発話の実時間で調整する。

## セグメント

### 01｜Scene 01｜0.0〜3.0秒｜フック

- shot_tag：なし
- narration：マイナンバーカード、スマホに入れられる？
- subtitle_display：
  - 「スマホに入れると」
  - 「何ができる？」
- visual：カードとスマホの抽象概念画。政府マーク、実在カード番号、公式UIは出さない
- intent：便利さの入口を一問にする

### 02｜Scene 02｜3.0〜11.0秒｜できること

- shot_tag：[SHOT-01]
- narration：マイナポータル、コンビニでの証明書取得、イータックスなどに使えます。
- subtitle_display：
  - 「マイナポータル」
  - 「コンビニの証明書」
  - 「e-Taxなど」
- visual：公式ページで案内される利用例を、実在画面ではなく大きな3項目のテンプレート図解で順に表示
- intent：利用例を一つの画面で詰め込まず、時間に沿って読ませる

### 03｜Scene 03｜11.0〜16.0秒｜保険証の例

- shot_tag：[SHOT-02]
- narration：対応する医療機関や薬局では、マイナ保険証として使える場合もあります。
- subtitle_display：
  - 「医療機関や薬局で」
  - 「使えることも」
- visual：病院・薬局のsemantic icon。対応条件の長文は表示しない
- intent：便利さを広げつつ、対応条件を残す

### 04｜Scene 04｜16.0〜22.0秒｜端末差

- shot_tag：[SHOT-03]
- narration：ただし、iPhoneとAndroidで、使える場所が違う場合があります。
- subtitle_display：
  - 「端末で違いあり」
- visual：端末アイコンの薄い2カラム。機種一覧や細かいOS条件は出さない
- intent：全員同じと誤解させない

### 05｜Scene 05｜22.0〜27.5秒｜実物カードと結論

- shot_tag：[SHOT-04]
- narration：実物カードが必要な場面もあります。スマホだけで全部、ではありません。
- subtitle_display：
  - 「実物カードが」
  - 「必要な場面も」
- visual：スマホと実物カードのsemantic iconを並べる。実在カード画像や番号は使わない
- intent：便利さの裏側の条件を結論として残す

### 06｜Scene 06｜27.5〜30.0秒｜共通CTA

- shot_tag：なし
- narration：次に困ったときのために、このチャンネルを登録しておいてください。
- subtitle_display：
  - 「次に困ったときのために」
  - 「このチャンネルを登録」
- visual：左側のブランド枠だけを使う軽い装飾。右側のShorts UI領域を空ける
- intent：Shorts共通CTAを最後約3秒で表示する

## Fact / production boundary

- 利用例はデジタル庁の収録日現在の案内を正とする。
- iPhone・Androidの利用場所差と、実物カードだけに対応する場面があることは、条件付きで保持する。
- 「カード本体は不要」「スマホだけで全部できる」とは言わない。
