# Short001 sources — Dictation / 音声入力

確認日：2026-09-07（JST）

## 一次情報

| ID | URL / path | 何が確認できたか | v7での扱い |
|---|---|---|---|
| S001 | https://help.openai.com/en/articles/12168547-voice-dictation-faq | マイクで録音した音声が文字起こしされ、文字として返り、送信前に編集できること | Dictationの主根拠。説明欄にも掲載候補 |
| S002 | https://help.openai.com/en/articles/20001274 | 機能境界を確認するため、録音を文字にして送る用途と音声会話の用途が別に説明されていること | 境界確認だけ。v7の画面素材には使わない |
| S003 | `shorts/work/ChatGPT Voice画面録画.MP4` | ユーザー提供の実録画。話す、文字起こし中、質問文が表示される流れ | v7の主役。3.800〜12.800秒を使用 |
| S004 | https://help.openai.com/en/articles/5722486-chatgpt-privacy-policies | ChatGPTのデータ利用・Data Controlsの確認先 | Shortの本文では詳細を詰め込まない |

## Capture確認

- source：`C:/Codex/260829_youtube-anshin/shorts/work/ChatGPT Voice画面録画.MP4`
- duration：19.28秒
- selected interval：3.800〜12.800秒（9.000秒）
- visible content：マイク入力中 → 文字起こし中 → 「冷蔵庫にキャベツがあります。簡単な料理を教えてください。」
- personal information：選択区間にアカウント名・会話履歴・個人連絡先は見当たらない。上部の表示は必要最小限のcropにする。

## v7の除外

- 公式の音声会話紹介ページをVisual素材として使用しない。
- 音声会話の画面、返答音声、返答全文を使用しない。
- ChatGPT UIをImageGenで作らない。ユーザー提供captureのpixelをcrop・resizeするだけにする。

## 需要・見せ方の参考

| URL | 扱い |
|---|---|
| https://www.youtube.com/results?search_query=ChatGPT+%E9%9F%B3%E5%A3%B0%E5%85%A5%E5%8A%9B | 需要と古いUI例の観測だけ。事実根拠にはしない |

## 制限

OpenAIの表示名・画面位置・利用条件は、アプリ版、OS、アカウント、地域などで変わる可能性がある。Short001ではcaptureで確認できた動作だけを述べ、すべての利用者に同一とは断定しない。
