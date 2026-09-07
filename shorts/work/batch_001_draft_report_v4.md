# Shorts探索バッチ001 Visual Redesign v4 report

- draft_v3 human gate REJECTED（スライドショー感）を受け、3 core scenes + 8 visual beatsへ変更。
- visual change target：2〜4秒。static hold >7秒：0。static hold >5秒：Short001/003は各1、Short002は0（各Shortで<=1）。
- dedicated CTA slide：0。結論Visualを維持し、最後2〜3秒に実チャンネルアイコン＋`大人のデジタル安心室`だけを表示。
- pseudo subscribe UI / red register button：0。
- ImageGen：既存v2完成画を再利用。新規ImageGen call：0、再生成：0。
- Short002 privacy：拒否済みのImageGen人物sceneを廃止し、generic document + 該当領域■■■■のrenderer-nativeへ置換。
- Short001：現行chatgpt.comログアウト画面を実画面として使用。公式Voice紹介ページは参照画面のみ。ライブVoiceセッションはCAPTURE_REQUIRED。
- 音声：ChatGPTの「ト」accent=3を確認した2文 + 共通CTAだけをv4再生成。その他は既存WAVを再利用。全音声再生成0。

| ID | duration | core | beats | mean visual interval | >5 sec | >7 sec | ImageGen | renderer beats | real UI | Voice capture | script変更 | audio再生成 | draft |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| Short001 | 28.21秒 | 3 | 8 | 3.53秒 | 1 | 0 | 2 reuse | 0 | 3 | CAPTURE_REQUIRED | 1 | 3 | `shorts/001_chatgpt_voice_input/output/draft_v4.mp4` |
| Short002 | 32.24秒 | 3 | 8 | 4.03秒 | 0 | 0 | 2 reuse | 3 | 0 | NOT_APPLICABLE | 1 | 1 | `shorts/002_ai_suspicious_message/output/draft_v4.mp4` |
| Short003 | 28.60秒 | 3 | 8 | 3.57秒 | 1 | 0 | 3 reuse | 2 | 0 | NOT_APPLICABLE | 1 | 1 | `shorts/003_mynumber_smartphone/output/draft_v4.mp4` |

## Draft Gate checklist

- core scene count：3本とも3。visual beat：3本とも8。
- static hold >7秒：0。static hold >5秒：Short001/003は各1、Short002は0。
- slideshow feel：1/5 REVIEW。Shorts-native feel：4/5 REVIEW。
- subtitle：target80px、min64px、max2行、overflow0。
- fake UI：0。official UI AI reconstruction：0。privacy fail：0。viewer-facing internal brand promise：0。
- ChatGPT pronunciation：`チャ・ッ・ト`の`ト`へaccent=3、query observation PASS。人間聴取はDraft Gate待ち。
- CTA spoken canonical：`次に困ったときのために、このチャンネルを登録しておいてください。`
- batch contact sheet：`shorts/work/batch_001_draft_contact_sheet_v4.png`

Shorts探索バッチ001 Visual Redesign v4完成。
静止画スライドショー方式を廃止し、
Shorts-native visual beats方式へ変更。
人間Draft Gate待ち。
