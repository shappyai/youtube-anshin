# Episode 012 brief

- Episode: 012
- Slug: phishing_message_safety
- Working title: 【詐欺メール】本物そっくりでも見分けなくていい？安全に確認する5つの場面
- Format experiment: `long_form_watchtime_v1`
- Pillar: protect
- Target viewer: 50〜70代、特に65歳以上。スマホやメールは使うが、届いた通知をその場で判断することに不安がある人。テレビ視聴を想定し、情報文字は44px未満を使わない。
- Viewer problem: いつも利用する会社や公的機関の名前で、支払い・再配達・不正利用・未払いを知らせるSMSやメールが届く。見た目だけで本物か判断しようとして、急いでリンクを押しそうになる。
- Promise: メール・SMSのリンクから入らず、自分で公式アプリや公式サイトを開いて確認する手順を、5つの生活場面で繰り返し使える形にする。
- Why now: 国民生活センターが2026年9月3日に、普段使うアプリ名で届いたメールから支払い情報を更新し、その後約20万円の利用通知を受けた80歳代の相談例を公表。公的機関・警察庁・事業者も同じ安全行動を案内している。
- Search intent: 「これ本物？」「支払い方法を更新してください」「再配達はこちら」「カード利用確認」「料金未払い SMS」「国税庁 SMS」など、届いたメッセージへの対処を知りたい。
- Browse hook: いつもの会社の名前とロゴが出ていても、本物かどうかをメールだけで当てなくてよい、という安心できる結論。
- Required real-device demos: 実機画面が必要な場面はなく、Phase Bではテストアカウントの個人情報を使わず、公式公開資料クロップと意味図解で確認手順を成立させた。
- Planned official visuals: 7 scene slots（5 source groups）。国民生活センター、フィッシング対策協議会、JCB、ソフトバンク、国税庁の公式公開資料クロップ5点と、公式アプリを自分で開く／安全な3入口の意味図解2点を採用。AIで公式UIを再現しない。
- Do not claim: すべてのSMS・メールが偽物、会社名・ロゴ・日本語・鍵マーク・送信元表示だけで判定できる、リンクを開いただけで必ず被害が出る、すべての携帯会社や行政機関の通知方法が同じ、とは言わない。
- Thumbnail status: `HUMAN_PROVIDED_QA_PASS`。ユーザー提供画像を正式採用し、原本を`assets/thumbnail/thumbnail_source.png`へ保持、公開用を1280×720へ内容変更なしで正規化した。
- Target length: 第一目標9〜11分、許容8〜12分。水増し区間を入れない。

## Human gates

1. テーマ・台本・一次情報（承認済み）
2. scene contact sheetとImageGen-native文字確認（Visual Gate v2承認済み）
3. full draft（人間全編確認済み、senior_readability=PASS）
4. thumbnail / publish（サムネイル確認済み・予約公開工程）

## Production boundary

Phase Aは完了し、Visual Gate v2の人間承認を反映した。Phase Bでは公式素材・意味図解、VOICEVOX、実測字幕、`output/draft_v4.mp4`まで制作済み。ユーザー修正版030.wavを反映し、`output/final.mp4`をcopy-onlyで確定した。ユーザー提供サムネイルを内容変更なしで正規化・QA済み。YouTube upload / scheduleを実施し、End Screen設定はYouTube Studioでの人間作業として残す。
