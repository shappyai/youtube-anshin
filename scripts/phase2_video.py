"""Build a 1080p Phase 2 draft from rendered scenes, measured audio, and ASS subtitles."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ANIMATION = "static"


def _ffmpeg_executable() -> str | None:
    executable = shutil.which("ffmpeg")
    if executable:
        return executable
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def _run(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def _scene_durations(data: dict[str, Any], timing: dict[str, Any]) -> list[tuple[dict[str, Any], float]]:
    times = {int(row["segment_id"]): row for row in timing["segments"]}
    result: list[tuple[dict[str, Any], float]] = []
    for scene in data.get("scenes", []):
        start = times[int(scene["start_segment"])]["start_sec"]
        end_row = times[int(scene["end_segment"])]
        end = float(end_row["end_sec"]) + float(end_row.get("pause_after") or 0)
        result.append((scene, max(0.1, float(end) - float(start))))
    return result


def _filter(animation: str, duration: float) -> str:
    frames = max(1, round(duration * 30))
    if animation in {"slow_zoom", "very_slow_zoom"}:
        return f"zoompan=z='min(zoom+0.00025,1.04)':d={frames}:s=1920x1080:fps=30"
    if animation == "slow_pan":
        # FFmpeg's crop filter exposes the current output frame as `n`.
        # `on` is not a valid variable in current FFmpeg releases.
        denominator = max(1, frames - 1)
        return f"scale=2000:1125,crop=1920:1080:x='(iw-ow)*n/{denominator}':y='(ih-oh)/2',fps=30"
    # crossfade is applied as a gentle fade at clip boundaries; unknown values are safely static.
    if animation == "crossfade":
        fade_out = max(0.0, duration - 0.35)
        return f"fps=30,fade=t=in:st=0:d=0.35,fade=t=out:st={fade_out:.3f}:d=0.35"
    return "fps=30"


def _resolve_asset(value: Any, base_dir: Path | None = None) -> Path:
    path = Path(str(value or ""))
    if path.is_absolute():
        return path
    if base_dir is not None:
        local = (base_dir / path).resolve()
        if local.exists() or (path.parts and path.parts[0] in {"work", "output", "assets", "audio", "raw", "thumbnail", "final"}):
            return local
    return ROOT / path


def build_video(
    data: dict[str, Any], final_scene_dir: Path, timing_path: Path, audio_path: Path,
    ass_path: Path, work_dir: Path, output_path: Path,
    cta_audio_path: Path | None = None, cta_trailing: float = 1.0,
) -> dict[str, Any]:
    ffmpeg = _ffmpeg_executable()
    if not ffmpeg:
        return {"status": "FAIL", "errors": ["ffmpeg was not found"]}
    timing = json.loads(timing_path.read_text(encoding="utf-8"))
    clip_dir = work_dir / "video_clips"
    clip_dir.mkdir(parents=True, exist_ok=True)
    clips: list[Path] = []
    scene_durations = _scene_durations(data, timing)
    main_duration = sum(duration for _scene, duration in scene_durations)
    for scene, duration in scene_durations:
        scene_id = int(scene["id"])
        source = final_scene_dir / f"scene_{scene_id:03d}.png"
        if not source.exists():
            return {"status": "FAIL", "errors": [f"missing rendered scene: {source.name}"]}
        clip = clip_dir / f"scene_{scene_id:03d}.mp4"
        animation = str(scene.get("animation") or DEFAULT_ANIMATION)
        _run([
            ffmpeg, "-y", "-loop", "1", "-i", str(source), "-t", f"{duration:.3f}",
            "-vf", _filter(animation, duration), "-an", "-c:v", "libx264", "-preset", "medium",
            "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", str(clip),
        ])
        clips.append(clip)
    postroll = data.get("postroll") or {}
    postroll_duration = float(postroll.get("duration_sec") or 0)
    postroll_source: Path | None = None
    if postroll_duration > 0:
        episode_dir = work_dir
        for candidate in (work_dir, work_dir.parent, work_dir.parent.parent, work_dir.parent.parent.parent):
            if (candidate / "episode.json").exists():
                episode_dir = candidate
                break
        postroll_source = _resolve_asset(postroll.get("asset"), episode_dir)
        if not postroll_source.exists():
            return {"status": "FAIL", "errors": [f"missing postroll asset: {postroll_source}"]}
        postroll_clip = clip_dir / "postroll_cta.mp4"
        _run([
            ffmpeg, "-y", "-loop", "1", "-i", str(postroll_source), "-t", f"{postroll_duration:.3f}",
            "-vf", _filter(str(postroll.get("animation") or "static"), postroll_duration),
            "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", str(postroll_clip),
        ])
        clips.append(postroll_clip)
    concat_path = clip_dir / "concat.txt"
    concat_path.write_text("\n".join(f"file '{path.as_posix()}'" for path in clips) + "\n", encoding="utf-8")
    visual = work_dir / "visual_phase2.mp4"
    _run([ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_path), "-c", "copy", str(visual)])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ass_filter = str(ass_path.resolve()).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
    subtitle_filter = (
        f"drawbox=x=0:y=900:w=1920:h=180:color=0x16263F@1:t=fill:enable='lt(t,{main_duration:.3f})',"
        f"ass='{ass_filter}'"
    )
    if cta_audio_path is not None and cta_audio_path.exists():
        # CTA音声を本編直後に連結し、余韻分をsilenceで延長する。
        # 画面と音声が同じ内容を伝える（audio_required / duration_mode=audio_based）。
        filter_complex = (
            f"[1:a][2:a]concat=n=2:v=0:a=1,apad=pad_dur={cta_trailing:.3f}[aout]"
        )
        command = [
            ffmpeg, "-y", "-i", str(visual), "-i", str(audio_path), "-i", str(cta_audio_path),
            "-filter_complex", filter_complex,
            "-vf", subtitle_filter,
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-ar", "48000", "-b:a", "192k",
            "-shortest", str(output_path),
        ]
        _run(command)
        return {
            "status": "PASS", "output": str(output_path), "clip_count": len(clips),
            "scene_count": len(scene_durations), "main_duration": round(main_duration, 3),
            "postroll_duration": round(postroll_duration, 3),
            "postroll_source": str(postroll_source) if postroll_source else "",
            "cta_audio": str(cta_audio_path),
        }
    command = [
        ffmpeg, "-y", "-i", str(visual), "-i", str(audio_path), "-vf", subtitle_filter,
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", "48000", "-b:a", "192k",
    ]
    if postroll_duration > 0:
        command.extend(["-af", f"apad=pad_dur={postroll_duration:.3f}"])
    command.extend(["-shortest", str(output_path)])
    _run(command)
    return {
        "status": "PASS", "output": str(output_path), "clip_count": len(clips),
        "scene_count": len(scene_durations), "main_duration": round(main_duration, 3),
        "postroll_duration": round(postroll_duration, 3),
        "postroll_source": str(postroll_source) if postroll_source else "",
    }
