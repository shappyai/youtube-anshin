# Episode012 pronunciation audio audit v3

確認日：2026-09-06  
対象：Episode012 draft_v3の実使用音声と、実エンジンで再取得した文脈audio_query  
VOICEVOX：剣崎雌雄／ノーマル  
判定：PASS

辞書のreading登録だけではPASSにせず、`contextual_pronunciation_audio_gate`で実際の文全体を再queryした。表示字幕は漢字・英字表記を維持し、読み仮名は字幕へ流出させていない。

## 本物：全7出現の回帰確認

対象segment：002 / 003 / 008 / 014 / 030 / 066 / 079  
全件の実クエリ列：**ホ / ン / モ / ノ（4モーラ）**  
`extra_vowel_after_honmono=0`、辞書readingのみでなく各文脈queryを確認：**PASS**

### seg 030（中盤CTA）

- 実際の文：`「これ、本物？」は公式情報で確認します。必要なら登録しておいてください。`
- segment override：`本物 → ホンモノ / accent=4`
- `ホ / ン / モ / ノ`：4モーラ
- 疑問文：`is_interrogative=true`（母音追加ではなくピッチで表現）
- 余計な「オ」：0
- 最終ノの母音長：0.187347秒（文脈ゲート上限0.22秒）
- 音声WAV SHA-256：`CC06F734C6857E5FD91561131B40D8428E4248641AF0FED3AF6BAA604D5144BB`

### exact direct query

`audio_query`へ文**「これ、本物？」**を直接投入し、`ホ / ン / モ / ノ`、4モーラ、`is_interrogative=true`、余計な母音0を確認した。最終ノの母音長は0.154618秒。

## e-Tax：文脈音声と標準辞書

- 標準辞書：`e-Tax → イータックス`
- 実際の文：`e-Taxのメールも、登録した人に決まったパターンで届くお知らせで、原則として本文にURLはなく、ファイルも添付しないと説明されています。`
- 実クエリ列：**イ / イ / タ / ッ / ク / ス**
- accent：3、ピーク：**タ**
- 語中internal pause：0
- `ス`母音長：0.032084秒（上限0.10秒）
- 音声WAV SHA-256：`7BB320F8996B889F1F8B2756B98FA1C62905ED83BE20AE8B893CA7EE129B5924`

`audio_query`へ**「e-Taxのメールも、」**を直接投入した原文queryと、標準辞書適用後の`イータックスのメールも、`実クエリを両方記録した。辞書適用後の実クエリは6モーラ・accent=3・タピーク・internal pause=0でPASS。

## 再生成・再利用

- v3ではsegment 030（文脈accent override）とsegment 056（e-Tax標準辞書accent更新）の音声状態を確定した。
- CTA音声はEpisode011実使用WAVを再利用し、発音対象音声の再生成対象には含めていない。
- 詳細な全query evidenceは `pronunciation_audio_audit_v3.json`、Phase Aの全79query結果は `pronunciation_preflight_v3.md` に保存した。
