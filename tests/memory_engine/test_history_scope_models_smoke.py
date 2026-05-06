from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_ingestion_builders import (
    build_default_history_ingestion_scope,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_scope_models import (
    HistoryIngestionScope,
)


def test_history_scope_models_smoke() -> None:
    scope = build_default_history_ingestion_scope()

    assert scope.track_name == "project_history_ingestion_track"
    assert scope.owning_domain == "memory_engine"
    assert scope.package_path == "MAKSIMAR_CORE_LIB/memory_engine/history_ingestion"
    assert scope.supporting_source_only is True
    assert scope.canonical_truth_write_allowed is False
    assert scope.real_data_import_allowed is False
    assert scope.supports_html is True
    assert scope.supports_pdf is True
    assert scope.dedup_required is True
    assert "json" in scope.supported_source_types
    assert "portable_storage" in scope.required_capabilities


def test_history_scope_models_reject_empty_track_name() -> None:
    with pytest.raises(ValueError, match="track_name must be a non-empty string"):
        HistoryIngestionScope(
            track_name="",
            owning_domain="memory_engine",
            package_path="MAKSIMAR_CORE_LIB/memory_engine/history_ingestion",
            supported_source_types=("html",),
            required_capabilities=("supporting_source_only",),
            supporting_source_only=True,
            canonical_truth_write_allowed=False,
            real_data_import_allowed=False,
        )


def test_history_scope_models_reject_duplicate_source_types() -> None:
    with pytest.raises(ValueError, match="supported_source_types must not contain duplicates"):
        HistoryIngestionScope(
            track_name="project_history_ingestion_track",
            owning_domain="memory_engine",
            package_path="MAKSIMAR_CORE_LIB/memory_engine/history_ingestion",
            supported_source_types=("html", "html"),
            required_capabilities=("supporting_source_only",),
            supporting_source_only=True,
            canonical_truth_write_allowed=False,
            real_data_import_allowed=False,
        )
