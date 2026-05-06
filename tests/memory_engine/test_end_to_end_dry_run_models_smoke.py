from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.end_to_end_dry_run_builder import (
    build_end_to_end_dry_run_proof,
)


def test_end_to_end_dry_run_models_smoke() -> None:
    proof = build_end_to_end_dry_run_proof()

    assert proof.route_ready is True
    assert proof.dry_run_only is True
