# Episode 005 Phase B Gate 2（2026-09-02）

対象: `episodes/005_google_photos_delete/`

## 判定

**PASS（本編生成へ進む）**。重大REVIEWは残っていない。

| Gate | Status | Detail |
|---|---|---|
| pronunciation | PASS | 65/65 effective query。seg046は人間承認済み（APPROVED_BY_HUMAN）。unresolved REVIEW 0 |
| GPT images | PASS | 5/5（001/003/013/017/025）。normalized_ai 1920×1080を再確認。SHA重複0、再生成0 |
| Android assets | PASS | SCENE-004/006はPhase B前半で局所解決済み。008/012/014は実画面PASS |
| iPhone / official | PASS | 9 assets / 8 scenes。path・source・crop検証OK |
| line-break QA | PASS | scene linebreak issues 0（日本語禁則＋ASCII token分断検出を追加適用） |
| English token QA | PASS | SCENE-016/017を修正済み（Goo/gle・G/oogleなし）。v3 contact sheetで25/25確認 |
| template leakage | PASS | unresolved placeholder 0 / placeholder asset 0 |
| scene mapping | PASS | 65 segments・25 scenes、item count不一致0 |
| visual balance | PASS/WARN | scene_visual_warnings 0。WARN専用計測11件はcontact sheetで確認済み候補として別記録 |
| item count | PASS | narration_items一致（0 issue） |
| subtitles | PASS | 65 cues。安全幅超過0、FAIL 0 / WARN 0 |
| render | PASS | 25/25、全て1920×1080（016/017のみ再render、他23はreuse） |

## 恒久化したEnglish token QA

- `scripts/scene_renderer.py` `_wrap_paragraph_japanese`: ASCII英数字の連続tokenを途中分断しない（幅超過時もtoken単位で保持し、fit_text_blockの縮小で調整）。
- `scripts/phase2_qa.py` `linebreak_issues`: 行境界でASCII runが連続し、元テキスト内で同一tokenなら「ASCII英数字token途中分断」として検出。
- `scripts/subtitle_preflight.py` `PROTECTED_TERMS`: Google / Googleフォト / Googleアカウント / YouTube / LINE を追加。

## 本編生成条件

次工程（VOICEVOX本編65件 → subtitle timing → draft assemble → draft QA）に進む。final・thumbnail・YouTube操作は行わない。
