"""Prepare readable Japanese display subtitle cues for Episode 012.

Narration remains one VOICEVOX segment per sentence.  Long display text is
split into consecutive temporal cues, then wrapped at semantic Japanese
boundaries.  The shared semantic policy lives in
``japanese_subtitle_semantics.py`` and is also used by subtitle preflight.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from japanese_subtitle_semantics import MAX_LINES, MAX_WIDTH, split_display_text, wrap_lines
from subtitle_preflight import estimated_width


def _wrap_lines(text: str) -> list[str]:
    return wrap_lines(text, estimated_width, MAX_WIDTH, 72.0)


def build_subtitles(data: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    output: list[dict[str, Any]] = []
    warnings: list[str] = []
    # Rebuild from each narration segment's canonical display text.  The
    # previous draft's hand-authored cue boundaries are intentionally not
    # treated as semantic source: several of them already contained the
    # unnatural breaks this generator is meant to remove (for example,
    # ``ただし、`` as a cue by itself).
    for segment in data.get("narration_segments", []):
        if not isinstance(segment, dict):
            continue
        segment_id = int(segment["id"])
        text = str(segment.get("display_text") or segment.get("narration") or "")
        if not text:
            continue
        chunks = split_display_text(text, estimated_width, MAX_WIDTH, MAX_LINES)
        if len(chunks) > 1:
            warnings.append(f"segment-{segment_id:03d}: split into {len(chunks)} temporal cues")
        for chunk in chunks:
            lines = _wrap_lines(chunk)
            if len(lines) > MAX_LINES or any(estimated_width(line) > MAX_WIDTH for line in lines):
                raise ValueError(f"unsafe result segment-{segment_id:03d}: {lines}")
            output.append(
                {
                    "id": "",
                    "text_lines": lines,
                    "segment_id": segment_id,
                    "font_px": 72,
                }
            )
    for index, cue in enumerate(output, 1):
        cue["id"] = f"SUB-{index:03d}"
    return output, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--warnings", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.episode.read_text(encoding="utf-8"))
    subtitles, warnings = build_subtitles(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(subtitles, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.warnings.write_text("\n".join(warnings) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"cue_count": len(subtitles), "split_count": len(warnings), "output": str(args.output)},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
