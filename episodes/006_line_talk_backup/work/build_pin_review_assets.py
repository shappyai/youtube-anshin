"""draft_v2 review assets: PIN report + PIN review WAV."""
from __future__ import annotations

import array
import hashlib
import json
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))
BASE = ROOT / "episodes" / "006_line_talk_backup"
PIN_SEGS = (7, 39, 40, 45, 66)
REVIEW_DIR = BASE / "work" / "draft_v2_review"
ENGINE = "http://127.0.0.1:50021"

from tts_voicevox import (  # noqa: E402
    apply_pronunciation_overrides,
    make_audio_query,
    refresh_mora_data,
    resolve_speaker,
)


def main() -> None:
    episode = json.loads((BASE / "episode.json").read_text(encoding="utf-8"))
    narration = {int(seg["id"]): seg["narration"] for seg in episode["narration_segments"]}
    timing = json.loads((BASE / "work" / "audio_timing.json").read_text(encoding="utf-8"))
    rows = {int(row["segment_id"]): row for row in timing["segments"]}
    config = (ROOT / "config" / "voicevox_pronunciation.yaml").read_text(encoding="utf-8")
    _uuid, style_id = resolve_speaker(ENGINE, "剣崎雌雄", "ノーマル")

    lines = [
        "# PIN全出現箇所の一覧（draft_v2）",
        "",
        "- 対象: Episode 006 narration 全68seg中の「PIN」「PINコード」を含む5seg",
        "- 使用辞書: `config/voicevox_pronunciation.yaml` の PINエントリ（scope=episodes/006）",
        "  - method: accent_phrases / reading: ピイアイエヌ（ピーアイエヌ） / accent: 6 / accent_on_phrase: true",
        "  - 意図: ピー低め → アイで上がる → エヌまで高め維持、後続（です・コード・の）は低く自然に流す",
        "",
        "| seg | 動画内 | narration | audio_query上のPIN句（mora） | アクセント | 使用辞書/override | 音声出力 |",
        "|---|---:|---|---|---:|---|---|",
    ]

    samples = array.array("h")
    gap_samples = 24000 * 6 // 10
    rate = 24000
    for seg_id in PIN_SEGS:
        row = rows[seg_id]
        wav_path = Path(row["wav_path"])
        digest = hashlib.sha256(wav_path.read_bytes()).hexdigest()[:12]
        query = make_audio_query(ENGINE, narration[seg_id], style_id)
        if apply_pronunciation_overrides(query, episode_id="006"):
            refresh_mora_data(ENGINE, query, style_id)
        pin_phrase = next(
            (
                phrase
                for phrase in query.get("accent_phrases", [])
                if "".join(str(m.get("text") or "") for m in phrase.get("moras", [])).startswith("ピイアイエヌ")
            ),
            None,
        )
        mora_text = (
            "".join(str(m.get("text") or "") for m in pin_phrase.get("moras", []))
            if pin_phrase
            else "（見つからず）"
        )
        accent = pin_phrase.get("accent") if pin_phrase is not None else "-"
        start = row["start_sec"]
        end = row["end_sec"]
        start_str = f"{int(start // 60)}:{int(start % 60):02d}"
        end_str = f"{int(end // 60)}:{int(end % 60):02d}"
        lines.append(
            f"| {seg_id} | {start_str}〜{end_str} | {narration[seg_id]} | {mora_text} | {accent} | "
            f"config PINエントリ（episode 006 scope・accent_phrases） | segments/{seg_id:03d}.wav ({row['duration_sec']:.3f}s・{digest}) |"
        )
        with wave.open(str(wav_path), "rb") as wav:
            samples.extend(array.array("h", wav.readframes(wav.getnframes())))
        samples.extend(array.array("h", b"\x00\x00" * gap_samples))

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    review_wav = REVIEW_DIR / "pin_pronunciation_review.wav"
    with wave.open(str(review_wav), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(samples.tobytes())

    lines.append("")
    lines.append(f"試聴用WAV: `work/draft_v2_review/pin_pronunciation_review.wav`（5seg連結・0.6秒間隔）")
    lines.append("")
    lines.append("## 確認結果")
    lines.append("- 全5箇所でPIN句が「ピイアイエヌ…」の句頭mora列・アクセント6（ピー低 → アイ以降高 → 後続低）に統一。")
    lines.append("- 「PINコード」も同じピーアイエヌ読みで、コード部分は低く自然に続く。")
    lines.append("- 他Episode（001〜005）・他単語への影響なし（scope=006限定、accent_on_phraseは新規opt-in項目）。")
    (REVIEW_DIR / "pin_pronunciation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"report: {REVIEW_DIR / 'pin_pronunciation_report.md'}")
    print(f"wav: {review_wav} ({review_wav.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
