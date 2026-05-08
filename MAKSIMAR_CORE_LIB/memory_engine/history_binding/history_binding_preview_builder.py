from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_binding.history_binding_builders import (
    build_history_binding_projection,
    build_history_binding_summary,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_binding.history_binding_dashboard_projection import (
    build_history_binding_dashboard_projection,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_binding.history_binding_models import (
    HistoryBindingPreview,
    HistoryBindingProjection,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_binding.history_binding_registry_projection import (
    build_history_binding_registry_projection,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_binding.history_binding_traceability_builder import (
    build_history_binding_traceability_projection,
)


def build_history_binding_preview(
    projection: HistoryBindingProjection | None = None,
) -> HistoryBindingPreview:
    """Build a full read-only preview for PHASE 1 History Binding."""

    selected_projection = projection or build_history_binding_projection()
    summary = build_history_binding_summary(selected_projection)

    status = "ready"
    if not summary.registry_ready or not summary.dashboard_ready:
        status = "blocked"

    return HistoryBindingPreview(
        status=status,
        summary=summary,
        registry_projection=build_history_binding_registry_projection(selected_projection),
        dashboard_projection=build_history_binding_dashboard_projection(selected_projection),
        traceability_projection=build_history_binding_traceability_projection(
            selected_projection
        ),
    )


def build_history_binding_preview_dict(
    projection: HistoryBindingProjection | None = None,
) -> Dict[str, object]:
    """Build a dictionary preview that is easy to render/test."""

    preview = build_history_binding_preview(projection)

    return {
        "status": preview.status,
        "summary": {
            "source_layer": preview.summary.source_layer,
            "memory_id": preview.summary.memory_id,
            "title": preview.summary.title,
            "storage_node_count": preview.summary.storage_node_count,
            "relation_count": preview.summary.relation_count,
            "registry_ready": preview.summary.registry_ready,
            "dashboard_ready": preview.summary.dashboard_ready,
            "readable_by_jarvis": preview.summary.readable_by_jarvis,
        },
        "registry_projection": preview.registry_projection,
        "dashboard_projection": preview.dashboard_projection,
        "traceability_projection": preview.traceability_projection,
    }
