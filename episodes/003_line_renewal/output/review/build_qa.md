# Episode 003 draft build QA

確認日: 2026-08-31  
対象: `draft_auto_v1.mp4`。final化・thumbnail・YouTube操作は未実施。

## Build

| Check | Result | Detail |
|---|---|---|
| Phase A integrated gate | PASS | episode schema / sources / subtitles / pronunciation / scenes / scene modes / official assets / GPT images |
| pronunciation review | PASS | remaining review=0。human_review.jsonの4件を反映 |
| VOICEVOX | PASS | 剣崎雌雄 / ノーマル / speed 1.00 / intonation 1.00 / pitch 0.00 |
| narration segments | PASS | 52 / 52 WAV |
| audio cache | PASS | regenerated 0 / reused 52 |
| seg_002 reading | PASS | `reading_overrides` は `方→かた`。build hashがeffective textと一致し、query kanaにも `カタ` を確認 |
| subtitles | PASS | episode.jsonの52cueを使用。文字数による再分割なし |
| scenes | PASS | 18 / 18。gpt_image 8 / template 3 / official 7 |

## Video QA

| Check | Result | Detail |
|---|---|---|
| output | PASS | `draft_auto_v1.mp4` |
| duration | PASS | 290.800 sec。audio_timing 290.865 secとの差 0.065 sec |
| video stream | PASS | H.264 / 1920×1080 / 30 fps / 8,724 frames |
| audio stream | PASS | AAC / 48,000 Hz / mono |
| black frame | PASS | 0件（blackdetect） |
| missing frame | PASS | 期待フレーム数と一致。decode errorなし |
| duplicate scene anomaly | PASS | rendered sceneの完全一致hashなし |
| official focus scenes | PASS | SCENE-004 / 005 / 006 / 008 / 009 / 011 / 012を18scene renderに含む |

## Audio QA

| Check | Result | Detail |
|---|---|---|
| missing audio | PASS | 0件 |
| abnormal silence | PASS | narration WAVで2秒以上の無音なし |
| clipping | PASS | 52 WAVでPCM clippingなし。draft max_volume=-2.0 dB |

## Subtitle / asset QA

| Check | Result | Detail |
|---|---|---|
| subtitle cue count | PASS | 52 / 52 |
| one-character cue | PASS | 0件 |
| subtitle overflow | PASS | 0件 |
| subtitle safe area | PASS | 下部180px帯。ASS 72px / Yu Gothic Bold / 白文字 / 黒outline |
| unresolved placeholder | PASS | 0件 |
| official asset missing | PASS | 0件 |
| GPT image assets | PASS | 8 / 8。PNG / 1920×1080 / 破損なし |
| GPT image fallback | PASS | gpt_image sceneをtemplateへfallbackしていない |

## WARN / FAIL

- WARN: なし
- FAIL: なし
- 人間確認: draftを最後まで視聴し、テンポ、sceneの単調さ、公式画面の実動画での可読性、AI画像の表示時間を確認する。
- seg_002の音声は機械確認済みだが、最終的な自然さは人間の試聴で確認する。

