# Episode 011 Visual Gate v2

確認日：2026-09-06

## 判定

`APPROVED_WITH_2_FIXES`

Visual Gate v1のscene構成、micro story、3つの行動、SCENE-019の中盤CTA位置、fact boundary、共通visual themeは維持し、指定された2点だけを修正した。

## 修正1：SCENE-003

- 修正版：`assets/official/mhlw_warning_core_v1.png`
- 表示の核心：`電話やSMSで直接、健康保険証の利用登録を求めることはありません。`
- 公式URL：`https://www.mhlw.go.jp/stf/newpage_44734.html`
- 表示方式：公式本文の意味を変えない短い核心表示をPILで正確に配置。AI生成文字・公式UIの再現は使用しない
- typography：核心文64〜80px以上、出典48px以上、下部180pxは字幕安全帯
- 結果：scene quality report v2でOK、contact sheet v2で大きな1メッセージとして確認

## 修正2：Episode010実使用CTA

- 検索・照合範囲：Episode010 `episode.json`、`publish.json`、`media_manifest.csv`、draft_v1/draft_v2で使用されたCTA設定・画面・音声
- variant：`registration_conversion_v1`
- canonical text：`スマホやパソコンの「これ、どうすればいい？」を、公式情報で分かりやすく確認しています。次に困ったときのために、チャンネル登録しておいてください。`
- 表示：`次に困ったときのために。` / `チャンネル登録しておいてください。`
- 結果：Episode011のpostrollへ画面・音声・文言を同一内容で再利用。CTA preflight PASS、fake subscribe UI 0

## Phase B確認

- scene：19/19 OK、WARN 0、FAIL 0
- draft representative frames：20枚を`draft_v1_contact_sheet_v2.png`へ収録
- SCENE-003、電話番号scene、SCENE-019、終了CTAの代表フレームを確認
- full draft全編視聴：未実施。人間Gateへ引き渡し
