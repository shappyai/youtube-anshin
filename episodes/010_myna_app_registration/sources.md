# Episode 010 Sources

確認日：2026-09-05（日本時間）

## 一次情報

| source_id | URL | title | organization | checked_at | 何が確認できたか |
|---|---|---|---|---|---|
| SRC-001 | https://services.digital.go.jp/mynaapp/ | マイナアプリ（旧マイナポータルアプリ） | デジタル庁 | 2026-09-05 | 現行アプリ名、2026年8月25日の刷新、既存アプリ更新、初回利用登録、マイナポータルとの関係 |
| SRC-002 | https://services.digital.go.jp/mynaapp/register/ | マイナアプリの利用登録の方法 | デジタル庁 | 2026-09-05 | 規約・プライバシー、利用登録開始、通知、端末ロック、本人認証、登録完了の6段階 |
| SRC-003 | https://services.digital.go.jp/mynaapp/system-requirements/ | マイナアプリの動作環境 | デジタル庁 | 2026-09-05 | iOS 16.4以上、Android 11以上、NFC、端末ロックなどアプリ本体の条件 |
| SRC-004 | https://services.digital.go.jp/mynaapp/scan-mynumbercard/ | マイナアプリを使ってマイナンバーカードを読み取る方法 | デジタル庁 | 2026-09-05 | 実物カードをスマートフォンに重ねる読み取り手順、機種別の注意 |
| SRC-005 | https://services.digital.go.jp/mynumbercard/auth-passcode/ | マイナンバーカードの利用者証明用暗証番号 | デジタル庁 | 2026-09-05 | 利用者証明用電子証明書の数字4桁、署名用パスワードとの違い |
| SRC-006 | https://services.digital.go.jp/mynumbercard-iphone/ | iPhoneのマイナンバーカード | デジタル庁 | 2026-09-05 | iPhoneのマイナンバーカードの別ルート、iOS 18.5以上・iPhone XS以上 |
| SRC-007 | https://services.digital.go.jp/mynumbercard-android/ | Androidスマホ用電子証明書搭載サービス | デジタル庁 | 2026-09-05 | Androidスマートフォンの電子証明書の別ルート、対応機種確認 |
| SRC-008 | https://services.digital.go.jp/mynaportal/login/ | マイナポータルへのログイン方法 | デジタル庁 | 2026-09-05 | マイナポータルへのログインと利用登録の区別 |
| SRC-009 | https://faq.myna.go.jp/faq/show/2685?category_id=14&site_domain=default | 利用者登録とは何ですか。 | マイナポータル | 2026-09-05 | マイナポータル利用者登録は利用者情報・メール等を登録する別概念 |
| SRC-010 | https://apps.apple.com/jp/app/マイナアプリ-旧マイナポータルアプリ/id1476359069 | マイナアプリ（旧マイナポータルアプリ） | Apple App Store | 2026-09-05 | ストア上の現行アプリ名・対応情報 |
| SRC-011 | https://play.google.com/store/apps/details?id=jp.go.cas.mpa&hl=ja | マイナアプリ（旧マイナポータルアプリ） | Google Play | 2026-09-05 | ストア上の現行アプリ名・配信情報 |

## 既存調査

- research/episode010_myna_app_registration/official_flow.md
- research/episode010_myna_app_registration/market_research.md
- research/episode010_myna_app_registration/youtube_competitors.md
- research/episode010_myna_app_registration/google_trends.md
- research/episode010_myna_app_registration/channel_evidence.md

## 素材の出典

公式UI素材は、Episode 002で取得・記録したデジタル庁公式素材のうち、利用登録に関係するPII-free原画を再利用した。利用元と内容は assets/official/README.md に記録する。

## 更新注意

アプリ名、画面文言、対応OS、Android機能名称、対応機種は更新され得る。公開前にSRC-001〜SRC-007を再確認する。

## 公開前最終再確認（2026-09-06・日本時間）

デジタル庁の現行公式ページを再確認した。ページの公開状態・名称・関連案内に、今回の最終動画を差し替える必要がある変更は見当たらなかった。画面文言と対応端末は更新され得るため、公開前の実機照合は継続する。

| source | 再確認できたこと | 最終扱い |
|---|---|---|
| SRC-001 / SRC-002 | マイナアプリの現行案内と利用登録手順ページが公開中 | 6段階の説明を維持 |
| SRC-003 | マイナアプリの動作環境ページが公開中 | 詳細条件は冒頭に置かず補足で扱う |
| SRC-004 / SRC-005 | カード読み取り案内と利用者証明用暗証番号の公式ページが公開中 | 機種共通の読み取り位置を断定しない。数字4桁を維持 |
| SRC-006 / SRC-007 | iPhone・Androidのスマホ内カード案内が公開中 | 対応機種・機能名称は一覧確認を促し、機種を列挙しない |

確認に使用した一次情報は、上表の既存URLを再利用した。画面の完全な現行性とAndroid対応機種の組合せは実機・公式一覧の確認が必要なため、FC-019 / FC-020をREVIEWとして残す。
