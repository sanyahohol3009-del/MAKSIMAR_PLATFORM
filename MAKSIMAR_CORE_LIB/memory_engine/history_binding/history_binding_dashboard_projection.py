from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_binding.history_binding_builders import (
    build_history_binding_projection,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_binding.history_binding_models import (
    HistoryBindingProjection,
)


def build_history_binding_dashboard_projection(
    projection: HistoryBindingProjection | None = None,
) -> Dict[str, object]:
    """Build a dashboard-facing read-only projection candidate."""

    selected_projection = projection or build_history_binding_projection()
    panel = selected_projection.panel_projection
    timeline = selected_projection.timeline_entry

    return {
        "memory_id": panel.memory_id,
        "title": panel.title,
        "status": panel.status,
        "truth_level": panel.truth_level,
        "project_area": panel.project_area,
        "affected_files": panel.affected_files,
        "timeline_id": timeline.timeline_id,
        "timeline_ready": timeline.timeline_ready,
        "panel_ready": panel.panel_ready,
        "dashboard_ready": selected_projection.dashboard_ready,
    }
