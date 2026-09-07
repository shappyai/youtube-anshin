# PIN全出現箇所の一覧（draft_v2）

- 対象: Episode 006 narration 全68seg中の「PIN」「PINコード」を含む5seg
- 使用辞書: `config/voicevox_pronunciation.yaml` の PINエントリ（scope=episodes/006）
  - method: accent_phrases / reading: ピイアイエヌ（ピーアイエヌ） / accent: 6 / accent_on_phrase: true
  - 意図: ピー低め → アイで上がる → エヌまで高め維持、後続（です・コード・の）は低く自然に流す

| seg | 動画内 | narration | audio_query上のPIN句（mora） | アクセント | 使用辞書/override | 音声出力 |
|---|---:|---|---|---:|---|---|
| 7 | 0:29〜0:34 | 三つ、バックアップ用の暗証番号、PINです。 | ピイアイエヌデス | 6 | config PINエントリ（episode 006 scope・accent_phrases） | segments/007.wav (4.405s・457e8f888765) |
| 39 | 3:42〜3:48 | 三つ目の確認は、バックアップ用の暗証番号、PINコードです。 | ピイアイエヌコオドデス | 6 | config PINエントリ（episode 006 scope・accent_phrases） | segments/039.wav (5.472s・035443ccd038) |
| 40 | 3:48〜3:55 | PINコードは、引き継ぎのときに、トーク履歴を復元するための、6桁の暗証番号です。 | ピイアイエヌコオドワ | 6 | config PINエントリ（episode 006 scope・accent_phrases） | segments/040.wav (7.061s・0803be871782) |
| 45 | 4:22〜4:27 | PINの設定は、「トークのバックアップ」の画面から、できます。 | ピイアイエヌノ | 6 | config PINエントリ（episode 006 scope・accent_phrases） | segments/045.wav (5.227s・5dba64af24fa) |
| 66 | 6:21〜6:28 | 三つ、バックアップ用の暗証番号、PIN。直近14日間の、セーフティネットです。 | ピイアイエヌ | 6 | config PINエントリ（episode 006 scope・accent_phrases） | segments/066.wav (7.296s・56a00d12f516) |

試聴用WAV: `work/draft_v2_review/pin_pronunciation_review.wav`（5seg連結・0.6秒間隔）

## 確認結果
- 全5箇所でPIN句が「ピイアイエヌ…」の句頭mora列・アクセント6（ピー低 → アイ以降高 → 後続低）に統一。
- 「PINコード」も同じピーアイエヌ読みで、コード部分は低く自然に続く。
- 他Episode（001〜005）・他単語への影響なし（scope=006限定、accent_on_phraseは新規opt-in項目）。
