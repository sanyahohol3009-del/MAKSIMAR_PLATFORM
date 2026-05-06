from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.end_to_end_dry_run_builder import (
    build_end_to_end_dry_run_proof,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.end_to_end_dry_run_validators import (
    validate_end_to_end_dry_run_ready,
)


def test_end_to_end_readiness_smoke() -> None:
    proof = build_end_to_end_dry_run_proof()
    validate_end_to_end_dry_run_ready(proof)

    assert proof.route_ready is True
