# Episode 010 制作ブリーフ

## 基本情報

- エピソード：010
- slug：myna_app_registration
- 制作基準日：2026-09-06
- 想定公開日：2026-09-06（公開希望日として記録。予約設定はしない）
- selected title：【マイナアプリ】登録方法は？初めて使う人が確認したい手順
- 判定：PRODUCTION GO（調査スコア78/100から人間判断で制作進行）
- 今回の停止位置：final確定後、ChatGPTサムネイル受領待ち
- 追加実験：registration_conversion_v1（micro story＋reason-to-return CTA）

## 役割

- Episode 002：マイナアプリで何が変わったか
- Episode 010：マイナアプリを初めて使うための利用登録
- Episode 007：ログインできない・読み取れない等の困ったとき
- 回遊：002 → 010 → 007

## 視聴者

50〜70代、特に65歳以上。TV視聴を想定し、画面全体を長時間見せず、操作箇所を大きく見せる。専門用語は直後に日常語へ言い換える。

## 扱う範囲

マイナアプリの利用登録を、デジタル庁の公式6段階に沿って説明する。本人認証は実物のマイナンバーカードを使う成功ルートを主役にし、iPhoneのマイナンバーカードとAndroidスマートフォンの電子証明書は別ルートとして短く示す。

## 扱わない範囲

マイナポータルへのログイン、マイナポータルの利用者登録、スマホ用電子証明書の登録、健康保険証利用登録、機種変更、読み取り失敗、暗証番号ロック、エラーコードの詳細は本編に混ぜない。困ったときはEpisode 007へ送る。

## 媒体

- 主媒体候補：スマートフォン実機
- 正確なUI：デジタル庁公式画面素材
- 概念説明：ImageGenの完成背景
- 画面ロック、生体認証、カード読み取りの実機確認：公開前に人間が確認する

## Phase Aの成果物

41 narration segments、20 scenes、公式UI 6 scenes、ImageGen 3 scenes、冒頭30秒v2、Fact Check、scene contact sheet v2、thumbnail brief、Visual QAを作成した。

## Registration conversion experiment

- 冒頭はSCENE-001画像を変えず、「マイナアプリを入れて、開いてみた。でも、最初に何をすればいい？」を字幕・narrationで追加した。
- 解決表現は「ここまで来れば、初めて使うときの利用登録は完了です。」へ変更した。
- CTAは`config/channel_cta.json`を変更せず、Episode 010専用overrideを使用する。
- `subscribers_gained / unique_viewers`を正式な登録転換率とし、1,000 unique viewersあたりの値も記録する。
- `registered / not subscribed`比率は登録転換率とは呼ばず、別指標として扱う。
- 中盤CTAは追加しない。詳細は`work/analytics_plan.md`。

## Phase Bで実施済み・次工程へ持ち越すもの

VOICEVOX音声、字幕タイミング、captions.srt、draft_v2動画は作成済み。draft_v1は比較用に保持する。draft_v2の人間全編確認を承認し、final動画をcopy-onlyで確定した。thumbnail画像、YouTube公開・予約設定は持ち越す。
