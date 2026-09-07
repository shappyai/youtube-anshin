# draft_v1 → draft_v2 変更点一覧（Episode 006）

- date: 2026-09-03
- 入力: `output/draft_v1.mp4` → 出力: `output/draft_v2.mp4`
- 方針: 人間レビューで指摘された2点のみ修正。他は一切変更していない。

## 1. readability 7sceneの入れ子表示を解消

- 原因: readability PNG（完成済み1920×1080）を、通常のofficial sceneレイアウト（タイトル＋説明＋素材枠）の素材枠へ縮小配置していたため、タイトル・説明が二重表示になっていた。
- 修正: readability PNGそのものをscene全面表示に変更。
  - `scripts/hybrid_scene_renderer.py`: `render_official_scene` に `full_bleed_asset` 対応を追加（flag時はassetをそのまま全面描画。タイトル・説明・枠を追加しない）。
  - `episodes/006_line_talk_backup/episode.json`: SCENE-006/007/011/014/016/020/022 に `"full_bleed_asset": true` を追加（`official_asset` は従来どおりreadability PNGを参照）。
  - 全24sceneを再レンダー。7sceneはreadability PNGと**ピクセル完全一致**であることを確認（`work/rendered_final_scenes/scene_006.png` 等）。
  - 二重タイトル・二重footer・カード枠内縮小はすべて消滅。下部字幕帯は既存方式のまま。

## 2. PINのVOICEVOXイントネーションを統一

- 修正: 「PIN」を「ピーアイエヌ」（エンジンmora表記: ピイアイエヌ）と読み、ピー低→アイで上がる→エヌまで高めを維持（アクセント位置6）する辞書エントリを追加。
  - `config/voicevox_pronunciation.yaml`: PINエントリ（method: accent_phrases / reading: ピイアイエヌ / accent: 6 / accent_on_phrase: true / scope: episodes/006）。
  - `scripts/tts_voicevox.py`: 既存の句列組み替え方式だと後続（です・コード・の）も再アクセントされるため、句頭一致でアクセントだけを設定する `accent_on_phrase`（opt-in）を追加。他エントリ・他Episodeには影響なし。
  - Episode 006の全出現5seg（7/39/40/45/66）に適用。audio_queryで全5箇所のPIN句がアクセント6であることを確認。
- 再生成: PINを含む5segのみ再生成（`--regen 7,39,40,45,66`）。他63segは既存音声を再利用。
- 字幕: `audio_timing.json`（実測）→ `captions_auto.srt/.ass` を再生成（68件を維持）。

## 3. 変更していないもの

- GPT画像5枚・narration原稿・subtitle文面・scene数・mapping・CTA・字幕スタイル・動画設定（1920×1080/30fps/H.264/AAC48kHz）。
- Episode 001〜005は未変更。

## 4. QA結果

- `phase2_qa`（draft_v2）: **PASS**（fail 0 / warn 0）。黒フレーム0・欠落0・長無音0・字幕安全幅0。
- readability確認フレーム: `work/draft_v2_review/readability_frames/`（7枚）。
- PIN試聴用WAV: `work/draft_v2_review/pin_pronunciation_review.wav`。詳細: `pin_pronunciation_report.md`。
