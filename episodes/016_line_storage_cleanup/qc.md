# Episode 016 Phase B QC

基準日: 2026-09-08  
状態: draft_auto_v5生成済み、Human Gate 2待ち

## Human提供画面

- `assets/normalized/human_talk_settings.png`: 原本「トーク.jpg」。設定画面の正規化copy。
- `assets/normalized/human_data_deletion.png`: 原本「データの削除.jpg」。容量内訳の正規化copy。
- `assets/normalized/human_talk_list_masked.png`: 原本「トーク毎に削除.jpg」。表示名部分がマスクされた正規化copy。
- viewer-facing用crop: `human_talk_settings_deletion_focus.png`、`human_data_deletion_cache_focus.png`、`human_data_deletion_talk_entry_focus.png`、`human_talk_list_masked_landscape.png`
- 画面確認: 本人名、友だち名、グループ名、実トーク、写真、電話番号、メールアドレス、QRコード、通知内容は判読できない。
- メタデータ: 正規化copyのEXIFは0件。原本は変更せず保持する。
- 個人情報QA: PASS（3枚ともHuman目視確認、マスク済みの容量表示のみ使用）。

## 安全境界

- Android EmulatorへのLINEアカウント作成・ログイン: 未実施
- 本番LINEでの追加操作: 未実施
- キャッシュを含む削除操作: 未実施
- 削除ボタン: 押していない
- `トーク毎に削除.jpg` はHuman指示により、マスク済みの容量順実画面として使用する。
- AIでLINE UIを再現した画像: 使用しない

## 現行UIで確認した項目

- 「トーク」画面の「データの削除」入口
- 「データの削除」画面の「キャッシュ 369.7MB」
- 「トークごとにデータを削除」入口
- マスク済みトーク一覧の容量表示（102.3MB、24.2MB、1.6MB）

## 自動QA

- sources / 公式URL: Phase A PASS。確認日はsources.mdに記録。
- JSON / scene参照: production preflight PASS。公式素材6件、subtitles 44 cue。
- VOICEVOX発音: PASS（剣崎雌雄・ノーマル、approved 28、review 0、queries 44/44）。`キャッシュ`は3モーラ（キャ・ッ・シュ）、最終モーラ「シュ」をアクセント核とする標準辞書登録を適用した。
- pitch shape QA: PASS（`キャッシュ` 12出現、対象セグメント005、010、018、019、020、021、022、024、025、040、042）。詳細は`work/voicevox_pitch_qa_v5.md`。
- subtitles: PASS（VOICEVOX実測音声を基準に実時間化、fail 0、warn 0）。
- viewer-facing internal brand promise: 0を維持。viewer-facing text QA PASS。
- scene: 公式UIはHuman提供実画面、説明カードはrenderer-native。AIによるLINE UI再現なし。
- CTA: `channel_common_cta`へ更新し、CTA preflight PASS。新音声11.456秒 + 余韻1秒。
- draft: `output/draft_auto_v5.mp4`、1920×1080、映像30fps、音声AAC、実尺280.2秒。phase2 QA PASS。v4は保持。
- scene quality report: 公式画面が白面中心でgradient背景との差分比較ができないため、SCENE-004〜007、009、010は`background comparison unavailable`の機械FAIL。代表フレームの目視確認では、公式画面の見切れ・字幕帯侵入・制作側ラベル残存なし。

## Human Gate 2修正結果

- 0:25付近のSCENE-002を、3項目が主役のrenderer-native一覧へ差し替えた。表示は「容量の内訳」「キャッシュ」「容量の大きいトーク」。
- 「今日見る3か所」は見出しであり、項目1ではない。追加の説明文・アイコンは置いていない。
- `キャッシュ`の出現は12回、影響セグメントは11本。005、010、018、019、020、021、022、024、025、040、042を再生成した。その他33本は再利用した。
- `config/voicevox_pronunciation.yaml`に重複のないglobal登録を追加し、`accent_phrases`のaccent 3、`pitch_shape: low_high_plateau`、`pitch_high_anchor_mora: 3`を適用した。`ッ`は無声モーラのため、聴感上の山は最終の「シュ」に置かれる。
- draft SHA-256: `C1D7B6DA8039DEC668FB9EAB8FAA8E51354D43246AA3B4D33E2750B3D2EECF28`
- thumbnail生成、finalize、YouTube upload/publish、実データ削除は未実施。

## Human Gate 2確認項目

1. 3枚の実画面に個人情報が残っていないか。
2. マスク済み一覧の容量表示だけを使い、名前や会話を読ませていないか。
3. 「キャッシュを消してもトーク履歴そのものは消えない」と「古い写真や動画などが見られなくなる場合」を両立して説明できているか。
4. 実際に削除操作をしていないこと。
5. VOICEVOXの読み、字幕の同期、実画面の可読性、full draftの切り替え。
6. タイトルと概要欄が内容以上に断定していないか。
