# Episode 003 draft_auto_v2 QA

確認日: 2026-08-31  
対象: `draft_auto_v2.mp4`。v1は保存。final化・thumbnail・YouTube操作は未実施。

## 前回から維持したもの

- 台本全体、既存52字幕cue、正常な50件前後の音声、official/template sceneは変更なし。
- 人間確認済みの新GPT画像8枚を使用。旧v1動画は`draft_auto_v1.mp4`として保存。

## 修正内容

| 対象 | 結果 |
|---|---|
| 0:04 / 0:33 / 1:24 / 2:12 / 2:58 / 3:04 / 3:50 / 4:33 | SCENE-001 / 003 / 007 / 010 / 013 / 014 / 016 / 018。新PNGを1920×1080 full_bleedで使用し、左右の追加白余白なし |
| 3:27 | SCENE-015。templateの右側をsoft gradientで連続化 |
| 3:13 | SCENE-014。横方向panを無効化しstatic |
| 2:07 | seg_024。`今ブラウン`→`いまブラウン`のsegment overrideを維持 |
| 3:56 | seg_043。`App Store`→`アップストア`を1アクセント句、accent=5で再生成 |
| 終盤 | Episode 002の`scene_034.png`をCTA postrollとして10.046秒再利用 |

GPT画像の描画標準は`full_bleed`を既定とし、`cover_blur`は既定化していない。Codexは大きな白カードや別layoutを追加せず、指定された日本語文字と文字周囲の局所scrimだけを描画した。

## Build

| Check | Result | Detail |
|---|---|---|
| Phase A integrated gate | PASS | episode schema / sources / subtitles / pronunciation / scenes / scene modes / official assets / GPT images |
| pronunciation | PASS | remaining review=0。人間承認4件を適用 |
| GPT image assets | PASS | 8/8、すべてPNG・1920×1080・破損なし |
| VOICEVOX | PASS | 剣崎雌雄 / ノーマル / speed 1.00 / intonation 1.00 / pitch 0.00 |
| narration segments | PASS | 52 / 52 WAV |
| audio diff build | PASS | regenerated: seg_043のみ / cache reuse: 51 |
| subtitles | PASS | episode.jsonの52 cueを実測音声タイムラインへ配置。再分割なし |
| scenes | PASS | 18 / 18 content scene。template 3 / official 7 / gpt_image 8 |

## Video QA

| Check | Result | Detail |
|---|---|---|
| v1 duration | PASS | 290.800 sec。ファイル保持を確認 |
| v2 duration | PASS | 300.833 sec。本編290.887 + CTA想定10.046 = 300.933 secとの差0.100 sec |
| video stream | PASS | H.264 / 1920×1080 / 30 fps |
| audio stream | PASS | AAC / 48,000 Hz / mono |
| black frame | PASS | 0件 |
| missing frame / scene | PASS | 18 content sceneのrendered PNGを全数確認、欠落なし |
| duplicate scene anomaly | PASS | 18 rendered sceneの完全一致重複なし |
| official focus scenes | PASS | SCENE-004 / 005 / 006 / 008 / 009 / 011 / 012を含む |
| CTA | PASS | Episode 002 `scene_034.png`を末尾10.046秒表示。最終フレームで文章・登録カードを確認 |

## Audio / Subtitle / Asset QA

| Check | Result | Detail |
|---|---|---|
| audio | PASS | 52/52 segment、missingなし、2秒以上の異常無音なし、clippingなし |
| seg_024 | PASS | episode.jsonのsegment overrideは`今ブラウン`→`いまブラウン`。既存の修正版WAVを再利用 |
| seg_043 query | PASS | 実生成auditで`アップストア`が1 phrase、6 mora、accent=5。5番目「ト」の後で6番目「ア」が下降 |
| subtitle cue count | PASS | 52 / 52 |
| subtitle layout | PASS | 1文字cueなし、overflowなし、下部180px安全帯、Yu Gothic Bold、白文字・黒outline |
| unresolved placeholder | PASS | 0件 |
| official asset missing | PASS | 0件 |
| GPT image fallback | PASS | gpt_image sceneをtemplateへfallbackしていない |
| AI 9 timestamp visual check | PASS | 指定時刻をSCENE-001 / 003 / 007 / 010 / 013 / 014 / 015 / 016 / 018へ対応付け。full_bleedまたはsoft gradientで画面端まで成立 |

## WARN / FAIL

- WARN: なし
- FAIL: なし
- 人間確認待ち: v2を最後まで視聴し、指定9時刻の見え方、SCENE-014の静止、2:07・3:56の発音、CTAのテンポを確認する。
