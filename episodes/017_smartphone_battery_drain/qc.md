# Episode 017 QC

## Phase B現在判定

- 判定: **FULL_DRAFT_READY_HUMAN_GATE_2_REVIEW**
- 対象: Human Gate 1 minor changes反映後の実画面同期、音声、字幕、scene、full draft
- 基準日: 2026-09-09
- Human Gate 1: **APPROVED WITH MINOR CHANGES**
- Human Gate 2: **REVIEW REQUIRED**。承認前のためupload eligibleではない
- Phase Bの完了条件: Human提供iPhone 12 mini／iOS 26.6.1の画面を受領し、正規化crop、音声、字幕、scene、full draft、個人情報QAを実施済み。発音レビューのみHuman確認待ち

## 確認結果

| 項目 | 判定 | 確認内容 |
|---|---|---|
| Fact | PASS_WITH_SCREEN_SYNC | Apple公式を主根拠に、使用状況・画面・バッテリー状態を紐付けた。撮影時点でApple公式を再確認し、iPhone 12 miniの実表示へ同期。 |
| Language | PASS_WITH_MINOR_CHANGES | 65歳以上を想定し、確認と変更を分離。バッテリー状態は最大容量・注意表示を中心にし、専門用語を実機確認後に補足する。 |
| Visual | PASS_WITH_HUMAN_CONTACT_SHEET_REVIEW | Human提供の実OS画面から正規化cropを作成。15 sceneとdraft contact sheetを目視確認し、アプリ名が見える使用状況rawはviewer-facingに使用しない。公式画面の機械的な視覚重心チェックは比較用背景がないため適用外とし、目視確認を正とする。 |
| Audio | REVIEW_PRONUNCIATION | VOICEVOXを1文単位で34セグメント生成。無音・クリッピングを含むdraft QAはPASS。`夕方`、`使われ方`、`画面上`、`開いて`、`バックグラウンド`、`iPhone/iOS/Apple`の発音をHuman聴取確認する。 |
| Policy | PASS | 位置情報、通知、バックグラウンド通信、5G、強制終了の一律オフ推奨を含めない。サムネイル生成・YouTube操作は行わない。 |
| Privacy | PASS_WITH_RESTRICTIONS | raw screenshotsはsource保管。production assetにはアプリ名を避けたcropのみ使用し、Apple Account・メールアドレス・電話番号・端末名・通知・位置情報履歴・個人的な利用状況・シリアル番号を残さない。raw screenshots/はcommit対象外。 |
| Subtitle | PASS | 34 cueを実音声タイミングから生成。60px、最大2行、subtitle preflight fail=0 / warn=0。 |
| Draft | PASS | `output/draft_auto_v1.mp4`。321.13秒、1920×1080、30fps、Phase 2 QA failures=0 / warnings=0。 |

## Human提供画面の確認結果

1. Human提供端末: iPhone 12 mini / iOS 26.6.1。
2. 「バッテリー」画面: 「1日の使用状況」「すべてのバッテリー使用状況を表示」「バッテリーの状態と充電」。
3. 「バッテリー使用状況」画面: グラフ、「画面オン」「画面オフ」。アプリ一覧はrawに個人利用が推測できる名前があるため使用しない。
4. アプリ詳細: 「アクティビティ」「画面上」「バックグラウンド」を確認できるcropを使用。
5. 「画面表示と明るさ」画面: 「明るさ」「自動ロック 5分」を確認。iPhone 12 miniに「常に画面オン」は表示されないため、viewer-facingでは一般化しない。
6. バッテリー状態: 「バッテリーの状態と充電」「最大容量 100%」「ピークパフォーマンス性能」を確認。「サービス」は表示されていないため、条件付き説明にする。

## 禁止事項チェック

- 節電のために設定を片っ端から変更: **該当なし**
- 位置情報・通知・バックグラウンド通信の一律オフ: **該当なし**
- 5Gを切れば必ず改善という断定: **該当なし**
- 強制終了の常用案内: **該当なし**
- バッテリー残量や最大容量だけで交換必須と断定: **該当なし**
- 怪しい節電アプリの紹介: **該当なし**
- 内部用ブランド文言のviewer-facing混入: **0件**

## 実施済みQA

- episode/schema、sources、scenes、official assets: **PASS**
- viewer-facing内部ブランド文言検査: **PASS / count 0**
- CTA canonical preflight: **PASS**。`config/channel_cta.json`の文言・Episode016再利用音声・visualを使用
- production preflight: **REVIEW**。失敗はなく、VOICEVOX発音レビュー6件のみHuman確認待ち
- 実尺: 本編音声 308.681秒。CTA音声 11.456秒＋末尾1秒を含むdraft 321.13秒
- サムネイル: **未生成**
- YouTube操作: **未実施**

## Human Gate 2確認ポイント

1. draft全体の実機UI、字幕、ナレーションの一致とテレビ視聴時の可読性
2. `画面上`、`開いて`、`夕方`、`使われ方`、`バックグラウンド`、`iPhone`、`iOS`、`Apple`の発音
3. app listを除いた正規化cropとdraftに個人情報がないこと
4. バッテリー状態の説明が「最大容量」「サービス等の注意表示」に留まり、数字だけで交換必須・故障と断定していないこと
5. CTA本文・音声がcanonicalと一致し、右側のEnd Screen予約領域を侵食していないこと
