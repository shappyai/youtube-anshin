"""Small, append-safe production metrics store for Phase 2 episodes."""
from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_or_create(path: Path, episode_id: str, gpt_image_count: int = 0) -> dict[str, Any]:
    value: dict[str, Any] = {}
    if path.exists():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                value = loaded
        except (OSError, json.JSONDecodeError):
            value = {}
    value.setdefault("episode_id", episode_id)
    value.setdefault("start_time", now_iso())
    value.setdefault("phase_a_completed", None)
    value.setdefault("gpt_image_count", gpt_image_count)
    value.setdefault("pronunciation_review_count", None)
    value.setdefault("draft_v1_completed", None)
    value.setdefault("draft_versions", [])
    value.setdefault("human_correction_count", None)
    value.setdefault("final_version", None)
    value.setdefault("finalize_time", None)
    # Optional orchestration metrics. Keep them append-safe for existing files.
    value.setdefault("subagent_count", None)
    value.setdefault("parallel_task_groups", None)
    value.setdefault("image_generation_agents", None)
    value.setdefault("image_generation_parallel_batches", None)
    value.setdefault("image_generation_calls", None)
    value.setdefault("image_regeneration_calls", None)
    value.setdefault("image_generation_elapsed_seconds", None)
    value.setdefault("human_gate_count", None)
    value.setdefault("human_correction_rounds", None)
    value.setdefault("phase_a_minutes", None)
    value.setdefault("phase_b_minutes", None)
    value.setdefault("finalization_minutes", None)
    value.setdefault("total_production_minutes", None)
    return value


def save(path: Path, metrics: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
