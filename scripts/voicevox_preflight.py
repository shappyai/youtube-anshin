"""Check VOICEVOX readings before synthesis without changing the dictionary."""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from episode_io import (
    PRONUNCIATION_PATH,
    dictionary_matches,
    find_context_terms,
    load_json,
    load_pronunciation_entries,
    replace_readings,
    segment_spoken_text,
    validate_episode,
)
from tts_voicevox import (  # noqa: E402
    apply_pronunciation_overrides,
    apply_pronunciation_pitch_patterns,
    apply_segment_accent_overrides,
    refresh_mora_data,
)

DEFAULT_ENGINE_URL = "http://127.0.0.1:50021"
DEFAULT_SPEAKER_NAME = "剣崎雌雄"
DEFAULT_STYLE_NAME = "ノーマル"


def query_audio(engine_url: str, text: str, speaker_id: int) -> dict[str, Any]:
    url = f"{engine_url}/audio_query?text={urllib.parse.quote(text)}&speaker={speaker_id}"
    request = urllib.request.Request(url, data=b"{}", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        value = json.loads(response.read().decode("utf-8"))
    return value if isinstance(value, dict) else {}


def resolve_speaker_id(engine_url: str, speaker_name: str, style_name: str) -> int:
    with urllib.request.urlopen(f"{engine_url}/speakers", timeout=15) as response:
        speakers = json.loads(response.read().decode("utf-8"))
    for speaker in speakers:
        if speaker.get("name") != speaker_name:
            continue
        for style in speaker.get("styles", []):
            if style.get("name") == style_name:
                return int(style["id"])
        names = ", ".join(str(style.get("name", "?")) for style in speaker.get("styles", []))
        raise ValueError(f"style '{style_name}' not found for speaker '{speaker_name}' ({names})")
    raise ValueError(f"speaker '{speaker_name}' not found")


def kana_from_query(query: dict[str, Any]) -> str:
    if query.get("kana"):
        return str(query["kana"])
    parts: list[str] = []
    for phrase in query.get("accent_phrases", []):
        if isinstance(phrase, dict):
            parts.append(str(phrase.get("kana") or ""))
    return "".join(parts)


def matching_dictionary_entry(
    text: str,
    surface: str,
    entries: list[dict[str, Any]],
    episode_id: str,
) -> dict[str, Any] | None:
    for entry in entries:
        if entry.get("surface") != surface:
            continue
        scope = str(entry.get("scope") or "")
        if scope and episode_id not in scope and "標準辞書" not in scope:
            continue
        return entry
    return None


def expected_reading(
    segment: dict[str, Any],
    entries: list[dict[str, Any]],
    episode_id: str,
) -> tuple[str, list[str]]:
    text = segment_spoken_text(segment)
    overrides = segment.get("reading_overrides") or {}
    effective = text
    approvals: list[str] = []
    for surface, reading in overrides.items():
        if surface in text:
            effective = replace_readings(effective, {str(surface): str(reading)})
            approvals.append(f"{surface} → {reading}（reading_overrides）")
    text_replacements: dict[str, str] = {}
    for entry in dictionary_matches(text, entries):
        surface = str(entry.get("surface"))
        if surface in overrides:
            continue
        active = matching_dictionary_entry(text, surface, entries, episode_id)
        if not active:
            continue
        target = active.get("to") or active.get("reading")
        if target:
            approvals.append(f"{surface} → {target}（pronunciation dictionary）")
            if active.get("pitch_shape"):
                approvals.append(
                    f"{surface} → {active['pitch_shape']}（pitch shape / mora QA対象）"
                )
            if active.get("method") == "text_replacement":
                # Apply all text replacements together.  ``replace_readings``
                # sorts surfaces by length, so an approved compound such as
                # 「セキュリティ キー」 wins over the reusable generic
                # 「セキュリティ」 rule and cannot be double-replaced.
                text_replacements[surface] = str(target)
    if text_replacements:
        effective = replace_readings(effective, text_replacements)
    for surface, spec in (segment.get("accent_overrides") or {}).items():
        if surface not in text or not isinstance(spec, dict):
            continue
        reading = str(spec.get("reading") or "")
        accent = spec.get("accent")
        if reading and isinstance(accent, int) and accent >= 1:
            approvals.append(f"{surface} → {reading} / accent={accent}（segment accent_overrides）")
    return effective, approvals


def prepared_query(
    engine_url: str,
    text: str,
    speaker_id: int,
    segment: dict[str, Any],
    episode_id: str,
) -> dict[str, Any]:
    """Query VOICEVOX and apply the same dictionary/segment edits as synthesis."""
    query = query_audio(engine_url, text, speaker_id)
    changed = apply_pronunciation_overrides(query, episode_id=episode_id)
    changed = apply_segment_accent_overrides(query, segment) or changed
    if changed:
        refresh_mora_data(engine_url, query, speaker_id)
    apply_pronunciation_pitch_patterns(query, episode_id=episode_id)
    return query


def _mora_window(query: dict[str, Any], target: str) -> dict[str, Any] | None:
    """Find one contiguous target reading in the engine's mora stream.

    Matching the concatenated mora text keeps this gate valid for VOICEVOX
    compound moras while still requiring the target to stay in one phrase.
    """
    target = "".join(str(target).replace(" ", "").split())
    for phrase_index, phrase in enumerate(query.get("accent_phrases") or []):
        moras = phrase.get("moras") or []
        for start in range(len(moras)):
            joined = ""
            for end in range(start, len(moras)):
                joined += str(moras[end].get("text") or "")
                if not target.startswith(joined):
                    break
                if joined == target:
                    return {
                        "phrase_index": phrase_index,
                        "start_mora": start,
                        "end_mora": end,
                        "moras": moras[start:end + 1],
                    }
    return None


def _query_window_summary(query: dict[str, Any], target: str) -> dict[str, Any]:
    """Return compact, JSON-safe evidence for a mora-level pronunciation gate."""
    window = _mora_window(query, target)
    if not window:
        return {
            "target": target,
            "found": False,
            "mora_texts": [],
            "mora_count": 0,
        }
    phrase = (query.get("accent_phrases") or [])[window["phrase_index"]]
    mora_rows = [
        {
            "text": str(mora.get("text") or ""),
            "vowel_length": round(float(mora.get("vowel_length") or 0.0), 6),
            "consonant_length": round(float(mora.get("consonant_length") or 0.0), 6),
            "pitch": round(float(mora.get("pitch") or 0.0), 6),
        }
        for mora in window["moras"]
    ]
    return {
        "target": target,
        "found": True,
        "phrase_index": window["phrase_index"],
        "start_mora": window["start_mora"],
        "end_mora": window["end_mora"],
        "mora_texts": [row["text"] for row in mora_rows],
        "mora_count": len(mora_rows),
        "moras": mora_rows,
        "phrase_accent": phrase.get("accent"),
        "is_interrogative": bool(phrase.get("is_interrogative")),
        "phrase_pause_mora": bool(phrase.get("pause_mora")),
    }


def _following_same_phrase_mora(query: dict[str, Any], summary: dict[str, Any]) -> str:
    if not summary.get("found"):
        return ""
    phrase = (query.get("accent_phrases") or [])[int(summary["phrase_index"])]
    next_index = int(summary["end_mora"]) + 1
    moras = phrase.get("moras") or []
    if next_index >= len(moras):
        return ""
    return str(moras[next_index].get("text") or "")


def contextual_pronunciation_audio_gate(
    segments: list[dict[str, Any]],
    query_details: dict[int, dict[str, Any]],
    engine_url: str,
    speaker_id: int | None,
    episode_id: str,
) -> dict[str, Any]:
    """Regression-check contextual audio, beyond dictionary reading alone.

    A dictionary entry proves only the intended reading.  This gate checks the
    actual prepared audio_query for question phrases, particle/auxiliary
    contexts, vowel-final words, words prone to elongation, and pitch-modified
    words.  Episode012's two human-marked contexts are included as explicit
    real-sentence checks; the generic 本物 scan covers every occurrence.
    """
    result: dict[str, Any] = {
        "rule": "contextual_pronunciation_audio_gate",
        "dictionary_reading_alone_is_not_pass": True,
        "status": "REVIEW",
        "honmono": {},
        "question_direct_query": {},
        "etax": {},
        "failures": [],
    }
    if speaker_id is None:
        result["failures"].append("VOICEVOX style id is unavailable")
        return result

    honmono_segments = [
        segment for segment in segments
        if "本物" in segment_spoken_text(segment)
    ]
    for segment in honmono_segments:
        segment_id = int(segment["id"])
        query = query_details.get(segment_id)
        item: dict[str, Any] = {"segment_id": segment_id}
        if query is None:
            item["status"] = "REVIEW"
            item["failure"] = "prepared audio_query is missing"
            result["failures"].append(f"seg {segment_id:03d}: 本物 query missing")
            result["honmono"][str(segment_id)] = item
            continue
        summary = _query_window_summary(query, "ホンモノ")
        item.update(summary)
        next_mora = _following_same_phrase_mora(query, summary)
        item["following_same_phrase_mora"] = next_mora
        item["extra_vowel_after_honmono"] = int(next_mora in {"オ", "ー"})
        item["exact_four_mora"] = bool(
            summary.get("found")
            and summary.get("mora_count") == 4
            and summary.get("mora_texts") == ["ホ", "ン", "モ", "ノ"]
        )
        item["status"] = "PASS" if item["exact_four_mora"] and not item["extra_vowel_after_honmono"] else "REVIEW"
        if not item["exact_four_mora"]:
            result["failures"].append(f"seg {segment_id:03d}: 本物 is not exactly ホ/ン/モ/ノ")
        if item["extra_vowel_after_honmono"]:
            result["failures"].append(f"seg {segment_id:03d}: 本物 has an extra vowel mora")
        if segment_id == 30:
            item["question_intonation_via_pitch"] = bool(summary.get("is_interrogative"))
            final_vowel = 0.0
            if summary.get("moras"):
                final_vowel = float(summary["moras"][-1].get("vowel_length") or 0.0)
            item["final_mora_vowel_length"] = round(final_vowel, 6)
            item["final_vowel_length_max_sec"] = 0.22
            item["no_unnatural_final_vowel_elongation"] = final_vowel <= 0.22
            item["status"] = "PASS" if (
                item["status"] == "PASS"
                and item["question_intonation_via_pitch"]
                and item["no_unnatural_final_vowel_elongation"]
            ) else "REVIEW"
            if not item["question_intonation_via_pitch"]:
                result["failures"].append("seg 030: question intonation flag is missing")
            if not item["no_unnatural_final_vowel_elongation"]:
                result["failures"].append("seg 030: final vowel is longer than the contextual gate")
        result["honmono"][str(segment_id)] = item

    # The exact user-marked question is queried independently from the longer
    # narration segment so the gate cannot pass on a dictionary-only assertion.
    try:
        direct_question = query_audio(engine_url, "これ、本物？", speaker_id)
        direct_summary = _query_window_summary(direct_question, "ホンモノ")
        direct_next = _following_same_phrase_mora(direct_question, direct_summary)
        direct_final_vowel = float((direct_summary.get("moras") or [{}])[-1].get("vowel_length") or 0.0)
        result["question_direct_query"] = {
            "text": "これ、本物？",
            "query_method": "direct /audio_query",
            "summary": direct_summary,
            "following_same_phrase_mora": direct_next,
            "extra_vowel_after_honmono": int(direct_next in {"オ", "ー"}),
            "exact_four_mora": direct_summary.get("mora_texts") == ["ホ", "ン", "モ", "ノ"],
            "is_interrogative": bool(direct_summary.get("is_interrogative")),
            "final_mora_vowel_length": round(direct_final_vowel, 6),
            "no_unnatural_final_vowel_elongation": direct_final_vowel <= 0.22,
        }
        if not result["question_direct_query"]["exact_four_mora"]:
            result["failures"].append("direct これ、本物？ query is not exactly ホ/ン/モ/ノ")
        if result["question_direct_query"]["extra_vowel_after_honmono"]:
            result["failures"].append("direct これ、本物？ query has an extra vowel mora")
        if not result["question_direct_query"]["is_interrogative"]:
            result["failures"].append("direct これ、本物？ query is not interrogative")
        if not result["question_direct_query"]["no_unnatural_final_vowel_elongation"]:
            result["failures"].append("direct これ、本物？ final vowel is too long")
    except (OSError, ValueError, KeyError, urllib.error.URLError, TimeoutError) as exc:
        result["failures"].append(f"direct これ、本物？ query failed: {exc}")

    etax_segment = next(
        (segment for segment in segments if "e-Tax" in segment_spoken_text(segment)),
        None,
    )
    if etax_segment is None:
        # This regression check is conditional: an episode that does not
        # narrate e-Tax should not inherit an unrelated REVIEW failure.
        result["etax"] = {
            "status": "N/A",
            "reason": "episode has no e-Tax narration segment",
        }
    else:
        etax_id = int(etax_segment["id"])
        etax_query = query_details.get(etax_id)
        etax_item: dict[str, Any] = {"segment_id": etax_id}
        if etax_query is None:
            etax_item["status"] = "REVIEW"
            etax_item["failure"] = "prepared audio_query is missing"
            result["failures"].append(f"seg {etax_id:03d}: e-Tax query missing")
        else:
            summary = _query_window_summary(etax_query, "イイタックス")
            etax_item.update(summary)
            moras = summary.get("moras") or []
            voiced = [row for row in moras if float(row.get("pitch") or 0.0) > 0.0]
            peak_index = max(range(len(moras)), key=lambda index: float(moras[index].get("pitch") or 0.0)) if moras else -1
            etax_item["accent_is_3"] = summary.get("phrase_accent") == 3
            etax_item["accent_peak_mora"] = moras[peak_index].get("text") if peak_index >= 0 else ""
            etax_item["accent_peak_is_ta"] = etax_item["accent_peak_mora"] == "タ"
            etax_item["internal_pause"] = 0 if summary.get("found") and summary.get("mora_count") == 6 else 1
            s_length = float(moras[-1].get("vowel_length") or 0.0) if moras else 1.0
            etax_item["su_vowel_length"] = round(s_length, 6)
            etax_item["su_vowel_length_max_sec"] = 0.10
            etax_item["su_not_unnaturally_long"] = s_length <= 0.10
            etax_item["status"] = "PASS" if all([
                summary.get("found"),
                summary.get("mora_texts") == ["イ", "イ", "タ", "ッ", "ク", "ス"],
                etax_item["accent_is_3"],
                etax_item["accent_peak_is_ta"],
                etax_item["internal_pause"] == 0,
                etax_item["su_not_unnaturally_long"],
            ]) else "REVIEW"
            if etax_item["status"] != "PASS":
                result["failures"].append(f"seg {etax_id:03d}: e-Tax contextual audio gate failed")
        result["etax"]["prepared_query"] = etax_item
        try:
            direct_etax = query_audio(engine_url, "e-Taxのメールも、", speaker_id)
            direct_effective = prepared_query(
                engine_url,
                "イータックスのメールも、",
                speaker_id,
                {"narration": "e-Taxのメールも、", "reading_overrides": {}, "accent_overrides": {}},
                episode_id,
            )
            result["etax"]["direct_query"] = {
                "text": "e-Taxのメールも、",
                "effective_text": "イータックスのメールも、",
                "query_method": "direct /audio_query (original and dictionary-effective input)",
                "original_summary": _query_window_summary(direct_etax, "イイタックス"),
                "effective_summary": _query_window_summary(direct_effective, "イイタックス"),
                "status": "PASS" if _query_window_summary(direct_effective, "イイタックス").get("mora_texts") == ["イ", "イ", "タ", "ッ", "ク", "ス"] else "REVIEW",
            }
            if result["etax"]["direct_query"]["status"] != "PASS":
                result["failures"].append("direct e-Tax dictionary-effective query is not イ/イ/タ/ッ/ク/ス")
        except (OSError, ValueError, KeyError, urllib.error.URLError, TimeoutError) as exc:
            result["etax"]["direct_query"] = {
                "text": "e-Taxのメールも、",
                "query_method": "direct /audio_query",
                "error": str(exc),
            }
            result["failures"].append(f"direct e-Tax query failed: {exc}")

    result["status"] = "PASS" if not result["failures"] else "REVIEW"
    return result


def context_term_is_overridden(term: str, overrides: dict[str, Any]) -> bool:
    if term in overrides:
        return True
    contextual_variants = {
        "開く/開ける": {"開く", "開ける", "開いて", "開かなく", "開け直す"},
    }
    allowed = contextual_variants.get(term, set())
    return any(surface in allowed for surface in overrides)


def human_context_approval_map(data: dict[str, Any]) -> dict[tuple[int, str], dict[str, Any]]:
    """Return episode-local human approvals without changing TTS input.

    These approvals are deliberately separate from the shared pronunciation
    dictionary and from human audio overrides.  They only close the REVIEW
    gate for the exact episode/segment/term that a person listened to.
    """
    result: dict[tuple[int, str], dict[str, Any]] = {}
    raw = data.get("pronunciation_human_approvals") or []
    if not isinstance(raw, list):
        return result
    for item in raw:
        if not isinstance(item, dict):
            continue
        if str(item.get("status") or "").upper() != "HUMAN_APPROVED":
            continue
        try:
            segment_id = int(item["segment_id"])
        except (KeyError, TypeError, ValueError):
            continue
        term = str(item.get("term") or "").strip()
        if term:
            result[(segment_id, term)] = item
    return result


def run_preflight(
    episode_path: Path,
    report_path: Path,
    engine_url: str = DEFAULT_ENGINE_URL,
    speaker_id: int | None = None,
    offline: bool = False,
    limit: int | None = None,
    speaker_name: str = DEFAULT_SPEAKER_NAME,
    style_name: str = DEFAULT_STYLE_NAME,
) -> dict[str, Any]:
    data = load_json(episode_path)
    schema_issues = validate_episode(data)
    if schema_issues:
        raise SystemExit("episode.json validation failed:\n- " + "\n- ".join(schema_issues))
    episode_id = str(data["episode"]["episode_id"])
    entries = load_pronunciation_entries()
    segments = data.get("narration_segments", [])
    human_approvals = human_context_approval_map(data)
    if limit:
        segments = segments[:limit]

    engine_ok = False
    engine_error = ""
    query_count = 0
    query_readings: dict[int, str] = {}
    query_details: dict[int, dict[str, Any]] = {}
    resolved_speaker_id = speaker_id
    if not offline and segments:
        try:
            if resolved_speaker_id is None:
                resolved_speaker_id = resolve_speaker_id(engine_url, speaker_name, style_name)
            first, _first_approvals = expected_reading(segments[0], entries, episode_id)
            first_query = prepared_query(engine_url, first, resolved_speaker_id, segments[0], episode_id)
            query_readings[int(segments[0]["id"])] = kana_from_query(first_query)
            query_details[int(segments[0]["id"])] = first_query
            query_count = 1
            engine_ok = True
        except (OSError, ValueError, KeyError, urllib.error.URLError, TimeoutError) as exc:
            engine_error = str(exc)
    if engine_ok:
        for segment in segments[1:]:
            try:
                segment_id = int(segment["id"])
                effective_text, _segment_approvals = expected_reading(segment, entries, episode_id)
                segment_query = prepared_query(
                    engine_url, effective_text, resolved_speaker_id, segment, episode_id
                )
                query_readings[segment_id] = kana_from_query(segment_query)
                query_details[segment_id] = segment_query
                query_count += 1
            except (OSError, ValueError, KeyError, urllib.error.URLError, TimeoutError) as exc:
                engine_error = str(exc)
                engine_ok = False
                break

    approvals: list[dict[str, Any]] = []
    reviews: list[dict[str, Any]] = []
    seen_approvals: set[tuple[int, str]] = set()
    for segment in segments:
        segment_id = int(segment["id"])
        text = segment_spoken_text(segment)
        _effective_text, segment_approvals = expected_reading(segment, entries, episode_id)
        for approval in segment_approvals:
            key = (segment_id, approval)
            if key not in seen_approvals:
                approvals.append({"segment_id": segment_id, "text": approval})
                seen_approvals.add(key)

        overrides = segment.get("reading_overrides") or {}
        accent_overrides = segment.get("accent_overrides") or {}
        terms = find_context_terms(text)
        for term in terms:
            if context_term_is_overridden(term, overrides) or term in accent_overrides:
                continue
            if any(str(surface) != term and term in str(surface) for surface in accent_overrides):
                continue
            if (segment_id, term) in human_approvals:
                approvals.append(
                    {
                        "segment_id": segment_id,
                        "text": f"{term}（human context approval）",
                    }
                )
                continue
            entry = matching_dictionary_entry(text, term, entries, episode_id)
            if entry and (entry.get("to") or entry.get("reading")):
                continue
            # A context-term regex can match a component of an already
            # approved compound surface, such as 上 inside 右上.  The
            # compound's dictionary replacement is the actual TTS input, so
            # do not report the component as an additional unresolved term.
            covered_by_dictionary = False
            for dictionary_entry in dictionary_matches(text, entries):
                surface = str(dictionary_entry.get("surface") or "")
                if not surface or surface == term or term not in surface:
                    continue
                active = matching_dictionary_entry(text, surface, entries, episode_id)
                if active and (active.get("to") or active.get("reading")):
                    covered_by_dictionary = True
                    break
            if covered_by_dictionary:
                continue
            reviews.append(
                {
                    "segment_id": segment_id,
                    "term": term,
                    "context": text,
                    "engine_reading": query_readings.get(segment_id, ""),
                }
            )

    contextual_gate = {
        "rule": "contextual_pronunciation_audio_gate",
        "status": "REVIEW",
        "failures": ["VOICEVOX /audio_query was not completed"],
    }
    if engine_ok:
        contextual_gate = contextual_pronunciation_audio_gate(
            segments,
            query_details,
            engine_url,
            resolved_speaker_id,
            episode_id,
        )
    if contextual_gate.get("status") != "PASS":
        reviews.insert(
            0,
            {
                "segment_id": 30,
                "term": "contextual_pronunciation_audio_gate",
                "context": "辞書の読みだけでなく、実際の文脈audio_queryのモーラ・ピッチ・母音長を確認する回帰ゲート。",
                "engine_reading": "; ".join(str(item) for item in contextual_gate.get("failures", [])),
            },
        )

    if not offline and not engine_ok:
        reviews.insert(
            0,
            {
                "segment_id": None,
                "term": "VOICEVOX /audio_query",
                "context": "エンジンへ接続できなかったため、読みの自動取得を完了できませんでした。",
                "engine_reading": "",
            },
        )

    status = "PASS" if not reviews else "REVIEW"
    report_lines = [
        "# VOICEVOX pronunciation preflight",
        "",
        f"Episode: {episode_path.parent.name}",
        f"Engine: {'PASS' if engine_ok else 'REVIEW (offline)' if offline else 'REVIEW (unavailable)'}",
        f"Speaker: {speaker_name} / {style_name}"
        + (f" (style_id={resolved_speaker_id})" if resolved_speaker_id is not None else ""),
        f"Query count: {query_count}/{len(segments)}",
        f"Dictionary: {PRONUNCIATION_PATH.relative_to(PRONUNCIATION_PATH.parents[1])}",
        "",
        "自動で pronunciation dictionary は変更していません。",
        "",
        "## PASS",
        "",
    ]
    if approvals:
        report_lines.extend(f"- seg {item['segment_id']:03d} {item['text']}" for item in approvals)
    else:
        report_lines.append("- 承認済みの辞書・segment単位指定はありません。")
    report_lines.extend(["", "## REVIEW", ""])
    if reviews:
        for item in reviews:
            segment_id = item["segment_id"]
            prefix = f"seg {segment_id:03d} " if isinstance(segment_id, int) else ""
            reading = f" / engine: {item['engine_reading']}" if item["engine_reading"] else ""
            report_lines.append(f"- {prefix}{item['term']}{reading}")
            report_lines.append(f"  context: {item['context']}")
    else:
        report_lines.append("- なし")
    if engine_error:
        report_lines.extend(["", f"Engine detail: {engine_error}"])
    report_lines.extend(
        [
            "",
            "## contextual_pronunciation_audio_gate",
            "",
            "辞書の読みが登録済みでも、文脈ごとの実音声audio_queryを別ゲートで確認する。",
            f"- result: {contextual_gate.get('status', 'REVIEW')}",
            f"- 本物 regression segments: {len(contextual_gate.get('honmono', {}))}",
            f"- 本物？ direct query: {'PASS' if contextual_gate.get('question_direct_query', {}).get('exact_four_mora') else 'REVIEW'}",
            f"- e-Tax direct query: {contextual_gate.get('etax', {}).get('direct_query', {}).get('status', 'REVIEW')}",
        ]
    )
    for failure in contextual_gate.get("failures", []):
        report_lines.append(f"- failure: {failure}")
    report_lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- result: {status}",
            f"- approved matches: {len(approvals)}",
            f"- human-approved context items: {len(human_approvals)}",
            f"- review items: {len(reviews)}",
            "- dictionary mutation: none",
        ]
    )
    if human_approvals:
        phase_a = data.get("phase_a") if isinstance(data.get("phase_a"), dict) else {}
        report_lines.extend(
            [
                "",
                "## Human approval",
                "",
                f"- result: HUMAN_APPROVED ({len(human_approvals)} context-specific items)",
                f"- approval record: {phase_a.get('pronunciation_human_approval_record', 'not recorded')}",
                f"- review pack: {phase_a.get('pronunciation_review_pack_audio', 'not recorded')}",
                "- audio regenerated: 0",
                "- global dictionary additions: 0",
            ]
        )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    return {
        "status": status,
        "engine_status": "PASS" if engine_ok else "REVIEW",
        "query_count": query_count,
        "segment_count": len(segments),
        "approved_count": len(approvals),
        "review_count": len(reviews),
        "report_path": str(report_path),
        "engine_error": engine_error,
        "reviews": reviews,
        "approvals": approvals,
        "human_approved_context_count": len(human_approvals),
        "query_readings": query_readings,
        "contextual_pronunciation_audio_gate": contextual_gate,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("episode", type=Path)
    parser.add_argument("--engine-url", default=DEFAULT_ENGINE_URL)
    parser.add_argument("--speaker-id", type=int)
    parser.add_argument("--speaker", default=DEFAULT_SPEAKER_NAME)
    parser.add_argument("--style", default=DEFAULT_STYLE_NAME)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--offline", action="store_true", help="skip HTTP and run dictionary/context checks only")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    report = args.report or args.episode.parent / "work" / "pronunciation_preflight.md"
    result = run_preflight(
        args.episode.resolve(),
        report.resolve(),
        args.engine_url,
        args.speaker_id,
        args.offline,
        args.limit,
        args.speaker,
        args.style,
    )
    print(
        f"pronunciation={result['status']} approved={result['approved_count']} "
        f"review={result['review_count']} queries={result['query_count']}/{result['segment_count']}"
    )
    print(f"report={result['report_path']}")
    return 2 if result["status"] == "REVIEW" else 0


if __name__ == "__main__":
    raise SystemExit(main())
