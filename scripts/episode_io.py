"""Shared helpers for the episode.json production tools.

The project intentionally keeps these helpers dependency-light.  The bundled
runtime may not have PyYAML or jsonschema available, so validation and the
small pronunciation YAML reader have standard-library fallbacks.
"""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "templates" / "episode.schema.json"
PRONUNCIATION_PATH = ROOT / "config" / "voicevox_pronunciation.yaml"

DEFAULT_SCENE_VALUES: dict[str, Any] = {
    "render_mode": "template",
    "text_render_mode": "imagegen_native",
    "fit_mode": "full_bleed",
    "background_fill": "none",
    "animation": "static",
}

# text_render_mode の正規値。codex / image は過去Episode用の後方互換別名
# （codex = pil_overlay、image = imagegen_native）。
TEXT_RENDER_MODES: frozenset[str] = frozenset({
    "imagegen_native",
    "pil_overlay",
    "no_text",
    "codex",
    "image",
})

# 新規sceneのdefault。既存Episodeは明示値を持つため再解釈されない。
DEFAULT_TEXT_RENDER_MODE = "imagegen_native"
GENERATED_IMAGE_RENDER_MODES: frozenset[str] = frozenset({"gpt_image", "hybrid"})


def canonical_text_render_mode(scene: dict[str, Any]) -> str:
    """Return the canonical text_render_mode for a scene.

    Legacy aliases are mapped for backward compatibility: ``codex`` is the
    old name of ``pil_overlay`` and ``image`` the old name of
    ``imagegen_native``.  Unspecified scenes use the new-scene default
    ``imagegen_native``.
    """
    value = scene.get("text_render_mode") or DEFAULT_TEXT_RENDER_MODE
    if value == "codex":
        return "pil_overlay"
    if value == "image":
        return "imagegen_native"
    return str(value)


def canonical_visual_mode(scene: dict[str, Any]) -> str:
    """Return the exclusive major visual mode for a scene.

    Generated-image scenes may carry their own ImageGen-native text or no
    image text. Deterministic text overlay is reserved for renderer-native
    scenes (template/official). This keeps a generated photograph/background
    from being paired with a large post-render headline.
    """
    render_mode = str(scene.get("render_mode") or "template")
    text_mode = canonical_text_render_mode(scene)
    if render_mode in GENERATED_IMAGE_RENDER_MODES:
        if text_mode == "pil_overlay":
            return "invalid_generated_image_text_overlay"
        return "imagegen_native"
    return "renderer_native"


def apply_episode_defaults(data: dict[str, Any]) -> dict[str, Any]:
    """Return a build-time copy with safe Phase 2 scene defaults applied.

    Defaults are deliberately applied to a copy: episode.json remains the
    human-authored source of truth and is never rewritten by the builder.
    """
    result = copy.deepcopy(data)
    scenes = result.get("scenes")
    if isinstance(scenes, list):
        for scene in scenes:
            if not isinstance(scene, dict):
                continue
            for key, value in DEFAULT_SCENE_VALUES.items():
                scene.setdefault(key, value)
    postroll = result.get("postroll")
    if isinstance(postroll, dict):
        postroll.setdefault("kind", "channel_cta")
        postroll.setdefault("animation", "static")
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"episode.json not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"episode.json root must be an object: {path}")
    return value


def episode_dir_from_path(path: Path) -> Path:
    return path.parent.resolve()


def resolve_repo_path(value: str | Path, episode_dir: Path | None = None) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    if episode_dir is not None:
        candidate = (episode_dir / path).resolve()
        if candidate.exists():
            return candidate
    return (ROOT / path).resolve()


def segment_spoken_text(segment: dict[str, Any]) -> str:
    """Return the text intended for VOICEVOX synthesis.

    ``narration`` remains the historical required field.  Newer manifests may
    provide ``spoken_text`` explicitly when the visible display text must stay
    in an official format such as a telephone number.
    """
    explicit = segment.get("spoken_text")
    if isinstance(explicit, str) and explicit.strip():
        return explicit
    return str(segment.get("narration") or "")


def segment_display_text(segment: dict[str, Any]) -> str:
    """Return the optional canonical text expected in the visible subtitles."""
    value = segment.get("display_text")
    return str(value) if isinstance(value, str) else ""


def _is_uri(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _require_object(parent: dict[str, Any], key: str, issues: list[str]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        issues.append(f"{key}: object is required")
        return {}
    return value


def _require_array(parent: dict[str, Any], key: str, issues: list[str]) -> list[Any]:
    value = parent.get(key)
    if not isinstance(value, list):
        issues.append(f"{key}: array is required")
        return []
    return value


def _require_nonempty_string(parent: dict[str, Any], key: str, prefix: str, issues: list[str]) -> None:
    value = parent.get(key)
    if not isinstance(value, str) or not value.strip():
        issues.append(f"{prefix}.{key}: non-empty string is required")


def validate_episode(data: dict[str, Any]) -> list[str]:
    """Return human-readable schema issues without requiring jsonschema."""
    issues: list[str] = []
    for key in ("schema_version", "episode", "sources", "narration_segments", "subtitles", "scenes", "publish"):
        if key not in data:
            issues.append(f"{key}: required")

    if "schema_version" in data and (
        not isinstance(data["schema_version"], str)
        or not re.fullmatch(r"\d+\.\d+\.\d+", data["schema_version"])
    ):
        issues.append("schema_version: expected semantic version such as 1.0.0")

    episode = _require_object(data, "episode", issues)
    for key in ("episode_id", "slug", "title", "topic", "target_audience"):
        _require_nonempty_string(episode, key, "episode", issues)
    if not re.fullmatch(r"\d{3}", str(episode.get("episode_id", ""))):
        issues.append("episode.episode_id: expected three digits")
    if not isinstance(episode.get("target_duration"), (int, float)) or episode.get("target_duration", 0) <= 0:
        issues.append("episode.target_duration: positive number is required")
    allowed_status = {"draft", "in_review", "ready_for_production", "publish_ready", "published", "archived"}
    if episode.get("status") not in allowed_status:
        issues.append(f"episode.status: expected one of {sorted(allowed_status)}")

    sources = _require_array(data, "sources", issues)
    source_ids: set[str] = set()
    for index, source in enumerate(sources, 1):
        prefix = f"sources[{index}]"
        if not isinstance(source, dict):
            issues.append(f"{prefix}: object is required")
            continue
        for key in ("source_id", "url", "title", "organization", "verified_at", "claim"):
            _require_nonempty_string(source, key, prefix, issues)
        source_id = source.get("source_id")
        if source_id in source_ids:
            issues.append(f"{prefix}.source_id: duplicate {source_id}")
        source_ids.add(str(source_id))
        if not _is_uri(source.get("url")):
            issues.append(f"{prefix}.url: http(s) URL is required")

    subtitles = _require_array(data, "subtitles", issues)
    subtitle_ids: set[str] = set()
    valid_segment_ids: set[int] = set()
    segments = _require_array(data, "narration_segments", issues)
    for index, segment in enumerate(segments, 1):
        prefix = f"narration_segments[{index}]"
        if not isinstance(segment, dict):
            issues.append(f"{prefix}: object is required")
            continue
        for key in ("id", "section", "narration", "reading_overrides", "pause_after", "scene_id", "subtitle_ids"):
            if key not in segment:
                issues.append(f"{prefix}.{key}: required")
        segment_id = segment.get("id")
        if not isinstance(segment_id, int) or segment_id < 1:
            issues.append(f"{prefix}.id: positive integer is required")
        else:
            valid_segment_ids.add(segment_id)
        _require_nonempty_string(segment, "section", prefix, issues)
        _require_nonempty_string(segment, "narration", prefix, issues)
        if not isinstance(segment.get("reading_overrides"), dict):
            issues.append(f"{prefix}.reading_overrides: object is required")
        if "spoken_text" in segment and (
            not isinstance(segment.get("spoken_text"), str)
            or not str(segment.get("spoken_text") or "").strip()
        ):
            issues.append(f"{prefix}.spoken_text: non-empty string is required when specified")
        if "display_text" in segment and not isinstance(segment.get("display_text"), str):
            issues.append(f"{prefix}.display_text: string is required when specified")
        accent_overrides = segment.get("accent_overrides")
        if accent_overrides is not None:
            if not isinstance(accent_overrides, dict):
                issues.append(f"{prefix}.accent_overrides: object is required when specified")
            else:
                for surface, spec in accent_overrides.items():
                    if not isinstance(surface, str) or not surface.strip():
                        issues.append(f"{prefix}.accent_overrides: surface must be a non-empty string")
                        continue
                    if not isinstance(spec, dict):
                        issues.append(f"{prefix}.accent_overrides.{surface}: object is required")
                        continue
                    if not str(spec.get("reading") or "").strip():
                        issues.append(f"{prefix}.accent_overrides.{surface}.reading: non-empty string is required")
                    accent = spec.get("accent")
                    if not isinstance(accent, int) or accent < 1:
                        issues.append(f"{prefix}.accent_overrides.{surface}.accent: positive integer is required")
        if not isinstance(segment.get("pause_after"), (int, float)) or segment.get("pause_after", -1) < 0:
            issues.append(f"{prefix}.pause_after: non-negative number is required")
        if segment.get("scene_id") is not None and not isinstance(segment.get("scene_id"), int):
            issues.append(f"{prefix}.scene_id: integer or null is required")
        if not isinstance(segment.get("subtitle_ids"), list):
            issues.append(f"{prefix}.subtitle_ids: array is required")

    for index, subtitle in enumerate(subtitles, 1):
        prefix = f"subtitles[{index}]"
        if not isinstance(subtitle, dict):
            issues.append(f"{prefix}: object is required")
            continue
        for key in ("id", "text_lines", "segment_id"):
            if key not in subtitle:
                issues.append(f"{prefix}.{key}: required")
        subtitle_id = subtitle.get("id")
        if subtitle_id in subtitle_ids:
            issues.append(f"{prefix}.id: duplicate {subtitle_id}")
        subtitle_ids.add(str(subtitle_id))
        lines = subtitle.get("text_lines")
        if not isinstance(lines, list) or not 1 <= len(lines) <= 2 or any(
            not isinstance(line, str) or not line.strip() for line in lines
        ):
            issues.append(f"{prefix}.text_lines: one or two non-empty strings are required")
        if subtitle.get("segment_id") not in valid_segment_ids:
            issues.append(f"{prefix}.segment_id: does not reference a narration segment")

    scenes = _require_array(data, "scenes", issues)
    scene_ids: set[int] = set()
    for index, scene in enumerate(scenes, 1):
        prefix = f"scenes[{index}]"
        if not isinstance(scene, dict):
            issues.append(f"{prefix}: object is required")
            continue
        for key in (
            "id",
            "layout",
            "main_message",
            "headline",
            "support_text",
            "official_asset",
            "official_asset_crop",
            "start_segment",
            "end_segment",
        ):
            if key not in scene:
                issues.append(f"{prefix}.{key}: required")
        scene_id = scene.get("id")
        if not isinstance(scene_id, int) or scene_id < 1:
            issues.append(f"{prefix}.id: positive integer is required")
        elif scene_id in scene_ids:
            issues.append(f"{prefix}.id: duplicate {scene_id}")
        else:
            scene_ids.add(scene_id)
        for key in ("layout", "main_message", "headline", "support_text"):
            _require_nonempty_string(scene, key, prefix, issues)
        if "animation" in scene:
            _require_nonempty_string(scene, "animation", prefix, issues)
        render_mode = scene.get("render_mode", "template")
        if render_mode not in {"template", "gpt_image", "official", "hybrid"}:
            issues.append(f"{prefix}.render_mode: template/gpt_image/official/hybrid expected")
        text_render_mode = scene.get("text_render_mode", DEFAULT_TEXT_RENDER_MODE)
        if text_render_mode not in TEXT_RENDER_MODES:
            issues.append(
                f"{prefix}.text_render_mode: imagegen_native/pil_overlay/no_text "
                "(or legacy codex/image) expected"
            )
        if canonical_visual_mode(scene) == "invalid_generated_image_text_overlay":
            issues.append(
                f"{prefix}: NO_IMAGE_TEXT_HYBRID / visual_mode_exclusive requires "
                "imagegen_native or no_text for generated-image scenes; "
                "large pil_overlay text is prohibited"
            )
        fit_mode = scene.get("fit_mode", "full_bleed")
        if fit_mode not in {"full_bleed", "crop", "cover_blur"}:
            issues.append(f"{prefix}.fit_mode: full_bleed/crop/cover_blur expected")
        background_fill = scene.get("background_fill", "none")
        if background_fill not in {"none", "soft_gradient", "cover_blur"}:
            issues.append(f"{prefix}.background_fill: none/soft_gradient/cover_blur expected")
        center_x = scene.get("visual_balance_center_x")
        if center_x is not None and (
            not isinstance(center_x, (int, float)) or not 0 <= float(center_x) <= 1920
        ):
            issues.append(f"{prefix}.visual_balance_center_x: number between 0 and 1920 expected")
        visual_balance = scene.get("visual_balance")
        if visual_balance is not None and not isinstance(visual_balance, dict):
            issues.append(f"{prefix}.visual_balance: object is required when specified")
        elif isinstance(visual_balance, dict):
            declared_center = visual_balance.get("center_x")
            if declared_center is not None and (
                not isinstance(declared_center, (int, float)) or not 0 <= float(declared_center) <= 1920
            ):
                issues.append(f"{prefix}.visual_balance.center_x: number between 0 and 1920 expected")
        if "animation_reason" in scene and not isinstance(scene.get("animation_reason"), str):
            issues.append(f"{prefix}.animation_reason: string is required when specified")
        if not isinstance(scene.get("official_asset"), list):
            issues.append(f"{prefix}.official_asset: array is required")
        if not isinstance(scene.get("official_asset_crop"), list):
            issues.append(f"{prefix}.official_asset_crop: array is required")
        if not isinstance(scene.get("start_segment"), int) or not isinstance(scene.get("end_segment"), int):
            issues.append(f"{prefix}: start_segment/end_segment must be integers")
        elif scene["start_segment"] > scene["end_segment"]:
            issues.append(f"{prefix}: start_segment must not exceed end_segment")

    if "postroll" in data:
        postroll = data.get("postroll")
        if not isinstance(postroll, dict):
            issues.append("postroll: object is required when specified")
        else:
            if "asset" in postroll and not isinstance(postroll.get("asset"), str):
                issues.append("postroll.asset: string is required when specified")
            duration = postroll.get("duration_sec", 0)
            if not isinstance(duration, (int, float)) or duration < 0:
                issues.append("postroll.duration_sec: non-negative number is required")
            if "animation" in postroll and not isinstance(postroll.get("animation"), str):
                issues.append("postroll.animation: string is required when specified")
            profile = postroll.get("cta_profile")
            if profile is not None and profile not in {"channel_common_cta"}:
                issues.append("postroll.cta_profile: unsupported CTA profile")

    publish = _require_object(data, "publish", issues)
    for key in ("title", "description", "chapters", "voice_credit"):
        if key not in publish:
            issues.append(f"publish.{key}: required")
    _require_nonempty_string(publish, "title", "publish", issues)
    if not isinstance(publish.get("description"), str):
        issues.append("publish.description: string is required")
    if not isinstance(publish.get("chapters"), list) or any(
        not isinstance(chapter, str) or not chapter.strip() for chapter in publish.get("chapters", [])
    ):
        issues.append("publish.chapters: array of strings is required")
    _require_nonempty_string(publish, "voice_credit", "publish", issues)
    return issues


def _yaml_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value.startswith('"') and value.endswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    if value.lower() in {"null", "~"}:
        return None
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def load_pronunciation_entries(path: Path = PRONUNCIATION_PATH) -> list[dict[str, Any]]:
    """Read the project's deliberately small pronunciation YAML format.

    PyYAML is used when present; the fallback handles the flat fields used by
    config/voicevox_pronunciation.yaml and never writes the dictionary.
    """
    if not path.exists():
        return []
    try:
        import yaml  # type: ignore
    except ImportError:
        yaml = None
    if yaml is not None:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        entries = loaded.get("pronunciations") or []
        return [dict(entry) for entry in entries if isinstance(entry, dict)]

    entries: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("- surface:"):
            if current:
                entries.append(current)
            current = {"surface": _yaml_scalar(line.split(":", 1)[1])}
            continue
        if current is None or not line or line.startswith("#") or line.startswith("- "):
            continue
        match = re.match(r"([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if match:
            key, value = match.groups()
            current[key] = _yaml_scalar(value)
    if current:
        entries.append(current)
    return entries


def replace_readings(text: str, replacements: dict[str, str]) -> str:
    result = text
    for surface in sorted(replacements, key=len, reverse=True):
        result = result.replace(surface, replacements[surface])
    return result


CONTEXT_DEPENDENT_TERMS: tuple[tuple[str, str], ...] = (
    ("方", r"(?<!方)方(?!法)"),
    ("後から", r"後から"),
    ("開けない", r"開けない"),
    ("開きます", r"開きます"),
    ("開く/開ける", r"開く|開ける|開いて|開かなく|開け直す"),
    ("生", r"生(?!活|まれ|き)"),
    ("上", r"(?<!以)上(?!記|位|が|り)"),
    ("下", r"(?<!左)(?<!右)下(?!記|げ)"),
    ("入る", r"入る"),
    ("行う", r"行う"),
    ("今日", r"今日"),
    ("明日", r"明日"),
    ("空く", r"空く(?![き])"),
)


def find_context_terms(text: str) -> list[str]:
    found: list[str] = []
    for label, pattern in CONTEXT_DEPENDENT_TERMS:
        if re.search(pattern, text) and label not in found:
            found.append(label)
    return found


def dictionary_matches(text: str, entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [entry for entry in entries if entry.get("surface") and str(entry["surface"]) in text]


def asset_path_from_item(item: dict[str, Any], episode_dir: Path) -> Path | None:
    path = item.get("path")
    if not isinstance(path, str) or not path:
        return None
    return resolve_repo_path(path, episode_dir)
