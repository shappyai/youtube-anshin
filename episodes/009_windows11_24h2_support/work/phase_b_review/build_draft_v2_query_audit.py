"""Save the complete post-review VOICEVOX query audit for Episode 009."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))

from episode_io import load_pronunciation_entries  # noqa: E402
from tts_voicevox import (  # noqa: E402
    apply_pronunciation_overrides,
    make_audio_query,
    refresh_mora_data,
)
from voicevox_preflight import expected_reading  # noqa: E402

ENGINE_URL = "http://127.0.0.1:50021"
STYLE_ID = 21
EPISODE_ID = "009"
EPISODE_PATH = ROOT / "episodes" / "009_windows11_24h2_support" / "episode.json"
AUDIT_PATH = ROOT / "episodes" / "009_windows11_24h2_support" / "work" / "voicevox_query_audit.json"
REVIEW_AUDIT_PATH = ROOT / "episodes" / "009_windows11_24h2_support" / "work" / "phase_b_review" / "pronunciation_fix_v2_query_audit.json"


def main() -> int:
    data = json.loads(EPISODE_PATH.read_text(encoding="utf-8"))
    entries = load_pronunciation_entries()
    audit: dict[str, dict] = {}
    for segment in data.get("narration_segments", []):
        segment_id = int(segment["id"])
        effective_text, approvals = expected_reading(segment, entries, EPISODE_ID)
        query = make_audio_query(ENGINE_URL, effective_text, STYLE_ID)
        changed = apply_pronunciation_overrides(query, episode_id=EPISODE_ID)
        if changed:
            refresh_mora_data(ENGINE_URL, query, STYLE_ID)
        query["speedScale"] = 1.0
        query["intonationScale"] = 1.0
        query["pitchScale"] = 0.0
        audit[str(segment_id)] = {
            "segment_id": segment_id,
            "effective_text": effective_text,
            "approvals": approvals,
            "query": query,
        }
    payload = {
        "version": 2,
        "engine_url": ENGINE_URL,
        "speaker": "剣崎雌雄",
        "style": "ノーマル",
        "style_id": STYLE_ID,
        "segment_count": len(audit),
        "audit": audit,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    AUDIT_PATH.write_text(text, encoding="utf-8")
    REVIEW_AUDIT_PATH.write_text(text, encoding="utf-8")
    print(json.dumps({"status": "PASS", "segment_count": len(audit), "path": str(REVIEW_AUDIT_PATH)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
