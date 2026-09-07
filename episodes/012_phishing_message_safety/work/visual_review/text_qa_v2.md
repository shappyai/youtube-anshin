# ImageGen文字QA

6 scene / auto_fail=0 / vision_review=6

ルール: imagegen_native → 文字QA → PASSなら採用 / FAILなら1回だけ再生成 / 2回目のFAILで pil_overlay へfallback（docs/text_render_policy.md）。

## SCENE-001 — imagegen_native

- headline: `リンクから入らない`
- support_text: `公式を自分で開く`
- image: `C:\Codex\260829_youtube-anshin\episodes\012_phishing_message_safety\assets\generated_ai\scene_001.png`
- text_qa: status=`passed` retry_count=0 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] promptにheadline文言が含まれている
- [x] promptにsupport_text文言が含まれている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: 580bc8eb7aeb488a...

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

- headline: `支払い方法の更新`
- support_text: `1 / 5　通販・普段使うアプリ`
- image: `C:\Codex\260829_youtube-anshin\episodes\012_phishing_message_safety\assets\generated_ai\scene_005.png`
- text_qa: status=`passed` retry_count=0 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] promptにheadline文言が含まれている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: 7c7bf688b645ffe3...

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

## SCENE-010 — imagegen_native

- headline: `再配達のお願い`
- support_text: `2 / 5　宅配・SMS`
- image: `C:\Codex\260829_youtube-anshin\episodes\012_phishing_message_safety\assets\generated_ai\scene_010.png`
- text_qa: status=`passed` retry_count=0 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] promptにheadline文言が含まれている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: f4043b030427341c...

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

## SCENE-016 — imagegen_native

- headline: `カードの利用確認`
- support_text: `3 / 5　通知が本物でも、入口は自分で`
- image: `C:\Codex\260829_youtube-anshin\episodes\012_phishing_message_safety\assets\generated_ai\scene_016.png`
- text_qa: status=`passed` retry_count=0 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] promptにheadline文言が含まれている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: 838da003e6996aa4...

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

## SCENE-020 — imagegen_native

- headline: `料金が未払いです`
- support_text: `4 / 5　携帯会社・通信料金`
- image: `C:\Codex\260829_youtube-anshin\episodes\012_phishing_message_safety\assets\generated_ai\scene_020.png`
- text_qa: status=`passed` retry_count=0 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] promptにheadline文言が含まれている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: 0f414b04cc605cd7...

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

## SCENE-024 — imagegen_native

- headline: `公的なお知らせ`
- support_text: `5 / 5　役所・公的機関を装う連絡`
- image: `C:\Codex\260829_youtube-anshin\episodes\012_phishing_message_safety\assets\generated_ai\scene_024.png`
- text_qa: status=`passed` retry_count=0 fallback=None

### 自動チェック（PASS）
- [x] 文言仕様がsceneに定義されている
- [x] promptにheadline文言が含まれている
- [x] 生成画像が配置されている
- [x] アスペクト比がおおよそ16:9
- [x] 画像サイズが1280x720以上
- [x] SHA-256: 9d98637df6781498...

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

