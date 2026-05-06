from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.canonical_mapping import (
    build_history_track_canonical_mapping,
)


def test_canonical_mapping_smoke() -> None:
    mapping = build_history_track_canonical_mapping()

    assert "H1_source_intake" in mapping
    assert "H15_completion_layer" in mapping
    assert "support_only_noncanonical_helpers" in mapping
