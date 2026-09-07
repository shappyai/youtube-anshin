# Episode012 draft_v3 QA

確認日：2026-09-06  
状態：**PASS / 人間の全編確認待ち**

## 変更確認

- `本物？`：segment030に文脈accent override（`ホンモノ` / accent=4）を適用。直接`audio_query`した`これ、本物？`はホ・ン・モ・ノの4モーラ、`is_interrogative=true`、余計な母音0。
- `本物`回帰：segment002 / 003 / 008 / 014 / 030 / 066 / 079の7出現を実文脈queryで確認。全件4モーラ、`extra_vowel_after_honmono=0`。
- `e-Tax`：標準辞書を`イータックス`、mora列をイ・イ・タ・ッ・ク・ス、accent=3（タピーク）、internal pause=0へ更新。`ス`母音長0.032084秒。
- CTA重複：SCENE-031を本編timelineから削除、segment080とSUB-118/119を削除。本編はSCENE-030（segment076〜079）で終了し、postroll CTAを直後に1回だけ連結。

## 機械QA

| 項目 | 結果 |
|---|---|
| Phase A / source / schema / scene mode | PASS |
| Fact Check | FAIL 0 / REVIEW 3 |
| Privacy | FAIL 0 / REVIEW 0 |
| Scene quality | PASS（30 OK / WARN 0 / FAIL 0） |
| Subtitle preflight | PASS（117 cue / 72px / minimum56px / fail0 / warn0） |
| TTS reading leakage | PASS（0） |
| Japanese semantic line break | PASS（4指標すべて0） |
| Contextual pronunciation audio gate | PASS |
| Draft decode / video | PASS（1920×1080 / 30fps / H.264） |
| Audio | PASS（AAC / 48kHz / mono） |
| End CTA count | 1 |
| Pre-CTA duplicate narration | 0 |

## 素材・尺

- draft：`output/draft_v3.mp4`
- 実測尺：**585.55秒**（本編570.551秒＋postroll15.000秒）
- narration：**79 segment**
- subtitle：**117 cue**
- CTA audio SHA-256：`1D21F765F5606310CA08BC0264EC6ED0136F68F5A7DA07318B5018F1735FDBC9`
- CTA visual SHA-256：`96EFB5195CD7F3D7121472A79F300AF19999108186D6B35C370EFA488185EAE0`
- CTA config hash：`7BB2FF3FCED403887046147741665B29ED948DBD27F4BB4A218DA5F263E6FF70`
- postroll：15.000秒、音声11.456秒、余韻3.544秒、Episode011実使用素材を変更なしで再利用

## Human gate

- 全編の音声・映像・字幕の確認待ち：`work/human_review_points_v3.md`
- thumbnail：未着手
- `final/final.mp4`：未着手
- YouTube upload / schedule：未着手
