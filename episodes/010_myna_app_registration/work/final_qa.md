# Episode 010 Final QA

確認日: 2026-09-06  
対象: `output/final.mp4`  
判定: **PASS**

## Final artifact

- source: `output/draft_v2.mp4`
- method: copy-only、再エンコードなし
- byte-identical: **PASS**
- SHA-256: `89BBDE65D864944B1E0940E077ADD8C3094997CBD44DCF26A286F0492D830374`
- size: `20,017,692 bytes`
- duration: `219.486 seconds`（ffmpeg表示 `00:03:39.49`）
- video: H.264 / `1920×1080` / `30fps`
- audio: AAC / `48kHz` / mono

## Required gates

| QA項目 | 結果 | 根拠 |
|---|---|---|
| decode error | 0 | final.mp4をvendor ffmpegでdecode、return code 0 |
| black frame | 0 | blackdetectの該当区間0 |
| unexpected silence | 0 | narration WAVに2秒以上の想定外無音なし。終端約3.69秒はCTA余韻 |
| audio peak error | 0 | max peak `-0.9dB`、0dB超過なし |
| av sync | PASS | 実測音声タイムライン・字幕・CTAを維持し、期待尺219.486秒に一致 |
| subtitle | PASS | 44 cue、minimum72px、font<56=0、overflow0、3-line0、unnatural split0、TTS leakage0 |
| privacy | PASS | `privacy_qa_v2.md`、final contentはdraft_v2と同一 |
| official UI integrity | PASS | デジタル庁公式原画とfocus crop 6件を維持。AI再現なし |
| senior readability | PASS | ユーザーによるdraft_v2全編確認で承認 |
| Visual Gate regression | 0 | draft_v2 correction QAおよびbyte-identical final |
| CTA clipping | 0 | CTA preflight PASS、60px、説明行+110px |
| End Screen reserved | PASS | 右40〜45%を動画側で予約 |
| intro micro story | PASS | 冒頭の迷いから実操作へ接続 |
| first action <=30s | PASS | 28.516秒 |
| registration_conversion_v1 | PASS | story_intro、reason_to_return_cta、midroll_cta0、duplicate_cta0 |
| fact error count | 0 | `fact_check.md`の公開前最終確認 |

## Viewer-facing ID scan

- 対象: narration、字幕、rendered scene、CTA、description
- `Episode 007` / `Episode007` / `E007` / `EP007` / `Episode 010` / `E010` / `EP010`: **0件**
- End Screen候補の内部routing情報は公開動画外の管理メタデータに限定する。

## Fact review

- Fact error count: **0**
- Fact REVIEW: **2**（FC-019 現行実機UI照合、FC-020 Android対応機種照合）
- 残る2件は更新・実機依存の運用確認。動画内では機種・画面変更を断定しない。

## Upload guard

- 既存のYouTube video ID：`rU5jlU7eq3I`（今回の1回のuploadで発行）
- upload attempt record：`work/youtube_publish/upload_attempt.json`、status=`uploaded_scheduled`
- publish scriptの既存ID検出とdraft拒否、retry時にvideos.insertを呼ばない保護を確認済み
- thumbnail：`assets/thumbnail/thumbnail.png`、1280×720、1,147,245 bytes、thumbnail QA **PASS**、API設定 **PASS**
- upload：**PASS**（private、予約時刻、title、channel、madeForKidsをAPI確認）
- synthetic media：**PASS**（status-only `videos.update` responseで`containsSyntheticMedia=true`を確認、video ID不変）

## Publish boundary

- title、description、chapters、category、言語、made-for-kids、synthetic media設定を `publish.json` に確定。
- `thumbnail_status=HUMAN_SELECTED`。ユーザー指定のChatGPT生成原本を受領し、公開用画像のQA・API設定はPASS。
- `upload_status=UPLOADED_SCHEDULED`。`rU5jlU7eq3I`をprivateで2026-09-06 19:00 JSTへ予約済み。
- End ScreenはYouTube Studioで関連動画とチャンネル登録を人間設定する。動画側の右40〜45% reservedは維持。

機械可読記録: `final_qa.json`
