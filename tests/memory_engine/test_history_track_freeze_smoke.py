from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_ingestion_builders import (
    build_default_history_track_freeze,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_scope_models import (
    HistoryIngestionTrackFreeze,
)


def test_history_track_freeze_smoke() -> None:
    freeze = build_default_history_track_freeze()

    assert freeze.freeze_phase_id == "PHASE-H0"
    assert freeze.freeze_confirmed is True
    assert freeze.duplicate_memory_world_allowed is False
    assert freeze.archive_equals_canonical_truth is False
    assert freeze.scope.supporting_source_only is True
    assert freeze.scope.canonical_truth_write_allowed is False
    assert freeze.scope.real_data_import_allowed is False


def test_history_track_freeze_rejects_duplicate_memory_world() -> None:
    scope = build_default_history_track_freeze().scope

    with pytest.raises(ValueError, match="duplicate_memory_world_allowed must remain False"):
        HistoryIngestionTrackFreeze(
            scope=scope,
            freeze_phase_id="PHASE-H0",
            freeze_reason="bad",
            duplicate_memory_world_allowed=True,
            archive_equals_canonical_truth=False,
        )


def test_history_track_freeze_rejects_archive_as_canonical_truth() -> None:
    scope = build_default_history_track_freeze().scope

    with pytest.raises(ValueError, match="archive_equals_canonical_truth must remain False"):
        HistoryIngestionTrackFreeze(
            scope=scope,
            freeze_phase_id="PHASE-H0",
            freeze_reason="bad",
            duplicate_memory_world_allowed=False,
            archive_equals_canonical_truth=True,
        )
