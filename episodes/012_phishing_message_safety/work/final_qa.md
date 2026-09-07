# Episode 012 final QA

確認日: 2026-09-06  
状態: `PASS / UPLOADED_SCHEDULED`

## Final video

| QA | 結果 | 記録 |
|---|---|---|
| draft v4 | PASS | `output/draft_v4.mp4`、585.400秒、47,642,598 bytes |
| final | PASS | `output/final.mp4`、585.400秒、47,642,598 bytes |
| copy-only | PASS | draft v4 / finalのSHA-256が一致。再エンコードなし |
| SHA-256 | PASS | `32933ED599E072DDF27FA7AF99756F4F78B15A3498DA0EA2071F44EC04660DD8` |
| video | PASS | H.264 / 1920×1080 / 30fps |
| audio | PASS | AAC / 48kHz / mono |
| decode | PASS | finalのデコードエラーなし |
| black frame | PASS | 0（0.5秒以上のblackdetect区間なし） |
| unexpected silence | PASS | 0 |
| av sync | PASS | audio_timing期待585.401秒、final実測585.400秒 |

`output/draft_v3.mp4` は保持し、SHA-256 `662804C23CD1FF6915CA65655671757A80118DD8E7EEC05F56627309EF9B1205` の旧版を変更していない。最初のv4 buildも `work/archive/draft_v4_first_build.mp4` に保持した。

## Audio override / pronunciation

- `segment030`「これ、本物？」は `audio/human_approved/030.wav` をsource of truthとして採用。
- human audio SHA-256: `7B534892A4AC893CC7F1D0D483B67A8A94E690353DB652EA16B0077C3F4C7106`。
- 人間修正版の実測は6.346667秒、timelineは213.189–219.536秒。
- v4 build log: `regenerated=[] reused=78 human_overrides=[30]`。自動再生成数は0。
- 優先順位は `human_audio_override > pronunciation dictionary > automatic VOICEVOX generation`。修正版はcleanup時にも保持する。
- e-Taxは `イ・イ・タ・ッ・ク・ス`、アクセントピークは「タ」、語中pause 0。v3監査に記録した音声SHAと一致し、v4で再生成していない。
- 本編は79 narration segment。`SCENE-031` と `segment080` はタイムラインに0件。
- pronunciation preflightは人間承認済みのv3実クエリ監査を継承してPASS。030はその後の人間音声overrideを採用し、辞書・自動生成で上書きしていない。

## Subtitle / visual

| QA | 結果 | 記録 |
|---|---|---|
| subtitle cue | PASS | 117 cue、実音声ベース |
| subtitle font | PASS | target 72px、minimum 56px |
| semantic linebreak | PASS | unnatural / word / conjugation / particle-orphan はすべて0 |
| layout | PASS | overflow 0、3-line 0 |
| TTS leakage | PASS | `tts_reading_leakage=0` |
| scene count | PASS | 30 scene、SCENE-031 timeline 0件 |
| contact sheet | PASS | `output/review/scene_contact_sheet_v4.png`、1,478,048 bytes、SHA-256 `224F5B78393D229F774D6D0ADD64222E1DC22CBC49EACAF7F552828C4B513F64` |
| visual regression | PASS | 公式素材・ImageGen・共通背景・字幕安全帯を維持 |
| privacy | PASS | 個人情報・実在アカウント情報・実在メッセージUIなし |
| official source integrity | PASS | 公式素材5点と公式引用・意味図解の対応を維持 |
| neutral frame remaining | PASS | 0 |
| oversized checkmark | PASS | 0 |
| meaningless filler icon | PASS | 0 |
| senior readability | PASS | draft_v3人間全編確認済み、v4変更は030音声のみ |

字幕正本は `captions.srt`。自動生成版 `work/captions_auto.srt` とSHA-256 `5CD32751C765CA269DE3BA789246BB3B344A0567C5C3ADD1C37B0E9F2560FBEC` が一致する。

## CTA / policy

- 中盤CTA: count `1`。終了CTAの重複: `0`。
- 終了CTAは1回。Episode011実使用postrollを画面・音声・canonical textで再利用した。
- Episode011実使用版との一致: `PASS`（content / visual / audio hash一致）。
- CTA content hash: `e20707f4cdf3a79dbd4bd4dc27be0d7c8159ed8693783881293c069be47cc08f`。
- CTA画面SHA-256: `96EFB5195CD7F3D7121472A79F300AF19999108186D6B35C370EFA488185EAE0`。
- CTA音声SHA-256: `1D21F765F5606310CA08BC0264EC6ED0136F68F5A7DA07318B5018F1735FDBC9`。
- 15秒（音声11.456秒＋末尾3.544秒）。右側40〜45%はEnd Screen予約領域。動画側に疑似subscribe UIはない。
- thumbnailはユーザー提供画像を正式採用。`assets/thumbnail/thumbnail_source.png`を保持し、`assets/thumbnail/thumbnail.png`へ内容変更なしで1280×720へ正規化。QA PASS、YouTube設定もAPI検証済み。
- YouTube video ID `CzTNLyAn1lY`を`privacyStatus=private`、`publishAt=2026-09-12T10:00:00Z`（2026-09-12 19:00 JST）で予約。End Screen設定のみYouTube Studioの人間作業として未実施。

## Fact / source gate

- Fact FAIL: 0
- Fact REVIEW: 3（公開前のlive page、事業者ごとの通知仕様、Apple Event後の公開順）
- Privacy FAIL: 0
- 主要事実の一次情報URLは `sources.md`、`description.md`、`publish.json` に保持。
- 公開直前に、国民生活センター、警察庁、フィッシング対策協議会、日本郵便、JCB、ソフトバンク、国税庁、消費者庁の各公式ページを再確認する。

最終成果物はcopy-onlyで確定し、サムネイル設定・予約公開・API検証まで完了。公開時刻までは`private`を維持し、End ScreenはYouTube Studioで人間が設定する。
