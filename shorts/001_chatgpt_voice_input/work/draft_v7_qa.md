# Short001 Draft v7 QA — Dictation

- target：Short001のみ。Short002 / Short003は変更していない。
- canonical title：`ChatGPT、文字を打たなくても使える？`
- feature：`Dictation / 音声入力`
- duration：27.345秒（30秒以内）
- script changed segment count：4
- Voice関連文言削除数：5件（VOICEVOXというナレーター名は除外）
- capture source：`shorts/work/ChatGPT Voice画面録画.MP4`
- capture used：3.800〜12.800秒（9.000秒）
- capture audio used：YES
- capture audio processing：70Hz high-pass＋volume 0.45。強いdenoise / gateなし。

## Required QA flags

| Flag | Result |
|---|---|
| feature | Dictation |
| Voice / Dictation confusion | 0 |
| real Dictation UI | PASS |
| fake UI | 0 |
| AI UI reconstruction | 0 |
| capture audio clipping | 0 |
| capture audio intelligibility | PASS_WITH_HUMAN_LISTENING |
| audio transition | PASS（capture区間へVOICEVOXを重ねない） |
| ChatGPT pronunciation | PASS（トを3モーラ目） |
| subtitle overflow | 0 |
| Shorts UI overlap | 0 |
| CTA | PASS（実アイコン180px＋チャンネル名中央、疑似subscribe0） |
| Fact FAIL | 0 |
| privacy FAIL | 0 |

## Visual order

- ImageGen-native hook → 実画面のマイク入力中 → 実録画の話す／文字起こし → 文字化後の質問確認 → ImageGen-native conclusion → CTA。
- 実画面はユーザー提供captureのcrop・resizeだけ。公式UIのAI再構成0。
- actual question：`冷蔵庫にキャベツがあります。簡単な料理を教えてください。`。返答全文と後半の評価dialogは使用していない。
- motion：意味のないzoom / pan / push-in 0。静止stateはhard cut、capture区間は元録画の自然なフレーム変化だけ。

## Protected outputs

- Short002 / Short003 v5 protected files：PASS。

final、upload、publish、scheduleは未実施。人間Draft Gate待ち。
- draft：`shorts/001_chatgpt_voice_input/output/draft_v7.mp4`
- render manifest：`shorts/001_chatgpt_voice_input/work/render_manifest_v7.json`
- audio QA：`shorts/001_chatgpt_voice_input/work/voice_capture_audio_qa.md`
