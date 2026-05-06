from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_boundary_models import (
    HistoryBoundaryContract,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_scope_models import (
    HistoryIngestionTrackFreeze,
)


def validate_history_track_freeze(
    freeze: HistoryIngestionTrackFreeze,
) -> None:
    if not freeze.freeze_confirmed:
        raise ValueError("History ingestion track freeze is not confirmed")


def validate_history_boundary_contract(
    boundary: HistoryBoundaryContract,
) -> None:
    if not boundary.preview_ready:
        raise ValueError("History boundary contract is not preview-ready")
