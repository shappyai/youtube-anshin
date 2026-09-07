# Episode 005 Phase B前半 Audio QA report（再評価）

確認日: 2026-09-01（JST）  
対象: `episodes/005_google_photos_delete/`  
担当範囲: 65 narration segments のVOICEVOX設定・文境界・数字・記号・固有名詞・発音辞書・preflight確認  

## 結論

**総合判定: pronunciation preflight PASS / full audio QA STOP（依頼された停止位置）**

65/65件のlive `audio_query`を、生成経路と同じeffective textで再実行した。話者・スタイル・速度設定は要求値と一致し、unresolved pronunciation REVIEWは0件になった。seg046だけに`方 → かた`のsegment overrideを適用し、global dictionaryは変更していない。

seg046の短いpreview WAVは生成済みで、query kanaは`オツカイノ/カタ`（「おつかいのかた」）。本編65件のWAV、連結音声、実尺字幕は依頼どおり未生成なので、音質・アクセント・全体同期のAudio QAは後段に残す。

## Phase B前半残課題の再評価

| 項目 | 判定 | 根拠 |
|---|---|---|
| 65/65 pronunciation preflight | **PASS** | live query 65/65、設定不一致0、unresolved pronunciation REVIEW 0 |
| seg046 | **PASS（TTS候補）** | effective inputは「お使いのかた」。表示字幕「お使いの方」は変更なし |
| 他の文脈候補7件 | **PASS（機械確認）** | `今日→キョオ`、`仕方→シカタ`、`開く/開いて→ヒラク/ヒライテ`、`両方→リョオホオ`。不自然な音列は検出なし |
| global pronunciation dictionary | **PASS** | `方`は追加なし。既存の`右上→みぎうえ`のみ再利用 |
| seg046 preview WAV | **PASS（生成確認）** | `work/phase_b_review/audio/seg046_otsukai_no_kata_preview.wav`、5.056秒、24kHz |
| full audio QA | **STOP** | 本編WAV 0/65。依頼どおり本編VOICEVOX生成は未実施 |

## 判定サマリー

| 確認項目 | 判定 | 結果・根拠 |
|---|---|---|
| narration inventory | PASS | `episode.json`のnarration_segmentsは65件、IDは1〜65で連番、空文なし |
| script ↔ JSON | PASS | `script.md`のナレーション行65件とJSONの65件を完全一致で照合、差分0件 |
| 1文1segment | PASS | 65件すべて1行・終端句読点1個。`episode.json`のsubtitleも65件で各segmentに1件 |
| target voice | PASS | VOICEVOX / 剣崎雌雄 / ノーマル / speedScale 1.00 / intonationScale 1.00 / pitchScale 0.00 |
| live engine | PASS | `/version`は0.25.2。`/speakers`で剣崎雌雄・ノーマルを解決しstyle_id=21 |
| audio_query | PASS | 001〜065を65/65件取得、エラー0、kana空欄0。全queryの設定値は1/1/0 |
| pronunciation dictionary | PASS | 有効な既存辞書一致は`右上→みぎうえ`のseg013・036の2件。preflightもeffective textで照合 |
| context-dependent terms | PASS（機械確認） | 保守的候補7件は文脈に合う音列。seg046はsegment overrideで解決。global登録なし |
| existing audio | STOP（後段） | 本編WAVは0/65。ただしseg046 preview WAVを1件生成 |
| human listening | REVIEW（限定） | seg046 previewの自然さを1件だけ確認。全体聴取は本編生成後 |

### segment-level preflightの内訳（音響品質を含まない）

- live `audio_query`: **65/65**
- 設定不一致: **0件**
- explicit approval: **3件**（seg013/036の既存辞書、seg046のoverride）
- context checks（機械確認）: **7件**
- unresolved pronunciation REVIEW: **0件**

これは台本・辞書・live `audio_query`の読み確認であり、本編WAVの音質・アクセント・ポーズの最終判定ではない。

## 対象ファイルと既存preflight

- `AGENTS.md`: 読了。1文1segment、VOICEVOX標準設定、文脈依存語を共通辞書へ追加しない方針、Phase B Audio QAのsingle-writer方針を確認。
- `episodes/005_google_photos_delete/script.md`: ナレーション本文は9〜117行、発音レビュー候補は129〜144行。
- `episodes/005_google_photos_delete/episode.json`: narration設定は24〜31行、65 segmentは203行以降。
- `config/voicevox_pronunciation.yaml`: `右上→みぎうえ`は36〜40行の標準辞書エントリ。`方`の共通辞書エントリはない。
- `episodes/005_google_photos_delete/work/phase_a_preflight.md`: scriptは65件・1文1segmentでPASS、pronunciationはREVIEW可、全文VOICEVOXは未実施と記録済み（7〜17行）。
- `episodes/005_google_photos_delete/work/pronunciation_candidates.md`: Phase Aの固有名詞・メニュー名・数字・一般語候補を照合。辞書変更はしていない。
- `scripts/voicevox_preflight.py`: `/speakers`解決、segmentごとの`/audio_query`、辞書一致、文脈依存語のREVIEWを行う実装を確認。
- `scripts/voicevox_incremental.py`: Episode 005で使う生成経路として、話者・スタイル・速度値を23〜27行に固定し、`expected_reading`を経由してからquery/synthesisする流れ（132〜153行）を確認。
- `episodes/005_google_photos_delete/audio/`: 空の`.gitkeep`（0 bytes）のみ。`segments/`、segments manifest、timing、review WAVは存在しない。

`voicevox_preflight.py` CLIを2026-09-01に実行し、稼働中のVOICEVOX ENGINEで`/speakers`と65件の`/audio_query`を確認した。辞書置換後のeffective textをqueryへ渡す局所修正も反映した。

## VOICEVOX設定・live query

`episode.json`の指定:

```text
speaker=VOICEVOX
voice=剣崎雌雄
style=ノーマル
speedScale=1.0
intonationScale=1.0
pitchScale=0.0
segment_policy=1文ずつaudio_query→synthesis
```

live engineの確認:

```text
VOICEVOX ENGINE version: 0.25.2
speaker: 剣崎雌雄
style: ノーマル
style_id: 21
audio_query: 65/65 success
query settings mismatches: 0
```

`audio_query`で得られたkanaは、VOICEVOXのアクセント・ポーズ記号を含む表記です。以下では比較しやすいよう、対象語の音列を中心に記載しています。

## Context-dependent termsの再評価

| segment | 台本中の語 | 生queryの読み | 期待・辞書適用後 | 判定 |
|---:|---|---|---|---|
| 003 | 今日 | キョオ | きょう | 機械確認PASS。「きょうは」の音列。 |
| 012 | 仕方 | シカタ | しかた | 機械確認PASS。 |
| 013 | 右上 | ミギウエ | みぎうえ | 既存辞書適用PASS。生テキストをそのままqueryに渡さない。 |
| 014 | 開く | ヒラク | ひらく | 機械確認PASS。設定画面の文脈。 |
| 036 | 右上 | ミギウエ | みぎうえ | 既存辞書適用PASS。 |
| 046 | お使いの方 | カタ | かた | **PASS（segment override）**。人を表す「方」は「かた」。 |
| 053 | 両方 | リョオホオ | りょうほう | 機械確認PASS。 |
| 056 | 開いて | ヒライテ | ひらいて | 機械確認PASS。ゴミ箱をひらいて。 |
| 060 | 今日 | キョオ | きょう | 機械確認PASS。「きょうのまとめ」。 |
| 062 | 両方 | リョオホオ | りょうほう | 機械確認PASS。 |

### `右上`の辞書適用確認

既存辞書の表面形`右上`はepisode 005でseg013・036に2回現れる。preflightを生成経路と同じeffective textへ修正し、`右上→みぎうえ`を適用したqueryで両方とも`ミギウエ`になった。新しい辞書登録は不要。

### seg046の扱い

seg046の全文は「次は、iPhoneをお使いの方に、確認しておきたいことがあります。」。`episode.json`のseg046だけに`方→かた`を記録し、TTS入力を「次は、iPhoneをお使いのかたに、確認しておきたいことがあります。」へ限定した。表示字幕「お使いの方」は変更していない。

短いpreview WAVを`work/phase_b_review/audio/seg046_otsukai_no_kata_preview.wav`へ生成した。live query kanaは`オツカイノ/カタ`で、VOICEVOXが「おつかいのかた」として出力することを確認した。`仕方`（seg012）・`両方`（seg053/062）へは適用していない。

## 数字・記号・固有名詞

### 数字・数量

| 表記 | segment | queryで確認した読み | 判定 |
|---|---|---|---|
| 3つ | 006 | ミッツ | PASS（query読み） |
| 一つ | 007 | ヒトツ | PASS（query読み） |
| 二つ | 008 | フタツ | PASS（query読み） |
| 三つ | 009 | ミッツ | PASS（query読み） |
| 60日間 | 023 | ロクジュウニチカン | PASS（query読み） |
| 30日 | 024・052 | サンジュウニチ | PASS（query読み） |
| 30日以内 | 041 | サンジュウニチイナイ | PASS（query読み） |
| 30日間 | 051 | サンジュウニチカン | PASS（query読み） |

`1 / 6`などの数字はsection見出しの文字列であり、65 narrationには含まれません。`pronunciation_candidates.md`にある`2つ`は候補メモ上の表記で、実際のnarrationは`二つ`です。

### 固有名詞・英字表記

| 表記 | 出現segment | queryで確認した読み | 判定 |
|---|---|---|---|
| Googleフォト | 002・004・013・018・020・028・029・039・040・047・049・053・055・057・062・063 | グウグルフォト | PASS（query読み）／アクセントは試聴待ち |
| Googleアカウント | 043 | グウグルアカウント | PASS（query読み）／試聴待ち |
| Google側 | 015・044・045 | グウグルガワ | PASS（query読み）／試聴待ち |
| iPhone | 046・047・051・053 | アイフォオン相当 | WARN：`アイフォーン`の長音を人間が確認。`アイフォーン`を明示入力したqueryも同じVOICEVOX kana表記 |
| Apple | 049 | アップル | PASS（query読み）／試聴待ち |
| Android | 041 | アンドロイド | PASS（query読み）／試聴待ち |

### メニュー名・一般語

`デバイス`、`デバイスから削除`、`このデバイスの空き容量を増やす`、`空き容量を増やす`、`最近削除した項目`、`バックアップ済み`、`バックアップが完了しました`、`保存容量`、`保管場所`、`完全に削除`、`ゴミ箱`、`復元`、`タップ`、`端末`、`いっしょに`、`あわてずに`を全65 queryの中で確認しました。kana上の読みはそれぞれ、デバイス、デバイスからサクジョ、あきヨウリョウをフヤス、サイキン・サクジョ・シタ・コウモク、バックアップズミ、ホゾンヨウリョウ、ホカンバショ、カンゼンニ・サクジョ、ゴミバコ、フクゲン、タップ、タンマツ等の期待音列と一致しました。

特に人間が聴く優先箇所は、長い表示名のseg026・033・034・050・051・053・063、`バックアップが完了しました`のseg015、`保存容量`のseg043、`完全に削除`のseg024・045・049・052・058です。長い語は機械的なkana一致だけでは、区切り・速度・アクセント・聞き取りやすさを確定できません。

### 記号

65 narrationに現れる記号は、日本語の句読点、読点、かぎ括弧等の文構造用記号だけでした。英字・数字以外の未確認記号はありません。かぎ括弧内の「削除」「空き容量を増やす」「復元」等はqueryで発話されず、前後のポーズとして処理されています。

`[SHOT-01]`〜`[SHOT-08]`、section見出し、発音レビュー候補メモはナレーションsegmentではないため、音声へ渡していません。

## 発音辞書の確認

現行`config/voicevox_pronunciation.yaml`の全エントリをepisode_id=005のscope規則で照合しました。

- episode 005に実際に適用されるsurfaceは`右上`のみ。
- `右上→みぎうえ`の一致はseg013・036の2件。
- `reading_overrides`が空でないsegmentは1/65件（seg046のみ）。
- `方`、`今日`、`開く/開いて`などの文脈依存語を共通辞書へ追加していないことを確認。
- `App Store`、`Gmail`、`開けます`、`セキュリティ`、`後から`等の既存エントリは、今回の65 narrationには現れない、またはepisode scope外のため適用対象外。

辞書の追加・変更・並び替えはしていません。

## 人間が聴くべき箇所

今回の停止位置で必要な確認は、seg046 previewの自然さ1件だけとした。本編生成後に全体試聴を行う。

1. **seg046 preview**: `seg046_otsukai_no_kata_preview.wav`を再生し、「おつかいのかた」が自然に聞こえるか確認する。字幕は「お使いの方」のまま。
2. 本編65件の生成後に、`右上`、固有名詞、数字、長いUI名、クリッピング、ポーズ、実尺字幕をまとめて全体試聴する。
3. 今回、`方`、`今日`、`仕方`、`開く`、`両方`、`開いて`へのglobal辞書追加はしない。
4. seg046 previewのファイルは5.056秒・24kHzで、full narrationではない。
5. full audio QAは、本編WAV生成後に実施する。
6. 今回の人間確認対象は1件に限定する。
7. 依頼どおり、全体の音声生成・実尺字幕は未実施。

## 未実施・制約

- 65件の本編WAV合成は未実施（依頼どおり）。
- seg046のpreview WAVだけ生成。query上の読みは確認済みだが、自然さ・アクセント・イントネーションの最終聴感はpreviewの再生確認に残る。
- `segments_manifest.csv`、`audio_timing.json`、連結review WAVがないため、segment境界・実尺・字幕タイミング・ポーズの確認は未実施。
- `scripts/voicevox_preflight.py` CLIを実行済み。話者解決と65件の`audio_query`を確認した。
- `config/voicevox_pronunciation.yaml`、`script.md`、既存audio、その他global辞書は変更していない。`episode.json`はseg046のoverrideのみ更新。

## 次の安全な判断

1. seg046 previewを人間が1件だけ再生し、自然さを確認する。
2. 承認後に65件をVOICEVOX標準設定で生成し、seg046とseg013・036を重点試聴する。
3. WAV・manifest・実尺字幕が揃った後、全65件の音響QAを再実施する。

## 変更ファイル

本再評価で更新・作成した成果物は次のとおり。

- `work/subagents/005_google_photos_delete/audio_qa_report.md`
- `episodes/005_google_photos_delete/work/phase_b_review/audio/seg046_otsukai_no_kata_preview.wav`
- `episodes/005_google_photos_delete/work/phase_b_review/audio/seg046_otsukai_no_kata_preview_query.json`

global pronunciation dictionary、既存の本編audio、final outputは変更していません。音声範囲でのcanonical変更はepisode.jsonのseg046 `reading_overrides`だけです。字幕・scene・manifest等の残課題反映は親Codex側のcanonical更新として別途記録しています。
