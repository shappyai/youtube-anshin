# Scene Plan — Episode 002 マイナアプリ（draft_v2用・35シーン）

制作方式（2026-08-30 人間レビューで確定）:
- ChatGPT = 映像デザイン / 完成静止画（`assets/generated_scenes/scene_###.png`・1920x1080 / 16:9）
- Codex = タイムライン実装 / 音声 / 字幕 / 公式素材の指定位置合成 / ffmpeg / QA
- Codexは映像レイアウトを新規デザインしない。ChatGPT完成画像をフルスクリーン表示し、
  必要最低限のゆっくりズーム・軽いパン・クロスフェード＋公式スクリーンショット合成のみ行う。
- 全画像の共通前提:
  - 1920x1080（16:9）。画面下部 y900〜1080（高さ180px）は字幕専用帯が被さるため、
    そこに文字・重要要素を置かない（余白を保つ）。
  - ブランド: 白基調＋ソフトな青・緑のアクセント（デジタル庁サイトの紺/青系トーンと調和）。
    「大人のデジタル安心室」= 静かで信頼感のあるトーン。派手な赤・ネオンは使わない。
  - 50〜70代がスマホ視聴でも読める大きさ。メインテキストは72px以上相当。
    サブテキストは48px以上相当。小さすぎる文字・情報の詰め込み・装飾の乱用をしない。
  - 公式スクリーンショットを後から合成するシーンでは、生成画像内に
    「枠線・アイコン・文字を描かない空白領域（合成スロット）」を確保する。
    公式のUI・日付・文言をAIで描き直す／公式画面のように見せることは禁止。
  - マイナアプリの実アイコンの見た目（ピンクグラデ・「マイナ」文字・桜）を生成画像内に
    描かない。アイコンが必要なときはCodexが公式素材を合成するため、空白領域を確保する。
- 音声: 本編ナレーション 80文・実測475.1秒（segments_manifest.csv）。scene境界は録音実時間ベース。

## SCENE-001

- time: start 0.000 / end 10.545 / duration 10.5s
- narration_segments: 1-2
- narration_text: アプリの名前やアイコンが、急に変わって驚いた方はいませんか。マイナポータルアプリは、8月25日から「マイナアプリ」になりました。
- main_message: 8月25日から「マイナポータルアプリ」は「マイナアプリ」に名前が変わりました
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_001.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. Clean white background, soft blue and light green accents, calm trustworthy design. Left side: large blank rounded-square slot (approx. 420x420px) reserved for an app icon (do NOT draw the icon or any logo inside; leave it as a very light gray placeholder outline). Right side: large Japanese headline: マイナポータルアプリは8月25日から「マイナアプリ」になりました (dark navy, headline size). Below headline, one short supportive line: 名前とアイコンが変わります (gray-blue, secondary size). Keep bottom 180px empty (subtitle band). No tiny text, no clutter, large margins. Friendly calm tone for viewers aged 50-70.
- official_asset_if_needed: official_icon_rounded_3x.png（新アイコン・Codex後合成）／任意で公式お知らせ(br_03)の小窓
- official_asset_crop_instruction: アイコンは透過PNGを左スロット(約420x420)へそのまま合成。日付の公式画面が必要なら br_03 を (143,240,1297,760) で縦長クロップし、画面下部のスロット（幅700px・Codex合成）に配置。生成画像には空白のみ確保。
- on_screen_text: ヘッドライン（名前の転換）
- text_priority: 名前の転換（旧→新）が最優先。アイコンはCodex合成と明示。
- animation: slow_zoom（1.0→1.05・10s）
- subtitle_text: SUB-001 / SUB-002（subtitle_plan.md参照）
- notes: 冒頭20秒のテンポ維持。公式アイコンはChatGPTに描かせない。

## SCENE-002

- time: start 10.545 / end 18.889 / duration 8.3s
- narration_segments: 3-4
- narration_text: お伝えしますが、マイナポータルというサービス自体は、なくなりません。アプリを消して、入れ直す必要もありません。
- main_message: マイナポータルというサービスはなくならない。アプリを消して入れ直す必要もない
- visual_type: generated_fullscreen
- image_required: yes
- image_filename: scene_002.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. Very clean white background. Center-left: large soft blue rounded shield illustration with a small green check mark (friendly, rounded, hand-drawn feel). Right side: large Japanese headline (dark navy): マイナポータルは なくなりません. Below it a supportive line (gray-blue, secondary size): アプリを消して、入れ直す必要はありません. Bottom 180px empty (subtitle band). No tiny text, no decorative clutter, large margins. Calm, reassuring tone.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: ヘッドライン＋サポート文
- text_priority: 「なくなりません」が最優先
- animation: none（軽いcrossfade出）
- subtitle_text: SUB-003 / SUB-004
- notes: 安心メッセージ。煽りなし。

## SCENE-003

- time: start 18.889 / end 25.174 / duration 6.3s
- narration_segments: 5
- narration_text: 今日は、何が変わったのか、今すべきことを、5つに分けて確認します。
- main_message: 今日は5つの項目を確認する
- visual_type: summary_card
- image_required: yes
- image_filename: scene_003.png
- chatgpt_image_brief: Summary card visual, 1920x1080, 16:9. Clean white background with one large rounded card (light blue-gray tint). Card title (top, dark navy, large): 今日は5つのことを確認します. 5 numbered rows (number in soft green circle, item text dark navy, readable size): 1 マイナアプリとは何か / 2 何が変わったのか / 3 すでに使っていた人は？ / 4 新しく使う人・開けない人 / 5 本物の確認ポイント. Generous spacing between rows. Bottom 180px empty (subtitle band). No tiny text, calm colors.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: 5項目リスト
- text_priority: リスト全体が1画面で読めること（行間を広く）
- animation: none
- subtitle_text: SUB-005
- notes: 章立て・サムネと平仄を合わせる。

## SCENE-004

- time: start 25.174 / end 36.357 / duration 11.2s
- narration_segments: 6-7
- narration_text: マイナアプリは、これまで使われてきたマイナポータルアプリの、新しい名前です。同じアプリのアップデート版で、いわば「名前を変えた」ものです。
- main_message: マイナアプリはマイナポータルアプリの「新しい名前・アップデート版」
- visual_type: generated_fullscreen
- image_required: yes
- image_filename: scene_004.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Centered: one large smartphone illustration (light blue-gray body); on its screen a simple app-name plate: マイナポータルアプリ (smaller, gray) → arrow → マイナアプリ (large, navy). Do NOT draw the real app icon (Codex composites it later). Below the phone, a Japanese line: 同じアプリの、新しい名前です (dark navy, secondary size). Bottom 180px empty. No tiny text, large margins, friendly tone.
- official_asset_if_needed: なし（本SCENEではアイコン合成しない）
- official_asset_crop_instruction: -
- on_screen_text: 名前プレート（旧→新）
- text_priority: 「マイナアプリ」の新しい名前プレート
- animation: slow_pan（左→右・電話図）
- subtitle_text: SUB-006 / SUB-007
- notes: 名前転換はscene_001と重複させず、ここでは「同じアプリ・アップデート版」を強調。

## SCENE-005

- time: start 36.357 / end 52.364 / duration 16.0s
- narration_segments: 8-10
- narration_text: そこに、「デジタル認証アプリ」の機能も統合されました。デジタル認証アプリは、マイナンバーカードで「本人であることを確認する」ためのアプリでした。「認証」は「本人確認」という意味です。
- main_message: デジタル認証アプリが統合された。「認証」＝「本人確認」
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_005.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Left 60%: friendly abstract illustration of identity check - a rounded shield/card with a simple person icon and a small key, soft blue and green. One smartphone next to it with a blank screen. Right side: a reserved rounded rectangle slot (approx 700x430px) with a very light gray outline; do NOT draw any UI inside (Codex places an official app screen there later). Japanese headline: 認証 は 本人確認 (dark navy, large). Support line: デジタル認証アプリが、ひとつに統合されました. Bottom 180px empty. Calm, trustworthy, no tiny text.
- official_asset_if_needed: official_screen_card.png（カード機能の公式画面・Codex後合成）
- official_asset_crop_instruction: official_screen_card.png（414x868）を右スロットへ高さ430px・縦長のまま合成（カード読み取り画面）。
- on_screen_text: 「認証」＝「本人確認」
- text_priority: 用語の説明（認証＝本人確認）を最優先
- animation: none（説明2単位で軽くzoom 1.0→1.06）
- subtitle_text: SUB-008 / SUB-009 / SUB-010
- notes: 専門用語の直後言い換え（AGENTSルール）を映像でも補強。

## SCENE-006

- time: start 52.364 / end 70.707 / duration 18.3s
- narration_segments: 11-13
- narration_text: これまで、行政の手続きにはマイナポータルアプリ、民間のサービスにはデジタル認証アプリと、場面によって使い分ける必要がありました。それが、マイナアプリひとつでできるようになります。ひとつのアプリにまとめたのが、今回の変更の中心です。
- main_message: 「行政用・民間用」の2つのアプリが、マイナアプリひとつにまとまった
- visual_type: generated_fullscreen
- image_required: yes
- image_filename: scene_006.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Left: two simple abstract app plates - one labeled 行政の手続き (building icon), one labeled 民間のサービス (shop icon), light gray-blue plates. Right: one larger plate labeled マイナアプリ ひとつでOK (strong navy, green check). Arrow from the two plates to the one plate. Below: Japanese line: 使い分けが、ひとつになりました. Do NOT draw real app icons. Bottom 180px empty. No tiny text, large margins.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: 2→1の転換プレート
- text_priority: 「ひとつでOK」の転換
- animation: slow_pan（左→右・矢印方向）
- subtitle_text: SUB-011 / SUB-012 / SUB-013
- notes: 1画面1メッセージ（統合の中心）。

## SCENE-007

- time: start 70.707 / end 80.974 / duration 10.3s
- narration_segments: 14-16
- narration_text: 変わったのは、主に3つです。1つ目は、スマホアプリの名前です。「マイナポータルアプリ」が「マイナアプリ」になりました。
- main_message: 変わったのは主に3つ。1つ目＝スマホアプリの名前
- visual_type: generated_fullscreen
- image_required: yes
- image_filename: scene_007.png
- chatgpt_image_brief: Section opener visual, 1920x1080, 16:9. White background. Top: small section badge (soft green rounded pill) 「2 / 5 何が変わったのか」. Center: large Japanese text 変わったのは、主に3つ (dark navy, large) with a simple numbered preview: 1 名前 / 2 アイコン / 3 アプリの統合 (numbers in soft green circles, item text readable size, the first item highlighted navy-bold). Bottom 180px empty. Calm, readable, no tiny text.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: 章バッジ＋3項目プレビュー
- text_priority: 章見出しと「1 名前」
- animation: none（次sceneへcrossfade）
- subtitle_text: SUB-014 / SUB-015 / SUB-016
- notes: セクション見出しの役割。情報パネル常設はしない。

## SCENE-008

- time: start 80.974 / end 95.866 / duration 14.9s
- narration_segments: 17-19
- narration_text: 2つ目は、アプリアイコンです。ピンクのグラデーションに「マイナ」の文字と、桜のマークのデザインになりました。しばらくの間は、左下に「マイナちゃん」がついた、期間限定のアイコンです。
- main_message: 2つ目＝アプリアイコン。新デザイン。しばらくは期間限定アイコン
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_008.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Centered: two large empty rounded-square slots side by side (each ~430x430px) with very light gray placeholder outlines. Do NOT draw any icon inside (Codex composites official icons later). Left slot caption: 新しいアイコン. Right slot caption: 期間限定アイコン（しばらくの間）. Above: Japanese headline: 2つ目は、アプリアイコン. Bottom 180px empty. No tiny text, big margins.
- official_asset_if_needed: official_icon_rounded_3x.png（新）＋ official_icon_limited_3x.png（期間限定・マイナちゃん入り）
- official_asset_crop_instruction: 透過PNGを各スロット(約430x430)へCodex合成。角丸は素材のまま。
- on_screen_text: 2スロットのキャプション
- text_priority: アイコン2種が並ぶこと
- animation: none（静止＋軽いcrossfade）
- subtitle_text: SUB-017 / SUB-018 / SUB-019
- notes: マイナちゃん旧アイコン切り出しは使わない（公式素材2種のみ）。

## SCENE-009

- time: start 95.866 / end 115.647 / duration 19.8s
- narration_segments: 20-22
- narration_text: デジタル庁は、年内をめどに、最終的なデザインに統一すると案内しています。3つ目は、ログインや認証に使うアプリが、ひとつに統合されたことです。デジタル認証アプリは、2026年8月25日をもって、単体での提供が終了しました。
- main_message: 3つ目＝認証アプリの統合。デジタル認証アプリは8月25日で単体提供終了
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_009.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Left 55%: abstract composition of two shapes merging into one - two soft blue rounded squares (labels ログイン / 認証) merging into one green rounded square (label マイナアプリ). Japanese headline: 3つ目は、アプリの統合. Right side: a reserved tall rounded slot (~560x420px) with a very light gray outline; do NOT draw UI inside (Codex places an official notice crop later). Bottom 180px empty. No tiny text.
- official_asset_if_needed: br_03_news_20260825.png（デジタル庁公式お知らせ・Codex後合成）
- official_asset_crop_instruction: br_03（1440x1600）を (143,240,1297,760) でクロップし、右スロットへ幅560pxで合成。「マイナポータルアプリにデジタル認証アプリの機能を統合したマイナアプリの提供を開始」の文言が見える範囲を優先。
- on_screen_text: 「3つ目は、アプリの統合」
- text_priority: 統合の概念＋公式お知らせ（8月25日）
- animation: slow_zoom（1.0→1.06・統合図へ）
- subtitle_text: SUB-020 / SUB-021 / SUB-022
- notes: 8月25日・単体終了は公式画面併用（AI再現禁止）。

## SCENE-010

- time: start 115.647 / end 135.078 / duration 19.4s
- narration_segments: 23-26
- narration_text: 開くと、マイナアプリの利用を案内する画面が表示される、と公式のよくある質問にあります。使っていた人も、同じ機能をマイナアプリで引き続き使えます。ここで、いちばん大事なことをお伝えします。マイナポータルというサービス自体が、なくなったわけではありません。
- main_message: デジタル認証アプリを開くと案内画面。マイナポータル自体はなくならない（公式FAQ「別のアプリですか→いいえ」）
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_010.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents, reassuring tone. Left 45%: large calm shield illustration with a green check and Japanese headline: マイナポータルは なくなりません, support line: 開くと、案内画面が表示されるだけ. Right side: two stacked reserved slots (each ~520x240px) with very light gray outlines; do NOT draw UI/FAQ content inside (Codex places official FAQ crops later). Bottom 180px empty.
- official_asset_if_needed: br_02_svc_top_faq.png（公式サービスサイトFAQ「別のアプリですか→いいえ」「マイナポータルWebは存続」・Codex後合成）
- official_asset_crop_instruction: br_02（1440x7000）を 上スロット=(0,5300,1440,5680)、下スロット=(0,5680,1440,6080) でクロップし、各スロットへ幅520pxで合成（Q「別のアプリですか」A「いいえ」が見える範囲）。
- on_screen_text: 「マイナポータルは なくなりません」
- text_priority: 安心メッセージ＋公式FAQの「いいえ」
- animation: none
- subtitle_text: SUB-023 / SUB-024 / SUB-025 / SUB-026
- notes: 最重要の安心ポイント。公式FAQは本物の公式画面として合成。

## SCENE-011

- time: start 135.078 / end 149.082 / duration 14.0s
- narration_segments: 27-29
- narration_text: マイナポータルは、行政サービスのオンライン窓口です。ウェブサイトは、引き続き使えます。医療費などの自己情報の確認や、引越し・パスポートなどの申請も、今までどおりです。
- main_message: マイナポータルは行政のオンライン窓口。Webは今後も今までどおり使える
- visual_type: generated_fullscreen
- image_required: yes
- image_filename: scene_011.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Center: friendly government-service window illustration: a rounded building icon with a counter, and three small icons below - medical receipt (医療費), moving box (引越し), passport (パスポート) - each with a tiny Japanese label in a soft green/blue circle. A small PC icon with line ウェブサイトでもOK. Headline: マイナポータルは、行政のオンライン窓口. Bottom 180px empty. No tiny text.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: 窓口＋アイコンラベル
- text_priority: 窓口のイメージと「今までどおり」
- animation: none（軽いcrossfade）
- subtitle_text: SUB-027 / SUB-028 / SUB-029
- notes: 申請の具体例はナレーションと一致させる。

## SCENE-012

- time: start 149.082 / end 165.521 / duration 16.4s
- narration_segments: 30-31
- narration_text: 変わったのは、スマホアプリの名前とアイコン、そしてログインや認証に使うアプリが統合されたことです。ログインのときの本人確認の役割が、マイナポータルアプリから、マイナアプリにバトンタッチされた、と考えると分かりやすいです。
- main_message: 変わるのは「アプリの名前・アイコン・ログイン認証の一本化」。ログインの役割がバトンタッチ
- visual_type: generated_fullscreen
- image_required: yes
- image_filename: scene_012.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Center: relay-baton metaphor - two simple hands passing a small blue baton labeled ログイン from plate マイナポータルアプリ to plate マイナアプリ (friendly line-art, soft colors). No real icons. Headline: 変わるのは、ログイン方法だけ, support: 本人確認の役割が、バトンタッチ. Bottom 180px empty.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: バトンタッチ図＋ヘッドライン
- text_priority: バトンタッチ（役割が移る）が伝わること
- animation: slow_pan（左→右・バトンの方向）
- subtitle_text: SUB-030 / SUB-031
- notes: 概念図であり実際のUIを描かない。

## SCENE-013

- time: start 166.205 / end 179.730 / duration 13.5s
- narration_segments: 32-33
- narration_text: では、ずっとマイナポータルアプリを使っていた人は、何をすればいいのでしょうか。まず、今お使いのアプリの名前とアイコン、そして、ストアで公開されている情報を確認してください。
- main_message: 3/5 すでに使っていた人：まず「名前・アイコン・ストア情報」を確認
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_013.png
- chatgpt_image_brief: Section opener visual, 1920x1080, 16:9. White background. Top: soft green pill badge 「3 / 5 すでに使っていた人は？」. Left: large smartphone illustration with three checklist rows (アイコン / 名前 / ストアの情報) each with a small green check circle, headline: まず、今のアプリを確認. Right: one reserved rounded slot (~420x520px) with very light gray outline; do NOT draw UI inside (Codex places an official store listing crop later). Bottom 180px empty.
- official_asset_if_needed: br_09_gplay.png（Google Play掲載名・Codex後合成）
- official_asset_crop_instruction: br_09（1440x2000）を (80,100,1240,560) でクロップし、右スロットへ幅420pxで合成（掲載名＋開発元が見える範囲）。
- on_screen_text: チェックリスト3項目
- text_priority: 「まず確認」の3つのチェック
- animation: none
- subtitle_text: SUB-032 / SUB-033
- notes: ストア掲載名は公式画面併用。

## SCENE-014

- time: start 179.730 / end 196.468 / duration 16.7s
- narration_segments: 34-36
- narration_text: マイナポータルアプリなら、アップデートするだけで、そのままマイナアプリとして使えます。削除して、入れ直す必要はありません。スマホの「自動更新」の設定がオンになっていれば、そのまま自動で更新されている場合があります。
- main_message: アップデートだけでOK・削除不要・自動更新ONなら自動で更新される場合がある
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_014.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Left: simple smartphone with a big circular update arrow (green), headline: アップデートするだけでOK, two short lines: 削除・入れ直しは不要 / 自動更新ONなら、自動で更新される場合もあります. Right: a reserved rounded card slot (~620x380px) with very light gray outline and a tiny label 公式FAQ (text placeholder only; do NOT write FAQ content - Codex renders the official quote later). Bottom 180px empty.
- official_asset_if_needed: 公式FAQ引用（自動更新）＝スクショ不可（Cloudflare）のためCodexが引用テキストをレンダリング
- official_asset_crop_instruction: 引用文「App StoreやGoogle Playの自動更新設定をご利用の場合は自動的に更新される場合があります。自動更新を利用していない場合は、ご自身でアップデートをお願いします」（出典: マイナアプリ よくある質問 61067610915737）を右スロットへCodex合成（72px・出典ラベル付き）。
- on_screen_text: ヘッドライン＋2行サポート
- text_priority: 「アップデートするだけでOK」
- animation: none
- subtitle_text: SUB-034 / SUB-035 / SUB-036
- notes: 公式文言はAIで再現せず、Codexが引用テキストとして配置（出典表記付き）。

## SCENE-015

- time: start 196.468 / end 206.319 / duration 9.9s
- narration_segments: 37
- narration_text: オンになっていなければ、App StoreやGoogle Playで「マイナアプリ（旧マイナポータルアプリ）」を探して、ご自分で更新してください。
- main_message: 自動更新OFFなら、ストアで「マイナアプリ（旧マイナポータルアプリ）」を更新
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_015.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background. Left: two small abstract store symbols (iOS-style blue bag shape and Google Play-style triangle) kept minimal and neutral, plus a large green update button illustration labeled アップデート. Headline: ストアで更新できます. Right: one reserved rounded slot (~560x360px) with very light gray outline for an official store listing (Codex composites later). Do not draw UI inside. Bottom 180px empty. Logo marks must stay small and non-decorative.
- official_asset_if_needed: br_09_gplay.png（掲載名・Codex後合成）
- official_asset_crop_instruction: br_09 を (80,100,1240,560) でクロップし、右スロットへ幅560pxで合成。アプリ名「マイナアプリ（旧マイナポータルアプリ）」が読めること。
- on_screen_text: 「ストアで更新できます」
- text_priority: 掲載名（旧併記）が見えること
- animation: none
- subtitle_text: SUB-037
- notes: ストアのロゴ・アイコンは装飾素材として使わない（説明用途のみ・控えめに）。

## SCENE-016

- time: start 206.319 / end 227.042 / duration 20.7s
- narration_segments: 38-41
- narration_text: アップデート後も、スマホの中に入れたマイナンバーカードの設定や、これまでの機能・データは引き継がれます。再登録は不要です。アップデートしなくても、マイナポータルアプリは当面使えます。ただ、一部の手続きでは、マイナアプリが必要になる、と公式に案内されています。
- main_message: 設定・データは引き継がれ再登録不要。当面使えるが一部手続きはマイナアプリが必要
- visual_type: generated_fullscreen
- image_required: yes
- image_filename: scene_016.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Center: two rounded info cards side by side. Card A (light green tint): 設定やデータは引き継がれます / 再登録は不要 (small box-arrow icon). Card B (light blue tint): 当面は使えます / 一部の手続きではマイナアプリが必要に (small clock icon). Text size readable. Headline: 安心の3つのポイント. Bottom 180px empty. No tiny text.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: 2枚のポイントカード
- text_priority: 「引き継がれます」「再登録不要」
- animation: slow_zoom（1.0→1.05・20.7sの静止感を軽減）
- subtitle_text: SUB-038 / SUB-039 / SUB-040 / SUB-041
- notes: 尺20.7sは目安上限ぎりぎり。1画面2カードで対応。

## SCENE-017

- time: start 227.042 / end 234.267 / duration 7.2s
- narration_segments: 42-43
- narration_text: ここで注意です。分からなくなったからといって、アプリを削除して入れ直すのは、まず待ってください。
- main_message: 注意：分からないからといって削除・入れ直しするのは待って
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_017.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background. Center-left: a soft amber warning sign (rounded triangle, friendly style, NOT scary) with a smartphone and a circle-slash over a delete/trash icon. Headline: 削除・入れ直しは、まず待って. Right: reserved rounded slot (~560x360px) light gray outline for an official FAQ quote (Codex renders later). Do not write FAQ text inside. Bottom 180px empty. Calm but clear caution tone.
- official_asset_if_needed: 公式FAQ引用（入れ直し・Q）＝スクショ不可のためCodexが引用テキストをレンダリング
- official_asset_crop_instruction: 引用「Q. アプリを入れ直したら、マイナアプリが開かなくなりました。」（出典: マイナアプリ よくある質問 60333701393049）を右スロットへCodex合成。
- on_screen_text: 「削除・入れ直しは、まず待って」
- text_priority: 注意の一言（恐怖にしない）
- animation: none
- subtitle_text: SUB-042 / SUB-043
- notes: 煽らない注意表現。

## SCENE-018

- time: start 234.267 / end 254.889 / duration 20.6s
- narration_segments: 44-45
- narration_text: 公式のよくある質問には、アプリを入れ直したあと、マイナアプリが開かなくなった、という質問への案内があります。スマホには「後からインストールしたアプリが優先して開く」という仕組みがあり、デジタル認証アプリを後から入れ直すと、マイナアプリの代わりに開いてしまうことがあるそうです。
- main_message: 後からインストールしたアプリが優先して開く仕組みがある（入れ直しの落とし穴）
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_018.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background. Left: simple timeline graphic of app installation order: ① マイナアプリ → ② デジタル認証アプリを後から入れ直す → ③ 後から入れた方が優先 (three small plates with arrows; ② highlighted soft amber). Headline: 後から入れたアプリが優先される仕組み. Right: reserved slot (~560x420px) for an official FAQ quote (Codex renders later). Bottom 180px empty.
- official_asset_if_needed: 公式FAQ引用（入れ直し・A）＝Codexが引用テキストをレンダリング
- official_asset_crop_instruction: 引用「A. 後からインストールしたアプリが優先して開く仕組みになっています。マイナアプリを優先したい場合は、マイナアプリをデジタル認証アプリより後にインストールし直すか、デジタル認証アプリをアンインストールします。」（出典: マイナアプリ よくある質問 60333701393049）を右スロットへCodex合成。
- on_screen_text: 順序図＋ヘッドライン
- text_priority: 「後から入れた方が優先」の順序図
- animation: slow_pan（順序図 左→右）
- subtitle_text: SUB-044 / SUB-045
- notes: 削除・再インストールを安易に勧めない理由を図解。

## SCENE-019

- time: start 254.889 / end 263.950 / duration 9.1s
- narration_segments: 46
- narration_text: 困ったときは、まず削除ではなく、公式のよくある質問や、概要欄の公式ページを確認するのが安心です。
- main_message: 困ったら削除ではなく、公式FAQ・概要欄の公式ページを確認
- visual_type: generated_fullscreen
- image_required: yes
- image_filename: scene_019.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Center: a smartphone held in a friendly hand illustration, on screen a small help/magnifier icon and a bookmark icon. Headline: 困ったら、まず確認. Two short lines: 公式のよくある質問 / 概要欄の公式ページ. A calm green check mark beside the phone. Bottom 180px empty. No tiny text.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: 「困ったら、まず確認」＋2つの行き先
- text_priority: 「まず確認」の行動
- animation: none
- subtitle_text: SUB-046
- notes: 削除誘導をしない安心の締め。

## SCENE-020

- time: start 263.950 / end 271.767 / duration 7.8s
- narration_segments: 47-48
- narration_text: 次に、新しく使う人や、アップデート後に開けない人向けの確認です。まず、動作環境です。
- main_message: 4/5 新しく使う人・開けない人向けの確認（動作環境から）
- visual_type: generated_fullscreen
- image_required: yes
- image_filename: scene_020.png
- chatgpt_image_brief: Section opener visual, 1920x1080, 16:9. White background. Top: soft green pill badge 「4 / 5 新しく使う人・開けない人」. Center: friendly illustration of a smartphone with a small gear/cog icon and a dotted question mark above it. Headline: まず、動作環境を確認. Bottom 180px empty. Calm, no tiny text.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: 章バッジ＋ヘッドライン
- text_priority: 章見出し
- animation: none（次sceneへcrossfade）
- subtitle_text: SUB-047 / SUB-048
- notes: セクション見出し。

## SCENE-021

- time: start 271.767 / end 284.724 / duration 13.0s
- narration_segments: 49-50
- narration_text: iPhoneはiOS 16.4以上、AndroidはAndroid 11以降で、NFC機能が必要です。NFCは、カードをかざして読み取るための機能です。
- main_message: 対応条件：iPhone= iOS 16.4以上／Android= 11以降＋NFC。NFCはカードをかざして読み取る機能
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_021.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Left 55%: two simple phone illustrations (one slim iPhone-like, one Android-like, neutral colors) with two readable label lines: iPhoneは iOS 16.4以上 / Androidは 11以降・NFCが必要. A small NFC icon (card touch) with caption: NFCはカードをかざして読み取る機能. Right side: a reserved rounded slot (~600x420px) with very light gray outline; do NOT draw UI inside (Codex places an official requirements page crop later). Bottom 180px empty.
- official_asset_if_needed: br_06_sysreq.png（デジタル庁公式「マイナアプリの動作環境」・Codex後合成）
- official_asset_crop_instruction: br_06（1440x2600）を (0,300,1440,1150) でクロップし、右スロットへ幅600pxで合成（対応OS「iOS 16.4以上」「Androidバージョン11以降」「NFC機能」が見える範囲）。
- on_screen_text: 対応OSラベル＋NFC説明
- text_priority: 対応条件（iOS/Android）を読ませる
- animation: none
- subtitle_text: SUB-049 / SUB-050
- notes: 現行条件のみ（旧マイナポータル推奨環境と混同しない）。

## SCENE-022

- time: start 284.724 / end 305.275 / duration 20.6s
- narration_segments: 51-53
- narration_text: 新しく使う人は、初回だけ「利用登録」という手続きが必要です。お手元に、マイナンバーカードと、数字4桁の「利用者証明用暗証番号」を用意してください。実物のカードをかざすか、スマホの中にカードを入れている人は、顔や指紋で認証します。
- main_message: 初回だけ利用登録。カード＋数字4桁の暗証番号を用意。カード内の人なら顔・指紋でOK
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_022.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Left 45%: simple supply list: ① マイナンバーカード (card illustration), ② 数字4桁の暗証番号 (four small squares), ③ スマホの中のカードなら顔・指紋でOK (face/fingerprint icon). Headline: 初回だけ「利用登録」. Right side: two small reserved vertical slots (~300x500px each) with very light gray outlines; do NOT draw UI inside (Codex composites official registration screens later). Bottom 180px empty. No tiny text.
- official_asset_if_needed: official_screen_register_card_auth.png ＋ official_screen_register_biometric.png（公式利用登録画面・Codex後合成）
- official_asset_crop_instruction: 公式画面2枚（縦長）を右の2スロット（高さ500px）へCodex合成。カード認証（4桁入力）と顔・指紋認証の画面が読める範囲。
- on_screen_text: 用意するもの3点リスト
- text_priority: 「カード＋数字4桁の暗証番号」を読ませる
- animation: none
- subtitle_text: SUB-051 / SUB-052 / SUB-053
- notes: 尺20.6s。登録フローの説明1ブロックとして構成。

## SCENE-023

- time: start 305.275 / end 319.397 / duration 14.1s
- narration_segments: 54-55
- narration_text: また、端末のロック設定が必須です。PIN、顔認証、指紋認証など、スマホ本体のロックが設定されていないと、マイナアプリは使えません、と公式に案内されています。
- main_message: 端末のロック設定（PIN・顔・指紋）が必須。未設定だとマイナアプリは使えない
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_023.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Left 50%: large smartphone with a simple key/lock icon and three small badges: PIN / 顔認証 / 指紋認証. Headline: 端末のロック設定が必須, support: 未設定だと、マイナアプリは使えません. Right side: two reserved slots (one ~520x360px, one small ~240x360px) with very light gray outlines; do NOT draw UI inside (Codex composites official lock-setting screen + official requirements section later). Bottom 180px empty.
- official_asset_if_needed: official_screen_register_device_lock.png（公式「端末ロックの利用許可」画面）＋ br_06（動作環境・端末ロック節）
- official_asset_crop_instruction: device_lock画面（縦長）を右スロット1へ高さ360pxで合成。br_06 を (0,1500,1440,2350) でクロップし、スロット2へ幅240pxで合成。
- on_screen_text: PIN・顔認証・指紋認証の3バッジ
- text_priority: 「ロック設定が必須」を読ませる
- animation: none
- subtitle_text: SUB-054 / SUB-055
- notes: 生体認証・暗証番号の実演はしない（公式画面のみ）。

## SCENE-024

- time: start 319.397 / end 339.455 / duration 20.1s
- narration_segments: 56-58
- narration_text: もし、マイナポータルにログインできない場合は、よくある原因があります。ブラウザの「プライベートブラウズ」や「シークレットモード」を使っていると、ストアへの移動を繰り返すことがあるそうです。通常モードに戻して、スマホを再起動してから、もう一度試してください。
- main_message: ログインできない場合：プライベートブラウズ/シークレットモードが原因かも。通常モード＋再起動で再試行
- visual_type: generated_fullscreen
- image_required: yes
- image_filename: scene_024.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Layout: left a smartphone browser screen sketch with two small toggle plates (プライベートブラウズ / シークレットモード) marked with a soft amber dot, arrow to 通常モード, then a restart icon (circular arrow). Headline: ログインできないときは, three short steps: ① 通常モードに戻す ② スマホを再起動 ③ もう一度試す. Bottom 180px empty. No tiny text.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: 3ステップ手順
- text_priority: 対処手順（通常モード→再起動→再試行）
- animation: none（3ステップなので静止＋軽いcrossfade）
- subtitle_text: SUB-056 / SUB-057 / SUB-058
- notes: トラブル時の対処は必ず公式FAQの記述に忠実に。

## SCENE-025

- time: start 339.455 / end 352.639 / duration 13.2s
- narration_segments: 59-60
- narration_text: なお、この動画では、カードの読み取りや暗証番号の入力は実演しません。個人情報にかかわる手続きは、ご自身のスマホで、画面の案内に沿って進めてください。
- main_message: この動画ではカード読み取り・暗証番号入力は実演しない。個人情報の手続きはご自身のスマホで
- visual_type: generated_fullscreen
- image_required: yes
- image_filename: scene_025.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Center: a smartphone with a small "glasses/guide" icon and a gentle hand, plus a green check under a small lock icon. Headline: 個人情報の手続きは、ご自身のスマホで. Support line: この動画では、カードの読み取りや暗証番号の入力は実演しません. Soft, trustworthy, no tiny text. Bottom 180px empty.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: ヘッドライン＋サポート
- text_priority: 「ご自身のスマホで」の安心メッセージ
- animation: none
- subtitle_text: SUB-059 / SUB-060
- notes: 個人情報を出さない方針を明示（チャンネルポリシー）。

## SCENE-026

- time: start 352.639 / end 366.392 / duration 13.8s
- narration_segments: 61-62
- narration_text: 最後に、偽物のアプリや、フィッシングにだまされないための、本物の確認ポイントです。公式のマイナアプリは、App StoreとGoogle Playの、ふたつの場所からだけ、ダウンロードできます。
- main_message: 5/5 本物の確認ポイント。公式アプリはApp StoreとGoogle Playだけ
- visual_type: generated_fullscreen
- image_required: yes
- image_filename: scene_026.png
- chatgpt_image_brief: Section opener + message visual, 1920x1080, 16:9. White background. Top: soft green pill badge 「5 / 5 本物の確認ポイント」. Center: two neutral store-symbol shapes (kept abstract, small) with a large green check and headline: 公式は、この2つの場所だけ. Support: App Store と Google Play. A subtle magnifier icon. Bottom 180px empty. Store logos must stay minimal and non-decorative.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: 章バッジ＋「2つの場所だけ」
- text_priority: 章見出し＋2ストアだけが公式
- animation: none（次sceneへcrossfade）
- subtitle_text: SUB-061 / SUB-062
- notes: ストアロゴは装飾でなく説明のための控えめなシンボル。

## SCENE-027

- time: start 366.392 / end 384.568 / duration 18.2s
- narration_segments: 63-64
- narration_text: アプリの名前は「マイナアプリ（旧マイナポータルアプリ）」、提供元の表示は、App Storeでは「Digital Agency of Japan」、Google Playでは「デジタル庁」です。どちらの場合も、デジタル庁が提供元であることを確認してください。
- main_message: ストアの掲載名と提供元を確認（App Store: Digital Agency of Japan／Google Play: デジタル庁）
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_027.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background. Layout: two large reserved rounded slots side by side (each ~820x430px) with very light gray outlines. Do NOT draw store UI inside (Codex composites official App Store / Google Play crops later). Above the slots small captions: 提供元を確認. Below each slot a thin label line: App Store: Digital Agency of Japan / Google Play: デジタル庁（Codexが後から実画面と合わせて表示）. Headline (top): 本物の確認ポイント. Bottom 180px empty.
- official_asset_if_needed: br_08_appstore.png ＋ br_09_gplay.png（公式ストア2ページ・Codex後合成・2カラム）
- official_asset_crop_instruction: br_08 を (250,60,1440,620) でクロップし左スロット（幅820px）へ。br_09 を (80,100,1240,560) でクロップし右スロットへ。掲載名と提供元が読める範囲を優先。
- on_screen_text: 2スロット＋提供元ラベル
- text_priority: 「提供元がデジタル庁」を読ませる
- animation: none（2カラムで比較提示）
- subtitle_text: SUB-063 / SUB-064
- notes: ストアの実画面は公式ページのみ。タイトル部を大きくクロップ。

## SCENE-028

- time: start 384.568 / end 391.034 / duration 6.5s
- narration_segments: 65
- narration_text: アイコンのデザインは、ピンクのグラデーションに「マイナ」の文字と、桜のマークです。
- main_message: アイコンのデザイン＝ピンクのグラデーション・「マイナ」・桜
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_028.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background. Center: one large empty rounded-square slot (~450x450px) with a very light gray outline (Codex composites the official icon later; do NOT draw it). Around the slot, three small caption chips: ピンクのグラデーション / 「マイナ」の文字 / 桜のマーク. Headline: アイコンのデザイン. Bottom 180px empty.
- official_asset_if_needed: official_icon_rounded_3x.png（公式新アイコン・Codex後合成）
- official_asset_crop_instruction: 透過PNGを中央スロット(約450x450)へCodex合成。
- on_screen_text: 3つの特徴チップ
- text_priority: アイコン（公式合成）＋特徴3点
- animation: none
- subtitle_text: SUB-065
- notes: アイコンの見た目は公式素材のみ。

## SCENE-029

- time: start 391.034 / end 406.288 / duration 15.3s
- narration_segments: 66-67
- narration_text: デジタル庁は、マイナポータルをかたる偽サイトや、偽アプリの事案について、注意喚起を出しています。メールや電話で、アプリのダウンロードや、暗証番号の入力を求められたら、まず疑ってください。
- main_message: 偽サイト・偽アプリの注意喚起あり。メール・電話でDLや暗証番号を求められたら疑う
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_029.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents with a gentle amber caution accent. Left 50%: an envelope and a phone illustration with a small warning triangle (friendly, not scary) and headline: メールや電話で求められたら、まず疑って. Support: アプリのダウンロード・暗証番号の入力. Right side: one reserved rounded slot (~600x430px) with a very light gray outline; do NOT draw news/UI inside (Codex composites the official notice crop later). Bottom 180px empty.
- official_asset_if_needed: br_10_notice_fakeapp.png（デジタル庁公式注意喚起・Codex後合成）
- official_asset_crop_instruction: br_10（1440x1600）を (0,380,1440,1000) でクロップし、右スロットへ幅600pxで合成（「偽サイト、偽アプリへ誘導」「不審なアプリをインストールしない」が見える範囲）。
- on_screen_text: ヘッドライン＋サポート
- text_priority: 「まず疑って」の行動
- animation: none
- subtitle_text: SUB-066 / SUB-067
- notes: 注意喚起は公式ページ併用（AI再現禁止）。

## SCENE-030

- time: start 406.288 / end 414.073 / duration 7.8s
- narration_segments: 68
- narration_text: 暗証番号などをメールや電話で聞かれても、入力・回答しないよう、デジタル庁は案内しています。
- main_message: 暗証番号をメール・電話で聞かれても入力・回答しない（デジタル庁の案内）
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_030.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background. Center-left: a smartphone message bubble with a red-outlined prohibition circle over a 4-digit PIN display (abstract dots, never a real PIN). Headline: 暗証番号は、誰にも教えない. Support: メールや電話で聞かれても、入力・回答しない（デジタル庁の案内）. Right side: reserved rounded slot (~560x360px) with very light gray outline for an official phishing notice crop (Codex composites later). Bottom 180px empty. Calm tone, not scary.
- official_asset_if_needed: br_11_notice_phishing.png（デジタル庁公式フィッシング注意喚起・Codex後合成）
- official_asset_crop_instruction: br_11（1440x1600）を (0,400,1440,1150) でクロップし、右スロットへ幅560pxで合成（「暗証番号などの個人情報は絶対に入力せず」が見える範囲）。
- on_screen_text: ヘッドライン＋サポート
- text_priority: 「暗証番号は誰にも教えない」
- animation: none
- subtitle_text: SUB-068
- notes: 公式文言「絶対に入力せず」は公式ページ表示で補強（ナレーション断定を避ける表現の維持）。

## SCENE-031

- time: start 414.073 / end 428.771 / duration 14.7s
- narration_segments: 69-70
- narration_text: 公式の相談窓口は、マイナンバー総合フリーダイヤル、0120-95-0178です。心配なことがあれば、一人で判断せず、確認するのもひとつの方法です。
- main_message: 相談窓口：マイナンバー総合フリーダイヤル 0120-95-0178。一人で判断せず確認を
- visual_type: generated_plus_official
- image_required: yes
- image_filename: scene_031.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background, soft blue/green accents. Center-left: a friendly telephone illustration with a large readable number plate: 0120-95-0178 (very large digits, navy), caption: マイナンバー総合フリーダイヤル. Support line: 心配なことがあれば、一人で判断せず、確認するのもひとつの方法です. Right side: reserved rounded slot (~560x360px) light gray outline for an official notice crop (Codex composites later). Bottom 180px empty.
- official_asset_if_needed: br_10_notice_fakeapp.png（下部・相談窓口記載部分・Codex後合成）
- official_asset_crop_instruction: br_10 を (0,1000,1440,1600) でクロップし、右スロットへ幅560pxで合成（「マイナンバー総合フリーダイヤル（0120-95-0178）」の記載が見える範囲）。
- on_screen_text: 電話番号プレート
- text_priority: 0120-95-0178 の数字が読めること
- animation: none
- subtitle_text: SUB-069 / SUB-070
- notes: 番号は公式通知ページの記載と一致していることを編集時に再確認。

## SCENE-032

- time: start 428.771 / end 440.838 / duration 12.1s
- narration_segments: 71-73
- narration_text: 今日の内容をまとめます。今やっていただきたいことは、3つです。1つ目、まず、お使いのアプリが本物かどうか、名前と提供元とアイコンを確認する。
- main_message: まとめ：今やること3つ（提示＋1つ目＝アプリ名・提供元・アイコンを確認）
- visual_type: summary_card
- image_required: yes
- image_filename: scene_032.png
- chatgpt_image_brief: Summary card visual, 1920x1080, 16:9. Clean white background, large rounded card (light blue-gray tint). Card title (top, dark navy, large): 今やること3つ. Three numbered rows (number in soft green circle, item text dark navy, large): 1 アプリ名とアイコンを確認 / 2 必要ならストアで更新 / 3 提供元がデジタル庁か確認. First row visually emphasized (highlight). Bottom 180px empty. No tiny text, generous spacing.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: 3項目カード
- text_priority: 3項目全体＋現在の項目（1）
- animation: none
- subtitle_text: SUB-071 / SUB-072 / SUB-073
- notes: 終盤の最重要カード。ChatGPTは3項目カード1枚を完成させ、強調は2枚目（弱）でも可。

## SCENE-033

- time: start 440.838 / end 456.421 / duration 15.6s
- narration_segments: 74-75
- narration_text: 2つ目、マイナポータルアプリなら、削除せずに、アップデートする。3つ目、利用登録の案内が出たら、マイナンバーカードと数字4桁の暗証番号を用意して、端末のロックが設定されているか確認する。
- main_message: 今やること：2つ目＝アップデート／3つ目＝カード・暗証番号・端末ロックを確認
- visual_type: summary_card
- image_required: yes
- image_filename: scene_033.png
- chatgpt_image_brief: Summary card visual, 1920x1080, 16:9. Same card design as scene_032 (今やること3つ・3項目). The second and third rows are emphasized in this variant while the first row is dimmed; final variant highlights row 3. Provide this as 2 subtle variants if possible (Codex will crossfade between them), otherwise one card with equal emphasis is acceptable. Bottom 180px empty.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: 3項目カード（強調移動）
- text_priority: 現在の項目（2→3）
- animation: crossfade（強調バリアント切替）＋slow_zoom
- subtitle_text: SUB-074 / SUB-075
- notes: 1画面内の強調移動はChatGPT2枚をCodexがクロスフェード。

## SCENE-034

- time: start 456.421 / end 466.467 / duration 10.0s
- narration_segments: 76-78
- narration_text: 慌てて消す前に、まず確認する。それが一番の近道です。役に立ったら、チャンネル登録して、次回も一緒に確認しましょう。
- main_message: ブランドライン「慌てて消す前に、まず確認する」＋チャンネル登録CTA
- visual_type: generated_fullscreen
- image_required: yes
- image_filename: scene_034.png
- chatgpt_image_brief: 16:9 landscape YouTube educational visual, 1920x1080. White background with a calm soft-blue band across the middle. Center large Japanese text (brand line, navy, X-large): 慌てて消す前に、まず確認する. Below it a small supportive line: それが一番の近道です. At the bottom area (above the reserved 180px subtitle band) a modest, non-pushy subscribe prompt: チャンネル登録して、次回も一緒に確認しましょう (with a simple rounded subscribe button illustration, calm blue, no glow, no urgency). No tiny text.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: ブランドライン＋登録ボタン
- text_priority: ブランドライン（チャンネル方針）
- animation: none
- subtitle_text: SUB-076 / SUB-077 / SUB-078
- notes: 煽らないCTA（登録誘導は控えめに）。

## SCENE-035

- time: start 466.467 / end 475.142 / duration 8.7s
- narration_segments: 79-80
- narration_text: 概要欄に、今回確認したデジタル庁の公式ページを載せておきます。分からないことがあれば、コメントで教えてください。
- main_message: 概要欄に公式ページ。コメントで質問歓迎（エンド）
- visual_type: generated_fullscreen
- image_required: yes
- image_filename: scene_035.png
- chatgpt_image_brief: End card visual, 1920x1080, 16:9. White background with a soft blue-green gradient corner accent (calm). Center: channel name 大人のデジタル安心室 (large, navy), and two short lines: 概要欄に、確認したデジタル庁の公式ページを載せました / 分からないことがあれば、コメントで教えてください. A simple green check icon. No tiny text, no pushy elements. Bottom 180px empty.
- official_asset_if_needed: なし
- official_asset_crop_instruction: -
- on_screen_text: チャンネル名＋2行メッセージ
- text_priority: チャンネル名と「概要欄・コメント」
- animation: none
- subtitle_text: SUB-079 / SUB-080
- notes: エンドカード。次回に続く自然な締め。

## 付記（ChatGPT向け補足）

- 生成画像は `assets/generated_scenes/scene_001.png` 〜 `scene_035.png`（全35枚・1920x1080・PNG）。
- 公式アイコン・ストア画面・動作環境・注意喚起・FAQ等はAIで描かず、必ず合成スロットを確保する。
- すべてのシーンで下部180pxを字幕帯用に空けること。
- 配色は白基調＋ソフト青・緑を基本とし、公式素材のピンク・桜・マイナちゃんは合成素材としてのみ現れる。
- 文字はすべて扁平でなく読みやすいWeb向けゴシック系のイメージ、太さは中〜太。
