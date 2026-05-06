from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.end_to_end_dry_run_builder import (
    build_end_to_end_dry_run_proof,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.end_to_end_dry_run_summary_builder import (
    build_end_to_end_dry_run_summary,
)


def test_end_to_end_dry_run_summary_builder_smoke() -> None:
    proof = build_end_to_end_dry_run_proof()
    summary = build_end_to_end_dry_run_summary(proof)

    assert summary["route_ready"] is True
    assert summary["dry_run_only"] is True
