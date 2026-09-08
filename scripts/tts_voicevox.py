"""Minimal VOICEVOX TTS wrapper for the 大人のデジタル安心室 channel.

Text -> resolve speaker/style by name -> audio_query -> (optional future
pronunciation overrides) -> synthesis -> WAV.

Dependencies: Python standard library only (urllib). No OpenAI TTS code is
touched; use this script only when the local VOICEVOX ENGINE is running
(default: http://127.0.0.1:50021).

Usage examples:
  python scripts/tts_voicevox.py --text-file episodes/001_google_security/audio/voicevox_test/suzumatsu_test_script.txt --output episodes/001_google_security/audio/voicevox_test/suzumatsu_baseline.wav --save-query episodes/001_google_security/audio/voicevox_test/suzumatsu_audio_query.json
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENGINE_URL = "http://127.0.0.1:50021"
DEFAULT_SPEAKER_NAME = "雀松朱司"
DEFAULT_STYLE_NAME = "ノーマル"
PRONUNCIATION_CONFIG = ROOT / "config" / "voicevox_pronunciation.yaml"

try:  # PyYAML is a project dependency; only needed when overrides exist.
    import yaml
except ImportError:  # pragma: no cover - environment without PyYAML
    yaml = None


def resolve_speaker(engine_url: str, speaker_name: str, style_name: str) -> tuple[str, int]:
    """Resolve (speaker_uuid, style_id) from the live /speakers list by name.

    Never hardcodes IDs: the engine output is the single source of truth.
    """
    with urllib.request.urlopen(f"{engine_url}/speakers", timeout=15) as resp:
        speakers = json.loads(resp.read().decode("utf-8"))
    for sp in speakers:
        if sp.get("name") != speaker_name:
            continue
        for st in sp.get("styles", []):
            if st.get("name") == style_name:
                return str(sp["speaker_uuid"]), int(st["id"])
        style_names = ", ".join(s.get("name", "?") for s in sp.get("styles", []))
        raise SystemExit(
            f"speaker '{speaker_name}' found but style '{style_name}' not in [{style_names}]"
        )
    raise SystemExit(f"speaker '{speaker_name}' not found in /speakers")


def make_audio_query(engine_url: str, text: str, style_id: int) -> dict:
    """POST /audio_query; keep default prosody (speed=1.0, pitch=0.0, ...)."""
    url = f"{engine_url}/audio_query?text={urllib.parse.quote(text)}&speaker={style_id}"
    req = urllib.request.Request(url, data=b"{}", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _yaml_scalar(value: str):
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    try:
        return int(value)
    except ValueError:
        return value


def _fallback_pronunciations(config_path: Path) -> list[dict]:
    """Parse the small project YAML subset when PyYAML is unavailable."""
    entries: list[dict] = []
    current: dict | None = None
    accent: dict | None = None
    for raw in config_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("- surface:"):
            if current:
                entries.append(current)
            current = {"surface": _yaml_scalar(line.split(":", 1)[1])}
            accent = None
            continue
        if current is None or not line or line.startswith("#"):
            continue
        if line.startswith("- kana:"):
            accent = {"kana": _yaml_scalar(line.split(":", 1)[1])}
            current.setdefault("accent_phrases", []).append(accent)
            continue
        match = re.match(r"([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if match:
            key, value = match.groups()
            if key == "accent_phrases" and not value:
                current[key] = []
                accent = None
                continue
            parsed = _yaml_scalar(value)
            if key == "accent" and accent is not None:
                accent[key] = parsed
            else:
                current[key] = parsed
    if current:
        entries.append(current)
    return entries


def _scope_matches(entry: dict, episode_id: str) -> bool:
    scope = str(entry.get("scope") or "")
    return not episode_id or not scope or episode_id in scope or "標準辞書" in scope


def _replace_accent_phrase_sequence(
    query: dict, reading: str, accent: int, occurrence: int = 0,
) -> bool:
    """Make one occurrence of a configured reading one accent phrase."""
    # Compare the concatenated VOICEVOX mora text rather than individual
    # Unicode characters.  This is important for compound moras such as
    # ``ディ`` in the reading of ``ID``.
    target = "".join(str(reading).replace(" ", "").split())
    phrases = query.get("accent_phrases") or []
    positions: list[tuple[int, int, str]] = []
    for phrase_index, phrase in enumerate(phrases):
        for mora_index, mora in enumerate(phrase.get("moras") or []):
            positions.append((phrase_index, mora_index, str(mora.get("text") or "")))
    if not target or len(target) > len(positions):
        return False
    match_start = -1
    match_end = -1
    match_count = 0
    for start in range(len(positions)):
        joined = ""
        for end in range(start, len(positions)):
            joined += positions[end][2]
            if not target.startswith(joined):
                break
            if joined == target:
                if match_count < occurrence:
                    match_count += 1
                    break
                match_start = start
                match_end = end
                break
        if match_start >= 0:
            break
    if match_start < 0:
        return False
    start_phrase, start_mora, _ = positions[match_start]
    end_phrase, end_mora, _ = positions[match_end]

    def clone_phrase(phrase: dict, moras: list[dict], phrase_accent: int | None = None) -> dict:
        result = copy.deepcopy(phrase)
        result["moras"] = moras
        if moras:
            original = int(result.get("accent") or 1)
            result["accent"] = max(1, min(len(moras), phrase_accent if phrase_accent is not None else original))
        else:
            result["accent"] = 1
        result["pause_mora"] = None
        result["is_interrogative"] = False
        return result

    rebuilt: list[dict] = []
    matched_phrase: dict | None = None
    for phrase_index, phrase in enumerate(phrases):
        moras = list(phrase.get("moras") or [])
        if phrase_index < start_phrase or phrase_index > end_phrase:
            rebuilt.append(phrase)
            continue
        first = start_mora if phrase_index == start_phrase else 0
        last = end_mora if phrase_index == end_phrase else len(moras) - 1
        prefix, suffix = moras[:first], moras[last + 1:]
        if prefix:
            rebuilt.append(clone_phrase(phrase, prefix))
        if phrase_index == start_phrase:
            matched_phrase = clone_phrase(phrase, moras[first:last + 1], int(accent))
            rebuilt.append(matched_phrase)
        elif matched_phrase is not None:
            matched_phrase["moras"].extend(moras[first:last + 1])
            if phrase_index == end_phrase:
                matched_phrase["accent"] = max(1, min(len(matched_phrase["moras"]), int(accent)))
        if suffix:
            remainder = clone_phrase(phrase, suffix, 1)
            if phrase_index == end_phrase:
                remainder["pause_mora"] = phrase.get("pause_mora")
                remainder["is_interrogative"] = phrase.get("is_interrogative", False)
            rebuilt.append(remainder)
        elif phrase_index == end_phrase and matched_phrase is not None:
            matched_phrase["pause_mora"] = phrase.get("pause_mora")
            matched_phrase["is_interrogative"] = phrase.get("is_interrogative", False)
    query["accent_phrases"] = rebuilt
    return True


def _accent_phrase_prefix(
    query: dict, reading: str, accent: int,
) -> bool:
    """Set the accent on the first phrase whose mora texts start with the reading.

    Unlike `_replace_accent_phrase_sequence`, the trailing moras stay inside the
    same phrase, so suffixes such as デス/コード/ノ keep a natural low start
    after the highlighted reading.  Used only when an entry opts in with
    `accent_on_phrase: true`.
    """
    # Compare the concatenated VOICEVOX mora text.  A kana reading can use
    # different Unicode boundaries from the engine (e.g. ア for 長音 and
    # シャ as one mora), so character-by-character matching would silently
    # miss otherwise valid compound-word overrides.
    target = "".join(str(reading).replace(" ", "").split())
    if not target:
        return False
    for phrase in query.get("accent_phrases", []):
        moras = [str(mora.get("text") or "") for mora in phrase.get("moras") or []]
        if not "".join(moras).startswith(target):
            continue
        phrase["accent"] = min(len(moras), max(1, int(accent)))
        return True
    return False


def apply_pronunciation_overrides(
    query: dict,
    config_path: Path = PRONUNCIATION_CONFIG,
    episode_id: str = "",
) -> bool:
    """Apply per-word reading/accent overrides from config/voicevox_pronunciation.yaml.

    Entries match accent phrases by surface text.  ``episode_id`` limits
    episode-scoped entries while retaining entries marked as 標準辞書.
    """
    if not config_path.exists():
        return False
    if yaml is None:
        overrides = _fallback_pronunciations(config_path)
    else:
        cfg = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        overrides = cfg.get("pronunciations") or []
    if not overrides:
        return False
    by_surface = {
        o["surface"]: o
        for o in overrides
        if o.get("surface") and _scope_matches(o, episode_id)
    }
    changed = False
    for accent_phrase in query.get("accent_phrases", []):
        surface = accent_phrase.get("text", "")
        if surface not in by_surface:
            continue
        ov = by_surface[surface]
        if "reading" in ov:
            accent_phrase["kana"] = ov["reading"]
        specs = ov.get("accent_phrases") or []
        if len(specs) == 1 and isinstance(specs[0], dict):
            if specs[0].get("kana"):
                accent_phrase["kana"] = specs[0]["kana"]
            if specs[0].get("accent") is not None:
                accent_phrase["accent"] = int(specs[0]["accent"])
        elif "accent" in ov:
            accent_phrase["accent"] = int(ov["accent"])
        changed = True

    # Current VOICEVOX versions expose no surface text on accent phrases, so
    # match configured kana across adjacent phrases (e.g. アップ｜ストアや).
    # A text_replacement entry may also carry an approved accent_phrases spec:
    # e-Tax is sent to the engine as イータックス, then receives the same
    # mora-level accent treatment as a normal accent_phrases entry.
    for ov in by_surface.values():
        specs = ov.get("accent_phrases") or []
        configured_reading = ""
        if len(specs) == 1 and isinstance(specs[0], dict):
            configured_reading = str(specs[0].get("kana") or "")
        configured_reading = configured_reading or str(ov.get("reading") or "")
        if not configured_reading:
            continue
        target_accent = int(specs[0].get("accent")) if specs and specs[0].get("accent") is not None else int(ov.get("accent") or 1)
        if ov.get("accent_on_phrase"):
            changed = _accent_phrase_prefix(query, configured_reading, target_accent) or changed
            continue
        occurrence = 0
        while _replace_accent_phrase_sequence(query, configured_reading, target_accent, occurrence):
            changed = True
            occurrence += 1
    return changed


def apply_segment_accent_overrides(query: dict, segment: dict | None) -> bool:
    """Apply explicit accent settings for one narration segment only.

    The manifest stores these under ``accent_overrides`` so a contextual phrase
    such as ``今だけ`` can be corrected without making the context-dependent
    word ``今`` a global dictionary entry.  Values use the same mora-indexed
    accent convention as VOICEVOX ``accent_phrases``.
    """
    if not isinstance(segment, dict):
        return False
    raw = segment.get("accent_overrides")
    if not isinstance(raw, dict):
        return False
    changed = False
    for _surface, spec in raw.items():
        if not isinstance(spec, dict):
            continue
        reading = str(spec.get("reading") or "")
        accent = spec.get("accent")
        if not reading or not isinstance(accent, int) or accent < 1:
            continue
        occurrence = 0
        while _replace_accent_phrase_sequence(query, reading, accent, occurrence):
            changed = True
            occurrence += 1
    return changed


def _config_bool(value: object) -> bool:
    return value is True or str(value).strip().lower() in {"1", "true", "yes", "on"}


def apply_pronunciation_pitch_patterns(
    query: dict,
    config_path: Path = PRONUNCIATION_CONFIG,
    episode_id: str = "",
) -> list[dict]:
    """Apply human-approved mora pitch shapes after VOICEVOX recalculation.

    ``/mora_data`` rebuilds pitch from the accent number, so explicit GUI-style
    tuning must run after that endpoint.  The current supported shape is
    ``low_high_plateau``: the first mora is lowered relative to the second,
    the second and all later moras in the approved reading share the same
    pitch, and an immediately following identical mora (for example the
    particle ``を`` rendered as ``オ`` after ``信用``) is aligned as well.
    """
    if not config_path.exists():
        return []
    if yaml is None:
        overrides = _fallback_pronunciations(config_path)
    else:
        cfg = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        overrides = cfg.get("pronunciations") or []
    results: list[dict] = []
    for override in overrides:
        if not isinstance(override, dict):
            continue
        if override.get("method") != "accent_phrases":
            continue
        if str(override.get("pitch_shape") or "") != "low_high_plateau":
            continue
        if not _scope_matches(override, episode_id):
            continue
        reading = str(override.get("reading") or "").replace(" ", "")
        target_text = "".join(reading.split())
        if not target_text:
            continue
        positions: list[tuple[int, int, str]] = []
        phrases = query.get("accent_phrases") or []
        for phrase_index, phrase in enumerate(phrases):
            for mora_index, mora in enumerate(phrase.get("moras") or []):
                positions.append((phrase_index, mora_index, str(mora.get("text") or "")))
        # Match by the engine's mora text, not Unicode characters. A single
        # Japanese mora can contain a small kana (キャ/シュ), so キャッシュ
        # is three engine moras rather than five Unicode characters.
        matches: list[tuple[int, int]] = []
        for start in range(len(positions)):
            joined = ""
            for end in range(start, len(positions)):
                joined += positions[end][2]
                if not target_text.startswith(joined):
                    break
                if joined == target_text:
                    matches.append((start, end))
                    break
        if not matches:
            continue
        try:
            low_delta = float(override.get("pitch_low_delta") or -0.45)
        except (TypeError, ValueError):
            low_delta = -0.45
        try:
            anchor_number = int(override.get("pitch_high_anchor_mora") or 2)
        except (TypeError, ValueError):
            anchor_number = 2
        equalize_following = _config_bool(override.get("pitch_equalize_following_same_mora"))
        for start, end in matches:
            target_mora_count = end - start + 1
            anchor_offset = max(1, min(target_mora_count - 1, anchor_number - 1))
            phrase_index, _mora_index, _ = positions[start]
            anchor_phrase, anchor_mora, _ = positions[start + anchor_offset]
            anchor_value = float(
                (phrases[anchor_phrase].get("moras") or [])[anchor_mora].get("pitch") or 0.0
            )
            if anchor_value <= 0.0:
                for candidate_offset in range(1, target_mora_count):
                    candidate_phrase, candidate_mora, _ = positions[start + candidate_offset]
                    candidate_value = float(
                        (phrases[candidate_phrase].get("moras") or [])[candidate_mora].get("pitch") or 0.0
                    )
                    if candidate_value > 0.0:
                        anchor_value = candidate_value
                        break
            if anchor_value <= 0.0:
                continue
            low_value = max(0.1, anchor_value + low_delta)
            for offset in range(target_mora_count):
                current_phrase, current_mora, _ = positions[start + offset]
                phrases[current_phrase]["moras"][current_mora]["pitch"] = (
                    low_value if offset == 0 else anchor_value
                )
            following_count = 0
            if equalize_following and target_text.endswith("オ"):
                next_index = end + 1
                while next_index < len(positions) and positions[next_index][2] == "オ":
                    previous_phrase, _previous_mora, _ = positions[end]
                    next_phrase, next_mora, _ = positions[next_index]
                    contiguous = (
                        next_phrase == previous_phrase
                        or (
                            next_phrase == previous_phrase + 1
                            and not (phrases[previous_phrase].get("pause_mora"))
                        )
                    )
                    if not contiguous:
                        break
                    phrases[next_phrase]["moras"][next_mora]["pitch"] = anchor_value
                    following_count += 1
                    end = next_index
                    next_index += 1
            results.append(
                {
                    "surface": str(override.get("surface") or ""),
                    "reading": reading,
                    "phrase_index": phrase_index,
                    "mora_count": target_mora_count,
                    "low_pitch": low_value,
                    "high_pitch": anchor_value,
                    "pattern": ["low"] + ["high"] * (target_mora_count - 1),
                    "following_same_mora_count": following_count,
                    "following_same_mora_pitch_delta": 0.0 if following_count else None,
                }
            )
    return results


def refresh_mora_data(engine_url: str, query: dict, style_id: int) -> None:
    """Recalculate mora lengths/pitches after an accent phrase edit."""
    phrases = query.get("accent_phrases") or []
    if not phrases:
        return
    url = f"{engine_url}/mora_data?speaker={style_id}"
    request = urllib.request.Request(
        url,
        data=json.dumps(phrases, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        refreshed = json.loads(response.read().decode("utf-8"))
    if not isinstance(refreshed, list) or len(refreshed) != len(phrases):
        raise ValueError("VOICEVOX /mora_data returned an invalid accent phrase list")
    query["accent_phrases"] = refreshed


def synthesize(engine_url: str, query: dict, style_id: int, out_path: Path) -> None:
    url = f"{engine_url}/synthesis?speaker={style_id}"
    data = json.dumps(query, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "audio/wav"},
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        wav = resp.read()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(wav)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--text-file", type=Path, help="UTF-8 text file to speak")
    parser.add_argument("--text", help="inline text to speak (alternative to --text-file)")
    parser.add_argument("--output", type=Path, required=True, help="output WAV path")
    parser.add_argument("--save-query", type=Path, help="also save the audio_query JSON")
    parser.add_argument("--speaker", default=DEFAULT_SPEAKER_NAME)
    parser.add_argument("--style", default=DEFAULT_STYLE_NAME)
    parser.add_argument("--engine-url", default=DEFAULT_ENGINE_URL)
    args = parser.parse_args()

    if args.text_file and args.text:
        parser.error("use either --text-file or --text, not both")
    if args.text_file:
        text = args.text_file.read_text(encoding="utf-8").strip()
    elif args.text:
        text = args.text.strip()
    else:
        parser.error("--text-file or --text is required")
    if not text:
        parser.error("text is empty")

    speaker_uuid, style_id = resolve_speaker(args.engine_url, args.speaker, args.style)
    print(f"speaker='{args.speaker}' style='{args.style}' style_id={style_id} chars={len(text)}")

    query = make_audio_query(args.engine_url, text, style_id)
    if apply_pronunciation_overrides(query):
        refresh_mora_data(args.engine_url, query, style_id)
    apply_pronunciation_pitch_patterns(query, episode_id="")
    if args.save_query:
        args.save_query.parent.mkdir(parents=True, exist_ok=True)
        args.save_query.write_text(
            json.dumps(query, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"saved query: {args.save_query}")

    synthesize(args.engine_url, query, style_id, args.output)
    print(f"saved wav:   {args.output} ({args.output.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (urllib.error.URLError, TimeoutError) as exc:
        print(
            f"VOICEVOX ENGINE connection failed ({DEFAULT_ENGINE_URL}): {exc}",
            file=sys.stderr,
        )
        print("Is VOICEVOX ENGINE running on 127.0.0.1:50021?", file=sys.stderr)
        raise SystemExit(1) from exc
