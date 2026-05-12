from __future__ import annotations

from MAKSIMAR_SERVER.PROPOSAL_AUDIT import build_proposal_audit_spine_contract


def test_proposal_audit_spine_models_smoke() -> None:
    contract = build_proposal_audit_spine_contract()

    assert contract.spine_ready is True
    assert contract.roadmap_family == "memory_roadmap_v5_1"
    assert contract.phase_id == "PHASE 6.2"
    assert contract.proposal_visible is True
    assert contract.audit_visible is True
    assert contract.approval_visible is True
    assert contract.code_write_allowed is False
    assert contract.action_execution_allowed is False
