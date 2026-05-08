from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_binding.history_binding_models import (
    HistoryBindingProjection,
    HistoryBindingSummary,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_context_reader import (
    build_jarvis_history_context,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_models import (
    MemoryObject,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.panel_projection_builder import (
    build_panel_projection,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_builders import (
    build_memory_relations,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_node_builder import (
    build_default_storage_nodes,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.timeline_builder import (
    build_timeline_entry,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.traceability_summary_builder import (
    build_traceability_projection,
)


def build_history_binding_projection(
    memory_object: MemoryObject | None = None,
) -> HistoryBindingProjection:
    """Build a read-only binding projection over accepted history_ingestion models."""

    selected_memory_object = memory_object or build_minimal_memory_object()

    storage_nodes = build_default_storage_nodes()
    relations = build_memory_relations(selected_memory_object)
    timeline_entry = build_timeline_entry(selected_memory_object)
    panel_projection = build_panel_projection(selected_memory_object)
    traceability_projection = build_traceability_projection(selected_memory_object)
    jarvis_history_read_model = build_jarvis_history_context()

    dashboard_ready = (
        panel_projection.panel_ready
        and timeline_entry.timeline_ready
        and traceability_projection.traceability_ready
        and all(node.dashboard_ready for node in storage_nodes)
    )

    readable_by_jarvis = (
        jarvis_history_read_model.readable_by_jarvis
        and jarvis_history_read_model.context_ready
    )

    return HistoryBindingProjection(
        source_layer="history_ingestion",
        memory_object=selected_memory_object,
        storage_nodes=storage_nodes,
        relations=relations,
        timeline_entry=timeline_entry,
        panel_projection=panel_projection,
        traceability_projection=traceability_projection,
        jarvis_history_read_model=jarvis_history_read_model,
        registry_ready=True,
        dashboard_ready=dashboard_ready,
        readable_by_jarvis=readable_by_jarvis,
    )


def build_history_binding_summary(
    projection: HistoryBindingProjection | None = None,
) -> HistoryBindingSummary:
    """Build a compact summary from a history binding projection."""

    selected_projection = projection or build_history_binding_projection()

    return HistoryBindingSummary(
        source_layer=selected_projection.source_layer,
        memory_id=selected_projection.memory_object.memory_id,
        title=selected_projection.memory_object.title,
        storage_node_count=len(selected_projection.storage_nodes),
        relation_count=len(selected_projection.relations),
        registry_ready=selected_projection.registry_ready,
        dashboard_ready=selected_projection.dashboard_ready,
        readable_by_jarvis=selected_projection.readable_by_jarvis,
    )
