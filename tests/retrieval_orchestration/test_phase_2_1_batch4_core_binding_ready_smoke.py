from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_memory_core_binding_contract,
    build_evidence_memory_core_binding_preview,
)


def test_phase_2_1_batch4_core_binding_ready_smoke() -> None:
    contract = build_evidence_memory_core_binding_contract()
    preview = build_evidence_memory_core_binding_preview()

    assert preview["phase_batch_ready"] is True
    assert contract.ready_bindings == contract.total_bindings
    assert contract.read_only_bindings == contract.total_bindings
    assert contract.backend_execution_allowed is False
