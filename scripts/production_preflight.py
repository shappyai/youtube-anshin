"""Run the episode.json production checks as one gate."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from episode_io import ROOT, asset_path_from_item, episode_dir_from_path, load_json, validate_episode  # noqa: E402
from subtitle_preflight import run_preflight as run_subtitle_preflight  # noqa: E402
from voicevox_preflight import run_preflight as run_voicevox_preflight  # noqa: E402
from viewer_facing_text_qa import run_scan as run_viewer_facing_text_scan  # noqa: E402


def check_sources(data: dict[str, Any]) -> tuple[str, list[str]]:
    issues: list[str] = []
    sources = data.get("sources", [])
    if not sources:
        issues.append("sourcesが空です")
    seen: set[str] = set()
    for index, source in enumerate(sources, 1):
        if not isinstance(source, dict):
            issues.append(f"sources[{index}]がobjectではありません")
            continue
        source_id = str(source.get("source_id", ""))
        if source_id in seen:
            issues.append(f"{source_id}が重複しています")
        seen.add(source_id)
        url = str(source.get("url", ""))
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            issues.append(f"{source_id or index}: URLが不正です")
        for key in ("title", "organization", "verified_at", "claim"):
            if not str(source.get(key, "")).strip():
                issues.append(f"{source_id or index}: {key}が空です")
    return ("PASS" if not issues else "FAIL"), issues


def check_scenes(data: dict[str, Any]) -> tuple[str, list[str]]:
    issues: list[str] = []
    segments = {int(segment["id"]) for segment in data.get("narration_segments", []) if isinstance(segment, dict) and isinstance(segment.get("id"), int)}
    subtitle_ids = {str(subtitle["id"]) for subtitle in data.get("subtitles", []) if isinstance(subtitle, dict)}
    scene_ids: set[int] = set()
    for scene in data.get("scenes", []):
        if not isinstance(scene, dict):
            issues.append("sceneがobjectではありません")
            continue
        scene_id = scene.get("id")
        if not isinstance(scene_id, int):
            issues.append("scene idが整数ではありません")
            continue
        if scene_id in scene_ids:
            issues.append(f"scene {scene_id:03d}が重複しています")
        scene_ids.add(scene_id)
        layout = str(scene.get("layout", ""))
        if not re.fullmatch(r"layout_\d{2}_[a-z_]+", layout):
            issues.append(f"scene {scene_id:03d}: layoutが不正です ({layout})")
        if not (ROOT / "templates" / "scenes" / f"{layout}.html").exists():
            issues.append(f"scene {scene_id:03d}: templateがありません ({layout})")
        start, end = scene.get("start_segment"), scene.get("end_segment")
        if not isinstance(start, int) or not isinstance(end, int) or start > end:
            issues.append(f"scene {scene_id:03d}: segment範囲が不正です")
        elif any(value not in segments for value in range(start, end + 1)):
            issues.append(f"scene {scene_id:03d}: narration segment参照が不正です")
        for subtitle_id in scene.get("subtitle_ids", []):
            if subtitle_id not in subtitle_ids:
                issues.append(f"scene {scene_id:03d}: {subtitle_id}が見つかりません")
    return ("PASS" if not issues else "FAIL"), issues


def check_official_assets(data: dict[str, Any], episode_dir: Path) -> tuple[str, list[str], int]:
    issues: list[str] = []
    count = 0
    for scene in data.get("scenes", []):
        scene_id = int(scene.get("id", 0))
        assets = scene.get("official_asset") or []
        crops = scene.get("official_asset_crop") or []
        count += len(assets)
        slot = scene.get("official_asset_slot") or {}
        capture_statuses = {
            str(scene.get("official_capture_status") or "").strip().lower(),
            str(scene.get("official_visual_status") or "").strip().lower(),
            str(slot.get("status") or "").strip().lower() if isinstance(slot, dict) else "",
        }
        if "official_capture_failed" in capture_statuses:
            # Fail closed: a partial extraction/OCR result must never pass as
            # an official visual.  Recovery must explicitly choose a real
            # official asset, exact quote, or semantic scene first.
            issues.append(
                f"scene {scene_id:03d}: official_capture_failed（公式素材を描画せず再取得またはsemantic sceneへ切替）"
            )
        if not isinstance(assets, list):
            issues.append(f"scene {scene_id:03d}: official_assetが配列ではありません")
            continue
        for index, asset in enumerate(assets):
            if not isinstance(asset, dict):
                issues.append(f"scene {scene_id:03d} asset {index}: objectではありません")
                continue
            if str(asset.get("status") or asset.get("capture_status") or "").strip().lower() == "official_capture_failed":
                issues.append(
                    f"scene {scene_id:03d} asset {index}: official_capture_failed（部分抽出テキストを公式素材として使用不可）"
                )
            kind = asset.get("kind")
            if kind == "image":
                path = asset_path_from_item(asset, episode_dir)
                if path is None or not path.exists():
                    issues.append(f"scene {scene_id:03d} asset {index}: 未配置 {asset.get('path')}")
            elif kind == "quote":
                if not str(asset.get("text", "")).strip() or not str(asset.get("source", "")).strip():
                    issues.append(f"scene {scene_id:03d} asset {index}: quoteのtext/sourceが不足")
            elif kind == "placeholder":
                issues.append(f"scene {scene_id:03d} asset {index}: placeholderはFAIL")
            else:
                issues.append(f"scene {scene_id:03d} asset {index}: kindが不正です ({kind})")
        if not isinstance(crops, list):
            issues.append(f"scene {scene_id:03d}: official_asset_cropが配列ではありません")
            continue
        for crop in crops:
            if not isinstance(crop, dict) or not isinstance(crop.get("asset_index"), int):
                issues.append(f"scene {scene_id:03d}: cropのasset_indexが不正です")
                continue
            if crop["asset_index"] >= len(assets):
                issues.append(f"scene {scene_id:03d}: cropのasset_indexが範囲外です")
            box = crop.get("box")
            if box is not None and (
                not isinstance(box, list)
                or len(box) != 4
                or any(not isinstance(value, int) or value < 0 for value in box)
                or box[2] <= box[0]
                or box[3] <= box[1]
            ):
                issues.append(f"scene {scene_id:03d}: crop boxが不正です")
    return ("PASS" if not issues else "FAIL"), issues, count


def write_report(
    report_path: Path,
    episode_name: str,
    checks: list[tuple[str, str, list[str]]],
) -> None:
    lines = [f"# Production preflight — {episode_name}", ""]
    for name, status, issues in checks:
        lines.append(f"- {name}: {status}")
        lines.extend(f"  - {issue}" for issue in issues)
    lines.extend(["", "REVIEW / FAIL がある場合は build を停止する。"])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_preflight(
    episode_path: Path,
    report_path: Path,
    offline_voicevox: bool = False,
) -> dict[str, Any]:
    data = load_json(episode_path)
    schema_issues = validate_episode(data)
    if schema_issues:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            "# Production preflight\n\n- episode.json: FAIL\n"
            + "".join(f"  - {issue}\n" for issue in schema_issues),
            encoding="utf-8",
        )
        return {
            "episode_id": str(data.get("episode", {}).get("episode_id", "?")),
            "overall": "FAIL",
            "checks": [("episode.json", "FAIL", schema_issues)],
        }

    episode_dir = episode_dir_from_path(episode_path)
    source_status, source_issues = check_sources(data)
    scene_status, scene_issues = check_scenes(data)
    asset_status, asset_issues, asset_count = check_official_assets(data, episode_dir)

    subtitle_report = episode_dir / "work" / "subtitle_preflight.md"
    subtitle = run_subtitle_preflight(episode_path, subtitle_report)
    pronunciation_report = episode_dir / "work" / "pronunciation_preflight.md"
    pronunciation = run_voicevox_preflight(
        episode_path,
        pronunciation_report,
        offline=offline_voicevox,
    )
    viewer_facing = run_viewer_facing_text_scan(
        episode_path,
        episode_dir / "work" / "viewer_facing_internal_brand_promise.md",
        episode_dir / "work" / "viewer_facing_internal_brand_promise.json",
    )

    checks: list[tuple[str, str, list[str]]] = [
        ("episode.json", "PASS", []),
        ("sources", source_status, source_issues),
        ("scenes", scene_status, scene_issues),
        ("official assets", asset_status, asset_issues + [f"declared asset count: {asset_count}"] if asset_status == "PASS" else asset_issues),
        (
            "subtitles",
            subtitle["status"],
            [f"fail={subtitle['fail_count']} warn={subtitle['warn_count']}"],
        ),
        (
            "pronunciation",
            pronunciation["status"],
            [f"review={pronunciation['review_count']} queries={pronunciation['query_count']}/{pronunciation['segment_count']}"],
        ),
        (
            "viewer-facing internal brand promise",
            viewer_facing["status"],
            [f"viewer_facing_internal_brand_promise={viewer_facing['viewer_facing_count']} expected=0"],
        ),
    ]
    statuses = [status for _name, status, _issues in checks]
    overall = "FAIL" if "FAIL" in statuses else "REVIEW" if "REVIEW" in statuses else "WARN" if "WARN" in statuses else "PASS"
    write_report(report_path, episode_path.parent.name, checks)
    return {
        "episode_id": str(data["episode"]["episode_id"]),
        "overall": overall,
        "checks": checks,
        "asset_count": asset_count,
        "subtitle": subtitle,
        "pronunciation": pronunciation,
        "report_path": str(report_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("episode", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--offline-voicevox", action="store_true", help="skip HTTP while still running dictionary/context checks")
    args = parser.parse_args()
    report = args.report or args.episode.parent / "work" / "production_preflight.md"
    result = run_preflight(args.episode.resolve(), report.resolve(), args.offline_voicevox)
    print(f"Episode {result.get('episode_id', '?')} Preflight")
    for name, status, issues in result.get("checks", []):
        detail = f" ({'; '.join(issues)})" if issues else ""
        print(f"{name:<20} {status}{detail}")
    print(f"overall              {result['overall']}")
    print(f"report               {result['report_path']}")
    return 1 if result["overall"] == "FAIL" else 2 if result["overall"] == "REVIEW" else 0


if __name__ == "__main__":
    raise SystemExit(main())
