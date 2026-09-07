"""ImageGen文字QA: imagegen_native生成画像の文字検査とretry/fallback管理。

背景が決まっている画像の文字は、機械で確実に読める部分（仕様の存在・
prompt一致・画像サイズ・破損・重複hash）だけ自動判定し、誤字・脱字・
    文字化け・重なり・コントラスト等の目視項目は人間/visionレビューへ出す。
    generated imageへの大きな後付け文字はNO_IMAGE_TEXT_HYBRIDとして許可しない。
OCR等の複雑な基盤は作らない（docs/text_render_policy.md）。

使い方:
  python scripts/text_qa.py episodes/NNN_slug/episode.json --ai-dir assets/generated_ai
  python scripts/text_qa.py episodes/NNN_slug/episode.json --mark SCENE-001:PASS
  python scripts/text_qa.py episodes/NNN_slug/episode.json --mark SCENE-001:FAIL
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from episode_io import canonical_text_render_mode, load_json  # noqa: E402

RENDERER_ONLY_AFTER_FAILS = 2
VISION_CHECKLIST = [
    "指定文言と一致している",
    "誤字なし",
    "脱字なし",
    "余計な文字なし",
    "文字化けなし",
    "不自然な漢字置換なし",
    "行順が指定どおり",
    "文字切れなし",
    "画像端にはみ出していない",
    "人物・重要オブジェクトと重なっていない",
    "背景とのコントラスト十分",
    "スマホ縮小時でも主見出しが読める",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def scene_text_spec(scene: dict[str, Any]) -> dict[str, str]:
    return {
        "headline": str(scene.get("headline") or "").strip(),
        "support_text": str(scene.get("support_text") or "").strip(),
    }


def deterministic_checks(scene: dict[str, Any], prompt: str, ai_dir: Path) -> list[str]:
    """Return a list of check names that pass (auto-deterministic only)."""
    passed: list[str] = []
    spec = scene_text_spec(scene)
    if spec["headline"] or spec["support_text"]:
        passed.append("文言仕様がsceneに定義されている")
    if spec["headline"] and spec["headline"] in prompt:
        passed.append("promptにheadline文言が含まれている")
    if spec["support_text"] and spec["support_text"] in prompt:
        passed.append("promptにsupport_text文言が含まれている")
    path = ai_dir / f"scene_{int(scene['id']):03d}.png"
    if path.exists():
        passed.append("生成画像が配置されている")
        try:
            with Image.open(path) as image:
                width, height = image.size
                ratio = width / height if height else 0
                if 1.5 <= ratio <= 1.9:
                    passed.append("アスペクト比がおおよそ16:9")
                if width >= 1280 and height >= 720:
                    passed.append("画像サイズが1280x720以上")
                passed.append(f"SHA-256: {sha256(path)[:16]}...")
        except OSError:
            pass  # broken imageはPASSに入れず、別項目でFAIL扱いにする
    return passed


def report_scene(
    scene: dict[str, Any],
    manifest: dict[str, Any] | None,
    ai_dir: Path,
) -> dict[str, Any]:
    scene_id = int(scene["id"])
    key = f"SCENE-{scene_id:03d}"
    prompt = str(scene.get("image_prompt") or "")
    row = {}
    if manifest:
        for candidate in manifest.get("scenes", []):
            if candidate.get("scene_id") == key:
                row = candidate
                prompt = str(candidate.get("image_prompt") or prompt)
                break
    passed = deterministic_checks(scene, prompt, ai_dir)
    spec = scene_text_spec(scene)
    path = ai_dir / f"scene_{scene_id:03d}.png"
    file_found = path.exists()
    file_valid = False
    if file_found:
        try:
            with Image.open(path) as image:
                file_valid = image.size[0] >= 1280 and image.size[1] >= 720
        except OSError:
            file_valid = False
    auto_fail = [] if file_found and file_valid else (
        ["生成画像がない/読めない"] if not file_found else ["画像が破損している"]
    )
    state = row.get("text_qa") or {"status": "pending", "retry_count": 0, "fallback": None}
    return {
        "scene_id": key,
        "text_render_mode": canonical_text_render_mode(scene),
        "headline": spec["headline"],
        "support_text": spec["support_text"],
        "auto_passed": passed,
        "auto_fail": auto_fail,
        "vision_checklist": VISION_CHECKLIST,
        "vision_status": "pending" if not auto_fail else "blocked",
        "text_qa": state,
        "image_path": str(path),
    }


def mark(manifest: dict[str, Any], scene_key: str, verdict: str) -> dict[str, Any]:
    """Apply PASS / FAIL / RESET to one scene's text_qa state in the manifest copy."""
    for row in manifest.get("scenes", []):
        if row.get("scene_id") != scene_key:
            continue
        state = row.setdefault("text_qa", {"status": "pending", "retry_count": 0, "fallback": None})
        if verdict == "PASS":
            state["status"] = "passed"
            state["fallback"] = None
        elif verdict == "FAIL":
            state["retry_count"] = int(state.get("retry_count") or 0) + 1
            if state["retry_count"] >= RENDERER_ONLY_AFTER_FAILS:
                state["status"] = "renderer_only_required"
                state["fallback"] = "renderer_only"
            else:
                state["status"] = "retry_required"
                state["fallback"] = None
        elif verdict == "RESET":
            state["status"] = "pending"
            state["retry_count"] = 0
            state["fallback"] = None
        return manifest
    raise SystemExit(f"unknown scene in manifest: {scene_key}")


def write_reports(results: list[dict[str, Any]], json_path: Path, md_path: Path) -> None:
    failed = [row for row in results if row["auto_fail"]]
    summary = {
        "total": len(results),
        "auto_fail": len(failed),
        "vision_review_required": len(results),
        "renderer_only_after": RENDERER_ONLY_AFTER_FAILS,
    }
    payload = {"summary": summary, "scenes": results}
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# ImageGen文字QA", ""]
    lines.append(f"{len(results)} scene / auto_fail={len(failed)} / vision_review={len(results)}")
    lines.append("")
    lines.append("ルール: imagegen_native → 文字QA → PASSなら採用 / FAILなら1回だけ再生成 / "
                 f"2回目のFAILは生成画像を捨て、renderer-onlyへ再設計（NO_IMAGE_TEXT_HYBRID）。")
    lines.append("")
    for row in results:
        lines.append(f"## {row['scene_id']} — {row['text_render_mode']}")
        lines.append("")
        lines.append(f"- headline: `{row['headline']}`")
        lines.append(f"- support_text: `{row['support_text']}`")
        lines.append(f"- image: `{row['image_path']}`")
        state = row["text_qa"]
        lines.append(f"- text_qa: status=`{state.get('status')}` retry_count={state.get('retry_count')} fallback={state.get('fallback')}")
        lines.append("")
        lines.append("### 自動チェック（PASS）")
        lines.extend([f"- [x] {item}" for item in row["auto_passed"]])
        if row["auto_fail"]:
            lines.append("")
            lines.append("### 自動チェック（FAIL）")
            lines.extend([f"- [ ] {item}" for item in row["auto_fail"]])
        lines.append("")
        lines.append("### 目視チェック（人間/vision）")
        lines.extend([f"- [ ] {item}" for item in row["vision_checklist"]])
        lines.append("")
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("episode", type=Path)
    parser.add_argument("--ai-dir", type=Path)
    parser.add_argument("--mark", help="SCENE-001:PASS / SCENE-001:FAIL / SCENE-001:RESET")
    parser.add_argument("--json", type=Path)
    parser.add_argument("--markdown", type=Path)
    args = parser.parse_args()

    data = load_json(args.episode.resolve())
    episode_dir = args.episode.resolve().parent
    ai_dir = (args.ai_dir or episode_dir / "assets" / "generated_ai").resolve()
    work_dir = episode_dir / "work"
    manifest_path = work_dir / "image_generation_manifest.json"
    manifest: dict[str, Any] | None = None
    if manifest_path.exists():
        manifest = load_json(manifest_path)

    if args.mark:
        if not manifest:
            raise SystemExit(f"manifest not found: {manifest_path}")
        scene_key, verdict = args.mark.split(":", 1)
        mark(manifest, scene_key.strip().upper(), verdict.strip().upper())
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"text_qa updated: {args.mark} -> {manifest_path}")

    results = [
        report_scene(scene, manifest, ai_dir)
        for scene in data.get("scenes", [])
        if scene.get("render_mode") in {"gpt_image", "hybrid"}
        and canonical_text_render_mode(scene) == "imagegen_native"
    ]
    if not results:
        print("no imagegen_native scenes to QA")
        return 0
    json_path = (args.json or work_dir / "text_qa.json").resolve()
    md_path = (args.markdown or work_dir / "text_qa.md").resolve()
    write_reports(results, json_path, md_path)
    failed = sum(1 for row in results if row["auto_fail"])
    print(f"text_qa: {len(results)} imagegen_native scenes, auto_fail={failed}")
    print(f"report: {md_path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
