from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.memory_engine.foundation_inspector.models import (
    MemoryFoundationInspectorReadModel,
)


@dataclass(frozen=True, slots=True)
class MemoryFoundationInspectorObservabilityView:
    """Read-only observability wrapper for the memory foundation inspector."""

    read_model: MemoryFoundationInspectorReadModel

    def __post_init__(self) -> None:
        if self.read_model.alert is None and self.read_model.heartbeat.status == "missing":
            raise ValueError(
                "missing heartbeat must produce an alert in observability view"
            )
