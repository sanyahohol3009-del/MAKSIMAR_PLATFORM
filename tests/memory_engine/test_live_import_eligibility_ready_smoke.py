from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.prelive_import_gate_builder import (
    build_prelive_import_gate_state,
)


def test_live_import_eligibility_ready_smoke() -> None:
    state = build_prelive_import_gate_state()
    assert state.live_import_eligibility_ready is True
