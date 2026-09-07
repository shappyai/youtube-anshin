# Episode 008 Final QA

確認日: 2026-09-05

- status: **PASS**
- final: `output/final.mp4`
- finalize: `draft_v3.mp4`からのbyte-identical copy（再encodeなし）
- SHA-256: `92166d59c228baff67ad32280899066ad050ff6c715646d773427ccba04f2854`
- duration: 336.870秒
- codec: H.264 1920×1080 30fps / AAC 48kHz mono
- decode errors: 0
- black frames: 0
- unexpected silence: 0（CTA末尾の意図した余韻を除く）
- Visual Gate v5 regression: 0
- subtitle regression: 0
- thumbnail QA: `work/thumbnail_review/thumbnail_qa.json` PASS

動画仕様のprobeはdraft_v3のPASS済み結果とSHA-256一致で確認し、decode・黒フレーム・無音はfinal.mp4を直接確認した。

## 未実施

- YouTube upload
- schedule / public
- thumbnail upload
- End Screen実設定
