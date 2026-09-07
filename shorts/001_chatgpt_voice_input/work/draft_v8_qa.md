# Short001 Draft v8 QA — Dictation + real answer

- target：Short001のみ。Short002 / Short003は変更していない。
- canonical title：`ChatGPT、文字を打たなくても使える？`
- feature：`Dictation / 音声入力`
- duration：29.965秒（30秒程度）
- real answer found：YES
- answer source range：14.200〜17.000秒
- answer video timestamp：20.256〜22.806秒
- answer display duration：2.550秒
- answer processing：元captureのcrop / resizeのみ。回答改変0。
- capture audio：YES（Dictation入力3.800〜12.800秒のみ）
- machine response audio：NO
- script changed segment count：1（実回答scene説明用の短いVOICEVOX文）
- full audio regeneration：0。既存v7音声5本＋v4 CTAを再利用。

## Required QA flags

| Flag | Result |
|---|---|
| real Dictation UI | PASS |
| real ChatGPT answer | PASS |
| fake UI | 0 |
| AI UI reconstruction | 0 |
| Voice / Dictation confusion | 0 |
| privacy FAIL | 0 |
| ChatGPT pronunciation | PASS（トを3モーラ目） |
| capture audio clipping | 0 |
| subtitle overflow | 0 |
| Shorts UI overlap | 0 |
| CTA | PASS（実アイコン180px＋チャンネル名中央、疑似subscribe0） |
| Fact FAIL | 0 |

## Visual order

- ImageGen hook → 実Dictation入力 → 文字化された質問 → 送信 → 実ChatGPT料理回答 → 短い結論ImageGen → CTA。
- 実回答はユーザー提供captureの後半からcrop / resize。回答全文、後半の評価dialog、架空UIは不使用。
- 回答sceneは実画面を主役にし、大きな説明見出しを後乗せしていない。
- motion：意味のないzoom / pan / push-in 0。実capture区間は元録画の自然な動きだけ。

## Protected outputs

- Short002 / Short003 protected files：PASS。

final、upload、publish、scheduleは未実施。人間Draft Gate待ち。
- draft：`shorts/001_chatgpt_voice_input/output/draft_v8.mp4`
- render manifest：`shorts/001_chatgpt_voice_input/work/render_manifest_v8.json`
- answer QA：`shorts/001_chatgpt_voice_input/work/chatgpt_answer_capture_v8.md`
- audio QA：`shorts/001_chatgpt_voice_input/work/voice_capture_audio_qa_v8.md`
