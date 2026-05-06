from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_completion_builder import (
    build_history_completion_state,
)


def test_full_history_import_ready_smoke() -> None:
    state = build_history_completion_state()
    assert state.full_history_import_ready is True
