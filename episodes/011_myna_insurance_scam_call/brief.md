# Episode 011 Brief

- Episode: 011
- Slug: myna_insurance_scam_call
- Working title: 【マイナ保険証】「1番を押して」の電話、本物？まず確認したい3つ
- Pillar: protect
- Target viewer: 50〜70代、特に65歳以上。マイナ保険証の話を電話で持ち出され、操作を急かされると不安になる人
- Viewer problem: 「確認です」「1番を押してください」と自動音声で言われたとき、押すべきか、折り返すべきか分からない
- Promise: 番号を押さず、情報を伝えず、公式窓口から自分で確認する3つを、その場で使える形で覚える
- Why now: 厚生労働省が、職員を装い健康保険証利用登録を音声案内で促す詐欺電話を確認し、電話音声やSMSで直接利用登録を要求しないと案内している
- Search intent: マイナ保険証／1番を押して／電話／自動音声／詐欺
- Browse hook: 実在の詐欺音声を流さず、聞き慣れた短い電話文言から「まず止まる」判断へ直結させる
- Required real-device demos: なし。実音声なし。公式ページの重要文は確認済み本文の拡大quote cropを使用する
- Do not claim: マイナ保険証関連の電話は全部詐欺、厚労省から電話が来ることは絶対にない、1番を押すと即被害、電話登録が正式手続き、SMSリンク登録が公式、#9110が緊急通報
- Target length: 4:00〜5:00 + CTA（Phase A推定。無理に引き延ばさず、Phase BでVOICEVOX実測）

## 登録者獲得実験 v2

- experiment：`registration_conversion_v2`
- story_intro：true。視聴者に電話がかかり、「1番を押してください」と言われる場面を入口にする。
- reason_to_return_cta：true。Episode010のreason-to-return CTAを基本reuseする。
- midroll_subscribe_cta：true。公式結論と「番号を押さない」の説明後に1回だけ、6.7秒予定で入れる。
- 比較対象：Episode010。テーマが異なるため、厳密なA/B testではなく準実験として公開後に確認する。

## Episode 010との境界

Episode 010はマイナアプリの初回利用登録。Episode 011はマイナ保険証の健康保険証利用登録を口実にした電話・自動音声詐欺の確認であり、アプリ操作は解説しない。
