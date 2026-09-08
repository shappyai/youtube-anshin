# Scene renderer Visual Gate v2 quality report

対象: `episodes\015_google_2fa_check\work\rendered_final_scenes` の 12 シーン

これは画像ラスタとrendererの配置ボックスによる機械判定であり、人間の可読性評価を置き換えない。公式画面の占有率は、実素材の文字画素ではなく配置ボックスのアクティブ領域比である。公式素材未配置のlayout_04_text_officialは、左の要点と右のneutral visual frameを前景として測定する。

判定基準: templateの見出しインク高さ60px未満、公式素材25%未満、主ビジュアル25%未満、小文字帯6本以上、カード4枚以上、空白率92%超、rendererが生成する補助文字44px未満をWARNとした。imagegen_native/gpt_imageは文字が画像内に一体化しているため、見出しラスタ計測を適用せずexact text QAで確認する。blank_white_slide（コンテンツ領域のほぼ白画素率）は66%超をWARN、common background theme（config/visual_theme.json）を適用していないテンプレートシーンで顕著に出る。画像背景プロファイルでは背景画像自身の意図的な白面をblank_white_slideに数えず、raw値はnear_white_ratio_rawへ保持する。cautionのsemantic icon onlyは意図した補助要素としてvisual<25%から除外する。visual balanceは主役の宣言中心がx=650未満またはx=1270超の場合にWARNとする。公式2カラムのvisual_centroid_preflightは、前景差分の重心xが768〜1152、右visual weightが20%以上であることを確認する。section labelは意図的な補助文字として除外し、公式引用の出典ラベルは例外候補として明示する。

| Scene | Layout | 見出しインク H | 公式素材率 | 主ビジュアル率 | 重心x | 小文字帯 | <44px | カード | 空白率 | 白面率 | 判定 | WARN |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 001 | layout_03_visual_text | 206px | 0.0% | 29.3% | 960.0 | 1 | 44px | 0 | 12.9% | 17% | OK | — |
| 002 | layout_02_list | 110px | 0.0% | 0.0% | 960.0 | 1 | 44px | 0 | 41.8% | 18% | OK | — |
| 003 | layout_08_section | 113px | 0.0% | 3.1% | 960.0 | 3 | 44px | 0 | 12.8% | 17% | OK | — |
| 004 | layout_04_text_official | 98px | 25.8% | 50.6% | 1240.0 | 1 | 44px | 0 | 56.3% | 60% | FAIL | visual_centroid_preflight FAIL (background comparison unavailable) |
| 005 | layout_03_visual_text | 177px | 0.0% | 29.3% | 960.0 | 2 | 44px | 0 | 12.4% | 17% | OK | — |
| 006 | layout_08_section | 107px | 0.0% | 3.1% | 960.0 | 3 | 44px | 0 | 13.4% | 17% | OK | — |
| 007 | layout_04_text_official | 99px | 25.8% | 50.6% | 1240.0 | 1 | 44px | 0 | 63.1% | 66% | FAIL | visual_centroid_preflight FAIL (background comparison unavailable) |
| 008 | layout_06_caution | 91px | 0.0% | 9.3% | 960.0 | 3 | 44px | 0 | 13.4% | 17% | OK | — |
| 009 | layout_08_section | 113px | 0.0% | 3.1% | 960.0 | 5 | 44px | 0 | 13.6% | 17% | OK | — |
| 010 | layout_04_text_official | 98px | 25.8% | 50.6% | 1240.0 | 1 | 44px | 0 | 70.7% | 72% | FAIL | blank white slide (72% near-white), visual_centroid_preflight FAIL (background comparison unavailable) |
| 011 | layout_06_caution | 95px | 0.0% | 9.3% | 960.0 | 4 | 44px | 0 | 13.1% | 17% | OK | — |
| 012 | layout_07_summary | 98px | 0.0% | 0.0% | 960.0 | 1 | 44px | 0 | 12.6% | 18% | OK | — |

## Visual centroid preflight

公式素材スロットを持つtemplateのlayout_04_text_officialについて、背景画像を差し引いた前景差分から左右の占有率と重心を測定した。`occupied_bbox`は前景差分の概算bbox、`visual_centroid_x`は左右ボックス内の加重重心である。
- SCENE-004: status=FAIL / occupied_bbox=None / visual_centroid_x=None / left_visual_weight=0.0000 / right_visual_weight=0.0000 / left_bias_fail=1 / reason=background comparison unavailable
- SCENE-007: status=FAIL / occupied_bbox=None / visual_centroid_x=None / left_visual_weight=0.0000 / right_visual_weight=0.0000 / left_bias_fail=1 / reason=background comparison unavailable
- SCENE-010: status=FAIL / occupied_bbox=None / visual_centroid_x=None / left_visual_weight=0.0000 / right_visual_weight=0.0000 / left_bias_fail=1 / reason=background comparison unavailable

## 集計

- OK: 9 シーン
- WARN: 0 シーン
- FAIL: 3 シーン
- background profile: adult_digital_soft_background / background_asset_pending: false
- permanent visual policy: oversized_checkmark_count=0 / decorative_checkmark_as_main_visual=0 / meaningless_filler_icon=0 / left_bias_fail=3 / tiny_text=0 / overflow=0
- visual_centroid_preflight: FAIL / checked=3 / right_weight_min=0.20 / centroid_range=768..1152
- v3 checks: icon_plate_alignment max=0px (FAIL>2px) / double_decoration=0 / subtitle_safe_area=PASS / background_consistency=PASS
- blank_white_slide flagged scenes: 1
- v4 checks: visual_axis_alignment max=0.0px (PASS<=12px) / stacked_panel_alignment max=0.0px (PASS<=12px) / section_pill_anchor=PASS (template x=100px, target <300) / repeated_channel_name=0
- v5 checks: semantic_icon_visual_center=PASS (axis<=4px / glyph-vs-plate<=2px) / measured_icon_scenes=0
- WARNは自動再配置の根拠ではなく、contact sheetで人間が確認する候補である。特に空白率の高いsection/end cardは、余白が意図かどうかを確認する。
- 公式素材の内容・一次情報との一致、実機手順、字幕の同期、音声、プライバシーはこの画像レポートの対象外である。

## 人間確認ポイント

1. 50〜70代が縮小contact sheetではなく、元画像で見出しと公式画面を読めるか。
2. 1シーン1主役になっているか。
3. 公式素材を架空UIとして描き直していないか。
4. 字幕帯に重要な図形・公式画面が侵入していないか。
5. WARNが内容上必要な情報を削りすぎた結果ではないか。
