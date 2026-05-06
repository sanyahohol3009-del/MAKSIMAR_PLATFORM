from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.canonical_mapping import (
    build_history_track_canonical_mapping,
)


def test_support_helpers_not_canonical_smoke() -> None:
    mapping = build_history_track_canonical_mapping()
    support_bucket = mapping["support_only_noncanonical_helpers"]

    assert "end_to_end_dry_run_builder.py" in support_bucket
    assert "__init__.py" in support_bucket
