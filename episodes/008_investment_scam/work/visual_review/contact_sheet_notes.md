# Episode 008 contact sheet QA note（2026-09-05）

contact sheet: work/visual_review/scene_contact_sheet.png（18 scene + 説明）

## 機械QA（scene_quality_report）
- OK 9 / WARN 9 / FAIL 0
- WARNの内訳:
  - section扉（SCENE-004/006/008/013）: "high blank" — GPT画像フルブリード背景のため、レイアウトボックス計測では空白率高めに出る。実画像は背景が全面にある（目視確認済み）。
  - caution（SCENE-007/010/011）: "visual<25%" — semantic icon円のみのため。アイコン占有は規定内（15%未満）。
  - list（SCENE-016/018）: "high blank" — リストレイアウトの意図的な余白。
- 見出しインク高: 全scene 71〜105px（規定 ≥80px 目安に対してSCENE-015の71pxは比較カード内タイトル。要人間確認）。
- 小文字帯: 最大4本・40px級のみ（rendererの補助文字。字幕帯侵入なし）。

## imagegen_native text QA（目視・5枚）
- SCENE-001「その投資広告、本物？」+補助行: PASS（誤字なし）
- SCENE-004「広告の有名人を、そのまま信用しない」+「まずは、そのまま信じない」: PASS
- SCENE-006「本人が、すすめているとは、限らない」+補助: PASS
- SCENE-008「LINEに誘導されたら、一度、止まる」+補助: PASS
- SCENE-013「送金する前に、登録と振込先を確認」+補助: PASS
- 実在人物・実在UI・QR・政府マーク: なし。顔はシルエット/ぼかし。
- 原本1672×941のままassets/generated_aiに保持（render時に1920×1080正規化）。

## 字幕帯
- 全scene 下部180pxに重要要素なし（renderer構造保証＋目視確認）。

## 人間確認ポイント（Gate 1/2共通）
1. 全sceneの元画像で見出しが読めるか（縮小表示ではなく）。
2. SCENE-015比較カードの文字量（「指定されたら、振り込まないで（…）」はPhase Bで短縮候補）。
3. section扉の進行pill（1/3・2/3・3/3）をPhase BでCodex overlay追加（現状なし）。
4. 詐欺画面が「本物のUI」と誤認されないか（SCENE-008の一時停止マーク・SCENE-013の架空振込画面）。
