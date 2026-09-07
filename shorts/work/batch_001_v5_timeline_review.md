# Shorts探索バッチ001 Visual Redesign v5 timeline review

v5の人間確認用タイムライン。静止画を微細zoom/panで動かさず、意味のあるasset/state切替をhard cutで行う。字幕はv4音声の実時間cueを再利用する。

## Batch metrics

| ID | duration | beats | mean static state | max state | >5 sec | >7 sec | micro motion | score |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Short001 | 28.21秒 | 6 | 4.70秒 | 5.08秒 | 2 | 0 | 0 | 68/100_REVIEW |
| Short002 | 32.24秒 | 7 | 4.61秒 | 4.94秒 | 0 | 0 | 0 | 68/100_REVIEW |
| Short003 | 28.60秒 | 8 | 3.57秒 | 5.51秒 | 2 | 0 | 0 | 68/100_REVIEW |

## Beat timeline

| ID | timestamp | visual beat | asset type | motion | headline | subtitle |
|---|---|---|---|---|---|---|
| Short001 | 0.00〜3.31秒 | A1 | imagegen | hard_cut_static | ChatGPT / 話すだけで使える？ | 文字入力は / 大変ですか？ |
| Short001 | 3.31〜8.22秒 | B1 | real_ui | hard_cut_static | (画面内の公式文言 / なし) | 音声モードなら / 話しかけて使える |
| Short001 | 8.22〜13.14秒 | B2 | official_reference | hard_cut_static | (画面内の公式文言 / なし) | 卵とキャベツで / 聞いてみる |
| Short001 | 13.14〜18.05秒 | B3 | imagegen | hard_cut_static | 今日のごはん、 / 何を作れる？ | 答え始める |
| Short001 | 18.05〜23.13秒 | C1 | imagegen | hard_cut_static | まずは / 話しかけるだけ | 次は写真で聞く |
| Short001 | 23.13〜28.21秒 | C2 | imagegen | hard_cut_static + CTA lockup(180px) | まずは / 話しかけるだけ | 次に困ったときのために / このチャンネルを登録 |
| Short002 | 0.00〜3.33秒 | A1 | imagegen | hard_cut_static | このメール、 / 本物？ | AIに聞く前に / 一呼吸 |
| Short002 | 3.33〜8.27秒 | B1 | renderer | hard_cut_static | (画面内の公式文言 / なし) | 名前や番号は / 先に隠す |
| Short002 | 8.27〜13.22秒 | B2 | renderer | hard_cut_static | (画面内の公式文言 / なし) | AIは整理の補助 / 怪しい点を洗い出す |
| Short002 | 13.22〜18.16秒 | B3 | renderer | hard_cut_static | (画面内の公式文言 / なし) | AIだけで決めない |
| Short002 | 18.16〜22.85秒 | C1 | imagegen | hard_cut_static | 最後は / 公式から確認 | 公式アプリから |
| Short002 | 22.85〜27.55秒 | C2 | imagegen_focus_crop | hard_cut_static | (画面内の公式文言 / なし) | AIは補助 / 確認は公式へ |
| Short002 | 27.55〜32.24秒 | C3 | imagegen | hard_cut_static + CTA lockup(180px) | 最後は / 公式から確認 | 次に困ったときのために / このチャンネルを登録 |
| Short003 | 0.00〜2.89秒 | A1 | imagegen | hard_cut_static | カードを / スマホに？ | スマホに入れると / 何ができる？ |
| Short003 | 2.89〜4.49秒 | B1 | official_image | hard_cut_static | (画面内の公式文言 / なし) | マイナポータル |
| Short003 | 4.49〜6.01秒 | B2 | imagegen | hard_cut_static | (画面内の公式文言 / なし) | コンビニの証明書 |
| Short003 | 6.01〜8.12秒 | B3 | imagegen | hard_cut_static | (画面内の公式文言 / なし) | e-Taxなど |
| Short003 | 8.12〜13.63秒 | B4 | imagegen | hard_cut_static | 保険証として / 使える場合も | 医療機関や薬局で / 使えることも |
| Short003 | 13.63〜18.59秒 | B5 | imagegen_focus_crop | hard_cut_static | (画面内の公式文言 / なし) | 端末で違いあり |
| Short003 | 18.59〜24.04秒 | C1 | imagegen | hard_cut_static | スマホだけで / 全部ではない | 実物カードが / 必要な場面も |
| Short003 | 24.04〜28.59秒 | C2 | imagegen | hard_cut_static + CTA lockup(180px) | スマホだけで / 全部ではない | 次に困ったときのために / このチャンネルを登録 |

## Human review points

- 0〜3秒のhookが、静止画の読みやすさを保ったまま一目で伝わるか。
- hard cutの切替が自然か。微細zoom/panがないことによる読みやすさを確認する。
- Short001のB1実ChatGPT画面、B2公式Voice参照、B3生活sceneがライブVoice画面と誤認されないか。実Voice captureは必要か。
- Short002のB1→B2→B3で、個人情報の該当欄だけが段階的に隠れて見えるか。
- Short003のB1公式マイナポータル、B2コンビニ証明書、B3 e-Taxがそれぞれ一目で具体的に分かるか。抽象rendererへ戻す必要がないか。
- 最後3秒の結論Visual上で、180pxの実チャンネルアイコンとチャンネル名が中央に見えるか。疑似subscribeに見えないか。
- CTAのcanonical音声、ChatGPTの発音、字幕の読みやすさを実音声で確認する。

final、thumbnail確定、upload、publish、scheduleは未実施。

Shorts探索バッチ001 Visual Redesign v5完成。
不要なmicro motionを廃止。
CTA中央化・Short003利用例Visualを具体化。
人間Draft Gate待ち。
