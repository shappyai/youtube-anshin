# Episode 010 Visual Gate v2

確認日：2026-09-05

## 判定

- Gate：APPROVED（2026-09-05、ユーザーによる人間承認）
- Phase：A Gate承認済み → B完了 → C final確定（thumbnail待ち）
- 冒頭30秒短縮：PASS（registration_conversion_v1反映後、VOICEVOX実測で最初の実操作28.516秒）
- Fact FAIL：0
- Fact REVIEW：2
- Privacy FAIL：0
- Scene renderer：20/20 PASS
- Scene quality：FAIL 0 / WARN 3
- ImageGen native text QA：自動FAIL 0。draft_v2全編視聴で人間承認済み。

## Intro QA

- 旧intro：segment 001–012、12 segment、486文字。
- 実験前intro core：segment 001–005、5 segment、130文字。
- registration_conversion_v1反映後intro core：segment 001–005、5 segment、129文字。
- 反映後intro（1 / 6への接続を含む）：segment 001–006、6 segment、146文字。
- 1 / 6開始：SCENE-004 / segment 006、実測25.347秒。
- 最初の実操作：SCENE-005 / segment 007。
- intro_before_first_action_seconds：28.516秒（VOICEVOX実測）。
- intro_core_only：PASS。
- 冒頭に残した内容：初めて使う人向け、利用登録の対象、最低限の準備、実物カードの数字4桁。
- 冒頭から外した内容：制度背景、旧アプリ刷新、既存利用者の更新、詳細OS/NFC条件、本人認証3ルート。

## Scene再編

- SCENE-001〜003を問題・短い全体像・準備物に限定した。
- SCENE-004で直ちに1 / 6へ入り、SCENE-005でアプリを開く最初の実操作を開始する。
- アプリ本体のiOS 16.4以上、Android 11以上、NFCはSCENE-012へ移動した。
- 本人認証3ルートはSCENE-013へ移動し、実物カード・iPhone・Androidを別選択肢として表示する。
- スマホ内カードの条件はSCENE-012とSCENE-018付近に残した。
- 旧アプリ刷新と既存利用者の更新に関する2文は、Episode 002との重複のため台本のナレーションから削除した。調査記録とFact Checkは保持する。
- total scene：20。新規ImageGen生成：0。承認済みImageGen 3枚を再利用し、再採番に合わせてtemplate・official renderを更新した。OS/NFC表記変更に伴いSCENE-012のみ再レンダーした。今回の実験ではSCENE-001を含むscene画像を変更していない。

## Official UI review

対象はSCENE-007、009、011、015、016、018の6 scene。公式原画は変更せず、6件のfocus cropを使用した。

- SCENE-015：数字4桁の入力欄と画面見出しを1920x1080 renderで確認。暗証番号そのものは表示しない。
- SCENE-016：カード読み取りの見出しと読み取り案内を1920x1080 renderで確認。機種ごとの位置差は一律に断定しない。
- SCENE-018：生体認証の見出しと案内を1920x1080 renderで確認。iPhoneとAndroidを同じ登録手順として扱わない。
- 3 sceneとも公式UIの改変はなく、65歳以上のTV視聴を想定したfocus cropで配置した。最終的な視認性は人間Gateで確認する。

## Fact REVIEWの解消条件

| ID | Phase Aで残る点 | Fact FAILを0にする確認 |
|---|---|---|
| FC-015 | NFCの読み取り位置は機種ごとに異なる | 採用する実機とカードで読み取り位置を確認し、機種名と説明を一致させる。 |
| FC-019 | 現行画面の文言・ボタン名・順番は更新され得る | 撮影直前にデジタル庁公式ページと実機を照合し、SCENE-007、009、011、015、016、018の文言を記録する。 |
| FC-020 | Androidの機能名称・対応機種は更新され得る | 撮影直前にAndroid公式案内と採用端末を照合し、現行表記と対応機種だけを説明する。 |

Fact REVIEWは実機・撮影直前確認が必要なため、Phase Aでは解消しない。Fact FAILは0を維持する。

## Deliverables

- episode.json：v2 scene order、registration_conversion_v1、41 narration segment、44 subtitle cue、intro_qaを反映。
- script.md：冒頭30秒v2、ミニストーリー、解決表現、専用postroll CTAを反映。
- scene_plan.json：20 sceneのv2 visual planと実験QAを反映。
- scene_contact_sheet_v2.png：20 scene一覧。
- intro_v1_v2_comparison.png：冒頭5 sceneのv1/v2比較。
- scene_quality_report_v2.md：機械QA。
- privacy_qa_v2.md：Privacy QA。
- pronunciation_preflight_v3.md：VOICEVOX Engine PASS、REVIEW 0。
- pronunciation_preflight_v4.md：segment 038更新後もVOICEVOX Engine PASS、REVIEW 0。
- subtitle_preflight_v3.md：44 cue、72px、FAIL/WARN 0。
- subtitle_preflight_v4.md：segment 038更新後も44 cue、72px、FAIL/WARN 0。
- cta_registration_conversion_v1_preflight.md：専用CTA、60px、clipping 0、PASS。
- draft_v1_qa.md：20 scene、44 cue、FAIL/WARN 0。
- draft_v2_qa.md：20 scene、44 cue、FAIL/WARN 0。
- qa_frames_draft_v2/contact_sheet.png：v2代表フレーム21枚。

## Post-approval experiment

Visual Gate v2承認後の台詞・postroll差分として、Episode 010だけに`registration_conversion_v1`を追加した。Visual Gate v2の20scene、公式UI、SCENE-001画像、タイトル、サムネイルは変更していない。

- `story_intro=true`：冒頭を「入れて、開いてみた。でも、最初に何をすればいい？」へ変更。
- `reason_to_return_cta=true`：専用CTAのcanonical narrationは「スマホやパソコンの『これ、どうすればいい？』を、公式情報で分かりやすく確認しています。次に困ったときのために、チャンネル登録しておいてください。」。
- `midroll_subscribe_cta=false`：中盤CTAは追加していない。
- first_action：28.516秒、micro_story_intro：PASS、problem_to_solution_clear：PASS。
- CTA音声：11.456秒。15秒postroll内に3.544秒の余韻を置き、表示文のclippingは0。
- 登録転換率：`subscribers_gained / unique_viewers`。1,000人あたりは正式値×1000。`registered / not subscribed`比率は別指標。
- 詳細な取得項目・比較対象・スナップショットは`work/analytics_plan.md`に記録した。

## Draft v2 human correction

- 3:03付近の旧文言「困ったときは、エピソード007の確認動画へ進んでください。」を「読み取れない、ログインできないときは、関連動画で確認してください。」へ変更した。
- viewer-facing表示は「ログインできないときは／関連動画で確認」へ変更し、SCENE-019も再レンダーした。関連動画への内部ルーティング情報は制作管理側に残し、視聴者向け文字列からEpisode番号を除いた。
- CTAの「次に困ったときのために」は説明ボックスを110px下げた。登録文言との意味ブロック、bottom 180px subtitle safe area、右側End Screen reserved領域、60px文字、clipping 0を維持した。
- latest fix QA：internal_episode_number_visible=0、internal_episode_number_spoken=0、related_video_wording=PASS、subtitle_sync=PASS、cta_visual_balance=PASS、cta_clipping=0、end_screen_reserved=PASS、subtitle_safe_area=PASS、draft_v1_regression=0。
- `internal_episode_id_not_viewer_facing`はproposed ruleとして記録し、canonical化は人間判断待ちとする。

## Final approval and STOP

- 2026-09-06、ユーザーが draft_v2.mp4 を全編視聴しAPPROVED。senior_readability=PASS。
- output/final.mp4 はdraft_v2からcopy-onlyで確定し、Final QAはPASS。SHA-256一致、再エンコードなし。
- thumbnailは未生成・未受領。YouTube upload、予約公開、public化は未実施。
- Fact FAILは0。FC-019 / FC-020は更新・実機依存のREVIEWとして残し、動画内表現は断定しない。

thumbnail受領後の人間確認まで停止する。

## Publication result

- 2026-09-06、ユーザー指定のChatGPT生成サムネイルを受領し、公開用1280×720画像を選択。文字・人物・UI・構図は変更していない。
- thumbnail QAはPASS。YouTube thumbnail設定もPASS。
- `output/final.mp4`を1回だけuploadし、video ID `rU5jlU7eq3I`を取得。再uploadは行っていない。
- channel guardは`UCgVRceTJYO5KOrPX4w2jXZw` / `大人のデジタル安心室`でPASS。
- privacyは`private`、publishAtは`2026-09-06T10:00:00Z`（2026-09-06 19:00 JST）。title、madeForKids=false、synthetic media=trueをAPI検証した。
- End Screenの関連動画・チャンネル登録要素はYouTube Studioで人間が設定する。動画側の右40〜45% reservedは維持する。
