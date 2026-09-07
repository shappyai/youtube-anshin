# Episode 011 draft_v2 change log

更新日：2026-09-06

## Human review fixes

1. SCENE-018を、背景・人物・文字を一体生成したImageGen-nativeの1枚へ変更した。
   - 主文：`迷ったら、` / `その場で決めない`
   - 補助文：`いったん止まって、` / `公式から確認`
   - 指定文言のexact text QA：PASS
   - ImageGen生成：2回（retry 1）
   - PIL・ffmpeg drawtext・別文字layerによる後付け文字：0
   - pil_overlay fallback：0
   - 余計な読み取り可能文字：0（目視）
   - 右側40〜45%のEnd Screen reserved領域と下部180pxの字幕安全帯を確保

2. 視聴者向けに表示していた `怖がらせる前に、確認する。` を削除した。
   - segment 039 narrationから削除
   - SUB-039から削除
   - 現行のscene画像、CTA、概要欄、チャプターから削除
   - 内部metadataのブランド定義、AGENTS.md、docs、researchは保持
   - viewer-facing brand promise scan：0 / PASS

## Scope lock

冒頭の安全行動、厚生労働省の公式結論、3つの確認、中盤CTA 1回（6.496秒）、登録者獲得実験 v2、Episode010実使用の終了CTA、電話番号、SCENE-003、全19scene構成は維持した。

## Regenerated / reused

- 音声：segment 039のみ再生成、他38 segmentを再利用。main narrationは236.795秒。
- scene asset：SCENE-018のみ差し替え、他18 sceneを再利用。
- 終了CTA：Episode010の画面・音声・canonical textを継続再利用。

## Output

- `output/draft_v2.mp4`
- probe：251.800秒（期待251.795秒）
- SHA256：`45AB01EC1FF4F807FFF4ED7F42436FAFD2D00A24FD087BAA7436AF371C78AAB4`
- 機械QA：PASS
- 人間ゲート：全編視聴待ち
