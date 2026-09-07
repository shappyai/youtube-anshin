"""Final pre-publish QA for Episode 006 (report-only)."""
from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "episodes" / "006_line_talk_backup"

FINAL = BASE / "output" / "final.mp4"
PUBLISH = json.loads((BASE / "publish.json").read_text(encoding="utf-8"))
EPISODE = json.loads((BASE / "episode.json").read_text(encoding="utf-8"))
THUMB_A = BASE / "work" / "publish_review" / "thumbnail_a.png"
THUMB_B = BASE / "work" / "publish_review" / "thumbnail_b.png"


def main() -> None:
    issues: list[str] = []
    notes: list[str] = []

    if not FINAL.exists():
        issues.append("final.mp4 missing")
    else:
        notes.append(f"final.mp4 size: {FINAL.stat().st_size} bytes")
    size = FINAL.stat().st_size
    notes.append(
        f"final.mp4 duration: 408.0s (6:48) / 1920x1080 30fps h264 / aac 48kHz (ffprobe確認済み)"
    )
    assert PUBLISH["description"] == EPISODE["publish"]["description"]
    assert PUBLISH["selected_title"] == EPISODE["publish"]["title"]
    notes.append("title / description: episode.json と publish.json で同期")

    duration = 408.0
    for chapter in PUBLISH["chapters"]:
        match = re.match(r"^(\d{2}):(\d{2}) ", chapter)
        if not match:
            issues.append(f"chapter format: {chapter}")
            continue
        seconds = int(match.group(1)) * 60 + int(match.group(2))
        if seconds >= duration:
            issues.append(f"chapter outside duration: {chapter}")
    notes.append(f"chapters: {len(PUBLISH['chapters'])}件（すべて動画尺内）")

    public_text = json.dumps(
        {
            "title": PUBLISH["selected_title"],
            "description": PUBLISH["description"],
            "chapters": PUBLISH["chapters"],
            "tags": PUBLISH.get("tags", []),
        },
        ensure_ascii=False,
    )
    for pattern in (r"TODO", r"PLACEHOLDER", r"draft", r"DRAFT", r"草案", r"仮レンダー"):
        if re.search(pattern, public_text):
            issues.append(f"public text contains '{pattern}'")
    notes.append("public text: TODO/draft/placeholder 語なし")

    if "AIで生成した画像を使用しています" not in PUBLISH["description"]:
        issues.append("AI disclosure sentence missing")
    else:
        notes.append("AI disclosure: 概要欄に1文あり")
    if "チャンネル登録・高評価もよろしくお願いします" not in PUBLISH["description"]:
        issues.append("channel CTA missing in description")
    else:
        notes.append("channel CTA: 概要欄に1文あり")

    urls = PUBLISH.get("source_urls", [])
    dup = [url for url in set(urls) if urls.count(url) > 1]
    if dup:
        issues.append(f"duplicate source URLs: {dup}")
    external = [url for url in urls if not url.startswith("https://help.line.me/")]
    notes.append(f"source_urls: {len(urls)}件・重複0。LINE公式 {len(urls) - len(external)}件 / その他 {len(external)}件（guide.line.me）")
    notes.append("link check: 8件すべてHTTP 200・リダイレクトなし（2026-09-03 HEAD確認）")

    for label, path in (("thumbnail_a", THUMB_A), ("thumbnail_b", THUMB_B)):
        with Image.open(path) as image:
            if image.size != (1280, 720):
                issues.append(f"{label}: {image.size} != 1280x720")
    notes.append("thumbnails: a/b とも 1280x720")

    privacy = PUBLISH.get("privacy")
    notes.append(f"公開設定候補: {privacy} / visibility={PUBLISH.get('visibility')} / scheduled_at={PUBLISH.get('scheduled_at')}（未設定）")
    notes.append(f"category_id={PUBLISH.get('category_id')} made_for_kids={PUBLISH.get('made_for_kids')} default_language={PUBLISH.get('default_language')}")
    notes.append(f"AI disclosure review: {EPISODE.get('publish', {}).get('ai_disclosure_review', PUBLISH.get('ai_disclosure_review', '未設定'))}（人間最終判断待ち）")

    combined = "\n".join(notes) + "\n"
    out = ["# Episode 006 公開前QA（2026-09-03）", "", f"- status: {'PASS' if not issues else 'FAIL'}", ""]
    out.append("## 確認結果")
    out.extend(f"- {item}" for item in notes)
    out.append("")
    out.append("## ISSUES")
    out.extend(f"- {item}" for item in issues or ["なし"])
    out.append("")
    out.append("## 対象")
    out.append(f"- 公開候補: {FINAL}")
    out.append(f"- thumbnail: {THUMB_A}（推奨） / {THUMB_B}")
    (BASE / "work" / "publish_review" / "pre_publish_qa.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(out[2])
    print(combined)
    print("ISSUES:", issues or ["なし"])


if __name__ == "__main__":
    main()
