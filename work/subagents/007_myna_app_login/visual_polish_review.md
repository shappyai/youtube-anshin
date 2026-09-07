# Visual polish review — Episode 007「マイナアプリ ログインできない？まず確認したい5つ」

レビュー日: 2026-09-04
レビュー者: Visual improvement reviewer（サブエージェント）
対象: episodes/007_myna_app_login/episode.json（22 scene）/ work/phase_b_review/scene_contact_sheet_v3.png / work/rendered_final_scenes/（描画済み17 scene）
基準: config/icon_catalog.json（Material Symbols Rounded・Apache 2.0）/ docs/text_render_policy.md / templates/scenes/README.md

レビュー方針: 「説明スライド感」を減らし、TV視聴で一瞬で意味が伝わること・1画面1メッセージ・内容の正確性の維持を軸に、sceneごとに最適な方式を選定する。全sceneを派手にしない。

## 確認方法

- 描画済み17 sceneの個別PNGを目視（vision）確認＋contact sheet v3と突き合わせ。
- 下部字幕安全領域（下180px）はPowerShell/System.Drawingで機械計測（非白ピクセルの最下Y座標）。SCENE-021のみ安全領域へ約8px侵入を検出（他は境界1px以内・無視可）。
- SCENE-007/011/014/017/022は画像生成サービス障害により生成待ち（work/phase_b_review/production_preflight.md で確認）。本レビューでは計画内容（headline/support_text）に基づく確認のみで、実画像のQAは生成後に実施する。
- アイコン追加名は config/icon_catalog.json に現存する意味（login/lock/contactless/block/support_agent/biometric）と、Material Symbols Roundedの一般的な意味論に基づく提案として記録する。catalogへの追加可否は親Codexの判断（canonical fileは編集しない）。

## scene別レビュー

| scene_id | current issue（現在の問題） | proposed mode（提案） | expected benefit（期待効果） | change/keep 判定 |
|---|---|---|---|---|
| SCENE-001 | なし（「ログインできない？」+semantic icon login/navy・人間承認済み）。※下部の淡い帯に表示される「導入（問題提示・結論）」はmain_message由来の内部ラベルの見え方。視聴者向け文言ではないため、親Codexで表示要否を一度確認することを推奨（変更提案はしない） | KEEP（触らない） | 冒頭の問題提示として成立。変更なしで安定 | keep |
| SCENE-002 | 白背景・文字中心でやや「説明スライド感」。5項目が番号丸のみで、各項目の意味アイコンがない。字幕帯への接触は1px（無視可） | ICON IMPROVE（任意）: 5項目それぞれに小さめのsemantic icon候補を追加（①phone_android：対応端末 ②contactless：カード読み取り ③pin：暗証番号 ④calendar_month：期限 ⑤support_agent：窓口。いずれもcatalog拡張候補・親Codex判断）。背景は白のままか、ごく淡いsoft gradient（画面の30%未満・見出しより弱く） | テレビ視聴で5項目の内容が文字を読む前におおよそ伝わる。一覧の「確認する順番」が視覚化され記憶に残りやすい | change（任意・優先度低） |
| SCENE-003 | なし。imagegen_native一体生成（A/B Candidate A採用・人間承認済み）描画済み（scene_003.png） | KEEP（採用済み・再生成しない） | TV可読性・文字とイラストの一体感を維持 | keep |
| SCENE-004 | なし（軽微）: 見出し2行・数字（iOS 16.4以上／Android 11以降／NFC）を含む。レイアウト重なり・文字切れなし | OFFICIAL KEEP。任意のマイナー案: 「iOS 16.4以上」「Android 11以降」の数字部分だけ色・太さを一段強調（pil_overlayのまま） | 公式数字の視認性が上がり、見比べやすくなる | keep（数字強調は任意） |
| SCENE-005 | なし（軽微）: 見出し3行と文字量は多めだが公式FAQの引用であり正確性優先。レイアウト破綻なし | OFFICIAL KEEP。任意のマイナー案: 見出しを「通常モードで開き直す」程度に短縮＋supportに「シークレットモード→通常モード」の1行補足（文言変更は親Codex・fact check経由で） | 一画面の読む量が減り、TVで追いやすくなる | keep（文言短縮は任意・要fact check） |
| SCENE-006 | なし（semantic icon lock/blue・人間承認済み） | KEEP（触らない） | 注意sceneとしての意味がアイコンで補強されている | keep |
| SCENE-007 | 生成待ち（計画のみ）: 見出し「カードを、読み取る」＋補助「スマホとカードの、向きと場所。」。総文字量はimagegen_native推奨（30〜40文字以下）に収まる | IMAGEGEN IMPROVE（計画済み・生成待ち）: gpt_image概念sceneとしてimagegen_native一体生成。生成後にexact text QA（完全一致・文字崩れ・TV可読性）必須、FAIL時は1回再生成→2回目NGでpil_overlay fallback | 概念sceneがテンプレ感なく、読み取りのイメージが一瞬で伝わる | change（生成待ち） |
| SCENE-008 | 既知の問題を確認: 左の引用テキストと右側の公式イラストが重なり、「https://services.digital.go.jp/mynaapp/scan-mynum…」と見出しの一部が画像に被って見切れている | LAYOUT FIX（必須）: テキストブロックの幅を右イラストと衝突しない範囲に制限（例: 見出し・URL行を左70%幅内に収める、またはURL行の背後にscrimを敷く）。URLは視聴者が手入力できるよう完全表示する | 公式情報の引用が欠けずに読め、出典リンクも辿れる。正確性と可読性が両立する | change（必須） |
| SCENE-009 | 既知の問題を確認: SCENE-008と同様に、引用テキストの右端が右側の公式イラストに重なり、出典URLが画像で隠れて見切れている | LAYOUT FIX（必須）: テキスト折返し幅をイラスト左端までに制限し、URL行を隠さない。見出し2行目「機種によって、場所は少し違いま…」も全文表示させる | Androidの読み取り位置説明が欠けず読める。08と左右同一ルールで統一感が出る | change（必須） |
| SCENE-010 | なし（semantic icon contactless/blue・人間承認済み） | KEEP（触らない） | 「読み取りの4つの注意」の意味をアイコンが補強 | keep |
| SCENE-011 | 生成待ち（計画のみ）: 見出し「暗証番号で、止まる」＋補助「使うのは、数字4桁。」。文字量は最適域 | IMAGEGEN IMPROVE（計画済み・生成待ち）: セクション扉としてimagegen_native一体生成→exact text QA→必要時fallback | 数字4桁の概念が短い見出しで一瞬伝わる | change（生成待ち） |
| SCENE-012 | なし（軽微）: 公式引用カード・見出し3行。文字量は多めだが「数字4桁」「顔・指紋」の正確性優先 | OFFICIAL KEEP。任意のマイナー案: support領域に小さなsemantic icon候補 pin（数字4桁の暗証番号）を淡いトーン円で補助追加。または「数字4桁」の数字部分を強調 | 「4桁」が数字として目に入り、6桁/英数字との誤解が減る | keep（pin追加は任意） |
| SCENE-013 | なし（semantic icon block/amber・人間承認済み） | KEEP（触らない） | 最重要注意（3回でロック）がアイコンとamberで強調済み | keep |
| SCENE-014 | 生成待ち（計画のみ）: 見出し「カードと、証明書の期限」＋補助「期限は、別もの。」。文字量OK | IMAGEGEN IMPROVE（計画済み・生成待ち）: imagegen_native一体生成→exact text QA→必要時fallback。「期限は、別もの。」のニュアンス（2つの期限が別物）を背景モチーフで表現 | 2つの期限の区別が概念レベルで伝わる | change（生成待ち） |
| SCENE-015 | なし（軽微）: 公式引用カード・見出し2行・数字（10回目・3か月前）を含む。重なりなし | OFFICIAL KEEP。任意のマイナー案: 「10回目の誕生日」「3か月前」の数字部分の強調 | 期限の数字がTVでも目に入る | keep（数字強調は任意） |
| SCENE-016 | なし（軽微）: 比較2カラム（カード=青／電子証明書=緑）は意味が明確。白背景・文字中心でアイコンなし | ICON IMPROVE（任意）: 左右パネルにsmall semantic icon候補（左: badge／右: keyまたはverified_user。期限ニュアンスなら両方にcalendar_monthの併用も可）。アイコンは淡いトーン小円に収め、パネル見出しより強くしない | カードと証明書の違いが色＋アイコンで一瞬で区別できる | change（任意・優先度低） |
| SCENE-017 | 生成待ち（計画のみ）: 見出し「それでも、ダメなら」＋補助「再設定・メンテナンス・公式窓口。」。補助が12文字で推奨上限内 | IMAGEGEN IMPROVE（計画済み・生成待ち）: imagegen_native一体生成→exact text QA→必要時fallback。クロージング前の「最後の砦」感のある背景 | 困ったときの逃げ場がある安心感を伝える | change（生成待ち） |
| SCENE-018 | なし（軽微）: 公式引用カード・見出し2行。公式文言の引用として整理されている | OFFICIAL KEEP | 障害・メンテナンス確認という案内が正確に伝わる | keep |
| SCENE-019 | なし（軽微）: 公式引用カード・見出し2行。文字量はやや多めだが「本人確認のため…入力が必要」という正確性優先の文言 | OFFICIAL KEEP。任意のマイナー案: support領域に小さなsemantic icon候補 lock_reset（再設定）を淡いトーン円で補助追加 | 「再設定」の意味が補強され、作業のイメージが湧く | keep（lock_reset追加は任意） |
| SCENE-020 | なし（semantic icon support_agent/green・人間承認済み）。※目視で中央下部に「案内（窓口・002案内）」というmain_message由来の内部用語が表示されている。視聴者には「002案内」の意味が通じないため、表示文言の変更（例: 「公式の窓口」）または非表示を親Codexへ提案（承認済みsceneのため変更はしない） | KEEP（触らない）＋親Codexへ文言確認事項を伝達 | 窓口案内の意味はアイコンで成立。内部ラベルが消えれば視聴者向け表現として完成度が上がる | keep（文言のみ要確認） |
| SCENE-021 | 軽微: 5つ目のチェック項目行が下部ブランド表記（「大人のデジタル安心室」）と接近し、字幕安全領域へ約8px侵入（機械計測）。目視でも項目5と下帯が重なり気味 | LAYOUT FIX（軽微）: 5項目の行間を詰める・リスト全体を上へ数10px移動し、項目5と下帯・安全領域をクリア。チェック丸（意図されたリスト表現）は維持。soft gradient背景は任意 | まとめの最後の項目が字幕に被らず、TVでも全文読める | change（軽微修正） |
| SCENE-022 | 生成待ち（計画のみ）: 見出し「あわてずに、確認しましょう」＋補助「困ったときは、この順番を。」。改行位置・句読点を含むexact text QA対象 | IMAGEGEN IMPROVE（計画済み・生成待ち）: gpt_image概念sceneとしてimagegen_native一体生成→exact text QA（改行位置・「。」の完全一致含む）→必要時fallback | クロージングの安心感が背景と一体化し、テンプレ感がない | change（生成待ち） |

## 分類サマリ

| 分類 | scene | 数 |
|---|---|---:|
| KEEP（現状維持・人間承認済みを含む） | SCENE-001, 003, 006, 010, 013, 020 | 6 |
| OFFICIAL KEEP（公式引用・内容正確性優先で現状維持） | SCENE-004, 005, 012, 015, 018, 019 | 6 |
| IMAGEGEN IMPROVE（計画済み・生成待ち） | SCENE-007, 011, 014, 017, 022 | 5 |
| ICON IMPROVE（改善候補・任意） | SCENE-002, 016 | 2 |
| LAYOUT FIX（必須修正） | SCENE-008, 009 | 2 |
| LAYOUT FIX（軽微修正） | SCENE-021 | 1 |
| **合計** | | **22** |

- 維持（KEEP＋OFFICIAL KEEP）: 12 scene
- 改善候補（任意）: 2 scene（ICON IMPROVE）
- 必須修正: 2 scene（SCENE-008/009の文字×画像の重なり・URL見切れ）＋軽微1 scene（SCENE-021の安全領域侵入）
- 生成待ち（計画どおり進行）: 5 scene（imagegen_native・生成後のexact text QAが前提）

## 補足（事実断定しない・親Codex判断事項）

- SCENE-008/009の重なり・URL見切れは目視（vision）で確認した。正式な修正対象の確定はフル解像度での人間確認を推奨する。
- SCENE-021の安全領域侵入は機械計測（下180px・非白ピクセル最下Y=908px）で確認。8px程度の軽微な接触。字幕実寸が入る前に修正するのが安全。
- SCENE-001/020の下部ラベル文言（「導入（問題提示・結論）」「案内（窓口・002案内）」）はmain_message由来とみられるが、内部用語が視聴者に見える表現になっている。承認済みsceneのため本レビューでは変更を提案せず、親Codexの確認事項として記録する（真偽の断定はしない）。
- 追加アイコン候補（phone_android/contactless/pin/calendar_month/support_agent/badge/key/verified_user/lock_reset）はすべて config/icon_catalog.json の既存意味またはMaterial Symbols Roundedの意味論に基づく提案であり、採用可否・catalog拡張は親Codexの判断。採用時は淡いトーン円（150〜220px目安・180px基準）・headlineより強くしない・画面の30%未満という恒久ルールに従う。
- imagegen_native 5 sceneは生成後に exact text QA（指定文言完全一致・誤字脱字・余計な文字・文字崩れ・行順・文字切れ・はみ出し・人物/オブジェクトとの重なり・コントラスト・縮小時可読性）を実施し、1回再生成→2回目NGはそのsceneのみpil_overlayへfallbackする方針を確認（docs/text_render_policy.md準拠）。

Visual polish review完了。親Codexの採用判断待ち
