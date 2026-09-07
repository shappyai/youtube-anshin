"""Incremental VOICEVOX generation keyed by narration/reading/voice hashes."""
from __future__ import annotations

import array
import csv
import hashlib
import io
import json
import sys
import urllib.request
import wave
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from episode_io import load_pronunciation_entries  # noqa: E402
from tts_voicevox import (  # noqa: E402
    apply_pronunciation_overrides,
    apply_pronunciation_pitch_patterns,
    apply_segment_accent_overrides,
    make_audio_query,
    refresh_mora_data,
    resolve_speaker,
)
from voicevox_preflight import expected_reading  # noqa: E402

SPEAKER = "剣崎雌雄"
STYLE = "ノーマル"
SPEED = 1.00
INTONATION = 1.00
PITCH = 0.00


def _active_pronunciation_signature(
    text: str, entries: list[dict[str, Any]], episode_id: str,
) -> list[dict[str, Any]]:
    active: list[dict[str, Any]] = []
    for entry in entries:
        surface = str(entry.get("surface") or "")
        scope = str(entry.get("scope") or "")
        if not surface or surface not in text:
            continue
        if scope and episode_id not in scope and "標準辞書" not in scope:
            continue
        active.append(entry)
    return active


def segment_hash(
    segment: dict[str, Any], effective_text: str,
    pronunciation_entries: list[dict[str, Any]] | None = None,
    episode_id: str = "",
) -> str:
    payload = {
        "narration": segment.get("narration"),
        "effective_text": effective_text,
        "reading_overrides": segment.get("reading_overrides") or {},
        "pronunciation_dictionary": _active_pronunciation_signature(
            str(segment.get("spoken_text") or segment.get("narration") or ""),
            pronunciation_entries or [],
            episode_id,
        ),
        "speaker": SPEAKER, "style": STYLE, "speed": SPEED, "intonation": INTONATION, "pitch": PITCH,
    }
    # Keep hashes backward-compatible for existing segments.  A new optional
    # field only participates when it changes synthesis behavior, so adding a
    # display-only ``display_text`` does not regenerate an approved audio file.
    if segment.get("accent_overrides"):
        payload["accent_overrides"] = segment.get("accent_overrides")
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def legacy_segment_hash(segment: dict[str, Any], effective_text: str) -> str:
    """Return the pre-dictionary-signature hash for cache migration.

    Adding the active pronunciation dictionary to the cache key must not
    regenerate an otherwise unchanged WAV.  Existing segment state files may
    still contain this older hash, so the incremental gate accepts it once and
    writes the current hash back after successful reuse.
    """
    payload = {
        "narration": segment.get("narration"),
        "effective_text": effective_text,
        "reading_overrides": segment.get("reading_overrides") or {},
        "speaker": SPEAKER, "style": STYLE, "speed": SPEED, "intonation": INTONATION, "pitch": PITCH,
    }
    if segment.get("accent_overrides"):
        payload["accent_overrides"] = segment.get("accent_overrides")
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / wav.getframerate()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _resolve_human_override_path(value: Any, episode_dir: Path) -> Path:
    raw = str(value or "").strip()
    if not raw:
        raise ValueError("human_audio_override path is empty")
    path = Path(raw)
    return path.resolve() if path.is_absolute() else (episode_dir / path).resolve()


def load_human_audio_overrides(
    data: dict[str, Any], episode_dir: Path,
) -> dict[int, dict[str, Any]]:
    """Load and verify approved human WAVs before any automatic synthesis.

    Human overrides are intentionally resolved before the normal segment cache.
    A valid override always wins, including when ``--regen-segment`` names the
    same segment.  Hash and optional narration hash checks make accidental
    replacement or reuse of an unrelated human recording fail closed.
    """
    raw = data.get("human_audio_overrides") or data.get("human_audio_override") or []
    items: list[dict[str, Any]] = []
    if isinstance(raw, dict):
        for segment_id, value in raw.items():
            if not isinstance(value, dict):
                raise ValueError(f"human_audio_override {segment_id}: entry must be an object")
            item = dict(value)
            item.setdefault("segment_id", segment_id)
            items.append(item)
    elif isinstance(raw, list):
        items = [dict(value) for value in raw if isinstance(value, dict)]
    elif raw:
        raise ValueError("human_audio_overrides must be a list or object")

    overrides: dict[int, dict[str, Any]] = {}
    for item in items:
        try:
            segment_id = int(item["segment_id"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"human_audio_override has invalid segment_id: {item!r}") from exc
        if segment_id in overrides:
            raise ValueError(f"human_audio_override duplicated segment {segment_id:03d}")
        status = str(item.get("status") or "approved").lower()
        if status not in {"approved", "human_approved"}:
            raise ValueError(f"human_audio_override seg {segment_id:03d} is not approved")
        path = _resolve_human_override_path(item.get("path"), episode_dir)
        if not path.exists():
            raise FileNotFoundError(f"human_audio_override missing: {path}")
        actual_sha = sha256_file(path)
        declared_sha = str(item.get("sha256") or "").upper()
        if declared_sha and actual_sha != declared_sha:
            raise ValueError(
                f"human_audio_override seg {segment_id:03d} SHA mismatch: "
                f"declared={declared_sha} actual={actual_sha}"
            )
        overrides[segment_id] = {
            "path": path,
            "sha256": actual_sha,
            "narration_sha256": str(item.get("narration_sha256") or "").upper(),
            "source_path": str(item.get("source_path") or ""),
            "automatic_regeneration": False,
        }
    return overrides


def read_existing_manifest(path: Path) -> dict[int, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return {int(row["segment_id"]): row for row in csv.DictReader(handle) if row.get("segment_id", "").isdigit()}


def synthesize(
    engine_url: str,
    text: str,
    style_id: int,
    output: Path,
    episode_id: str = "",
    segment: dict[str, Any] | None = None,
) -> dict[str, Any]:
    # Priority is deliberate: approved human WAV > human-approved dictionary
    # reading/accent > ordinary VOICEVOX automatic generation.
    query = make_audio_query(engine_url, text, style_id)
    changed = apply_pronunciation_overrides(query, episode_id=episode_id)
    changed = apply_segment_accent_overrides(query, segment) or changed
    if changed:
        refresh_mora_data(engine_url, query, style_id)
    apply_pronunciation_pitch_patterns(query, episode_id=episode_id)
    query["speedScale"], query["intonationScale"], query["pitchScale"] = SPEED, INTONATION, PITCH
    request = urllib.request.Request(
        f"{engine_url}/synthesis?speaker={style_id}",
        data=json.dumps(query, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "audio/wav"},
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(response.read())
    return query


def concat_segments(rows: list[dict[str, Any]], output: Path) -> float:
    samples = array.array("h")
    rate = channels = sample_width = 0
    for row in rows:
        path = Path(row["wav_path"])
        with wave.open(str(path), "rb") as wav:
            current = (wav.getframerate(), wav.getnchannels(), wav.getsampwidth())
            if rate == 0:
                rate, channels, sample_width = current
            if current != (rate, channels, sample_width):
                raise ValueError(f"WAV format mismatch: {path}")
            samples.extend(array.array("h", wav.readframes(wav.getnframes())))
        pause = float(row["pause_after"])
        if pause > 0:
            samples.extend(array.array("h", b"\x00\x00" * int(rate * pause)))
    output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output), "wb") as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(sample_width)
        wav.setframerate(rate)
        wav.writeframes(samples.tobytes())
    return len(samples) / rate


def generate_incremental(
    data: dict[str, Any], episode_dir: Path, work_dir: Path, engine_url: str,
    force_segment: int | None = None, dry_run: bool = False, audio_dir: Path | None = None,
) -> dict[str, Any]:
    episode_id = str(data["episode"]["episode_id"])
    audio_dir = audio_dir or episode_dir / "audio" / "voicevox_kenzaki"
    segment_dir = audio_dir / "segments"
    state_path = work_dir / "voicevox_segment_state.json"
    old_state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {"segments": {}}
    legacy = read_existing_manifest(audio_dir / "segments_manifest.csv")
    entries = load_pronunciation_entries()
    human_overrides = load_human_audio_overrides(data, episode_dir)
    planned: list[int] = []
    skipped: list[int] = []
    human_override_ids: list[int] = []
    rows: list[dict[str, Any]] = []
    style_id: int | None = None
    cursor = 0.0
    new_state: dict[str, Any] = {"version": 1, "segments": {}}
    query_audit: dict[str, Any] = {}

    for segment in data.get("narration_segments", []):
        segment_id = int(segment["id"])
        # Human audio overrides are checked before this automatic path; within
        # the automatic path, expected_reading applies the approved dictionary
        # before synthesis and cache hashing records the active entries.
        effective, _approvals = expected_reading(segment, entries, episode_id)
        digest = segment_hash(segment, effective, entries, episode_id)
        legacy_digest = legacy_segment_hash(segment, effective)
        override = human_overrides.get(segment_id)
        if override:
            expected_narration_sha = override.get("narration_sha256")
            actual_narration_sha = hashlib.sha256(
                str(segment.get("narration") or "").encode("utf-8")
            ).hexdigest().upper()
            if expected_narration_sha and expected_narration_sha != actual_narration_sha:
                raise ValueError(
                    f"human_audio_override seg {segment_id:03d} narration SHA mismatch: "
                    f"declared={expected_narration_sha} actual={actual_narration_sha}"
                )
            path = Path(override["path"])
            duration = wav_duration(path)
            pause = float(segment.get("pause_after") or 0)
            rows.append({
                "segment_id": segment_id, "wav_path": str(path), "hash": digest,
                "wav_sha256": override["sha256"], "source": "human_audio_override",
                "start_sec": round(cursor, 3), "end_sec": round(cursor + duration, 3),
                "duration_sec": round(duration, 3), "pause_after": pause,
            })
            cursor += duration + pause
            new_state["segments"][str(segment_id)] = {
                "hash": digest, "wav_path": str(path),
                "source": "human_audio_override", "wav_sha256": override["sha256"],
            }
            query_audit[str(segment_id)] = {
                "source": "human_audio_override", "wav_path": str(path),
                "wav_sha256": override["sha256"], "automatic_regeneration": False,
            }
            human_override_ids.append(segment_id)
            continue
        path = segment_dir / f"{segment_id:03d}.wav"
        previous = old_state.get("segments", {}).get(str(segment_id), {})
        legacy_text = legacy.get(segment_id, {}).get("text", "")
        legacy_reuse = not previous and legacy_text == str(segment.get("narration") or "")
        reusable = path.exists() and (
            previous.get("hash") in {digest, legacy_digest} or legacy_reuse
        )
        if force_segment == segment_id:
            reusable = False
        if reusable:
            skipped.append(segment_id)
        else:
            planned.append(segment_id)
            if not dry_run:
                if style_id is None:
                    _uuid, style_id = resolve_speaker(engine_url, SPEAKER, STYLE)
                query_audit[str(segment_id)] = {
                    "effective_text": effective,
                    "query": synthesize(
                        engine_url, effective, style_id, path, episode_id, segment=segment
                    ),
                }
        if not path.exists():
            if dry_run:
                continue
            raise FileNotFoundError(path)
        duration = wav_duration(path)
        pause = float(segment.get("pause_after") or 0)
        rows.append({
            "segment_id": segment_id, "wav_path": str(path), "hash": digest,
            "start_sec": round(cursor, 3), "end_sec": round(cursor + duration, 3),
            "duration_sec": round(duration, 3), "pause_after": pause,
        })
        cursor += duration + pause
        new_state["segments"][str(segment_id)] = {"hash": digest, "wav_path": str(path)}

    if not dry_run and len(rows) == len(data.get("narration_segments", [])):
        work_dir.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(new_state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        timing_path = work_dir / "audio_timing.json"
        timing_path.write_text(json.dumps({"duration": round(cursor, 3), "segments": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        concat_segments(rows, audio_dir / "narration_kenzaki_auto.wav")
        (work_dir / "voicevox_query_audit.json").write_text(
            json.dumps(query_audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return {
        "status": "DRY_RUN" if dry_run else "PASS", "planned": planned,
        "skipped": skipped, "human_overrides": human_override_ids, "rows": rows,
        "duration": round(cursor, 3),
    }
