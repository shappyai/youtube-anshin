# Episode 011 登録者獲得実験 v2 / Analytics Plan

## 位置づけ

- experiment：`registration_conversion_v2`
- comparison_episode：`010`
- 比較方法：テーマが異なるため、厳密なA/B testではなく「中盤CTAが有望かを見る準実験」とする。
- 010：story_intro=yes / reason_to_return_cta=yes / midroll_subscribe_cta=no
- 011：story_intro=yes / reason_to_return_cta=yes / midroll_subscribe_cta=yes
- 追加変数：中盤CTAの有無だけに近づける。テーマ、3つの確認、公式情報、シニア向け可読性は変更しない。

## CTA計画

- 挿入位置：segment 012の直後、segment 014「2つ目です」の直前。
- Phase B実測位置：01:08.822〜01:15.518（segment 012直後、segment 014直前）。
- narration：`「これ、本物？」は公式情報で確認します。必要なら登録しておいてください。`
- 音声実測：6.496秒。上限7秒をPASS。
- Visual：SCENE-019の静かな1scene。`これ、本物？` / `公式情報で確認` / `次に困ったときのために` を表示する。
- 禁止：fake subscribe button、赤い登録演出、恐怖語、派手な独立登録画面。
- CTA直後：segment 014の「2つ目です。個人情報や暗証番号を伝えません。」へ即時復帰する。

## 終了CTA

Episode010のdraft_v1で実際に使われたregistration_conversion_v1 CTAを、画面・音声ともそのままreuseする。Phase BでEpisode011へコピーし、SHAとcanonical textを照合済み。

確認メモ：2026-09-06にEpisode010のdraft_v1/draft_v2、`work/cta_registration_conversion_v1.json`、画面、音声、media manifestを照合した。実使用のcanonical textは次のとおり。Episode010は変更していない。

> スマホやパソコンの「これ、どうすればいい？」を、公式情報で分かりやすく確認しています。次に困ったときのために、チャンネル登録しておいてください。

End Screenの実登録要素はYouTube Studio側で配置する。動画側に疑似登録アイコンは描画しない。

## 公開後に記録するKPI

- `views`
- `unique_viewers`
- `subscribers_gained`
- `subscriber_conversion_rate = subscribers_gained / unique_viewers`
- `subscribers_per_1000_unique_viewers = subscribers_gained / unique_viewers * 1000`
- `first_30_sec_retention`
- `midroll_cta_retention_before`
- `midroll_cta_retention_during`
- `midroll_cta_retention_after`
- `average_percentage_viewed`
- `average_view_duration`
- `end_screen_ctr`
- `returning_viewers`
- `browse_home_percent`
- `search_percent`
- `age_65plus_percent`
- `tv_percent`

## Retention確認窓

- CTA直前：CTA開始の30秒前〜開始時刻
- CTA区間：CTA開始〜終了
- CTA後30秒：CTA終了〜30秒後
- 判定：登録者数だけで成功とせず、`subscriber_conversion_rate` が有望で、CTA区間だけの目立つ急落がないことを重視する。
- CTA区間だけ急落した場合：登録理由の文言、画面の長さ、置き場所を再設計する。

## 実績記録欄

| 項目 | Episode 010 | Episode 011 | 備考 |
|---|---:|---:|---|
| views | 未入力 | 未入力 | YouTube Analyticsから転記 |
| unique_viewers | 未入力 | 未入力 | 同上 |
| subscribers_gained | 未入力 | 未入力 | 同上 |
| subscriber_conversion_rate | 未入力 | 未入力 | subscribers_gained / unique_viewers |
| first_30_sec_retention | 未入力 | 未入力 | 冒頭micro storyの確認 |
| midroll_cta_retention_before | — | 未入力 | 011のみ |
| midroll_cta_retention_during | — | 未入力 | 011のみ |
| midroll_cta_retention_after | — | 未入力 | 011のみ |
| average_percentage_viewed | 未入力 | 未入力 | テーマ差を注記 |
| average_view_duration | 未入力 | 未入力 | テーマ差を注記 |
| end_screen_ctr | 未入力 | 未入力 | 終了CTAを揃えて確認 |
| returning_viewers | 未入力 | 未入力 | reason-to-returnの確認 |
| browse_home_percent | 未入力 | 未入力 | 流入比較 |
| search_percent | 未入力 | 未入力 | 流入比較 |
| age_65plus_percent | 未入力 | 未入力 | 視聴者属性 |
| tv_percent | 未入力 | 未入力 | デバイス属性 |

## 注意

YouTube Analyticsの実測値が入るまで、登録転換率やRetentionを推測しない。010と011の差は中盤CTAだけの純粋な因果効果とは断定しない。
