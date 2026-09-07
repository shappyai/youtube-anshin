"""Episode 007 Phase B後半 build driver（006と同一パターン）。draft_v1.mp4 を生成する。"""
from __future__ import annotations
import os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

FFMPEG_BIN = (
    Path(r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages")
    / "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    / "ffmpeg-8.1.1-full_build" / "bin"
)
os.environ["PATH"] = str(FFMPEG_BIN) + os.pathsep + os.environ.get("PATH", "")

from episode_io import apply_episode_defaults, load_json  # noqa: E402
from create_channel_cta import build_cta, content_hash, load_config, synthesize_cta_audio  # noqa: E402
from voicevox_incremental import generate_incremental, wav_duration  # noqa: E402
from build_subtitle_timeline import build_from_files  # noqa: E402
from phase2_video import build_video  # noqa: E402
from phase2_qa import run_qa  # noqa: E402

BASE = ROOT / "episodes" / "007_myna_app_login"
ENGINE = "http://127.0.0.1:50021"


def main() -> int:
    data = apply_episode_defaults(load_json(BASE / "episode.json"))
    work = BASE / "work"
    audio_dir = BASE / "audio" / "voicevox_kenzaki"

    # 1) CTA画面（channel_common_cta・canonical）
    cta = build_cta(output_path=work / "channel_cta.png")
    print("CTA:", cta)

    # 2) CTA音声（canonical。hash一致ならreuse）
    cta_config = load_config()
    cta_trailing = float(cta_config.get("trailing_seconds") or 1.0)
    cta_audio = audio_dir / "cta_channel_common.wav"
    postroll = data.get("postroll") or {}
    if cta_audio.exists() and str(postroll.get("cta_content_hash") or "") == content_hash():
        cta_duration = wav_duration(cta_audio)
        print(f"CTA audio reused: {cta_duration:.3f}s")
    else:
        cta_result = synthesize_cta_audio(engine_url=ENGINE, output_path=cta_audio)
        cta_duration = float(cta_result["duration"])
        print(f"CTA audio generated: {cta_duration:.3f}s")
    # End Screen対応（2026-09-04）: 音声後にEnd Screenを見て選べる時間を確保（CTA/ESシーン15秒前後）
    declared_postroll = float(postroll.get("duration_sec") or 0)
    cta_trailing = max(0.0, declared_postroll - cta_duration)
    print(f"CTA/End Screen: total {declared_postroll:.2f}s (audio {cta_duration:.2f}s + trailing {cta_trailing:.2f}s)")

    # 3) VOICEVOX 本編（hash/selective）: draft_v2 発音修正 seg のみ再生成（NFC/PIN/上/方×2）
    REGEN_SEGMENTS = [13, 17, 26, 32, 40]
    planned_total, skipped_total = [], []
    for seg_id in REGEN_SEGMENTS:
        step = generate_incremental(data, BASE, work, ENGINE, audio_dir=audio_dir, force_segment=seg_id)
        planned_total.extend(step["planned"]); skipped_total.extend(step["skipped"]); duration = step.get("duration")
    step_all = generate_incremental(data, BASE, work, ENGINE, audio_dir=audio_dir)
    planned_total.extend(step_all["planned"]); skipped_total.extend(step_all["skipped"]); duration = step_all.get("duration")
    print(f"voice regenerated={len(planned_total)} reused={len(skipped_total)} duration={duration}")

    # 4) 字幕タイムライン（実測audioベース）
    timing = work / "audio_timing.json"
    srt, ass = work / "captions_auto.srt", work / "captions_auto.ass"
    build_from_files(data, timing, srt, ass)
    print("timing:", timing)

    # 5) draft assemble
    draft = BASE / "output" / "draft_v5.mp4"
    if draft.exists():
        print(f"STOP: draft already exists: {draft}")
        return 1
    audio = audio_dir / "narration_kenzaki_auto.wav"
    video = build_video(
        data, work / "rendered_final_scenes", timing, audio, ass, work, draft,
        cta_audio_path=cta_audio, cta_trailing=cta_trailing,
    )
    if video["status"] != "PASS":
        print("STOP: " + "; ".join(video["errors"]))
        return 1
    print("draft:", draft)

    # 6) QA
    qa = run_qa(data, work / "rendered_final_scenes", timing, draft, work / "phase2_qa", audio)
    print("QA:", qa["status"])
    for item in qa.get("failures", []):
        print("FAIL:", item)
    for item in qa.get("warnings", []):
        print("WARN:", item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
