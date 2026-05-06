from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.prelive_import_gate_models import (
    PreLiveImportGateState,
)


def test_prelive_import_gate_models_smoke() -> None:
    state = PreLiveImportGateState(
        live_import_eligibility_ready=True,
        live_source_acceptance_ready=True,
        live_dedup_before_write_ready=True,
        live_target_readiness_ready=True,
        live_rollback_safe_session_ready=True,
        live_noncanonical_only_ready=True,
        prelive_gate_ready=True,
    )
    assert state.prelive_gate_ready is True
