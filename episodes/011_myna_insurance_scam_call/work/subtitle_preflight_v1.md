# Subtitle preflight

Episode: 011_myna_insurance_scam_call
Cues: 39
Safe width: 1800px (72px font measurement when available)

## FAIL

- seg 013: display_text不一致 (expected=「これ、本物？」を公式情報で確認。必要なら登録しておく / actual=「これ、本物？」を公式情報で確認しています。必要なら、登録しておいてください。)
- seg 015: display_text不一致 (expected=伝えない情報：マイナンバー／暗証番号／カード・口座情報／SMS認証コード / actual=伝えない情報：マイナンバー・暗証番号・カード・口座情報・SMS認証コード)
- seg 022: display_text不一致 (expected=正式な登録手順：医療機関・薬局／マイナポータル／セブン銀行ATM / actual=正式な登録方法：医療機関・薬局／マイナポータル／セブン銀行ATM)
- seg 038: display_text不一致 (expected=迷ったときは、その場で決めず、いったん止まる / actual=迷ったときは、その場で決めず、いったん止まって公式から確認)
- seg 039: display_text不一致 (expected=確認してから、必要な手続きを進める / actual=確認してから、必要な手続きを進める怖がらせる前に、確認する)
- なし

## WARN

- SUB-006: 2行の長さのバランスが悪い
- SUB-010: 2行の長さのバランスが悪い
- SUB-014: 2行の長さのバランスが悪い
- SUB-021: 2行の長さのバランスが悪い
- SUB-023: 1行が極端に短い (確認)
- SUB-023: 2行の長さのバランスが悪い
- SUB-029: 1行が極端に短い (緊急時)
- SUB-029: 2行の長さのバランスが悪い
- なし

## tts_reading_leakage

- result: FAIL
- fail count: 5

## Summary

- result: FAIL
- fail count: 5
- warn count: 8
- cue text is read from episode.json; no character-count auto-splitting is performed
