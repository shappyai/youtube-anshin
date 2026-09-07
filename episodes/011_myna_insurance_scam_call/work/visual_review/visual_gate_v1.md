# Episode 011 Visual Gate v1

確認日：2026-09-06

## 判定

`PASS_WITH_HUMAN_REVIEW`

既存18sceneを全面再生成せず、公式引用の可読性のためSCENE-003だけ表示assetを全画面quote cropへ差し替え、中盤CTAのSCENE-019を1scene追加した。残りの既存scene画像は再利用している。

## 自動・目視相当チェック

| gate | result | evidence |
|---|---|---|
| Fact FAIL | 0 | `fact_check.md`、一次情報突合済み。 |
| Privacy FAIL | 0 | `privacy_qa_v1.md`。 |
| template leakage | 0 | 共通Background System適用、旧Episode文字・ロゴなし。 |
| tiny text | 0 | `scene_quality_report_v1.md`で19scene OK。情報文字の最小基準を満たすよう配置。 |
| overflow | 0 | 19sceneのラスタ・配置確認。 |
| visual axis | PASS | renderer reportのvisual axis max 0px。 |
| semantic icon center | PASS | renderer reportのvisual center PASS、icon plate alignment 0px。 |
| official source legibility | PASS候補 | SCENE-003を全画面quote cropへ調整。本文は大きく、出典ラベルは字幕帯の上。元画像の人間確認待ち。 |
| subtitle safe area | PASS | template 19sceneの下部180pxをrendererで確保。AI sceneも下部180pxを設計。 |
| official answer <=15s | PASS estimate | 14.8秒推定。VOICEVOX実測はPhase B。 |
| three actions <=35s | PASS estimate | 23.0秒推定。 |
| contact sheet | PASS候補 | `scene_contact_sheet_v1.png`、19scene。 |

## ImageGen文字QA

- SCENE-001：`imagegen_native`。`scripts/text_qa.py` auto_fail=0、指定文言2行を目視確認しPASS。
- 指定文言：`その電話、本物？` / `まず止まって確認`
- SCENE-018：`pil_overlay`。短い締めの文言はCodex側で正確に重ね、右40〜45%をreserved。
- 再生成回数：0。承認済みAI sceneを再生成していない。

## 登録者獲得実験 v2のVisual QA

- `midroll_cta_count`：1
- 配置：SCENE-019、segment 013。公式結論と「番号を押さない」の説明後。
- 表示：`「これ、本物？」` / `公式情報で確認` / `次に困ったときのために`
- 派手な登録画面：0
- fake subscribe UI：0
- 恐怖語：0
- CTA予定尺：6.7秒、最大7秒。実測はPhase B。
- CTA直後：segment 014「2つ目です」へ戻る。

## 物語・終了QA

- micro_story_present：PASS
- viewer_is_protagonist：PASS
- problem_visible_early：PASS
- first_safe_action：10.4秒推定 / PASS
- official_answer：14.8秒推定 / PASS
- story_does_not_delay_core：PASS
- fictional_testimonial：0
- fear_bait：0
- story_resolution_present：PASS
- reason_to_return_cta：PASS（Episode010 reuse指定）
- duplicate_end_cta：0
- cta_full_text_visible：Phase Bで画面生成後に確認
- end_screen_reserved：PASS候補。SCENE-018右側を確保。

## Human Gateで見る箇所

1. SCENE-001〜003を元画像で連続視聴し、電話文言 → 停止 → 厚労省結論が15秒以内に感じられるか。
2. SCENE-003の公式引用が原文と一致し、出典が公式本文の引用として誤認なく読めるか。
3. `0120-95-0178`、音声案内5番、受付時間、`#9110`、`110`の用途分けが読めるか。
4. SCENE-019が登録お願いだけに見えず、次回も公式確認できる理由として自然か。
5. SCENE-018に疑似subscribe要素がなく、End Screen reserved領域が保たれているか。
6. 非写実的AI概念画2sceneのAI開示要否を人間判断すること。
