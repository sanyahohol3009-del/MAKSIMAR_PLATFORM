from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal, Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_read_models import (
    JarvisHistoryReadModel,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_models import (
    MemoryObject,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.panel_projection_models import (
    PanelProjection,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_models import (
    MemoryRelation,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_node_models import (
    StorageNode,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.timeline_models import (
    TimelineEntry,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.traceability_models import (
    TraceabilityProjection,
)


HistoryBindingStatus = Literal["ready", "blocked"]


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value


@dataclass(frozen=True, slots=True)
class HistoryBindingProjection:
    """Read-only binding over the accepted history_ingestion layer.

    This model intentionally reuses accepted history_ingestion contracts.
    It does not redefine MemoryObject, graph, timeline, storage or panel truth.
    """

    source_layer: str
    memory_object: MemoryObject
    storage_nodes: Tuple[StorageNode, ...]
    relations: Tuple[MemoryRelation, ...]
    timeline_entry: TimelineEntry
    panel_projection: PanelProjection
    traceability_projection: TraceabilityProjection
    jarvis_history_read_model: JarvisHistoryReadModel
    registry_ready: bool
    dashboard_ready: bool
    readable_by_jarvis: bool

    def __post_init__(self) -> None:
        _ensure_non_empty_str(self.source_layer, "source_layer")

        if self.source_layer != "history_ingestion":
            raise ValueError("source_layer must be 'history_ingestion'")

        if not self.storage_nodes:
            raise ValueError("storage_nodes must not be empty")

        memory_id = self.memory_object.memory_id

        if self.timeline_entry.memory_id != memory_id:
            raise ValueError("timeline_entry.memory_id must match memory_object.memory_id")

        if self.panel_projection.memory_id != memory_id:
            raise ValueError("panel_projection.memory_id must match memory_object.memory_id")

        if self.traceability_projection.memory_id != memory_id:
            raise ValueError(
                "traceability_projection.memory_id must match memory_object.memory_id"
            )

        if not self.panel_projection.panel_ready:
            raise ValueError("panel_projection must be panel_ready")

        if not self.timeline_entry.timeline_ready:
            raise ValueError("timeline_entry must be timeline_ready")

        if not self.traceability_projection.traceability_ready:
            raise ValueError("traceability_projection must be traceability_ready")

        if self.readable_by_jarvis and not self.jarvis_history_read_model.readable_by_jarvis:
            raise ValueError("readable_by_jarvis requires jarvis_history_read_model readiness")


@dataclass(frozen=True, slots=True)
class HistoryBindingSummary:
    """Compact summary for registry/dashboard/preview consumers."""

    source_layer: str
    memory_id: str
    title: str
    storage_node_count: int
    relation_count: int
    registry_ready: bool
    dashboard_ready: bool
    readable_by_jarvis: bool

    def __post_init__(self) -> None:
        _ensure_non_empty_str(self.source_layer, "source_layer")
        _ensure_non_empty_str(self.memory_id, "memory_id")
        _ensure_non_empty_str(self.title, "title")

        if self.storage_node_count < 1:
            raise ValueError("storage_node_count must be >= 1")

        if self.relation_count < 0:
            raise ValueError("relation_count must be >= 0")


@dataclass(frozen=True, slots=True)
class HistoryBindingPreview:
    """Dictionary-ready preview for read-only dashboard/testing surfaces."""

    status: HistoryBindingStatus
    summary: HistoryBindingSummary
    registry_projection: Dict[str, object]
    dashboard_projection: Dict[str, object]
    traceability_projection: Dict[str, object]

    def __post_init__(self) -> None:
        if self.status == "ready" and not self.summary.registry_ready:
            raise ValueError("ready preview requires registry_ready summary")

        if self.status == "ready" and not self.summary.dashboard_ready:
            raise ValueError("ready preview requires dashboard_ready summary")
