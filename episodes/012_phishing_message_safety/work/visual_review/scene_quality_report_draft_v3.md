# Scene renderer draft_v3 quality report

対象: `episodes\012_phishing_message_safety\work\rendered_final_scenes` の 30 シーン

これは画像ラスタとrendererの配置ボックスによる機械判定であり、人間の可読性評価を置き換えない。公式画面の占有率は、実素材の文字画素ではなく配置ボックスのアクティブ領域比である。公式素材未配置のlayout_04_text_officialは、左の要点と右のneutral visual frameを前景として測定する。

判定基準: templateの見出しインク高さ60px未満、公式素材25%未満、主ビジュアル25%未満、小文字帯6本以上、カード4枚以上、空白率92%超、rendererが生成する補助文字44px未満をWARNとした。imagegen_native/gpt_imageは文字が画像内に一体化しているため、見出しラスタ計測を適用せずexact text QAで確認する。blank_white_slide（コンテンツ領域のほぼ白画素率）は66%超をWARN、common background theme（config/visual_theme.json）を適用していないテンプレートシーンで顕著に出る。画像背景プロファイルでは背景画像自身の意図的な白面をblank_white_slideに数えず、raw値はnear_white_ratio_rawへ保持する。cautionのsemantic icon onlyは意図した補助要素としてvisual<25%から除外する。visual balanceは主役の宣言中心がx=650未満またはx=1270超の場合にWARNとする。公式2カラムのvisual_centroid_preflightは、前景差分の重心xが768〜1152、右visual weightが20%以上であることを確認する。section labelは意図的な補助文字として除外し、公式引用の出典ラベルは例外候補として明示する。

| Scene | Layout | 見出しインク H | 公式素材率 | 主ビジュアル率 | 重心x | 小文字帯 | <44px | カード | 空白率 | 白面率 | 判定 | WARN |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 001 | layout_01_hero | 102px | 0.0% | 27.5% | 960.0 | 2 | 44px | 0 | 30.0% | — | OK | — |
| 002 | layout_01_hero | 179px | 0.0% | 27.5% | 960.0 | 0 | 44px | 0 | 41.4% | 44% | OK | — |
| 003 | layout_02_list | 102px | 0.0% | 0.0% | 960.0 | 1 | 44px | 0 | 26.3% | 32% | OK | — |
| 004 | layout_03_visual_text | 179px | 0.0% | 29.3% | 960.0 | 0 | 44px | 0 | 42.1% | 44% | OK | — |
| 005 | layout_01_hero | 146px | 0.0% | 27.5% | 960.0 | 1 | 44px | 0 | 28.5% | — | OK | — |
| 006 | layout_03_visual_text | 102px | 0.0% | 29.3% | 960.0 | 1 | 44px | 0 | 40.9% | 43% | OK | — |
| 007 | layout_04_text_official | 103px | 25.8% | 50.6% | 960.0 | 1 | 44px | 0 | 50.1% | 47% | OK | — |
| 008 | layout_04_text_official | 105px | 0.0% | 50.6% | 960.0 | 1 | 44px | 0 | 40.8% | 40% | OK | — |
| 009 | layout_07_summary | 99px | 0.0% | 0.0% | 960.0 | 1 | 44px | 0 | 40.7% | 42% | OK | — |
| 010 | layout_01_hero | 165px | 0.0% | 27.5% | 960.0 | 4 | 44px | 0 | 30.3% | — | OK | — |
| 011 | layout_03_visual_text | 161px | 0.0% | 29.3% | 960.0 | 0 | 44px | 0 | 40.6% | 43% | OK | — |
| 012 | layout_04_text_official | 102px | 25.8% | 50.6% | 960.0 | 3 | 44px | 0 | 46.3% | 44% | OK | — |
| 013 | layout_04_text_official | 102px | 0.0% | 44.2% | 960.0 | 1 | 44px | 0 | 22.9% | 30% | OK | — |
| 014 | layout_07_summary | 99px | 0.0% | 0.0% | 960.0 | 1 | 44px | 0 | 40.2% | 42% | OK | — |
| 015 | layout_06_caution | 95px | 0.0% | 9.3% | 960.0 | 0 | 44px | 0 | 41.0% | 43% | OK | — |
| 016 | layout_01_hero | 122px | 0.0% | 27.5% | 960.0 | 2 | 44px | 0 | 30.0% | — | OK | — |
| 017 | layout_03_visual_text | 103px | 0.0% | 29.3% | 960.0 | 1 | 44px | 0 | 41.1% | 43% | OK | — |
| 018 | layout_04_text_official | 103px | 25.8% | 50.6% | 960.0 | 2 | 44px | 0 | 47.3% | 45% | OK | — |
| 019 | layout_07_summary | 99px | 0.0% | 0.0% | 960.0 | 1 | 44px | 0 | 39.9% | 42% | OK | — |
| 020 | layout_01_hero | 127px | 0.0% | 27.5% | 960.0 | 3 | 44px | 0 | 30.2% | — | OK | — |
| 021 | layout_03_visual_text | 179px | 0.0% | 29.3% | 960.0 | 0 | 44px | 0 | 40.9% | 43% | OK | — |
| 022 | layout_04_text_official | 103px | 25.8% | 50.6% | 960.0 | 1 | 44px | 0 | 46.9% | 45% | OK | — |
| 023 | layout_06_caution | 91px | 0.0% | 9.3% | 960.0 | 0 | 44px | 0 | 40.7% | 43% | OK | — |
| 024 | layout_01_hero | 143px | 0.0% | 27.5% | 960.0 | 3 | 44px | 0 | 28.4% | — | OK | — |
| 025 | layout_03_visual_text | 60px | 0.0% | 29.3% | 960.0 | 1 | 44px | 0 | 40.9% | 43% | OK | — |
| 026 | layout_04_text_official | 103px | 25.8% | 50.6% | 960.0 | 1 | 44px | 0 | 44.9% | 43% | OK | — |
| 027 | layout_07_summary | 99px | 0.0% | 0.0% | 960.0 | 1 | 44px | 0 | 39.7% | 41% | OK | — |
| 028 | layout_02_list | 100px | 0.0% | 0.0% | 960.0 | 0 | 44px | 0 | 25.8% | 32% | OK | — |
| 029 | layout_05_compare | 92px | 0.0% | 38.9% | 960.0 | 0 | 44px | 2 | 25.4% | 33% | OK | — |
| 030 | layout_07_summary | 99px | 0.0% | 0.0% | 960.0 | 0 | 44px | 0 | 40.9% | 43% | OK | — |

## Visual centroid preflight

公式素材スロットを持つtemplateのlayout_04_text_officialについて、背景画像を差し引いた前景差分から左右の占有率と重心を測定した。`occupied_bbox`は前景差分の概算bbox、`visual_centroid_x`は左右ボックス内の加重重心である。
- SCENE-007: status=PASS / occupied_bbox=[89, 139, 1812, 832] / visual_centroid_x=1119.96 / left_visual_weight=0.3127 / right_visual_weight=0.6873 / left_bias_fail=0 / reason=—
- SCENE-008: status=PASS / occupied_bbox=[89, 139, 1812, 832] / visual_centroid_x=1018.85 / left_visual_weight=0.4333 / right_visual_weight=0.5667 / left_bias_fail=0 / reason=—
- SCENE-012: status=PASS / occupied_bbox=[89, 139, 1812, 832] / visual_centroid_x=1067.93 / left_visual_weight=0.3486 / right_visual_weight=0.6514 / left_bias_fail=0 / reason=—
- SCENE-013: status=PASS / occupied_bbox=None / visual_centroid_x=960.0 / left_visual_weight=0.5000 / right_visual_weight=0.5000 / left_bias_fail=0 / reason=centered semantic entry options
- SCENE-018: status=PASS / occupied_bbox=[89, 139, 1812, 832] / visual_centroid_x=1100.66 / left_visual_weight=0.3419 / right_visual_weight=0.6581 / left_bias_fail=0 / reason=—
- SCENE-022: status=PASS / occupied_bbox=[89, 139, 1812, 832] / visual_centroid_x=1048.68 / left_visual_weight=0.3767 / right_visual_weight=0.6233 / left_bias_fail=0 / reason=—
- SCENE-026: status=PASS / occupied_bbox=[89, 139, 1812, 832] / visual_centroid_x=1101.12 / left_visual_weight=0.3171 / right_visual_weight=0.6829 / left_bias_fail=0 / reason=—

## 集計

- OK: 30 シーン
- WARN: 0 シーン
- FAIL: 0 シーン
- background profile: adult_digital_soft_image_bg / background_asset_pending: false
- permanent visual policy: oversized_checkmark_count=0 / decorative_checkmark_as_main_visual=0 / meaningless_filler_icon=0 / left_bias_fail=0 / tiny_text=0 / overflow=0
- visual_centroid_preflight: PASS / checked=7 / right_weight_min=0.20 / centroid_range=768..1152
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
