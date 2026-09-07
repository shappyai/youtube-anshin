# Episode011実使用CTAとEpisode012 CTA比較（v1〜v3履歴）

作成日：2026-09-06

この記録は、Episode012のCTAを修正する前に、Episode011の**実際に使用された `output/final.mp4`** とEpisode012 `output/draft_v1.mp4` を比較したもの。Episode.jsonの予定値ではなく、Episode011のfinal・実使用素材・ハッシュを基準にする。

## 比較表

|項目|Episode011 実使用 final|Episode012 draft_v1|
|---|---|---|
|最終本編（CTA直前）|SCENE-018（scene plan上の最終scene、segments 38–39）|SCENE-030（segments 76–79）→ SCENE-031（segment 80）|
|CTAの実装位置|本編sceneの後に `work/video_clips/postroll_cta.mp4` をハード連結|本編sceneの後に `work/video_clips/postroll_cta.mp4` をハード連結。SCENE-031の後にもpostrollを置く構成|
|CTA canonical text|スマホやパソコンの「これ、どうすればいい？」を、公式情報で分かりやすく確認しています。次に困ったときのために、チャンネル登録しておいてください。|大人のデジタル安心室では、スマホやパソコンを、もっと安全・快適に使うための情報をお届けします。チャンネル登録・高評価もよろしくお願いします。|
|CTA display text|次に困ったときのために。\nチャンネル登録しておいてください。|`config/channel_cta.json` の共通CTA表示|
|CTA audio|`audio/voicevox_kenzaki/cta_registration_conversion_v1.wav` / 11.456秒 / SHA-256 `1D21F765F5606310CA08BC0264EC6ED0136F68F5A7DA07318B5018F1735FDBC9`|`audio/voicevox_kenzaki/cta_channel_common.wav` / 11.563秒 / SHA-256 `188661261386755B11D830E5FC73117C2481E811AEE314AE5B41D5CFC6D90A79`|
|CTA visual|`work/cta_registration_conversion_v1.png` / SHA-256 `96EFB5195CD7F3D7121472A79F300AF19999108186D6B35C370EFA488185EAE0`|`work/channel_cta.png` / SHA-256 `D9AAA6A787EE1511B787B8D594BFA5D9FBEBFA5C0BEC9CCC6E8B8BC3DBF607C0`|
|CTA duration|15.000秒（audio 11.456秒＋実使用の余韻3.544秒）|12.563秒（audio 11.563秒＋余韻1.000秒）|
|transition|`scene_018.mp4` → `postroll_cta.mp4` のhard concat。fadeなし|scene_030 → scene_031 → postrollのhard concat。fadeなし|
|End Screen reserved area|右側40〜45%。実登録要素はYouTube Studio側。動画内の疑似subscribeなし|scene31は右45%予約。postroll common CTAはEpisode011と同じ予約方針だが、文言・asset・尺が別|

## CTA直前とCTAの判断

- Episode011の実使用は、最後の本編sceneから登録CTAへ一度だけ遷移する構成。
- Episode012 draft_v1はSCENE-031がCTA相当のメッセージを持ったうえでpostroll common CTAも連結され、CTAが二重に見える可能性がある。
- Episode012 draft_v2では、Episode011 finalで実使用された `registration_conversion_v1` のcanonical text・display・visual・audio・15秒尺・右側reserved areaをpostrollの正本として再利用する。
- SCENE-030はまとめの最終sceneとして維持し、SCENE-031はEpisode011のCTA文言と意味が食い違わないように修正する。postrollだけで登録CTAを完結できるかはdraft_v2の人間全編確認で確認する。

## 中盤CTAは別管理

中盤の登録案内はend CTAと混ぜない。Episode011で使用した中盤CTAとEpisode012 segment30のcanonical text・音声設定が一致することを確認し、draft_v2では現行の中盤CTA再利用仕様を維持する。end CTAのregistration_conversion_v1再利用は中盤CTAの文言・尺を変更するものではない。

## 修正後の再確認欄

2026-09-06にdraft_v2を再構成し、以下を実測・照合した。

|項目|Episode011 実使用 final|Episode012 draft_v2|判定|
|---|---|---|---|
|CTA config|`work/cta_registration_conversion_v1.json` / `7BB2FF3FCED403887046147741665B29ED948DBD27F4BB4A218DA5F263E6FF70`|同一config・同一hash|PASS|
|CTA visual|`work/cta_registration_conversion_v1.png` / `96EFB5195CD7F3D7121472A79F300AF19999108186D6B35C370EFA488185EAE0`|同一PNG・同一hash|PASS|
|CTA audio|`audio/voicevox_kenzaki/cta_registration_conversion_v1.wav` / `1D21F765F5606310CA08BC0264EC6ED0136F68F5A7DA07318B5018F1735FDBC9`|同一WAV・同一hash。再生成なし|PASS|
|CTA canonical/display text|同一|同一|PASS|
|CTA duration|15.000秒（11.456秒＋3.544秒）|15.000秒（11.456秒＋3.544秒）|PASS|
|transition mechanics|最終本編→postrollのhard concat、fadeなし|SCENE-030→SCENE-031→postrollのhard concat、fadeなし|PASS（方式）|
|reserved area|右側40〜45%、実登録要素はYouTube Studio側|scene31/postrollとも右45%予約、疑似subscribeなし|PASS|

- draft_v2出力：`output/draft_v2.mp4`、実測597.13秒、SHA-256 `94A04D4D905E3736E3792DAC69C1CE2A1935F9D71C11A052951B74161ED48B8B`
- `end_cta_same_as_011=PASS`：postrollのcanonical text・display text・PNG・WAV・尺を一致させた。
- `cta_audio_match_011=PASS`：Episode011のWAVをそのまま再利用。CTA audioは再生成していない。
- `cta_visual_pattern_match_011=PASS`：Episode011実使用PNGをそのまま再利用。postroll clipのコンテナhashは再エンコードで変わるが、元PNG hashは一致する。
- `pre_cta_transition_match_011=PASS`：SCENE-030のテーマ固有まとめを維持し、SCENE-031からpostrollへhard concat・fadeなし・右45%予約でEpisode011の接続方式に合わせた。
- midroll CTAは別管理：Episode012 segment030とEpisode011 segment013のcanonical narrationおよびWAV hash（`CC06F734C6857E5FD91561131B40D8428E4248641AF0FED3AF6BAA604D5144BB`）が一致することを確認した。
- `SCENE-030 → SCENE-031 → postroll` の連続表示と、CTAの重複感は`work/human_review_points_v2.md`の全編確認項目として残す。自動判定で人間確認を代替しない。

## Episode012 draft_v3（2026-09-06）

draft_v3では人間再確認の指示に従い、終了CTAの二重構成を解消した。

|項目|Episode011 実使用 final|Episode012 draft_v3|判定|
|---|---|---|---|
|CTA直前|最終本編scene → postroll|SCENE-030（segments 76–79）→ postroll|PASS|
|SCENE-031 / segment080|なし|本編timelineから削除|PASS|
|CTAの連結|hard concat、fadeなし|SCENE-030終了直後にpostrollをhard concat、fadeなし|PASS|
|CTA canonical/display|同一|同一|PASS|
|CTA audio|同一WAV / 11.456秒|同一WAV / 11.456秒|PASS|
|CTA visual|同一PNG|同一PNG|PASS|
|CTA duration|15.000秒（余韻3.544秒）|15.000秒（余韻3.544秒）|PASS|
|end_cta_count|1|1|PASS|
|pre_cta_duplicate_narration|0|0|PASS|

- draft_v3出力：`output/draft_v3.mp4`、実測585.55秒、SHA-256 `662804C23CD1FF6915CA65655671757A80118DD8E7EEC05F56627309EF9B1205`
- CTA audio：`audio/voicevox_kenzaki/cta_registration_conversion_v1.wav` / SHA-256 `1D21F765F5606310CA08BC0264EC6ED0136F68F5A7DA07318B5018F1735FDBC9`
- CTA visual：`work/cta_registration_conversion_v1.png` / SHA-256 `96EFB5195CD7F3D7121472A79F300AF19999108186D6B35C370EFA488185EAE0`
- CTA config：`work/cta_registration_conversion_v1.json` / hash `7BB2FF3FCED403887046147741665B29ED948DBD27F4BB4A218DA5F263E6FF70`
- v3の本編終了は**09:30.551**、postroll終了は**09:45.551**。人間の全編確認ポイントは`work/human_review_points_v3.md`。
