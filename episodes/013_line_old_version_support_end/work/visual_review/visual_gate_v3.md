# Episode013 Visual Gate v3 — 2026-09-06

## 判定

- machine QA: **PASS**
- human Visual Gate v3: **APPROVED**（2026-09-06）
- F-011 fact boundary: **HUMAN_APPROVED_REVIEW**（具体日未確定。「11月上旬にサポート終了予定」まで）
- pronunciation review pack: **HUMAN_APPROVED_ALL_OK**（8件、67.053秒、再生成0、共通辞書追加0）
- draft generation: **STOP**
- scope: 24 scenes / 7 real UI captures / SCENE-005 official-fact renderer

Visual Redesign v2の人間承認済みImageGen assetは再生成せず、Phase Bで揃った実画面だけを差し替えた。SCENE-005はiPhone版LINEの実機画面を用意できないため、LINE公式の事実を正確な文字で表示するrenderer-native sceneとした。LINE画面のAI再現・fake UIは使用していない。

## 機械QA

| Check | Result |
|---|---:|
| 24scene render | PASS（24 / 24） |
| scene quality report | PASS（OK 24 / WARN 0 / FAIL 0） |
| real UI capture | PASS（7 / 7） |
| SCENE-005 official-fact renderer | PASS（1 / 1） |
| official UI AI reconstruction | PASS（0） |
| fake UI | PASS（0） |
| fabricated update button | PASS（0） |
| privacy violation in final crops | PASS（0） |
| neutral frame remaining in official scene | PASS（0） |
| tiny text / overflow / subtitle safe area | PASS（0 / 0 / PASS） |
| visual centroid preflight | PASS（7 / 7） |
| background consistency / blank white slide | PASS / 0 flagged |
| Phase 2 scene/audio QA | PASS（24 scenes / 74 subtitle cues / WARN 0 / FAIL 0） |
| subtitle preflight | PASS（FAIL 0 / WARN 0） |
| CTA preflight | PASS（text clipping 0 / font 60px） |
| ImageGen text QA | PASS（5 scenes / auto_fail 0） |
| production preflight | REVIEW（VOICEVOX query 74 / 74、発音レビュー8件） |

機械レポート: `work/visual_review/scene_quality_report_visual_gate_v3.md`  
contact sheet: `work/visual_review/scene_contact_sheet_v3.png`

## 実画面の確認結果

| Scene | Device | Final asset | 実画面で確認した内容 |
|---|---|---|---|
| SCENE-006 | Android Emulator | `assets/captures/android/android_scene006_line_version.png` | LINE `現在のバージョン 26.14.0` |
| SCENE-009 | iPhone | `assets/captures/iphone/iphone_scene009_ios_version.png` | `iOSバージョン 26.6.1` |
| SCENE-010 | Android Emulator | `assets/captures/android/android_scene010_android_version.png` | `Android バージョン 16` |
| SCENE-013 | iPhone | `assets/captures/iphone/iphone_scene013_line_update.png` | LINEの実表示は`開く`。更新ボタンなし |
| SCENE-014 | Android Emulator | `assets/captures/android/android_scene014_line_update.png` | Google Play検索結果のLINE行は`インストール済`・`開く`。更新ボタンなし |
| SCENE-015 | iPhone | `assets/captures/iphone/iphone_scene015_os_update.png` | `iOSは最新です`、`iOS 26.6.1` |
| SCENE-016 | Android Emulator | `assets/captures/android/android_scene016_os_update.png` | `お使いのシステムは最新の状態です`、`アップデートを確認` |

## 台本・menu差分

- Androidの端末情報入口は`エミュレートされたデバイスについて`。
- AndroidのOS更新入口は`ソフトウェア アップデート`（空白あり）。
- SCENE-014は台本に記録していた`アプリとデバイスの管理`画面ではなく、Google PlayのLINE検索結果の実画面。表示された状態を優先し、更新ボタンを補わない。
- iPhone / Androidのストア画面はいずれも今回の端末では`開く`だった。「更新あり」とは断定しない。

## privacy

最終cropからGoogle account、email、device ID、serial、IMEI、notification、Apple Account、端末名、購入履歴を除外した。raw probeは作業領域に保持し、出力sceneには使っていない。privacy重大指摘は0件。

## 人間承認済み

- 現在の24scene構成を正式採用。Visual Gate v3の人間判定はAPPROVED。
- real UI 7/7、SCENE-005 official-fact renderer、fake UI、AI reconstruction、fabricated update button、privacy FAILはいずれも問題なし。
- F-011は具体的実施日が未発表・未確定というFact boundaryとして承認済み。動画では「11月上旬にサポート終了予定」までに制限する。
- 発音8件は`work/pronunciation_review_v3.wav`を全件聴取し、ALL OK。Episode013のcontext-specific approvalとして記録し、共通辞書と既存audioは変更しない。

## 次の人間確認で残す項目

1. draft Human Gateで、元サイズのSCENE-006/009/010/013/014/015/016の主要行が65歳以上・TV視聴でも読めるか確認する。
2. draft Human Gateで、SCENE-005の公式事実表示と、SCENE-013/014の実表示「開く」が誤認されないことを再確認する。
3. draft buildのsafe-area samplerが背景コンテンツを検出したSCENE-008 / SCENE-012 / SCENE-022の下部180pxを、字幕との重なりと65+ / TV可読性の観点で再確認する。承認済みassetは変更しない。
4. Fact / Privacy / Audio / Subtitleの最終人間確認を完了する。

## 一次情報

- [LINE公式のお知らせ](https://help.line.me/line/smartphone?contentId=200002720&lang=ja)（確認日 2026-09-06）
