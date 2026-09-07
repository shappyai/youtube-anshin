# Scene renderer Phase 1.5 quality report

対象: `episodes\005_google_photos_delete\work\phase_b_review\rendered_scenes` の 25 シーン

これは画像ラスタとrendererの配置ボックスによる機械判定であり、人間の可読性評価を置き換えない。公式画面の占有率は、実素材の文字画素ではなく配置ボックスのアクティブ領域比である。

判定基準: 見出しインク高さ60px未満、公式素材25%未満、主ビジュアル25%未満、小文字帯6本以上、カード4枚以上、空白率92%超、rendererが生成する補助文字40px未満をWARNとした。visual balanceは主役の宣言中心がx=650未満またはx=1270超の場合にWARNとする。section labelは意図的な補助文字として除外し、公式引用の出典ラベルは例外候補として明示する。

| Scene | Layout | 見出しインク H | 公式素材率 | 主ビジュアル率 | 重心x | 小文字帯 | <40px | カード | 空白率 | 判定 | WARN |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 001 | layout_03_visual_text | 0px | 0.0% | 29.3% | 960.0 | 6 | 40px | 0 | 7.0% | WARN | headline<60px (0px), small-text proxy (6 bands) |
| 002 | layout_02_list | 103px | 0.0% | 0.0% | 960.0 | 1 | 40px | 0 | 92.1% | WARN | high blank (92.1%) |
| 003 | layout_03_visual_text | 80px | 0.0% | 29.3% | 960.0 | 2 | 40px | 0 | 4.9% | OK | — |
| 004 | layout_04_text_official | 101px | 26.5% | 26.5% | 960.0 | 2 | 40px | 0 | 90.0% | OK | — |
| 005 | layout_08_section | 107px | 0.0% | 3.1% | 960.0 | 1 | 40px | 0 | 90.9% | OK | — |
| 006 | layout_04_text_official | 89px | 26.5% | 26.5% | 960.0 | 1 | 40px | 0 | 69.9% | OK | — |
| 007 | layout_05_compare | 102px | 0.0% | 43.0% | 960.0 | 1 | 40px | 2 | 51.5% | OK | — |
| 008 | layout_04_text_official | 100px | 26.5% | 26.5% | 960.0 | 1 | 40px | 0 | 92.7% | WARN | high blank (92.7%) |
| 009 | layout_06_caution | 85px | 0.0% | 9.3% | 960.0 | 2 | 40px | 0 | 86.2% | WARN | visual<25% (9.3%) |
| 010 | layout_08_section | 113px | 0.0% | 3.1% | 960.0 | 1 | 40px | 0 | 91.1% | OK | — |
| 011 | layout_05_compare | 100px | 0.0% | 43.0% | 960.0 | 1 | 40px | 2 | 50.7% | OK | — |
| 012 | layout_04_text_official | 102px | 26.5% | 26.5% | 960.0 | 5 | 40px | 0 | 88.3% | OK | — |
| 013 | layout_03_visual_text | 87px | 0.0% | 29.3% | 960.0 | 7 | 40px | 0 | 7.9% | WARN | small-text proxy (7 bands) |
| 014 | layout_04_text_official | 100px | 26.5% | 26.5% | 960.0 | 3 | 40px | 0 | 91.1% | OK | — |
| 015 | layout_05_compare | 111px | 0.0% | 43.0% | 960.0 | 1 | 40px | 2 | 50.5% | OK | — |
| 016 | layout_03_visual_text | 81px | 0.0% | 29.3% | 960.0 | 1 | 40px | 0 | 64.4% | OK | — |
| 017 | layout_03_visual_text | 0px | 0.0% | 29.3% | 960.0 | 0 | 40px | 0 | 2.9% | WARN | headline<60px (0px) |
| 018 | layout_04_text_official | 100px | 26.5% | 26.5% | 960.0 | 13 | 40px | 0 | 88.6% | WARN | small-text proxy (13 bands) |
| 019 | layout_04_text_official | 102px | 26.5% | 26.5% | 960.0 | 9 | 40px | 0 | 89.6% | WARN | small-text proxy (9 bands) |
| 020 | layout_05_compare | 100px | 0.0% | 43.0% | 960.0 | 1 | 40px | 2 | 50.9% | OK | — |
| 021 | layout_08_section | 103px | 0.0% | 3.1% | 960.0 | 1 | 40px | 0 | 90.5% | OK | — |
| 022 | layout_04_text_official | 100px | 26.5% | 26.5% | 960.0 | 12 | 40px | 0 | 91.1% | WARN | small-text proxy (12 bands) |
| 023 | layout_06_caution | 69px | 0.0% | 9.3% | 960.0 | 1 | 40px | 0 | 86.5% | WARN | visual<25% (9.3%) |
| 024 | layout_07_summary | 98px | 0.0% | 0.0% | 960.0 | 2 | 40px | 0 | 89.4% | OK | — |
| 025 | layout_03_visual_text | 0px | 0.0% | 29.3% | 960.0 | 0 | 40px | 0 | 2.7% | WARN | headline<60px (0px) |

## 集計

- OK: 14 シーン
- WARN: 11 シーン
- FAIL: 0 シーン
- WARNは自動再配置の根拠ではなく、contact sheetで人間が確認する候補である。特に空白率の高いsection/end cardは、余白が意図かどうかを確認する。
- 公式素材の内容・一次情報との一致、実機手順、字幕の同期、音声、プライバシーはこの画像レポートの対象外である。

## 人間確認ポイント

1. 50〜70代が縮小contact sheetではなく、元画像で見出しと公式画面を読めるか。
2. 1シーン1主役になっているか。
3. 公式素材を架空UIとして描き直していないか。
4. 字幕帯に重要な図形・公式画面が侵入していないか。
5. WARNが内容上必要な情報を削りすぎた結果ではないか。
