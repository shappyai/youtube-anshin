"""Safely publish Short001 after its human-approved v8 finalize gate.

This is intentionally separate from the Episode publisher because Shorts use
``short.json`` and a vertical 1080x1920 deliverable.  It supports only a new
private upload; immediate public publishing is rejected by project policy.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import publish_youtube as core  # noqa: E402
import viewer_facing_text_qa as viewer_qa  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
SHORT_DIR = ROOT / "shorts" / "001_chatgpt_voice_input"
CONFIG_PATH = ROOT / "config" / "youtube_publish.json"
UTC = timezone.utc
MAX_TITLE_CHARS = 100
MAX_DESCRIPTION_BYTES = 5000
MAX_TAG_CHARS = 500
MAX_THUMBNAIL_BYTES = 2 * 1024 * 1024
IMMEDIATE_PUBLIC_ERROR = "Immediate public publishing is disabled by policy."
PROTECTED_FILES = (
    "shorts/002_ai_suspicious_message/output/draft_v5.mp4",
    "shorts/002_ai_suspicious_message/short.json",
    "shorts/002_ai_suspicious_message/script.md",
    "shorts/003_mynumber_smartphone/output/draft_v5.mp4",
    "shorts/003_mynumber_smartphone/short.json",
    "shorts/003_mynumber_smartphone/script.md",
)


class ShortPublishError(RuntimeError):
    """An expected local publication gate or safe API failure."""


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ShortPublishError(f"Required JSON file is missing: {path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise ShortPublishError(f"Invalid JSON file: {path}") from exc
    if not isinstance(value, dict):
        raise ShortPublishError(f"JSON object is required: {path}")
    return value


def save_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def state_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?mi)^\s*-\s*{re.escape(key)}\s*:\s*(.*?)\s*$", text)
    if not match:
        return None
    return match.group(1).strip().strip("`")


def protected_hashes() -> dict[str, str]:
    return {
        path: sha256(ROOT / path)
        for path in PROTECTED_FILES
        if (ROOT / path).exists()
    }


def approved_draft(review: dict[str, Any]) -> str | None:
    video = review.get("video")
    if not isinstance(video, dict):
        return None
    approved = []
    for key, value in video.items():
        if value == "approved" and str(key).startswith("draft_"):
            name = str(key)
            approved.append(name if name.lower().endswith(".mp4") else f"{name}.mp4")
    return approved[0] if len(approved) == 1 else None


def validate_metadata(publish: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    title = str(publish.get("selected_title") or publish.get("title") or "").strip()
    description = publish.get("description")
    tags = publish.get("tags")
    category_id = str(publish.get("category_id") or "").strip()
    language = str(publish.get("default_language") or "").strip()
    made_for_kids = publish.get("made_for_kids")
    ai_disclosure = publish.get("contains_synthetic_media")
    configured_privacy = str(publish.get("privacy") or publish.get("visibility") or "private").strip().lower()

    if not title:
        errors.append("title is empty")
    elif len(title) > MAX_TITLE_CHARS:
        errors.append(f"title exceeds {MAX_TITLE_CHARS} characters")
    if not isinstance(description, str) or not description.strip():
        errors.append("description is missing")
    elif len(description.encode("utf-8")) > MAX_DESCRIPTION_BYTES:
        errors.append(f"description exceeds {MAX_DESCRIPTION_BYTES} UTF-8 bytes")
    if not isinstance(tags, list) or any(not isinstance(tag, str) or not tag.strip() for tag in tags):
        errors.append("tags must be a non-empty-string array")
        clean_tags: list[str] = []
    else:
        clean_tags = [str(tag).strip() for tag in tags]
        if sum(len(tag) + (2 if " " in tag else 0) for tag in clean_tags) > MAX_TAG_CHARS:
            errors.append(f"tags exceed {MAX_TAG_CHARS} characters")
    if not category_id:
        errors.append("category_id is missing")
    if not language:
        errors.append("default_language is missing")
    if not isinstance(made_for_kids, bool):
        errors.append("made_for_kids must be boolean")
    if not isinstance(ai_disclosure, bool):
        errors.append("contains_synthetic_media must be an explicit boolean")
    if configured_privacy == "public":
        errors.append(IMMEDIATE_PUBLIC_ERROR)
    if configured_privacy not in {"private", "scheduled"}:
        errors.append("Only private publication is supported for this Short command")

    plan = {
        "episode": "Short001",
        "episode_dir": str(SHORT_DIR),
        "final_path": str(SHORT_DIR / "output" / "final.mp4"),
        "thumbnail_path": str(SHORT_DIR / str(publish.get("thumbnail") or "assets/thumbnail/thumbnail.jpg")),
        "title": title,
        "description": description if isinstance(description, str) else "",
        "tags": clean_tags,
        "category_id": category_id,
        "default_language": language,
        "made_for_kids": made_for_kids,
        "contains_synthetic_media": ai_disclosure,
        "privacy": "private",
        "schedule_api": None,
        "schedule_local_label": None,
        "video_sha256": None,
    }
    return errors, plan


def validate_thumbnail(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"Thumbnail missing: {path}"]
    if path.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
        errors.append("Thumbnail must be PNG or JPG/JPEG")
    if path.stat().st_size > MAX_THUMBNAIL_BYTES:
        errors.append(f"Thumbnail exceeds 2 MiB: {path}")
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            if image.format not in {"PNG", "JPEG"}:
                errors.append(f"Thumbnail format is not PNG/JPEG: {image.format}")
            if image.width <= 0 or image.height <= 0:
                errors.append("Thumbnail dimensions are invalid")
            ratio = image.width / image.height
            if abs(ratio - (9 / 16)) > 0.01:
                errors.append(f"Shorts thumbnail aspect ratio is not 9:16: {image.width}x{image.height}")
    except (OSError, SyntaxError) as exc:
        errors.append(f"Thumbnail is corrupt or unreadable: {exc}")
    return errors


def final_gate() -> tuple[list[str], str]:
    errors: list[str] = []
    final_path = SHORT_DIR / "output" / "final.mp4"
    draft_path = SHORT_DIR / "output" / "draft_v8.mp4"
    state_path = SHORT_DIR / "STATE.md"
    review_path = SHORT_DIR / "work" / "human_review.json"
    qa_path = SHORT_DIR / "work" / "final_qa.md"

    if not final_path.exists() or final_path.stat().st_size <= 0:
        errors.append(f"Final video missing or empty: {final_path}")
        return errors, ""
    if not state_path.exists():
        errors.append(f"STATE.md is missing: {state_path}")
    else:
        state = state_path.read_text(encoding="utf-8")
        if state_value(state, "status") != "finalized":
            errors.append("STATE.md status is not finalized")
        if (state_value(state, "human_approved") or "").lower() != "true":
            errors.append("STATE.md human_approved is not true")
    if not review_path.exists():
        errors.append(f"Human review record is missing: {review_path}")
    else:
        review = read_json(review_path)
        approved = approved_draft(review)
        if approved != "draft_v8.mp4":
            errors.append("human_review.json must approve exactly draft_v8.mp4")
        elif not draft_path.exists():
            errors.append(f"Approved draft is missing: {draft_path}")
    final_hash = sha256(final_path)
    if draft_path.exists() and sha256(draft_path) != final_hash:
        errors.append("final.mp4 SHA-256 does not match approved draft_v8.mp4")
    if not qa_path.exists():
        errors.append(f"Final QA PASS record is missing: {qa_path}")
    else:
        qa = qa_path.read_text(encoding="utf-8")
        if not re.search(r"(?mi)^\s*-\s*status\s*:\s*`?PASS`?\s*$", qa):
            errors.append("Final QA status is not PASS")
        if final_hash.lower() not in qa.lower():
            errors.append("Final QA does not record the current final.mp4 SHA-256")
    return errors, final_hash


def contains_internal_brand_promise(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    compact = re.sub(r"[\s\u3000]", "", text)
    target = re.sub(r"[\s\u3000]", "", viewer_qa.INTERNAL_BRAND_PROMISE)
    return viewer_qa.INTERNAL_BRAND_PROMISE in text or target in compact


def preflight() -> tuple[dict[str, Any], list[str]]:
    short_data = read_json(SHORT_DIR / "short.json")
    publish = read_json(SHORT_DIR / "publish.json")
    metadata_errors, plan = validate_metadata(publish)
    final_errors, final_hash = final_gate()
    plan["video_sha256"] = final_hash or None
    errors = metadata_errors + final_errors
    errors.extend(validate_thumbnail(Path(plan["thumbnail_path"])))

    viewer_report = SHORT_DIR / "work" / "viewer_facing_internal_brand_promise_publish.md"
    viewer_json = SHORT_DIR / "work" / "viewer_facing_internal_brand_promise_publish.json"
    scan = viewer_qa.run_scan(SHORT_DIR / "short.json", viewer_report, viewer_json)
    if scan.get("status") != "PASS":
        errors.append(f"viewer-facing internal brand promise scan: {scan.get('status')}")
    if contains_internal_brand_promise(SHORT_DIR / "publish.json"):
        errors.append("viewer-facing internal brand promise found in publish.json")

    if short_data.get("short_id") != "Short001":
        errors.append("short.json is not Short001")
    plan["short_data"] = short_data
    plan["publish_data"] = publish
    return plan, errors


def existing_video_id() -> tuple[str | None, str | None, bool]:
    state_path = SHORT_DIR / "STATE.md"
    if state_path.exists():
        value = state_value(state_path.read_text(encoding="utf-8"), "youtube_video_id")
        if value and value.lower() not in {"null", "none"}:
            return value, "STATE.md", False
    publish_path = SHORT_DIR / "publish.json"
    if publish_path.exists():
        data = read_json(publish_path)
        value = data.get("youtube_video_id")
        if value:
            return str(value), "publish.json", False
    attempt = SHORT_DIR / "work" / "youtube_publish" / "upload_attempt.json"
    if attempt.exists():
        data = read_json(attempt)
        value = data.get("video_id") or data.get("youtube_video_id")
        if value:
            return str(value), "upload_attempt.json", False
        status = str(data.get("status") or "").lower()
        if status in {"started", "uploading", "in_progress", "unknown"}:
            return None, None, True
    return None, None, False


def dry_run_report(plan: dict[str, Any], errors: list[str], existing_id: str | None) -> dict[str, Any]:
    return {
        "status": "FAIL" if errors else "PASS",
        "api_called": False,
        "oauth_called": False,
        "short_id": "Short001",
        "final_path": plan["final_path"],
        "thumbnail_path": plan["thumbnail_path"],
        "title": plan["title"],
        "privacy": "private",
        "ai_disclosure": plan["contains_synthetic_media"],
        "video_sha256": plan.get("video_sha256"),
        "existing_video_id": existing_id,
        "expected_api_requests": [
            "channels.list part=id,snippet mine=true",
            "videos.insert part=snippet,status resumable=True notifySubscribers=False",
            "thumbnails.set",
            "videos.list part=snippet,status",
        ],
        "errors": errors,
    }


def print_preflight(plan: dict[str, Any], errors: list[str], *, dry_run: bool) -> None:
    print("SHORT001 PUBLISH PREFLIGHT")
    print(f"Title: {plan['title']}")
    print("Privacy: PRIVATE")
    print(f"AI disclosure: {'YES' if plan['contains_synthetic_media'] else 'NO'}")
    print(f"File: {plan['final_path']}")
    print(f"SHA256: {plan.get('video_sha256') or '(missing)'}")
    print(f"Thumbnail: {plan['thumbnail_path']}")
    print("OAuth/API: NOT CALLED (dry-run)" if dry_run else "OAuth/API: pending")
    if errors:
        print("\nSTOP")
        for error in errors:
            print(f"- {error}")


def update_short_after_upload(plan: dict[str, Any], video_id: str) -> None:
    path = SHORT_DIR / "short.json"
    data = read_json(path)
    timestamp = now_utc()
    data.update(
        {
            "publish_status": "UPLOADED_PRIVATE_VERIFIED",
            "draft_status": "FINALIZED_AND_UPLOADED_PRIVATE",
            "final_path": "output/final.mp4",
            "final_sha256": plan["video_sha256"],
            "thumbnail_status": "UPLOADED",
            "thumbnail_path": "assets/thumbnail/thumbnail.jpg",
            "youtube_video_id": video_id,
            "youtube_url": f"https://youtu.be/{video_id}",
            "youtube_privacy": "private",
            "youtube_ai_disclosure": bool(plan["contains_synthetic_media"]),
            "publication_verified_at": timestamp,
        }
    )
    save_json(path, data)
    result = {
        "short_id": "Short001",
        "video_id": video_id,
        "youtube_url": f"https://youtu.be/{video_id}",
        "privacy": "private",
        "ai_disclosure": bool(plan["contains_synthetic_media"]),
        "final_sha256": plan["video_sha256"],
        "thumbnail": "assets/thumbnail/thumbnail.jpg",
        "verified_at": timestamp,
    }
    save_json(SHORT_DIR / "work" / "youtube_publish" / "short_upload_result.json", result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private", action="store_true", help="Upload as private (the only supported mode)")
    parser.add_argument("--public", action="store_true", help="Disabled by policy")
    parser.add_argument("--dry-run", action="store_true", help="Run local gates without OAuth or API calls")
    parser.add_argument("--yes", action="store_true", help="Skip the final upload confirmation")
    parser.add_argument("--force-reauth", action="store_true", help="Ignore the saved token and open browser OAuth")
    parser.add_argument("--config", type=Path, default=CONFIG_PATH, help="YouTube publish config JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.public:
        print(f"ERROR\n{IMMEDIATE_PUBLIC_ERROR}")
        return 2
    if args.config.resolve() != CONFIG_PATH.resolve():
        config_path = args.config.resolve()
    else:
        config_path = CONFIG_PATH

    try:
        plan, errors = preflight()
        video_id, source, unknown = existing_video_id()
        if unknown:
            errors.append("upload_attempt.json indicates an unresolved upload; refusing a new upload")
        if video_id:
            errors.append(f"Short001 already has a YouTube video ID ({video_id} from {source}); refusing duplicate upload")
        if args.dry_run:
            print_preflight(plan, errors, dry_run=True)
            report_path = SHORT_DIR / "work" / "youtube_publish" / "dry_run.json"
            save_json(report_path, dry_run_report(plan, errors, video_id))
            print(f"Dry-run report: {report_path}")
            return 1 if errors else 0
        print_preflight(plan, errors, dry_run=False)
        if errors:
            return 1

        before_protected = protected_hashes()
        config = core.load_youtube_config(config_path)
        youtube = core.get_youtube_service(config, force_reauth=args.force_reauth)
        channel_id, _ = core.verify_channel(youtube, config, allow_save=False)

        print("\nREADY TO UPLOAD")
        print("Short: Short001")
        print(f"Title: {plan['title']}")
        print("Privacy: PRIVATE")
        print(f"File: {plan['final_path']}")
        print(f"SHA256: {plan['video_sha256']}")
        print(f"Thumbnail: {plan['thumbnail_path']}")
        if not args.yes:
            try:
                if input("Proceed? [y/N] ").strip().lower() not in {"y", "yes"}:
                    print("Upload cancelled; no API upload was started.")
                    return 0
            except EOFError:
                print("Upload cancelled; no API upload was started.")
                return 0

        video_id = core.execute_publish(youtube, config, plan, channel_id)
        after_protected = protected_hashes()
        if before_protected != after_protected:
            raise ShortPublishError("Short002 / Short003 protected hashes changed unexpectedly")
        update_short_after_upload(plan, video_id)
        print(f"DONE: https://youtu.be/{video_id}")
        print("YouTube privacy: PRIVATE")
        return 0
    except (ShortPublishError, core.PublishError) as exc:
        print(f"ERROR\n{exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
