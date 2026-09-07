"""Run the Episode 009 draft_v3 QA gate without changing Visual Gate assets."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import wave
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
EP = ROOT / "episodes" / "009_windows11_24h2_support"
FFMPEG = ROOT / "work" / "vendor" / "imageio_ffmpeg" / "binaries" / "ffmpeg-win-x86_64-v7.1.exe"
DRAFT = EP / "output" / "draft_v3.mp4"
REPORT_JSON = EP / "work" / "draft_v3_qa.json"
REPORT_MD = EP / "work" / "draft_v3_qa.md"
SUBTITLE_PREFLIGHT = EP / "work" / "phase_b_review" / "subtitle_preflight_final.md"
PRONUNCIATION_QA = EP / "work" / "phase_b_review" / "pronunciation_v3_qa.json"
AMBIGUOUS_QA = EP / "work" / "phase_b_review" / "ambiguous_kanji_pronunciation_v3.json"

NEW_PHRASES = {
    6: "三つ目は、更新が表示されないときに考えるポイントです。",
    38: "24H2の場合は、まず25H2が表示されるかを確認してください。",
}
OLD_PHRASES = {
    6: "三つ目、更新が表示されないときの考え方です。",
    38: "24H2の方は、まず25H2が表示されるかを確認してください。",
}


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(FFMPEG), *args], capture_output=True, text=True, check=False)


def seconds(value: str) -> float:
    hours, minutes, sec = value.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(sec)


def probe(path: Path) -> tuple[dict[str, Any], str]:
    result = run(["-hide_banner", "-i", str(path), "-f", "null", "-"])
    text = result.stderr + result.stdout
    duration_match = re.search(r"Duration:\s+(\d{2}:\d{2}:\d{2}\.\d+)", text)
    video_match = re.search(r"Video:\s+([^,\s]+).*?(\d{3,5})x(\d{3,5}).*?(\d+(?:\.\d+)?)\s*fps", text, re.S)
    audio_match = re.search(r"Audio:\s+([^,\s]+).*?(\d+)\s*Hz", text, re.S)
    streams = []
    if video_match:
        streams.append({"codec_type": "video", "codec_name": video_match.group(1), "width": int(video_match.group(2)), "height": int(video_match.group(3)), "fps": float(video_match.group(4))})
    if audio_match:
        streams.append({"codec_type": "audio", "codec_name": audio_match.group(1), "sample_rate": audio_match.group(2)})
    return {
        "duration": seconds(duration_match.group(1)) if duration_match else 0.0,
        "streams": streams,
        "probe_returncode": result.returncode,
    }, text


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def subtitle_texts(data: dict[str, Any]) -> dict[int, str]:
    result: dict[int, str] = {}
    for cue in data.get("subtitles") or []:
        sid = int(cue["segment_id"])
        result[sid] = result.get(sid, "") + "".join(str(line) for line in cue.get("text_lines") or [])
    return result


def chapter_time(value: str) -> int:
    match = re.match(r"^(\d+):(\d{2})\s", value)
    if not match:
        return -1
    return int(match.group(1)) * 60 + int(match.group(2))


def main() -> int:
    sys.path.insert(0, str(ROOT / "scripts"))
    from scene_renderer import make_contact_sheet
    from subtitle_preflight import estimated_width

    data = json.loads((EP / "episode.json").read_text(encoding="utf-8"))
    timing = json.loads((EP / "work" / "audio_timing.json").read_text(encoding="utf-8"))
    cues = subtitle_texts(data)
    failures: list[str] = []
    warnings: list[str] = []

    if not DRAFT.exists():
        failures.append("draft_v3.mp4 is missing")
    probe_data, probe_text = probe(DRAFT) if DRAFT.exists() else ({"duration": 0.0, "streams": [], "probe_returncode": 1}, "")
    decode = run(["-hide_banner", "-loglevel", "error", "-i", str(DRAFT), "-f", "null", "-"]) if DRAFT.exists() else None
    black = run(["-hide_banner", "-i", str(DRAFT), "-vf", "blackdetect=d=0.10:pix_th=0.01", "-f", "null", "-"]) if DRAFT.exists() else None
    narration_audio = EP / "audio" / "voicevox_kenzaki" / "narration_kenzaki_auto.wav"
    silence = run(["-hide_banner", "-i", str(narration_audio), "-af", "silencedetect=n=-50dB:d=1.0", "-f", "null", "-"]) if narration_audio.exists() else None
    video = next((stream for stream in probe_data["streams"] if stream["codec_type"] == "video"), {})
    audio = next((stream for stream in probe_data["streams"] if stream["codec_type"] == "audio"), {})

    if decode is None or decode.returncode != 0:
        failures.append("decode error")
    if not video or (video.get("codec_name"), video.get("width"), video.get("height")) != ("h264", 1920, 1080):
        failures.append("video spec is not H.264 1920x1080")
    if not video or video.get("fps") != 30.0:
        failures.append("video frame rate is not 30fps")
    if not audio or (audio.get("codec_name"), audio.get("sample_rate")) != ("aac", "48000"):
        failures.append("audio spec is not AAC 48kHz")
    expected_duration = float(timing["duration"]) + float((data.get("postroll") or {}).get("duration_sec") or 0.0)
    duration_delta = abs(float(probe_data["duration"]) - expected_duration)
    if duration_delta > 0.5:
        failures.append(f"duration delta: {duration_delta:.3f}s")
    black_text = (black.stderr + black.stdout) if black else ""
    silence_text = (silence.stderr + silence.stdout) if silence else ""
    if "black_start" in black_text:
        failures.append("black frame detected")
    if "silence_start" in silence_text:
        failures.append("unexpected silence detected in narration")

    subtitle_fonts = [int(cue.get("font_px") or 0) for cue in data.get("subtitles") or []]
    overflow_rows = []
    three_line_ids = []
    for cue in data.get("subtitles") or []:
        font_px = float(cue.get("font_px") or 72)
        if font_px < 56:
            overflow_rows.append({"id": cue.get("id"), "reason": "font<56"})
        if len(cue.get("text_lines") or []) >= 3:
            three_line_ids.append(str(cue.get("id")))
        for line_index, line in enumerate(cue.get("text_lines") or [], 1):
            measured = estimated_width(str(line)) * font_px / 72.0
            if measured > 1800:
                overflow_rows.append({"id": cue.get("id"), "line": line_index, "measured_px": round(measured)})
    preflight_text = SUBTITLE_PREFLIGHT.read_text(encoding="utf-8") if SUBTITLE_PREFLIGHT.exists() else ""
    subtitle_checks = {
        "cue_count": len(data.get("subtitles") or []),
        "minimum_font_px": min(subtitle_fonts) if subtitle_fonts else 0,
        "font_lt_56_count": sum(1 for font in subtitle_fonts if font < 56),
        "overflow_count": len(overflow_rows),
        "three_line_count": len(three_line_ids),
        "semantic_split": "- result: PASS" in preflight_text and "- fail count: 0" in preflight_text,
        "tts_reading_leakage": "## tts_reading_leakage" in preflight_text and "- result: PASS" in preflight_text.split("## tts_reading_leakage", 1)[1] and "- fail count: 0" in preflight_text.split("## tts_reading_leakage", 1)[1],
        "new_wording_present": all(cues.get(sid) == phrase for sid, phrase in NEW_PHRASES.items()),
        "old_wording_absent_from_target_cues": all(OLD_PHRASES[sid] not in cues.get(sid, "") for sid in OLD_PHRASES),
    }
    if subtitle_checks["cue_count"] != 59:
        failures.append(f"subtitle cue count: {subtitle_checks['cue_count']}")
    if subtitle_checks["font_lt_56_count"] != 0:
        failures.append("subtitle font<56 count is not zero")
    if subtitle_checks["overflow_count"] != 0:
        failures.append("subtitle overflow count is not zero")
    if subtitle_checks["three_line_count"] != 0:
        failures.append("3-line subtitle count is not zero")
    if not subtitle_checks["semantic_split"]:
        failures.append("semantic subtitle split did not pass")
    if not subtitle_checks["tts_reading_leakage"]:
        failures.append("TTS reading leakage did not pass")
    if not subtitle_checks["new_wording_present"] or not subtitle_checks["old_wording_absent_from_target_cues"]:
        failures.append("target wording is not synchronized in narration/subtitles")

    narration_by_id = {int(segment["id"]): str(segment.get("narration") or "") for segment in data.get("narration_segments") or []}
    wording_sync = {
        "script_segment_006": NEW_PHRASES[6] in (EP / "script.md").read_text(encoding="utf-8"),
        "script_segment_038": NEW_PHRASES[38] in (EP / "script.md").read_text(encoding="utf-8"),
        "episode_segment_006": narration_by_id.get(6) == NEW_PHRASES[6],
        "episode_segment_038": narration_by_id.get(38) == NEW_PHRASES[38],
    }
    if not all(wording_sync.values()):
        failures.append("script.md and episode.json narration are not synchronized")

    # Confirm chapters point to the measured starts of the corresponding sections.
    start_by_segment = {int(row["segment_id"]): float(row["start_sec"]) for row in timing.get("segments", [])}
    section_starts: dict[str, int] = {}
    for scene in data.get("scenes") or []:
        label = str(scene.get("section_label") or "")
        if label in {"1 / 3", "2 / 3", "3 / 3", "困ったとき", "まとめ"} and label not in section_starts:
            section_starts[label] = int(round(start_by_segment[int(scene["start_segment"])]))
    chapter_values = data.get("publish", {}).get("chapters") or []
    chapter_seconds = [chapter_time(str(item)) for item in chapter_values]
    expected_chapters = [0, section_starts.get("1 / 3", -1), section_starts.get("2 / 3", -1), section_starts.get("3 / 3", -1), section_starts.get("困ったとき", -1), section_starts.get("まとめ", -1)]
    chapters_ok = chapter_seconds == expected_chapters
    if not chapters_ok:
        failures.append(f"chapter timing mismatch: actual={chapter_seconds} expected={expected_chapters}")

    # A deterministic contact sheet hash is the all-scene regression check.
    regression_sheet = EP / "work" / "phase_b_review" / "scene_contact_sheet_v3_regression.png"
    make_contact_sheet(EP / "assets" / "scenes", data.get("scenes") or [], regression_sheet)
    v2_sheet = EP / "work" / "visual_review" / "scene_contact_sheet_v2.png"
    visual_regression = {"v2_contact_sheet_sha256": sha256(v2_sheet) if v2_sheet.exists() else None, "v3_regression_sheet_sha256": sha256(regression_sheet) if regression_sheet.exists() else None}
    visual_regression["status"] = "PASS" if visual_regression["v2_contact_sheet_sha256"] == visual_regression["v3_regression_sheet_sha256"] else "FAIL"
    if visual_regression["status"] != "PASS":
        failures.append("Visual Gate v2 contact sheet regression mismatch")
    target_scene_hashes = {}
    for scene_id in (6, 7, 9):
        canonical = EP / "assets" / "scenes" / f"scene_{scene_id:03d}.png"
        staging = EP / "work" / "visual_review" / "v2_render_staging" / f"scene_{scene_id:03d}.png"
        target_scene_hashes[f"scene_{scene_id:03d}"] = {"canonical": sha256(canonical) if canonical.exists() else None, "v2_staging": sha256(staging) if staging.exists() else None}
    target_regression = all(row["canonical"] == row["v2_staging"] for row in target_scene_hashes.values())
    if not target_regression:
        failures.append("Visual Gate v2 target scene hash mismatch")

    # PII source and canonical references must both be absent.
    pii_path = EP / "assets" / "official" / "_source_tmp" / "devicenameandmodel.png"
    canonical_files = [EP / name for name in ("episode.json", "script.md", "shotlist.md", "media_manifest.csv", "publish.json")]
    pii_refs = [str(path) for path in canonical_files if path.exists() and any(token in path.read_text(encoding="utf-8") for token in ("devicenameandmodel.png", "_source_tmp", "official_source_tmp"))]
    privacy_ok = not pii_path.exists() and not pii_refs
    if not privacy_ok:
        failures.append("PII temporary source or canonical reference remains")

    cta_preflight_path = EP / "work" / "phase_b_review" / "cta_preflight.json"
    cta_preflight = json.loads(cta_preflight_path.read_text(encoding="utf-8")) if cta_preflight_path.exists() else {}
    cta_audio = EP / "audio" / "voicevox_kenzaki" / "cta_channel_common.wav"
    cta_duration = 0.0
    if cta_audio.exists():
        with wave.open(str(cta_audio), "rb") as handle:
            cta_duration = handle.getnframes() / handle.getframerate()
    cta_ok = cta_preflight.get("status") == "PASS" and (EP / "work" / "channel_cta.png").exists() and cta_duration <= 15.05
    if not cta_ok:
        failures.append("CTA regression/preflight did not pass")

    pronunciation = json.loads(PRONUNCIATION_QA.read_text(encoding="utf-8")) if PRONUNCIATION_QA.exists() else {"status": "MISSING"}
    ambiguous = json.loads(AMBIGUOUS_QA.read_text(encoding="utf-8")) if AMBIGUOUS_QA.exists() else {"status": "MISSING"}
    if pronunciation.get("status") != "PASS":
        failures.append("pronunciation v3 QA did not pass")
    if not ambiguous.get("target_checks") or any(row.get("status") != "PASS" for row in ambiguous.get("target_checks") or []):
        failures.append("ambiguous_kanji_pronunciation targeted checks did not pass")

    draft_v2_hash = sha256(EP / "output" / "draft_v2.mp4") if (EP / "output" / "draft_v2.mp4").exists() else None
    draft_v1_hash = sha256(EP / "output" / "draft_v1.mp4") if (EP / "output" / "draft_v1.mp4").exists() else None
    if draft_v2_hash is None or draft_v1_hash is None:
        failures.append("draft_v1/draft_v2 preservation check failed")

    result = {
        "status": "FAIL" if failures else "WARN" if warnings else "PASS",
        "failures": failures,
        "warnings": warnings,
        "probe": probe_data,
        "decode_returncode": decode.returncode if decode else None,
        "black_frame_matches": len(re.findall(r"black_start", black_text)),
        "silence_matches": len(re.findall(r"silence_start", silence_text)),
        "expected_duration": round(expected_duration, 3),
        "duration_delta": round(duration_delta, 3),
        "narration_duration_seconds": round(float(timing["duration"]), 3),
        "cta_start_seconds": round(float(timing["duration"]), 3),
        "cta_duration_seconds": round(cta_duration, 3),
        "scene_count": len(data.get("scenes") or []),
        "narration_segment_count": len(data.get("narration_segments") or []),
        "subtitle": subtitle_checks,
        "wording_sync": wording_sync,
        "chapters": {"actual_seconds": chapter_seconds, "expected_seconds": expected_chapters, "status": "PASS" if chapters_ok else "FAIL"},
        "visual_gate_v2_regression": visual_regression,
        "target_scene_hashes": target_scene_hashes,
        "privacy": {"status": "PASS" if privacy_ok else "FAIL", "temporary_source_exists": pii_path.exists(), "canonical_reference_count": len(pii_refs)},
        "cta": {"status": "PASS" if cta_ok else "FAIL", "preflight_status": cta_preflight.get("status"), "audio_duration_seconds": round(cta_duration, 3)},
        "pronunciation": pronunciation,
        "ambiguous_kanji_pronunciation": ambiguous,
        "draft_v1_sha256": draft_v1_hash,
        "draft_v2_sha256": draft_v2_hash,
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Episode 009 draft_v3 QA",
        "",
        f"- status: **{result['status']}**",
        f"- draft_v3 duration: {probe_data['duration']:.3f}s / expected {expected_duration:.3f}s",
        f"- video: {video.get('codec_name')} {video.get('width')}x{video.get('height')} {video.get('fps')}fps",
        f"- audio: {audio.get('codec_name')} {audio.get('sample_rate')}Hz",
        f"- decode error: {result['decode_returncode']}",
        f"- black frame matches: {result['black_frame_matches']}",
        f"- unexpected narration silence matches: {result['silence_matches']}",
        f"- scenes: {result['scene_count']} / narration segments: {result['narration_segment_count']}",
        f"- subtitles: {subtitle_checks['cue_count']} cues / min {subtitle_checks['minimum_font_px']}px / font<56 {subtitle_checks['font_lt_56_count']} / overflow {subtitle_checks['overflow_count']} / 3-line {subtitle_checks['three_line_count']}",
        f"- semantic split: {'PASS' if subtitle_checks['semantic_split'] else 'FAIL'}",
        f"- TTS reading leakage: {'PASS' if subtitle_checks['tts_reading_leakage'] else 'FAIL'}",
        f"- targeted wording synchronization: {'PASS' if all(wording_sync.values()) and subtitle_checks['new_wording_present'] else 'FAIL'}",
        f"- chapters / CTA start: {'PASS' if chapters_ok else 'FAIL'} / {float(timing['duration']):.3f}s",
        f"- Visual Gate v2 regression: {visual_regression['status']}",
        f"- privacy: {'PASS' if privacy_ok else 'FAIL'}",
        f"- pronunciation targets: {pronunciation.get('status')}",
        f"- ambiguous_kanji_pronunciation targeted checks: {'PASS' if ambiguous.get('target_checks') and all(row.get('status') == 'PASS' for row in ambiguous.get('target_checks') or []) else 'FAIL'} (overall {ambiguous.get('status')})",
        f"- CTA: {'PASS' if cta_ok else 'FAIL'}",
        "",
        "## FAIL",
        "",
    ]
    lines.extend(f"- {failure}" for failure in failures or ["なし"])
    lines.extend(["", "## WARN", ""])
    lines.extend(f"- {warning}" for warning in warnings or ["なし"])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "duration": round(probe_data["duration"], 3), "failures": failures, "warnings": warnings, "visual_regression": visual_regression["status"]}, ensure_ascii=False))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
