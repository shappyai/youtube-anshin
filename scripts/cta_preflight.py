"""Verify the common CTA keeps its canonical text visible and in-bounds."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from create_channel_cta import cta_text_metrics, load_config  # noqa: E402


def clean(value: str) -> str:
    return re.sub(r"\s+", "", str(value or ""))


def box(value: Any) -> tuple[int, int, int, int]:
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError(f"invalid CTA box: {value!r}")
    return tuple(int(item) for item in value)  # type: ignore[return-value]


def run_qa(
    config_path: Path,
    image_path: Path | None = None,
) -> dict[str, Any]:
    config = load_config(config_path)
    text = config.get("text") or {}
    layout = config.get("layout") or {}
    canonical = str(config.get("display_text") or config.get("canonical_text") or "")
    description = str(text.get("description") or "")
    cta = str(text.get("cta") or "")
    metrics = cta_text_metrics(config_path)
    failures: list[str] = []

    sentences = canonical.split("。")
    if len(sentences) >= 2:
        expected_description = sentences[0] + "。"
        expected_cta = sentences[1] + ("。" if sentences[1] else "")
        if clean(description) != clean(expected_description):
            failures.append("descriptionがcanonical本文の前半と一致しません")
        if clean(cta).rstrip("。") != clean(expected_cta).rstrip("。"):
            failures.append("ctaがcanonical本文の後半と一致しません")
    if clean(description + cta).rstrip("。") != clean(canonical).rstrip("。").rstrip("。"):
        # Display-only omission of the final Japanese full stop is allowed;
        # missing content inside a sentence is not.
        if clean(description + cta) != clean(canonical).rstrip("。"):  # pragma: no cover - defensive branch
            failures.append("CTA表示文字列がcanonical_textと一致しません")

    for name in ("description", "cta"):
        item = metrics[name]
        if not item["complete"]:
            failures.append(f"{name}: text boxから末尾が欠落しています")
        if int(item["font_size"]) < 56:
            failures.append(f"{name}: font sizeが56px未満です ({item['font_size']}px)")
        if len(item["lines"]) > int(item["max_lines"]):
            failures.append(f"{name}: max_lines超過です")

    reserved_start = box((config.get("next_label") or {}).get("box"))[0]
    for name in ("panel", "description_box", "cta_box", "cta_text_box"):
        current = box(layout.get(name))
        if current[2] > reserved_start:
            failures.append(f"{name}: End Screen reserved領域へ侵入しています")
    next_box = box((config.get("next_label") or {}).get("box"))
    if next_box[0] < reserved_start:
        failures.append("next_labelの配置がreserved開始位置より左です")

    image_info: dict[str, Any] = {}
    if image_path is not None:
        try:
            from PIL import Image

            with Image.open(image_path) as image:
                image_info = {"path": str(image_path), "size": list(image.size), "mode": image.mode}
                if image.size != (1920, 1080):
                    failures.append(f"CTA画像サイズが1920x1080ではありません: {image.size}")
        except (OSError, ValueError) as exc:
            failures.append(f"CTA画像を確認できません: {exc}")

    return {
        "status": "PASS" if not failures else "FAIL",
        "qa": "cta_full_text_visible",
        "canonical_text": canonical,
        "description": description,
        "cta": cta,
        "metrics": metrics,
        "image": image_info,
        "end_screen_reserved_start_x": reserved_start,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "config" / "channel_cta.json")
    parser.add_argument("--image", type=Path)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    args = parser.parse_args()
    config_path = args.config.resolve()
    image_path = args.image.resolve() if args.image else None
    result = run_qa(config_path, image_path)
    output_json = (args.output_json or ROOT / "work" / "cta_preflight.json").resolve()
    output_md = (args.output_md or ROOT / "work" / "cta_preflight.md").resolve()
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# CTA preflight",
        "",
        f"- result: {result['status']}",
        "- qa: cta_full_text_visible",
        f"- description font: {result['metrics']['description']['font_size']}px",
        f"- cta font: {result['metrics']['cta']['font_size']}px",
        f"- description complete: {result['metrics']['description']['complete']}",
        f"- cta complete: {result['metrics']['cta']['complete']}",
        f"- text clipping: {len(result['failures'])}",
        "",
        "## Failures",
        "",
    ]
    lines.extend(f"- {item}" for item in result["failures"]) or lines.append("- なし")
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "json": str(output_json), "md": str(output_md)}, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
