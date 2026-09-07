# Episode 003 draft_auto_v3 QA

確認日: 2026-08-31  
対象: `draft_auto_v3.mp4`。v1 / v2は保存。final化・thumbnail・YouTube操作は未実施。

## v2から保持した内容

- GPT画像8枚のfull_bleed、cover_blur非default、大型白カードなし。
- SCENE-014のstatic、seg_024の`今ブラウン`→`いまブラウン`、seg_043のApp Store承認アクセント、App Store辞書登録。
- 52 narration segment、52 subtitle cue、official assets、既存のscene構成と正常音声。

## 今回の局所修正

| 項目 | 結果 |
|---|---|
| 3:32 scene | SCENE-015。実タイムライン205.238–227.917秒内 |
| 左寄りの原因 | layout_06_cautionのシンボルと文章群がx=120–1080付近で完結し、右側をgradientだけで補っていた |
| 位置修正 | シンボル・headline・support・main messageをグループとして`content_offset_x=360px`移動。主な範囲を約x=480–1440へ変更し、視覚中心を画面中央付近へ戻した |
| animation | static。横panなし |
| GPT画像 | 今回は新規生成なし。8枚ともv2のfull_bleedを維持 |

## 新CTA

- ロゴ: `local/channel/icon.png`
- Episode 001から参考にした要素: 白〜淡色の落ち着いた背景、青・緑のアクセント、ロゴとチャンネル名の明確な階層、控えめな登録誘導、静止画中心の終端構成。
- 表示文言:
  - `やさしく・安全に・安心して`
  - `大人のデジタル安心室`
  - `スマホやパソコンを、もっと安全・快適に使うための情報をお届けします`
  - `チャンネル登録・高評価もよろしくお願いします`
  - `怖がらせる前に、確認する。`
- CTAは10.046秒のstatic postroll。新ナレーション・CTA専用字幕なし。
- Episode 002の`scene_034.png`はruntimeのpostrollから完全に除去。`episode.json`は`cta_v3.png`を参照し、旧文言`慌てて消す前に、まず確認する`は新CTAに含めていない。

## Build / Cache

| Check | Result | Detail |
|---|---|---|
| Phase A integrated gate | PASS | episode schema / sources / subtitles / pronunciation / scenes / scene modes / official assets / GPT images |
| VOICEVOX regenerated | PASS | 0 segment |
| VOICEVOX cache | PASS | 52 / 52 reused |
| narration / subtitles | PASS | 52 / 52 / 52 / 52 |
| CTA asset | PASS | PNG / 1920×1080 / 破損なし |

## Video QA

| Check | Result | Detail |
|---|---|---|
| v2 duration | PASS | 300.833333 sec |
| v3 duration | PASS | 300.833333 sec。CTA表示時間は10.046秒 |
| v1 / v2 preservation | PASS | v1・v2のファイルとSHA-256を照合し、v3生成前後で変更なし |
| video stream | PASS | H.264 / 1920×1080 / 30 fps |
| audio stream | PASS | AAC / 48,000 Hz / mono |
| black frame | PASS | 0件 |
| missing frame / scene | PASS | 18 content sceneを全数使用、欠落なし |
| duplicate scene anomaly | PASS | 18 rendered sceneの完全一致重複なし |
| 3:32 | PASS | 実動画フレームでSCENE-015のコンテンツが中央付近。横panなし |
| CTA end | PASS | v3最終フレームで現行ロゴ・チャンネル名・登録/高評価誘導を確認 |

## Audio / Subtitle / Asset QA

| Check | Result | Detail |
|---|---|---|
| audio | PASS | 52/52、音声変更なし、欠落・異常無音・clippingなし |
| subtitle cue count | PASS | 52 / 52。再分割なし |
| subtitle layout | PASS | 1文字cueなし、overflowなし、下部180px安全帯を維持 |
| official asset missing | PASS | 0件 |
| GPT image assets | PASS | 8/8、PNG・1920×1080・破損なし |
| unresolved placeholder | PASS | 0件 |
| v2 rules | PASS | full_bleed / no large white card / cover_blur非default / App Store accent / `いまブラウン`を維持 |

## WARN / FAIL

- WARN: なし
- FAIL: なし
- 人間確認待ち: v3を最後まで視聴し、3:32の視覚中心、4:53以降のCTAの読みやすさ・表示時間・Episode 001とのブランド連続性を確認する。

成果物:

- `episodes/003_line_renewal/output/draft_auto_v3.mp4`
- `episodes/003_line_renewal/output/review/cta_v3.png`
- `episodes/003_line_renewal/output/review/scene_015_v3.png`

## Finalization addendum

- 人間最終レビュー: approved
- 承認対象: `episodes/003_line_renewal/output/draft_auto_v3.mp4`
- finalize: 再encodeせず `output/final.mp4` へcopy
- YouTube upload / thumbnail / publish: 未実施
