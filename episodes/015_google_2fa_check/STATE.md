# Episode015 STATE

## 現在地

- Episode: 015_google_2fa_check
- 更新日: 2026-09-08
- status: finalized
- human_approved: true
- phase: Final candidate（Human Gate 2 APPROVED / copy-only finalized）
- 次の停止点: thumbnail完成後のpublish preflightと、YouTube StudioでのEnd Screen設定。upload／schedule／publishは未実施。

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
- main narration duration: 300.356秒（5分00.356秒）
- full draft duration: 313.356秒（5分13.356秒、QA基準timeline。final container probeは312.918秒）
- VOICEVOX: 剣崎雌雄 / ノーマル / 42セグメント生成済み
- approved draft: `output/draft_auto_v4.mp4`（共通CTA音声を含む。旧draftは比較用に保持）
- final: `output/final.mp4`
- finalization method: copy-only; no re-encode
- full draft SHA-256: `7AB436A319D66CC7EF27BA9A936CC6AC15AC0A725EBEFA7818AFC2C7131EDB5D`
- final SHA-256: `7AB436A319D66CC7EF27BA9A936CC6AC15AC0A725EBEFA7818AFC2C7131EDB5D`（draft_auto_v4と一致）
- final QA: `output/review/final_qa.md`、PASS / FAIL 0 / WARN 0。SHA一致、decode error 0、black frame 0、音声clipping 0。
- Final production preflight: PASS（sources、scenes、official assets、subtitles、pronunciation、viewer-facing INTERNAL_ONLY）。
- Publish preflight dry-run: PASS（final／Human approval／final QA／metadata、privacy=PRIVATE）。OAuth/APIは未呼出し。
- Phase 2 QA: v4再実行済み（`work/phase2_qa.md`、PASS / FAIL 0 / WARN 0）。
- scene quality report: v4再実行済み（`work/scene_quality_report_v4.md`、9 OK / 0 WARN / 3 FAIL）。3件はgradient背景の差分比較ができない既知の機械判定で、実画面入口のprivacy/readabilityは別レポートと目視で確認する。
- contact sheet: `output/review/draft_contact_sheet_v4.png`
- 音声・字幕修正v4: section番号、`セキュリティー`、文脈限定の「なにで」、compound語の連続読みを反映。`work/audio_subtitle_revision_v4.md`で確認済み。
- Human Gate 2: APPROVED（映像・音声・字幕）。

## Phase Bの確認結果と未実施

- Google公式ヘルプの現行表示で、導線・正式UI名称を確認した。
- Humanログイン済みPCブラウザで、実Google UIの入口だけをcaptureした。Scene 004はセキュリティ設定の導線、Scene 007はバックアップ コード入口、Scene 010はパスキー入口。後段の個人情報・秘密情報は既存カードで説明する。
- バックアップ コードは入口・存在確認のみ。実コードの数字は撮影・保存・字幕化していない。新規作成・更新もしていない。
- captions.srtの実時間確定、動画render、full draft生成、copy-only finalize、final QAは完了した。
- サムネイル生成（ChatGPT側）
- YouTube upload / schedule / publish
- YouTube StudioのEnd Screen設定
- グローバルSTATE.mdの変更

## Human Gate 2承認後の公開前確認

1. thumbnailをChatGPT側で作成し、指定パスへ配置する。
2. YouTube StudioでEnd Screenを人間設定する。動画内に疑似登録UIはない。
3. thumbnail配置後にpublish preflightを再実行する。upload／schedule／publishは別途人間確認後に行う。
4. YouTube AI開示（contains_synthetic_media）の最終判断をupload前に人間確認する。

## CTA

既存のchannel_common_ctaをcopy-onlyで使用する予定。追加案「次回はログイン中の端末も確認する」は候補として記録しただけで、現時点ではcanonicalなナレーション・概要欄に採用していない。
