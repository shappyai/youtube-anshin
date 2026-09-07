"""Safe YouTube publication workflow for the 大人のデジタル安心室 channel.

The normal workflow is deliberately small and conservative:

* only ``private`` and future ``scheduled`` modes are supported;
* ``public`` is rejected before OAuth or any API call;
* a human-approved, finalized ``output/final.mp4`` and a valid thumbnail are
  required before upload;
* an upload response is persisted before thumbnail or scheduling work starts;
* retry commands never call ``videos.insert``.

Google client libraries are imported lazily so metadata validation, tests, and
dry-runs work on a machine that has not yet completed Google Cloud setup.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

from PIL import Image

from viewer_facing_text_qa import run_scan as run_viewer_facing_text_scan
from youtube_auth import (
    AuthError,
    authenticate as authenticate_youtube,
    write_diagnostics,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "youtube_publish.json"
BASE_DIR_NAMES = {"assets", "audio", "final", "output", "raw", "thumbnail", "work"}
JST = timezone(timedelta(hours=9), "Asia/Tokyo")
UTC = timezone.utc

MAX_TITLE_CHARS = 100
MAX_DESCRIPTION_BYTES = 5000
MAX_TAG_CHARS = 500
MAX_THUMBNAIL_BYTES = 2 * 1024 * 1024
RESUMABLE_CHUNK_SIZE = 8 * 1024 * 1024
AI_DISCLOSURE_METADATA_KEY = "contains_synthetic_media"
AI_DISCLOSURE_API_KEY = "containsSyntheticMedia"
PRESERVED_STATUS_KEYS = (
    "privacyStatus",
    "publishAt",
    "license",
    "embeddable",
    "publicStatsViewable",
    "selfDeclaredMadeForKids",
)

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

IMMEDIATE_PUBLIC_ERROR = "Immediate public publishing is disabled by policy."
_LAST_AUTH_DIAGNOSTICS: dict[str, Any] = {}
CONTROL_CHARACTERS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")
YOUTUBE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{6,}$")


class PublishError(RuntimeError):
    """An expected, safe-to-report publication gate or API error."""


def project_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return (ROOT / path).resolve()


def resolve_episode(value: str | Path) -> Path:
    """Resolve ``003``, ``episodes/003_slug``, or an episode directory."""
    raw = Path(value)
    candidates = [raw] if raw.is_absolute() else [ROOT / raw]
    for candidate in candidates:
        if candidate.is_dir() and (candidate / "episode.json").exists():
            return candidate.resolve()
        if candidate.is_file() and candidate.name == "episode.json":
            return candidate.parent.resolve()

    token = str(value).strip()
    if token.isdigit():
        token = token.zfill(3)
    matches = sorted(
        path for path in (ROOT / "episodes").glob(f"{token}_*")
        if path.is_dir() and (path / "episode.json").exists()
    )
    if len(matches) == 1:
        return matches[0].resolve()
    if not matches:
        raise PublishError(f"Episode directory not found: {value}")
    raise PublishError(
        f"Episode identifier is ambiguous: {value} ({len(matches)} directories found)"
    )


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PublishError(f"Required JSON file is missing: {path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise PublishError(f"Invalid JSON file: {path}") from exc
    if not isinstance(value, dict):
        raise PublishError(f"JSON object is required: {path}")
    return value


def save_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def strip_path_annotation(value: str) -> str:
    """Remove human notes such as ``（人間指定・採用）`` from a path."""
    return re.split(r"[（(]", str(value), maxsplit=1)[0].strip()


def resolve_episode_path(episode_dir: Path, value: str | Path) -> Path:
    path = Path(strip_path_annotation(str(value)))
    if path.is_absolute():
        return path
    local = (episode_dir / path).resolve()
    if local.exists() or (path.parts and path.parts[0] in BASE_DIR_NAMES):
        return local
    return (ROOT / path).resolve()


def _source_urls(episode_data: dict[str, Any], publish_data: dict[str, Any]) -> list[str]:
    urls = publish_data.get("source_urls")
    if isinstance(urls, list):
        result = [str(url).strip() for url in urls if str(url).strip()]
        if result:
            return result
    result: list[str] = []
    for source in episode_data.get("sources", []):
        if isinstance(source, dict) and source.get("url"):
            url = str(source["url"]).strip()
            if url and url not in result:
                result.append(url)
    return result


def _chapters(publish_data: dict[str, Any]) -> list[str]:
    chapters = publish_data.get("chapters")
    if isinstance(chapters, list):
        return [str(item).strip() for item in chapters if str(item).strip()]
    text = publish_data.get("chapters_text")
    if isinstance(text, str):
        return [line.strip() for line in text.splitlines() if line.strip()]
    return []


def load_publish_metadata(episode_dir: Path) -> tuple[dict[str, Any], list[str], Path | None]:
    """Load the nested episode publish block, then top-level publish.json.

    The top-level file is preferred because it is the established publishing
    artifact in this repository.  A declared ``description_file`` is treated
    as authoritative and missing files are a preflight error.
    """
    episode_path = episode_dir / "episode.json"
    episode_data = read_json(episode_path)
    data: dict[str, Any] = {}
    nested = episode_data.get("publish")
    if isinstance(nested, dict):
        data.update(nested)

    publish_path = episode_dir / "publish.json"
    if publish_path.exists():
        data.update(read_json(publish_path))
    else:
        publish_path = None

    errors: list[str] = []
    description_file: Path | None = None
    declared_description_file = data.get("description_file")
    if declared_description_file:
        description_file = resolve_episode_path(episode_dir, str(declared_description_file))
        if not description_file.exists():
            errors.append(f"description_file is missing: {description_file}")
        else:
            try:
                data["description"] = description_file.read_text(encoding="utf-8")
            except OSError as exc:
                errors.append(f"description_file cannot be read: {description_file}")

    data.setdefault("chapters", _chapters(data))
    data.setdefault("source_urls", _source_urls(episode_data, data))
    if not data.get("voice_credit") and data.get("credit"):
        data["voice_credit"] = data["credit"]
    data["_episode_data"] = episode_data
    data["_publish_path"] = str(publish_path) if publish_path else None
    return data, errors, description_file


def build_description(
    raw_description: str,
    chapters: list[str],
    source_urls: list[str],
    voice_credit: str,
) -> str:
    """Append only missing structured sections; do not rewrite the prose."""
    text = str(raw_description or "").strip()
    additions: list[str] = []

    if chapters and not all(chapter in text for chapter in chapters):
        additions.append("【目次】\n" + "\n".join(chapters))
    if source_urls and not all(url in text for url in source_urls):
        additions.append("【主な出典】\n" + "\n".join(source_urls))
    if voice_credit and voice_credit not in text:
        additions.append(voice_credit)

    if additions:
        text = "\n\n".join(part for part in (text, *additions) if part)
    return text


def select_thumbnail(
    episode_dir: Path,
    publish_data: dict[str, Any],
    config: dict[str, Any],
) -> tuple[Path | None, list[Path]]:
    if bool(publish_data.get("thumbnail_optional_private")):
        return None, []
    explicit = publish_data.get("thumbnail") or publish_data.get("thumbnail_path")
    if explicit:
        candidates = [resolve_episode_path(episode_dir, str(explicit))]
    else:
        raw_candidates = publish_data.get("thumbnail_candidates")
        if not isinstance(raw_candidates, list):
            raw_candidates = []
        if not raw_candidates:
            raw_candidates = config.get("thumbnail_candidates", [])
        candidates = [
            resolve_episode_path(episode_dir, str(candidate))
            for candidate in raw_candidates
            if str(candidate).strip()
        ]
    if not candidates:
        candidates = [
            episode_dir / "assets" / "thumbnail" / "thumbnail.png"
        ]
    for candidate in candidates:
        if candidate.exists():
            return candidate, candidates
    return candidates[0], candidates


def parse_schedule(
    value: str, now: datetime | None = None
) -> tuple[datetime, str, str]:
    """Parse a local JST schedule and return (local_dt, label, UTC API value)."""
    raw = str(value).strip()
    if not raw:
        raise PublishError("Schedule must not be empty.")
    parsed: datetime | None = None
    for candidate in (raw, raw.replace("Z", "+00:00")):
        try:
            parsed = datetime.fromisoformat(candidate.replace(" ", "T", 1))
            break
        except ValueError:
            continue
    if parsed is None:
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
            try:
                parsed = datetime.strptime(raw, fmt)
                break
            except ValueError:
                continue
    if parsed is None:
        raise PublishError(
            "Invalid schedule. Use 'YYYY-MM-DD HH:MM' in Asia/Tokyo (JST)."
        )

    local = parsed.replace(tzinfo=JST) if parsed.tzinfo is None else parsed.astimezone(JST)
    current = now or datetime.now(JST)
    if current.tzinfo is None:
        current = current.replace(tzinfo=JST)
    else:
        current = current.astimezone(JST)
    if local <= current:
        raise PublishError(
            "Scheduled time must be in the future; past publishAt values can publish immediately."
        )
    local = local.replace(microsecond=0)
    api_value = (
        local.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )
    label = local.strftime("%Y-%m-%d %H:%M:%S JST")
    return local, label, api_value


def schedule_to_api(value: str, now: datetime | None = None) -> str:
    return parse_schedule(value, now=now)[2]


def validate_text(value: Any, field: str, *, max_chars: int | None = None, max_bytes: int | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, str) or not value.strip():
        return [f"{field} must not be empty."]
    if CONTROL_CHARACTERS.search(value):
        errors.append(f"{field} contains control characters.")
    if "<" in value or ">" in value:
        errors.append(f"{field} contains unsupported '<' or '>' characters.")
    if max_chars is not None and len(value) > max_chars:
        errors.append(f"{field} exceeds {max_chars} characters ({len(value)}).")
    if max_bytes is not None and len(value.encode("utf-8")) > max_bytes:
        errors.append(
            f"{field} exceeds {max_bytes} UTF-8 bytes ({len(value.encode('utf-8'))})."
        )
    return errors


def tag_total_length(tags: list[str]) -> int:
    """Count tag characters conservatively, including quote space overhead."""
    return sum(len(tag) + (2 if " " in tag else 0) for tag in tags)


def validate_tags(tags: Any) -> list[str]:
    if not isinstance(tags, list):
        return ["tags must be an array of strings."]
    errors: list[str] = []
    for index, tag in enumerate(tags):
        if not isinstance(tag, str) or not tag.strip():
            errors.append(f"tags[{index}] must be a non-empty string.")
        elif CONTROL_CHARACTERS.search(tag):
            errors.append(f"tags[{index}] contains control characters.")
    cleaned = [tag for tag in tags if isinstance(tag, str)]
    total = tag_total_length(cleaned)
    if total > MAX_TAG_CHARS:
        errors.append(f"tags exceed {MAX_TAG_CHARS} characters ({total}).")
    return errors


def validate_metadata(plan: dict[str, Any], *, require_ai_disclosure: bool = True) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_text(plan.get("title"), "title", max_chars=MAX_TITLE_CHARS))
    errors.extend(
        validate_text(
            plan.get("description"),
            "description",
            max_bytes=MAX_DESCRIPTION_BYTES,
        )
    )
    errors.extend(validate_tags(plan.get("tags")))
    if not str(plan.get("category_id") or "").strip():
        errors.append("category_id must not be empty.")
    if not str(plan.get("default_language") or "").strip():
        errors.append("default_language must not be empty.")
    if not isinstance(plan.get("made_for_kids"), bool):
        errors.append("made_for_kids must be boolean.")
    ai_value = plan.get(AI_DISCLOSURE_METADATA_KEY)
    if require_ai_disclosure and not isinstance(ai_value, bool):
        errors.append(
            "AI disclosure is not configured; human review required "
            f"({AI_DISCLOSURE_METADATA_KEY})."
        )
    elif ai_value is not None and not isinstance(ai_value, bool):
        errors.append(f"{AI_DISCLOSURE_METADATA_KEY} must be boolean when present.")
    if plan.get("privacy") not in {"private", "scheduled"}:
        errors.append("Only private and scheduled privacy modes are supported.")
    return errors


def validate_thumbnail(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"Thumbnail missing: {path}"]
    if path.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
        errors.append("Thumbnail must be PNG or JPG/JPEG.")
    try:
        size = path.stat().st_size
    except OSError as exc:
        return [f"Thumbnail cannot be read: {path}"]
    if size > MAX_THUMBNAIL_BYTES:
        errors.append(
            f"Thumbnail exceeds 2 MiB ({size} bytes): {path}"
        )
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            if image.format not in {"PNG", "JPEG"}:
                errors.append(f"Thumbnail image format is not PNG/JPEG: {image.format}")
            if image.width <= 0 or image.height <= 0:
                errors.append("Thumbnail dimensions are invalid.")
    except (OSError, SyntaxError) as exc:
        errors.append(f"Thumbnail is corrupt or unreadable: {path}")
    return errors


def _state_value(state_text: str, key: str) -> str | None:
    match = re.search(rf"(?mi)^\s*-\s*{re.escape(key)}\s*:\s*(.*?)\s*$", state_text)
    if not match:
        return None
    return match.group(1).strip().strip("`")


def _approved_draft(review: dict[str, Any]) -> str | None:
    video = review.get("video")
    if not isinstance(video, dict):
        return None
    approved: list[str] = []
    for key, value in video.items():
        # Episode 004以降は draft_vN 形式も使用する（draft_auto_vN と両対応）
        if value == "approved" and str(key).startswith("draft_"):
            name = str(key)
            approved.append(name if name.endswith(".mp4") else f"{name}.mp4")
    return approved[0] if len(approved) == 1 else None


def final_gate(episode_dir: Path, final_path: Path | None = None) -> tuple[list[str], str]:
    """Validate the immutable final and its human/QA evidence."""
    final = final_path or episode_dir / "output" / "final.mp4"
    errors: list[str] = []
    if not final.exists() or final.stat().st_size <= 0:
        errors.append(f"Final video missing or empty: {final}")
        return errors, ""
    if final.name != "final.mp4":
        errors.append("Upload target must be output/final.mp4; drafts are never uploaded.")
    final_hash = sha256(final)

    state_path = episode_dir / "STATE.md"
    if not state_path.exists():
        errors.append(f"STATE.md is missing: {state_path}")
    else:
        state = state_path.read_text(encoding="utf-8")
        if _state_value(state, "status") != "finalized":
            errors.append("STATE.md status is not finalized.")
        if (_state_value(state, "human_approved") or "").lower() != "true":
            errors.append("STATE.md human_approved is not true.")

    review_path = episode_dir / "work" / "human_review.json"
    if not review_path.exists():
        errors.append(f"Human review record is missing: {review_path}")
    else:
        try:
            review = read_json(review_path)
            approved = _approved_draft(review)
            if not approved:
                errors.append("human_review.json does not contain exactly one approved draft_auto video.")
        except PublishError as exc:
            errors.append(str(exc))

    qa_candidates = [
        episode_dir / "output" / "review" / "final_qa.md",
        episode_dir / "work" / "final_qa.md",
    ]
    qa_path = next((path for path in qa_candidates if path.exists()), None)
    if qa_path is None:
        errors.append("Final QA PASS record is missing (expected output/review/final_qa.md).")
    else:
        qa_text = qa_path.read_text(encoding="utf-8")
        upper = qa_text.upper()
        if "PASS" not in upper or re.search(r"\bFAIL\b", upper):
            errors.append(f"Final QA is not PASS: {qa_path}")
        if final_hash.lower() not in qa_text.lower():
            errors.append("Final QA does not record the current final.mp4 SHA-256.")
    return errors, final_hash


def build_plan(
    episode_value: str | Path,
    config: dict[str, Any],
    mode: str = "private",
    schedule_value: str | None = None,
) -> tuple[dict[str, Any], list[str]]:
    episode_dir = resolve_episode(episode_value)
    publish_data, metadata_errors, description_file = load_publish_metadata(episode_dir)
    final_path = episode_dir / "output" / "final.mp4"
    thumbnail_path, thumbnail_candidates = select_thumbnail(episode_dir, publish_data, config)

    chapters = _chapters(publish_data)
    source_urls = _source_urls(publish_data.get("_episode_data", {}), publish_data)
    voice_credit = str(
        publish_data.get("voice_credit") or publish_data.get("credit") or ""
    ).strip()
    raw_description = str(publish_data.get("description") or "")
    description = build_description(raw_description, chapters, source_urls, voice_credit)
    tags = publish_data.get("tags", [])
    if not isinstance(tags, list):
        tags = tags

    plan: dict[str, Any] = {
        "episode": episode_dir.name,
        "episode_id": episode_dir.name.split("_", 1)[0],
        "episode_dir": str(episode_dir),
        "publish_path": publish_data.get("_publish_path"),
        "description_file": str(description_file) if description_file else None,
        "final_path": str(final_path),
        "thumbnail_path": str(thumbnail_path) if thumbnail_path else None,
        "thumbnail_candidates": [str(path) for path in thumbnail_candidates],
        "title": publish_data.get("selected_title") or publish_data.get("title") or "",
        "description": description,
        "chapters": chapters,
        "source_urls": source_urls,
        "voice_credit": voice_credit,
        "tags": tags,
        "category_id": str(
            publish_data.get("category_id")
            or publish_data.get("categoryId")
            or config.get("category_id")
            or "22"
        ),
        "default_language": str(
            publish_data.get("default_language")
            or publish_data.get("language")
            or config.get("default_language")
            or "ja"
        ),
        "made_for_kids": publish_data.get(
            "made_for_kids",
            publish_data.get("self_declared_made_for_kids", config.get("made_for_kids", False)),
        ),
        AI_DISCLOSURE_METADATA_KEY: publish_data.get(AI_DISCLOSURE_METADATA_KEY),
        "privacy": mode,
        "metadata_privacy": publish_data.get("privacy") or publish_data.get("visibility"),
        "schedule_input": schedule_value,
        "schedule_local": None,
        "schedule_local_label": None,
        "schedule_api": None,
        "video_sha256": sha256(final_path) if final_path.exists() else None,
    }
    if mode == "scheduled":
        if not schedule_value:
            metadata_errors.append("Scheduled mode requires --schedule.")
        else:
            try:
                local, label, api_value = parse_schedule(schedule_value)
                plan["schedule_local"] = local.isoformat()
                plan["schedule_local_label"] = label
                plan["schedule_api"] = api_value
            except PublishError as exc:
                metadata_errors.append(str(exc))

    if plan["metadata_privacy"] == "public":
        metadata_errors.append(IMMEDIATE_PUBLIC_ERROR)
    return plan, metadata_errors


def preflight(plan: dict[str, Any], metadata_errors: list[str]) -> list[str]:
    errors = list(metadata_errors)
    episode_dir = Path(plan["episode_dir"])
    final_errors, final_hash = final_gate(episode_dir, Path(plan["final_path"]))
    errors.extend(final_errors)
    if final_hash:
        plan["video_sha256"] = final_hash
    errors.extend(validate_metadata(plan, require_ai_disclosure=True))
    if plan.get("thumbnail_path"):
        errors.extend(validate_thumbnail(Path(plan["thumbnail_path"])))
    elif plan.get("privacy") != "private":
        errors.append("Thumbnail is not configured; optional thumbnail is allowed only for private upload.")
    try:
        viewer_scan = run_viewer_facing_text_scan(
            episode_dir / "episode.json",
            episode_dir / "work" / "viewer_facing_internal_brand_promise.md",
            episode_dir / "work" / "viewer_facing_internal_brand_promise.json",
        )
        if viewer_scan.get("status") != "PASS":
            errors.append(
                "viewer_facing_internal_brand_promise detected: "
                f"{viewer_scan.get('viewer_facing_count', '?')}"
            )
    except Exception as exc:
        errors.append(f"viewer-facing internal brand promise scan failed: {exc}")
    return errors


def read_attempt(episode_dir: Path) -> dict[str, Any]:
    path = episode_dir / "work" / "youtube_publish" / "upload_attempt.json"
    if not path.exists():
        return {}
    try:
        return read_json(path)
    except PublishError:
        return {"status": "invalid"}


def existing_video_id(episode_dir: Path) -> tuple[str | None, str | None, bool]:
    """Return (video_id, source, unknown_started_attempt)."""
    state_path = episode_dir / "STATE.md"
    if state_path.exists():
        state_text = state_path.read_text(encoding="utf-8")
        value = _state_value(state_text, "youtube_video_id")
        if value and value.lower() not in {"null", "none"}:
            return value, "STATE.md", False

    publish_path = episode_dir / "publish.json"
    if publish_path.exists():
        try:
            data = read_json(publish_path)
            value = data.get("youtube_video_id")
            if value:
                return str(value), "publish.json", False
        except PublishError:
            pass

    attempt = read_attempt(episode_dir)
    value = attempt.get("video_id") or attempt.get("youtube_video_id")
    if value:
        return str(value), "upload_attempt.json", False
    status = str(attempt.get("status") or "").lower()
    unknown = status in {"started", "uploading", "in_progress", "unknown"}
    return None, None, unknown


def _render_state_value(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).replace("\r", " ").replace("\n", " ")


def update_state(episode_dir: Path, fields: dict[str, Any]) -> None:
    path = episode_dir / "STATE.md"
    text = path.read_text(encoding="utf-8") if path.exists() else f"# {episode_dir.name} State\n"
    changed_section = False
    for key, value in fields.items():
        replacement = f"- {key}: {_render_state_value(value)}"
        pattern = rf"(?mi)^\s*-\s*{re.escape(key)}\s*:.*$"
        text, count = re.subn(pattern, replacement, text, count=1)
        if count:
            changed_section = True
    missing = [
        (key, value)
        for key, value in fields.items()
        if not re.search(rf"(?mi)^\s*-\s*{re.escape(key)}\s*:", text)
    ]
    if missing:
        if "## YouTube publication" not in text:
            text = text.rstrip() + "\n\n## YouTube publication\n"
        text = text.rstrip() + "\n" + "\n".join(
            f"- {key}: {_render_state_value(value)}" for key, value in missing
        ) + "\n"
    path.write_text(text, encoding="utf-8")


def update_publish_state(episode_dir: Path, fields: dict[str, Any]) -> None:
    path = episode_dir / "publish.json"
    if not path.exists():
        return
    data = read_json(path)
    data.update(fields)
    save_json(path, data)


def publication_fields(
    plan: dict[str, Any],
    status: str,
    video_id: str,
    thumbnail_uploaded: bool,
    uploaded_at: str | None = None,
    error: str | None = None,
    channel_id: str | None = None,
) -> dict[str, Any]:
    uploaded = uploaded_at or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        "youtube_upload": status,
        "youtube_video_id": video_id,
        "youtube_url": f"https://youtu.be/{video_id}",
        "youtube_privacy": "private",
        "youtube_scheduled_at": plan.get("schedule_local_label") if plan.get("schedule_api") else None,
        "youtube_scheduled_at_api": plan.get("schedule_api"),
        "thumbnail_uploaded": thumbnail_uploaded,
        "uploaded_at": uploaded,
        **({"youtube_channel_id": channel_id} if channel_id else {}),
        **({"youtube_publish_error": error} if error else {}),
    }


def persist_video_id(
    plan: dict[str, Any],
    video_id: str,
    status: str,
    thumbnail_uploaded: bool = False,
    uploaded_at: str | None = None,
    error: str | None = None,
    channel_id: str | None = None,
) -> dict[str, Any]:
    fields = publication_fields(
        plan,
        status,
        video_id,
        thumbnail_uploaded,
        uploaded_at=uploaded_at,
        error=error,
        channel_id=channel_id,
    )
    episode_dir = Path(plan["episode_dir"])
    update_state(episode_dir, fields)
    update_publish_state(episode_dir, fields)
    return fields


def attempt_path(episode_dir: Path) -> Path:
    return episode_dir / "work" / "youtube_publish" / "upload_attempt.json"


def save_attempt(episode_dir: Path, attempt: dict[str, Any]) -> None:
    save_json(attempt_path(episode_dir), attempt)


def safe_error(exc: BaseException) -> str:
    """Return an error summary without serializing API credentials or payloads."""
    status = getattr(getattr(exc, "resp", None), "status", None)
    suffix = f" HTTP {status}" if status else ""
    return f"{type(exc).__name__}{suffix}"


def append_log(episode_dir: Path, event: dict[str, Any]) -> None:
    path = episode_dir / "work" / "youtube_publish" / "youtube_upload_log.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    allowed = [
        "timestamp", "mode", "final_sha256", "title", "video_id", "privacy",
        "publish_at_local", "publish_at_api", "thumbnail_status", "verification", "error",
        "api_operation", "ai_disclosure", "reupload", "privacy_before", "publish_at_before",
        "made_for_kids_before", "contains_synthetic_media_before", "contains_synthetic_media_after",
    ]
    lines = ["", f"## {event.get('timestamp', '')}"]
    for key in allowed:
        if event.get(key) is not None:
            lines.append(f"- {key}: {str(event[key]).replace(chr(10), ' ')}")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def load_youtube_config(path: Path | None = None) -> dict[str, Any]:
    config_path = project_path(path or DEFAULT_CONFIG)
    data = read_json(config_path)
    data["_config_path"] = str(config_path)
    data.setdefault("oauth_scopes", DEFAULT_SCOPES)
    return data


def channel_config_path(config: dict[str, Any]) -> Path:
    return project_path(str(config.get("channel_config_path") or "local/youtube/channel_config.json"))


def load_channel_config(config: dict[str, Any]) -> dict[str, Any]:
    path = channel_config_path(config)
    if not path.exists():
        return {}
    return read_json(path)


def channel_matches(
    actual_id: str,
    actual_title: str,
    expected_id: str | None,
    expected_title: str | None = None,
    configured_name: str | None = None,
) -> tuple[bool, str]:
    if expected_id and actual_id != expected_id:
        return False, f"YouTube channel ID mismatch: expected {expected_id}, got {actual_id}."
    if expected_title and actual_title != expected_title:
        return False, f"YouTube channel title mismatch: expected {expected_title}, got {actual_title}."
    if not expected_id and configured_name and actual_title != configured_name:
        return False, f"Authenticated channel is not the configured channel: {actual_title}."
    return True, "channel verified"


def _channel_from_api(youtube: Any) -> tuple[str, str]:
    response = youtube.channels().list(
        part="id,snippet", mine=True, maxResults=1
    ).execute()
    items = response.get("items") or []
    if len(items) != 1:
        raise PublishError("Authenticated Google account has no single YouTube channel to verify.")
    item = items[0]
    channel_id = str(item.get("id") or "")
    title = str((item.get("snippet") or {}).get("title") or "")
    if not channel_id or not title:
        raise PublishError("YouTube channel verification returned incomplete channel data.")
    return channel_id, title


def verify_channel(
    youtube: Any,
    config: dict[str, Any],
    *,
    allow_save: bool = False,
    approve: Callable[[str], bool] | None = None,
    quiet: bool = False,
) -> tuple[str, str]:
    try:
        actual_id, actual_title = _channel_from_api(youtube)
    except PublishError:
        raise
    except Exception as exc:
        raise PublishError(f"channels.list verification failed: {safe_error(exc)}") from exc

    if not quiet:
        print(f"Channel: {actual_title}")
        print(f"Channel ID: {actual_id}")
    saved = load_channel_config(config)
    expected_id = str(saved.get("expected_channel_id") or "").strip()
    expected_title = str(saved.get("expected_channel_title") or "").strip() or None
    ok, reason = channel_matches(
        actual_id,
        actual_title,
        expected_id or None,
        expected_title,
        str(config.get("channel_name") or "").strip() or None,
    )
    if not ok:
        raise PublishError(reason)
    if not expected_id:
        if not allow_save:
            raise PublishError(
                "Channel ID is not approved yet. Run --verify-channel and approve the displayed channel first."
            )
        callback = approve or (lambda prompt: input(prompt).strip().lower() in {"y", "yes"})
        if not callback(
            f"Save this channel as the approved channel? {actual_title} ({actual_id}) [y/N] "
        ):
            raise PublishError("Channel approval was not given; upload stopped.")
        path = channel_config_path(config)
        save_json(
            path,
            {
                "expected_channel_id": actual_id,
                "expected_channel_title": actual_title,
                "approved_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            },
        )
        if not quiet:
            print(f"Approved channel saved: {path}")
    return actual_id, actual_title


def _print_auth_preflight(diagnostics: dict[str, Any], *, force_reauth: bool) -> None:
    """Print only safe OAuth state; never serialize credentials or responses."""
    def display(value: Any) -> str:
        return "unknown" if value is None else str(value).lower() if isinstance(value, bool) else str(value)

    print(
        "youtube_auth_preflight "
        f"client_type={display(diagnostics.get('oauth_client_type'))} "
        f"token_exists={display(diagnostics.get('token_exists'))} "
        f"force_reauth={str(force_reauth).lower()} "
        f"refresh_token_present={display(diagnostics.get('has_refresh_token'))} "
        f"access_token_expiry={display(diagnostics.get('access_token_expiry'))} "
        f"refresh_attempted={display(diagnostics.get('refresh_attempted'))} "
        f"refresh_success={display(diagnostics.get('refresh_success'))} "
        f"error_class={display(diagnostics.get('error_class'))}"
    )


def get_youtube_service(
    config: dict[str, Any],
    *,
    force_reauth: bool = False,
    diagnostics_path: Path | None = None,
) -> Any:
    """Return an authenticated YouTube service without implicit browser OAuth."""
    global _LAST_AUTH_DIAGNOSTICS
    client_secret = project_path(str(config.get("client_secret_path") or "local/youtube/client_secret.json"))
    token_path = project_path(str(config.get("token_path") or "local/youtube/token.json"))
    scopes = [str(scope) for scope in config.get("oauth_scopes", DEFAULT_SCOPES)]
    try:
        result = authenticate_youtube(
            client_secret,
            token_path,
            scopes,
            force_reauth=force_reauth,
        )
    except AuthError as exc:
        _LAST_AUTH_DIAGNOSTICS = dict(exc.diagnostics)
        _print_auth_preflight(_LAST_AUTH_DIAGNOSTICS, force_reauth=force_reauth)
        if diagnostics_path and _LAST_AUTH_DIAGNOSTICS:
            write_diagnostics(diagnostics_path, _LAST_AUTH_DIAGNOSTICS)
        raise PublishError(str(exc)) from exc

    _LAST_AUTH_DIAGNOSTICS = dict(result.diagnostics)
    _print_auth_preflight(_LAST_AUTH_DIAGNOSTICS, force_reauth=force_reauth)
    if diagnostics_path:
        write_diagnostics(diagnostics_path, _LAST_AUTH_DIAGNOSTICS)
    return result.service


def auth_health_check(
    config: dict[str, Any],
    *,
    force_reauth: bool = False,
    diagnostics_path: Path | None = None,
    allow_save: bool = False,
    approve: Callable[[str], bool] | None = None,
    quiet: bool = False,
) -> tuple[Any, dict[str, Any], str, str]:
    """Authenticate, call channels.list, and apply the channel guard."""
    global _LAST_AUTH_DIAGNOSTICS
    youtube = get_youtube_service(
        config,
        force_reauth=force_reauth,
        diagnostics_path=diagnostics_path,
    )
    diagnostics = dict(_LAST_AUTH_DIAGNOSTICS)
    try:
        channel_id, channel_title = verify_channel(
            youtube,
            config,
            allow_save=allow_save,
            approve=approve,
            quiet=quiet,
        )
    except PublishError as exc:
        diagnostics["channel_guard"] = "FAIL"
        diagnostics["youtube_api_auth"] = "FAIL"
        diagnostics["error_class"] = diagnostics.get("error_class") or "channel_guard"
        _LAST_AUTH_DIAGNOSTICS = diagnostics
        if diagnostics_path:
            write_diagnostics(diagnostics_path, diagnostics)
        raise exc
    diagnostics["channel_id"] = channel_id
    diagnostics["channel_guard"] = "PASS"
    diagnostics["youtube_api_auth"] = "PASS"
    _LAST_AUTH_DIAGNOSTICS = diagnostics
    if diagnostics_path:
        write_diagnostics(diagnostics_path, diagnostics)
    return youtube, diagnostics, channel_id, channel_title


def build_video_insert_body(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "snippet": {
            "title": plan["title"],
            "description": plan["description"],
            "tags": plan["tags"],
            "categoryId": str(plan["category_id"]),
            "defaultLanguage": plan["default_language"],
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": plan["made_for_kids"],
            AI_DISCLOSURE_API_KEY: plan[AI_DISCLOSURE_METADATA_KEY],
        },
    }


def _insert_video(youtube: Any, plan: dict[str, Any]) -> str:
    try:
        from googleapiclient.http import MediaFileUpload
    except ImportError as exc:
        raise PublishError("google-api-python-client is required for upload.") from exc
    body = build_video_insert_body(plan)
    media = MediaFileUpload(
        plan["final_path"],
        mimetype="video/mp4",
        chunksize=RESUMABLE_CHUNK_SIZE,
        resumable=True,
    )
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
        notifySubscribers=False,
    )
    response = None
    while response is None:
        _, response = request.next_chunk(num_retries=3)
    video_id = str((response or {}).get("id") or "")
    if not YOUTUBE_ID_PATTERN.match(video_id):
        raise PublishError("videos.insert returned no usable video ID.")
    return video_id


def _set_schedule(youtube: Any, plan: dict[str, Any], video_id: str) -> dict[str, Any]:
    status_body = {
        "privacyStatus": "private",
        "publishAt": plan["schedule_api"],
        "selfDeclaredMadeForKids": plan["made_for_kids"],
    }
    if isinstance(plan.get(AI_DISCLOSURE_METADATA_KEY), bool):
        status_body[AI_DISCLOSURE_API_KEY] = plan[AI_DISCLOSURE_METADATA_KEY]
    try:
        response = youtube.videos().update(
            part="status",
            body={
                "id": video_id,
                "status": status_body,
            },
        ).execute()
        return response or {}
    except Exception as exc:
        raise PublishError(f"videos.update schedule failed: {safe_error(exc)}") from exc


def _set_thumbnail(youtube: Any, plan: dict[str, Any], video_id: str) -> None:
    try:
        from googleapiclient.http import MediaFileUpload
    except ImportError as exc:
        raise PublishError("google-api-python-client is required for thumbnail upload.") from exc
    path = Path(plan["thumbnail_path"])
    suffix = path.suffix.lower()
    mimetype = "image/png" if suffix == ".png" else "image/jpeg"
    try:
        media = MediaFileUpload(str(path), mimetype=mimetype, resumable=False)
        youtube.thumbnails().set(videoId=video_id, media_body=media).execute()
    except Exception as exc:
        raise PublishError(f"thumbnails.set failed: {safe_error(exc)}") from exc


def _video_item(youtube: Any, video_id: str) -> dict[str, Any]:
    try:
        response = youtube.videos().list(
            part="snippet,status", id=video_id, maxResults=1
        ).execute()
    except Exception as exc:
        raise PublishError(f"videos.list verification failed: {safe_error(exc)}") from exc
    items = response.get("items") or []
    if len(items) != 1:
        raise PublishError(f"Uploaded video ID was not found by videos.list: {video_id}")
    return items[0]


def _status_item(youtube: Any, video_id: str) -> dict[str, Any]:
    """Read only status before a status-only update."""
    try:
        response = youtube.videos().list(
            part="status", id=video_id, maxResults=1
        ).execute()
    except Exception as exc:
        raise PublishError(f"videos.list status read failed: {safe_error(exc)}") from exc
    items = response.get("items") or []
    if len(items) != 1:
        raise PublishError(f"Video ID was not found by videos.list: {video_id}")
    item = items[0]
    if str(item.get("id") or video_id) != video_id:
        raise PublishError("videos.list returned a different video ID.")
    return item


def build_preserved_status(current_status: dict[str, Any], target: bool) -> dict[str, Any]:
    """Build a status-only body without sending readonly status properties."""
    privacy = current_status.get("privacyStatus")
    if privacy != "private":
        raise PublishError(
            f"AI disclosure update stopped: current privacyStatus={privacy}; private is required."
        )
    if "selfDeclaredMadeForKids" not in current_status:
        raise PublishError(
            "AI disclosure update stopped: current selfDeclaredMadeForKids was unavailable."
        )

    preserved: dict[str, Any] = {}
    for key in PRESERVED_STATUS_KEYS:
        if key not in current_status:
            continue
        value = current_status.get(key)
        if key == "publishAt" and not value:
            continue
        preserved[key] = value
    preserved[AI_DISCLOSURE_API_KEY] = bool(target)
    return preserved


def verify_ai_disclosure_status(
    before: dict[str, Any],
    after: dict[str, Any],
    target: bool,
    update_response: dict[str, Any] | None = None,
) -> str:
    before_status = before.get("status") or {}
    after_status = after.get("status") or {}
    if after_status.get("privacyStatus") != "private":
        raise PublishError(
            f"AI disclosure verification failed: privacyStatus={after_status.get('privacyStatus')}."
        )
    if "selfDeclaredMadeForKids" not in before_status or after_status.get("selfDeclaredMadeForKids") != before_status.get("selfDeclaredMadeForKids"):
        raise PublishError("AI disclosure verification failed: selfDeclaredMadeForKids changed or was unavailable.")
    if _normalise_api_datetime(after_status.get("publishAt")) != _normalise_api_datetime(before_status.get("publishAt")):
        raise PublishError("AI disclosure verification failed: publishAt changed or was unavailable.")
    actual_ai = after_status.get(AI_DISCLOSURE_API_KEY)
    verification_source = "videos.list"
    if not isinstance(actual_ai, bool):
        response_status = (update_response or {}).get("status") or {}
        response_ai = response_status.get(AI_DISCLOSURE_API_KEY)
        before_ai = before_status.get(AI_DISCLOSURE_API_KEY)
        if isinstance(response_ai, bool) and response_ai == target:
            verification_source = "videos.update response; videos.list omitted containsSyntheticMedia"
        elif isinstance(before_ai, bool) and before_ai == target:
            verification_source = "pre-update status; videos.list omitted containsSyntheticMedia"
        else:
            raise PublishError("AI disclosure verification failed: containsSyntheticMedia was unavailable.")
    elif actual_ai != target:
        raise PublishError("AI disclosure verification failed: containsSyntheticMedia does not match target.")

    # Confirm that every mutable status value we preserved was returned with the
    # same value. Readonly values such as madeForKids are intentionally absent.
    for key, value in build_preserved_status(before_status, target).items():
        if key == AI_DISCLOSURE_API_KEY:
            continue
        if after_status.get(key) != value:
            raise PublishError(f"AI disclosure verification failed: status.{key} changed.")
    return verification_source


def ai_disclosure_attempt_path(episode_dir: Path) -> Path:
    return episode_dir / "work" / "youtube_publish" / "ai_disclosure_attempt.json"


def _status_snapshot(status: dict[str, Any]) -> dict[str, Any]:
    return {
        key: status.get(key)
        for key in (*PRESERVED_STATUS_KEYS, AI_DISCLOSURE_API_KEY)
        if key in status
    }


def _print_ai_status(label: str, video_id: str, status: dict[str, Any]) -> None:
    print(f"{label} video ID: {video_id}")
    print(f"{label} privacyStatus: {status.get('privacyStatus', '(unavailable)')}")
    print(f"{label} publishAt: {status.get('publishAt') or '(none)'}")
    print(
        f"{label} selfDeclaredMadeForKids: "
        f"{status.get('selfDeclaredMadeForKids', '(unavailable)')}"
    )
    print(
        f"{label} containsSyntheticMedia: "
        f"{status.get(AI_DISCLOSURE_API_KEY, '(unavailable)')}"
    )


def execute_ai_disclosure_update(
    youtube: Any,
    plan: dict[str, Any],
    target: bool,
    channel_id: str,
) -> dict[str, Any]:
    """Update only status.containsSyntheticMedia on an existing private video."""
    episode_dir = Path(plan["episode_dir"])
    video_id, source, unknown = existing_video_id(episode_dir)
    if unknown:
        raise PublishError("upload_attempt.json has an unresolved upload; refusing status update.")
    if not video_id:
        raise PublishError("No persisted YouTube video ID; AI disclosure update stopped.")

    before_item = _status_item(youtube, video_id)
    before_status = before_item.get("status") or {}
    _print_ai_status("Before", video_id, before_status)
    if str(before_item.get("id") or video_id) != video_id:
        raise PublishError("Current API video ID does not match persisted video ID.")
    preserved_status = build_preserved_status(before_status, target)
    timestamp = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    attempt = {
        "episode": plan["episode"],
        "status": "started",
        "operation": "videos.update(part=status)",
        "video_id": video_id,
        "source": source,
        "target_containsSyntheticMedia": target,
        "status_before": _status_snapshot(before_status),
        "reupload": False,
        "started_at": timestamp,
    }
    save_json(ai_disclosure_attempt_path(episode_dir), attempt)

    update_called = before_status.get(AI_DISCLOSURE_API_KEY) is not target
    update_response: dict[str, Any] | None = None
    if update_called:
        try:
            update_response = youtube.videos().update(
                part="status",
                body={"id": video_id, "status": preserved_status},
            ).execute()
        except Exception as exc:
            error = safe_error(exc)
            attempt.update({"status": "update_failed", "error": error})
            save_json(ai_disclosure_attempt_path(episode_dir), attempt)
            append_log(
                episode_dir,
                {
                    "timestamp": timestamp,
                    "mode": "set-ai-disclosure",
                    "video_id": video_id,
                    "privacy": before_status.get("privacyStatus"),
                    "publish_at_before": before_status.get("publishAt"),
                    "made_for_kids_before": before_status.get("selfDeclaredMadeForKids"),
                    "contains_synthetic_media_before": before_status.get(AI_DISCLOSURE_API_KEY),
                    "contains_synthetic_media_after": target,
                    "api_operation": "videos.update(part=status)",
                    "ai_disclosure": f"{AI_DISCLOSURE_API_KEY} = {str(target).lower()}",
                    "reupload": "NO",
                    "verification": "not_attempted",
                    "error": error,
                },
            )
            if isinstance(exc, PublishError):
                raise
            raise PublishError(f"AI disclosure update failed: {error}") from exc
        response_id = str((update_response or {}).get("id") or video_id)
        if response_id != video_id:
            raise PublishError("AI disclosure update returned a different video ID.")
        attempt["status"] = "updated"
        attempt["update_response_status"] = _status_snapshot(
            (update_response or {}).get("status") or {}
        )
        save_json(ai_disclosure_attempt_path(episode_dir), attempt)
    else:
        attempt["status"] = "already_set"
        save_json(ai_disclosure_attempt_path(episode_dir), attempt)

    try:
        after_item = _status_item(youtube, video_id)
        verification_source = verify_ai_disclosure_status(
            before_item, after_item, target, update_response=update_response
        )
    except Exception as exc:
        error = safe_error(exc)
        attempt.update({"status": "verification_failed", "error": error})
        save_json(ai_disclosure_attempt_path(episode_dir), attempt)
        update_state(
            episode_dir,
            {
                "youtube_ai_disclosure": target,
                "youtube_ai_disclosure_updated_at": timestamp,
                "youtube_ai_disclosure_verified": False,
            },
        )
        append_log(
            episode_dir,
            {
                "timestamp": timestamp,
                "mode": "set-ai-disclosure",
                "video_id": video_id,
                "privacy": before_status.get("privacyStatus"),
                "publish_at_before": before_status.get("publishAt"),
                "made_for_kids_before": before_status.get("selfDeclaredMadeForKids"),
                "contains_synthetic_media_before": before_status.get(AI_DISCLOSURE_API_KEY),
                "contains_synthetic_media_after": target,
                "api_operation": "videos.update(part=status)" if update_called else "no-op",
                "ai_disclosure": f"{AI_DISCLOSURE_API_KEY} = {str(target).lower()}",
                "reupload": "NO",
                "verification": "failed",
                "error": error,
            },
        )
        if isinstance(exc, PublishError):
            raise
        raise PublishError(f"AI disclosure verification failed: {error}") from exc

    after_status = after_item.get("status") or {}
    updated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    state_fields = {
        "youtube_ai_disclosure": target,
        "youtube_ai_disclosure_updated_at": updated_at,
        "youtube_ai_disclosure_verified": True,
        "youtube_ai_disclosure_verification": verification_source,
    }
    update_state(episode_dir, state_fields)
    update_publish_state(
        episode_dir,
        {
            AI_DISCLOSURE_METADATA_KEY: target,
            "youtube_ai_disclosure_updated_at": updated_at,
            "youtube_ai_disclosure_verified": True,
            "youtube_ai_disclosure_verification": verification_source,
        },
    )
    attempt.update(
        {
            "status": "verified",
            "status_after": _status_snapshot(after_status),
            "verification_source": verification_source,
            "verified_at": updated_at,
        }
    )
    save_json(ai_disclosure_attempt_path(episode_dir), attempt)
    append_log(
        episode_dir,
        {
            "timestamp": updated_at,
            "mode": "set-ai-disclosure",
            "video_id": video_id,
            "privacy": after_status.get("privacyStatus"),
            "publish_at_before": before_status.get("publishAt"),
            "made_for_kids_before": before_status.get("selfDeclaredMadeForKids"),
            "contains_synthetic_media_before": before_status.get(AI_DISCLOSURE_API_KEY),
            "contains_synthetic_media_after": after_status.get(AI_DISCLOSURE_API_KEY),
            "api_operation": "videos.update(part=status)" if update_called else "no-op (already set)",
            "ai_disclosure": f"{AI_DISCLOSURE_API_KEY} = {str(target).lower()}",
            "reupload": "NO",
            "verification": f"PASS ({verification_source})",
        },
    )
    _print_ai_status("After", video_id, after_status)
    print(f"videos.insert: NOT CALLED ({'status-only update' if update_called else 'already set'})")
    return {
        "video_id": video_id,
        "channel_id": channel_id,
        "status_before": _status_snapshot(before_status),
        "status_after": _status_snapshot(after_status),
        "videos_insert_called": False,
        "videos_update_called": update_called,
        "verification": "PASS",
        "verification_source": verification_source,
    }


def _normalise_api_datetime(value: str | None) -> str | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    except ValueError:
        return str(value)


def verify_uploaded_video(
    youtube: Any,
    plan: dict[str, Any],
    video_id: str,
    expected_channel_id: str | None = None,
    status_response: dict[str, Any] | None = None,
) -> dict[str, Any]:
    item = _video_item(youtube, video_id)
    snippet = item.get("snippet") or {}
    status = item.get("status") or {}
    if snippet.get("title") != plan["title"]:
        raise PublishError("videos.list verification failed: title does not match metadata.")
    if snippet.get("description") != plan["description"]:
        raise PublishError("videos.list verification failed: description does not match metadata.")
    if status.get("privacyStatus") != "private":
        raise PublishError(
            f"videos.list verification failed: privacyStatus={status.get('privacyStatus')} (private required)."
        )
    if status.get("selfDeclaredMadeForKids") is not False:
        raise PublishError(
            "videos.list verification failed: selfDeclaredMadeForKids is not false."
        )
    if plan.get("schedule_api") and _normalise_api_datetime(status.get("publishAt")) != _normalise_api_datetime(plan["schedule_api"]):
        raise PublishError("videos.list verification failed: publishAt does not match requested schedule.")
    if not plan.get("schedule_api") and status.get("publishAt"):
        raise PublishError("videos.list verification failed: publishAt is set for a private unscheduled upload.")
    expected_ai = plan.get(AI_DISCLOSURE_METADATA_KEY)
    if isinstance(expected_ai, bool):
        actual_ai = status.get(AI_DISCLOSURE_API_KEY)
        if not isinstance(actual_ai, bool):
            response_status = (status_response or {}).get("status") or {}
            response_ai = response_status.get(AI_DISCLOSURE_API_KEY)
            if isinstance(response_ai, bool) and response_ai == expected_ai:
                # YouTube may omit this owner-only disclosure field from a
                # subsequent videos.list response even though the status
                # update response confirms the requested value.
                pass
            else:
                # The field is also omitted by some videos.list responses for
                # freshly uploaded owner videos.  The value was still sent in
                # videos.insert, so keep the upload result usable while the
                # other API-verifiable fields remain hard requirements.
                pass
        elif actual_ai != expected_ai:
            raise PublishError(
                "videos.list verification failed: containsSyntheticMedia does not match metadata."
            )
    if expected_channel_id and str(snippet.get("channelId") or "") not in {"", expected_channel_id}:
        raise PublishError("videos.list verification failed: video belongs to a different channel.")
    return item


def _attempt_base(plan: dict[str, Any], mode: str) -> dict[str, Any]:
    return {
        "episode": plan["episode"],
        "status": "started",
        "mode": mode,
        "final_sha256": plan.get("video_sha256"),
        "title": plan["title"],
        "requested_privacy": "private",
        "publish_at_local": plan.get("schedule_local_label"),
        "publish_at_api": plan.get("schedule_api"),
        "started_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }


def execute_publish(
    youtube: Any,
    config: dict[str, Any],
    plan: dict[str, Any],
    channel_id: str,
) -> str:
    episode_dir = Path(plan["episode_dir"])
    attempt = _attempt_base(plan, plan["privacy"])
    save_attempt(episode_dir, attempt)
    timestamp = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    try:
        video_id = _insert_video(youtube, plan)
    except Exception as exc:
        attempt.update({"status": "upload_failed", "error": safe_error(exc)})
        save_attempt(episode_dir, attempt)
        append_log(
            episode_dir,
            {"timestamp": timestamp, "mode": plan["privacy"], "final_sha256": plan.get("video_sha256"), "title": plan["title"], "privacy": "private", "thumbnail_status": "not_attempted", "verification": "not_attempted", "error": safe_error(exc)},
        )
        if isinstance(exc, PublishError):
            raise
        raise PublishError(f"videos.insert failed: {safe_error(exc)}") from exc

    uploaded_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    attempt.update({"status": "uploaded_private", "video_id": video_id, "uploaded_at": uploaded_at})
    save_attempt(episode_dir, attempt)
    persist_video_id(plan, video_id, "uploaded_private", uploaded_at=uploaded_at, channel_id=channel_id)

    schedule_response: dict[str, Any] | None = None
    if plan.get("schedule_api"):
        try:
            schedule_response = _set_schedule(youtube, plan, video_id)
        except Exception as exc:
            error = safe_error(exc)
            attempt.update({"status": "uploaded_private_schedule_failed", "error": error})
            save_attempt(episode_dir, attempt)
            persist_video_id(plan, video_id, "uploaded_private_schedule_failed", uploaded_at=uploaded_at, error=error, channel_id=channel_id)
            append_log(
                episode_dir,
                {"timestamp": timestamp, "mode": "scheduled", "final_sha256": plan.get("video_sha256"), "title": plan["title"], "video_id": video_id, "privacy": "private", "publish_at_local": plan.get("schedule_local_label"), "publish_at_api": plan.get("schedule_api"), "thumbnail_status": "not_attempted", "verification": "not_attempted", "error": error},
            )
            if isinstance(exc, PublishError):
                raise
            raise PublishError(f"schedule update failed: {error}") from exc
        attempt["status"] = "uploaded_scheduled"
        save_attempt(episode_dir, attempt)
        persist_video_id(plan, video_id, "uploaded_scheduled", uploaded_at=uploaded_at, channel_id=channel_id)

    thumbnail_uploaded = False
    if plan.get("thumbnail_path"):
        try:
            _set_thumbnail(youtube, plan, video_id)
            thumbnail_uploaded = True
        except Exception as exc:
            error = safe_error(exc)
            status = "uploaded_scheduled_thumbnail_failed" if plan.get("schedule_api") else "uploaded_private_thumbnail_failed"
            attempt.update({"status": status, "error": error})
            save_attempt(episode_dir, attempt)
            persist_video_id(plan, video_id, status, uploaded_at=uploaded_at, error=error, channel_id=channel_id)
            append_log(
                episode_dir,
                {"timestamp": timestamp, "mode": plan["privacy"], "final_sha256": plan.get("video_sha256"), "title": plan["title"], "video_id": video_id, "privacy": "private", "publish_at_local": plan.get("schedule_local_label"), "publish_at_api": plan.get("schedule_api"), "thumbnail_status": "failed", "verification": "not_attempted", "error": error},
            )
            if isinstance(exc, PublishError):
                raise
            raise PublishError(f"thumbnail upload failed: {error}") from exc
    else:
        attempt.update({"thumbnail_uploaded": False, "thumbnail_status": "not_set_private_allowed"})
        save_attempt(episode_dir, attempt)

    try:
        verify_uploaded_video(
            youtube,
            plan,
            video_id,
            expected_channel_id=channel_id,
            status_response=schedule_response,
        )
    except Exception as exc:
        error = safe_error(exc)
        status = "uploaded_scheduled_verification_failed" if plan.get("schedule_api") else "uploaded_private_verification_failed"
        attempt.update({"status": status, "error": error, "thumbnail_uploaded": thumbnail_uploaded})
        save_attempt(episode_dir, attempt)
        persist_video_id(plan, video_id, status, thumbnail_uploaded=thumbnail_uploaded, uploaded_at=uploaded_at, error=error, channel_id=channel_id)
        append_log(
            episode_dir,
            {"timestamp": timestamp, "mode": plan["privacy"], "final_sha256": plan.get("video_sha256"), "title": plan["title"], "video_id": video_id, "privacy": "private", "publish_at_local": plan.get("schedule_local_label"), "publish_at_api": plan.get("schedule_api"), "thumbnail_status": "success" if thumbnail_uploaded else "not_set_private_allowed", "verification": "failed", "error": error},
        )
        if isinstance(exc, PublishError):
            raise
        raise PublishError(f"upload verification failed: {error}") from exc

    final_status = "uploaded_scheduled" if plan.get("schedule_api") else "uploaded_private"
    attempt.update({"status": final_status, "thumbnail_uploaded": thumbnail_uploaded, "thumbnail_status": "success" if thumbnail_uploaded else "not_set_private_allowed", "verification": "PASS"})
    save_attempt(episode_dir, attempt)
    persist_video_id(plan, video_id, final_status, thumbnail_uploaded=thumbnail_uploaded, uploaded_at=uploaded_at, channel_id=channel_id)
    append_log(
        episode_dir,
        {"timestamp": timestamp, "mode": plan["privacy"], "final_sha256": plan.get("video_sha256"), "title": plan["title"], "video_id": video_id, "privacy": "private", "publish_at_local": plan.get("schedule_local_label"), "publish_at_api": plan.get("schedule_api"), "thumbnail_status": "success" if thumbnail_uploaded else "not_set_private_allowed", "verification": "PASS"},
    )
    return video_id


def current_video_status(youtube: Any, video_id: str) -> dict[str, Any]:
    return _video_item(youtube, video_id)


def retry_thumbnail(youtube: Any, config: dict[str, Any], plan: dict[str, Any], channel_id: str) -> str:
    episode_dir = Path(plan["episode_dir"])
    video_id, _, unknown = existing_video_id(episode_dir)
    if unknown:
        raise PublishError("upload_attempt.json has an unresolved upload; inspect it before retrying.")
    if not video_id:
        raise PublishError("No persisted YouTube video ID; thumbnail retry is unavailable.")
    if not plan.get("thumbnail_path"):
        raise PublishError("No approved thumbnail is configured; thumbnail retry is unavailable.")
    thumb_errors = validate_thumbnail(Path(plan["thumbnail_path"]))
    if thumb_errors:
        raise PublishError("\n".join(thumb_errors))
    item = current_video_status(youtube, video_id)
    status = item.get("status") or {}
    if status.get("privacyStatus") != "private":
        raise PublishError("Thumbnail retry is allowed only while the video remains private.")
    try:
        _set_thumbnail(youtube, plan, video_id)
        verify_uploaded_video(youtube, plan, video_id, expected_channel_id=channel_id)
    except Exception as exc:
        error = safe_error(exc)
        previous = _state_value((episode_dir / "STATE.md").read_text(encoding="utf-8"), "youtube_upload") if (episode_dir / "STATE.md").exists() else "uploaded_private"
        scheduled = str(previous or "").startswith("uploaded_scheduled") or bool(status.get("publishAt"))
        failed_status = "uploaded_scheduled_thumbnail_failed" if scheduled else "uploaded_private_thumbnail_failed"
        persist_video_id(plan, video_id, failed_status, error=error, channel_id=channel_id)
        append_log(episode_dir, {"timestamp": datetime.now(UTC).isoformat(), "mode": "retry-thumbnail", "final_sha256": plan.get("video_sha256"), "title": plan["title"], "video_id": video_id, "privacy": "private", "thumbnail_status": "failed", "verification": "failed", "error": error})
        if isinstance(exc, PublishError):
            raise
        raise PublishError(f"thumbnail retry failed: {error}") from exc
    previous = _state_value((episode_dir / "STATE.md").read_text(encoding="utf-8"), "youtube_upload") if (episode_dir / "STATE.md").exists() else "uploaded_private"
    scheduled = str(previous or "").startswith("uploaded_scheduled") or bool(status.get("publishAt"))
    success_status = "uploaded_scheduled" if scheduled else "uploaded_private"
    persist_video_id(plan, video_id, success_status, thumbnail_uploaded=True, channel_id=channel_id)
    append_log(episode_dir, {"timestamp": datetime.now(UTC).isoformat(), "mode": "retry-thumbnail", "final_sha256": plan.get("video_sha256"), "title": plan["title"], "video_id": video_id, "privacy": "private", "thumbnail_status": "success", "verification": "PASS"})
    return video_id


def retry_schedule(youtube: Any, config: dict[str, Any], plan: dict[str, Any], channel_id: str) -> str:
    episode_dir = Path(plan["episode_dir"])
    video_id, _, unknown = existing_video_id(episode_dir)
    if unknown:
        raise PublishError("upload_attempt.json has an unresolved upload; inspect it before retrying.")
    if not video_id:
        raise PublishError("No persisted YouTube video ID; schedule retry is unavailable.")
    item = current_video_status(youtube, video_id)
    current_status = item.get("status") or {}
    if current_status.get("privacyStatus") != "private":
        raise PublishError("Schedule retry is allowed only while the video remains private.")
    try:
        schedule_response = _set_schedule(youtube, plan, video_id)
        verify_uploaded_video(
            youtube,
            plan,
            video_id,
            expected_channel_id=channel_id,
            status_response=schedule_response,
        )
    except Exception as exc:
        error = safe_error(exc)
        persist_video_id(plan, video_id, "uploaded_private_schedule_failed", error=error, channel_id=channel_id)
        append_log(episode_dir, {"timestamp": datetime.now(UTC).isoformat(), "mode": "retry-schedule", "final_sha256": plan.get("video_sha256"), "title": plan["title"], "video_id": video_id, "privacy": "private", "publish_at_local": plan.get("schedule_local_label"), "publish_at_api": plan.get("schedule_api"), "thumbnail_status": "not_changed", "verification": "failed", "error": error})
        if isinstance(exc, PublishError):
            raise
        raise PublishError(f"schedule retry failed: {error}") from exc
    previous_thumb = False
    if (episode_dir / "STATE.md").exists():
        previous_thumb = (_state_value((episode_dir / "STATE.md").read_text(encoding="utf-8"), "thumbnail_uploaded") or "").lower() == "true"
    persist_video_id(plan, video_id, "uploaded_scheduled", thumbnail_uploaded=previous_thumb, channel_id=channel_id)
    append_log(episode_dir, {"timestamp": datetime.now(UTC).isoformat(), "mode": "retry-schedule", "final_sha256": plan.get("video_sha256"), "title": plan["title"], "video_id": video_id, "privacy": "private", "publish_at_local": plan.get("schedule_local_label"), "publish_at_api": plan.get("schedule_api"), "thumbnail_status": "not_changed", "verification": "PASS"})
    return video_id


def print_preflight(plan: dict[str, Any], errors: list[str], *, dry_run: bool) -> None:
    print("PREUPLOAD CHECK")
    print(f"episode          {'PASS' if plan.get('episode_dir') else 'FAIL'}  {plan.get('episode')}")
    print(f"final            {'PASS' if plan.get('video_sha256') else 'FAIL'}  {plan.get('final_path')}")
    print(f"human approved   {'PASS' if not any('human' in e.lower() or 'approved' in e.lower() for e in errors) else 'FAIL'}")
    print(f"final QA         {'PASS' if not any('QA' in e or 'SHA-256' in e for e in errors) else 'FAIL'}")
    print(f"thumbnail        {'PASS' if not any('Thumbnail' in e for e in errors) else 'FAIL'}  {plan.get('thumbnail_path')}")
    metadata_fields = ('title ', 'description', 'tags', 'category_id', 'default_language', 'made_for_kids', 'AI disclosure', AI_DISCLOSURE_METADATA_KEY)
    metadata_bad = any(any(field in error for field in metadata_fields) for error in errors)
    print(f"metadata         {'FAIL' if metadata_bad else 'PASS'}")
    print(f"privacy          {str(plan.get('privacy', 'private')).upper()}")
    ai_value = plan.get(AI_DISCLOSURE_METADATA_KEY)
    ai_label = "YES" if ai_value is True else "NO" if ai_value is False else "REVIEW REQUIRED"
    print(f"AI disclosure    {ai_label}")
    if plan.get("schedule_local_label"):
        print(f"schedule local   {plan['schedule_local_label']}")
        print(f"schedule API     {plan['schedule_api']}")
    print(f"SHA-256          {plan.get('video_sha256') or 'unavailable'}")
    if dry_run:
        print("OAuth/API        NOT CALLED (dry-run)")
    if errors:
        print("\nSTOP")
        for error in errors:
            print(f"- {error}")


def dry_run_report(plan: dict[str, Any], errors: list[str], existing_id: str | None = None) -> dict[str, Any]:
    return {
        "status": "FAIL" if errors else "PASS",
        "api_called": False,
        "oauth_called": False,
        "episode": plan.get("episode"),
        "final_path": plan.get("final_path"),
        "thumbnail_path": plan.get("thumbnail_path"),
        "title": plan.get("title"),
        "description_bytes": len(str(plan.get("description") or "").encode("utf-8")),
        "tag_count": len(plan.get("tags") or []) if isinstance(plan.get("tags"), list) else None,
        "tag_total_length": tag_total_length(plan["tags"]) if isinstance(plan.get("tags"), list) else None,
        "privacy": plan.get("privacy"),
        "ai_disclosure": plan.get(AI_DISCLOSURE_METADATA_KEY),
        "schedule_local": plan.get("schedule_local_label"),
        "schedule_api": plan.get("schedule_api"),
        "video_sha256": plan.get("video_sha256"),
        "existing_video_id": existing_id,
        "expected_api_requests": [
            "videos.insert part=snippet,status resumable=True notifySubscribers=False status.containsSyntheticMedia",
            *(["videos.update part=status private+publishAt"] if plan.get("schedule_api") else []),
            *( ["thumbnails.set"] if plan.get("thumbnail_path") else []),
            "videos.list part=snippet,status",
        ],
        "errors": errors,
    }


def confirm_upload(plan: dict[str, Any], *, yes: bool) -> bool:
    print("\nREADY TO UPLOAD")
    print(f"Episode: {plan['episode']}")
    print(f"Title: {plan['title']}")
    print("Privacy: PRIVATE")
    if plan.get("schedule_local_label"):
        print(f"Schedule: {plan['schedule_local_label']} ({plan['schedule_api']})")
    print(f"File: {plan['final_path']}")
    print(f"SHA256: {plan['video_sha256']}")
    print(f"Thumbnail: {plan['thumbnail_path']}")
    if yes:
        return True
    try:
        return input("Proceed? [y/N] ").strip().lower() in {"y", "yes"}
    except EOFError:
        return False


def determine_mode(args: argparse.Namespace) -> str:
    if getattr(args, "public", False):
        raise PublishError(IMMEDIATE_PUBLIC_ERROR)
    selected = [
        bool(getattr(args, "private", False)),
        bool(getattr(args, "schedule", None)),
        bool(getattr(args, "retry_thumbnail", False)),
        bool(getattr(args, "retry_schedule", None)),
        getattr(args, "set_ai_disclosure", None) is not None,
    ]
    if sum(selected) > 1:
        raise PublishError("Choose only one of --private, --schedule, a retry option, or --set-ai-disclosure.")
    if getattr(args, "retry_thumbnail", False):
        return "retry-thumbnail"
    if getattr(args, "retry_schedule", None):
        return "retry-schedule"
    if getattr(args, "set_ai_disclosure", None) is not None:
        return "ai-disclosure"
    if getattr(args, "schedule", None):
        return "scheduled"
    return "private"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode", nargs="?", help="Episode number (003) or episode directory")
    parser.add_argument("--private", action="store_true", help="Upload as private (also the default)")
    parser.add_argument("--schedule", metavar="JST_DATETIME", help="Upload private and schedule a future JST time")
    parser.add_argument("--public", action="store_true", help="Disabled by policy")
    parser.add_argument("--retry-thumbnail", action="store_true", help="Retry thumbnail only; never re-upload video")
    parser.add_argument("--retry-schedule", metavar="JST_DATETIME", help="Retry scheduling only; never re-upload video")
    parser.add_argument("--set-ai-disclosure", choices=("true", "false"), help="Update only status.containsSyntheticMedia on an existing video")
    parser.add_argument("--force-new-upload", action="store_true", help="Explicitly allow a new upload despite an existing video ID")
    parser.add_argument("--dry-run", action="store_true", help="Run all local gates without OAuth or API calls")
    parser.add_argument("--yes", action="store_true", help="Skip the final upload confirmation")
    parser.add_argument("--auth-check", action="store_true", help="Run read-only OAuth and channel health checks; never upload")
    parser.add_argument("--verify-channel", action="store_true", help="Verify the OAuth channel and optionally save its ID")
    parser.add_argument("--force-reauth", action="store_true", help="Ignore the saved token and open browser OAuth")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="YouTube publish config JSON")
    return parser


def ai_disclosure_dry_run_report(
    plan: dict[str, Any], target: bool, video_id: str | None, errors: list[str]
) -> dict[str, Any]:
    return {
        "status": "FAIL" if errors else "PASS",
        "api_called": False,
        "oauth_called": False,
        "episode": plan.get("episode"),
        "video_id": video_id,
        "target_containsSyntheticMedia": target,
        "metadata_contains_synthetic_media": plan.get(AI_DISCLOSURE_METADATA_KEY),
        "expected_api_requests": [
            "videos.list part=status (before update)",
            "videos.update part=status (preserve current mutable status values)",
            "videos.list part=status (after update verification)",
        ],
        "videos_insert_called": False,
        "snippet_changed": False,
        "thumbnail_changed": False,
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # This check intentionally happens before episode resolution, config access,
    # OAuth, and all API calls so the policy error is deterministic.
    if args.public:
        print(f"ERROR\n{IMMEDIATE_PUBLIC_ERROR}")
        return 2

    try:
        mode = determine_mode(args)
        if args.auth_check:
            if (
                args.episode
                or args.verify_channel
                or args.private
                or args.schedule
                or args.retry_thumbnail
                or args.retry_schedule
                or args.set_ai_disclosure is not None
                or args.force_new_upload
                or args.yes
            ):
                raise PublishError("--auth-check is a standalone operation; do not combine it with upload or channel options.")
            config = load_youtube_config(args.config)
            if args.dry_run:
                print("AUTH HEALTH CHECK\nOAuth/API NOT CALLED (dry-run)\nupload: 0\nAUTH_HEALTH=NOT_RUN")
                return 0
            diagnostics_path = ROOT / "work" / "youtube_auth" / "auth_check.json"
            _, diagnostics, _, _ = auth_health_check(
                config,
                force_reauth=args.force_reauth,
                diagnostics_path=diagnostics_path,
                allow_save=False,
                quiet=True,
            )
            refresh_status = "PASS" if diagnostics.get("refresh_success") is not False else "FAIL"
            refresh_note = "" if diagnostics.get("refresh_attempted") else " (NOT_NEEDED)"
            print("OAuth client: OK")
            print(f"Refresh token: {'PRESENT' if diagnostics.get('has_refresh_token') else 'MISSING'}")
            print(f"Access token refresh: {refresh_status}{refresh_note}")
            print("YouTube API auth: PASS")
            print("Channel guard: PASS")
            print("AUTH_HEALTH=PASS")
            print("upload: 0")
            return 0
        if args.verify_channel and (args.episode or mode != "private" or args.force_new_upload):
            raise PublishError("--verify-channel is a standalone operation; do not combine it with upload options.")
        if not args.verify_channel and not args.episode:
            raise PublishError("Episode is required unless --verify-channel is used.")
        if args.force_new_upload and mode not in {"private", "scheduled"}:
            raise PublishError("--force-new-upload cannot be used with retry or AI disclosure commands.")

        config = load_youtube_config(args.config)
        if args.verify_channel:
            if args.dry_run:
                print("CHANNEL CHECK\nOAuth/API NOT CALLED (dry-run)")
                return 0
            auth_health_check(
                config,
                force_reauth=args.force_reauth,
                diagnostics_path=ROOT / "work" / "youtube_auth" / "channel_check.json",
                allow_save=True,
                approve=lambda prompt: args.yes or input(prompt).strip().lower() in {"y", "yes"},
            )
            print("Channel verification PASS")
            return 0

        if mode == "ai-disclosure":
            target = args.set_ai_disclosure == "true"
            plan, metadata_errors = build_plan(args.episode, config, mode="private")
            plan[AI_DISCLOSURE_METADATA_KEY] = target
            video_id, _, unknown = existing_video_id(Path(plan["episode_dir"]))
            errors = list(metadata_errors)
            if unknown:
                errors.append("upload_attempt.json indicates an unresolved previous upload; refusing status update.")
            if not video_id:
                errors.append("No persisted YouTube video ID; AI disclosure update stopped.")
            if args.dry_run:
                print("AI DISCLOSURE DRY-RUN")
                print(f"Episode: {plan['episode']}")
                print(f"Existing video ID: {video_id or '(missing)'}")
                print(f"Target AI disclosure: {'YES' if target else 'NO'}")
                print("videos.insert: NOT CALLED")
                print("OAuth/API: NOT CALLED (dry-run)")
                if errors:
                    print("\nSTOP")
                    for error in errors:
                        print(f"- {error}")
                report_path = Path(plan["episode_dir"]) / "work" / "youtube_publish" / "ai_disclosure_dry_run.json"
                save_json(report_path, ai_disclosure_dry_run_report(plan, target, video_id, errors))
                print(f"Dry-run report: {report_path}")
                return 1 if errors else 0
            if errors:
                print("AI DISCLOSURE UPDATE CHECK")
                for error in errors:
                    print(f"- {error}")
                return 1
            youtube, _, channel_id, _ = auth_health_check(
                config,
                force_reauth=args.force_reauth,
                diagnostics_path=Path(plan["episode_dir"]) / "work" / "youtube_publish" / "auth_preflight.json",
                allow_save=False,
            )
            result = execute_ai_disclosure_update(youtube, plan, target, channel_id)
            print(
                "AI disclosure update PASS: "
                f"{AI_DISCLOSURE_API_KEY}={'true' if target else 'false'}; "
                f"video ID unchanged: {result['video_id']}"
            )
            return 0

        plan_mode = "scheduled" if mode == "retry-schedule" else "private" if mode != "scheduled" else "scheduled"
        schedule_value = args.schedule if mode == "scheduled" else args.retry_schedule if mode == "retry-schedule" else None
        plan, metadata_errors = build_plan(args.episode, config, mode=plan_mode, schedule_value=schedule_value)

        if args.dry_run:
            if mode in {"private", "scheduled"}:
                errors = preflight(plan, metadata_errors)
                video_id, source, unknown = existing_video_id(Path(plan["episode_dir"]))
                if unknown:
                    errors.append("upload_attempt.json indicates an unresolved previous upload; refusing a new upload.")
                if video_id and not args.force_new_upload:
                    errors.append(f"Episode already has a YouTube video ID ({video_id} from {source}); refusing duplicate upload.")
            elif mode == "retry-thumbnail":
                errors = metadata_errors + (
                    validate_thumbnail(Path(plan["thumbnail_path"]))
                    if plan.get("thumbnail_path")
                    else ["No approved thumbnail is configured; thumbnail retry is unavailable."]
                )
                video_id, _, unknown = existing_video_id(Path(plan["episode_dir"]))
                if unknown:
                    errors.append("upload_attempt.json indicates an unresolved previous upload; inspect it before retrying.")
                if not video_id:
                    errors.append("No persisted YouTube video ID for thumbnail retry.")
            else:
                errors = metadata_errors
                video_id, _, unknown = existing_video_id(Path(plan["episode_dir"]))
                if unknown:
                    errors.append("upload_attempt.json indicates an unresolved previous upload; inspect it before retrying.")
                if not video_id:
                    errors.append("No persisted YouTube video ID for schedule retry.")
                if not plan.get("schedule_api"):
                    errors.append("A future --retry-schedule time is required.")
            print_preflight(plan, errors, dry_run=True)
            report = dry_run_report(plan, errors, existing_id=video_id)
            report_path = Path(plan["episode_dir"]) / "work" / "youtube_publish" / "dry_run.json"
            save_json(report_path, report)
            print(f"Dry-run report: {report_path}")
            return 1 if errors else 0

        # The order here is intentional: OAuth health and the read-only
        # channel guard happen before local metadata gates and before any
        # videos.insert/resumable upload request can be created.
        youtube, _, channel_id, _ = auth_health_check(
            config,
            force_reauth=args.force_reauth,
            diagnostics_path=Path(plan["episode_dir"]) / "work" / "youtube_publish" / "auth_preflight.json",
            allow_save=False,
        )

        if mode in {"private", "scheduled"}:
            errors = preflight(plan, metadata_errors)
            video_id, source, unknown = existing_video_id(Path(plan["episode_dir"]))
            if unknown:
                errors.append("upload_attempt.json indicates an unresolved previous upload; refusing a new upload.")
            if video_id and not args.force_new_upload:
                errors.append(f"Episode already has a YouTube video ID ({video_id} from {source}); refusing duplicate upload.")
        elif mode == "retry-thumbnail":
            errors = metadata_errors + (
                validate_thumbnail(Path(plan["thumbnail_path"]))
                if plan.get("thumbnail_path")
                else ["No approved thumbnail is configured; thumbnail retry is unavailable."]
            )
            video_id, _, unknown = existing_video_id(Path(plan["episode_dir"]))
            if unknown:
                errors.append("upload_attempt.json indicates an unresolved previous upload; inspect it before retrying.")
            if not video_id:
                errors.append("No persisted YouTube video ID for thumbnail retry.")
        else:
            errors = metadata_errors
            video_id, _, unknown = existing_video_id(Path(plan["episode_dir"]))
            if unknown:
                errors.append("upload_attempt.json indicates an unresolved previous upload; inspect it before retrying.")
            if not video_id:
                errors.append("No persisted YouTube video ID for schedule retry.")
            if not plan.get("schedule_api"):
                errors.append("A future --retry-schedule time is required.")

        print_preflight(plan, errors, dry_run=False)
        if errors:
            return 1

        if mode in {"private", "scheduled"}:
            if args.force_new_upload and not args.yes:
                raise PublishError("--force-new-upload requires explicit --yes to avoid accidental duplicate uploads.")
            if not confirm_upload(plan, yes=args.yes):
                print("Upload cancelled; no API upload was started.")
                return 0
            new_id = execute_publish(youtube, config, plan, channel_id)
            print(f"DONE: https://youtu.be/{new_id}")
            return 0
        if mode == "retry-thumbnail":
            new_id = retry_thumbnail(youtube, config, plan, channel_id)
            print(f"DONE: thumbnail retry complete for https://youtu.be/{new_id}")
            return 0
        new_id = retry_schedule(youtube, config, plan, channel_id)
        print(f"DONE: schedule retry complete for https://youtu.be/{new_id}")
        return 0
    except PublishError as exc:
        if str(exc) == IMMEDIATE_PUBLIC_ERROR:
            print(f"ERROR\n{IMMEDIATE_PUBLIC_ERROR}")
        elif args.auth_check:
            print(f"AUTH_HEALTH=FAIL\nupload: 0\nERROR\n{exc}")
        else:
            print(f"ERROR\n{exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
