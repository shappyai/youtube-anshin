# Line-break QA — Episode 004（draft_v3向け）

基準: 2026-08-31。全18sceneのoverlay text（headline / support_text / main_message / compare card / items）を、renderと同じbox・fontでwrap再現し検査。QA用ヘルパは `scripts/phase2_qa.py` の `linebreak_issues()`・`narration_item_count_issues()`、renderer共通の日本語wrapは `scripts/scene_renderer.py` の `wrap_text()`（禁則処理・孤立行統合つき）。

## 共通ルール（renderer恒久化）

`wrap_text()` を以下のルールで更新した（Episode 004以降の全episodeに適用）。

- 行頭禁則: 、。，．・：；！？％）」』】〕〉｝＞ー… を文頭に置かない
- 行末禁則: （「『【〔〈｛＜ を行末に残さない
- 1文字だけの孤立行を作らない（前後の行へ統合し、単語途中分断を防ぐ）
- 明示改行（\\n）はそのまま尊重（段落単位で処理）

大規模renderer改修はしていない（wrap関数1箇所＋QA検出の追加のみ）。

## scene別 修正記録

| scene | 対象 | before | after | reason |
|---|---|---|---|---|
| SCENE-006 | headline | 「＋から始まる番｜号」（2行・「号」孤立） | 「＋から始まる番号」（1行） | 1文字孤立行の統合→1行化 |
| SCENE-007 | compare全体 | マイナポータルアプリ／マイナアプリ（前episode文言） | 「＋81｜日本の国番号」／「＋81以外｜国際電話の可能性・知らない番号は慎重に確認」 | templateのhard-code文言をsceneデータ（compare_cards）へ置換。他episode由来文字列の排除（text provenance） |
| SCENE-008 | layout | アイコン＋テキストgroupが左寄り（右に大空白） | group全体を中央寄せ（content centroid約960） | template（layout_06_caution）の基準座標を中央化。assetsなし時のみ適用 |
| SCENE-011 | main_message | 「…番号でも｜、偽装の可能性があり｜ます」（助詞行頭＋語尾孤立） | 「警察署の実在番号でも、｜偽装の可能性があります」（2行） | 文言を短くし、wrap改善と合わせて自然な2行へ |
| SCENE-011 | support_text | 「…／＃｜9110へ相談…」（＃9110分断） | 「自分で調べた番号へ／＃9110へ相談／教えられた番号、かけない」（明示3行） | 電話番号途中の不自然な改行を禁止（記号＋数字の分断もQA検出対象に追加） |
| SCENE-011 | layout | 左寄り | 中央寄せ | SCENE-008と同じtemplate修正 |
| SCENE-013 | support_text | 「個人名義の口座への送金もありませ｜ん」 | 1行 | 1文字孤立行の統合 |
| SCENE-015 | headline | 「今すぐできる対｜策」 | 「今すぐできる対策」 | 1文字孤立行の統合（単語「対策」の分断防止） |
| SCENE-016 | layout | 左寄り | 中央寄せ | SCENE-008と同じtemplate修正 |

## 全scene検査結果（draft_v3再render後）

- `linebreak_issues()`: 0件（孤立行・禁則違反・単語分断・記号+数字分断なし）
- `narration_item_count_issues()`: 0件（SCENE-014はナレーション「4つ」＝画面4項目）
- 目視: SCENE-006/007/008/011/013/015/016、およびcontact sheet全体で確認済み

## 恒久QAへ追加した項目

- `phase2_qa.linebreak_issues()`: 全sceneのoverlay textをrenderと同じwrapで再現し、孤立行・禁則・既知単語分断・記号+数字分断をWARN検出（draft QA）。
- `phase2_qa.narration_item_count_issues()`: ナレーションが「Nつ」と明示するsceneの画面items数との不一致を検出。
- `phase2_qa.scene_visual_warnings()`: template scene（一覧・注意・まとめ・セクション系）にcontent centroid検査を追加（重心Xが650..1270の範囲外ならWARN）。左右構図のGPT画像・2カラム設計（03/04/05）には適用しない。
- `build_episode.check_item_counts()`: production preflightの「item counts」ゲート（REVIEW扱い）。
