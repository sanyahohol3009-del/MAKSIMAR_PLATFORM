from __future__ import annotations

from MAKSIMAR_SERVER.CODEGEN_CONTEXT import build_codegen_intent_contract


def test_codegen_intent_models_smoke() -> None:
    contract = build_codegen_intent_contract()

    assert contract.intent_contract_ready is True
    assert len(contract.intents) >= 5
    assert contract.proposal_required_for_all is True
    assert contract.audit_required_for_all is True
    assert contract.approval_required_for_all is True
    assert contract.sandbox_required_later_for_all is True
    assert contract.direct_write_allowed is False
