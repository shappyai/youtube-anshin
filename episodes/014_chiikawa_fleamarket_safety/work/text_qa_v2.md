# ImageGen文字QA

2 scene / auto_fail=0 / vision_review=2

ルール: imagegen_native → 文字QA → PASSなら採用 / FAILなら1回だけ再生成 / 2回目のFAILは生成画像を捨て、renderer-onlyへ再設計（NO_IMAGE_TEXT_HYBRID）。

## SCENE-001 — imagegen_native

- headline: `限定品を買う前に確認`
- support_text: `フリマで見つけたときの5つ`
- image: `C:\Codex\260829_youtube-anshin\episodes\014_chiikawa_fleamarket_safety\assets\generated_ai\scene_001.png`
- text_qa: status=`PASS` retry_count=1 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: fb1d8cdda0264e67...

### 目視チェック（人間/vision）
- [ ] 指定文言と一致している
- [ ] 誤字なし
- [ ] 脱字なし
- [ ] 余計な文字なし
- [ ] 文字化けなし
- [ ] 不自然な漢字置換なし
- [ ] 行順が指定どおり
- [ ] 文字切れなし
- [ ] 画像端にはみ出していない
- [ ] 人物・重要オブジェクトと重なっていない
- [ ] 背景とのコントラスト十分
- [ ] スマホ縮小時でも主見出しが読める

## SCENE-005 — imagegen_native

- headline: `残り1個
どうする？`
- support_text: `架空の例`
- image: `C:\Codex\260829_youtube-anshin\episodes\014_chiikawa_fleamarket_safety\assets\generated_ai\scene_005.png`
- text_qa: status=`PASS` retry_count=0 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] promptにsupport_text文言が含まれている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: 9d9468204584228e...

### 目視チェック（人間/vision）
- [ ] 指定文言と一致している
- [ ] 誤字なし
- [ ] 脱字なし
- [ ] 余計な文字なし
- [ ] 文字化けなし
- [ ] 不自然な漢字置換なし
- [ ] 行順が指定どおり
- [ ] 文字切れなし
- [ ] 画像端にはみ出していない
- [ ] 人物・重要オブジェクトと重なっていない
- [ ] 背景とのコントラスト十分
- [ ] スマホ縮小時でも主見出しが読める

