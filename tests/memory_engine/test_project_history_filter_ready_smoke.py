from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_completion_builder import (
    build_history_completion_state,
)


def test_project_history_filter_ready_smoke() -> None:
    state = build_history_completion_state()
    assert state.project_history_filter_ready is True
