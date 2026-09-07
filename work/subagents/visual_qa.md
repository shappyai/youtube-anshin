# Episode 005 Phase B前半 — Visual QA

確認日: 2026-09-01（JST）  
担当: 親Codexによる補完確認（Visual QA agentは長時間の反復読み込みを停止し、同じレビュー対象を機械チェック＋contact sheet目視で完了）

## 総合判定

**REVIEW / STOP**。レビュー用stillは25 scene中24 sceneが1920×1080で生成され、contact sheetで確認できる。SCENE-022の復元UIは未取得のため、推測の画面を作らず未取得タイルにした。字幕の安全幅超過12件と、音声QAのseg046 STOPは解消前にdraftへ進めない。

## 機械チェック

| 項目 | 結果 |
|---|---|
| scene数 | 25 |
| rendered still | 24/25、すべて1920×1080。欠落はSCENE-022のみ |
| GPT画像 | 5/5、レビュー用normalized_aiは1920×1080 |
| GPT画像SHA重複 | 0 group |
| item数整合 | 指摘なし |
| 1文字だけのsubtitle cue | 0件 |
| Visual balance / letterbox | 自動指摘なし。人間レビューは残す |
| subtitle safe width | FAIL 12件（SUB-004/015/020/023/032/034/044/045/047/051/062/064） |
| scene text linebreak | WARN 2件（SCENE-020 support_textの「確認」、SCENE-025 headlineの「確認」） |

## GPT画像の確認

- SCENE-001/003/013/017/025は一枚のfull-frame背景で、collage、storyboard、split panel、grid、巨大な白い片側、読める生成UI・ロゴは目視なし。
- SCENE-017は1枚の写真からバックアップコピーが1つのクラウドへ流れる構図で、独立した2つの写真ライブラリには見えない。
- 下180pxの可読性はWARN。自動検出ではSCENE-001/003/017/025に下部の視覚要素があり、生成担当の目視注記ではSCENE-003/013にも字幕帯への一部重なりがある。再生成はせず、contact sheet＋実尺字幕を人間確認する。
- 原本1672×941は保持し、1920×1080の正規化copyをレビュー用に分離した。原本の上書きなし。

## 公式・実画面の確認

- AndroidのSCENE-004/006/008/012/014は、Googleフォトの実画面cropを使用。SCENE-004は「バックアップ済み」補助表示で、Phase A記載の「バックアップが完了しました」は未取得。SCENE-006はゴミ箱操作前の画面で、削除後の反映は未検証。いずれもREVIEW。
- SCENE-008/012/014は、ゴミ箱の60日/30日、デバイスから削除、空き容量を増やす表示が読める。SCENE-008はゴミ箱内アイテム表示ではなく保持期間確認用。
- SCENE-018/019は、保存済みGoogle/Apple公式HTMLからのcrop。実機画面と誤認させず、公式ページfallbackとして扱う。viewport版のApple `null`表示は不採用。
- 個人情報、個人写真、通知、地図、GPS、ログイン済み識別子は採用cropに見当たらない。Androidは自作ダミー1枚のみで撮影し、完全削除は行っていない。
- 旧Episodeの画像・文言の混入はcontact sheet上で確認されなかった。テスト入力名の`episode005_safe_dummy`はAndroidの自作ダミー由来で、公開用の人物・個人情報ではない。

## 人間確認の優先順位

1. SCENE-022を専用テスト環境で再取得するか判断（復元UIを推測で代替しない）。
2. SCENE-004の完了表示、SCENE-006の削除後反映、SCENE-008のアイテム表示を追加確認するか判断。
3. SUB-004等12件の字幕幅とSCENE-020/025の「確認」改行を、72px前後・最大2行の範囲で修正確認。
4. GPT画像の下180px、SCENE-018の2枚組の文字可読性、SCENE-019の公式本文の読みやすさを実尺表示で確認。

## 成果物

- `episodes/005_google_photos_delete/work/phase_b_review/scene_contact_sheet.png`
- `episodes/005_google_photos_delete/work/phase_b_review/gpt_image_contact_sheet.png`
- `episodes/005_google_photos_delete/work/phase_b_review/rendered_scenes/`
- 機械結果: `episodes/005_google_photos_delete/work/phase_b_review/visual_checks.json`

canonical fileは変更していない。VOICEVOX音声・draft・finalは未作成。
