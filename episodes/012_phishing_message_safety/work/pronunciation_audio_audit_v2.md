# Episode012 pronunciation audio audit v2

確認日：2026-09-06  
対象：Episode012全 narration segment の対象語出現箇所  
VOICEVOX：剣崎雌雄／ノーマル  
判定：PASS

`audio_query`へ辞書・segment overrideを適用した実クエリを再確認した。表示字幕は漢字・英字表記を維持し、読み仮名を字幕へ流出させていない。

|語|全出現segment|実クエリ確認|判定|
|---|---|---|---|
|普段|010, 012|フダン、accent=1（ふ）|PASS|
|何も|017|ナニモ、accent=2（に）|PASS|
|届け物|029|text replacement後のトドケモノ|PASS|
|本物|002, 003, 008, 014, 030, 066, 079|text replacement後のホンモノ。長音なし|PASS|
|カード会社|034, 038, 039, 071|カアドガイシャ、全4出現でaccent=3（ド）|PASS|
|e-Tax|056|イータックス。VOICEVOX mora列ではイ／イ／タ／ッ／ク／スだが、1つのaccent phrase内でinternal pause=0|PASS|

## 再生成・再利用

- `カード会社`のSCENE-034／038／039／071に対応する音声を、複合mora照合修正後に再生成した。
- `普段`／`何も`／`届け物`／`本物`／`e-Tax`は辞書適用済み音声を全出現で確認した。
- 既存承認語（SMS、ID、URL、JCB、Android、iPhone、188、#9110等）はVOICEVOX preflightで回帰なし。
- CTA音声はEpisode011実使用WAVを再利用し、発音対象音声の再生成対象には含めていない。

詳細な実クエリ・WAV hashは `pronunciation_audio_audit_v2.json` に保存した。人間の聴取範囲は `human_review_points_v2.md` に記載する。
