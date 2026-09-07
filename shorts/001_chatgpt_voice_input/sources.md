# Short001 sources — Dictation / 音声入力 / v8

確認日：2026-09-07（JST）

## 一次情報

| ID | URL / path | 何が確認できたか | v8での扱い |
|---|---|---|---|
| S001 | https://help.openai.com/en/articles/12168547-voice-dictation-faq | マイクで録音した音声が文字起こしされ、文字として返り、送信前に編集できること | Dictationの主根拠。説明欄にも掲載候補 |
| S002 | https://help.openai.com/en/articles/20001274 | Dictationで録音を文字にして送る用途と、Voiceで音声会話をする用途の境界 | 境界確認だけ。v8の画面素材・返答音声には使わない |
| S003 | `shorts/work/ChatGPT Voice画面録画.MP4` | ユーザー提供の実録画。質問の音声入力、文字化、送信後の実際のテキスト回答 | v8の主役。入力3.800〜12.800秒、回答14.200〜17.000秒をcrop / resize |
| S004 | https://help.openai.com/en/articles/5722486-chatgpt-privacy-policies | ChatGPTのデータ利用・Data Controlsの確認先 | Shortの本文では詳細を詰め込まない |

## Capture確認

- source：`C:/Codex/260829_youtube-anshin/shorts/work/ChatGPT Voice画面録画.MP4`
- duration：19.28秒
- Dictation入力区間：3.800〜12.800秒（9.000秒）
- 実回答区間：14.200〜17.000秒（2.800秒）
- visible flow：質問を話す → 文字起こし中 → 質問文表示 → 送信済み質問 → 実際のテキスト回答
- 回答冒頭：`もちろんです！キャベツだけでも、かなり簡単に作れます。`
- 料理名：`いちばん簡単「キャベツの塩昆布炒め」`
- personal information：採用cropではアカウント名・会話履歴・個人連絡先を含めない。

## v8の除外

- 公式の音声会話紹介ページをVisual素材として使用しない。
- Voice / リアルタイム会話の画面、返答音声を使用しない。
- ChatGPT UIや料理回答をImageGenで作らない。元captureのpixelをcrop・resizeするだけにする。
- 元capture後半の回答全文・評価dialogは使用しない。回答冒頭と料理名・材料が見える範囲だけを使う。

## 需要・見せ方の参考

| URL | 扱い |
|---|---|
| https://www.youtube.com/results?search_query=ChatGPT+%E9%9F%B3%E5%A3%B0%E5%85%A5%E5%8A%9B | 需要と古いUI例の観測だけ。事実根拠にはしない |

## 制限

OpenAIの表示名・画面位置・利用条件は、アプリ版、OS、アカウント、地域などで変わる可能性がある。Short001ではcaptureで確認できた動作だけを述べ、すべての利用者に同一とは断定しない。
