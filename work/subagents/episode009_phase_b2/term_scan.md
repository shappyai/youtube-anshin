# Episode 009 Phase B2 発音局所修正候補スキャン

確認日: 2026-09-05

## 目的と扱い

Episode 009 の episode.json、script.md、実測 work/audio_timing.json、現在の config/voicevox_pronunciation.yaml を読み合わせ、方 / Windows / Update / ID の該当segmentと、draft_v2で検討できる局所発音修正候補を整理した。

この報告ではcanonicalファイルを変更していない。episode.json、script.md、work/audio_timing.json、config/voicevox_pronunciation.yamlは読み取りのみである。

## 読み合わせ結果

- episode.json の音声本文は narration_segments に52件ある。
- narration がVOICEVOX入力の正本。display_text は表示字幕用で、発音修正候補では変更しない。
- 実測音声timingは52件で、start_sec / end_sec はsegment単位で対応している。
- 現在の reading_overrides はsegment単位。対象語の既存overrideは24H2 / 25H2 / 26H1だけで、方 / Windows / Update / ID は未登録。
- 現在の標準辞書は18エントリ。対象4語と Windows Update の辞書エントリはない。
- VOICEVOX query audit上の現在の読みは、Windows=ウィンドオズ、Update=アップデエト、ID=アイディイ。方は文脈に応じて ホオ または複合語内の カタ になっている。

## 1. 方 の全該当segment

現在の pronunciation preflight では、次の4件が文脈依存語としてREVIEWになっている。

| segment | scene | audio timing | 文脈 | 現在のquery上の読み | 候補 |
|---:|---:|---:|---|---|---|
| 001 | 001 | 0.000–9.867 | Windows 11を使っている方、2026年10月13日に、一部のWindows 11で更新の提供が終わります。 | ホオ（ほう） | かた。視聴者・利用者を指すため、方→かたの強い候補 |
| 006 | 002 | 27.464–31.304 | 三つ目、更新が表示されないときの考え方です。 | カンガエカタ（考え方の「かた」） | 変更しない。複合語として現在の読みで意味に合う |
| 011 | 003 | 62.360–67.693 | 家庭でよく使われるHomeやProの方は、まず自分のバージョンを確認しましょう。 | ホオ（ほう） | かた。HomeやProを使っている人を指すため、方→かたの強い候補 |
| 038 | 013 | 204.539–212.229 | 24H2の方は、まず25H2が表示されるかを確認してください。 | ホオ（ほう） | 変更しない候補。「24H2のほうは」= 24H2について、の意味で現在の読みが自然 |

### 方 の推奨適用範囲

グローバル辞書に方を追加しない。かたとほうが同一episode内で必要になるため、局所的に次を候補とする。

- seg001: 方→かた
- seg011: 方→かた
- seg006: 現状維持
- seg038: 現状維持（ほう）

006と038は現状維持候補。特に038を一括でかたにしないことが重要。

## 2. Windows の全該当segment

該当は16segment。現在は全件、query上で概ねウィンドオズになっている。

| segment | scene | audio timing | 文脈 | 現在の読み | 局所修正候補 |
|---:|---:|---:|---|---|---|
| 001 | 001 | 0.000–9.867 | Windows 11を使っている方、2026年10月13日に、一部のWindows 11で更新の提供が終わります。 | ウィンドオズ | Windows→ウィンドウズ |
| 002 | 001 | 10.067–15.741 | ただし、Windows 11全部が、その日に使えなくなるわけではありません。 | ウィンドオズ | Windows→ウィンドウズ |
| 004 | 002 | 21.080–24.035 | 一つ目、自分のWindowsのバージョンです。 | ウィンドオズ | Windows→ウィンドウズ |
| 005 | 002 | 24.235–27.264 | 二つ目、Windows Updateの画面です。 | ウィンドオズ | Windows→ウィンドウズ |
| 008 | 003 | 34.471–50.279 | 今回、2026年10月13日に更新の終了とされているのは、Windows 11のうち、バージョン24H2のHome、Pro、Pro Education、Pro for Workstationsです。 | ウィンドオズ | Windows→ウィンドウズ |
| 009 | 003 | 50.579–57.555 | これは、Windows 11全体が10月13日に終了する、という意味ではありません。 | ウィンドオズ | Windows→ウィンドウズ |
| 014 | 004 | 76.297–79.743 | 下のほうにある、Windowsの仕様を見てください。 | ウィンドオズ | Windows→ウィンドウズ |
| 020 | 007 | 104.413–108.904 | デバイスの仕様という見出しの下で、Windowsの仕様を探します。 | ウィンドオズ | Windows→ウィンドウズ |
| 022 | 008 | 114.503–117.255 | 二つ目は、Windows Updateです。 | ウィンドオズ | Windows→ウィンドウズ |
| 023 | 008 | 117.455–120.793 | 設定から、Windows Updateを開きます。 | ウィンドオズ | Windows→ウィンドウズ |
| 025 | 009 | 123.843–134.019 | 更新が準備できている場合は、Windows 11 version 25H2のダウンロードとインストールが表示されます。 | ウィンドオズ | Windows→ウィンドウズ |
| 037 | 012 | 196.004–204.239 | Microsoftは、26H1を既存のパソコンへWindows Updateで提供しないと説明しています。 | ウィンドオズ | Windows→ウィンドウズ |
| 039 | 013 | 212.429–216.792 | まずは、いまのWindows Updateを最新の状態にします。 | ウィンドオズ | Windows→ウィンドウズ |
| 047 | 016 | 260.868–268.367 | まず、バージョンを確認し、Windows Updateを確認する。これが、いま行う順番です。 | ウィンドオズ | Windows→ウィンドウズ |
| 049 | 017 | 271.053–274.552 | 一つ目、自分のWindowsのバージョンを確認する。 | ウィンドオズ | Windows→ウィンドウズ |
| 050 | 018 | 274.752–279.061 | 二つ目、Windows Updateで更新プログラムを確認する。 | ウィンドオズ | Windows→ウィンドウズ |

### Windows の扱い

Windowsは16件すべて同一の固有名詞として扱えるため、候補は16segmentにだけWindows→ウィンドウズのsegment-local overrideを追加すること。人間試聴で自然さを確認後、Episode 009限定の設定として管理する。

現在の標準辞書へ無条件追加する候補ではない。英語UI・公式表記は画面と字幕に残し、変更対象はVOICEVOX入力だけにする。

## 3. Update の全該当segment

該当は7segmentで、すべてWindows Updateの一部。現在のquery上のUpdateはアップデエト。

| segment | scene | audio timing | 文脈 | 現在の読み | 局所修正候補 |
|---:|---:|---:|---|---|---|
| 005 | 002 | 24.235–27.264 | 二つ目、Windows Updateの画面です。 | アップデエト | Update→アップデート |
| 022 | 008 | 114.503–117.255 | 二つ目は、Windows Updateです。 | アップデエト | Update→アップデート |
| 023 | 008 | 117.455–120.793 | 設定から、Windows Updateを開きます。 | アップデエト | Update→アップデート |
| 037 | 012 | 196.004–204.239 | Microsoftは、26H1を既存のパソコンへWindows Updateで提供しないと説明しています。 | アップデエト | Update→アップデート |
| 039 | 013 | 212.429–216.792 | まずは、いまのWindows Updateを最新の状態にします。 | アップデエト | Update→アップデート |
| 047 | 016 | 260.868–268.367 | まず、バージョンを確認し、Windows Updateを確認する。これが、いま行う順番です。 | アップデエト | Update→アップデート |
| 050 | 018 | 274.752–279.061 | 二つ目、Windows Updateで更新プログラムを確認する。 | アップデエト | Update→アップデート |

### Update の扱い

Windowsと同時に候補適用する場合、音声上の候補はウィンドウズ・アップデート。表示字幕・公式UIのWindows Updateは変更しない。

候補の局所マッピング:

- seg005、022、023、037、039、047、050: Windows→ウィンドウズ、Update→アップデート

上記は候補の形であり、canonical episode.jsonにはまだ反映していない。

## 4. ID の全該当segment

| segment | scene | audio timing | 文脈 | 現在の読み | 局所修正候補 |
|---:|---:|---:|---|---|---|
| 019 | 006 | 98.748–104.113 | 個人名やIDが見えている場合は、動画や人に見せる前に隠してください。 | アイディイ | ID→アイディー。個人情報注意の説明として、聞き取りやすい標準的な読みを優先 |

IDは1件だけなので、グローバル辞書へ追加せずsegment 019の局所修正候補とする。

## 5. 現在の reading_overrides

現在のEpisode 009で明示されているsegment-local overrideは、バージョン表記11segment分だけ。

| segment | override |
|---:|---|
| 008 | 24H2→にじゅうよん、エイチ、ツー |
| 016 | 24H2→にじゅうよん、エイチ、ツー、25H2→にじゅうご、エイチ、ツー |
| 021 | 24H2→にじゅうよん、エイチ、ツー |
| 025 | 25H2→にじゅうご、エイチ、ツー |
| 029 | 25H2→にじゅうご、エイチ、ツー |
| 034 | 26H1→にじゅうろく、エイチ、ワン |
| 035 | 26H1→にじゅうろく、エイチ、ワン |
| 036 | 24H2→にじゅうよん、エイチ、ツー、26H1→にじゅうろく、エイチ、ワン |
| 037 | 26H1→にじゅうろく、エイチ、ワン |
| 038 | 24H2→にじゅうよん、エイチ、ツー、25H2→にじゅうご、エイチ、ツー |
| 044 | 24H2→にじゅうよん、エイチ、ツー |

episode.jsonのepisode-levelまたはnarration-levelに、対象4語の共通overrideはない。reading_overridesのないsegmentは空オブジェクトで保持されている。

## 6. 現在の標準辞書構造

ファイル: config/voicevox_pronunciation.yaml

- ルート: pronunciations 配列。
- method: text_replacement は、表記をVOICEVOX入力用の読みへ置換する方式。
- method: accent_phrases は、reading / accent_phrasesでアクセント句を調整する方式。
- 18エントリ中、対象4語とWindows Updateは未登録。
- 方 / 下 / 今日 / 行うなど文脈依存語は、既存実装でも無条件の標準辞書化を避ける方針。
- NFC / PINのような略語や、24H2 / 25H2 / 26H1のようなEpisode固有の読みは、置換・segment overrideで局所適用する構造が既にある。

対象surfaceとの重複:

| surface | 現在の標準辞書 |
|---|---|
| 方 | なし |
| Windows | なし |
| Update | なし |
| Windows Update | なし |
| ID | なし |

## 7. 変更対象segment候補のまとめ

### 強い候補

- 方: seg001、seg011をかた。seg006は現状維持、seg038はほうのまま。
- ID: seg019をアイディー。

### 一括確認候補

- Windows: seg001、002、004、005、008、009、014、020、022、023、025、037、039、047、049、050の16件をウィンドウズ。
- Update: seg005、022、023、037、039、047、050の7件をアップデート。

### 変更しないもの

- display_text、字幕表記、公式UI上の英語表記。
- グローバル pronunciation dictionaryへの方の無条件登録。
- 方のseg006「考え方」のかた。
- 方のseg038「24H2のほうは」のほう。
- 今回の指定外の文脈依存語 今日 / 下 / 行う。別途人間試聴対象だが、本スキャンの変更候補には含めない。

## 8. draft_v2へ進める場合の注意

候補を採用する場合も、canonical episode.jsonのnarration / display_textを書き換えず、既存のsegment-local reading_overrides方式に合わせて音声入力だけを変えるのが安全。

候補適用後は、対象segmentだけを再生成し、次を再確認する。

1. 対象segmentの音声を人間試聴する。
2. audio_timing.jsonを再計測し、後続字幕・scene timelineのずれを確認する。
3. 方の4文を連続して聴き、かた / ほうの使い分けを確認する。
4. ウィンドウズ・アップデートの連続語が不自然に間延びしないか確認する。
5. seg019は個人情報注意の文脈なので、IDの読みが聞き取りやすいか確認する。
6. 表示字幕には読み仮名を流出させない。

## 参照したファイル

- episodes/009_windows11_24h2_support/episode.json
- episodes/009_windows11_24h2_support/script.md
- episodes/009_windows11_24h2_support/work/audio_timing.json
- episodes/009_windows11_24h2_support/work/voicevox_query_audit.json（現在のquery読みの確認用）
- config/voicevox_pronunciation.yaml
- episodes/009_windows11_24h2_support/work/phase_b_review/pronunciation_preflight.md

結論: draft_v2の局所修正候補は、最優先が方のseg001/011とIDのseg019。Windows/Updateは16/7segmentに同一方針で適用できるが、変更範囲が広いため、候補音声を作ってから人間試聴で採否を決める。
