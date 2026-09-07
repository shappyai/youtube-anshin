"""3-way VOICEVOX naturalness comparison (A/B/C) for a ~30-40s segment.

A: one audio_query -> synthesis for the whole segment (standard values).
B: one audio_query -> synthesis per sentence, concatenated in order
   (standard values; only short 0.2-0.35s gaps added if the engine's own
   sentence-end pause is shorter than 0.2s).
C: same per-sentence flow with small, non-extreme tuning:
   speedScale 0.94, intonationScale 1.10, pitchScale 0.0.

No full-episode generation, no pronunciation dictionary changes, and no
judgement of "which sounds better" - that is left to the human listener.
"""
from __future__ import annotations

import argparse
import json
import sys
import wave
from pathlib import Path
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from tts_voicevox import resolve_speaker, make_audio_query  # noqa: E402

ENGINE_URL = "http://127.0.0.1:50021"
DEFAULT_SPEAKER_NAME = "雀松朱司"
STYLE_NAME = "ノーマル"
TEST_DIR = ROOT / "episodes" / "001_google_security" / "audio" / "voicevox_test"
COMMON_SCRIPT = TEST_DIR / "naturalness_common_script.txt"
SRC_SCRIPT = TEST_DIR / "suzumatsu_test_script.txt"

FILES = {
    "A": {
        "suffix": "A_long_query.wav",
        "query_json_suffix": "A_audio_query.json",
        "speed": 1.0,
        "intonation": 1.0,
        "pitch": 0.0,
        "per_sentence": False,
    },
    "B": {
        "suffix": "B_sentence.wav",
        "speed": 1.0,
        "intonation": 1.0,
        "pitch": 0.0,
        "per_sentence": True,
    },
    "C": {
        "suffix": "C_tuned.wav",
        "speed": 0.94,
        "intonation": 1.10,
        "pitch": 0.0,
        "per_sentence": True,
    },
}

MIN_TAIL_SILENCE = 0.20   # seconds; pad only if the engine's own tail is shorter
TARGET_GAP = 0.25         # seconds; short inter-sentence gap when padding is needed
SILENCE_THRESHOLD = 100   # |sample| below this is treated as silence (16-bit)


def synth_bytes(query: dict, speaker: int, timeout: int = 300) -> bytes:
    url = f"{ENGINE_URL}/synthesis?speaker={speaker}"
    data = json.dumps(query, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "Accept": "audio/wav"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def wav_info(wav_bytes: bytes) -> tuple[int, int, int]:
    w = wave.open(__import__("io").BytesIO(wav_bytes), "rb")
    try:
        return w.getframerate(), w.getnchannels(), w.getsampwidth()
    finally:
        w.close()


def tail_silence_seconds(wav_bytes: bytes, rate: int) -> float:
    import array
    w = wave.open(__import__("io").BytesIO(wav_bytes), "rb")
    try:
        samples = array.array("h", w.readframes(w.getnframes()))
    finally:
        w.close()
    n = 0
    for s in reversed(samples):
        if abs(s) < SILENCE_THRESHOLD:
            n += 1
        else:
            break
    return n / rate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--speaker", default=DEFAULT_SPEAKER_NAME)
    parser.add_argument("--style", default=STYLE_NAME)
    parser.add_argument(
        "--prefix",
        default="naturalness_",
        help="output file name prefix (e.g. 'kenzaki_'), used for A/B/C WAVs, A query JSON and manifest",
    )
    args = parser.parse_args()

    speaker_uuid, style_id = resolve_speaker(ENGINE_URL, args.speaker, args.style)
    lines = [l for l in COMMON_SCRIPT.read_text(encoding="utf-8").splitlines() if l.strip()]
    src = SRC_SCRIPT.read_text(encoding="utf-8")
    for l in lines:
        if l not in src:
            print(f"common script line not verbatim in suzumatsu_test_script.txt: {l}", file=sys.stderr)
            return 1

    manifest = {
        "generated": "2026-08-30",
        "engine": "VOICEVOX ENGINE 0.25.2",
        "speaker": args.speaker,
        "style": args.style,
        "style_id": style_id,
        "common_script": str(COMMON_SCRIPT.relative_to(ROOT)),
        "sentences": lines,
        "files": {},
    }

    for mode, cfg in FILES.items():
        out_name = args.prefix + cfg["suffix"]

        def query_for(text: str) -> dict:
            q = make_audio_query(ENGINE_URL, text, style_id)
            q["speedScale"] = cfg["speed"]
            q["intonationScale"] = cfg["intonation"]
            q["pitchScale"] = cfg["pitch"]
            return q

        if not cfg["per_sentence"]:
            text = "\n".join(lines)
            q = query_for(text)
            wav = synth_bytes(q, style_id)
            if cfg.get("query_json_suffix"):
                (TEST_DIR / (args.prefix + cfg["query_json_suffix"])).write_text(
                    json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8"
                )
            (TEST_DIR / out_name).write_bytes(wav)
            rate, ch, sw = wav_info(wav)
            dur = _duration(wav, rate)
            manifest["files"][mode] = {
                "path": out_name,
                "duration_s": round(dur, 3),
                "speedScale": cfg["speed"],
                "intonationScale": cfg["intonation"],
                "pitchScale": cfg["pitch"],
                "audio_query_count": 1,
                "synthesis_count": 1,
                "channels": ch,
                "sample_rate": rate,
                "sample_width": sw,
            }
            print(f"{mode}: {out_name} dur={dur:.2f}s queries=1")
            continue

        # per-sentence mode (B and C)
        clips: list[bytes] = []
        parts: list[dict] = []
        rate, ch, sw = None, None, None
        for i, sentence in enumerate(lines):
            q = query_for(sentence)
            wav = synth_bytes(q, style_id)
            r, ch, sw = wav_info(wav)
            if rate is None:
                rate = r
            assert (r, ch, sw) == (rate, ch, sw), "format mismatch between sentences"
            clips.append(wav)
            parts.append({
                "sentence_index": i + 1,
                "text": sentence,
                "duration_s": round(_duration(wav, rate), 3),
                "tail_silence_s": round(tail_silence_seconds(wav, rate), 3),
            })
            print(f"{mode}: sentence {i+1}/{len(lines)} generated ({parts[-1]['duration_s']}s)")

        # concatenate, padding only when the engine's own tail pause is short
        import array, io
        out = array.array("h")
        padding_applied = 0
        for i, wav in enumerate(clips):
            w = wave.open(io.BytesIO(wav), "rb")
            out.extend(array.array("h", w.readframes(w.getnframes())))
            w.close()
            if i < len(clips) - 1:
                tail = parts[i]["tail_silence_s"]
                if tail < MIN_TAIL_SILENCE:
                    pad = int(rate * max(TARGET_GAP - tail, 0.0))
                    out.extend(array.array("h", b"\x00\x00" * pad))
                    padding_applied += 1
                    parts[i]["padded_gap_to"] = round(TARGET_GAP, 3)
        out_path = TEST_DIR / out_name
        with wave.open(str(out_path), "wb") as w:
            w.setnchannels(ch)
            w.setsampwidth(sw)
            w.setframerate(rate)
            w.writeframes(out.tobytes())
        dur = len(out) / rate
        manifest["files"][mode] = {
            "path": out_name,
            "duration_s": round(dur, 3),
            "speedScale": cfg["speed"],
            "intonationScale": cfg["intonation"],
            "pitchScale": cfg["pitch"],
            "audio_query_count": len(lines),
            "synthesis_count": len(lines),
            "channels": ch,
            "sample_rate": rate,
            "sample_width": sw,
            "sentences": parts,
            "padding_applied_after_sentence": padding_applied,
        }
        print(f"{mode}: {out_name} dur={dur:.2f}s queries={len(lines)} padding={padding_applied}")

    (TEST_DIR / (args.prefix + "manifest.json")).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("manifest:", TEST_DIR / (args.prefix + "manifest.json"))
    return 0


def _duration(wav_bytes: bytes, rate: int) -> float:
    import io, wave as wv
    w = wv.open(io.BytesIO(wav_bytes), "rb")
    try:
        return w.getnframes() / w.getframerate()
    finally:
        w.close()


if __name__ == "__main__":
    raise SystemExit(main())
