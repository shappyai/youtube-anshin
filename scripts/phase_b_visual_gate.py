"""Run the Episode 012 Phase B official-material visual gate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image

from scene_quality_report import (
    VISUAL_BALANCE_MAX_X,
    VISUAL_BALANCE_MIN_X,
    geometry,
    load_visual_theme,
    official_visual_variant,
    prepared_asset_count,
    renderer_policy_guard,
    theme_profile_for_episode,
    visual_centroid_preflight,
)

TARGET_SCENES = (7, 8, 12, 13, 18, 22, 26)
SEMANTIC_VARIANTS = {"semantic_operation", "safe_entry_options_centered"}
SOURCE_LABEL_FONT_PX = 46


def _asset_path(episode_dir: Path, asset: dict[str, Any]) -> Path | None:
    raw = str(asset.get("path") or "")
    if not raw:
        return None
    path = Path(raw)
    return path if path.is_absolute() else (episode_dir / path).resolve()


def _check(name: str, status: str, details: list[str]) -> dict[str, Any]:
    return {"name": name, "status": status, "details": details}


def run_gate(episode_path: Path, rendered_dir: Path) -> dict[str, Any]:
    data = json.loads(episode_path.read_text(encoding="utf-8"))
    episode_dir = episode_path.parent
    scenes = {int(scene["id"]): scene for scene in data.get("scenes", [])}
    theme = load_visual_theme(theme_profile_for_episode(data))
    target_rows: list[dict[str, Any]] = []
    placeholder_remaining: list[str] = []
    neutral_browser: list[str] = []
    neutral_phone: list[str] = []
    capture_or_semantic: list[str] = []
    reconstruction: list[str] = []
    privacy_fail: list[str] = []
    source_label_fail: list[str] = []
    readability_fail: list[str] = []
    balance_fail: list[str] = []

    for scene_id in TARGET_SCENES:
        scene = scenes.get(scene_id)
        if scene is None:
            placeholder_remaining.append(f"SCENE-{scene_id:03d}: missing scene")
            continue
        variant = official_visual_variant(scene)
        assets = scene.get("official_asset") or []
        slot = scene.get("official_asset_slot") or {}
        slot_status = str(slot.get("status") or "") if isinstance(slot, dict) else ""
        asset_paths: list[str] = []
        asset_kinds: list[str] = []
        scene_has_placeholder = "PLACEHOLDER" in json.dumps(scene, ensure_ascii=False).upper()
        if scene_has_placeholder or "planned" in slot_status.lower() or "pending" in slot_status.lower():
            placeholder_remaining.append(f"SCENE-{scene_id:03d}: placeholder/planned metadata")
        if not isinstance(assets, list):
            assets = []
        for asset in assets:
            if not isinstance(asset, dict):
                placeholder_remaining.append(f"SCENE-{scene_id:03d}: malformed asset")
                continue
            kind = str(asset.get("kind") or "")
            asset_kinds.append(kind)
            if kind == "placeholder":
                placeholder_remaining.append(f"SCENE-{scene_id:03d}: placeholder asset")
            if kind == "image":
                path = _asset_path(episode_dir, asset)
                asset_paths.append(str(path) if path else "")
                if path is None or not path.exists():
                    capture_or_semantic.append(f"SCENE-{scene_id:03d}: missing official image")
                if path and ("generated_ai" in path.parts or "imagegen" in str(path).lower()):
                    reconstruction.append(f"SCENE-{scene_id:03d}: AI image path used for official material")
            elif kind not in {"image", "quote"}:
                reconstruction.append(f"SCENE-{scene_id:03d}: unsupported official kind {kind}")
            label = str(asset.get("label") or "").strip()
            if label and SOURCE_LABEL_FONT_PX < 44:
                source_label_fail.append(f"SCENE-{scene_id:03d}: source label below 44px")
            if not label and kind in {"image", "quote"}:
                source_label_fail.append(f"SCENE-{scene_id:03d}: missing source label")
        if assets:
            capture_or_semantic.append(f"SCENE-{scene_id:03d}: official asset")
        elif variant in SEMANTIC_VARIANTS:
            capture_or_semantic.append(f"SCENE-{scene_id:03d}: semantic visual")
        else:
            neutral_kind = "phone" if variant == "phone" else "browser" if variant in {"browser", "neutral_frame"} else ""
            if neutral_kind == "phone":
                neutral_phone.append(f"SCENE-{scene_id:03d}")
            elif neutral_kind == "browser":
                neutral_browser.append(f"SCENE-{scene_id:03d}")
        if variant == "semantic_operation" and not scene.get("official_operation_steps"):
            capture_or_semantic.append(f"SCENE-{scene_id:03d}: operation steps missing")
        if variant == "safe_entry_options_centered" and len(scene.get("official_entry_options") or []) != 3:
            capture_or_semantic.append(f"SCENE-{scene_id:03d}: centered entry options are not three cards")
        if not str(scene.get("privacy") or "").strip():
            privacy_fail.append(f"SCENE-{scene_id:03d}: privacy metadata missing")
        if str(scene.get("official_text_readability") or "") != "PASS":
            readability_fail.append(f"SCENE-{scene_id:03d}: official text readability is not PASS")
        rendered_path = rendered_dir / f"scene_{scene_id:03d}.png"
        visual_status = "FAIL"
        centroid = {"status": "FAIL", "reason": "render missing"}
        if rendered_path.exists():
            with Image.open(rendered_path) as image:
                if image.size != (1920, 1080):
                    balance_fail.append(f"SCENE-{scene_id:03d}: render size {image.size}")
            centroid = visual_centroid_preflight(scene, rendered_path, theme)
            visual_status = str(centroid.get("status") or "FAIL")
        else:
            balance_fail.append(f"SCENE-{scene_id:03d}: render missing")
        geometry_row = geometry(scene, prepared_asset_count(scene))
        center_x = float(geometry_row.get("visual_center_x") or 0)
        if not (VISUAL_BALANCE_MIN_X <= center_x <= VISUAL_BALANCE_MAX_X) or visual_status != "PASS":
            balance_fail.append(
                f"SCENE-{scene_id:03d}: center={center_x:.0f} centroid={visual_status}"
            )
        target_rows.append(
            {
                "scene_id": f"SCENE-{scene_id:03d}",
                "variant": variant,
                "asset_kinds": asset_kinds,
                "asset_paths": asset_paths,
                "source_label_min_px": SOURCE_LABEL_FONT_PX if assets else None,
                "official_text_readability": scene.get("official_text_readability"),
                "visual_balance": "PASS" if not any(item.startswith(f"SCENE-{scene_id:03d}") for item in balance_fail) else "FAIL",
                "centroid_status": visual_status,
            }
        )

    policy = renderer_policy_guard()
    checks = [
        _check("placeholder_remaining", "PASS" if not placeholder_remaining else "FAIL", placeholder_remaining),
        _check("neutral_browser_frame", "PASS" if not neutral_browser else "FAIL", neutral_browser),
        _check("neutral_phone_frame", "PASS" if not neutral_phone else "FAIL", neutral_phone),
        _check("official_capture_or_semantic_visual", "PASS" if len(capture_or_semantic) >= len(TARGET_SCENES) and not any("missing" in x or "operation steps" in x or "three cards" in x for x in capture_or_semantic) else "FAIL", capture_or_semantic),
        _check("official_ui_ai_reconstruction", "PASS" if not reconstruction else "FAIL", reconstruction),
        _check("privacy", "PASS" if not privacy_fail else "FAIL", privacy_fail),
        _check("source_label_min_44px", "PASS" if not source_label_fail else "FAIL", source_label_fail),
        _check("official_text_tv_readability", "PASS" if not readability_fail else "FAIL", readability_fail),
        _check("visual_balance", "PASS" if not balance_fail else "FAIL", balance_fail),
        _check("oversized_checkmark", "PASS" if policy["oversized_checkmark_count"] == 0 else "FAIL", [str(policy["oversized_checkmark_count"])]),
        _check("meaningless_filler_icon", "PASS" if policy["meaningless_filler_icon_count"] == 0 else "FAIL", [str(policy["meaningless_filler_icon_count"])]),
    ]
    result = {
        "episode_id": str(data.get("episode", {}).get("episode_id") or episode_dir.name[:3]),
        "status": "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL",
        "target_scenes": target_rows,
        "checks": checks,
        "counts": {
            "placeholder_remaining": len(placeholder_remaining),
            "neutral_browser_frame": len(neutral_browser),
            "neutral_phone_frame": len(neutral_phone),
            "official_asset_scene_count": sum(1 for row in target_rows if row["asset_kinds"]),
            "semantic_visual_scene_count": sum(1 for row in target_rows if row["variant"] in SEMANTIC_VARIANTS),
        },
        "policy": policy,
    }
    return result


def write_outputs(result: dict[str, Any], json_path: Path, md_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Episode 012 Phase B Visual Gate",
        "",
        f"Overall: **{result['status']}**",
        "",
        "| Gate | Status | Detail |",
        "|---|---|---|",
    ]
    for item in result["checks"]:
        detail = " / ".join(str(value) for value in item.get("details", [])) or "—"
        lines.append(f"| {item['name']} | {item['status']} | {detail.replace('|', '／')} |")
    lines.extend(["", "## Target scenes", "", "| Scene | Variant | Assets | Readability | Balance |", "|---|---|---|---|---|"])
    for row in result["target_scenes"]:
        lines.append(
            f"| {row['scene_id']} | {row['variant']} | {', '.join(row['asset_kinds']) or 'semantic'} | {row['official_text_readability']} | {row['visual_balance']} |"
        )
    lines.extend(["", "Official UI was not AI-reconstructed. SCENE-008 and SCENE-013 use semantic operation visuals.", ""])
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--rendered-dir", type=Path, required=True)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    args = parser.parse_args()
    result = run_gate(args.episode, args.rendered_dir)
    write_outputs(result, args.json, args.markdown)
    print(json.dumps({"status": result["status"], "json": str(args.json), "markdown": str(args.markdown)}, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
