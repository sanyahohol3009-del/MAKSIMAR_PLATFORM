from __future__ import annotations

from MAKSIMAR_SERVER.CODEGEN_CONTEXT import build_codegen_boundary_contract


def test_codegen_boundary_models_smoke() -> None:
    contract = build_codegen_boundary_contract()

    assert contract.boundary_contract_ready is True
    assert contract.immutable_core_protected is True
    assert contract.runtime_mutation_blocked is True
    assert contract.deployment_blocked is True
    assert contract.sandbox_execution_deferred is True
    assert contract.artifact_reference_required is True
