# ImageGen文字QA

3 scene / auto_fail=0 / vision_review=3

ルール: imagegen_native → 文字QA → PASSなら採用 / FAILなら1回だけ再生成 / 2回目のFAILで pil_overlay へfallback（docs/text_render_policy.md）。

## SCENE-001 — imagegen_native

- headline: `Windows 11
このままで大丈夫？`
- support_text: `10月13日までに、確認すること`
- image: `C:\Codex\260829_youtube-anshin\episodes\009_windows11_24h2_support\assets\generated_ai\scene_001.png`
- text_qa: status=`passed` retry_count=0 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: ed0a5ec6a153be2b...

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

## SCENE-015 — imagegen_native

- headline: `慌てて買い替えなくて大丈夫`
- support_text: `10月13日までに、まずバージョンと更新を確認`
- image: `C:\Codex\260829_youtube-anshin\episodes\009_windows11_24h2_support\assets\generated_ai\scene_015.png`
- text_qa: status=`passed` retry_count=0 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] promptにheadline文言が含まれている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: 39b089e39fd9ab76...

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

## SCENE-019 — imagegen_native

- headline: `まずバージョンを確認`
- support_text: `役に立ったら、チャンネル登録して、次回も一緒に確認しましょう。`
- image: `C:\Codex\260829_youtube-anshin\episodes\009_windows11_24h2_support\assets\generated_ai\scene_019.png`
- text_qa: status=`passed` retry_count=0 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] promptにheadline文言が含まれている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: 33f20834d8ae48f5...

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

