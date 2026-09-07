# Scene renderer Phase 1.5 quality report

対象: `episodes\002_myna_app\work\efficiency_test_v2` の 35 シーン

これは画像ラスタとrendererの配置ボックスによる機械判定であり、人間の可読性評価を置き換えない。公式画面の占有率は、実素材の文字画素ではなく配置ボックスのアクティブ領域比である。

判定基準: 見出しインク高さ60px未満、公式素材25%未満、主ビジュアル25%未満、小文字帯6本以上、カード4枚以上、空白率92%超、rendererが生成する補助文字40px未満をWARNとした。section labelは意図的な補助文字として除外し、公式引用の出典ラベルは例外候補として明示する。

| Scene | Layout | 見出しインク H | 公式素材率 | 主ビジュアル率 | 小文字帯 | <40px | カード | 空白率 | 判定 | WARN |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 001 | layout_03_visual_text | 107px | 29.3% | 29.3% | 1 | 40px | 0 | 72.8% | OK | — |
| 002 | layout_06_caution | 67px | 0.0% | 9.3% | 1 | 40px | 0 | 86.5% | WARN | visual<25% (9.3%) |
| 003 | layout_02_list | 103px | 0.0% | 0.0% | 1 | 40px | 0 | 90.7% | OK | — |
| 004 | layout_03_visual_text | 109px | 0.0% | 29.3% | 1 | 40px | 0 | 65.2% | OK | — |
| 005 | layout_04_text_official | 102px | 26.5% | 26.5% | 1 | 40px | 0 | 85.9% | OK | — |
| 006 | layout_05_compare | 100px | 0.0% | 43.0% | 1 | 40px | 2 | 52.8% | OK | — |
| 007 | layout_08_section | 114px | 0.0% | 3.1% | 1 | 40px | 0 | 91.9% | OK | — |
| 008 | layout_05_compare | 98px | 25.5% | 43.0% | 1 | 40px | 2 | 69.2% | OK | — |
| 009 | layout_04_text_official | 100px | 26.5% | 26.5% | 8 | 40px | 0 | 85.3% | WARN | small-text proxy (8 bands) |
| 010 | layout_05_compare | 97px | 25.5% | 43.0% | 1 | 40px | 2 | 75.3% | OK | — |
| 011 | layout_01_hero | 108px | 0.0% | 27.5% | 1 | 40px | 0 | 59.4% | OK | — |
| 012 | layout_03_visual_text | 103px | 0.0% | 29.3% | 1 | 40px | 0 | 68.2% | OK | — |
| 013 | layout_04_text_official | 105px | 26.5% | 26.5% | 1 | 40px | 0 | 76.4% | OK | — |
| 014 | layout_04_text_official | 102px | 26.5% | 26.5% | 1 | 18px | 0 | 74.6% | WARN | <40px helper text (18px) |
| 015 | layout_04_text_official | 103px | 26.5% | 26.5% | 1 | 40px | 0 | 75.9% | OK | — |
| 016 | layout_02_list | 100px | 0.0% | 0.0% | 1 | 40px | 0 | 89.7% | OK | — |
| 017 | layout_06_caution | 80px | 26.4% | 26.4% | 1 | 18px | 0 | 84.0% | WARN | <40px helper text (18px) |
| 018 | layout_05_compare | 94px | 12.7% | 43.0% | 1 | 18px | 2 | 62.0% | WARN | official<25% (12.7%), <40px helper text (18px) |
| 019 | layout_06_caution | 81px | 0.0% | 9.3% | 1 | 40px | 0 | 86.2% | WARN | visual<25% (9.3%) |
| 020 | layout_08_section | 115px | 0.0% | 3.1% | 1 | 40px | 0 | 91.1% | OK | — |
| 021 | layout_04_text_official | 103px | 26.5% | 26.5% | 4 | 40px | 0 | 80.2% | OK | — |
| 022 | layout_04_text_official | 107px | 26.5% | 26.5% | 1 | 40px | 0 | 67.8% | OK | — |
| 023 | layout_06_caution | 80px | 26.4% | 26.4% | 5 | 40px | 0 | 84.2% | OK | — |
| 024 | layout_02_list | 99px | 0.0% | 0.0% | 1 | 40px | 0 | 91.5% | OK | — |
| 025 | layout_06_caution | 70px | 0.0% | 9.3% | 1 | 40px | 0 | 85.6% | WARN | visual<25% (9.3%) |
| 026 | layout_08_section | 113px | 0.0% | 3.1% | 1 | 40px | 0 | 91.7% | OK | — |
| 027 | layout_05_compare | 99px | 25.5% | 43.0% | 1 | 40px | 2 | 69.7% | OK | — |
| 028 | layout_03_visual_text | 103px | 29.3% | 29.3% | 2 | 40px | 0 | 72.7% | OK | — |
| 029 | layout_06_caution | 80px | 26.4% | 26.4% | 2 | 40px | 0 | 84.7% | OK | — |
| 030 | layout_06_caution | 81px | 26.4% | 26.4% | 6 | 40px | 0 | 84.1% | WARN | small-text proxy (6 bands) |
| 031 | layout_06_caution | 81px | 26.4% | 26.4% | 4 | 40px | 0 | 85.0% | OK | — |
| 032 | layout_07_summary | 99px | 0.0% | 0.0% | 2 | 40px | 0 | 91.9% | OK | — |
| 033 | layout_07_summary | 103px | 0.0% | 0.0% | 2 | 40px | 0 | 89.5% | OK | — |
| 034 | layout_01_hero | 112px | 0.0% | 27.5% | 2 | 40px | 0 | 59.5% | OK | — |
| 035 | layout_01_hero | 112px | 0.0% | 27.5% | 2 | 40px | 0 | 58.9% | OK | — |

## 集計

- OK: 27 シーン
- WARN: 8 シーン
- FAIL: 0 シーン
- WARNは自動再配置の根拠ではなく、contact sheetで人間が確認する候補である。特に空白率の高いsection/end cardは、余白が意図かどうかを確認する。
- 公式素材の内容・一次情報との一致、実機手順、字幕の同期、音声、プライバシーはこの画像レポートの対象外である。

## 人間確認ポイント

1. 50〜70代が縮小contact sheetではなく、元画像で見出しと公式画面を読めるか。
2. 1シーン1主役になっているか。
3. 公式素材を架空UIとして描き直していないか。
4. 字幕帯に重要な図形・公式画面が侵入していないか。
5. WARNが内容上必要な情報を削りすぎた結果ではないか。
