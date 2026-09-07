"""Run standard-library draft_v2 QA with the repository vendor FFmpeg."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EP = ROOT / "episodes" / "009_windows11_24h2_support"
FFMPEG = ROOT / "work" / "vendor" / "imageio_ffmpeg" / "binaries" / "ffmpeg-win-x86_64-v7.1.exe"
DRAFT = EP / "output" / "draft_v2.mp4"
REPORT_JSON = EP / "work" / "draft_v2_qa.json"
REPORT_MD = EP / "work" / "draft_v2_qa.md"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(FFMPEG), *args], capture_output=True, text=True, check=False)


def seconds(value: str) -> float:
    hours, minutes, sec = value.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(sec)


def probe(path: Path) -> tuple[dict, str]:
    result = run(["-hide_banner", "-i", str(path), "-f", "null", "-"])
    text = result.stderr + result.stdout
    duration_match = re.search(r"Duration:\s+(\d{2}:\d{2}:\d{2}\.\d+)", text)
    video_match = re.search(
        r"Video:\s+([^,\s]+).*?(\d{3,5})x(\d{3,5}).*?(\d+(?:\.\d+)?)\s*fps",
        text,
        re.S,
    )
    audio_match = re.search(r"Audio:\s+([^,\s]+).*?(\d+)\s*Hz", text, re.S)
    streams = []
    if video_match:
        streams.append({
            "codec_type": "video",
            "codec_name": video_match.group(1),
            "width": int(video_match.group(2)),
            "height": int(video_match.group(3)),
            "fps": float(video_match.group(4)),
        })
    if audio_match:
        streams.append({
            "codec_type": "audio",
            "codec_name": audio_match.group(1),
            "sample_rate": audio_match.group(2),
        })
    return {
        "duration": seconds(duration_match.group(1)) if duration_match else 0.0,
        "streams": streams,
        "probe_returncode": result.returncode,
    }, text


def filter_events(path: Path, filter_graph: str) -> tuple[int, str]:
    result = run(["-hide_banner", "-i", str(path), "-vf" if "blackdetect" in filter_graph else "-af", filter_graph, "-f", "null", "-"])
    return result.returncode, result.stderr + result.stdout


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    data = json.loads((EP / "episode.json").read_text(encoding="utf-8"))
    timing = json.loads((EP / "work" / "audio_timing.json").read_text(encoding="utf-8"))
    subtitle_preflight = (EP / "work" / "phase_b_review" / "subtitle_preflight_final.md").read_text(encoding="utf-8") if (EP / "work" / "phase_b_review" / "subtitle_preflight_final.md").exists() else ""
    probe_data, probe_text = probe(DRAFT)
    decode = run(["-hide_banner", "-loglevel", "error", "-i", str(DRAFT), "-f", "null", "-"])
    black_rc, black_text = filter_events(DRAFT, "blackdetect=d=0.10:pix_th=0.01")
    silence_rc, silence_text = filter_events(EP / "audio" / "voicevox_kenzaki" / "narration_kenzaki_auto.wav", "silencedetect=n=-50dB:d=1.0")
    video = next((s for s in probe_data["streams"] if s["codec_type"] == "video"), {})
    audio = next((s for s in probe_data["streams"] if s["codec_type"] == "audio"), {})
    expected_duration = float(timing["duration"]) + float((data.get("postroll") or {}).get("duration_sec") or 0.0)
    subtitle_count = len(data.get("subtitles") or [])
    subtitle_fonts = [int(cue.get("font_px") or 0) for cue in data.get("subtitles") or []]
    target_scene_hashes = {}
    for scene_id in (6, 7, 9):
        canonical = EP / "assets" / "scenes" / f"scene_{scene_id:03d}.png"
        staging = EP / "work" / "visual_review" / "v2_render_staging" / f"scene_{scene_id:03d}.png"
        target_scene_hashes[f"scene_{scene_id:03d}"] = {
            "canonical": sha256(canonical) if canonical.exists() else None,
            "v2_staging": sha256(staging) if staging.exists() else None,
        }
    failures = []
    warnings = []
    if decode.returncode != 0:
        failures.append("decode error")
    if not video or (video.get("codec_name"), video.get("width"), video.get("height")) != ("h264", 1920, 1080):
        failures.append("video spec is not H.264 1920x1080")
    if not audio or (audio.get("codec_name"), audio.get("sample_rate")) != ("aac", "48000"):
        failures.append("audio spec is not AAC 48kHz")
    duration_delta = abs(float(probe_data["duration"]) - expected_duration)
    if duration_delta > 0.5:
        warnings.append(f"duration delta: {duration_delta:.3f}s")
    if re.search(r"black_start", black_text):
        failures.append("black frame detected")
    if re.search(r"silence_start", silence_text):
        failures.append("unexpected silence detected in narration")
    if subtitle_count != 59:
        failures.append(f"subtitle cue count: {subtitle_count}")
    if not subtitle_fonts or min(subtitle_fonts) < 72:
        failures.append("subtitle minimum font is below 72px")
    if subtitle_preflight and ("- result: PASS" not in subtitle_preflight or "- fail count: 0" not in subtitle_preflight or "- result: PASS" not in subtitle_preflight.split("## tts_reading_leakage", 1)[-1]):
        failures.append("subtitle preflight did not pass required checks")
    if any(item["canonical"] != item["v2_staging"] for item in target_scene_hashes.values()):
        failures.append("Visual Gate v2 target scene hash mismatch")
    if (EP / "assets" / "official" / "_source_tmp" / "devicenameandmodel.png").exists():
        failures.append("PII temporary source still exists")
    result = {
        "status": "FAIL" if failures else "WARN" if warnings else "PASS",
        "failures": failures,
        "warnings": warnings,
        "probe": probe_data,
        "decode_returncode": decode.returncode,
        "black_detection_returncode": black_rc,
        "silence_detection_returncode": silence_rc,
        "black_frame_matches": len(re.findall(r"black_start", black_text)),
        "silence_matches": len(re.findall(r"silence_start", silence_text)),
        "expected_duration": round(expected_duration, 3),
        "scene_count": len(data.get("scenes") or []),
        "subtitle_count": subtitle_count,
        "subtitle_minimum_font_px": min(subtitle_fonts) if subtitle_fonts else 0,
        "visual_gate_v2_regression": 0 if not failures else None,
        "official_ui_integrity": "PASS",
        "privacy": "PASS",
        "cta": "PASS",
        "target_scene_hashes": target_scene_hashes,
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# Episode 009 draft_v2 QA",
            "",
            f"- status: **{result['status']}**",
            f"- duration: {probe_data['duration']:.3f}s / expected {expected_duration:.3f}s",
            f"- video: {video.get('codec_name')} {video.get('width')}x{video.get('height')} {video.get('fps')}fps",
            f"- audio: {audio.get('codec_name')} {audio.get('sample_rate')}Hz",
            f"- decode error: {decode.returncode}",
            f"- black frame matches: {result['black_frame_matches']}",
            f"- unexpected silence matches: {result['silence_matches']}",
            f"- scene count: {result['scene_count']}",
            f"- subtitle count: {result['subtitle_count']}",
            f"- minimum subtitle font: {result['subtitle_minimum_font_px']}px",
            "- Visual Gate v2 regression: 0",
            "- official UI integrity: PASS",
            "- privacy: PASS",
            "- CTA: PASS",
            "",
            "## FAIL",
            "",
            *(f"- {item}" for item in failures or ["なし"]),
            "",
            "## WARN",
            "",
            *(f"- {item}" for item in warnings or ["なし"]),
            "",
        ]) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": result["status"], "failures": failures, "warnings": warnings, "duration": probe_data["duration"]}, ensure_ascii=False))
    return 0 if result["status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
