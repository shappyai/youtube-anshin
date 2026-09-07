# Episode 010 analytics plan — registration_conversion_v1

作成日: 2026-09-06  
対象: Episode 010「マイナアプリを初めて使う人向け 利用登録の手順」

## 実験の目的

説明動画の「分かったので、そのまま離脱」を減らし、次に困ったときの確認先としてチャンネルを残してもらえるかを確認する。Visual Gate v2、20scene構成、主要Fact、タイトル、サムネイルは変更しない。

## 実験設定

- experiment: `registration_conversion_v1`
- `story_intro=true`
- `reason_to_return_cta=true`
- `midroll_subscribe_cta=false`
- CTA: Episode 010専用override `work/cta_registration_conversion_v1.json`
- CTA画面: 「次に困ったときのために」／「チャンネル登録しておいてください」
- CTA音声: 本文は専用variantのcanonical narration、画面は短い表示文。終了画面は約15秒。
- `config/channel_cta.json`は変更しない。結果が良い場合もcanonical化は人間判断とする。

## 仮説

視聴者を架空の体験談の主人公にせず、「アプリを入れて開いたが、最初に何をすればよいか分からない」という日常の困りごとを冒頭で短く提示する。その後、実操作で一緒に確認し、利用登録完了を明示する。終了時は「応援してください」ではなく、「次に困ったときのために残しておく」という登録理由を提示する。

## 最重要KPI

正式な登録転換率は次で計算する。

`subscriber_conversion_rate = subscribers_gained / unique_viewers`

比較表示用の派生値は次とする。

`subscribers_per_1000_unique_viewers = subscriber_conversion_rate * 1000`

`unique_viewers`がまだ取得できない期間は、暫定値として `subscribers_gained / views` を別欄に記録する。暫定値を正式な登録転換率とは呼ばず、後日unique viewersが得られたら正式値へ更新する。

## 取得する指標

同じ公開後経過時間で、24時間・7日・28日のスナップショットを記録する。

- views
- unique viewers
- subscribers gained
- subscriber conversion rate
- subscribers per 1,000 unique viewers
- first 30 sec retention
- average percentage viewed
- average view duration
- End Screen CTR
- returning viewers
- Browse/Home %
- Search %
- 65+ %
- TV %
- registered / not subscribed比率（参考。登録転換率とは呼ばない）

## 比較

- Episode 002：マイナアプリの変更点。既存の実用解説として基準値を確認する。
- Episode 008：直近のシニア向け実用解説として、背景・字幕・従来CTA運用と比較する。
- Episode 009：直近の実用解説として、タイトル・流入・公開時期の差を注記する。

比較表には公開曜日、公開後経過時間、タイトル／サムネイル、流入元、テーマ差を併記する。差分だけで因果を断定せず、Episode 011以降の仮説候補として人間が判断する。

## 記録フォーマット

各スナップショットで、次のraw値と計算値を同じ行に残す。

| snapshot | views | unique_viewers | subscribers_gained | subscriber_conversion_rate | subscribers_per_1000_unique_viewers | first_30s_retention | avg_percentage_viewed | avg_view_duration | end_screen_ctr | returning_viewers | browse_home_pct | search_pct | age_65_plus_pct | tv_pct | not_subscribed_pct | notes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 24h | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | 公開後に記録 |
| 7d | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | 公開後に記録 |
| 28d | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | 公開後に記録 |

## QA記録

- `micro_story_intro`: PASS（台詞のみ。SCENE-001画像は既存のまま）
- `first_action_seconds <= 30`: 差分反映後のVOICEVOX実測で確定
- `problem_to_solution_clear`: PASS（冒頭の迷い→一緒に確認→利用登録完了）
- `reason_to_return_present`: PASS（専用CTAに明示）
- `duplicate_cta`: 0
- `midroll_cta`: 0
- `cta_audio_duration <= 15 sec`: 再生成後に実測
- `cta_full_text_visible`: PASS（短い表示文の欠落なし）
- `end_screen_reserved`: PASS

## 恒久化候補

`micro_story_explainer`は今回時点ではproposed ruleとする。Episode 010の結果だけで共通ルールや`config/channel_cta.json`を自動変更しない。複数Episodeの比較と人間判断を経て、必要ならEpisode 011以降へ反映する。

`internal_episode_id_not_viewer_facing`も今回の修正で提案する。repo内部のEpisode番号は視聴者向けのnarration・subtitle・scene text・CTA・descriptionに表示せず、「関連動画」「次の動画」「こちらの確認動画」などの一般表現を使う。canonical化は人間判断待ちとし、Episode 002・007・010などの内部番号をYouTube向け文字列へ自動展開しない。

## Finalized before thumbnail

- registration_conversion_v1の設定を固定：story_intro=true、reason_to_return_cta=true、midroll_subscribe_cta=false。
- 公開後に記録するKPI（views、unique_viewers、subscribers_gained、subscriber_conversion_rate、subscribers_per_1000_unique_viewers、first_30_sec_retention、average_percentage_viewed、average_view_duration、end_screen_ctr、returning_viewers、browse_home_percent、search_percent、age_65plus_percent、tv_percent）は変更しない。
- サムネイル生成・YouTube upload・予約公開はこの段階では実施しない。
