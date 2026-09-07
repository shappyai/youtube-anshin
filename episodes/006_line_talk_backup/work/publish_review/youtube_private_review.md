# Episode 006 YouTube private 確認（人間用）

- uploaded: **true**（2026-09-03 06:06 JST・video_id DK0431L9TwA）
- URL: https://youtu.be/DK0431L9TwA
- 公開設定: **private**（publishAtなし・scheduledなし・unlisted/publicではない）
- 1080p処理: succeeded（APIのprocessingStatusで確認）

## YouTube private確認

- [ ] 1080p処理完了（API確認済み・必要ならStudioで目視）
- [ ] タイトルOK: 【LINE】機種変更の前に確認！トーク履歴を残すバックアップとPIN
- [ ] サムネイルOK（assets/thumbnail/thumbnail.png・1280×720）
- [ ] 概要欄OK（final_metadata.txt と一致・AI開示文あり）
- [ ] チャプターOK（8章・final_chapters.txt と一致）
- [ ] AI生成コンテンツ開示設定OK（YouTube status containsSyntheticMedia=true・videos.updateで検証済み）
- [ ] スマホでサムネイル確認
- [ ] スマホで字幕サイズ確認
- [ ] 冒頭〜末尾を一周確認
- [ ] 公開設定はprivate（public/unlisted/scheduledへ変更しない）

## 重点時刻（動画内）

- 約1:53 SCENE-006（readability・バックアップ・引き継ぎ手順）
- 約2:11 SCENE-007（今すぐバックアップ）
- 約2:52 SCENE-011（自動バックアップ）
- 約3:38 SCENE-014（iCloud Drive）
- 約3:42〜3:55 PIN（seg 39/40）
- 約3:56 SCENE-016（PINコード）
- 約5:04 SCENE-020（同じOSのみ）
- 約5:33 SCENE-022（写真・動画は対象外）
- 約6:28〜末尾 CTA・クロージング

## API確認結果（2026-09-03）

- privacyStatus=private / publishAt=none / license=youtube / madeForKids=false / categoryId=22 / defaultLanguage=ja
- duration=PT6M49S（6:48+丸め） / processingStatus=succeeded / fileDetails duration=408000ms
- title・tags（8件）・サムネイルアップロード確認済み

## 決定後の流れ（この工程では実施しない）

1. 上記チェックがすべてOKなら、人間が公開方法を判断（scheduled or public）
2. public昇格・予約はYouTube Studio/許可された工程で別途実施（本工程では行わない）
