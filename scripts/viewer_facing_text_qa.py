"""Detect the internal brand promise in viewer-facing episode/Shorts assets.

The channel brand promise may remain in internal planning and production
documents, but it must never enter a completed video, subtitle, CTA,
thumbnail/end-card metadata, or other viewer-facing text. This checker is a
text/metadata gate; raster-image visual text remains covered by the existing
ImageGen text QA and human visual gate.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable

RULE_NAME = "viewer_facing_internal_brand_promise"
INTERNAL_BRAND_PROMISE = "怖がらせる前に、確認する。"
_COMPACT_PROMISE = re.sub(r"\s+", "", INTERNAL_BRAND_PROMISE)


def _has_promise(value: str) -> bool:
    if INTERNAL_BRAND_PROMISE in value:
        return True
    compact = re.sub(r"[\s\u3000]", "", value)
    return _COMPACT_PROMISE in compact


def _iter_strings(value: Any, path: str) -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            next_path = f"{path}.{key}" if path else str(key)
            yield from _iter_strings(child, next_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _iter_strings(child, f"{path}[{index}]")
    elif isinstance(value, str):
        yield path, value


def _add_hits(hits: list[dict[str, str]], source: str, field: str, value: str) -> None:
    if _has_promise(value):
        hits.append({"source": source, "field": field, "match": INTERNAL_BRAND_PROMISE})


def _add_fields(
    hits: list[dict[str, str]],
    source: str,
    obj: dict[str, Any],
    keys: set[str],
    prefix: str,
) -> None:
    for key in keys:
        if key not in obj:
            continue
        for field, value in _iter_strings(obj[key], f"{prefix}.{key}"):
            _add_hits(hits, source, field, value)


def _scan_episode(episode_json: Path) -> tuple[list[dict[str, str]], list[str]]:
    data = json.loads(episode_json.read_text(encoding="utf-8"))
    hits: list[dict[str, str]] = []
    coverage: list[str] = []
    source = str(episode_json)

    episode = data.get("episode") if isinstance(data.get("episode"), dict) else {}
    _add_fields(
        hits,
        source,
        episode,
        {"title", "description", "viewer_facing_title", "thumbnail_text", "cta_text"},
        "episode",
    )
    coverage.append("episode title/description metadata")

    scene_keys = {
        "headline", "support_text", "main_message", "section_label", "items",
        "body", "text", "display_text", "visible_text", "overlay_text", "caption",
        "quote", "steps", "labels", "columns", "rows", "cards", "compare_cards",
        "official_asset", "image_prompt", "imagegen_prompt", "generated_text",
    }
    for scene in data.get("scenes", []):
        if not isinstance(scene, dict):
            continue
        scene_id = scene.get("id", "?")
        _add_fields(hits, source, scene, scene_keys, f"scene[{scene_id}]")
    coverage.append("scene renderer text and ImageGen prompt/generated-text metadata")

    for segment in data.get("narration_segments", []):
        if isinstance(segment, dict):
            _add_fields(
                hits,
                source,
                segment,
                {"narration", "spoken_text", "display_text", "subtitle_text"},
                f"narration_segment[{segment.get('id', '?')}]",
            )
    for subtitle in data.get("subtitles", []):
        if isinstance(subtitle, dict):
            _add_fields(
                hits,
                source,
                subtitle,
                {"text_lines", "display_text", "text", "caption"},
                f"subtitle[{subtitle.get('id', '?')}]",
            )
    coverage.append("narration and subtitle canonical text")

    postroll = data.get("postroll")
    if isinstance(postroll, dict):
        _add_fields(
            hits,
            source,
            postroll,
            {"canonical_text", "narration", "spoken_text", "display_text", "text", "cta_text"},
            "postroll",
        )
    coverage.append("CTA/end-card canonical text")

    episode_dir = episode_json.parent
    for relative in ("captions.srt", "captions.ass"):
        path = episode_dir / relative
        if path.exists():
            _add_hits(hits, str(path), "file", path.read_text(encoding="utf-8", errors="replace"))
    coverage.append("subtitle and overlay files; narration is checked from episode.json")

    # These are viewer-facing candidate metadata or exact text specifications.
    # Internal review reports and metadata.brand_promise are deliberately not
    # included: they are allowed to document the rule itself.
    candidate_files = [
        episode_dir / "publish.json",
        episode_dir / "work" / "image_generation_manifest.json",
        episode_dir / "work" / "cta_registration_conversion_v1.json",
    ]
    candidate_files.extend(sorted((episode_dir / "work").glob("thumbnail*.json")))
    candidate_files.extend(sorted((episode_dir / "work").glob("end_screen*.json")))
    for path in candidate_files:
        if not path.exists():
            continue
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if path.name == "publish.json":
            visible_keys = {
                "selected_title", "title", "description", "chapters", "tags",
                "voice_credit", "thumbnail_text", "thumbnail_title", "cta_text",
                "canonical_text", "display_text", "end_screen_candidates",
            }
            _add_fields(hits, str(path), obj, visible_keys, "publish")
        else:
            for field, value in _iter_strings(obj, path.stem):
                _add_hits(hits, str(path), field, value)
    coverage.append("publish description, thumbnail metadata, end-card metadata, and CTA/ImageGen manifests")
    return hits, coverage


def _scan_short(short_json: Path) -> tuple[list[dict[str, str]], list[str]]:
    data = json.loads(short_json.read_text(encoding="utf-8"))
    hits: list[dict[str, str]] = []
    coverage = ["Shorts title/script/caption metadata"]
    source = str(short_json)
    visible_keys = {
        "title", "title_provisional", "headline", "main_message", "support_text",
        "narration", "spoken_text", "display_text", "caption", "captions",
        "subtitle", "subtitles", "text", "text_lines", "cta_text", "thumbnail_text",
    }
    _add_fields(hits, source, data, visible_keys, "short")
    short_dir = short_json.parent
    for relative in ("captions.srt", "captions.ass"):
        path = short_dir / relative
        if path.exists():
            _add_hits(hits, str(path), "file", path.read_text(encoding="utf-8", errors="replace"))
    for path in sorted((short_dir / "work").glob("*manifest*.json")):
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for field, value in _iter_strings(obj, path.stem):
            _add_hits(hits, str(path), field, value)
    coverage.append("Shorts render/ImageGen manifests and overlay files")
    return hits, coverage


def _scan_one(content_json: Path) -> dict[str, Any]:
    if content_json.name == "episode.json":
        hits, coverage = _scan_episode(content_json)
        kind = "episode"
    elif content_json.name == "short.json":
        hits, coverage = _scan_short(content_json)
        kind = "short"
    else:
        raise ValueError(f"Expected episode.json or short.json: {content_json}")
    return {
        "kind": kind,
        "path": str(content_json),
        "rule": RULE_NAME,
        "internal_brand_promise": INTERNAL_BRAND_PROMISE,
        "classification": "INTERNAL_ONLY",
        "viewer_facing_expected_count": 0,
        "viewer_facing_count": len(hits),
        "status": "PASS" if not hits else "FAIL",
        "coverage": coverage,
        "hits": hits,
    }


def _resolve_content_targets(target: Path) -> list[Path]:
    target = target.resolve()
    if target.is_file():
        return [target]
    if (target / "episode.json").exists():
        return [target / "episode.json"]
    if (target / "short.json").exists():
        return [target / "short.json"]
    return sorted(target.glob("episodes/*/episode.json")) + sorted(target.glob("shorts/*/short.json"))


def run_scan(
    target: Path,
    report_path: Path | None = None,
    json_path: Path | None = None,
) -> dict[str, Any]:
    targets = _resolve_content_targets(target)
    if not targets:
        raise ValueError(f"No episode.json or short.json found under {target}")
    results = [_scan_one(path) for path in targets]
    hits = [hit for result in results for hit in result["hits"]]
    payload: dict[str, Any] = {
        "rule": RULE_NAME,
        "internal_brand_promise": INTERNAL_BRAND_PROMISE,
        "classification": "INTERNAL_ONLY",
        "viewer_facing_expected_count": 0,
        "viewer_facing_count": len(hits),
        "status": "PASS" if not hits else "FAIL",
        "targets": results,
    }
    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Viewer-facing internal brand promise QA",
            "",
            f"- rule: `{RULE_NAME}`",
            "- classification: `INTERNAL_ONLY`",
            "- viewer-facing expected count: `0`",
            f"- viewer-facing count: `{len(hits)}`",
            f"- status: **{payload['status']}**",
            "",
            "Internal planning/brand documents may contain the phrase. Viewer-facing scene text, prompts/text specs, subtitles, narration, CTA, thumbnail/end-card metadata, and overlay candidates may not.",
            "",
        ]
        for result in results:
            lines.append(f"## {result['kind']}: {result['path']}")
            lines.append("")
            lines.extend(f"- coverage: {item}" for item in result["coverage"])
            if result["hits"]:
                lines.append("")
                lines.append("### Violations")
                lines.extend(f"- `{hit['source']}` `{hit['field']}`" for hit in result["hits"])
            else:
                lines.append("- violations: none")
            lines.append("")
        report_path.write_text("\n".join(lines), encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("target", type=Path, help="episode.json, short.json, content directory, or repository root")
    parser.add_argument("--report", type=Path, help="Markdown report path")
    parser.add_argument("--json", type=Path, help="JSON report path")
    args = parser.parse_args()
    target = args.target.resolve()
    report = args.report
    json_path = args.json
    if report is None and target.is_file():
        report = target.parent / "work" / "viewer_facing_internal_brand_promise.md"
    if json_path is None and target.is_file():
        json_path = target.parent / "work" / "viewer_facing_internal_brand_promise.json"
    result = run_scan(target, report, json_path)
    print(f"{RULE_NAME}: {result['status']}")
    print(f"viewer-facing count: {result['viewer_facing_count']}")
    if report:
        print(f"report: {report.resolve()}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
