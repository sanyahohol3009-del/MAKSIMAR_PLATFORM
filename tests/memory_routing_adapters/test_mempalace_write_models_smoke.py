from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_write_request_contract,
)


def test_mempalace_write_models_smoke() -> None:
    contract = build_mempalace_write_request_contract()

    assert contract.total_write_requests == 4
    assert contract.ready_write_requests == contract.total_write_requests
    assert contract.allowed_write_requests == 3
    assert contract.approval_required_write_requests == 3
    assert contract.approval_granted_write_requests == 0
    assert contract.sandbox_stage_required_write_requests == 3
    assert contract.diff_preview_required_write_requests == 3
    assert contract.risk_summary_required_write_requests == 3
    assert contract.canonical_write_allowed_write_requests == 0
    assert contract.auto_promotion_allowed_write_requests == 0
    assert contract.runtime_mutation_allowed_write_requests == 0
