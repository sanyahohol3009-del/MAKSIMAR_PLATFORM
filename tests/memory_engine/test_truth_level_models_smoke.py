from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.truth_level_models import (
    SUPPORTED_TRUTH_LEVELS,
)


def test_truth_level_models_smoke() -> None:
    assert "raw_archive_fact" in SUPPORTED_TRUTH_LEVELS
    assert "validated_project_fact" in SUPPORTED_TRUTH_LEVELS
    assert "canonical_rule" in SUPPORTED_TRUTH_LEVELS
