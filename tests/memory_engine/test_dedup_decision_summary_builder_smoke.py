from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.dedup_decision_summary_builder import (
    build_dedup_decision_summary,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.dedup_models import (
    DedupDecision,
)


def test_dedup_decision_summary_builder_smoke() -> None:
    decision = DedupDecision(
        file_already_imported=False,
        content_already_imported=False,
        duplicate_unit_count=0,
        new_unit_count=1,
        write_required=True,
        deterministic_output=True,
        parallel_safe_by_design=True,
    )
    summary = build_dedup_decision_summary(decision)

    assert summary["write_required"] is True
    assert summary["new_unit_count"] == 1
