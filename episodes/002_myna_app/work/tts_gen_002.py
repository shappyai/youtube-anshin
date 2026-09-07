"""Episode 002 main narration generation (VOICEVOX 剣崎雌雄, 1 sentence at a time).

Source of truth: script.md narration lines (each sentence = one TTS unit).
Human-approved dictionary (config/voicevox_pronunciation.yaml) is applied:
  - text_replacement entries: replaced before audio_query
  - accent_phrases entries (e.g. App Store -> アップストア accent 5):
    structural surgery + /mora_length + /mora_pitch recompute

Gap policy (001 adopted): 0.30s normal / 0.50s after important /
0.80s before section start; pads only when the natural tail is short.

Usage:
  python episodes/002_myna_app/work/tts_gen_002.py                # full run
  python episodes/002_myna_app/work/tts_gen_002.py --approved-appstore  # one WAV
"""
from __future__ import annotations

import argparse
import copy
import csv
import io
import json
import re
import sys
import urllib.request
import wave
import array as _array
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from tts_voicevox import resolve_speaker, make_audio_query  # noqa: E402

ENGINE_URL = "http://127.0.0.1:50021"
SPEAKER_NAME = "剣崎雌雄"
STYLE_NAME = "ノーマル"
SPEED, INTONATION, PITCH = 1.00, 1.00, 0.00

EP = ROOT / "episodes" / "002_myna_app"
SCRIPT = EP / "script.md"
OUT_DIR = EP / "audio" / "voicevox_kenzaki"
SEG_DIR = OUT_DIR / "segments"
MANIFEST = OUT_DIR / "segments_manifest.csv"
NARRATION_WAV = OUT_DIR / "narration_kenzaki.wav"
DICT_PATH = ROOT / "config" / "voicevox_pronunciation.yaml"
WORK = EP / "work"
SEGMENT_FIXES = WORK / "segment_fixes_002.json"

GAP_TARGET_NORMAL = 0.30
GAP_TARGET_IMPORTANT = 0.50
GAP_TARGET_SECTION = 0.80
GAP_PAD_MIN_NORMAL = 0.20
GAP_PAD_MIN_IMPORTANT = 0.40
GAP_PAD_MIN_SECTION = 0.60
SILENCE_THRESHOLD = 100

IMPORTANT_KEYWORDS = ("注意", "安心", "大事", "確認してください", "必要はありません",
                      "案内しています", "お願い", "まとめ", "一つです")


# ---------- script parsing ----------

def parse_script(path: Path) -> list[dict]:
    units: list[dict] = []
    section = "（はじめに）"
    shot = ""
    section_start = True
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("## "):
            header = line[3:].strip()
            if "pronunciation" in header.lower():
                break  # candidates list at the end of script.md is NOT narration
            section = re.sub(r"^[\d:]+", "", header).strip()
            section_start = True
            continue
        if line.startswith("#") or line.startswith("- "):
            continue
        m = re.match(r"^\[SHOT-([0-9A-Za-z]+)\]$", line)
        if m:
            shot = f"SHOT-{m.group(1)}"
            continue
        for sentence in split_sentences(line):
            units.append(
                {
                    "text": sentence,
                    "section": section,
                    "shot": shot,
                    "section_start": section_start,
                    "important": any(k in sentence for k in IMPORTANT_KEYWORDS),
                }
            )
            section_start = False
    return units


def split_sentences(line: str) -> list[str]:
    parts = re.split(r"(?<=[。！？])", line)
    return [p for p in (x.strip() for x in parts) if p]


# ---------- dictionary (ported from scripts/tts_voicevox_kenzaki_fix.py) ----------

def load_dictionary(path: Path) -> dict:
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


def post_json(url: str, body) -> list:
    req = urllib.request.Request(
        url, data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def accent_variants(reading: str) -> list[list[str]]:
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


def split_accent_span(accent_phrases: list[dict], reading: str, phrases_spec: list[tuple[str, int]]) -> list[dict]:
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
    # first consumed phrase: the phrase containing the window start
    first_phrase_idx = 0
    for i, b in enumerate(boundaries[:-1]):
        next_b = boundaries[i + 1]
        if b <= start < next_b:
            first_phrase_idx = i
            break
    last_phrase_idx = 0
    for i, b in enumerate(boundaries[1:]):
        if b - 1 >= end - 1:
            last_phrase_idx = i
            break
    last_phrase = accent_phrases[last_phrase_idx]
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
    return (
        accent_phrases[:first_phrase_idx]
        + new_phrases
        + accent_phrases[last_phrase_idx + 1 :]
    )


def verify_accent_span(accent_phrases: list[dict], phrases_spec: list[tuple[str, int]]) -> bool:
    seq = [(len(p["moras"]), p["accent"]) for p in accent_phrases]
    target = [(len(kana), accent) for kana, accent in phrases_spec]
    for i in range(len(seq) - len(target) + 1):
        if seq[i : i + len(target)] == target:
            return True
    return False


def query_kana(query: dict) -> str:
    return "".join(m["text"] for p in query["accent_phrases"] for m in p["moras"])


def build_query(text: str, speaker: int, d: dict) -> dict:
    q = make_audio_query(ENGINE_URL, text, speaker)
    q["speedScale"], q["intonationScale"], q["pitchScale"] = SPEED, INTONATION, PITCH
    for surface in d["accent_specs"]:
        if surface in text:
            spec = d["accent_specs"][surface]
            q["accent_phrases"] = split_accent_span(
                q["accent_phrases"], spec["reading"], spec["phrases"]
            )
            q["accent_phrases"] = post_json(
                f"{ENGINE_URL}/mora_length?speaker={speaker}", q["accent_phrases"]
            )
            q["accent_phrases"] = post_json(
                f"{ENGINE_URL}/mora_pitch?speaker={speaker}", q["accent_phrases"]
            )
    return q


def synth_bytes(query: dict, speaker: int) -> bytes:
    url = f"{ENGINE_URL}/synthesis?speaker={speaker}"
    req = urllib.request.Request(
        url, data=json.dumps(query, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "audio/wav"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return resp.read()


def wav_metrics(wav_bytes: bytes) -> tuple[int, int, int, int, float, float]:
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
    peak = max((abs(s) for s in samples), default=0) / 32768
    return rate, ch, sw, nf, nf / rate, tail / rate, peak


def concat_wavs(paths: list[Path], pads: list[float], out_path: Path) -> float:
    out = _array.array("h")
    rate = ch = sw = 0
    for path, pad in zip(paths, pads):
        r, c, s, nf, _d, _t, _p = wav_metrics(path.read_bytes())
        if rate == 0:
            rate, ch, sw = r, c, s
        assert (r, c, s) == (rate, ch, sw), "segment format mismatch"
        w = wave.open(str(path), "rb")
        try:
            out.extend(_array.array("h", w.readframes(nf)))
        finally:
            w.close()
        if pad > 0:
            out.extend(_array.array("h", b"\x00\x00" * int(rate * pad)))
    with wave.open(str(out_path), "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(sw)
        w.setframerate(rate)
        w.writeframes(out.tobytes())
    return len(out) / rate


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--approved-appstore", action="store_true",
                    help="regenerate 005_app_store_approved.wav only")
    ap.add_argument("--approved-after-kara", action="store_true",
                    help="generate after_kara_approved.wav only")
    ap.add_argument("--approved-hirakenai", action="store_true",
                    help="generate hirakenai_approved.wav only")
    ap.add_argument("--fix-segments", action="store_true",
                    help="regenerate only segments listed in segment_fixes_002.json "
                         "then rebuild timeline + concat")
    ap.add_argument("--only-segments", default="",
                    help="with --fix-segments, comma-separated segment ids to regenerate")
    ap.add_argument("--limit", type=int, default=0, help="generate only first N units (test)")
    args = ap.parse_args()

    speaker_uuid, style_id = resolve_speaker(ENGINE_URL, SPEAKER_NAME, STYLE_NAME)
    d = load_dictionary(DICT_PATH)
    print(f"dictionary: text_replacements={[s for s, _ in d['text_replacements']]} "
          f"accent={list(d['accent_specs'])}")

    if args.approved_appstore:
        text = "App Storeで提供元を確認します。"
        hint = text
        for surface, to in d["text_replacements"]:
            hint = hint.replace(surface, to)
        raw_q = make_audio_query(ENGINE_URL, hint, style_id)
        print("PRE-SURGERY phrases:")
        for p in raw_q["accent_phrases"]:
            print("   phrase:", "".join(m["text"] for m in p["moras"]), "accent=", p["accent"])
        q = build_query(hint, style_id, d)
        spec = d["accent_specs"]["App Store"]
        ok = verify_accent_span(q["accent_phrases"], spec["phrases"])
        wav = synth_bytes(q, style_id)
        out = EP / "audio" / "pronunciation_review" / "005_app_store_approved.wav"
        out.write_bytes(wav)
        dur, peak = wav_metrics(wav)[4], wav_metrics(wav)[6]
        print(f"005_app_store_approved.wav: {dur:.2f}s peak={peak:.2f} "
              f"appstore_ok={ok} kana={query_kana(q)}")
        for p in q["accent_phrases"][:6]:
            print("   phrase:", "".join(m["text"] for m in p["moras"]), "accent=", p["accent"])
        (WORK / "appstore_approved_query.json").write_text(
            json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return 0

    if args.approved_after_kara:
        text = "後からインストールしたアプリが優先されます。"
        hint = text
        for surface, to in d["text_replacements"]:
            hint = hint.replace(surface, to)
        q = build_query(hint, style_id, d)
        wav = synth_bytes(q, style_id)
        out = EP / "audio" / "pronunciation_review" / "after_kara_approved.wav"
        out.write_bytes(wav)
        (WORK / "after_kara_approved_query.json").write_text(
            json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        dur, peak = wav_metrics(wav)[4], wav_metrics(wav)[6]
        print(f"after_kara_approved.wav: {dur:.2f}s peak={peak:.2f} kana={query_kana(q)}")
        return 0

    if args.approved_hirakenai:
        text = "アップデート後に開けない人向けの確認です。"
        hint = text
        for surface, to in d["text_replacements"]:
            hint = hint.replace(surface, to)
        q = build_query(hint, style_id, d)
        wav = synth_bytes(q, style_id)
        out = EP / "audio" / "pronunciation_review" / "hirakenai_approved.wav"
        out.write_bytes(wav)
        (WORK / "hirakenai_approved_query.json").write_text(
            json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        dur, peak = wav_metrics(wav)[4], wav_metrics(wav)[6]
        print(f"hirakenai_approved.wav: {dur:.2f}s peak={peak:.2f} kana={query_kana(q)}")
        return 0

    if args.fix_segments:
        fixes = json.loads(SEGMENT_FIXES.read_text(encoding="utf-8"))
        with MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        by_id = {int(r["segment_id"]): r for r in rows}
        changed = []
        only = {int(x.strip()) for x in args.only_segments.split(",") if x.strip()}
        for sid_str, spec in sorted(fixes.items(), key=lambda kv: int(kv[0])):
            sid = int(sid_str)
            if only and sid not in only:
                continue
            row = by_id[sid]
            orig_text = row["text"]
            hint = orig_text
            for surface, to in d["text_replacements"]:
                hint = hint.replace(surface, to)
            for surface, to in spec.get("replace", []):
                hint = hint.replace(surface, to)
            if hint == orig_text:
                print(f"{sid:03d}: text unchanged - skipped")
                continue
            q = build_query(hint, style_id, d)
            wav_bytes = synth_bytes(q, style_id)
            path = SEG_DIR / f"{sid:03d}.wav"
            path.write_bytes(wav_bytes)
            (WORK / f"segment_{sid:03d}_query.json").write_text(
                json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            rate, ch, sw, nf, dur, tail, peak = wav_metrics(wav_bytes)
            old_dur = float(row["duration_sec"])
            row["duration_sec"] = f"{dur:.3f}"
            row["peak"] = f"{peak:.2f}"
            row["status"] = "updated"
            note = spec.get("desc", "")
            note += f" (old {old_dur:.3f}s -> new {dur:.3f}s, diff {dur - old_dur:+.3f}s; timeline recomputed)"
            row["notes"] = (row["notes"] + "; " if row["notes"] else "") + note
            changed.append((sid, orig_text, spec.get("desc", ""), str(path.relative_to(EP)), old_dur, dur))
            print(f"{sid:03d}: {old_dur:.3f}s -> {dur:.3f}s ({dur - old_dur:+.3f}s) {spec.get('desc','')} kana={query_kana(q)[:40]}")

        # rebuild full timeline from measured wavs
        cursor = 0.0
        for i, r in enumerate(rows):
            dur = float(r["duration_sec"])
            r["start_sec"] = f"{cursor:.3f}"
            cursor += dur
            r["end_sec"] = f"{cursor:.3f}"
            pad = 0.0
            if i < len(rows) - 1:
                nxt = rows[i + 1]
                if nxt["section_start"] == "yes":
                    target, min_pad = GAP_TARGET_SECTION, GAP_PAD_MIN_SECTION
                elif r["important_after"] == "yes":
                    target, min_pad = GAP_TARGET_IMPORTANT, GAP_PAD_MIN_IMPORTANT
                else:
                    target, min_pad = GAP_TARGET_NORMAL, GAP_PAD_MIN_NORMAL
                tail = wav_metrics((SEG_DIR / f"{int(r['segment_id']):03d}.wav").read_bytes())[5]
                if tail < min_pad:
                    pad = max(0.0, target - tail)
                r["pad_after_sec"] = f"{pad:.3f}"
            else:
                r["pad_after_sec"] = ""
            cursor += pad
        with MANIFEST.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        pads = [float(r["pad_after_sec"] or 0) for r in rows]
        paths = [SEG_DIR / f"{int(r['segment_id']):03d}.wav" for r in rows]
        total = concat_wavs(paths, pads, NARRATION_WAV)
        print(f"reconcat: narration_kenzaki.wav total={total:.3f}s")
        print("FIX REPORT (segment_id, 元文, 修正内容, 新WAV, old->new sec):")
        for sid, txt, desc, wav, old, new in changed:
            print(f"  {sid}: {txt[:45]}... | {desc} | {wav} | {old:.3f} -> {new:.3f}")
        return 0

    units = parse_script(SCRIPT)
    if args.limit:
        units = units[: args.limit]
    print(f"units={len(units)}")
    SEG_DIR.mkdir(parents=True, exist_ok=True)

    paths: list[Path] = []
    rows: list[dict] = []
    for i, u in enumerate(units, 1):
        seg_text = u["text"]
        hint = seg_text
        for surface, to in d["text_replacements"]:
            hint = hint.replace(surface, to)
        q = build_query(hint, style_id, d)
        wav_bytes = synth_bytes(q, style_id)
        path = SEG_DIR / f"{i:03d}.wav"
        path.write_bytes(wav_bytes)
        rate, ch, sw, nf, dur, tail, peak = wav_metrics(wav_bytes)
        notes = ""
        if "App Store" in seg_text:
            spec = d["accent_specs"]["App Store"]
            ok = verify_accent_span(q["accent_phrases"], spec["phrases"])
            notes = f"appstore_ok={ok} kana={query_kana(q)}"
        paths.append(path)
        rows.append({
            "segment_id": i,
            "text": seg_text,
            "wav_path": f"segments/{i:03d}.wav",
            "section": u["section"],
            "shot": u["shot"],
            "section_start": "yes" if u["section_start"] else "",
            "important_after": "yes" if u["important"] else "",
            "duration_sec": f"{dur:.3f}",
            "peak": f"{peak:.2f}",
            "notes": notes,
            "status": "generated",
        })
        print(f"{i:03d} [{u['shot']}] {dur:6.2f}s peak={peak:.2f} {notes} {seg_text[:32]}")

    # timeline with gaps
    cursor = 0.0
    for i, r in enumerate(rows):
        dur = float(r["duration_sec"])
        r["start_sec"] = f"{cursor:.3f}"
        cursor += dur
        r["end_sec"] = f"{cursor:.3f}"
        pad = 0.0
        if i < len(rows) - 1:
            nxt = rows[i + 1]
            if nxt["section_start"] == "yes":
                target, min_pad = GAP_TARGET_SECTION, GAP_PAD_MIN_SECTION
            elif r["important_after"] == "yes":
                target, min_pad = GAP_TARGET_IMPORTANT, GAP_PAD_MIN_IMPORTANT
            else:
                target, min_pad = GAP_TARGET_NORMAL, GAP_PAD_MIN_NORMAL
            tail = wav_metrics(paths[i].read_bytes())[5]
            if tail < min_pad:
                pad = max(0.0, target - tail)
            r["pad_after_sec"] = f"{pad:.3f}"
        else:
            r["pad_after_sec"] = ""
        cursor += pad

    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "segment_id", "text", "wav_path", "section", "shot",
                "section_start", "important_after", "duration_sec", "peak",
                "start_sec", "end_sec", "pad_after_sec", "notes", "status",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    pads = [float(r["pad_after_sec"] or 0) for r in rows]
    total = concat_wavs(paths, pads, NARRATION_WAV)
    print(f"narration: {NARRATION_WAV} total={total:.3f}s (video track length) units={len(rows)}")
    print(f"manifest: {MANIFEST}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"VOICEVOX ENGINE connection failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
