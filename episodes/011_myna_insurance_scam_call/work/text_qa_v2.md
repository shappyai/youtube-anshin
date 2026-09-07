# ImageGen文字QA

2 scene / auto_fail=0 / vision_review=2

ルール: imagegen_native → 文字QA → PASSなら採用 / FAILなら1回だけ再生成 / 2回目のFAILで pil_overlay へfallback（docs/text_render_policy.md）。

## SCENE-001 — imagegen_native

- headline: `その電話、本物？`
- support_text: `マイナ保険証の確認を口実にした電話`
- image: `C:\Codex\260829_youtube-anshin\episodes\011_myna_insurance_scam_call\assets\generated_ai\scene_001.png`
- text_qa: status=`passed` retry_count=0 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] promptにheadline文言が含まれている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: b1b66ade4dc55543...

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

## SCENE-018 — imagegen_native

- headline: `迷ったら、その場で決めない`
- support_text: `いったん止まって、公式から確認`
- image: `C:\Codex\260829_youtube-anshin\episodes\011_myna_insurance_scam_call\assets\generated_ai\scene_018.png`
- text_qa: status=`passed` retry_count=1 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] promptにheadline文言が含まれている
- [x] promptにsupport_text文言が含まれている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: 9f60c19ed62b3613...

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

