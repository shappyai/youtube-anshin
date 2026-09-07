
## 2026-09-04T12:47:48Z
- timestamp: 2026-09-04T12:47:48Z
- mode: private
- final_sha256: 80AD01947A57A4AAFF4745122BFE35B41B7F62009E89BA43664BEF8621289393
- title: 【マイナアプリ】ログインできない？まず確認したい5つ
- video_id: CAb0b7n0ByY
- privacy: private
- thumbnail_status: success
- verification: failed
- error: PublishError

## 2026-09-04T12:49:47Z（verification 完了・記録更新）
- 原因: videos.list(part=status) が containsSyntheticMedia を返さない（YouTube API 仕様）ため upload 直後の verify が停止
- 対応: 既存フォールバック経路（--set-ai-disclosure true → videos.update 応答で accepted 確認）
- ai_disclosure: containsSyntheticMedia=true verified（update response status に含まれることを確認）
- privacyStatus: private（videos.list 実測）
- selfDeclaredMadeForKids: false
- uploadStatus: processed
- channelId: UCgVRceTJYO5KOrPX4w2jXZw
- description: 存在（1085 bytes）
- duration: PT6M41S（400.4s）
- final_status: uploaded_private / verification: PASS

## 2026-09-04T12:49:47Z
- timestamp: 2026-09-04T12:49:47Z
- mode: set-ai-disclosure
- video_id: CAb0b7n0ByY
- privacy: private
- verification: PASS (videos.update response; videos.list omitted containsSyntheticMedia)
- api_operation: videos.update(part=status)
- ai_disclosure: containsSyntheticMedia = true
- reupload: NO
- made_for_kids_before: False
