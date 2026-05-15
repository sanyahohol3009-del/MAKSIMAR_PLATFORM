from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_update_approval_registry


def test_regulatory_update_approval_models_smoke() -> None:
    registry = build_regulatory_update_approval_registry()

    assert registry.registry_ready is True
    assert len(registry.proposals) >= 2
    assert registry.evidence_pack_ready is True
    assert registry.approval_gate_required is True
    assert registry.approval_required is True
    assert registry.approval_granted is False
    assert registry.auto_apply_allowed is False
    assert registry.canonical_truth_update_allowed is False
    assert registry.runtime_mutation_allowed is False
