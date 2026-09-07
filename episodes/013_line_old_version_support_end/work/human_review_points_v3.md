# Episode 013 human review points v3

判定時点: 2026-09-06  
状態: **PRE-DRAFT GATE RECORD — VISUAL_GATE_V3_APPROVED / PRONUNCIATION_HUMAN_APPROVED / DRAFT_V1_GENERATED**

7つの実画面とSCENE-005の公式事実rendererは配置済み。Visual Gate v3は人間承認済み（24scene OK / WARN 0 / FAIL 0）。F-011も具体日未確定のFact boundaryとして人間承認済み。発音8件は全件聴取ALL OK。下記の時刻は、生成済みVOICEVOX本編（405.874秒）の実測タイムラインを基準にしたpre-draft確認記録である。全編Draft Gateの新しい確認点は`work/human_review_points_draft_v1.md`を正本とする。

## 実画面キャプチャ確認ポイント

| 時刻（本編音声） | Scene | 人間確認 |
|---|---:|---|
| 01:15.150–01:25.809 | 006 | AndroidのLINE `現在のバージョン 26.14.0`が読める。機種差を注記し、個人情報がないこと |
| 01:55.790–02:12.420 | 009 | iPhoneの`iOSバージョン 26.6.1`が読める。Apple Account等がないこと |
| 02:12.540–02:28.110 | 010 | Androidの`Android バージョン 16`が読める。端末識別情報がないこと |
| 03:11.490–03:28.000 | 013 | App StoreのLINE行に実際に表示された`開く`を更新ボタンと誤認しないこと |
| 03:28.150–03:42.590 | 014 | Google Play検索結果のLINE行に表示された`インストール済`・`開く`を確認。想定メニューとの差分が伝わること |
| 03:42.720–03:58.840 | 015 | iPhoneの`iOSは最新です`と`iOS 26.6.1`が読めること |
| 03:58.960–04:15.300 | 016 | Androidの`お使いのシステムは最新の状態です`が読めること |

## SCENE-005確認

- iPhone版LINEの実画面ではなく、`LINE 14.6.3以上`と`14.6.3未満は、11月上旬にサポート終了予定`という公式事実だけを表示していること。
- LINE設定画面のAI再現・fake UIに見えないこと。

## 条件文・発音確認

| 時刻（本編音声） | Scene / Segment | 人間確認 |
|---|---:|---|
| 04:26.180–04:45.000 | 018 / 049–052 | 「ケースA　今回は対応不要」と、LINE・OSが基準以上で更新できる条件が同時に伝わること |
| 06:34.964–06:40.777 | 073 | 「11月上旬の予定」「全員ではない」の発音・字幕同期 |
| 06:40.927–06:45.674 | 074 | まとめの結論と字幕の読みやすさ |

## CTA確認（ドラフト生成後）

- 本編終了後の15.000秒postrollが1回だけ連結されること。
- `registration_conversion_v1`の画面・音声・canonical textが完全一致すること。
- 中盤CTA、重複CTA、疑似subscribe UIがないこと。

## 現在の保留条件

- 元画像での65歳以上・TV視聴向け可読性、SCENE-005の事実表示、SCENE-013/014の`開く`表示のdraft Human Gate再確認
- Fact / Privacy / Audio / Subtitleの最終人間確認（機械QAはPASS）

本ファイルはVisual Gate v3前後の確認記録として保持する。`output/draft_v1.mp4`生成後の全編確認は`work/human_review_points_draft_v1.md`で行う。
