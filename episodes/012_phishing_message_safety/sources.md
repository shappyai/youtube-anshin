# Episode 012 sources

確認日: 2026-09-06

一次情報を優先して、2026年9月6日に本文を再確認した。ページは更新されるため、公開直前に再確認する。Case 1は公式相談例、Case 2〜5は公式注意喚起に基づく架空の再現として扱う。

| ID | 組織 / URL | 確認できたこと | 使用箇所 |
|---|---|---|---|
| SRC-001 | 国民生活センター / https://www.kokusen.go.jp/mimamori/mj_mailmag/mj-shinsen550.html | 2026年9月3日公表。普段使うアプリ名のメールから支払い情報を更新し、後に約20万円の利用通知を受けた80歳代の相談例。メール・SMSのリンクを使わず、正規サイト・アプリから確認し、明細をこまめに確認する助言。188も案内。 | 冒頭、Case 1、まとめ、相談先 |
| SRC-002 | 警察庁 / https://www.npa.go.jp/bureau/cyber/countermeasures/phishing.html | 実在サービス・企業をかたるメール・SMSから偽サイトへ誘導する手口。リンクは偽装可能で見た目の判定が困難。ブックマークや公式アプリを使う、OS・アプリを更新する、使い回しを避ける、ワンタイムパスワード等を使う案内。 | 共通ルール、被害後 |
| SRC-003 | フィッシング対策協議会 / https://www.antiphishing.jp/report/report/phishing_report2026.html | 2026年6月1日公表のレポート。SMSで装う対象は宅配業者、クレジットカード会社、ECサイトが上位。官公庁を装う手口の増加にも言及。ケース選定の需要根拠。 | 企画判断、長尺gate |
| SRC-004 | フィッシング対策協議会 / https://www.antiphishing.jp/report/guideline/consumer_guideline2026.html | 2026年度版利用者向けガイドライン。宅配便の不在連絡を装うSMSから、Androidは不正アプリ、iPhoneなどは偽ログイン画面へ誘導される例。正規アプリストア、提供元、不要権限の確認、重要情報入力後の対応も説明。 | Case 2、被害後 |
| SRC-005 | 日本郵便 / https://www.post.japanpost.jp/notification/notice/fraud-mail.html | 日本郵便を装う不審メール・SMSが個人情報・カード情報の不正取得、不正アプリ等につながる可能性。リンクをクリックせず、迷う場合は公式ページの問い合わせ先へ。再配達・配送支払いを装う例。 | Case 2 |
| SRC-006 | JCB / https://www.jcb.co.jp/security/phishing/ | JCBを名乗る「不正ログイン」「利用制限」等から偽サイトへ誘導し、カード情報・MyJCBのID／パスワードを盗む事例。MyJCBアプリ・ブックマークした公式サイトを使う。カード暗証番号をメール・SMSで求めない。入力後の停止・変更案内。 | Case 3、被害後 |
| SRC-007 | 三井住友カード / https://www.smbc-card.com/customer_voice/survey/sur0000047.jsp | 2026年4月8日公表。カード利用確認通知の受信方法を案内し、2026年1月以降はフィッシング対策としてメールからの回答を廃止したこと、アプリプッシュ通知等の運用を説明。正規通知も存在することの補助根拠。 | Case 3 |
| SRC-008 | ソフトバンク / https://www.softbank.jp/mobile/support/protect/spam/ | 料金未払い・利用停止予告を装うメール・SMSに対し、URLアクセス・返信をせず、ブックマーク・アプリ・検索経由で正規サイトを確認する案内。公式サイトで利用状況・請求額を確認でき、入力後は公式側でパスワード変更・登録情報確認。 | Case 4、被害後 |
| SRC-009 | 国税庁 / https://www.nta.go.jp/information/attention/attention.htm | 国税庁等はSMSにURLを記載した案内を送らず、国税の納付・差押えをSMS・メール・LINEで求めない。不審なメッセージはアクセス・支払いをしない。e-Taxは決まったパターン、原則URLなし、添付なし。 | Case 5 |
| SRC-010 | 消費者庁 / https://www.caa.go.jp/notice/statement/horii/044840.html | 2026年1月15日会見要旨。消費者庁から電話・メール・はがき等で個人情報の提供や金銭の支払いを求めることはないと説明。 | Case 5 |
| SRC-011 | Apple / https://www.apple.com/jp/apple-events/ | 2026年9月10日午前2時（日本時間）の特別イベントを掲載。公開順を見直す条件の外部予定。 | Apple Event gate |
| SRC-012 | フィッシング対策協議会 / https://www.antiphishing.jp/report/guideline/antiphishing_guideline2026.html | 2026年度版事業者向けガイドライン。国内携帯番号等を使うSMS、宅配便不在通知、偽サイト・不正アプリの拡大例を説明。 | Case 2、共通ルール |

## 公式画面・素材の扱い

- Phase Aでは公式UIの画像を取得せず、公式ページの主張を正確な引用カード／source labelとして設計する。
- Phase Bで公式画面を使う場合は、公式sourceまたは自分のテスト端末のcaptureだけを採用する。
- 架空のSMS・メール画面を実際に再現する場合だけ `再現イメージ` を表示する。今回のSCENE-006 / 011 / 017 / 021 / 025は説明用の意味図解へ変更し、画面再現ラベルを置かない。実在のメールアドレス、URL、電話番号、QRコード、氏名、アカウント番号、ロゴは入れない。
- sources.mdのURLと確認日、何が確認できたかを概要欄・media_manifestへ引き継ぐ。画面には長いURLや確認日を表示しない。

## Phase Bで採用した公式素材

2026年9月6日に公式公開ページ・公開資料から該当箇所を取得し、視聴者向け画面では必要な事実だけをクロップして使用する。元資料は `assets/official/_source/` に保持し、採用copyは `assets/official/` に置く。SCENE-008とSCENE-013は公式UIを再現せず、台本の安全行動を意味図解として描画する。

| Scene | 採用素材 | 一次情報 | 画面上の扱い | プライバシー |
|---|---|---|---|---|
| SCENE-007 | 公式PDFからの正確な短い引用（quote asset） | SRC-001 / https://www.kokusen.go.jp/mimamori/pdf/shinsen550.pdf | 「記載されているURLにはアクセスせず、事前にブックマークした正規サイトのURLや、正規のアプリからアクセスしましょう。」を全文引用。部分抽出・OCR fallbackは使用しない。 | 公式公開資料のみ |
| SCENE-008 | semantic operation visual | SRC-001 | 「メールを閉じる」→「自分で公式アプリを開く」。実在アプリ画面は作らない。 | 個人情報なし |
| SCENE-012 | `assets/official/scene_012_antiphishing_delivery_flow.png` | SRC-004 / https://www.antiphishing.jp/report/guideline/consumer_guideline2026.html | 宅配SMSから偽サイト・不正アプリへ誘導される公式図。出典ラベルを表示。 | 公式公開資料のみ |
| SCENE-013 | centered safe-entry options visual | SRC-004, SRC-005 | 公式アプリ・公式サイト・手元の不在票の3入口を中央に配置。 | 個人情報なし |
| SCENE-018 | `assets/official/scene_018_jcb_warning.png` | SRC-006 / https://www.jcb.co.jp/security/phishing/ | JCB公式のリンク誘導イラスト。出典ラベルを表示。 | 公式公開資料のみ |
| SCENE-022 | `assets/official/scene_022_softbank_warning.png` | SRC-008 / https://www.softbank.jp/mobile/support/protect/spam/ | 警告見出しだけをクロップ。宛先・金額・日付は表示しない。 | PIIなしの警告部分のみ |
| SCENE-026 | `assets/official/scene_026_nta_warning.png` | SRC-009 / https://www.nta.go.jp/information/attention/attention.htm | 国税庁のSMS・メールに関する警告バナーを1点大きく表示。 | 公式公開資料のみ |

## Fact gaps / recheck

2026-09-06 final primary-source recheck: `FAIL 0`。上表の8件を再確認し、主要な台本主張・概要欄URL・公式素材の対応に欠落はない。公開直前のlive page、各事業者の通知仕様、Apple Event後の公開順だけは、人間確認の`REVIEW 3`として残す。

- 事業者ごとの正規SMS送信元、通知チャネル、問い合わせ手順は異なる。動画では各社の共通安全行動に留め、公開前に実際に使用する公式画面を再確認する。
- 国税庁・消費者庁の連絡方法は更新される可能性があるため、公開直前に本文を再確認する。
- Apple Event後の公開順は、発表内容を見て人間が判断する。Episode 012の制作中止条件ではない。
