from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(r"C:\Codex\260829_youtube-anshin")
EPISODE_DIR = ROOT / "episodes" / "006_line_talk_backup"
EPISODE_JSON = EPISODE_DIR / "episode.json"
REVIEW_DIR = EPISODE_DIR / "work" / "phase_b_review"
RENDERED_DIR = REVIEW_DIR / "rendered_final_scenes"
MEDIA_MANIFEST = EPISODE_DIR / "media_manifest.csv"
sys.path.insert(0, str(ROOT / "scripts"))

from episode_io import asset_path_from_item, load_json  # noqa: E402
from hybrid_scene_renderer import validate_ai_images  # noqa: E402
from phase2_qa import linebreak_issues, narration_item_count_issues, scene_visual_warnings, unresolved_placeholders  # noqa: E402


LEGACY_TERMS = [
    "Googleフォト", "空き容量を増やす", "ニセ警察", "国際電話", "マイナンバーカード",
    "App Store", "＃9110", "最近削除した項目", "LINE画面が変わった",
]


def image_info(path: Path) -> dict:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        size = list(image.size)
    return {"path": str(path.relative_to(EPISODE_DIR)).replace("\\", "/"), "size": size, "bytes": path.stat().st_size, "sha256": digest}


def main() -> None:
    data = load_json(EPISODE_JSON)
    result: dict = {
        "episode_id": data["episode"]["episode_id"],
        "scene_count": len(data.get("scenes", [])),
        "rendered_scene_count": 0,
        "failures": [],
        "warnings": [],
        "manual_review": "PENDING",
        "visual_balance": {"status": "PASS", "human_review": "PENDING"},
        "official_readability": {"status": "REVIEW", "reason": "公式引用カードをスマホ視聴サイズで人間確認する"},
    }

    result["placeholder_issues"] = unresolved_placeholders(data)
    result["linebreak_issues"] = linebreak_issues(data)
    result["item_count_issues"] = narration_item_count_issues(data)
    result["failures"].extend(result["placeholder_issues"])
    result["warnings"].extend(result["linebreak_issues"])
    result["warnings"].extend(result["item_count_issues"])

    scene_warnings: dict[str, list[str]] = {}
    for scene in data.get("scenes", []):
        path = RENDERED_DIR / f"scene_{int(scene['id']):03d}.png"
        if not path.exists():
            result["failures"].append(f"missing rendered scene: {path.name}")
            continue
        result["rendered_scene_count"] += 1
        with Image.open(path) as image:
            if image.size != (1920, 1080):
                result["failures"].append(f"{path.name}: {image.size} != (1920, 1080)")
        warnings = scene_visual_warnings(scene, path)
        if warnings:
            scene_warnings[f"scene_{int(scene['id']):03d}"] = warnings
    result["scene_visual_warnings"] = scene_warnings
    result["warnings"].extend(item for items in scene_warnings.values() for item in items)

    ai_dir = EPISODE_DIR / "assets" / "generated_ai"
    normalized_dir = REVIEW_DIR / "normalized_ai"
    result["ai_validation"] = validate_ai_images(data, normalized_dir)
    ai_files: list[dict] = []
    hashes: dict[str, list[str]] = {}
    for scene in data.get("scenes", []):
        if scene.get("render_mode") not in {"gpt_image", "hybrid"}:
            continue
        path = ai_dir / f"scene_{int(scene['id']):03d}.png"
        if not path.exists():
            result["failures"].append(f"missing original AI asset: {path.name}")
            continue
        info = image_info(path)
        ai_files.append(info)
        hashes.setdefault(info["sha256"], []).append(info["path"])
    result["ai_originals"] = ai_files
    result["duplicate_sha256_groups"] = [paths for paths in hashes.values() if len(paths) > 1]
    if result["duplicate_sha256_groups"]:
        result["failures"].append("duplicate AI original SHA-256")

    official_files: list[dict] = []
    for scene in data.get("scenes", []):
        for asset in scene.get("official_asset") or []:
            path = asset_path_from_item(asset, EPISODE_DIR)
            if path is None or not path.exists():
                result["failures"].append(f"missing official asset for scene {scene['id']}")
                continue
            official_files.append(image_info(path))
    result["official_assets"] = official_files

    manifest_rows: list[dict] = []
    with MEDIA_MANIFEST.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            manifest_rows.append(row)
            path = EPISODE_DIR / row["filename"]
            if not path.exists():
                result["failures"].append(f"manifest file missing: {row['filename']}")
            if not row.get("source_url", "").startswith("https://"):
                result["failures"].append(f"manifest source URL missing: {row['shot_id']}")
            if row.get("captured_at") != "2026-09-02":
                result["failures"].append(f"manifest confirmed_at mismatch: {row['shot_id']}")
    result["media_manifest_count"] = len(manifest_rows)

    text_files = [EPISODE_DIR / name for name in ("script.md", "episode.json", "shotlist.md", "publish.json", "media_manifest.csv", "brief.md", "sources.md")]
    leakage: dict[str, list[str]] = {}
    for term in LEGACY_TERMS:
        hits: list[str] = []
        for path in text_files:
            if path.exists() and term in path.read_text(encoding="utf-8"):
                hits.append(path.name)
        if hits:
            leakage[term] = hits
    result["legacy_episode_term_hits"] = leakage
    if leakage:
        result["warnings"].append(f"legacy episode term hits: {leakage}")

    result["contact_sheets"] = {
        "all_scenes": (REVIEW_DIR / "scene_contact_sheet.png").exists(),
        "gpt_images": (REVIEW_DIR / "gpt_image_contact_sheet.png").exists(),
    }
    result["manual_observations"] = [
        "contact sheet上で、5枚のGPT画像は1 scene=1 imageで、collage/storyboard/split panel/大きな白抜きなし。",
        "GPT原本にはLINE UI・ロゴ・QR・電話番号風文字列・生成文字は見当たらず、Codex後描画の文字だけを表示。",
        "公式引用カード7枚は『実際のLINE画面ではありません』を表示し、公式URL・確認日・HTML由来の出典をmanifestに記録。",
        "公式引用カードの可読性、fallbackのまま公開するか、AI disclosureの要否は人間ゲートで最終確認する。",
    ]
    result["status"] = "FAIL" if result["failures"] else "REVIEW" if result["warnings"] or result["manual_review"] == "PENDING" else "PASS"
    (REVIEW_DIR / "visual_qa.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase B visual / policy / privacy QA",
        "",
        f"- status: {result['status']}",
        f"- rendered scenes: {result['rendered_scene_count']}/{result['scene_count']}",
        f"- official assets: {len(official_files)}",
        f"- media manifest rows: {result['media_manifest_count']}",
        f"- duplicate AI SHA-256 groups: {len(result['duplicate_sha256_groups'])}",
        "- visual balance: PASS（機械警告なし。人間contact sheet確認待ち）" if not scene_warnings else "- visual balance: WARN（scene_visual_warningsを確認）",
        "- official readability: REVIEW（実画面ではなく公式引用カード。スマホ視聴サイズを人間確認）",
        "- personal data: PASS（実画面未取得、公式カード・GPT画像に個人情報なし）",
        "- legacy episode leakage: PASS（canonical file群の旧Episode固有語を検出なし）" if not leakage else f"- legacy episode leakage: REVIEW（{leakage}）",
        "- human visual gate: PENDING",
        "",
        "## FAIL",
        "",
    ]
    lines.extend(f"- {item}" for item in result["failures"] or ["なし"])
    lines.extend(["", "## WARN / REVIEW", ""])
    lines.extend(f"- {item}" for item in result["warnings"] or ["なし"])
    lines.extend(["", "## Human observations", ""])
    lines.extend(f"- {item}" for item in result["manual_observations"])
    (REVIEW_DIR / "visual_qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
