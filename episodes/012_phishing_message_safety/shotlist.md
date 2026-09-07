# Episode 012 shot list（Phase B draft_v4 / final copy-only）

## Media decision（撮影前に決定）

主媒体はスマホ。ただし、正確な公式情報を読ませる場面は、読ませやすさを優先して公式公開ページのPCブラウザ素材または正確な短い引用を使う。実在アプリの画面が不要な場面は意味図解にする。SCENE-006 / 011 / 017 / 021 / 025は架空のSMS・メール画面を再現せず、説明用のsemantic sceneとして制作した。Phase Bでは公式公開資料・正確な引用・意味図解でdraft_v4を制作した。

| ID | Device | Action | Expected screen | Privacy check | Filename / phase |
|---|---|---|---|---|---|
| SHOT-01 | template（実機撮影なし） | 支払い更新・再配達・カード確認・未払い・公的通知で生じる判断ポイントを説明 | 架空画面を再現せず、意味図解と短い説明を大きく表示 | 実在の会社名・ロゴ・URL・電話番号・QR・氏名・番号を使わない | `work/rendered_final_scenes/scene_006.png` ほか / draft_v4 |
| SHOT-02 | semantic operation visual | メールを閉じ、公式アプリを自分で開く手順を示す | `SCENE-008`の「メールを閉じる」→「自分で公式アプリを開く」意味図解 | 個人情報なし。実在アプリ画面は再現しない | `work/rendered_final_scenes/scene_008.png` / 採用済み |
| SHOT-03 | PCブラウザ公式公開資料 | SMSとは別の入口で宅配の案内を確認する | `SCENE-012`のフィッシング対策協議会公式図＋`SCENE-013`の安全な3入口意味図解 | 公式公開資料のみ。個人情報なし | `assets/official/scene_012_antiphishing_delivery_flow.png` / 採用済み |
| SHOT-04 | PCブラウザ公式公開資料 | カード会社の公式注意喚起から確認する | `SCENE-018`のJCB公式警告イラストを大きく表示 | 公式公開資料のみ。カード番号等なし | `assets/official/scene_018_jcb_warning.png` / 採用済み |
| SHOT-05 | PCブラウザ公式公開資料 | 携帯会社の公式案内で料金を確認する | `SCENE-022`のソフトバンク公式警告部分だけをクロップ | 宛先・金額・日付・契約情報を表示しない | `assets/official/scene_022_softbank_warning.png` / 採用済み |
| SHOT-06 | PCブラウザ公式公開資料 | 公的機関の公式サイトを自分で開き、案内を確認する | `SCENE-026`の国税庁公式注意喚起バナーを1点大きく表示 | 個人情報なし。URL全文・確認日は画面に出さずmetadataへ | `assets/official/scene_026_nta_warning.png` / 採用済み |
| SHOT-07 | template | リンクを開いた後の対応を段階カードで整理 | 開いただけ／ID・パスワード／カード／送金・口座／アプリ導入を別カード表示 | 実在の窓口番号・URLは画面に入れず、概要欄の公式情報へ誘導 | `work/rendered_final_scenes/scene_029.png` / draft_v4 |

## Visual capture rules

- 全体画面は場所を理解させるための2〜4秒。内容を読ませる箇所は必ず大きくcropする。
- 公式UIは公式sourceまたは自分のcaptureだけを使用し、ImageGenでは作らない。
- 架空SMS・メール画面を実際に再現するsceneだけ、`再現イメージ`を44px以上で表示する。今回の5sceneは説明用semantic sceneなので、ラベルも架空UIも描画しない。
- 公式画面を実機で撮影できない場合は、確認済みの公式公開資料クロップまたは意味図解に切り替え、未確認の画面を作らない。今回の対象7sceneはすべてこの条件を満たす。
- 下部180pxは字幕安全帯として空ける。文字はheadline 88〜120px、main 64〜80px、secondary 52px以上を目安にする。
- draft_v4の本編タイムラインはSCENE-030（segments 076〜079）で終了し、SCENE-031 / segment080は除外した。Episode011の実使用CTAは本編直後のpostrollへ1回だけ直接連結する。segment030はユーザー修正版のhuman audio overrideを使用し、finalはcopy-onlyで確定済み。
