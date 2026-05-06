from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.prelive_import_gate_builder import (
    build_prelive_import_gate_state,
)


def test_prelive_import_gate_builder_smoke() -> None:
    state = build_prelive_import_gate_state()
    assert state.prelive_gate_ready is True
