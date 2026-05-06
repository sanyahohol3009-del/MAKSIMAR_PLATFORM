from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.prelive_import_gate_models import (
    PreLiveImportGateState,
)


def validate_prelive_import_gate_ready(
    state: PreLiveImportGateState,
) -> None:
    if not state.prelive_gate_ready:
        raise ValueError("Pre-live import gate must be ready")
