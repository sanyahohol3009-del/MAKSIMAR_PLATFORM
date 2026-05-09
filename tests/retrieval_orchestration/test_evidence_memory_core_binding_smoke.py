from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_memory_core_binding_contract,
)


def test_evidence_memory_core_binding_smoke() -> None:
    contract = build_evidence_memory_core_binding_contract()

    assert contract.total_bindings == 6
    assert contract.ready_bindings == contract.total_bindings
    assert contract.server_phase_ready is True
    assert contract.core_preview_ready is True
