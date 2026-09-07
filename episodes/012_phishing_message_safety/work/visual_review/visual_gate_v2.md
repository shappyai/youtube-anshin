# Episode 012 Visual Gate v2

確認日: 2026-09-06  
段階: Phase A  
v1 human gate: **REJECTED_WITH_COMMON_RENDERER_FIX**  
v2 mechanical design gate: **PASS / HUMAN REVIEW REQUIRED**

## 1. v1の根本原因

対象7sceneの `layout_04_text_official` で、公式素材が未配置のときにPillow rendererの空き枠が従来の概念パネル・確認バッジへフォールバックしていた。HTML/CSS側にも未配置の公式枠を完成形として表す分岐がなく、公式visual slotの代わりに意味のない大きなチェックマークが入り、前景の重心が左へ寄った。Episode012固有の描画指定ではなく、共通rendererのfallback回帰として扱った。

## 2. 共通renderer / visual policyの修正

- `scripts/scene_renderer.py`: `layout_04_text_official`を左右2カラムへ統一。左は短い要点カード、右は公式素材または実寸に近いneutral browser/phone frameを描画する。公式素材が未配置でも、viewer-facingのplaceholder・pending・URL・架空UI文字は描かない。
- `scripts/scene_renderer.py`: `official_visual_variant`、`visual_points`、`official_entry_options`をscene dataから読む方式に変更。チェック・感嘆符・疑問符・×などの装飾glyphを`draw_symbol` / `draw_badge`が拒否し、意味のないglyph fallbackを再発させない。
- `templates/scenes/layout_04_text_official.html` / `templates/scenes/styles.css`: HTML/CSSも同じ左右構成とneutral frameを使う。空の公式slotはneutral frameとして表示し、制作用文言を表示しない。
- `scripts/scene_quality_report.py`: `visual_centroid_preflight`を追加。背景差分から`occupied_bbox`、`visual_centroid_x`、`left_visual_weight`、`right_visual_weight`を測定し、公式2カラムで右weight 20%以上、重心x=768〜1152を満たさない場合はWARNではなくFAILにする。
- `templates/scenes/README.md` / `config/icon_catalog.json`: `no_oversized_decorative_checkmark`、`no_meaningless_filler_icon`、公式未配置時のneutral frame、icon size policy、visual centroid QAを恒久ルールとして追加。

## 3. 対象7sceneの修正

| Scene | 左側 | 右側 | v2判定 |
|---:|---|---|---|
| 007 | 「普段使う名前でも、急がない」「メールのリンクから更新しない」 | 国民生活センター公式ページを入れるbrowser frame | チェックマークなし / PASS |
| 008 | 「公式アプリを自分で開く」「お知らせ・注文履歴を確認」 | 公式アプリ・サイトを入れるphone frame | チェックマークなし / PASS |
| 012 | 日本郵便・フィッシング対策協議会の注意点を短く整理 | 公式注意喚起を入れるbrowser frame | チェックマークなし / PASS |
| 013 | 公式アプリ・公式サイト・手元の不在票をMaterial Symbols Rounded付き3カードで表示 | 公式入口を入れるphone frame | チェックマークなし / PASS |
| 018 | 「メッセージからログインしない」「カード番号・暗証番号を入力しない」 | カード会社公式入口・注意喚起を入れるbrowser frame | チェックマークなし / PASS |
| 022 | 「SMSではなく公式側で確認」「請求金額は公式アプリ・サイトで見る」 | 通信会社公式ページ・アプリを入れるbrowser frame | チェックマークなし / PASS |
| 026 | 国税庁・消費者庁の要点を短く整理 | 公的機関の公式案内を入れるbrowser frame | チェックマークなし / PASS |

Phase Aでは公式素材7枠を未配置のまま保持している（planned 7 / captured 0）。neutral frameはPhase Bの実際の公式ページ・テスト画面へ差し替えるためのレイアウト枠であり、公式UIの再現ではない。政府ロゴ・実在URL・電話番号・個人情報は生成していない。

## 4. Visual Gate v2 QA

- 31/31 scene render: **PASS**、全scene 1920×1080、破損なし。
- `scene_quality_report_v2.md`: **31 OK / 0 WARN / 0 FAIL**。
- `oversized_checkmark_count=0`
- `decorative_checkmark_as_main_visual=0`
- `meaningless_filler_icon=0`
- `left_bias_fail=0`
- `tiny_text=0`
- `overflow=0`
- `visual_centroid_preflight`: **PASS**、7/7 scene checked、right weight minimum 38.27%、重心x range 892.93〜965.22。

### visual centroid実測

| Scene | occupied_bbox | visual_centroid_x | left_visual_weight | right_visual_weight | left_bias_fail |
|---:|---|---:|---:|---:|---:|
| 007 | [89, 139, 1812, 838] | 965.22 | 0.5286 | 0.4714 | 0 |
| 008 | [89, 139, 1812, 832] | 933.81 | 0.5576 | 0.4424 | 0 |
| 012 | [89, 139, 1812, 838] | 918.86 | 0.5664 | 0.4336 | 0 |
| 013 | [89, 139, 1812, 832] | 931.82 | 0.6173 | 0.3827 | 0 |
| 018 | [89, 139, 1812, 838] | 955.29 | 0.5354 | 0.4646 | 0 |
| 022 | [89, 139, 1812, 838] | 907.65 | 0.5713 | 0.4287 | 0 |
| 026 | [89, 139, 1812, 838] | 892.93 | 0.5808 | 0.4192 | 0 |

## 5. 他24scene regression

- v1 baseline `work/phase_a_render/final/` とv2を比較し、対象7scene以外の24sceneはSHA-256がすべて一致した。
- 24sceneの欠落なし、v2出力サイズは全31sceneで1920×1080。対象7sceneだけが共通renderer修正により更新された。
- ImageGen chapter doorのSCENE-001 / 005 / 010 / 016 / 020 / 024は、v1 baseline・v2出力・`assets/generated_ai/`のSHA-256がそれぞれ一致。再生成していない。

## 6. 再生成成果物とHuman Gate

- contact sheet: `episodes/012_phishing_message_safety/work/visual_review/scene_contact_sheet_v2.png`
- quality report: `episodes/012_phishing_message_safety/work/visual_review/scene_quality_report_v2.md`
- v1 contact sheetとv1 quality reportは履歴として保持し、上書きしていない。
- v2は人間確認待ち。neutral frameの完成形バランス、50〜70代・TV縮小時の可読性、Phase Bで入れる公式素材範囲を人間が確認する。

## 7. Phase A stop

今回の停止位置はPhase A Visual Gate v2。VOICEVOX、字幕、draft、final、thumbnail、YouTube upload、schedule、End Screen設定はまだ開始していない。
