# Scene renderer Phase 1.5 quality report

対象: `episodes\011_myna_insurance_scam_call\work\rendered_final_scenes` の 19 シーン

これは画像ラスタとrendererの配置ボックスによる機械判定であり、人間の可読性評価を置き換えない。公式画面の占有率は、実素材の文字画素ではなく配置ボックスのアクティブ領域比である。

判定基準: templateの見出しインク高さ60px未満、公式素材25%未満、主ビジュアル25%未満、小文字帯6本以上、カード4枚以上、空白率92%超、rendererが生成する補助文字40px未満をWARNとした。imagegen_native/gpt_imageは文字が画像内に一体化しているため、見出しラスタ計測を適用せずexact text QAで確認する。blank_white_slide（コンテンツ領域のほぼ白画素率）は66%超をWARN、common background theme（config/visual_theme.json）を適用していないテンプレートシーンで顕著に出る。画像背景プロファイルでは背景画像自身の意図的な白面をblank_white_slideに数えず、raw値はnear_white_ratio_rawへ保持する。cautionのsemantic icon onlyは意図した補助要素としてvisual<25%から除外する。visual balanceは主役の宣言中心がx=650未満またはx=1270超の場合にWARNとする。section labelは意図的な補助文字として除外し、公式引用の出典ラベルは例外候補として明示する。

| Scene | Layout | 見出しインク H | 公式素材率 | 主ビジュアル率 | 重心x | 小文字帯 | <40px | カード | 空白率 | 白面率 | 判定 | WARN |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 001 | layout_01_hero | 0px | 0.0% | 27.5% | 960.0 | 0 | 40px | 0 | 4.1% | — | OK | — |
| 002 | layout_03_visual_text | 107px | 0.0% | 29.3% | 960.0 | 0 | 40px | 0 | 41.6% | 44% | OK | — |
| 004 | layout_02_list | 103px | 0.0% | 0.0% | 960.0 | 1 | 40px | 0 | 26.3% | 33% | OK | — |
| 003 | layout_04_text_official | 62px | 26.5% | 26.5% | 960.0 | 1 | 40px | 0 | 69.1% | 72% | OK | — |
| 005 | layout_08_section | 113px | 0.0% | 3.1% | 960.0 | 1 | 40px | 0 | 43.4% | 45% | OK | — |
| 006 | layout_03_visual_text | 102px | 0.0% | 29.3% | 960.0 | 1 | 40px | 0 | 41.5% | 44% | OK | — |
| 007 | layout_06_caution | 93px | 0.0% | 9.3% | 960.0 | 0 | 40px | 0 | 41.4% | 44% | OK | — |
| 019 | layout_01_hero | 176px | 0.0% | 27.5% | 960.0 | 0 | 40px | 0 | 41.2% | 44% | OK | — |
| 008 | layout_08_section | 114px | 0.0% | 3.1% | 960.0 | 0 | 40px | 0 | 43.1% | 45% | OK | — |
| 009 | layout_02_list | 103px | 0.0% | 0.0% | 960.0 | 1 | 40px | 0 | 26.9% | 33% | OK | — |
| 010 | layout_06_caution | 95px | 0.0% | 9.3% | 960.0 | 0 | 40px | 0 | 41.3% | 44% | OK | — |
| 011 | layout_08_section | 113px | 0.0% | 3.1% | 960.0 | 1 | 40px | 0 | 43.3% | 45% | OK | — |
| 012 | layout_03_visual_text | 176px | 0.0% | 29.3% | 960.0 | 0 | 40px | 0 | 41.4% | 44% | OK | — |
| 013 | layout_01_hero | 161px | 0.0% | 27.5% | 960.0 | 0 | 40px | 0 | 27.0% | 34% | OK | — |
| 014 | layout_01_hero | 161px | 0.0% | 27.5% | 960.0 | 0 | 40px | 0 | 27.1% | 34% | OK | — |
| 015 | layout_06_caution | 95px | 0.0% | 9.3% | 960.0 | 0 | 40px | 0 | 41.7% | 44% | OK | — |
| 016 | layout_05_compare | 101px | 0.0% | 38.9% | 960.0 | 0 | 40px | 2 | 25.6% | 33% | OK | — |
| 017 | layout_07_summary | 99px | 0.0% | 0.0% | 960.0 | 0 | 40px | 0 | 40.8% | 43% | OK | — |
| 018 | layout_01_hero | 0px | 0.0% | 27.5% | 960.0 | 0 | 40px | 0 | 2.7% | — | OK | — |

## 集計

- OK: 19 シーン
- WARN: 0 シーン
- FAIL: 0 シーン
- background profile: adult_digital_soft_image_bg / background_asset_pending: false
- v3 checks: icon_plate_alignment max=0px (FAIL>2px) / double_decoration=0 / subtitle_safe_area=PASS / background_consistency=PASS
- blank_white_slide flagged scenes: 0
- v4 checks: visual_axis_alignment max=0.0px (PASS<=12px) / stacked_panel_alignment max=0.0px (PASS<=12px) / section_pill_anchor=PASS (template x=90px, target <300) / repeated_channel_name=0
- v5 checks: semantic_icon_visual_center=PASS (axis<=4px / glyph-vs-plate<=2px) / measured_icon_scenes=9
- WARNは自動再配置の根拠ではなく、contact sheetで人間が確認する候補である。特に空白率の高いsection/end cardは、余白が意図かどうかを確認する。
- 公式素材の内容・一次情報との一致、実機手順、字幕の同期、音声、プライバシーはこの画像レポートの対象外である。

## 人間確認ポイント

1. 50〜70代が縮小contact sheetではなく、元画像で見出しと公式画面を読めるか。
2. 1シーン1主役になっているか。
3. 公式素材を架空UIとして描き直していないか。
4. 字幕帯に重要な図形・公式画面が侵入していないか。
5. WARNが内容上必要な情報を削りすぎた結果ではないか。
