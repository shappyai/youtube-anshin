# Episode 009 Final QA

確認日: 2026-09-05  
対象: `output/final.mp4`  
判定: **PASS**

## Final artifact

- source: `output/draft_v3.mp4`
- method: copy-only、再エンコードなし
- byte-identical: **PASS**
- SHA-256: `e4e181b9a264f00bae04673352bf88676c47982508fcfe6de4b73ad5c825fc70`
- size: `28,770,325 bytes`
- duration: `304.880 seconds`
- video: H.264 / `1920×1080` / `30fps`
- audio: AAC / `48kHz` / mono

## Required gates

| QA項目 | 結果 | 根拠 |
|---|---|---|
| decode | PASS | return code 0 |
| black frame | PASS | 0 |
| unexpected narration silence | PASS | 0 |
| visual regression | PASS | Visual Gate v2 regression 0 |
| subtitle regression | PASS | 0、59 cue、minimum 72px、overflow 0、3-line 0、TTS leakage 0 |
| privacy | PASS | 一時原画なし、canonical reference 0 |
| CTA regression | PASS | CTA preflight PASS、音声11.563秒 |
| pronunciation unresolved | PASS | 0。残り2件は人間承認済み |
| fact error count | PASS | 0 |
| fact review count | PASS | 0 |

Chapterは実測scene開始に一致（`00:00 / 01:08 / 01:55 / 02:52 / 03:55 / 04:29`）。Visual Gate v2、字幕、CTA、公式UI crop、draft_v1 / draft_v2は変更せず保持した。

機械可読記録: `final_qa.json`
