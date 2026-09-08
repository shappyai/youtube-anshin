# Episode015 STATE

## 現在地

- Episode: 015_google_2fa_check
- 更新日: 2026-09-08
- status: FULL_DRAFT_V3_COMPLETE_WAITING_HUMAN_GATE_2
- phase: Phase B（現行UI確認・音声・字幕・scene・full draft）
- 次の停止点: Human Gate 2（draft_auto_v3・実Google UI入口の可読性・個人情報混入の最終確認）

## 今回の結論

2段階認証を設定済みの人向けに、次の3項目へ絞った。

1. 2段階認証で現在使う確認方法
2. バックアップ コード
3. 登録済みのパスキーとセキュリティ キー

Episode001の「セキュリティ チェックアップ」「再設定用の電話番号・メールアドレス」「2段階認証」「ログイン中の端末」「Googleと接続したアプリ」という広い5項目を、そのまま繰り返さない。Episode015では、Episode001内の2段階認証・パスキーの説明を、現在使える確認方法、予備の入口、別のログイン手段の登録状態という3点へ深掘りする。再設定用連絡先、端末一覧、接続アプリ、セキュリティ チェックアップは本編の確認対象から外した。

## 公式情報

- 公式情報の確認日: 2026-09-08
- 主な根拠: Googleアカウント ヘルプ
- selected sources: SRC-001〜SRC-007
- 補足・重複確認: SRC-008〜SRC-011
- 2段階認証をオフにする提案はしていない。
- 「2段階認証を設定していても危険」「乗っ取られる」などの根拠のない断定は採用していない。

## Phase B成果物

- narration segments: 42（旧SEG-015〜017を圧縮、旧SEG-044を削除）
- subtitles: 61（発話実時間に合わせて分割）
- scenes: 12
- official UI entry captures: 3（SRC-001 / SRC-003 / SRC-004。Scene 004・007・010）
- AI-generated visual assets: 0
- main narration duration: 306.180秒（5分06.180秒）
- full draft duration: 318.740秒（5分18.740秒、共通CTA音声11.563秒と余韻を含む）
- VOICEVOX: 剣崎雌雄 / ノーマル / 42セグメント生成済み
- full draft: `output/draft_auto_v3.mp4`（共通CTA音声を含む。v2は比較用に保持）
- full draft SHA-256: `B42AAFCD4773BA727B50465AE24CD326F65DF8EBC9ECE1EFF65C4E47D47D923C`
- Phase 2 QA: v3再実行済み（`work/phase2_qa.md`、PASS / FAIL 0 / WARN 0）。
- scene quality report: v3再実行済み（`work/scene_quality_report_v3.md`、9 OK / 0 WARN / 3 FAIL）。3件はgradient背景の差分比較ができない既知の機械判定で、実画面入口のprivacy/readabilityは別レポートと目視で確認する。
- contact sheet: `work/draft_contact_sheet_v3.png`、`output/review/draft_contact_sheet_v3.png`

## Phase Bの確認結果と未実施

- Google公式ヘルプの現行表示で、導線・正式UI名称を確認した。
- Humanログイン済みPCブラウザで、実Google UIの入口だけをcaptureした。Scene 004はセキュリティ設定の導線、Scene 007はバックアップ コード入口、Scene 010はパスキー入口。後段の個人情報・秘密情報は既存カードで説明する。
- バックアップ コードは入口・存在確認のみ。実コードの数字は撮影・保存・字幕化していない。新規作成・更新もしていない。
- captions.srtの実時間確定、動画render、full draft生成は完了した。
- サムネイル生成
- YouTube upload / publish
- グローバルSTATE.mdの変更

## Human Gateで確認する点

1. full draftの冒頭30秒以内に、対象・3項目・「今日は3か所だけ」が伝わるか。
2. draft_auto_v3のScene 004・007・010で、実Google UIの入口が65歳以上でも読めるか。表示される時刻などを含め、視聴に不要な情報がないか確認する。
3. テストアカウントで「現在の確認方法」に表示される項目と、実際に使える方法の一致。
4. バックアップ コードの入口・存在確認だけで成立しているか。コードの数字がどの素材にも出ていないか。
5. パスキー一覧の端末が本人所有か、現在も使っているか。削除・追加を急がない説明になっているか。
6. Scene 007にバックアップコード本体がなく、Scene 010に端末名などがないことを含め、PC表示のcropと字幕が65歳以上でも読みやすいか。4〜6分の情報量で水増しがないか。
7. VOICEVOXの「Google」「2段階認証プロセス」「バックアップ コード」「パスキー」などの発音を人間が試聴確認する。

## CTA

既存のchannel_common_ctaをcopy-onlyで使用する予定。追加案「次回はログイン中の端末も確認する」は候補として記録しただけで、現時点ではcanonicalなナレーション・概要欄に採用していない。
