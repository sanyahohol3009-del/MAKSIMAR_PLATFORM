from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.end_to_end_dry_run_builder import (
    build_end_to_end_dry_run_proof,
)


def test_end_to_end_dedup_path_smoke() -> None:
    proof = build_end_to_end_dry_run_proof()

    assert proof.dedup_decision.new_unit_count == 1
    assert proof.dedup_decision.write_required is True
