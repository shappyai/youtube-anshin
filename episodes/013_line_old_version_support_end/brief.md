# Episode 013 brief — LINE旧バージョン・古いOSのサポート終了

## 制作判断

- Episode: 013
- Slug: `line_old_version_support_end`
- 基準日: 2026-09-06
- Phase: **Phase B / Visual Gate v3 machine QA PASS、human review待ち**
- 制作判定: **real UI 7 / 7 + SCENE-005 official-fact renderer → HUMAN_REVIEW_REQUIRED**
- Working title: **【LINE】11月に使えなくなる？今のスマホで確認したい3つ**
- 想定尺: 6分50秒〜7分50秒（第一目標 約7分20秒）
- 形式: problem_solver_medium / micro story
- 媒体: iPhone実機＋Android Emulator＋LINE公式ヘルプに基づくテンプレート図解
- 公式UI: real UI 7scene。SCENE-005はLINE公式Fact rendererで、LINE公式UIの再現画像は生成しない
- ナレーター: VOICEVOX「剣崎雌雄」ノーマル（74segment実測生成済み。発音の人間聴取レビューは継続）
- 終了CTA: Episode011 / 012で人間承認・実使用された `registration_conversion_v1` を画面・音声・canonical textで完全reuse。15秒postrollを1回だけ使用する。
- Phase A承認後の修正: SCENE-004 / 008 / 012のsemantic iconを小〜中サイズへ縮小、SCENE-018の見出しを「ケースA　今回は対応不要」へ変更。

## 視聴者への約束

「11月からLINEが使えなくなる」という情報を見た人に、全員ではないことを最初に伝える。今のスマホで、次の3つを順に確認できる動画にする。

1. LINEアプリのバージョン
2. iPhone／AndroidのOSバージョン
3. LINEとOSを更新できるか

結論は「古いLINEやOSが対象。まず自分の状態を確認し、更新できる人は更新する。更新できない場合だけ、公式案内に沿って別の対応を考える」。最初から買い替えを勧めない。

## 最新一次情報の要約

LINE公式ヘルプは、2026年11月上旬に、iOS／iPadOSではLINE 14.6.3未満、AndroidではLINE 14.4.6未満のサポートを終了する予定と案内している。LINE全体の終了ではない。

- iOS／iPadOS 15.0以上、Android 8.0以上では、該当OS上でLINEをそれぞれ14.6.3以上／14.4.6以上へ更新する案内。
- iOS／iPadOS 14.8.1以下、Android 7.1.2以下では、OSを15.0以上／8.0以上へ更新してからLINEを更新する手順が示されている。
- OSまたはLINEを更新できない場合は、LINE公式は動作環境を満たす別端末での利用を検討するよう案内している。
- LINEの最新版を利用できる推奨環境（iOS 18.0以上／Android 11.0以上）と、今回の11月対応で確認する下限は別の情報として整理する。

## 冒頭Retention設計

- `problem_visible`: 4秒以内。11月に使えなくなるという不安をそのまま提示。
- `core_answer`: 10〜15秒。全員ではなく、古いLINE／OSが対象だと先に回答。
- `first_check_action`: 22〜25秒。LINEを開き、バージョン確認へ入る。
- 初期フレーズで「全員」「買い替え」を断定しない。

## 既存Episodeとの境界

- Episode 003（LINE画面リニューアル）: 今回はUI変更の説明をしない。LINEアプリのバージョン確認だけを扱う。
- Episode 006（LINEトーク履歴バックアップ）: 機種変更になる場合のバックアップ・引き継ぎを1sceneで注意喚起するだけ。詳細手順、PIN、写真・動画の仕様は再説明しない。
- Episode 012（SMS・メール確認）: 更新通知を装った詐欺の話は本編の主題にしない。公式ストアから更新するという基本だけを扱う。

## 中盤CTA

なし。6〜8分の問題解決動画で、3つの確認とケース分岐を優先する。CTAはregistration_conversion_v1のpostrollのみとし、途中で登録を求めて操作説明を止めない。

## Apple Event後の扱い

2026-09-10のApple Event後、古いiPhoneへの影響や公開タイミングを人間が再判定する。Phase Aは止めずに進めるが、Apple発表で本テーマの優先順位が変わる場合は公開順を変更できるよう、公開日は固定しない。

## サムネイル

画像生成は行わず、ChatGPT側で別途制作する前提。案は `work/thumbnail_brief.md` に記録する。
