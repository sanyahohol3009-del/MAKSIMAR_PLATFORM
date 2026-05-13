from __future__ import annotations

from MAKSIMAR_SERVER.SELF_EXPANSION_GATE import build_self_expansion_readiness_contract


def test_self_expansion_readiness_models_smoke() -> None:
    contract = build_self_expansion_readiness_contract()

    assert contract.readiness_ready is True
    assert contract.phase_id == "PHASE 6.5"
    assert contract.gap_detection_ready is True
    assert contract.proposal_preparation_ready is True
    assert contract.human_approval_required is True
    assert contract.proposal_only_self_expansion_allowed is True
    assert contract.autonomous_self_expansion_allowed is False
    assert contract.direct_core_write_allowed is False
    assert contract.productization_allowed_now is False
