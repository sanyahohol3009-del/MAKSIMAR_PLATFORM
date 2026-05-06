from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.dedup_models import (
    DedupDecision,
)


def test_dedup_models_smoke() -> None:
    decision = DedupDecision(
        file_already_imported=False,
        content_already_imported=False,
        duplicate_unit_count=0,
        new_unit_count=1,
        write_required=True,
        deterministic_output=True,
        parallel_safe_by_design=True,
    )

    assert decision.write_required is True
    assert decision.new_unit_count == 1
