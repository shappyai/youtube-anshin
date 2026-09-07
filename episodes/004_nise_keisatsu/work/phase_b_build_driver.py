"""Episode 004 Phase B後半 build driver.

Phase A/B前半ゲートは人間承認済み（pronunciation PASS / GPT safe-area REVIEWは
人間承認済みとして記録済み）。ここでは同ライブラリを順に呼んでdraftを生成する。
ffmpegはWinGetインストール先をPATHへ追加して使用。
"""
from __future__ import annotations

import sys
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
import os

os.environ["PATH"] = str(FFMPEG_BIN) + os.pathsep + os.environ.get("PATH", "")

from episode_io import apply_episode_defaults, load_json  # noqa: E402
from create_channel_cta import build_cta  # noqa: E402
from voicevox_incremental import generate_incremental  # noqa: E402
from build_subtitle_timeline import build_from_files  # noqa: E402
from phase2_video import build_video  # noqa: E402
from phase2_qa import run_qa  # noqa: E402

BASE = ROOT / "episodes" / "004_nise_keisatsu"
ENGINE = "http://127.0.0.1:50021"


def main() -> int:
    data = apply_episode_defaults(load_json(BASE / "episode.json"))
    work = BASE / "work"
    audio_dir = BASE / "audio" / "voicevox_kenzaki"

    # 1) CTA（channel_common_cta・brand_promiseなし）
    cta = build_cta(output_path=work / "channel_cta.png")
    print("CTA:", cta)

    # 2) VOICEVOX 本編（hash/selective。指定segmentだけ再生成）
    regen: list[int] = []
    if "--regen" in sys.argv:
        index = sys.argv.index("--regen")
        regen = [int(item) for item in sys.argv[index + 1].split(",") if item.strip().isdigit()]
    voice = {"planned": [], "skipped": []}
    if regen:
        for seg in regen:
            step = generate_incremental(data, BASE, work, ENGINE, force_segment=seg, audio_dir=audio_dir)
            voice["planned"].extend(step["planned"])
            voice["skipped"].extend(step["skipped"])
    else:
        voice = generate_incremental(data, BASE, work, ENGINE, audio_dir=audio_dir)
    print(f"voice planned={len(voice['planned'])} skipped={len(voice['skipped'])}")

    # 3) 字幕タイムライン（実測audioベース）
    timing = work / "audio_timing.json"
    srt, ass = work / "captions_auto.srt", work / "captions_auto.ass"
    build_from_files(data, timing, srt, ass)
    print("timing:", timing)

    # 4) draft assemble
    version = sys.argv[1] if len(sys.argv) > 1 else "draft_v1.mp4"
    draft = BASE / "output" / version
    if draft.exists():
        print(f"STOP: draft already exists: {draft}")
        return 1
    audio = audio_dir / "narration_kenzaki_auto.wav"
    video = build_video(data, work / "rendered_final_scenes", timing, audio, ass, work, draft)
    if video["status"] != "PASS":
        print("STOP: " + "; ".join(video["errors"]))
        return 1
    print("draft:", draft)

    # 5) QA
    qa = run_qa(data, work / "rendered_final_scenes", timing, draft, work / "phase2_qa", audio)
    print("QA:", qa["status"])
    for item in qa.get("failures", []):
        print("FAIL:", item)
    for item in qa.get("warnings", []):
        print("WARN:", item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
