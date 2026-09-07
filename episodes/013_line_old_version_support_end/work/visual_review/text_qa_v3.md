# ImageGen文字QA

5 scene / auto_fail=0 / vision_review=5

ルール: imagegen_native → 文字QA → PASSなら採用 / FAILなら1回だけ再生成 / 2回目のFAILは生成画像を捨て、renderer-onlyへ再設計（NO_IMAGE_TEXT_HYBRID）。

## SCENE-001 — imagegen_native

- headline: `11月に使えなくなる？`
- support_text: `全員ではありません。まず3つ確認`
- image: `C:\Codex\260829_youtube-anshin\episodes\013_line_old_version_support_end\assets\generated_ai_v2\scene_001.png`
- text_qa: status=`passed` retry_count=0 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: 251a28531ef38210...

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

## SCENE-004 — imagegen_native

- headline: `LINEのバージョンを確認`
- support_text: `まずアプリの数字を見る`
- image: `C:\Codex\260829_youtube-anshin\episodes\013_line_old_version_support_end\assets\generated_ai_v2\scene_004.png`
- text_qa: status=`passed` retry_count=1 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: 74686a661f8521fc...

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

## SCENE-008 — imagegen_native

- headline: `スマホのOSを確認`
- support_text: `LINEとは別に見る`
- image: `C:\Codex\260829_youtube-anshin\episodes\013_line_old_version_support_end\assets\generated_ai_v2\scene_008.png`
- text_qa: status=`passed` retry_count=0 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: 95a0ade0aed347ae...

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

## SCENE-012 — imagegen_native

- headline: `更新できるか確認`
- support_text: `3つ目は更新の可否`
- image: `C:\Codex\260829_youtube-anshin\episodes\013_line_old_version_support_end\assets\generated_ai_v2\scene_012.png`
- text_qa: status=`passed` retry_count=0 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: 0284102e484f56e7...

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

## SCENE-022 — imagegen_native

- headline: `買い替え前に確認`
- support_text: `LINE → OS → 次の手順`
- image: `C:\Codex\260829_youtube-anshin\episodes\013_line_old_version_support_end\assets\generated_ai_v2\scene_022.png`
- text_qa: status=`passed` retry_count=1 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: dd4516ae7d660786...

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

