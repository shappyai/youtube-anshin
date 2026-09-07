# Shorts探索バッチ001 Visual Redesign v5 report

- v4 Human Draft Gate（約50/100、静止画の微細zoom/panとShort003抽象renderer）を受けたfocused visual correction。
- `shorts_micro_motion_for_motion_sake`：FORBIDDEN。意味のない105→110% zoom、pan、micro motionを廃止。
- visual beat countはKPIにしない。静止表示2〜5秒を基本に、hard cut / real UI / official asset / meaningful crop / info-state changeだけで切り替える。
- CTAは専用slideなし。spoken canonicalは変更せず、最後3秒だけ結論Visual上へ実チャンネルアイコン180px＋チャンネル名を中央表示。疑似subscribeなし。
- Short001：現行ChatGPT実画面＋公式Voice参照＋生活scene。ライブVoice captureはCAPTURE_REQUIRED。
- Short002：privacy rendererの未マスク→一部マスク→全マスクを静止状態で表示。v4 approved rendererを再利用。
- Short003：デジタル庁公式マイナポータル画面→コンビニ証明書→e-Tax生活scene→医療利用scene。抽象rendererを廃止。
- 音声：3本とも`audio/narration_v4.wav`を再利用。台本変更0、全音声再生成0。

| ID | duration | core | beats | mean static state | >5 sec | ImageGen reuse/new | renderer | real UI/ref | official image | score | Draft v5 |
|---|---:|---:|---:|---:|---:|---|---:|---|---:|---|---|
| Short001 | 28.21秒 | 3 | 6 | 4.70秒 | 2 | 3 reuse / 0 new | 0 | 1 / 1 | 0 | 68/100_REVIEW | `shorts/001_chatgpt_voice_input/output/draft_v5.mp4` |
| Short002 | 32.24秒 | 3 | 7 | 4.61秒 | 0 | 3 reuse / 0 new | 3 | 0 / 0 | 0 | 68/100_REVIEW | `shorts/002_ai_suspicious_message/output/draft_v5.mp4` |
| Short003 | 28.60秒 | 3 | 8 | 3.57秒 | 2 | 4 reuse / 2 new | 0 | 0 / 0 | 1 | 68/100_REVIEW | `shorts/003_mynumber_smartphone/output/draft_v5.mp4` |

## v5 QA / human gate boundary

- micro motion only：0。meaningless zoom：0。meaningless pan：0。static hard cut only。
- dedicated CTA slide：0。CTA icon 180px、center offset 0px。CTA本文は音声字幕で全文表示し、音声canonicalは不変。
- fake UI：0。official UI AI reconstruction：0。privacy fail：0。viewer-facing internal brand promise：0。
- subtitle：target80px、min64px、最大2行、overflow0。Shorts UI overlap：0。
- ImageGen new calls：Short003の2枚のみ。再生成0。NO_IMAGE_TEXT_HYBRID：PASS。
- Short003のマイナポータル画面はデジタル庁公式素材。生成画像は文字なし生活sceneで、公式UIを再現していない。
- Short001 live Voice capture：CAPTURE_REQUIRED。人間Draft Gateで追加収録の要否を判断する。
- final、thumbnail確定、upload、publish、scheduleは未実施。

Contact sheet：`shorts/work/batch_001_draft_contact_sheet_v5.png`
Timeline review：`shorts/work/batch_001_v5_timeline_review.md`

Shorts探索バッチ001 Visual Redesign v5完成。
不要なmicro motionを廃止。
CTA中央化・Short003利用例Visualを具体化。
人間Draft Gate待ち。
