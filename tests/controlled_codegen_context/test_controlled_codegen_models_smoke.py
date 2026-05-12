from __future__ import annotations

from MAKSIMAR_SERVER.CODEGEN_CONTEXT import build_controlled_codegen_context_contract


def test_controlled_codegen_models_smoke() -> None:
    contract = build_controlled_codegen_context_contract()

    assert contract.controlled_codegen_context_ready is True
    assert contract.phase_id == "PHASE 6.3"
    assert contract.intent_models_ready is True
    assert contract.boundary_models_ready is True
    assert contract.direct_core_write_allowed is False
    assert contract.deployment_allowed is False
    assert contract.sandbox_execution_allowed_now is False
