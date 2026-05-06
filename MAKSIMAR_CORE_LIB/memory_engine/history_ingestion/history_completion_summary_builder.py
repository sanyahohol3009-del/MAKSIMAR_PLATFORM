from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_completion_builder import (
    build_history_completion_state,
)


def build_history_completion_summary() -> Dict[str, object]:
    state = build_history_completion_state()
    return {
        "full_history_import_ready": state.full_history_import_ready,
        "project_history_graph_ready": state.project_history_graph_ready,
        "project_history_panel_ready": state.project_history_panel_ready,
        "project_history_filter_ready": state.project_history_filter_ready,
        "project_history_readable_by_jarvis": state.project_history_readable_by_jarvis,
        "incremental_reimport_safe": state.incremental_reimport_safe,
        "completion_ready": state.completion_ready,
        "readiness_source": "derived_from_existing_history_layers",
    }
