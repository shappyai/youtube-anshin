# VOICEVOX 発音レビュー標準

Phase 2は、文脈依存の誤読を共通辞書へ広げない。標準ナレーターはVOICEVOX:剣崎雌雄、normal、speed 1.00、intonation 1.00、pitch 0.00とする。

## 手順

1. segmentごとに`/audio_query`を取得する。
2. `config/voicevox_pronunciation.yaml`の人間承認済み辞書と比較する。
3. suspiciousな語だけをREVIEWとして`work/human_review.json`に出す。
4. 人間が文脈内の音声を確認し、読みを承認する。
5. 読み仮名だけの修正は該当segmentの`reading_overrides`に記録する。アクセントだけを文脈限定で直す場合は、`accent_overrides`に`surface`・`reading`・`accent`を記録する（global辞書へ昇格しない）。
6. 変更segmentだけVOICEVOXを再生成し、他はhash cacheを再利用する。

AIの推測だけで共通辞書を追加しない。特に次は文脈依存のため、グローバル登録禁止とする。

- `方`: 「驚いた方」「考え方」「探し方」は`かた`、「一方で」は`いっぽうで`
- `今`: Episode 003の「今ブラウン」は該当segmentだけ`いまブラウン`。単独の「今」は登録しない

音声用テキストと画面表示は別の正本として扱う。`narration`または`spoken_text`をVOICEVOXへ渡し、公式表記が必要な場合はsegmentの`display_text`と`subtitles.text_lines`へ表示文字列を置く。TTS用の読み仮名を字幕へコピーしない。字幕側は`tts_reading_leakage`で検査する。

## 人間承認済み App Store

| 表記 | 読み | アクセント句 | モーラ | accent | 下降位置 |
|---|---|---:|---:|---:|---|
| `App Store` | `アップストア` | 1 | 6 | 5 | 「ト」の後 |

この1件は`config/voicevox_pronunciation.yaml`に重複なく登録済みで、今後のpreflightでは自動PASS対象とする。辞書ファイルはpreflightが自動変更しない。

## 人間承認済みの音高形状

辞書の`accent`だけでは、VOICEVOXの`/mora_data`再計算時に後半が下降することがある。添付VOICEVOX画面などで人間が手動調整した場合は、辞書エントリに`pitch_shape: low_high_plateau`、`pitch_high_anchor_mora: 2`、`pitch_low_delta`、`pitch_equalize_following_same_mora: true`を記録する。

- 最初のmoraを低くし、2mora目で上げ、2mora目以降は高い位置を完全に維持する。
- `信用`は`シンヨオ`を対象とし、`信用を`のように後続の`オ`が連続する場合は同じ高さにそろえ、O-Oのpitch差を0にする。
- 適用は`/mora_data`後・synthesis前に行う。pitch shapeのQAは`first_mora_low`、`second_mora_rise`、`later_mora_plateau`、`consecutive_same_mora_pitch_delta`、総合`approved_pitch_shape_match`で記録する。
- 文脈ごとにaudio_queryを確認し、該当segmentだけ再生成する。古いaccent-only設定と競合する重複entryは残さない。

## 3文字英字略語の音読ポリシー（2026-09-04・Episode 007 draft_v1レビューで確定）

- 対象: ASCII大文字3文字で日本語ナレーション上「英字を1文字ずつ読む略語（initialism）」（NFC / PIN / API / URL 等）。
- 読み方: **1文字目だけにアクセントピークを置かない**。2文字目以降にイントネーションの山を持たせ、3文字を平板に機械読みしない。
- 実装: text_replacement（カナ表記へ）＋ accent_phrases（accent 指定）の2段で保証する（英字3文字はエンジンが text を持たない phrase として解析し accent 指定が効かないことがあるため）。
- 人間承認済み: NFC → エヌエフシー（accent 3・尾高）・PIN → ピーアイエヌ（accent 6・尾高・Episode 006 approved を 007 へ scope 拡張して再利用）。
- 運用: 新規3文字略語は初回 audio_query で REVIEW とし、approved 済みは辞書再利用。global 辞書への自動登録・重複登録はしない。QA: `three_letter_acronym_accent`（[A-Z]{3} 検出→ approved あり=use / なし=REVIEW）。
