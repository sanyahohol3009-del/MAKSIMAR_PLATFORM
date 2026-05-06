from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.prelive_import_gate_builder import (
    build_prelive_import_gate_state,
)


def build_prelive_import_gate_summary() -> Dict[str, object]:
    state = build_prelive_import_gate_state()
    return {
        "live_import_eligibility_ready": state.live_import_eligibility_ready,
        "live_source_acceptance_ready": state.live_source_acceptance_ready,
        "live_dedup_before_write_ready": state.live_dedup_before_write_ready,
        "live_target_readiness_ready": state.live_target_readiness_ready,
        "live_rollback_safe_session_ready": state.live_rollback_safe_session_ready,
        "live_noncanonical_only_ready": state.live_noncanonical_only_ready,
        "prelive_gate_ready": state.prelive_gate_ready,
        "gate_kind": "pre_live_import_gate",
    }
