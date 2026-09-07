"""Full-episode 剣崎雌雄 narration material for episode 001 (draft_v9 text).

Source of truth: captions_v8.srt (the narration actually read in draft_v9,
CTA included) - each caption is one sentence, generated separately as
audio_query -> synthesis so any single sentence can be re-generated /
replaced later without touching the rest.

Settings (fixed for this adoption): speedScale 1.00, intonationScale 1.00,
pitchScale 0.00, speaker 剣崎雌雄 / ノーマル (resolved from /speakers).

Run:
  python scripts/tts_voicevox_kenzaki.py              # generate all + concat
  python scripts/tts_voicevox_kenzaki.py --limit 3    # smoke test
  python scripts/tts_voicevox_kenzaki.py --concat-only # rebuild review wav after
                                                       # replacing individual segment(s)

Does not touch video, captions, narration_v6.mp3, OpenAI TTS or drafts.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import shutil
import subprocess
import sys
import urllib.request
import wave
import array as _array
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from tts_voicevox import resolve_speaker, make_audio_query  # noqa: E402

ENGINE_URL = "http://127.0.0.1:50021"
SPEAKER_NAME = "剣崎雌雄"
STYLE_NAME = "ノーマル"

EP = ROOT / "episodes" / "001_google_security"
SRT = EP / "captions_v8.srt"
OUT_DIR = EP / "audio" / "voicevox_kenzaki"
SEG_DIR = OUT_DIR / "segments"
MANIFEST = OUT_DIR / "segments_manifest.csv"
REVIEW_WAV = OUT_DIR / "narration_kenzaki_review.wav"

SPEED = 1.00
INTONATION = 1.00
PITCH = 0.00

# First caption of each section: intro, 1..5, summary, CTA.
SECTION_STARTS = {1, 4, 18, 28, 44, 56, 68, 79}
# Sentences after which a slightly longer "comprehension pause" is wanted
# (注意点・重要説明の後): 13, 27, 35, 39, 43, 53, 64, 65, 66, 74
IMPORTANT_AFTER = {13, 27, 35, 39, 43, 53, 64, 65, 66, 74}
GAP_TARGET_NORMAL = 0.30    # seconds; only pads when the natural tail is short
GAP_TARGET_IMPORTANT = 0.50
GAP_TARGET_SECTION = 0.80
GAP_PAD_MIN_NORMAL = 0.20
GAP_PAD_MIN_IMPORTANT = 0.40
GAP_PAD_MIN_SECTION = 0.60
SILENCE_THRESHOLD = 100    # |sample| below this counts as silence (16-bit)


def parse_srt_sentences(srt_path: Path) -> list[str]:
    """Return caption texts in order; the caption index must equal its position."""
    sentences: list[str] = []
    current: int | None = None
    for raw in srt_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or "-->" in line:
            continue
        if line.isdigit():
            current = int(line)
            continue
        if current is None:
            continue
        if current != len(sentences) + 1:
            raise SystemExit(f"caption order broken at {current}")
        sentences.append(line)
    return sentences


def wav_metrics(wav_bytes: bytes) -> tuple[int, int, int, int, float, float]:
    """Return (rate, channels, sampwidth, frames, duration_sec, tail_silence_sec)."""
    w = wave.open(io.BytesIO(wav_bytes), "rb")
    try:
        rate, ch, sw, nf = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
        samples = _array.array("h", w.readframes(nf))
    finally:
        w.close()
    tail = 0
    for s in reversed(samples):
        if abs(s) < SILENCE_THRESHOLD:
            tail += 1
        else:
            break
    return rate, ch, sw, nf, nf / rate, tail / rate


def _read_samples(wav_bytes: bytes, nframes: int) -> _array.array:
    w = wave.open(io.BytesIO(wav_bytes), "rb")
    try:
        return _array.array("h", w.readframes(nframes))
    finally:
        w.close()


def peak_amplitude(wav_bytes: bytes) -> float:
    w = wave.open(io.BytesIO(wav_bytes), "rb")
    try:
        nf = w.getnframes()
        samples = _array.array("h", w.readframes(nf))
    finally:
        w.close()
    return max(abs(s) for s in samples) / 32768


def synth_segment(text: str, style_id: int) -> bytes:
    q = make_audio_query(ENGINE_URL, text, style_id)
    q["speedScale"] = SPEED
    q["intonationScale"] = INTONATION
    q["pitchScale"] = PITCH
    url = f"{ENGINE_URL}/synthesis?speaker={style_id}"
    req = urllib.request.Request(  # noqa: F821 - imported below
        url, data=json.dumps(q, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "audio/wav"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return resp.read()


def write_manifest(rows: list[dict]) -> None:
    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_manifest() -> list[dict]:
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def build_timeline(files: list[tuple[int, Path, bool]]) -> tuple[list[dict], list[float]]:
    """Measure segments, decide pads, return (rows, pads_after)."""
    rows: list[dict] = []
    pads: list[float] = []
    cursor = 0.0
    infos = []
    for seg_id, path, is_section in files:
        rate, ch, sw, nf, dur, tail = wav_metrics(path.read_bytes())
        infos.append((seg_id, path, is_section, dur, tail, rate, ch, sw, nf))
    for i, (seg_id, path, is_section, dur, tail, rate, ch, sw, nf) in enumerate(infos):
        is_section_start = seg_id in SECTION_STARTS
        row = {
            "segment_id": seg_id,
            "text": SENTENCES[seg_id - 1],
            "wav_path": str(path.relative_to(OUT_DIR)),
            "duration_sec": round(dur, 3),
            "speedScale": f"{SPEED:.2f}",
            "intonationScale": f"{INTONATION:.2f}",
            "pitchScale": f"{PITCH:.2f}",
            "status": "generated",
            "start_sec": f"{cursor:.3f}",
            "end_sec": f"{cursor + dur:.3f}",
            "section_start": "yes" if is_section_start else "",
            "pad_after_sec": "",
            "notes": "",
        }
        rows.append(row)
        pad = 0.0
        if i < len(infos) - 1:
            next_is_section = infos[i + 1][2]
            if next_is_section:
                target, min_pad = GAP_TARGET_SECTION, GAP_PAD_MIN_SECTION
            elif seg_id in IMPORTANT_AFTER:
                target, min_pad = GAP_TARGET_IMPORTANT, GAP_PAD_MIN_IMPORTANT
            else:
                target, min_pad = GAP_TARGET_NORMAL, GAP_PAD_MIN_NORMAL
            if tail < min_pad:
                pad = max(0.0, target - tail)
                rows[-1]["pad_after_sec"] = f"{pad:.3f}"
        pads.append(pad)
        cursor += dur + pad
    return rows, pads


def concat_review_wav(files: list[tuple[int, Path, bool]], pads: list[float], out_path: Path) -> float:
    out = _array.array("h")
    rate = ch = sw = 0
    for (seg_id, path, _is_section), pad in zip(files, pads):
        wav_bytes = path.read_bytes()
        r, c, s, nf, _dur, _tail = wav_metrics(wav_bytes)
        if rate == 0:
            rate, ch, sw = r, c, s
        assert (r, c, s) == (rate, ch, sw), "segment format mismatch"
        out.extend(_read_samples(wav_bytes, nf))
        if pad > 0:
            out.extend(_array.array("h", b"\x00\x00" * int(rate * pad)))
    with wave.open(str(out_path), "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(sw)
        w.setframerate(rate)
        w.writeframes(out.tobytes())
    return len(out) / rate


def make_mp3(wav_path: Path) -> Path | None:
    if shutil.which("ffmpeg") is None:
        return None
    mp3 = wav_path.with_suffix(".mp3")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(wav_path), "-b:a", "192k", str(mp3)],
        check=True,
    )
    return mp3


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--limit", type=int, help="only generate the first N segments (test)")
    parser.add_argument("--concat-only", action="store_true",
                        help="rebuild review wav + timeline from existing manifest (after manual segment replacement)")
    parser.add_argument("--out", type=Path, default=REVIEW_WAV,
                        help="output WAV path for --concat-only (default: narration_kenzaki_review.wav)")
    args = parser.parse_args()

    global SENTENCES
    SENTENCES = parse_srt_sentences(SRT)
    if args.concat_only:
        rows = read_manifest()
        files = [
            (int(r["segment_id"]), OUT_DIR / r["wav_path"], r.get("section_start") == "yes")
            for r in rows
        ]
        new_rows, pads = build_timeline(files)
        dur = concat_review_wav(files, pads, args.out)
        # preserve existing status/notes
        old = {int(r["segment_id"]): r for r in rows}
        for nr in new_rows:
            o = old.get(nr["segment_id"], {})
            nr["status"] = o.get("status", "generated")
            nr["notes"] = o.get("notes", "")
        write_manifest(new_rows)
        print(f"concat-only: {args.out.name} dur={dur:.2f}s")
        return 0

    speaker_uuid, style_id = resolve_speaker(ENGINE_URL, SPEAKER_NAME, STYLE_NAME)
    print(f"speaker={SPEAKER_NAME} style={STYLE_NAME} style_id={style_id} sentences={len(SENTENCES)}")
    SEG_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    files: list[tuple[int, Path, bool]] = []
    for i, text in enumerate(SENTENCES, 1):
        if args.limit and i > args.limit:
            break
        seg_id = i
        path = SEG_DIR / f"{seg_id:03d}.wav"
        wav_bytes = synth_segment(text, style_id)
        path.write_bytes(wav_bytes)
        dur = wave.open(io.BytesIO(wav_bytes), "rb").getnframes() / 24000
        peak = peak_amplitude(wav_bytes)
        files.append((seg_id, path, seg_id in SECTION_STARTS))
        print(f"{seg_id:03d}: {dur:6.2f}s peak={peak:.2f} {text[:34]}")

    rows, pads = build_timeline(files)
    # status flags: clipping or suspiciously short
    for i, (seg_id, path, _s) in enumerate(files):
        wav_bytes = path.read_bytes()
        peak = peak_amplitude(wav_bytes)
        dur = float(rows[i]["duration_sec"])
        if peak >= 0.98:
            rows[i]["status"] = "needs_review"
            rows[i]["notes"] = "peak near clipping"
        elif dur < 0.6:
            rows[i]["status"] = "needs_review"
            rows[i]["notes"] = "suspiciously short audio"
    write_manifest(rows)

    dur = concat_review_wav(files, pads, REVIEW_WAV)
    print(f"review wav: {REVIEW_WAV.relative_to(ROOT)} total={dur:.2f}s segments={len(files)}")
    mp3 = make_mp3(REVIEW_WAV)
    if mp3:
        print(f"mp3 (optional): {mp3.relative_to(ROOT)}")
    return 0


SENTENCES: list[str] = []


if __name__ == "__main__":
    raise SystemExit(main())
