"""Restore status='updated' / notes for pronunciation-fixed segments.

Run after closing segments_manifest.csv in Excel if the fix-run metadata
was lost by a --concat-only rebuild:

    python scripts/restore_manifest_segment_status.py

Idempotent: existing 'updated' rows are just refreshed.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "episodes" / "001_google_security" / "audio" / "voicevox_kenzaki" / "segments_manifest.csv"

FIXED = {
    4: "セキュリティー",
    5: "セキュリティー",
    7: "ひらけます",
    9: "セキュリティー",
    1: "Gmail→ジーメール",
    18: "再設定用 2句構成(サイ2|セッテイヨウ5)",
    36: "再設定用 2句構成(サイ2|セッテイヨウ5)",
    37: "再設定用 2句構成(サイ2|セッテイヨウ5)",
    38: "再設定用 2句構成(サイ2|セッテイヨウ5)",
    61: "セキュリティー",
    69: "セキュリティー",
    70: "再設定用 2句構成(サイ2|セッテイヨウ5)",
}


def main() -> int:
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    changed = 0
    for r in rows:
        sid = int(r["segment_id"])
        if sid in FIXED:
            r["status"] = "updated"
            r["notes"] = (
                f"regenerated 2026-08-30: {FIXED[sid]}; "
                "timeline recomputed at concat 2026-08-30"
            )
            changed += 1
    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"restored status/notes for {changed} segments")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PermissionError:
        print(
            "segments_manifest.csv is locked (open in Excel?). "
            "Close the file and run this script again.",
            file=sys.stderr,
        )
        raise SystemExit(1)
