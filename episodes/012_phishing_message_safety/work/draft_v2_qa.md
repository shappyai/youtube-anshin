# Episode012 draft_v2 QA

確認日：2026-09-06  
対象：`output/draft_v2.mp4`  
総合：**PASS／人間の全編確認待ち**

## QA結果

|領域|結果|実測|
|---|---|---|
|字幕|PASS|119 cue、target 72px、minimum 56px、overflow 0、3-line 0|
|日本語意味境界改行|PASS|`unnatural_japanese_line_break=0` / `word_split=0` / `conjugation_split=0` / `particle_or_auxiliary_orphan=0`|
|読み仮名漏出|PASS|`tts_reading_leakage=0`|
|再現ラベル|PASS|31 scene scan、`incorrect_reproduction_label=0`。SCENE-006 / 011 / 017 / 021 / 025を削除・説明用へ変更|
|公式素材|PASS|`capture_failure_fallback_text=0` / `official_source_integrity=PASS`|
|発音|PASS|6語を標準承認辞書へ登録、実クエリ監査PASS|
|CTA|PASS|Episode011実使用CTAのconfig・visual・audio・canonical text・15秒を一致再利用|
|Fact|PASS|FAIL 0 / REVIEW 3|
|Privacy|PASS|FAIL 0 / REVIEW 0|
|動画|PASS|1920×1080、30fps、AAC 48kHz mono、Phase 2 QA PASS|

## 主要修正

- 字幕は文字数だけで折らず、文の自然さ・文節・修飾関係を優先し、長い文は時間方向へ分割した。
- SCENE-007は国民生活センター公式PDFの中途半端なcrop／抽出断片を採用せず、同PDFの正確な短い引用「記載されているURLにはアクセスせず、事前にブックマークした正規サイトのURLや、正規のアプリからアクセスしましょう。」と出典ラベルを表示する。表示は語の途中で切れない4行に固定した。
- `official_capture_failed`では抽出断片を公式画面として描画しないfail-closed policyを `docs/official_capture_failure_policy.md` に追加した。
- `普段`＝フダン accent 1、`何も`＝ナニモ accent 2、`届け物`＝トドケモノ、`本物`＝ホンモノ、`カード会社`＝カアドガイシャ accent 3、`e-Tax`＝イータックス（語中pause 0）を確認した。
- 終了CTAはEpisode011 `output/final.mp4`の実使用postrollをsource of truthとし、CTA audioは再生成せず同一WAVを再利用した。中盤CTAもEpisode011 segment013とWAV hash一致。

## CTA照合

- `end_cta_same_as_011=PASS`
- `cta_audio_match_011=PASS`
- `cta_visual_pattern_match_011=PASS`
- `pre_cta_transition_match_011=PASS`（hard concat、fadeなし、右40〜45% reserved）
- 詳細：`work/cta_compare_011_vs_012.md`

## 出力・人間確認

- draft_v2：`output/draft_v2.mp4`
- 実測尺：597.13秒（期待値597.127秒）
- SHA-256：`94A04D4D905E3736E3792DAC69C1CE2A1935F9D71C11A052951B74161ED48B8B`
- contact sheet：`output/review/scene_contact_sheet_v2.png`
- pronunciation audit：`work/pronunciation_audio_audit_v2.md`
- 聴取ポイント：`work/human_review_points_v2.md`
- thumbnail、final、upload、schedule、End Screen設定：未実施
