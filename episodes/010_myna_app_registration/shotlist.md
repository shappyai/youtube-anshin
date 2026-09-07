# Episode 010 Shotlist v2

- episode_id：010
- title：【マイナアプリ】登録方法は？初めて使う人が確認したい手順
- phase：Phase B（draft_v2）
- target_publish_date：2026-09-11（目標日。予約・公開は未実施）
- device decision：スマートフォン実機をPhase Bで照合する。正確なUIはデジタル庁公式画面を優先し、概念説明だけImageGenを使う。
- timing rule：冒頭30秒だけ核心へ早く入り、SCENE-004で1 / 6（25.347秒）、SCENE-005で最初の実操作（28.516秒）へ進む。draft_v2実測基準は本編204.486秒＋CTA15秒。
- privacy rule：氏名、生年月日、顔写真、マイナンバー、カード番号、製造番号、暗証番号、QRコード、通知内の個人情報を含む素材は採用しない。

| Shot | Segment | Section | Device / medium | Visual material | Focal point | Text-safe / display rule | Motion |
|---|---:|---|---|---|---|---|---|
| [SHOT-001] | 1–2 | はじめに | ImageGen概念画像 | assets/generated_ai/scene_001.png | 初めて使う人とスマートフォン | ImageGen内の大見出しのみ。下部180pxは字幕安全帯 | static |
| [SHOT-002] | 3 | はじめに | template図解 | 共通背景＋semantic icon | 利用登録の短い全体像 | 規約から「はじめる」までを大きく表示。制度背景は出さない | static |
| [SHOT-003] | 4–5 | はじめに | template図解 | 共通背景＋preparation icon | 最低限の準備と数字4桁 | 「最新版・画面ロック・本人確認」を大きく表示。数字4桁を明示 | static |
| [SHOT-004] | 6 | 1 / 6 | template section | 共通背景＋section pill | 1 / 6の位置 | 数字と見出しを大きく。ここを最初の1 / 6として固定 | static |
| [SHOT-005] | 7–9 | 1 / 6 | スマートフォン実機（Phase B照合）＋template補助 | 共通背景＋操作手順 | アプリを開き、規約を確認して次へ進む | segment 007から最初の実操作。字幕安全帯を空ける | static |
| [SHOT-006] | 10 | 2 / 6 | template section | 共通背景＋section pill | 2 / 6の位置 | 「利用登録を開始」を大きく表示 | static |
| [SHOT-007] | 11–12 | 2 / 6 | 公式画面（Phase Bで実機照合） | assets/official/official_screen_register_start.png | 利用登録をはじめる操作箇所 | 公式画面を拡大し、操作箇所を見せる。AI再現は禁止 | very slow zoom |
| [SHOT-008] | 13 | 3 / 6 | template section | 共通背景＋section pill | 3 / 6の位置 | 「通知を確認」を大きく表示 | static |
| [SHOT-009] | 14–15 | 3 / 6 | 公式画面（Phase Bで実機照合） | assets/official/official_screen_register_agreement.png | 通知を受け取るかの選択 | 原画のUIは改変せず、必要部分だけ拡大 | very slow zoom |
| [SHOT-010] | 16 | 4 / 6 | template section | 共通背景＋section pill | 4 / 6の位置 | 「画面ロックを確認」を大きく表示 | static |
| [SHOT-011] | 17–18 | 4 / 6 | 公式画面（Phase Bで実機照合） | assets/official/official_screen_register_device_lock.png | 端末ロック許可 | 公式画面の確認箇所を拡大。架空UIを描かない | very slow zoom |
| [SHOT-012] | 19–21 | 5 / 6 | template比較 | 共通背景＋compare layout | アプリ本体とスマホ内カードの条件差 | iOS 16.4以上、Android 11以上、NFCを分けて表示。冒頭には戻さない | static |
| [SHOT-013] | 22–23 | 5 / 6 | template list | 共通背景＋semantic icon | 本人認証3ルート | 実物カード・iPhone・Androidを3行で大きく表示。詳細条件は音声 | static |
| [SHOT-014] | 24 | 5 / 6 | template section | 共通背景＋section pill | 本人認証を選ぶ位置 | 実物カード・iPhone・Androidを同じ手順に見せない | static |
| [SHOT-015] | 25–27 | 5 / 6 | 公式画面（Phase Bで実機照合） | assets/official/official_register_card_passcode_crop.png | 数字4桁の入力欄 | 暗証番号そのものは表示しない。公式UIの入力欄をcrop拡大 | very slow zoom |
| [SHOT-016] | 28–29 | 5 / 6 | 公式画面（Phase Bで実機照合） | assets/official/official_register_card_read_crop.png | カード読み取り開始と待機 | 「スマホの背面をカードに重ねる」を大きく。QRや個人情報なし | very slow zoom |
| [SHOT-017] | 30 | 5 / 6 | ImageGen概念画像 | assets/generated_ai/scene_017.png | スマートフォンとカードを重ねる動作 | 画像内にUI・ロゴ・文字を置かない。公式画面の代替にしない | very slow zoom |
| [SHOT-018] | 31–32 | 5 / 6 | 公式画面（Phase Bで実機照合） | assets/official/official_screen_register_biometric.png | スマホ内カードの生体認証 | 公式画面をcrop拡大。iPhoneとAndroidは別手順と音声で明示 | very slow zoom |
| [SHOT-019] | 33–40 | 6 / 6 | template summary | 共通背景＋summary cards | 登録完了までの順番と困ったときの導線 | 完了画面は未採用。関連動画への案内は一般表現で表示し、内部routingは公開設定側で確定 | static |
| [SHOT-020] | 41 | まとめ | ImageGen概念画像 | assets/generated_ai/scene_020.png | 落ち着いて順番を確認する人物 | ImageGen内の短い見出しのみ。右側のEnd Screen reserved領域は空ける | very slow zoom |

## Human gate

1. 冒頭の実時間が30秒以内に収まり、SCENE-004で1 / 6、SCENE-005で実操作へ入ることを確認する。
2. 公式画面の現在のボタン名・順番と実機を照合する。
3. 採用端末とカードでNFC読み取り位置を確認し、機種依存の説明にする。
4. SCENE-015の4桁入力、SCENE-016のカード読み取り、SCENE-018の生体認証が65歳以上でもTVで読めることを確認する。
5. raw素材を含めて個人情報がなく、ImageGenの文字が完全一致することを確認する。

## Deferred

VOICEVOX、字幕、draft_v2までPhase Bで完了。thumbnail生成、finalize、YouTube予約・公開は人間全編確認後に行う。
