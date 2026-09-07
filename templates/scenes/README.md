# Scene templates

共通サイズは1920x1080。下部180pxは字幕安全領域で、styles.cssが内容をそこへ置かない構造を持つ。

| template | 用途 |
|---|---|
| layout_01_hero | 結論・冒頭・CTA |
| layout_02_list | 3〜5項目の一覧 |
| layout_03_visual_text | 図解・イラストと説明 |
| layout_04_text_official | 説明と公式スクリーンショット |
| layout_05_compare | 左右比較 |
| layout_06_caution | 注意・安心・相談導線 |
| layout_07_summary | まとめ・今やること |
| layout_08_section | セクション見出し |

Phase 1.5/Phase 2では、見出しを80〜100px級、強調時を100〜140px級、二次説明を48〜60px級として扱い、主役の図形または公式画面を大きく置く。カードの外枠・小さな補助文を増やさず、下部180pxの字幕安全領域を空ける。

scene_renderer.pyは、episode.jsonのlayoutをこの一覧に解決し、公式素材はofficial_assetとofficial_asset_cropの指定だけから読み込む。`official_asset_slot`があるPhase Aで素材が未配置の場合、viewer-facingのplaceholder文字は描かず、`layout_04_text_official`の左右2カラムとneutral visual frameで完成形を示す。明示された素材パスが不正な場合はFAILとして扱う。将来のsceneでは、schemaを変えずに `visual_emphasis`、`headline_scale`、`composition`、`visual_balance_center_x` を任意指定でき、未指定時は安全なlayoutデフォルトを使う。

## Phase 2 scene contract

- `render_mode=template`: 箇条書き、3ステップ、チェックリスト、まとめ、正確な文字。
- `render_mode=official`: 実在する公式UI・FAQ・ストア・設定画面。AIでUIを描き直さない。
- `render_mode=gpt_image`: 人間確認済みの完成背景。1scene=1枚の1920×1080 PNGをfull bleedで配置する。
- `render_mode=hybrid`: full-frame GPT背景に、正確なCodex文字と実在する公式素材を重ねる。
- `text_render_mode` は画像への文字入れ方式（Episode 007以降の新規sceneは `imagegen_native` を既定。詳細は `docs/text_render_policy.md`）。`imagegen_native` はImageGen内で背景と正確な日本語を同時生成し、生成後に文字QAする。`pil_overlay`（旧 `codex`）は文字だけを後描画し、大きな白カード、AI画像の縮小、画面半分の白塗り、新しいtemplate layoutは作らない。文字周囲の小さなscrim、shadow、outlineだけを許可する。`no_text` は画像内に文字を入れない。公式引用・手順・URL・数字・PIN・長文は `pil_overlay` を使う。
- GPT画像のfit優先順は `full_bleed` → 軽微な比率差の `crop` → 明示指定した場合だけ `cover_blur`。下部180pxは字幕帯とする。
- animationの既定は `static`。人物・説明画面は`very_slow_zoom`/`slow_zoom`を次候補とし、`slow_pan`は`animation_reason`がある場合だけ使う。
- scene QAのvisual balance・左右の巨大な白空間・official画面の小ささはWARN候補。WARNは人間のcontact sheet確認へ回し、意図したminimal designを許可する。

## 日本語字幕の意味境界改行（恒久ルール・2026-09-06）

- 字幕改行は `scripts/japanese_subtitle_semantics.py` を唯一の判定基準とし、`scripts/subtitle_phase_b_split.py`（生成）と `scripts/subtitle_preflight.py`（QA）が同じ規則を共有する。
- 優先順位は、自然な文意・節のまとまり、文節のまとまり、修飾関係、視覚的なバランス、72pxの順。文字数だけで分割しない。長い文はフォントを小さくせず、意味の切れ目で時間方向に分割する。
- 画面内は最大2行、字幕フォントは目標72px・最小56px。語中分割、活用語尾の分断、助詞・助動詞の行頭孤立を許可しない。
  - preflightは全cueの行内改行と同一segment内の時間cue境界を走査し、`unnatural_japanese_line_break=0`、`word_split=0`、`conjugation_split=0`、`particle_or_auxiliary_orphan=0` を必須とする。

## 文脈別の音声発音ゲート（恒久ルール・2026-09-06）

- `config/voicevox_pronunciation.yaml` の辞書readingは意図する読みの候補であり、音声のPASSそのものではない。
- `scripts/voicevox_preflight.py` の `contextual_pronunciation_audio_gate` は、疑問文、助詞・助動詞が続く語、語尾が母音の語、引き伸ばされやすい語、ピッチ変更語を、実際の文全体の`audio_query`で回帰確認する。モーラ数、余計な母音・長音、自然なフレーズ境界、疑問文のピッチ、アクセント位置、母音長を記録する。
- gateがREVIEWの場合は辞書登録済みでもPhase AをPASSにせず、人間の試聴・修正へ戻す。短い単語queryだけで文脈音声を代用しない。
- 人間が個別に承認した音声は`episode.json`の`human_audio_overrides`と`audio/human_approved/`へ記録する。`human_audio_override > pronunciation dictionary > automatic VOICEVOX generation`の順で優先し、SHA-256と対象narrationの一致を検証してからtimelineへreuseする。override対象へ`--regen-segment`を指定しても自動再生成せず、cleanupでも削除しない。

## 公式素材の取得失敗（恒久ルール・2026-09-06）

`official_capture_failed` はfail closedとする。抽出途中の文字、OCR結果、部分的な画像を公式素材として描画せず、renderer / preflightをFAILにする。復旧の優先順位は、同じ公式URLからのページまたはPDF再取得、同一公式ソース内の別表示、出典付き完全一致の短い引用、公式として見せないsemantic scene。取得元URL・確認日・ページ範囲・採用asset・SHA-256は `sources.md` と `media_manifest.csv` に残す。詳細は `docs/official_capture_failure_policy.md`。

## アイコンは「意味を持つsemantic SVG」を基本（恒久ルール・2026-09-04更新）

- 単純記号（✓ / ! / ? 等）を自作の丸バッジで大きく表示する方式は使わない。**sceneの意味に対応する高品質SVGアイコン**（Material Symbols Rounded 等、公式配布元取得・Apache 2.0等ライセンス記録必須）を採用する。
- アイコンは補助要素だが存在感はあってよい: **150〜220px程度（目安180px）**を淡いトーン円（navy/blue/green/amber）に載せる。headlineより強くしない・画面の30%以上を占有しない・大型カード化しない・アイコン単独中央置きで終わらせない。
- sceneデータの `icon_name` / `icon_tone` から選択（episode-specific hard-code禁止）。意味→アイコンは `config/icon_catalog.json` を参照。
- サイズ目安: アイコン単体が画面面積の15%以上を占有する場合WARN（`oversized_single_icon`）。
- caution: 意味アイコン（block / lock / contactless等）を淡いトーン円に。巨大な黄色い「!」カード・UIバッジ風は禁止。
- 数字・URL・電話番号等のASCII連続tokenは折返しで分断しない（`scene_renderer._wrap_paragraph_japanese` の token 保護）。

## Official two-column / filler icon permanent rule（2026-09-06）

- 大きなチェックマーク（✓）や単純記号を、装飾・空間埋め・公式素材の代替・主ビジュアルとして描画しない。完了・選択などの意味が明確な場合でも、小さな補助記号に限定する。
- lock / shield / question / success などのsemantic iconも、sceneの意味を伝える場合だけ小〜中サイズで使う。空いた右側を埋める目的の無意味なfiller iconは禁止する。
- template explanatory sceneのsemantic iconは主見出しより視覚的重要度を上げず、単体で画面面積の20%以上を占有しない。official information sceneではさらに小さな補助にとどめる。
- `official_asset_slot`があるPhase Aで公式素材が未配置の場合は、placeholder / pending / URL / 架空UI文字を表示せず、右側へ意味のない文字を含まないneutral visual frameを置く。実素材が入るPhase Bでも同じ右側visual boxを再利用する。
- 公式2カラムは、左に短い要点、右に公式素材またはneutral visual frameを置く。`scene_quality_report.py` の `visual_centroid_preflight` が背景差分の `occupied_bbox`、`visual_centroid_x`、`left_visual_weight`、`right_visual_weight` を測定し、重心x=768〜1152、右weight 20%以上を目標とする。`left_bias_fail=1` はFAILとして人間確認前に止める。

## 共通Background System（恒久ルール・2026-09-05確定・Episode 008〜）

- テンプレートsceneは**白一色禁止**。`config/visual_theme.json` のプロファイル `adult_digital_soft_background`（明るいsoft gradient: 左上淡ブルー→中央ほぼ白→右下わずかに青み）を共通テーマとして、レンダラー（HTML/CSS・Pillow両パス）が自動適用する。
- 共通shell: 左上のrounded section pill（44px以上・初期52px）／淡いaccent circle（低opacity・文字の背後）／右下の小さなdot cluster／accent line／semantic icon用の淡い円plate（iconを一回り大きく包む）。装飾は1sceneに全部入れない・文字と重ねない・文字より目立たせない。
- セクション別accent: はじめに=blue / 1=blue＋淡amber / 2=blue＋淡green / 3=blue＋淡teal / 困ったとき=淡amber / まとめ=soft blue-green。caution系（layout_06_caution）は自動で淡amber accentへ切替。強い色面・黒背景・neon・glossy 3D・過剰shadow・stock写真風人物追加は禁止。
- 重要数字scene（hero＋数字headline）は淡いpanel＋控えめmotifを背景に置く（数字が主役）。list行は横線ではなく淡いrounded card/band。compareカードは薄いdepth（shadow）を持たせる。
- 適用順（再現性）: template scene生成 → common background theme → semantic icon → text layout。Episodeごとにaccentだけ変える場合は `config/visual_theme.json` のsectionsを編集する（hard-code禁止）。
- QA: `blank_white_slide`（コンテンツ領域のほぼ白画素率）を scene_quality_report が検査（66%超WARN）。文字サイズ基準はこの変更で緩めない（headline≥80px / main fact≥60px / secondary≥52px / source≥44px）。

### ユーザー提供背景プロファイル（Episode 008以降）

- ユーザー提供画像を使うtemplate sceneは `config/visual_theme.json` の `adult_digital_soft_image_bg` を選ぶ。`background_type=image` のassetを縦横比維持のcover＋LANCZOSで1920×1080へ配置し、元画像と正規化copyを保持する。
- `overlay_decorations=false` により、画像内の図形と競合する巨大circle・dots・leaf/wave・背景tint・大きな自動icon backingを追加しない。section pill、semantic icon（plate中心とicon中心を一致）、必要最小限のaccent line、下部180px字幕安全帯だけを共通shellとして残す。
- listは背景が見える淡いblue-white card、compareは薄いdepth、cautionはicon tone・headline accent・細いamber lineで意味を伝える。背景全体をamber化しない。assetが無いときはdummy背景へfallbackせず、contact sheet生成前に停止する。

### Visual Gate v4の整列ルール

- 本編template sceneへチャンネル名を常設しない。チャンネル名や登録要素はCTA／End Screenのルールで扱い、本編の毎sceneには描画しない。
- ユーザー提供背景プロファイルではsection pillを左上（原則x=60〜100、y=45〜75、QAはx<300）へ置き、headline・semantic icon・icon plate・main fact・support・panel/listの主要visual centroidをx=960へ揃える。
- heroのsemantic iconは基本center_x=960、icon plateとの中心差は2px以内。縦にpanelを積む場合は`stacked_panel_alignment`でcenter_x差12px以内を機械QAする。
- 背景画像の再生成・色相変更・opacity変更は行わず、v4の調整対象はoverlay layoutだけとする。

### Semantic iconの可視中心正規化（Visual Gate v5・2026-09-05）

- semantic iconは元SVG/PNGのキャンバス中心ではなく、最終render PNG上の可視グリフbbox中心をvisual axisとして扱う。
- 元素材に透明余白がある場合は、alpha threshold=4でbboxをtrimし、アスペクト比を維持した固定visual box（標準180×180px）へcontain配置する。元SVG/PNGは変更せず、正規化cacheを使用する。
- QA閾値は可視グリフ中心と意図した軸の差4px以下、可視グリフ中心とicon plate中心の差2px以下。plate自体の配置QAとは別に `semantic_icon_visual_center` を実施する。

## 最小文字サイズ（恒久ルール・2026-09-04確定・50〜60代中心＋視力弱め視聴者想定）

- **読めない情報は、ないのと同じ**。画面の情報文字は原則44px未満を出さない。
- main headline 80px以上（目安88〜120px）／main fact・must-read 60px以上（目安64〜80px）／secondary 52px以上／source label等は表示するなら44〜48px以上。
- URL全文・確認日・細かい注記・制作用ラベル（導入（問題提示・結論）等）は画面に出さない（sources.md / media_manifest / 説明欄 / workへ）。出典は「出典：○○公式」等の短形のみ44px以上。
- 入りきらない場合: 文字を小さくせず、①情報を短く整理→②main factのみ画面→③詳細はナレーション→④詳細sourceは概要欄→⑤次sceneへ分割、の順。
- 画面=結論・数字・操作箇所を大きく／ナレーション=条件・詳細・補足／概要欄=URL・source・詳細情報。
- QA: `tiny_text`（<44px FAIL・<52px REVIEW）・`unreadable_footer`（footer領域の極小URL/source/note/date/disclaimerはWARN・不要なら削除）。
