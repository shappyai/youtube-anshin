# Episode 009 Visual Gate v1 QA

確認日: 2026-09-05

## 機械検査

- レンダー: 19 / 19 scene PASS
- scene quality report: 17 OK / 2 WARN / 0 FAIL
- WARN: scene 006・007の公式見出しcrop。余白率は高いが、公式画面の該当箇所を読ませるための意図的な拡大構成
- ImageGen exact text QA: SCENE-001 / SCENE-015 / SCENE-019 の3 / 3 PASS
- `blank_white_slide`: 該当なし
- `tiny_text`: PASS
- visual axis / stacked panel alignment: PASS
- semantic icon visual center / plate alignment: PASS
- subtitle safe area: PASS（下部180px）
- background consistency: PASS（`adult_digital_soft_image_bg`）

## 人間確認項目

- contact sheet全体の視線誘導、scene間の重複、文字の縮小時可読性
- ImageGen 3sceneの指定文言、誤字・脱字・余計な文字、人物と文字の重なり
- scene 006・007の公式cropが「バージョン情報」「デバイスの仕様」の場所として読み取れるか
- scene 009の公式「Check for updates」ボタンと日本語ナレーションの対応
- 公式画面を実機画面と誤認しない説明になっているか

## Phase Bへ進めない理由

このファイルはVisual Gateの機械検査結果をまとめたもの。人間確認が完了するまで、VOICEVOX、字幕、draft、thumbnail、YouTube uploadは開始しない。

個人情報を含む一時原画 `assets/official/_source_tmp/devicenameandmodel.png` は、採用素材・manifestから参照していないことを確認後、2026-09-05に削除済み。
