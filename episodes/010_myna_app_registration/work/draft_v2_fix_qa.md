# Episode 010 draft_v2 修正QA

確認日：2026-09-06

## 変更範囲

- 3:03付近：segment 038のnarration、subtitle、SCENE-019の視聴者向け文言を更新。
- 3:30付近：CTA「次に困ったときのために」の説明ボックスを下方向へ110px移動。
- segment 038の音声1件とSCENE-019のPNG 1件を再生成。ほか40音声segment、19scene、CTA音声11.456秒は再利用。
- `draft_v1.mp4`は比較用に保持し、`draft_v2.mp4`を別ファイルとして生成。

## Required QA

| QA | Result | Evidence |
|---|---|---|
| internal_episode_number_visible | 0 | viewer-facing canonical fields、字幕、scene、CTA、descriptionの文字列scan |
| internal_episode_number_spoken | 0 | narration canonical textの文字列scan |
| related_video_wording | PASS | 「読み取れない、ログインできないときは、関連動画で確認してください。」 |
| subtitle_sync | PASS | SUB-038はsegment 038の実測区間179.193–184.142秒に同期 |
| cta_visual_balance | PASS | 説明行を+110px。登録文言との1ブロック構成を維持 |
| cta_clipping | 0 | CTA preflight PASS、60px |
| end_screen_reserved | PASS | 右側reserved領域を維持 |
| subtitle_safe_area | PASS | bottom 180pxを侵食しない |
| draft_v1_regression | 0 | 20scene、6 official focus crop、28.516秒first action、72px字幕、CTA音声11.456秒、titleを維持 |

## Internal ID scan

scan対象は視聴者向けの`episode.json`（narration / display_text / subtitles / scene text / publish.description）、`script.md`、`scene_plan.json`、`publish.json`、`captions.srt`、`captions.ass`、CTA config。`Episode 007`、`E007`、`EP007`、`エピソード007`は0件。制作管理用のbrief・research・shotlistにある内部routingメモは対象外。

## Fact / Human gate

- Fact FAIL：0
- Fact REVIEW：3（FC-015、FC-019、FC-020。実機・撮影直前確認が必要）
- `internal_episode_id_not_viewer_facing`：PROPOSED。canonical化は人間判断待ち。
- 次の停止位置：`output/draft_v2.mp4`の人間全編確認。thumbnail、finalize、YouTube公開は未実施。
