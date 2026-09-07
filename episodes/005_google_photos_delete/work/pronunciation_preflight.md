# VOICEVOX pronunciation preflight（Phase B前半再評価）

Episode: 005_google_photos_delete
Engine: PASS
Speaker: 剣崎雌雄 / ノーマル (style_id=21)
Query count: 65/65
Dictionary: config\voicevox_pronunciation.yaml

自動で pronunciation dictionary は変更していません。

## PASS

- seg 013 右上 → みぎうえ（pronunciation dictionary）
- seg 036 右上 → みぎうえ（pronunciation dictionary）
- seg 046 方 → かた（reading_overrides）

## Context checks（機械確認済み・未解決ではない）

保守的な候補検出が拾った7件は、effective text（既存辞書・seg単位override適用後）の65/65 live `audio_query`で、文脈に合う標準音列を確認した。新しいglobal辞書は追加していない。

- seg 003 `今日` → `キョオ`（「きょうは」）
- seg 012 `仕方` → `シカタ`（「しかた」）
- seg 014 `開く` → `ヒラク`（設定画面をひらく）
- seg 053 `両方` → `リョオホオ`（「りょうほう」）
- seg 056 `開いて` → `ヒライテ`（ゴミ箱をひらいて）
- seg 060 `今日` → `キョオ`（「きょうのまとめ」）
- seg 062 `両方` → `リョオホオ`（「りょうほうから」）

VOICEVOXの`キョオ`は、同じ剣崎雌雄のEpisode 004で人間承認済みの「きょう」に対応する表記。上記に誤読を示す音列は見つからなかったため、今回の未解決REVIEWには残していない。

## REVIEW

- なし

## Summary

- result: PASS
- approved matches: 3
- machine-confirmed context checks: 7
- review items: 0
- unresolved pronunciation REVIEW: 0
- query count: 65/65
- dictionary mutation: none

## seg046 preview

- TTS input: `次は、iPhoneをお使いのかたに、確認しておきたいことがあります。`
- display subtitle: `お使いの方`（変更なし）
- override: seg046 only `方 → かた`
- human approval: **APPROVED_BY_HUMAN（2026-09-02、Phase B後半開始時に確定）**
- preview WAV: `episodes/005_google_photos_delete/work/phase_b_review/audio/seg046_otsukai_no_kata_preview.wav`
- live query kana: `オツカイノ/カタ`（「おつかいのかた」）
- full narration WAV: 未生成

## 空く（draft_v3、2026-09-02 人間レビュー反映）

- 修正segment: seg37（約3:20）・seg44（約4:01）のみ。`reading_overrides: {"空く": "あく"}`。
- query kana: seg37「アクヨオリョオガ」、seg44「デアクノワ」＝「あく」。表示字幕・画面の「空く」漢字は維持。
- 恒久対応: single「空く→あく」のglobal登録はしない。容量文脈限定フレーズ2件（「で空くのは→であくのは」「空く容量が→あく容量が」）を`config/voicevox_pronunciation.yaml`へ登録（approved context rule）。`episode_io.py`の文脈候補（要調査の自動提案）へ「空く」を追加。
- `episode.json`更新のみで対応可能なsegmentにはoverrideを自動提案する方針を維持（今回はoverride適用済み）。
