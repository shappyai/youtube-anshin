# Episode017 Privacy QA Final

- status: **PASS**
- Human Gate 2で、`draft_auto_v2.mp4`を全編確認済み。個人情報がないことを確認済み。
- productionで使用するiPhone画面は、Human提供の正規化cropのみ。`media_manifest.csv`のSHOT-01〜05はprivacy pass、SHOT-03はmaskedとして記録。
- バッテリー使用状況の個人利用が推測できるアプリ一覧はviewer-facingに使用していない。
- Apple Account、メールアドレス、電話番号、端末名、通知内容、位置情報履歴、シリアル番号などをproduction asset・scene構成・字幕・ナレーションに残していない。
- raw `screenshots/` はローカル保管のみで、Git追跡対象外。マスク前素材をproduction assetとして追加していない。
- Apple UIのAI生成・再現はない。公式UI sceneはHuman提供実画面の`official` assetのみで、その他はrenderer-nativeの説明scene。
- 個人情報を含む可能性のある新規撮影・設定変更は行っていない。
