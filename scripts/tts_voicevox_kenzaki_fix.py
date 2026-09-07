"""Apply human-approved pronunciation fixes (2026-08-30) to 剣崎雌雄 segments.

Dictionary: config/voicevox_pronunciation.yaml
- text_replacement entries (開けます→ひらけます, セキュリティ→セキュリティー):
  applied to the sentence text BEFORE audio_query so the engine reads
  the kana naturally (no manual accent changes).
- accent_phrases entry (再設定用: サイ|セッテイ|ヨウ accent 2/4/1):
  structural surgery on the audio_query accent phrases, then
  /mora_length + /mora_pitch recompute (the same flow as VOICEVOX GUI
  accent editing).

Only segments containing these surfaces are regenerated. Parameters stay
speed 1.00 / intonation 1.00 / pitch 0.00. No full concat rebuild.
"""
from __future__ import annotations

import copy
import csv
import io
import json
import re
import sys
import urllib.parse
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
SPEED, INTONATION, PITCH = 1.00, 1.00, 0.00

EP = ROOT / "episodes" / "001_google_security"
OUT_DIR = EP / "audio" / "voicevox_kenzaki"
SEG_DIR = OUT_DIR / "segments"
MANIFEST = OUT_DIR / "segments_manifest.csv"
PRON_DIR = OUT_DIR / "pronunciation_test"
DICT_PATH = ROOT / "config" / "voicevox_pronunciation.yaml"

RESET_TEXT = "再設定用のメールアドレスを確認します。"
RESET_WAV = PRON_DIR / "reset_approved.wav"
RESET_QUERY_JSON = PRON_DIR / "saiseitteiyo_approved_query.json"
SAMPLE_QUERY_JSON = PRON_DIR / "segment_018_query.json"

def load_dictionary(path: Path) -> dict:
    """Minimal loader for config/voicevox_pronunciation.yaml (no PyYAML needed)."""
    text = path.read_text(encoding="utf-8")
    text_replacements: list[tuple[str, str]] = []
    accent_specs: dict[str, dict] = {}
    blocks = re.split(r"(?m)^  - surface:", text)
    for block in blocks[1:]:
        lines = block.splitlines()
        surface = lines[0].strip().strip('"').strip("'")
        rest = "\n".join(lines[1:])
        method_m = re.search(r"^    method:\s*(\w+)", rest, re.M)
        if not method_m:
            continue
        method = method_m.group(1)
        if method == "text_replacement":
            to_m = re.search(r'^    to:\s*"([^"]+)"', rest, re.M)
            if to_m:
                text_replacements.append((surface, to_m.group(1)))
        elif method == "accent_phrases":
            reading_m = re.search(r'^    reading:\s*"([^"]+)"', rest, re.M)
            phrases = re.findall(r"^\s*- kana:\s*\"([^\"]+)\"\s*$", rest, re.M)
            accents = re.findall(r"^\s+accent:\s*(\d+)", rest, re.M)
            spec = {
                "reading": reading_m.group(1) if reading_m else "",
                "phrases": list(zip(phrases, [int(a) for a in accents])),
            }
            if spec["phrases"]:
                accent_specs[surface] = spec
    return {"text_replacements": text_replacements, "accent_specs": accent_specs}


def synth_bytes(query: dict, speaker: int) -> bytes:
    url = f"{ENGINE_URL}/synthesis?speaker={speaker}"
    req = urllib.request.Request(
        url, data=json.dumps(query, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "audio/wav"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return resp.read()


def post_json(url: str, body) -> list:
    req = urllib.request.Request(
        url, data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def phrase_mora_texts(phrase: dict) -> list[str]:
    return [m["text"] for m in phrase["moras"]]


def accent_variants(reading: str) -> list[list[str]]:
    """Mora-text variants of a reading kana string.

    The engine's kana convention renders テイ as テエ and ヨウ as ヨオ,
    so every combination of those renderings is accepted.
    """
    base = list(reading)
    result = [base]
    for i in range(len(base) - 1):
        if base[i] == "テ" and base[i + 1] == "イ":
            for v in list(result):
                vv = list(v)
                vv[i + 1] = "エ"
                if vv not in result:
                    result.append(vv)
        if base[i] == "ヨ" and base[i + 1] == "ウ":
            for v in list(result):
                vv = list(v)
                vv[i + 1] = "オ"
                if vv not in result:
                    result.append(vv)
    return result


def split_accent_span(
    accent_phrases: list[dict], reading: str, phrases_spec: list[tuple[str, int]]
) -> list[dict]:
    """Split the reading's mora window into the given accent phrases (kana, accent)."""
    flat: list[dict] = []
    boundaries = [0]
    for p in accent_phrases:
        flat.extend(p["moras"])
        boundaries.append(len(flat))
    target = None
    k = len(accent_variants(reading)[0])
    for cand in accent_variants(reading):
        for start in boundaries[:-1]:
            if [m["text"] for m in flat[start : start + k]] == cand:
                target = (cand, start)
                break
        if target:
            break
    if not target:
        raise SystemExit(f"mora window not found in query: {reading}")
    cand, start = target
    end = start + k

    # compute last consumed phrase index
    last_phrase_idx = 0
    for i, b in enumerate(boundaries[1:]):
        if b - 1 >= end - 1:
            last_phrase_idx = i
            break
    last_phrase = accent_phrases[last_phrase_idx]
    # moras of the last consumed phrase that come after the window
    phrase_start = boundaries[last_phrase_idx]
    leftover = last_phrase["moras"][end - phrase_start :]

    new_phrases: list[dict] = []
    for kana, accent in phrases_spec:
        n = len(kana)
        moras = [copy.deepcopy(m) for m in flat[start : start + n]]
        start += n
        new_phrases.append({
            "moras": moras,
            "accent": accent,
            "pause_mora": None,
            "is_interrogative": False,
        })
    if leftover:
        new_phrases.append({
            "moras": [copy.deepcopy(m) for m in leftover],
            "accent": 1 if len(leftover) == 1 else last_phrase["accent"],
            "pause_mora": last_phrase.get("pause_mora"),
            "is_interrogative": last_phrase.get("is_interrogative", False),
        })
    else:
        new_phrases[-1]["pause_mora"] = last_phrase.get("pause_mora")
        new_phrases[-1]["is_interrogative"] = last_phrase.get("is_interrogative", False)

    result = accent_phrases[:last_phrase_idx] + new_phrases + accent_phrases[last_phrase_idx + 1 :]
    return result


def verify_accent_span(accent_phrases: list[dict], phrases_spec: list[tuple[str, int]]) -> bool:
    """Check for consecutive phrases with mora counts/accent values matching the spec."""
    seq = [(len(p["moras"]), p["accent"]) for p in accent_phrases]
    target = [(len(kana), accent) for kana, accent in phrases_spec]
    for i in range(len(seq) - len(target) + 1):
        if seq[i : i + len(target)] == target:
            return True
    return False


def build_query(text: str, speaker: int, accent_specs: dict) -> dict:
    q = make_audio_query(ENGINE_URL, text, speaker)
    q["speedScale"], q["intonationScale"], q["pitchScale"] = SPEED, INTONATION, PITCH
    if any(s in text for s in accent_specs):
        spec = accent_specs[next(s for s in accent_specs if s in text)]
        q["accent_phrases"] = split_accent_span(
            q["accent_phrases"], spec["reading"], spec["phrases"]
        )
        q["accent_phrases"] = post_json(f"{ENGINE_URL}/mora_length?speaker={speaker}", q["accent_phrases"])
        q["accent_phrases"] = post_json(f"{ENGINE_URL}/mora_pitch?speaker={speaker}", q["accent_phrases"])
    return q


def wav_duration(wav_bytes: bytes) -> float:
    w = wave.open(io.BytesIO(wav_bytes), "rb")
    try:
        dur = w.getnframes() / w.getframerate()
        nf = w.getnframes()
        samples = _array.array("h", w.readframes(nf))
    finally:
        w.close()
    peak = max((abs(s) for s in samples), default=0) / 32768
    return dur, peak


def query_kana(query: dict) -> str:
    return "".join(m["text"] for p in query["accent_phrases"] for m in p["moras"])


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", type=str, default="",
                        help="comma-separated segment ids to regenerate (default: all dictionary matches)")
    args = parser.parse_args()
    only = {int(x) for x in args.only.split(",") if x.strip()}

    speaker_uuid, style_id = resolve_speaker(ENGINE_URL, SPEAKER_NAME, STYLE_NAME)
    d = load_dictionary(DICT_PATH)
    replacements = d["text_replacements"]
    accent_specs = d["accent_specs"]
    print(f"dictionary: text_replacements={[s for s, _ in replacements]} accent={list(accent_specs)}")

    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    targets = {
        int(r["segment_id"]): r
        for r in rows
        if any(s in r["text"] for s, _ in replacements) or any(s in r["text"] for s in accent_specs)
    }
    if only:
        targets = {sid: r for sid, r in targets.items() if sid in only}
    print(f"target segments: {sorted(targets)}")
    if not targets:
        raise SystemExit("no target segments found")

    SEG_DIR.mkdir(parents=True, exist_ok=True)
    PRON_DIR.mkdir(parents=True, exist_ok=True)
    changed = []
    for seg_id in sorted(targets):
        row = targets[seg_id]
        orig_text = row["text"]
        hint = orig_text
        for surface, to in replacements:
            hint = hint.replace(surface, to)
        q = build_query(hint, style_id, accent_specs)
        wav = synth_bytes(q, style_id)
        path = SEG_DIR / f"{seg_id:03d}.wav"
        path.write_bytes(wav)
        dur, peak = wav_duration(wav)
        fixes = []
        if "開けます" in orig_text:
            fixes.append("ひらけます" if "ヒラケマス" in query_kana(q) else "NG:ヒラケマス")
        if "セキュリティ" in orig_text:
            fixes.append("セキュリティー" if "セキュリティイ" in query_kana(q) else "NG:セキュリティイ")
        if "Gmail" in orig_text:
            fixes.append("ジーメール" if "ジイメエル" in query_kana(q) else "NG:ジーメール")
        if "右上" in orig_text:
            fixes.append("みぎうえ" if "ミギウエ" in query_kana(q) else "NG:みぎうえ")
        if any(s in orig_text for s in accent_specs):
            spec = accent_specs[next(s for s in accent_specs if s in orig_text)]
            fixes.append(
                "再設定用OK" if verify_accent_span(q["accent_phrases"], spec["phrases"])
                else "NG:再設定用"
            )
        changed.append((seg_id, dur, peak, fixes))
        print(
            f"{seg_id:03d}: {dur:6.2f}s peak={peak:.2f} fixes={','.join(fixes)} "
            f"kana={query_kana(q)[:50]}..."
        )
        if seg_id == 18:
            (SAMPLE_QUERY_JSON).write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")

    # reset_approved.wav (same pipeline, approved accent)
    q = build_query(RESET_TEXT, style_id, accent_specs)
    wav = synth_bytes(q, style_id)
    RESET_WAV.write_bytes(wav)
    (RESET_QUERY_JSON).write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")
    dur, peak = wav_duration(wav)
    spec = accent_specs[next(s for s in accent_specs if s in RESET_TEXT)]
    ok = verify_accent_span(q["accent_phrases"], spec["phrases"])
    print(f"reset_approved.wav: {dur:.2f}s peak={peak:.2f} 再設定用={ok}")
    for p in q["accent_phrases"][:4]:
        print("   phrase:", "".join(phrase_mora_texts(p)), "accent=", p["accent"])

    # update manifest rows (duration/status/notes); start/end stay as-is
    # (timeline will be recomputed at the next full concat)
    by_id = {int(r["segment_id"]): r for r in rows}
    for seg_id, dur, peak, fixes in changed:
        r = by_id[seg_id]
        r["duration_sec"] = f"{dur:.3f}"
        r["status"] = "updated"
        r["notes"] = "regenerated 2026-08-30: " + "; ".join(fixes) + " (timeline next concat)"
    try:
        with MANIFEST.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print("manifest updated (duration/status/notes); start/end kept until next concat")
    except PermissionError:
        print(
            "WARNING: segments_manifest.csv is locked (open in Excel). "
            "Audio segments are updated; run restore_manifest_segment_status.py after closing Excel.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
