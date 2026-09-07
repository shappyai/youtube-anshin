"""Recommend template/official/gpt_image/hybrid for episode scenes.

Recommendations never mutate episode.json.  Use --fixture-output to create a
reviewable copy with the recommendations applied.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from episode_io import load_json, validate_episode  # noqa: E402

MODES = ("template", "official", "gpt_image", "hybrid")
SHORT_TEXT_LIMIT = 48  # headline+support_text がこの文字数以下なら imagegen_native 向き
TEMPLATE_LAYOUTS = {"layout_02_list", "layout_05_compare", "layout_07_summary"}
VISUAL_LAYOUTS = {"layout_01_hero", "layout_03_visual_text", "layout_06_caution", "layout_08_section"}
CONCEPT_TERMS = (
    "とは", "概念", "仕組み", "たとえ", "比喩", "冒頭", "安心", "慌て", "怖",
    "詐欺", "偽サイト", "注意", "結論", "まとめると", "一緒に", "確認しましょう",
)
OFFICIAL_TERMS = (
    "設定", "画面", "App Store", "Google Play", "公式", "FAQ", "対応OS", "NFC",
    "ログイン", "利用登録", "掲載", "提供元", "発表", "暗証番号", "ストア",
)


def scene_text(scene: dict[str, Any]) -> str:
    values = [scene.get("headline"), scene.get("support_text"), scene.get("main_message")]
    values.extend(scene.get("items") or [])
    return " ".join(str(value or "") for value in values)


def recommend_scene_mode(scene: dict[str, Any]) -> dict[str, Any]:
    text = scene_text(scene)
    layout = str(scene.get("layout") or "")
    assets = scene.get("official_asset") or []
    has_official = bool(assets)
    concept_hits = [term for term in CONCEPT_TERMS if term in text]
    official_hits = [term for term in OFFICIAL_TERMS if term in text]
    reasons: list[str] = []

    if has_official and (concept_hits or layout in {"layout_01_hero", "layout_03_visual_text", "layout_06_caution"}):
        mode = "hybrid"
        reasons.extend(["見た目の主役が必要", "公式素材を同時に提示"])
    elif has_official:
        mode = "official"
        reasons.append("正確な公式画面・文言を優先")
    elif official_hits:
        mode = "template"
        reasons.append("公式性が必要だが素材未指定のため、捏造しないtemplateを使用")
    elif layout in TEMPLATE_LAYOUTS:
        mode = "template"
        reasons.append("一覧・比較・まとめはtemplate向き")
    elif concept_hits or layout in VISUAL_LAYOUTS:
        mode = "gpt_image"
        reasons.append("概念・注意・章扉を視覚中心で説明")
    else:
        mode = "template"
        reasons.append("既存layoutで十分に伝達可能")

    # A plain comparison/list stays template unless it actually carries official evidence.
    if layout in TEMPLATE_LAYOUTS and not has_official:
        mode = "template"
    return {
        "scene_id": f"SCENE-{int(scene['id']):03d}",
        "recommended_mode": mode,
        "current_mode": scene.get("render_mode"),
        "reasons": reasons,
        "recommended_text_render_mode": recommend_text_render_mode(scene, mode),
        "concept_hits": concept_hits,
        "official_hits": official_hits,
    }


def recommend_text_render_mode(scene: dict[str, Any], render_mode: str) -> str:
    """Recommend imagegen_native / pil_overlay / no_text for a scene.

    Official quotes, steps, URLs, numbers, dates, PINs and long text are
    deterministic by nature and stay pil_overlay only in renderer-native
    scenes. Generated-image scenes must never be recommended as a large
    post-render text overlay hybrid.
    """
    if render_mode in {"template", "official"}:
        return "pil_overlay"
    headline = str(scene.get("headline") or "").strip()
    support = str(scene.get("support_text") or "").strip()
    if not headline and not support:
        return "no_text"
    if render_mode in {"gpt_image", "hybrid"}:
        # NO_IMAGE_TEXT_HYBRID: use ImageGen-native text or no text. If exact
        # text is too long/strict, change the scene mode to template/official
        # instead of layering a large overlay on generated art.
        return "imagegen_native"
    combined = headline + support
    if re.search(r"[0-9０-９]", combined) or "http" in combined.lower() or "www" in combined.lower() or "pin" in combined.lower():
        # 数字・URL・PIN等は1文字の誤りも許容できないため正確性重視
        return "pil_overlay"
    if len(combined) <= SHORT_TEXT_LIMIT:
        return "imagegen_native"
    return "pil_overlay"


def advise_episode(data: dict[str, Any]) -> list[dict[str, Any]]:
    return [recommend_scene_mode(scene) for scene in data.get("scenes", [])]


def write_reports(rows: list[dict[str, Any]], json_path: Path | None, md_path: Path | None) -> None:
    counts = Counter(row["recommended_mode"] for row in rows)
    text_counts = Counter(row.get("recommended_text_render_mode") or "" for row in rows)
    payload = {
        "counts": {mode: counts.get(mode, 0) for mode in MODES},
        "text_render_mode_counts": dict(text_counts),
        "scenes": rows,
    }
    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if md_path:
        lines = ["# Scene mode advisor", "", "| Scene | Current | Recommended | Text render | Reason |", "|---|---|---|---|---|"]
        for row in rows:
            lines.append(
                f"| {row['scene_id']} | {row['current_mode'] or '未指定'} | "
                f"{row['recommended_mode']} | {row.get('recommended_text_render_mode') or '-'} | "
                f"{' / '.join(row['reasons'])} |"
            )
        lines.extend(["", "## Count", ""] + [f"- {mode}: {counts.get(mode, 0)}" for mode in MODES])
        lines.extend(["", "## Text render mode count", ""] + [f"- {mode}: {text_counts.get(mode, 0)}" for mode in ("imagegen_native", "pil_overlay", "no_text") if text_counts.get(mode)])
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("episode", type=Path)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--markdown", type=Path)
    parser.add_argument("--fixture-output", type=Path, help="write a copy with recommendations; never edits the source")
    args = parser.parse_args()
    data = load_json(args.episode.resolve())
    issues = validate_episode(data)
    if issues:
        raise SystemExit("episode.json validation failed:\n- " + "\n- ".join(issues))
    rows = advise_episode(data)
    counts = Counter(row["recommended_mode"] for row in rows)
    work = args.episode.parent / "work"
    write_reports(rows, (args.json or work / "scene_mode_advisor.json").resolve(), (args.markdown or work / "scene_mode_advisor.md").resolve())
    if args.fixture_output:
        fixture = json.loads(json.dumps(data, ensure_ascii=False))
        by_id = {row["scene_id"]: row for row in rows}
        for scene in fixture["scenes"]:
            row = by_id[f"SCENE-{int(scene['id']):03d}"]
            scene["render_mode"] = row["recommended_mode"]
            scene.setdefault("text_render_mode", row["recommended_text_render_mode"])
        args.fixture_output.parent.mkdir(parents=True, exist_ok=True)
        args.fixture_output.write_text(json.dumps(fixture, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(" ".join(f"{mode}={counts.get(mode, 0)}" for mode in MODES))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
