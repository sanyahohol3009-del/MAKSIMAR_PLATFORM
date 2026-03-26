from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_debug import (
    build_patch_candidate_contract,
)


def test_patch_candidate_contract_builds() -> None:
    """Patch candidate contract should build successfully."""
    contract = build_patch_candidate_contract()

    assert contract.total_candidates == 2
    assert len(contract.candidates) == 2
    assert contract.auto_deploy_allowed is False


def test_patch_candidate_contract_is_sandbox_only() -> None:
    """Patch candidates should remain sandbox-only and core-safe."""
    contract = build_patch_candidate_contract()

    assert contract.candidates[0].sandbox_only is True
    assert contract.candidates[0].core_write_allowed is False
    assert contract.candidates[-1].sandbox_only is True
    assert contract.candidates[-1].core_write_allowed is False
