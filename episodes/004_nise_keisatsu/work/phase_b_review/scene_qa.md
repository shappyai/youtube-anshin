# Scene QA — Episode 004 Phase B前半（2026-08-31）

## レンダリング結果

- 18シーンすべて `work/rendered_final_scenes/scene_NNN.png`（1920×1080・PNG）
- scene mode内訳: gpt_image=7 / template=10 / official=1（episode.jsonのrender_modeどおり）
- contact sheet: `work/phase_b_review/scene_contact_sheet.png`（5列・ラベルは画像外の下側）
- 自動QA（phase2_qa.scene_visual_warnings）: **WARN 0件**

## 目視確認の結果と修正

- GPT画像7枚（001/003/006/009/012/015/018）はすべて単一構図・文字なし・破損なし。collage/contact sheetではない。Codex文字は背景の上に直接重ねており、Episode 003で起きた「GPT画像＋大型白カードの二重レイアウト」は確認されない（scrimは文字周囲のみ）。
- 見出し折返しの単語分断8箇所を修正（scene 003/006/008/009/011/012/016/018）。見出しを短くするか、自然な分岐点で折り返す文言・headline_scaleに変更。
- SHOT-13（official）: 国民生活センターの明言文（ピンク強調）を含む要旨部を大きく表示。ページ全体の極小表示はしていない。明言文・188・#9110の誘導文言・相談事例見出しが読める。

## WARN候補（自動QA対象外・人間確認用メモ）

- GPT画像の下部180pxに淡い絵柄（コップ・コード・机など）が写り込む7枚。本編では字幕帯（y=900〜1080）が上書きするため表示上は問題ない想定だが、contact sheetで確認してほしい。
- 人間生成画像の解像度は1672×941。原本は無変更で、検証・レンダリングはLANCZOS拡大の1920×1080正規化コピー（`work/phase_b_review/normalized_ai/`）を使用。再出力での差し替え可。
- scene 003の見出し「ニセ警察詐欺」は背景の淡色部に重なる。白outline・影付きで視認できるが、明るい背景上の発色はcontact sheetで最終確認。

## 停止状態

本編VOICEVOX生成・ffmpeg・draft・final・thumbnail・YouTube操作は未実施。pronunciation REVIEW 10件の人間確認と、contact sheetの人間レビュー待ち。

## Phase B後半の更新（2026-08-31・draft v1/v2）

- 本編VOICEVOX 72セグメント生成完了。pause: normal 0.30s / important 0.50s / section 0.80s を反映。
- pronunciation: 人間承認を反映しunresolved REVIEW = 0。override適用9件（方4・＋1・電話番号4）。
- CTA: channel_common_cta（brand promise非表示）を生成・確認済み。
- draft_v1.mp4 生成後、SCENE-013のofficial画面を本編フレームで確認し、明言文の実効表示が小さいと判断。公式素材を「明言文2文＋相談事例見出し」へ再cropし、表示スロット幅1680pxに対して約2.2倍に拡大。draft_v2のフレーム上で明言文（ピンク強調）が読めることを確認。
- draft_v2.mp4 を生成（音声は72件すべてhash再利用）。自動QA: PASS（decodeエラー0・黒フレーム0・無音異常0・シーン18・字幕72・時間一致）。

## Phase B後半v3（人間視聴レビュー反映・2026-08-31）

- 日本語改行の恒久ルール化: `wrap_text()`に禁則処理（行頭禁則・行末禁則）と1文字孤立行の統合を追加。全18sceneのoverlay textを再検査し、`linebreak_issues()=0`・`narration_item_count_issues()=0`。
- SCENE-006「＋から始まる番号」は1行表示に、SCENE-013/015の1文字孤立行も解消。
- SCENE-007: `compare_default()`の他episode文言（マイナポータルアプリ・マイナアプリ等）を除去し、sceneデータ（compare_cards）駆動に変更。再render後に「＋81／＋81以外」の国コード構成を確認（マイナ文言の残存grep 0件）。
- SCENE-008/011/016: layout_06_caution（assetsなし時）のグループ座標を中央寄せに変更。template centroid検査をQAへ追加し、全template sceneでWARN 0を確認。修正前後の比較画像: `work/phase_b_review/alignment_comparison_v3.png`。
- SCENE-011: support_textを電話番号分断のない明示3行（＃9110を1ユニット）に変更。main_messageも2行の自然な文言へ。
- SCENE-014: ナレーション・字幕を「次の4つを行います」へ修正（seg49のみ再生成）。画面4項目と一致。
- seg071: 188の読みを「イチ、ハチ、ハチ」（カタカナ・読点区切り）に変更し再生成。kana上で [h] 子音を確認。試聴用wav: `work/qa_frames/seg071_188_preview.wav`。
- draft_v3.mp4 生成（seg49/71のみ再生成、他はhash再利用）。自動QA: PASS。duration 401.8s。
