"""Generate pronunciation-review WAVs for a set of words (VOICEVOX 剣崎雌雄).

For each word a short, script-like sentence is synthesised so a human can
audition the reading in context. Also writes a manifest CSV and a single
concatenated review WAV.

No pronunciation overrides are applied: this script is for REVIEWING new
terms before anyone adds them to config/voicevox_pronunciation.yaml.

Usage:
  python scripts/tts_pronunciation_review.py --words local/pronunciation_review_words.json
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
import wave
from pathlib import Path
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from tts_voicevox import resolve_speaker, make_audio_query, synthesize  # noqa: E402

ENGINE_URL = "http://127.0.0.1:50021"
SPEAKER = "剣崎雌雄"
STYLE = "ノーマル"
DEFAULT_OUT = ROOT / "episodes" / "002_myna_app" / "audio" / "pronunciation_review"
GAP_SECONDS = 0.35


def phrase_kana(phrase: dict) -> str:
    """Rebuild a phrase's kana from its moras (VOICEVOX >= 0.24 omits
    phrase-level text/kana and keeps only mora-level kana)."""
    return "".join(m.get("text", "") or "" for m in phrase.get("moras", []))


def extract_reading(engine_url: str, style_id: int, surface: str) -> tuple[str, str]:
    """Speak the word alone and return (voicevox_reading, accent_summary).

    Reads are taken from a word-only audio_query so the manifest records the
    VOICEVOX kanji->kana decision per word (context sentence is in the WAV).
    """
    q = make_audio_query(engine_url, surface, style_id)
    phrases = q.get("accent_phrases", [])
    all_kana = "".join(phrase_kana(p) for p in phrases)
    accents = "｜".join(f"{phrase_kana(p)}({p.get('accent')})" for p in phrases)
    return all_kana, accents


def concat_wavs(paths: list[Path], out_path: Path, gap_s: float = GAP_SECONDS) -> None:
    frames = bytearray()
    params = None
    gap = None
    for p in paths:
        with wave.open(str(p), "rb") as w:
            if params is None:
                params = (w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes(), w.getcomptype(), w.getcompname())
                gap = b"\x00" * int(w.getframerate() * gap_s) * w.getnchannels() * w.getsampwidth()
            frames += w.readframes(w.getnframes())
        frames += gap
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), "wb") as w:
        w.setparams(params)
        w.writeframes(bytes(frames))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--words", type=Path, required=True, help="JSON: [{id, surface, example_text}]")
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    words = json.loads(args.words.read_text(encoding="utf-8"))
    style_id = resolve_speaker(ENGINE_URL, SPEAKER, STYLE)[1]
    args.out_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    wav_paths: list[Path] = []
    for w in words:
        wid = w["id"]
        surface = w["surface"]
        text = w["example_text"]
        query = make_audio_query(ENGINE_URL, text, style_id)
        reading, accent = extract_reading(ENGINE_URL, style_id, surface)
        out = args.out_dir / f"{wid}.wav"
        synthesize(ENGINE_URL, query, style_id, out)
        wav_paths.append(out)
        rows.append(
            {
                "id": wid,
                "surface": surface,
                "example_text": text,
                "voicevox_reading": reading,
                "accent_summary": accent,
                "wav_path": str(out.relative_to(ROOT)),
                "status": "human_review_pending",
            }
        )
        print(f"{wid}  {surface}  kana={reading}  ({accent})  -> {out.name}")

    all_wav = args.out_dir / "pronunciation_review_all.wav"
    concat_wavs(wav_paths, all_wav)
    print(f"concatenated: {all_wav} ({all_wav.stat().st_size} bytes)")

    manifest = args.out_dir / "pronunciation_manifest.csv"
    with manifest.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "surface",
                "example_text",
                "voicevox_reading",
                "accent_summary",
                "wav_path",
                "status",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"manifest: {manifest}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"VOICEVOX ENGINE connection failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
