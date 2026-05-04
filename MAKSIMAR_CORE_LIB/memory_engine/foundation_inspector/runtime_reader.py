from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .builders import (
    build_memory_foundation_inspector_read_model,
    build_memory_heartbeat_snapshot,
)
from .models import MemoryFoundationInspectorReadModel, MemoryObjectPreview
from .validators import (
    validate_memory_heartbeat_payload,
    validate_runtime_state_path,
)


@dataclass(frozen=True, slots=True)
class MemoryRuntimeStatePaths:
    """Filesystem paths required by the memory foundation inspector reader."""

    runtime_state_dir: Path
    heartbeat_file: Path

    def __post_init__(self) -> None:
        if not self.runtime_state_dir.is_absolute():
            raise ValueError("runtime_state_dir must be absolute")
        validate_runtime_state_path(self.heartbeat_file)


def _read_json_file(path: Path) -> dict[str, Any] | None:
    """Read a JSON artifact defensively."""

    if not path.exists():
        return None

    content = path.read_text(encoding="utf-8")
    parsed = json.loads(content)
    if not isinstance(parsed, dict):
        raise ValueError("JSON artifact root must be an object")
    return parsed


def read_memory_foundation_inspector_state(
    *,
    paths: MemoryRuntimeStatePaths,
    memory_engine_alive: bool,
    memory_registry_alive: bool,
    retrieval_path_ready: bool,
    preview: MemoryObjectPreview | None = None,
) -> MemoryFoundationInspectorReadModel:
    """Read runtime state and build the memory foundation inspector read model.

    This reader is intentionally read-only.
    It does not mutate runtime state and does not import control-plane internals.
    """

    payload = _read_json_file(paths.heartbeat_file)
    age_seconds: float | None = None

    if payload is not None:
        validate_memory_heartbeat_payload(payload)
        age_seconds = max(0.0, time.monotonic() - float(payload["timestamp_monotonic"]))

    heartbeat = build_memory_heartbeat_snapshot(
        source_name="memory_engine",
        payload=payload,
        age_seconds=age_seconds,
    )

    return build_memory_foundation_inspector_read_model(
        heartbeat=heartbeat,
        memory_engine_alive=memory_engine_alive,
        memory_registry_alive=memory_registry_alive,
        retrieval_path_ready=retrieval_path_ready,
        preview=preview,
    )
