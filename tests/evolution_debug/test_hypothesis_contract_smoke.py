from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_debug import (
    build_debug_hypothesis_contract,
)


def test_hypothesis_contract_builds() -> None:
    """Debug hypothesis contract should build successfully."""
    contract = build_debug_hypothesis_contract()

    assert contract.total_hypotheses == 2
    assert len(contract.hypotheses) == 2
    assert contract.sandbox_required is True


def test_hypothesis_contract_contains_expected_scope() -> None:
    """Debug hypothesis contract should contain known patch scopes."""
    contract = build_debug_hypothesis_contract()

    scopes = {hypothesis.proposed_patch_scope for hypothesis in contract.hypotheses}

    assert "runtime_observability" in scopes
    assert "oob_dashboard" in scopes
