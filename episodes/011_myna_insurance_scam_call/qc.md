# Episode 011 QC

更新日：2026-09-06

## Status

`READY_FOR_HUMAN_REVIEW`

Phase Bのdraft_v2、字幕、VOICEVOX音声、CTA、機械QAは完了。人間によるdraft_v2全編視聴後にfinal化する。thumbnail、final、YouTube upload、scheduleは未着手。

## Fact / Privacy / Policy

- Fact FAIL：0
- Fact REVIEW：0
- Privacy FAIL：0
- Template leakage：0
- fake subscribe UI：0
- 主要事実：厚生労働省・デジタル庁・警察庁の一次情報URLを`sources.md`と説明欄に保持
- SCENE-003：MHLW公式の核心メッセージを大きく表示。公式UIのAI再現なし
- SCENE-018：背景・人物・主文・補助文を1枚のImageGen-native画像へ一体化。指定文言の文字QA PASS、後付け文字レイヤー0
- viewer-facing brand promise：`怖がらせる前に、確認する。` の表示・ナレーション・字幕・CTA・概要欄・チャプター・現行scene画像への残存0。内部metadataのブランド定義は保持

## Visual

- Visual Gate：`APPROVED_WITH_2_FIXES`
- scene quality：19 OK / WARN 0 / FAIL 0
- SCENE-003：可読性修正済み
- 代表フレーム：20枚。`work/visual_review/draft_v2_contact_sheet.png`
- 字幕安全帯：PASS
- Subtitle preflight：FAIL 0 / WARN 8。WARNは文字サイズを下げずにcue分割した後のバランス確認項目で、全編視聴時に人間確認する

## Audio / subtitles

- VOICEVOX：剣崎雌雄 / ノーマル
- narration：39 segment、連結236.795秒。segment 039のみ再生成、他38件を再利用
- pronunciation preflight：PASS、REVIEW 0
- phone number QA：PASS（表示・字幕・機械読み確認。人間聴取待ち）
- captions：39 cue、`captions.srt` / `captions.ass`
- TTS reading leakage：0
- 目標字幕サイズ：72px、最小56px未満なし

## CTA

- 中盤CTA：1回、68.822〜75.518秒、音声6.496秒、上限7秒をPASS
- 終了CTA：Episode010 draft_v1実使用のregistration_conversion_v1を完全再利用。canonical text・画面・音声照合PASS
- 終了CTA音声：11.456秒、CTA枠15秒、余白3.544秒
- CTA preflight：PASS。本文欠落・clipping・fake subscribe UIなし

## Draft artifact

- Path：`output/draft_v2.mp4`
- Duration：probe 251.800秒（期待251.795秒）
- Video：H.264 / 1920×1080 / 30fps
- Audio：AAC / 48kHz / mono
- SHA256：`45AB01EC1FF4F807FFF4ED7F42436FAFD2D00A24FD087BAA7436AF371C78AAB4`
- draft QA：PASS。decode・black frame・unexpected silence・仕様不一致のFAILなし

## Human Gate

人間はdraft_v2を全編視聴し、冒頭の安全行動、SCENE-003の公式核心、SCENE-018のImageGen-native文字、電話番号・略語の発音、字幕の同期と読みやすさ、中盤CTA、Episode010と同一の終了CTA、AI disclosure要否を確認する。
