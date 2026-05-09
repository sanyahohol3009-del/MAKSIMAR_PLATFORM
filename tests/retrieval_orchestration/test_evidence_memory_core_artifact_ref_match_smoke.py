from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_memory_core_binding_contract,
)


def test_evidence_memory_core_artifact_ref_match_smoke() -> None:
    contract = build_evidence_memory_core_binding_contract()

    assert contract.artifact_ref_matched_bindings == contract.total_bindings
    for entry in contract.entries:
        assert entry.artifact_ref_match is True
