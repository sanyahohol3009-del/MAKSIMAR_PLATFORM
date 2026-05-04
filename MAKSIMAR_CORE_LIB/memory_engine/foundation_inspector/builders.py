from __future__ import annotations

from typing import Any

from .models import (
    MemoryFoundationInspectorReadModel,
    MemoryHeartbeatSnapshot,
    MemoryInspectorAlert,
    MemoryObjectPreview,
)


def build_memory_heartbeat_snapshot(
    *,
    source_name: str,
    payload: dict[str, Any] | None,
    age_seconds: float | None,
) -> MemoryHeartbeatSnapshot:
    """Build a canonical memory heartbeat snapshot from validated raw input."""

    if payload is None:
        return MemoryHeartbeatSnapshot(
            source_name=source_name,
            status="missing",
            age_seconds=None,
            timestamp_wall=None,
            timestamp_monotonic=None,
            pid=None,
        )

    status = "fresh"
    if age_seconds is not None and age_seconds > 5.0:
        status = "stale"

    return MemoryHeartbeatSnapshot(
        source_name=source_name,
        status=status,
        age_seconds=age_seconds,
        timestamp_wall=payload["timestamp_wall"],
        timestamp_monotonic=float(payload["timestamp_monotonic"]),
        pid=int(payload["pid"]),
    )


def build_memory_foundation_inspector_read_model(
    *,
    heartbeat: MemoryHeartbeatSnapshot,
    memory_engine_alive: bool,
    memory_registry_alive: bool,
    retrieval_path_ready: bool,
    preview: MemoryObjectPreview | None,
) -> MemoryFoundationInspectorReadModel:
    """Build the read-only memory foundation inspector model."""

    alert: MemoryInspectorAlert | None = None

    if heartbeat.status == "missing":
        alert = MemoryInspectorAlert(
            severity="critical",
            code="memory_heartbeat_missing",
            summary="Memory heartbeat artifact is missing.",
        )
    elif heartbeat.status == "stale":
        alert = MemoryInspectorAlert(
            severity="warning",
            code="memory_heartbeat_stale",
            summary="Memory heartbeat artifact is stale.",
            details=f"age_seconds={heartbeat.age_seconds}",
        )
    elif not memory_engine_alive:
        alert = MemoryInspectorAlert(
            severity="critical",
            code="memory_engine_not_alive",
            summary="Memory engine is not alive.",
        )
    elif not memory_registry_alive:
        alert = MemoryInspectorAlert(
            severity="warning",
            code="memory_registry_not_alive",
            summary="Memory registry is not alive.",
        )
    elif not retrieval_path_ready:
        alert = MemoryInspectorAlert(
            severity="warning",
            code="memory_retrieval_path_not_ready",
            summary="Memory retrieval path is not ready.",
        )

    return MemoryFoundationInspectorReadModel(
        heartbeat=heartbeat,
        memory_engine_alive=memory_engine_alive,
        memory_registry_alive=memory_registry_alive,
        retrieval_path_ready=retrieval_path_ready,
        preview=preview,
        alert=alert,
    )
