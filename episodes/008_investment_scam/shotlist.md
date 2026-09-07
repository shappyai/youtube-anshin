# Shotlist — Episode 008（その投資広告、本物？）

- Device方針: **実機/実アプリの新規録画はなし**。本編の主役は「確認の考え方」であり、金融庁検索サイトのPCブラウザcaptureは、draftの可読性を優先して追加しない判断とした。それ以外はGPT画像（imagegen_native）＋テンプレート（Codex renderer）で構成し、**実在LINE・実在アプリ等のUIはAIで再現・偽造しない**。
- 全scene: 1920×1080・下部180px字幕安全領域・TV視聴前提（headline ≥80px・main fact ≥60px・secondary ≥52px・出典短形 ≥44px・字幕60〜72px）。

| SCENE | 内容 | タイプ | 表示テキスト（大きさ区分） | 備考 |
|---|---|---|---|---|
| SCENE-001 | オープニング: 広告→LINE誘導→「本物?」 | GPT画像（imagegen_native） | 大見出し「その投資広告、本物？」＋補助「LINEに誘導されたら、振り込む前に、3つ確認」 | 実在人物を描かない。スマホ＋広告＋シルエット。 |
| SCENE-002 | 被害増加の案内 | template（hero＋icon campaign） | 大「高額な被害が、増えています」＋小「こうした流れから、投資詐欺に（警察庁ほか）」 | 数字は出さない（次のsceneへ）。 |
| SCENE-003 | 3つの確認の一覧 | template（list） | 大「今日確認する、3つ」＋3項目 | タイトル・冒頭・まとめで完全一致。 |
| SCENE-004 | 1/3セクション扉 | GPT画像（imagegen_native） | 大「広告の有名人を、そのまま信用しない」＋小「まずは、そのまま信じない」 | 1/3 pillはCodex overlay。 |
| SCENE-005 | 最新の数字（1画面に集中） | template（hero＋icon account_balance） | 大「6,566件」「およそ881億円」＋小「SNS型投資詐欺・今年7月末までの暫定値（警察庁）」＋メイン「前年の同じ時期より、7割以上、増えています」 | 1日4.4億円・60代最多はナレーション中心。 |
| SCENE-006 | なりすまし広告の概念 | GPT画像（imagegen_native） | 大「本人が、すすめているとは、限らない」＋小「写真や動画を無断で使った広告が増加（警察庁）」 | 顔はシルエット・モザイク表現。 |
| SCENE-007 | 「必ずもうかる」注意 | template（caution＋icon warning） | 大「「必ずもうかる」「あなただけ」は、注意の言葉」＋小「そういう言葉が出たら、まず、疑いましょう」 | SOS47チェックポイント。 |
| SCENE-008 | 2/3セクション扉 | GPT画像（imagegen_native） | 大「LINEに誘導されたら、一度、止まる」＋小「グループに移る前に、確認」 | 2/3 pillはCodex overlay。 |
| SCENE-009 | LINE誘導9割 | template（hero＋icon forum） | 大「LINEに誘導されるのは、およそ9割」＋小「広告やメッセージで接触した後（令和7年・警察庁）」 | 集計範囲つき表示。 |
| SCENE-010 | サクラ・焦らす言葉 | template（caution＋icon groups） | 大「グループには、サクラが、いることも」＋小「もうかったふりをする書き込みに、ご用心」 | |
| SCENE-011 | 「相談しないで」＝詐欺のサイン | template（caution＋icon group_off） | 大「「相談しないで」は、詐欺のサイン」＋小「家族や銀行に、言わないよう、仕向けられたら」 | LINEヤフー公式。 |
| SCENE-012 | LINEは危険ではない（安心） | template（visual_text＋icon forum） | 大「LINEは、危険ではありません」＋小「知らない人と、お金の話でつながるのが、危険」 | |
| SCENE-013 | 3/3セクション扉 | GPT画像（imagegen_native） | 大「送金する前に、登録と振込先を確認」＋小「この2つが、最後の確認」 | 3/3 pillはCodex overlay。 |
| SCENE-014 | 会社の登録確認 | template（hero＋icon verified_user） | 大「会社の登録を、確認する」＋小「株・FX・暗号資産は、国の登録が必要（金融庁）」＋メイン「登録がない会社には、お金を振り込まない」 | URLは画面に出さない（説明欄へ）。 |
| SCENE-015 | 振込先の2チェック（比較） | template（compare 2カラム） | 大「振込先に、不審な点はありませんか」＋左「個人名義の口座」右「振込のたびに、口座が変わる」 | 2項目の左右比較。 |
| SCENE-016 | 困ったら: 送金しない・記録を残す・相談する | template（list） | 大「まず、これ以上、送金しない」＋2項目 | |
| SCENE-017 | 相談先3つ | template（list） | 大「困ったら、相談を」＋「#9110 警察相談専用電話」「188 消費者ホットライン」「0570-050588 金融庁・投資詐欺の相談ダイヤル」 | 番号を大きく。受付時間はナレーション/description。 |
| SCENE-018 | まとめ（3つ再掲） | template（list） | 大「まとめ」＋3項目 | 冒頭と完全一致。 |
| CTA | 共通CTA（channel_common_cta） | 既存アセット再利用 | 説明・CTA本文 | End Screen右40〜45%はreserved。ロゴ・疑似登録アイコン描画なし。 |

## official UI（Phase B判断済み）
- 金融庁「金融事業者一括検索機能」https://search.fsa.go.jp/ のPCブラウザcaptureは今回のdraftには追加しない。テンプレートSCENE-014の短い出典表示で確認先を伝え、URLは説明欄へ置く。
- 公式captureで情報量が増えるより、65歳以上でも読める大きな説明を維持することを優先した。
- 警察庁・国民生活センター等の画面は本編では使わない（数字はテンプレートで表現）。

## 撮影・生成メモ
- GPT画像5枚（IMG-001〜005）は「1 scene=1 image=1 path」で生成。imagegen_native文字はexact text QA必須。FAIL時は1回だけ再生成→2回目はpil_overlayへfallback。
- 有名人の顔・実在サービスUI・QRコード・口座番号・個人情報は一切生成しない。
