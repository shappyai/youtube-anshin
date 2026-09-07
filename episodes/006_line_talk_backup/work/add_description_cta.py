"""Append the approved channel CTA sentence to the description tail."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TARGETS = [
    ROOT / "episodes" / "006_line_talk_backup" / "episode.json",
    ROOT / "episodes" / "006_line_talk_backup" / "publish.json",
]

CTA = "大人のデジタル安心室では、スマホやパソコンを、もっと安全・快適に使うための情報をお届けします。チャンネル登録・高評価もよろしくお願いします。"
OLD = "\\n\\nナレーション：VOICEVOX:剣崎雌雄\""
NEW = f"\\n\\n{CTA}\\n\\nナレーション：VOICEVOX:剣崎雌雄\""


def main() -> None:
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        count = text.count(OLD)
        if count != 1:
            raise SystemExit(f"{path.name}: expected 1 occurrence, got {count}")
        path.write_text(text.replace(OLD, NEW), encoding="utf-8")
        print(f"updated {path.name}")


if __name__ == "__main__":
    main()
