"""HEAD-check the published source URLs (report-only, no mutation)."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PUBLISH = ROOT / "episodes" / "006_line_talk_backup" / "publish.json"


def main() -> None:
    data = json.loads(PUBLISH.read_text(encoding="utf-8"))
    lines: list[str] = []
    for url in data["source_urls"]:
        try:
            request = urllib.request.Request(
                url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(request, timeout=15) as response:
                final = response.geturl()
                redirect = "" if final == url else f"redirect-> {final}"
                lines.append(f"{response.status} {url} {redirect}".strip())
        except urllib.error.HTTPError as error:
            lines.append(f"HTTP {error.code} {url}")
        except Exception as exc:  # noqa: BLE001 - report-only
            lines.append(f"ERR {type(exc).__name__} {url}")
    (ROOT / "work_tmp_linkcheck.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
