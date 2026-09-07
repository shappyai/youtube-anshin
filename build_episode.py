"""Phase 2 gated hybrid episode builder."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_image_generation_manifest import write_manifest  # noqa: E402
from build_subtitle_timeline import build_from_files  # noqa: E402
from episode_io import apply_episode_defaults, load_json, validate_episode  # noqa: E402
from hybrid_scene_renderer import render_episode_scenes, validate_ai_images  # noqa: E402
from phase2_qa import approved_draft_filename, finalize_allowed, narration_item_count_issues, run_qa  # noqa: E402
from phase2_video import build_video  # noqa: E402
from create_channel_cta import build_cta  # noqa: E402
from production_metrics import load_or_create, now_iso, save as save_metrics  # noqa: E402
from production_preflight import check_official_assets, check_scenes, check_sources  # noqa: E402
from scene_mode_advisor import advise_episode, write_reports  # noqa: E402
from subtitle_preflight import run_preflight as run_subtitle_preflight  # noqa: E402
from voicevox_incremental import generate_incremental  # noqa: E402
from voicevox_preflight import run_preflight as run_voicevox_preflight  # noqa: E402

VALID_MODES = {"template", "gpt_image", "official", "hybrid"}


def resolve_episode(value: str) -> Path:
    path = Path(value)
    if path.exists():
        return (path / "episode.json" if path.is_dir() else path).resolve()
    episode_id = value.zfill(3) if value.isdigit() else value
    matches = list((ROOT / "episodes").glob(f"{episode_id}_*/episode.json"))
    if len(matches) != 1:
        raise SystemExit(f"Episode target must resolve exactly once: {value} ({len(matches)} matches)")
    return matches[0].resolve()


def read_review(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def apply_pronunciation_review(result: dict[str, Any], review: dict[str, Any]) -> dict[str, Any]:
    approved_raw = review.get("pronunciation", {}).get("approved_segments", [])
    approved = {int(value) for value in approved_raw if str(value).isdigit()}
    for key, value in review.get("pronunciation", {}).items():
        if str(key).startswith("seg_") and value:
            suffix = str(key).removeprefix("seg_")
            if suffix.isdigit():
                approved.add(int(suffix))
    remaining = [item for item in result.get("reviews", []) if item.get("segment_id") not in approved]
    updated = dict(result)
    updated["reviews"] = remaining
    updated["review_count"] = len(remaining)
    updated["status"] = "PASS" if not remaining else "REVIEW"
    return updated


def check_scene_modes(data: dict[str, Any]) -> tuple[str, list[str]]:
    issues: list[str] = []
    for scene in data.get("scenes", []):
        scene_id = int(scene.get("id", 0))
        mode = str(scene.get("render_mode") or "template")
        if mode not in VALID_MODES:
            issues.append(f"scene {scene_id:03d}: invalid render_mode {mode}")
        assets = scene.get("official_asset") or []
        if mode in {"official", "hybrid"} and not assets:
            issues.append(f"scene {scene_id:03d}: {mode} requires official_asset")
    return ("PASS" if not issues else "FAIL"), issues


def check_item_counts(data: dict[str, Any]) -> tuple[str, list[str]]:
    """ナレーションで明示する項目数と画面のitems数が一致するか（REVIEW扱い）。"""
    issues = narration_item_count_issues(data)
    return ("PASS" if not issues else "REVIEW"), issues


def gate_overall(checks: list[dict[str, Any]]) -> str:
    statuses = [item["status"] for item in checks]
    if any(status in {"FAIL", "MISSING"} for status in statuses):
        return "FAIL"
    if any(status in {"REVIEW", "WARN"} for status in statuses):
        return "REVIEW"
    return "PASS"


def write_gate_report(work_dir: Path, episode_name: str, checks: list[dict[str, Any]]) -> dict[str, Any]:
    overall = gate_overall(checks)
    result = {"episode": episode_name, "overall": overall, "checks": checks}
    json_path = work_dir / "production_preflight_phase2.json"
    md_path = work_dir / "production_preflight_phase2.md"
    work_dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [f"# Phase 2 production preflight — {episode_name}", "", "| Gate | Status | Detail |", "|---|---|---|"]
    for item in checks:
        detail = " / ".join(str(value) for value in item.get("details", [])) or "—"
        lines.append(f"| {item['name']} | {item['status']} | {detail.replace('|', '／')} |")
    lines.extend(["", f"Overall: **{overall}**", "", "REVIEW / WARN / FAIL / MISSING がある場合は build を停止する。"])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    result["json_path"], result["md_path"] = str(json_path), str(md_path)
    return result


def run_phase_a(episode_path: Path, data: dict[str, Any], work_dir: Path, ai_dir: Path, offline: bool) -> dict[str, Any]:
    episode_dir = episode_path.parent
    review = read_review(work_dir / "human_review.json")
    schema_issues = validate_episode(data)
    source_status, source_issues = check_sources(data) if not schema_issues else ("FAIL", ["schema invalid"])
    scene_status, scene_issues = check_scenes(data) if not schema_issues else ("FAIL", ["schema invalid"])
    asset_status, asset_issues, asset_count = check_official_assets(data, episode_dir) if not schema_issues else ("FAIL", ["schema invalid"], 0)
    mode_status, mode_issues = check_scene_modes(data)

    subtitle = run_subtitle_preflight(episode_path, work_dir / "subtitle_preflight.md") if not schema_issues else {"status": "FAIL", "fail_count": 1, "warn_count": 0}
    pronunciation = run_voicevox_preflight(episode_path, work_dir / "pronunciation_preflight.md", offline=offline) if not schema_issues else {"status": "REVIEW", "review_count": 1, "reviews": []}
    pronunciation = apply_pronunciation_review(pronunciation, review)
    ai = validate_ai_images(data, ai_dir)
    ai_gate_status = ai["status"]
    ai_gate_details = ai["missing"] + ai["invalid"] + ai["safe_area_warnings"]
    # Visual Gate v3 already approved these exact ImageGen assets.  The
    # renderer's safe-area sampler can still flag non-text background content
    # in the bottom 180px; retain that evidence and defer the final readability
    # decision to the requested draft Human Gate.  Missing or broken assets are
    # never waived.
    if (
        ai["status"] == "REVIEW"
        and not ai["missing"]
        and not ai["invalid"]
        and ai["safe_area_warnings"]
        and str(data.get("phase_a", {}).get("visual_gate_decision") or "")
        == "APPROVED_HUMAN_VISUAL_GATE_V3"
    ):
        ai_gate_status = "PASS"
        ai_gate_details = [
            "Visual Gate v3 APPROVED; safe-area background warning retained for draft Human Gate"
        ] + ai["safe_area_warnings"]
        ai["build_gate_status"] = "PASS_HUMAN_VISUAL_GATE_SAFE_AREA_RECHECK_PENDING"
    checks = [
        {"name": "episode schema", "status": "PASS" if not schema_issues else "FAIL", "details": schema_issues},
        {"name": "sources", "status": source_status, "details": source_issues},
        {"name": "subtitles", "status": subtitle["status"], "details": [f"fail={subtitle.get('fail_count', 0)} warn={subtitle.get('warn_count', 0)}"]},
        {"name": "pronunciation", "status": pronunciation["status"], "details": [f"remaining review={pronunciation.get('review_count', 0)}"]},
        {"name": "scenes", "status": scene_status, "details": scene_issues},
        {"name": "scene modes", "status": mode_status, "details": mode_issues},
        {"name": "item counts", "status": check_item_counts(data)[0], "details": check_item_counts(data)[1]},
        {"name": "official assets", "status": asset_status, "details": asset_issues + [f"declared={asset_count}"]},
        {"name": "GPT image assets", "status": ai_gate_status, "details": ai_gate_details},
    ]
    result = write_gate_report(work_dir, episode_path.parent.name, checks)
    result.update({"subtitle": subtitle, "pronunciation": pronunciation, "ai": ai})
    return result


def paths_for(episode_path: Path, work_override: Path | None, ai_override: Path | None) -> dict[str, Path]:
    episode_dir = episode_path.parent
    work = (work_override or episode_dir / "work").resolve()
    isolated = work_override is not None
    return {
        "work": work,
        "ai": (ai_override or ((work / "assets" / "generated_ai") if isolated else (episode_dir / "assets" / "generated_ai"))).resolve(),
        "template": ((work / "assets" / "generated_template") if isolated else (episode_dir / "assets" / "generated_template")).resolve(),
        "final_scenes": (work / "rendered_final_scenes").resolve(),
        "output": ((work / "output") if isolated else (episode_dir / "output")).resolve(),
        "audio": ((work / "audio" / "voicevox_kenzaki") if isolated else (episode_dir / "audio" / "voicevox_kenzaki")).resolve(),
    }


def resolve_postroll_asset(value: Any, episode_dir: Path) -> Path:
    """Resolve episode-local work/output assets before repository-root paths."""
    path = Path(str(value or ""))
    if path.is_absolute():
        return path
    local = (episode_dir / path).resolve()
    if local.exists() or (path.parts and path.parts[0] in {"work", "output", "assets", "audio", "raw", "thumbnail", "final"}):
        return local
    return (ROOT / path).resolve()


def ensure_declared_cta(data: dict[str, Any], episode_dir: Path) -> dict[str, Any]:
    """Generate a missing declared common CTA without touching episode.json."""
    postroll = data.get("postroll")
    if not isinstance(postroll, dict) or postroll.get("cta_profile") != "channel_common_cta":
        return data
    if not postroll.get("asset"):
        postroll["asset"] = "work/channel_cta.png"
    target = resolve_postroll_asset(postroll["asset"], episode_dir)
    if not target.exists():
        build_cta(output_path=target)
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode")
    parser.add_argument("--continue", dest="continue_build", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--use-advisor", action="store_true")
    parser.add_argument("--work-dir", type=Path)
    parser.add_argument("--ai-dir", type=Path)
    parser.add_argument("--offline-voicevox", action="store_true")
    parser.add_argument("--engine-url", default="http://127.0.0.1:50021")
    parser.add_argument("--rerender-scene", type=int)
    parser.add_argument("--regen-segment", type=int)
    parser.add_argument("--output-name", default="draft_auto_v1.mp4")
    parser.add_argument("--review-name", default="scene_contact_sheet.png")
    parser.add_argument("--finalize", action="store_true")
    args = parser.parse_args()

    episode_path = resolve_episode(args.episode)
    data = apply_episode_defaults(load_json(episode_path))
    paths = paths_for(episode_path, args.work_dir, args.ai_dir)
    paths["work"].mkdir(parents=True, exist_ok=True)
    if args.use_advisor:
        advisory = advise_episode(data)
        write_reports(
            advisory,
            paths["work"] / "scene_mode_advisor.json",
            paths["work"] / "scene_mode_advisor.md",
        )
        by_id = {int(str(row["scene_id"]).split("-")[-1]): row for row in advisory}
        for scene in data.get("scenes", []):
            scene["render_mode"] = by_id[int(scene["id"])]["recommended_mode"]
    from build_image_generation_manifest import manifest_rows
    data = ensure_declared_cta(data, episode_path.parent)
    manifest = manifest_rows(data)
    write_manifest(
        manifest,
        paths["work"] / "image_generation_manifest.json",
        paths["work"] / "image_generation_manifest.md",
    )
    metrics_path = paths["work"] / "production_metrics.json"
    metrics = load_or_create(metrics_path, str(data.get("episode", {}).get("episode_id") or episode_path.parent.name[:3]), len(manifest))
    metrics["gpt_image_count"] = len(manifest)
    gate = run_phase_a(episode_path, data, paths["work"], paths["ai"], args.offline_voicevox)
    metrics["pronunciation_review_count"] = int(gate.get("pronunciation", {}).get("review_count", 0))
    if gate["overall"] == "PASS" and not metrics.get("phase_a_completed"):
        metrics["phase_a_completed"] = now_iso()
    save_metrics(metrics_path, metrics)
    print(f"Phase A: {gate['overall']}")
    print(f"report: {gate['md_path']}")
    if gate["ai"]["missing"]:
        print("GPT IMAGE ASSETS REQUIRED")
        for name in gate["ai"]["missing"]:
            print(f"- {name}")
        print(f"Generate these images with ChatGPT and place them in: {paths['ai']}")
    if args.dry_run or gate["overall"] != "PASS":
        print("STOP: Phase A gate requires human correction/review.")
        return 2 if gate["overall"] == "REVIEW" else 1 if gate["overall"] == "FAIL" else 0

    if args.finalize:
        review_path = paths["work"] / "human_review.json"
        review = read_review(review_path)
        approved_name = approved_draft_filename(review)
        allowed, reason = finalize_allowed(review_path, paths["output"])
        draft = paths["output"] / approved_name if approved_name else paths["output"] / "__no_approved_draft__.mp4"
        final = paths["output"] / "final.mp4"
        existing_finals = list(episode_path.parent.rglob("final.mp4"))
        if not allowed or not draft.exists() or existing_finals:
            print(f"STOP: finalize denied ({reason}; draft={draft.exists()}; existing_finals={len(existing_finals)})")
            return 1
        final.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(draft, final)
        metrics["final_version"] = approved_name
        metrics["finalize_time"] = now_iso()
        save_metrics(metrics_path, metrics)
        print(final)
        return 0

    render = render_episode_scenes(episode_path, data, paths["ai"], paths["template"], paths["final_scenes"], args.rerender_scene)
    if render["status"] != "PASS":
        print("STOP: scene render failed: " + "; ".join(render["errors"]))
        return 1
    if args.rerender_scene:
        print(f"Re-rendered scene {args.rerender_scene:03d}")
        return 0

    review_dir = paths["output"] / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(paths["final_scenes"] / "scene_contact_sheet.png", review_dir / args.review_name)

    voice = generate_incremental(
        data, episode_path.parent, paths["work"], args.engine_url, args.regen_segment,
        audio_dir=paths["audio"],
    )
    timing = paths["work"] / "audio_timing.json"
    srt, ass = paths["work"] / "captions_auto.srt", paths["work"] / "captions_auto.ass"
    build_from_files(data, timing, srt, ass)
    audio = paths["audio"] / "narration_kenzaki_auto.wav"
    draft = paths["output"] / args.output_name
    if draft.exists():
        print(f"STOP: draft already exists; choose a new --output-name to preserve version history: {draft}")
        return 1
    postroll = data.get("postroll") or {}
    cta_audio: Path | None = None
    if postroll.get("cta_audio"):
        cta_audio = resolve_postroll_asset(postroll["cta_audio"], episode_path.parent)
    cta_trailing = float(postroll.get("trailing_seconds") or 1.0)
    video = build_video(
        data,
        paths["final_scenes"],
        timing,
        audio,
        ass,
        paths["work"],
        draft,
        cta_audio_path=cta_audio,
        cta_trailing=cta_trailing,
    )
    if video["status"] != "PASS":
        print("STOP: " + "; ".join(video["errors"]))
        return 1
    qa = run_qa(data, paths["final_scenes"], timing, draft, paths["work"] / "phase2_qa", audio)
    if video["status"] == "PASS":
        version_name = args.output_name
        versions = metrics.setdefault("draft_versions", [])
        if version_name not in versions:
            versions.append(version_name)
        metrics["human_audio_override_used"] = voice.get("human_overrides", [])
        metrics["automatic_regeneration_count"] = len(voice.get("planned", []))
        if version_name == "draft_auto_v1.mp4" and not metrics.get("draft_v1_completed"):
            metrics["draft_v1_completed"] = now_iso()
        save_metrics(metrics_path, metrics)
    print(
        f"audio regenerated={voice['planned']} reused={len(voice['skipped'])} "
        f"human_overrides={voice.get('human_overrides', [])}"
    )
    print(f"draft={draft}")
    print(f"QA={qa['status']}")
    return 0 if qa["status"] == "PASS" else 2 if qa["status"] == "WARN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
