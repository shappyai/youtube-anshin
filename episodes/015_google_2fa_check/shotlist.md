# Episode015 撮影・画面設計

## Phase B / draft_auto_v3 Human Gate 2待ち

- 作成日: 2026-09-08
- 状態: Phase B / draft_auto_v3 Human Gate 2待ち
- 対象: Googleの2段階認証をすでに設定している人
- 実測尺: 5分18.740秒（本編5分06.180秒＋共通CTA音声11.563秒＋余韻。full draft）
- 主媒体: PCブラウザのGoogleアカウント画面
- 補助媒体: Googleからの通知を実演する場合だけ、本人所有の実機を任意で使用

今回は、Episode001のようにGoogleアカウント全体を広く見せない。2段階認証の設定画面の中で、いつもの確認方法、スマホが使えないときの予備、登録されているパスキーを確認する。PCブラウザを主媒体にして、視聴者が画面の場所を理解しやすい大きさで見せる。正式なGoogle UI名は画面上の補足で示す。

## 共通の表示ルール

- 1920×1080、共通Background Systemの「adult_digital_soft_background」を使用する。
- 実画面の全体表示は場所を理解するためだけに2〜4秒とし、説明中は対象の行・ボタンを大きくcropする。
- 実画面はGoogleの本人所有テストアカウントまたは人間確認済みの公式画面だけを使用する。Google UIをAIで再現しない。
- 主要な事実は60px以上、見出しは80px以上、補助情報は52px以上、字幕は72px前後・最小56pxを目安にする。
- 字幕専用の下部安全帯（180px）を確保し、実画面の確認対象を字幕で覆わない。
- 画面上は1画面1メッセージ。URL、確認日、長い出典は画面に出さず、概要欄とsources.mdに保持する。
- バックアップ コードの数字、メールアドレス、電話番号、端末名、QRコードは記録・表示しない。必要な場合は撮影前に隠す。
- 画面の文言や位置がアカウント、OS、GoogleのUI更新で異なる場合は、実画面を優先して台本とshotlistを人間確認する。

## Shot list

| Shot ID | Scene | Device / medium | 画面の役割 | 撮影・表示内容 | Phase B status |
|---|---:|---|---|---|---|
| SHOT-01 | 4 | PCブラウザ | 冒頭と入口 | Googleアカウントの「セキュリティとログイン」にある「Google にログインする方法」から「2 段階認証プロセス」へ進む場所を、実Google UIで示す。 | CAPTURED_OFFICIAL_UI_ENTRY / scene_004 / PII-free crop |
| SHOT-02 | 4〜5 | PCブラウザ | いつもの確認方法 | 正式名称「2段階認証プロセス」の現在の設定内容を大きく見せる。Googleからのメッセージ、確認コード、Google認証システムなど、実際に表示された方法だけを示す。設定のオン・オフ操作はしない。 | CAPTURED_OFFICIAL_UI_ENTRY / scene_004 / no setting change |
| SHOT-03 | 7〜8 | PCブラウザ | スマホが使えないときの予備 | 正式名称「バックアップ コード」の入口行だけを実Google UIで示す。コード一覧は開かず、実コード・QRコード・アカウント情報は保存しない。 | CAPTURED_OFFICIAL_UI_ENTRY / scene_007 / entry only |
| SHOT-04 | 10〜11 | PCブラウザ | 登録されているパスキー | 正式名称「パスキーとセキュリティ キー」の入口行だけを実Google UIで示す。端末名などの個人情報が並ぶ一覧は開かず、後段の説明はカードを使用する。 | CAPTURED_OFFICIAL_UI_ENTRY / scene_010 / entry only |
| SHOT-05 | 12 | テンプレート | まとめ | 3項目を大きく並べる。いつもの確認方法／スマホが使えないときの予備／登録されているパスキー。 | generated in full draft |
| SHOT-06 | postroll | 既存CTA asset | CTA | config/channel_cta.jsonのchannel_common_ctaをcopy-onlyで使用する。動画側に疑似登録ボタンやチャンネルアイコンを描画しない。 | generated in full draft |

## Phase B公式UI確認結果

| Scene | Source | 取得方針 | 注意点 |
|---:|---|---|---|
| 4 | [SRC-001](https://support.google.com/accounts/answer/185839?co=GENIE.Platform%3DDesktop&hl=ja) | Humanログイン済みPCブラウザで「Google にログインする方法」→「2 段階認証プロセス」の入口をcapture | Scene 004は入口の場所説明。表示される確認方法はアカウントにより異なるため、ナレーションで一般化しすぎない。 |
| 7 | [SRC-003](https://support.google.com/accounts/answer/1187538?co=GENIE.Platform%3DDesktop&hl=ja) | Humanログイン済みPCブラウザで「バックアップ コード」の入口行だけをcapture | コード一覧は開いていない。数字・QRコード・アカウント情報は表示・保存・配布しない。 |
| 10 | [SRC-004](https://support.google.com/accounts/answer/13548313?hl=ja) | Humanログイン済みPCブラウザで「パスキーとセキュリティ キー」の入口行だけをcapture | 個別の端末名が並ぶ一覧は開いていない。後段は既存の説明カードを使用し、端末の所有者は視聴者自身が照合する。 |

## Phase Bで実施した確認とHuman Gateへ引き継ぐ点

1. Google公式ヘルプとHumanログイン済みPCブラウザで、「セキュリティとログイン」「Google にログインする方法」「2 段階認証プロセス」「バックアップ コード」「パスキーとセキュリティ キー」の入口を照合済み。
2. Scene 004は入口の場所説明と、実画面で確認できた現在の表示だけを使う。設定のオン・オフ操作はしていない。
3. Scene 007は入口行だけ。コード一覧を開かず、実コードの数字・QRコードは撮影・保存していない。
4. Scene 010は入口行だけ。端末名などの個人情報が並ぶ一覧は開かず、後段は既存fallbackカードを使用する。
5. Googleからの通知を実演する場合、本人所有の端末だけを使い、場所・時刻・端末名などの個人情報を撮影しない。
6. draft_auto_v3のPC表示を65歳以上の視聴者が読める大きさで目視確認し、必要ならHuman Gateでcropを調整する。

## 禁止事項

- AI生成画像でGoogleの設定画面・Googleロゴ・Googleの公式UIを再現しない。
- 実コード、認証通知の承認操作、QRコード、個人のメール・電話番号を動画へ入れない。
- 「2段階認証していても危険」「乗っ取られる」など、公式根拠のない断定を表示・ナレーションしない。
- viewer-facingの表示・字幕・ナレーションに制作内部のブランド文言を入れない。
- thumbnail生成とYouTube uploadは実行しない。full draft生成後にHuman Gateで停止する。
