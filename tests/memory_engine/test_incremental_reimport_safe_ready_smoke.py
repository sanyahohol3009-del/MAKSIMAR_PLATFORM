from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_completion_builder import (
    build_history_completion_state,
)


def test_incremental_reimport_safe_ready_smoke() -> None:
    state = build_history_completion_state()
    assert state.incremental_reimport_safe is True
