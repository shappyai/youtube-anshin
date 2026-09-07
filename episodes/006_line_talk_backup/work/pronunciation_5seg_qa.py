"""Phase B後半: 承認済みpronunciation 5件の実音声QAとレビュー用WAV作成."""
from __future__ import annotations

import array
import json
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "episodes" / "006_line_talk_backup"
EPISODE_JSON = BASE / "episode.json"
WORK = BASE / "work"
AUDIO_DIR = BASE / "audio" / "voicevox_kenzaki"
SEGMENTS = (18, 20, 37, 47, 62)


def main() -> None:
    episode = json.loads(EPISODE_JSON.read_text(encoding="utf-8"))
    narration = {int(seg["id"]): seg["narration"] for seg in episode["narration_segments"]}
    timing = json.loads((WORK / "audio_timing.json").read_text(encoding="utf-8"))
    rows = {int(row["segment_id"]): row for row in timing["segments"]}
    audit = json.loads((WORK / "voicevox_query_audit.json").read_text(encoding="utf-8"))

    lines = ["# pronunciation 5件の実音声QA（本番生成後）", ""]
    gap = 0.6
    samples = array.array("h")
    rate = 24000
    for seg in SEGMENTS:
        row = rows[seg]
        query = audit.get(str(seg), {}).get("query", {})
        kana = query.get("kana") or ""
        path = Path(row["wav_path"])
        with wave.open(str(path), "rb") as wav:
            frames = wav.readframes(wav.getnframes())
            samples.extend(array.array("h", frames))
        samples.extend(array.array("h", b"\x00\x00" * int(rate * gap)))
        lines.append(f"- seg {seg} | {narration[seg]}")
        lines.append(f"  - query kana: {kana}")
        lines.append(f"  - 実測 {row['duration_sec']:.3f}s | 動画内 {row['start_sec']:.2f}s 〜 {row['end_sec']:.2f}s")

    review_dir = BASE / "work" / "phase_b_review" / "audio"
    review_dir.mkdir(parents=True, exist_ok=True)
    review = review_dir / "pronunciation_5seg_review.wav"
    with wave.open(str(review), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(samples.tobytes())
    lines.append("")
    lines.append(f"レビュー用WAV（5件連結・0.6秒間隔）: {review}")
    (BASE / "work" / "phase_b_review" / "pronunciation_real_audio_qa.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print("\n".join(lines))


if __name__ == "__main__":
    main()
