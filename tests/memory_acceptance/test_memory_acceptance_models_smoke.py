from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE import build_memory_acceptance_contract


def test_memory_acceptance_models_smoke() -> None:
    contract = build_memory_acceptance_contract()

    assert contract.contract_id
    assert contract.roadmap_family == "memory_roadmap_v5_1"
    assert contract.phase_id == "PHASE 6.0"
    assert contract.track_scope == "memory"
    assert contract.acceptance_ready is True
    assert len(contract.criteria) >= 5
    assert contract.dashboard_read_only is True
    assert contract.duplicate_write_allowed is False
    assert contract.canonical_write_allowed is False
    assert contract.runtime_mutation_allowed is False
