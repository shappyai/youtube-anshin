# ImageGen文字QA

1 scene / auto_fail=0 / vision_review=1

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

### 目視チェック（親Codex/vision）
- [x] 指定文言と一致している
- [x] 誤字なし
- [x] 脱字なし
- [x] 余計な文字なし
- [x] 文字化けなし
- [x] 不自然な漢字置換なし
- [x] 行順が指定どおり
- [x] 文字切れなし
- [x] 画像端にはみ出していない
- [x] 人物・重要オブジェクトと重なっていない
- [x] 背景とのコントラスト十分
- [x] スマホ縮小時でも主見出しが読める

親Codexの画像確認はPASS。公開前の人間Gateでは、元画像と動画尺での最終確認を残す。

