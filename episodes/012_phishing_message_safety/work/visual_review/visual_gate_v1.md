# Episode 012 Visual Gate v1

確認日: 2026-09-06  
段階: Phase A  
判定: **DESIGN PASS / HUMAN REVIEW REQUIRED**

## 構成カウント

- scene数: **31**（設計目標25〜35の範囲）
- template: **25**
- ImageGen concept / chapter door: **6**
- ImageGen generation calls: **12**（採用6枚、同じ主人公へ統一する置換5回を含む。文字QAによる再生成は0回）
- 5ケースの章扉は、Heroの同じ日本人高齢男性を参照画像として統一。場面だけを通販・宅配・カード・携帯料金・公的通知へ変える。
- 公式情報・公式画面の設計枠: **7 scene slots / 5 source groups**（SCENE-007 / 008 / 012 / 013 / 018 / 022 / 026）
- Phase Aで実際に配置した公式UIキャプチャ: **0**。枠だけを先に設計し、Phase Bで公式ページまたはテスト画面を人間確認後に配置する。
- 再現メッセージ: templateのみ。すべて `再現イメージ`、実在URL・電話番号・氏名・アカウント番号・QR・ロゴなし。
- 共通背景: `config/visual_theme.json` の `adult_digital_soft_image_bg`、`assets/backgrounds/adult_digital_soft_v2.png`、字幕安全帯180px。
- レンダー機械QA: **OK 24 / WARN 7 / FAIL 0**。7 WARNは、Phase Aで公式素材を未配置にした7scene slotsに伴う主ビジュアル面積の警告で、欠落した公式UIを本物として見せるFAILではない。
- `tiny_text`: **0**。`overflow`: **0（設計）**。`case_distinctness`: **PASS**。`case_adds_new_value`: **PASS**。
- `micro_story`: **PASS（設計）**。`core_answer_20s`: **PASS（設計）**。`promise_30s`: **PASS（設計）**。`long_form_depth`: **PASS（机上）**。

## Gate checklist

| 項目 | 判定 | 根拠 |
|---|---|---|
| scene count | PASS | 31 scene、5ケースを扉→再現→公式→確認→結論で分離 |
| 文字サイズ設計 | PASS | headline 88〜120px、main 64〜80px、secondary 52px以上、source 44px以上を指定 |
| tiny text | PASS | URL・確認日・制作用ラベルを画面に出さず、sources.md等へ保持 |
| overflow | PASS（設計） | template text-safe areaと2行上限を指定。レンダー後に機械QAする |
| repetition | LOW | 同じ行動でもケースごとに迷う理由・公式source・視覚素材が異なる |
| official UI integrity | PASS（計画） | 公式UIをAI生成せず、5枠は未配置で停止。Phase Bは実画面のみ |
| privacy | PASS | 架空メッセージに実在の識別情報を入れない。実機はテストアカウント前提 |
| imagegen text | PASS | 6枚の指定見出しを目視確認。余計な文字・ロゴ・政府マーク・UIなし |
| background | PASS | image backgroundを全面使用し、二重装飾・白一色を避ける |
| micro story | PASS（設計） | 0〜8秒問題、20秒以内核心、30秒以内5場面の約束 |
| CTA | PASS（設計） | 中盤1回・7秒以内、終了はEpisode 011文言を再利用。動画内疑似subscribeなし |
| End Screen | PASS（設計） | SCENE-031右側45%を予約し、登録要素はStudio側へ分離 |

## 人間確認待ち

1. contact sheet全31枚の重心・TV縮小可読性・ケース間の見た目の差。
2. 公式5枠に入れるページ範囲と、公式UIを使う場合のキャプチャ。
3. ImageGen概念6枚の採用可否。採用する場合は公開時のAI開示を `containsSyntheticMedia=true` として人間承認する。
4. Apple Event後（2026-09-10 JST）の公開順・リンク再確認。
