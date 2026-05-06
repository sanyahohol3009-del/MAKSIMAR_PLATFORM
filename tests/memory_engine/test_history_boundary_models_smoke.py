from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_boundary_models import (
    HistoryBoundaryContract,
    HistoryCanonicalTruthSplit,
    HistoryStoragePortabilityRequirement,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_ingestion_builders import (
    build_default_history_boundary_contract,
)


def test_history_boundary_models_smoke() -> None:
    boundary = build_default_history_boundary_contract()

    assert boundary.boundary_id == "HBOUNDARY-0001"
    assert boundary.owning_package == "MAKSIMAR_CORE_LIB/memory_engine/history_ingestion"
    assert boundary.truth_split.archive_is_supporting_source is True
    assert boundary.truth_split.canonical_truth_write_allowed is False
    assert boundary.truth_split.auto_promotion_allowed is False
    assert boundary.storage_portability.portable_storage_required is True
    assert boundary.storage_portability.hardcoded_absolute_paths_forbidden is True
    assert boundary.storage_portability.future_nas_compatibility_required is True
    assert boundary.multi_format_required is True
    assert boundary.dedup_required_before_real_import is True
    assert boundary.preview_ready is True


def test_history_canonical_truth_split_rejects_wrong_flags() -> None:
    with pytest.raises(ValueError, match="canonical_truth_write_allowed must be False"):
        HistoryCanonicalTruthSplit(
            archive_is_supporting_source=True,
            canonical_truth_write_allowed=True,
            auto_promotion_allowed=False,
        )


def test_history_storage_portability_rejects_non_portable_contract() -> None:
    with pytest.raises(ValueError, match="portable_storage_required must be True"):
        HistoryStoragePortabilityRequirement(
            portable_storage_required=False,
            hardcoded_absolute_paths_forbidden=True,
            future_nas_compatibility_required=True,
        )


def test_history_boundary_contract_rejects_missing_dedup_rule() -> None:
    with pytest.raises(ValueError, match="dedup_required_before_real_import must be True"):
        HistoryBoundaryContract(
            boundary_id="HBOUNDARY-0002",
            title="Bad Boundary",
            owning_package="MAKSIMAR_CORE_LIB/memory_engine/history_ingestion",
            truth_split=HistoryCanonicalTruthSplit(
                archive_is_supporting_source=True,
                canonical_truth_write_allowed=False,
                auto_promotion_allowed=False,
            ),
            storage_portability=HistoryStoragePortabilityRequirement(
                portable_storage_required=True,
                hardcoded_absolute_paths_forbidden=True,
                future_nas_compatibility_required=True,
            ),
            multi_format_required=True,
            dedup_required_before_real_import=False,
        )
