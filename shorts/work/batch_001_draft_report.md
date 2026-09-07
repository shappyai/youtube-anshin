# Shorts探索バッチ001 Draft v1 report

- Phase：B draft完成
- 公開状態：3本ともNOT_UPLOADED
- サムネイル：未作成
- 共通CTA：同一文面を再利用

| ID | duration | scene数 | Fact FAIL | pronunciation | real UI数 | visual QA | draft |
|---|---:|---:|---:|---|---:|---|---|
| Short001 | 27.70秒 | 6 | 0 | REVIEW (human listening pending) | 1 | REVIEW (Voice icon not available in public logged-out screen) | shorts\001_chatgpt_voice_input\output\draft_v1.mp4 |
| Short002 | 30.98秒 | 6 | 0 | REVIEW (human listening pending) | 0 | PASS | shorts\002_ai_suspicious_message\output\draft_v1.mp4 |
| Short003 | 27.34秒 | 6 | 0 | REVIEW (human listening pending) | 0 | PASS | shorts\003_mynumber_smartphone\output\draft_v1.mp4 |

## 共通QA

- CTA duration：各Shortの末尾約2秒。同一文面・同一hash。
- subtitle QA：rendererで2行以内・64px以上を検査。overflow 0を確認。
- vertical safe area：下部220pxと右側のShorts UI領域を避けた。
- visual QA：Short002・003はrenderer中心でPASS。Short001は公開ログアウト画面にVoiceアイコンが出ないためREVIEW。
- privacy：実在メール、企業ロゴ、実QR、個人情報、アカウント履歴は未使用。

## Contact sheet

- shorts\work\batch_001_draft_contact_sheet.png
- 各Shortのwork/contact_sheet.pngも参照する。

Draft v1のため、final、thumbnail、upload、schedule、publishへは進まない。
