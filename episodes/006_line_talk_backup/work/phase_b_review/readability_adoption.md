# readability 7scene 採用一覧（canonical反映済み）

- date: 2026-09-02
- 反映先: `episode.json` の `official_asset`（7scene）／`shotlist.md`（SHOT-01〜07）／`media_manifest.csv`（status=approved_readability）
- 元素材（`assets/official/*_fallback.png` 等7枚）はすべて保持。削除していない。
- GPT画像・narration・subtitle・scene mappingは変更していない。

| Scene | 動画内 | 採用素材（本編） | 元素材（保持） | 拡大率 |
|---|---:|---|---|---:|
| SCENE-006 | 1:45 | `work/phase_b_review/readability_fix/scene_006_readability.png` | `assets/official/line_backup_transfer_menu_fallback.png` | 2.02 |
| SCENE-007 | 2:03 | `work/phase_b_review/readability_fix/scene_007_readability.png` | `assets/official/line_talk_backup_datetime_fallback.png` | 2.02 |
| SCENE-011 | 2:44 | `work/phase_b_review/readability_fix/scene_011_readability.png` | `assets/official/line_auto_backup_fallback.png` | 1.77 |
| SCENE-014 | 3:29 | `work/phase_b_review/readability_fix/scene_014_readability.png` | `assets/official/line_icloud_drive_crop.png` | 2.02 |
| SCENE-016 | 3:48 | `work/phase_b_review/readability_fix/scene_016_readability.png` | `assets/official/line_backup_pin_fallback.png` | 2.02 |
| SCENE-020 | 4:55 | `work/phase_b_review/readability_fix/scene_020_readability.png` | `assets/official/line_standard_backup_same_os_crop.png` | 2.02 |
| SCENE-022 | 5:24 | `work/phase_b_review/readability_fix/scene_022_readability.png` | `assets/official/line_backup_trouble_media_crop.png` | 2.02 |

## 反映確認

- 24sceneすべてのレンダーが `work/rendered_final_scenes/` に存在（24/24）。
- 動画 `output/draft_v1.mp4` の該当時刻フレームで、readability拡大カード（「拡大表示（実在UIではありません）」ラベル＋赤字免責）が表示されることを確認済み。
- 旧fallback画像が本編フレームに出ないことを確認済み。
