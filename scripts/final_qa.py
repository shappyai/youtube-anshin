"""Verify a copy-only final against its human-approved draft."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from phase2_qa import (  # noqa: E402
    _black_frames,
    _ffmpeg_executable,
    _long_silences,
    _probe as phase2_probe,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def probe(path: Path) -> dict[str, Any]:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return phase2_probe(path)
    result = subprocess.run(
        [
            ffprobe, "-v", "error", "-show_entries",
            "format=duration", "-show_entries",
            "stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
            "-of", "json", str(path),
        ],
        check=False, capture_output=True, text=True,
    )
    if result.returncode:
        return {"error": result.stderr.strip() or "ffprobe failed"}
    return json.loads(result.stdout)


def decode_errors(path: Path) -> list[str]:
    ffmpeg = _ffmpeg_executable()
    if not ffmpeg:
        return ["ffmpeg was not found"]
    result = subprocess.run(
        [ffmpeg, "-v", "error", "-i", str(path), "-f", "null", "-"],
        check=False, capture_output=True, text=True,
    )
    return [line for line in result.stderr.splitlines() if line.strip()]


def black_frames(path: Path) -> list[str]:
    ffmpeg = _ffmpeg_executable()
    if not ffmpeg:
        return ["ffmpeg was not found"]
    result = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", str(path), "-vf", "blackdetect=d=0.5:pix_th=0.10", "-an", "-f", "null", "-"],
        check=False, capture_output=True, text=True,
    )
    return [line.strip() for line in result.stderr.splitlines() if "black_start:" in line]


def clipped_samples(path: Path) -> int:
    ffmpeg = _ffmpeg_executable()
    if not ffmpeg or not path.exists():
        return 0
    result = subprocess.run(
        [
            ffmpeg, "-hide_banner", "-i", str(path), "-vn",
            "-af", "astats=metadata=1:reset=0", "-f", "null", "-",
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    matches = []
    for line in result.stderr.splitlines():
        if "Number of clipped samples" not in line:
            continue
        try:
            matches.append(int(float(line.rsplit(":", 1)[-1].strip())))
        except ValueError:
            continue
    return max(matches or [0])


def run(draft: Path, final: Path, audio: Path | None = None) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    for path in (draft, final):
        if not path.exists():
            failures.append(f"missing: {path}")
    if failures:
        return {"status": "FAIL", "failures": failures, "warnings": warnings}

    draft_hash, final_hash = sha256(draft), sha256(final)
    if draft_hash != final_hash:
        failures.append("draft and final SHA-256 do not match (copy-only finalize expected)")
    final_probe = probe(final)
    if final_probe.get("error"):
        failures.append(f"probe: {final_probe['error']}")
    else:
        video = next((item for item in final_probe.get("streams", []) if item.get("codec_type") == "video"), {})
        audio_stream = next((item for item in final_probe.get("streams", []) if item.get("codec_type") == "audio"), {})
        if (video.get("width"), video.get("height")) != (1920, 1080):
            failures.append("resolution is not 1920x1080")
        if video.get("codec_name") != "h264":
            failures.append(f"video codec is not h264: {video.get('codec_name')}")
        if video.get("r_frame_rate") not in {"30/1", "30000/1001"}:
            failures.append(f"frame rate is not 30fps: {video.get('r_frame_rate')}")
        if not audio_stream:
            failures.append("audio stream is missing")
        else:
            if audio_stream.get("codec_name") != "aac":
                failures.append(f"audio codec is not aac: {audio_stream.get('codec_name')}")
            if str(audio_stream.get("sample_rate")) != "48000":
                failures.append(f"audio sample rate is not 48000Hz: {audio_stream.get('sample_rate')}")
    errors = decode_errors(final)
    if errors == ["ffmpeg was not found"]:
        warnings.append("ffmpeg was not found; decode check not run")
    elif errors:
        failures.extend(f"decode: {line}" for line in errors)
    black = black_frames(final)
    if black:
        failures.extend(f"black frame: {line}" for line in black)

    draft_probe = probe(draft)
    draft_duration = float((draft_probe.get("format") or {}).get("duration") or 0)
    final_duration = float((final_probe.get("format") or {}).get("duration") or 0)
    av_sync = "PASS" if draft_duration and final_duration and abs(draft_duration - final_duration) <= 0.05 else "FAIL"
    if av_sync != "PASS":
        failures.append(f"AV sync duration check failed: draft={draft_duration:.3f}s final={final_duration:.3f}s")

    audio_path = audio if audio and audio.exists() else final
    silence_intervals = _long_silences(audio_path)
    if silence_intervals:
        failures.extend(f"unexpected silence: {line}" for line in silence_intervals)
    clipping = clipped_samples(audio_path)
    if clipping:
        failures.append(f"audio clipping detected: {clipping} clipped samples")

    result = {
        "status": "FAIL" if failures else "WARN" if warnings else "PASS",
        "failures": failures,
        "warnings": warnings,
        "draft": {"path": str(draft), "sha256": draft_hash},
        "final": {"path": str(final), "sha256": final_hash},
        "sha256_match": draft_hash == final_hash,
        "probe": final_probe,
        "decode_error_count": len(errors),
        "black_frame_count": len(black),
        "unexpected_silence_count": len(silence_intervals),
        "av_sync": av_sync,
        "audio_clipping_count": clipping,
        "audio_checked": str(audio_path),
        "subtitle_burn_in": "manual review required; no subtitle stream is expected",
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--final", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--markdown", type=Path)
    parser.add_argument("--audio", type=Path, help="canonical narration WAV for silence/clipping checks")
    args = parser.parse_args()
    result = run(
        args.draft.resolve(),
        args.final.resolve(),
        args.audio.resolve() if args.audio else None,
    )
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown:
        final_hash = result.get("final", {}).get("sha256", "")
        probe_data = result.get("probe") or {}
        video = next((item for item in probe_data.get("streams", []) if item.get("codec_type") == "video"), {})
        lines = [
            "# Final QA PASS" if result["status"] == "PASS" else f"# Final QA {result['status']}",
            "",
            f"- status: **{result['status']}**",
            f"- final_sha256: `{final_hash}`",
            f"- sha256_match: `{result.get('sha256_match')}`",
            f"- decode_error_count: `{result.get('decode_error_count', 0)}`",
            f"- black_frame_count: `{result.get('black_frame_count', 0)}`",
            f"- unexpected_silence_count: `{result.get('unexpected_silence_count', 0)}`",
            f"- av_sync: `{result.get('av_sync')}`",
            f"- audio_clipping_count: `{result.get('audio_clipping_count', 0)}`",
            f"- resolution: `{video.get('width')}x{video.get('height')}`",
            f"- video_codec: `{video.get('codec_name')}`",
            f"- failure_count: `{len(result.get('failures', []))}`",
            f"- warning_count: `{len(result.get('warnings', []))}`",
        ]
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 2 if result["status"] == "WARN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
