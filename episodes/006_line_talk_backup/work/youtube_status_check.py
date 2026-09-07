"""Post-upload YouTube status QA for Episode 006 (report-only)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from publish_youtube import (  # noqa: E402
    get_youtube_service,
    load_youtube_config,
)

EPISODE_DIR = ROOT / "episodes" / "006_line_talk_backup"
CONFIG = ROOT / "config" / "youtube_publish.json"


def main() -> None:
    config = load_youtube_config(CONFIG)
    publish = json.loads((EPISODE_DIR / "publish.json").read_text(encoding="utf-8"))
    video_id = publish.get("youtube_video_id") or "DK0431L9TwA"
    youtube = get_youtube_service(config)
    response = (
        youtube.videos()
        .list(
            part="snippet,contentDetails,status,processingDetails,fileDetails",
            id=video_id,
        )
        .execute()
    )
    item = response["items"][0]
    status = item.get("status") or {}
    snippet = item.get("snippet") or {}
    content = item.get("contentDetails") or {}
    processing = item.get("processingDetails") or {}
    files = item.get("fileDetails") or {}
    thumbs = item.get("thumbnails") or {}

    duration_text = content.get("duration") or ""

    def to_min_sec(text: str) -> str:
        import re

        m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(\d+(?:\.\d+)?)S", text or "")
        if not m:
            return text or "-"
        total = int(m.group(2) or 0) * 60 + int(float(m.group(3) or 0))
        return f"{total // 60}:{total % 60:02d}"

    lines = [
        "# YouTube status QA — Episode 006",
        "",
        f"- video_id: {video_id}",
        f"- privacyStatus: {status.get('privacyStatus')}",
        f"- publishAt: {status.get('publishAt') or '(none)'}",
        f"- license: {status.get('license')}",
        f"- selfDeclaredMadeForKids: {status.get('selfDeclaredMadeForKids')}",
        f"- embeddable: {status.get('embeddable')}",
        f"- containsSyntheticMedia(api): {status.get('containsSyntheticMedia')}",
        f"- title: {snippet.get('title')}",
        f"- categoryId: {snippet.get('categoryId')}",
        f"- defaultLanguage: {snippet.get('defaultLanguage')}",
        f"- tags: {snippet.get('tags')}",
        f"- duration: {duration_text} -> {to_min_sec(duration_text)}",
        f"- processingStatus: {processing.get('processingStatus')}",
        f"- processingProgress: {processing.get('processingProgress') or {}}",
        f"- fileDetails_hasAudio: {files.get('hasAudio')}",
        f"- fileDetails_duration: {files.get('durationMs')}",
        f"- fileDetails_videoStreams: {[s.get('height') for s in files.get('videoStreams', [])]}",
        f"- thumbnails: {sorted(thumbs.keys())}",
    ]
    (EPISODE_DIR / "work" / "youtube_publish" / "status_check.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print("\n".join(lines))


if __name__ == "__main__":
    main()
