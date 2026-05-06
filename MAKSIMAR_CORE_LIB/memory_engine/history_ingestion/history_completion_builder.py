from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.dedup_builders import (
    build_incremental_import_preview,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_completion_models import (
    HistoryCompletionState,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_completion_validators import (
    validate_history_completion_ready,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_summary_builder import (
    build_jarvis_history_summary,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.panel_projection_builder import (
    build_panel_projection_preview,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.filter_projection_builder import (
    build_filter_projection_preview,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_builders import (
    build_relation_preview,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)


def _compute_full_history_import_ready() -> bool:
    source = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/history_readiness_source.txt",
        text_payload="history readiness proof",
        binary_available=False,
    )
    preview = build_incremental_import_preview(
        source=source,
        existing_file_hashes=[],
        existing_content_hashes=[],
        existing_unit_hashes=[],
    )
    return bool(preview["incremental_import_ready"] and preview["write_required"])


def _compute_project_history_graph_ready() -> bool:
    preview = build_relation_preview(build_minimal_memory_object())
    return bool(
        preview["graph_ready"]
        and preview["timeline_ready"]
        and preview["relation_count"] >= 1
    )


def _compute_project_history_panel_ready() -> bool:
    preview = build_panel_projection_preview(build_minimal_memory_object())
    return bool(
        preview["panel_ready"]
        and preview["affected_files_count"] >= 1
        and preview["project_area_count"] >= 1
    )


def _compute_project_history_filter_ready() -> bool:
    preview = build_filter_projection_preview(build_minimal_memory_object())
    return bool(
        preview["filter_ready"]
        and preview["tag_count"] >= 1
        and preview["project_area_count"] >= 1
    )


def _compute_project_history_readable_by_jarvis() -> bool:
    summary = build_jarvis_history_summary()
    return bool(
        summary["readable_by_jarvis"]
        and summary["context_ready"]
        and summary["memory_count"] >= 1
    )


def _compute_incremental_reimport_safe() -> bool:
    source = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/history_reimport_source.txt",
        text_payload="history reimport proof",
        binary_available=False,
    )
    preview = build_incremental_import_preview(
        source=source,
        existing_file_hashes=[],
        existing_content_hashes=[],
        existing_unit_hashes=[],
    )
    return bool(
        preview["incremental_import_ready"]
        and preview["new_unit_count"] >= 1
        and preview["duplicate_unit_count"] == 0
    )


def build_history_completion_state() -> HistoryCompletionState:
    full_history_import_ready = _compute_full_history_import_ready()
    project_history_graph_ready = _compute_project_history_graph_ready()
    project_history_panel_ready = _compute_project_history_panel_ready()
    project_history_filter_ready = _compute_project_history_filter_ready()
    project_history_readable_by_jarvis = _compute_project_history_readable_by_jarvis()
    incremental_reimport_safe = _compute_incremental_reimport_safe()

    completion_ready = all(
        (
            full_history_import_ready,
            project_history_graph_ready,
            project_history_panel_ready,
            project_history_filter_ready,
            project_history_readable_by_jarvis,
            incremental_reimport_safe,
        )
    )

    state = HistoryCompletionState(
        full_history_import_ready=full_history_import_ready,
        project_history_graph_ready=project_history_graph_ready,
        project_history_panel_ready=project_history_panel_ready,
        project_history_filter_ready=project_history_filter_ready,
        project_history_readable_by_jarvis=project_history_readable_by_jarvis,
        incremental_reimport_safe=incremental_reimport_safe,
        completion_ready=completion_ready,
    )
    validate_history_completion_ready(state)
    return state


def build_history_completion_preview() -> Dict[str, object]:
    state = build_history_completion_state()
    return {
        "full_history_import_ready": state.full_history_import_ready,
        "project_history_graph_ready": state.project_history_graph_ready,
        "project_history_panel_ready": state.project_history_panel_ready,
        "project_history_filter_ready": state.project_history_filter_ready,
        "project_history_readable_by_jarvis": state.project_history_readable_by_jarvis,
        "incremental_reimport_safe": state.incremental_reimport_safe,
        "completion_ready": state.completion_ready,
    }
