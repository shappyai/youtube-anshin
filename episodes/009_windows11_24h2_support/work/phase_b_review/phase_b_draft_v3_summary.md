# Episode 009 Phase B draft_v3 summary

確認日: 2026-09-05

## Scope

- 入力: `output/draft_v2.mp4`
- 出力: `output/draft_v3.mp4`
- draft_v1 / draft_v2は上書きせず保持。
- Visual Gate v2の19scene、SCENE-006 / 007 / 009、公式UI crop、CTA画面・CTA音声は変更なし。
- 停止位置はdraft_v3とQAまで。final、thumbnail、upload、schedule/public、End Screen設定は未着手。

## 1. 約00:30の変更

- segment 006
- 変更前: 「三つ目、更新が表示されないときの考え方です。」
- 変更後: 「三つ目は、更新が表示されないときに考えるポイントです。」
- 発音overrideで「方」を読ませる方法は使わず、自然な台本文言へ変更。

## 2. 約03:29の変更

- segment 038
- 変更前: 「24H2の方は、まず25H2が表示されるかを確認してください。」
- 変更後: 「24H2の場合は、まず25H2が表示されるかを確認してください。」
- `24H2` / `25H2`の承認済みVOICEVOX読みは維持。

## 3. 「方」全出現scan

- 対象: `script.md`、`episode.json`の全52 narration segment。
- narration内の変更後の「方」: 2件。

| segment | 分類 | 判定 | 内容 |
|---:|:---:|:---:|---|
| 001 | A: 人を指す | REVIEW | 「Windows 11を使っている方」／かた。今回は非対象のため改稿なし。 |
| 011 | D: 「〜の方は」 | REWRITE候補 | 「HomeやProの方は」／かた。今回は非対象のため改稿なし。 |

- `script.md`の「方」文字数: 4（narration 2件、構造見出し・制作メモを含む）。
- `episode.json`のnarration/display/subtitle以外では、Visual Gate v2で承認済みのSCENE-013 headline「24H2の方は、まず25H2」とpublish descriptionの説明文が残る。いずれもVOICEVOX narrationではなく、Visual Gate v2を変更しないため保持。
- `ambiguous_kanji_pronunciation` report: `work/phase_b_review/ambiguous_kanji_pronunciation_v3.md`
- reusable preflight: `scripts/ambiguous_kanji_pronunciation.py`（canonical report: `work/phase_b_review/ambiguous_kanji_pronunciation_v3_canonical.md`）
- target wording checks: segment 006 / 038ともPASS。
- `方`のglobal pronunciation dictionary entry: なし。

## 4. 恒久ルール

- `AGENTS.md`へ`ambiguous_方_avoidance`を追加。
- 自然な代替表現がある「方」はVOICEVOX生成前の台本段階で避ける。
- `方`を残す例外は固有名称・引用・公式UI・不自然／意味変更となる場合。残す場合は`ambiguous_kanji_pronunciation`でSAFE / REWRITE / REVIEWを分類する。

## 5. narration regenerated / reused

- regenerated: 2 segments（006 / 038）
- reused: 50 segments
- narration duration: 289.880s（pause込み）
- approved pronunciation QA: Windows / Update / ID / 24H2 / 25H2 / 26H1 = PASS
- QA report: `work/phase_b_review/pronunciation_v3_qa.md`

## 6. subtitle / timing

- 59 cuesを実測音声から再生成。
- SUB-006: 新文言を2行へ整形。
- SUB-038: 新文言を既存の意味の切れ目で2行へ整形。
- SUB-031-2は表示文言を変えず2行へ整形し、既存の幅超過候補を解消。
- minimum font: 72px
- font <56: 0
- overflow: 0
- 3-line: 0
- semantic split: PASS
- TTS reading leakage: 0
- scene timeline / CTA start: 再計算。CTA startは289.880s。
- chapter: `01:08 / 01:55 / 02:52 / 03:55 / 04:29`へ実測scene開始に同期。

## 7. draft_v3 / QA

- draft_v3: `output/draft_v3.mp4`
- duration: 304.880s（narration 289.880s + CTA postroll 15.000s）
- video: H.264 / 1920x1080 / 30fps
- audio: AAC / 48kHz
- decode error: 0
- black frame: 0
- unexpected narration silence: 0
- Visual Gate v2 regression: 0
- official UI: PASS
- privacy: PASS。`assets/official/_source_tmp/devicenameandmodel.png`は存在せず、canonical reference 0。
- CTA: PASS。画面・音声とも変更なし。
- draft QA report: `work/draft_v3_qa.md`

## 8. 人間再確認timestamp

以下の開始位置の前後10秒程度を確認し、全編も視聴する。

| 対象 | segment | 開始 |
|---|---:|---:|
| 新文言「考えるポイント」 | 006 | 00:27.379 |
| 新文言「24H2の場合は」 | 038 | 03:24.944 |

確認ポイント:

- 2箇所で旧文言が消え、新文言が音声・字幕とも自然か。
- Windows / Update / ID / 24H2 / 25H2 / 26H1の読みが意図どおりか。
- 006→007→009の操作導線と、字幕の読みやすさ。
- Visual Gate v2のSCENE-006 / 007 / 009とCTAが変わっていないか。

Episode 009 draft_v3完成。「方」を台本段階で避ける恒久対策を反映。人間最終確認待ち
