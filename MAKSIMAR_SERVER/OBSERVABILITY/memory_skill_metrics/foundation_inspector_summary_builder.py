from __future__ import annotations

from .foundation_inspector_read_model import MemoryFoundationInspectorObservabilityView


def build_memory_foundation_inspector_summary(
    view: MemoryFoundationInspectorObservabilityView,
) -> str:
    """Build a compact summary string for observability/preview surfaces."""

    heartbeat = view.read_model.heartbeat
    alert = view.read_model.alert

    parts = [
        f"heartbeat={heartbeat.status}",
        f"memory_engine_alive={view.read_model.memory_engine_alive}",
        f"memory_registry_alive={view.read_model.memory_registry_alive}",
        f"retrieval_path_ready={view.read_model.retrieval_path_ready}",
    ]

    if alert is not None:
        parts.append(f"alert={alert.code}")

    if view.read_model.preview is not None:
        parts.append(f"preview={view.read_model.preview.memory_id}")

    return " | ".join(parts)
