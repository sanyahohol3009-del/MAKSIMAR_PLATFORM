from __future__ import annotations

from MAKSIMAR_CORE_LIB.evidence_memory import (
    build_evidence_memory_contract,
    build_evidence_memory_preview,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_bound_memory_phase_readiness,
    build_evidence_memory_core_binding_contract,
    build_evidence_memory_core_binding_preview,
    build_evidence_source_chain_contract,
)


def test_phase_2_1_final_acceptance_smoke() -> None:
    core = build_evidence_memory_contract()
    core_preview = build_evidence_memory_preview()
    source_chain = build_evidence_source_chain_contract()
    server_readiness = build_evidence_bound_memory_phase_readiness()
    core_binding = build_evidence_memory_core_binding_contract()
    core_binding_preview = build_evidence_memory_core_binding_preview()

    assert core.total_records == 6
    assert core.ready_records == core.total_records
    assert core.conflict_detected_records == 0
    assert core.memory_truth_records == core.total_records
    assert core.knowledge_graph_projection_records == core.total_records
    assert core.read_only_records == core.total_records
    assert core_preview["phase_batch_ready"] is True

    assert source_chain.total_items == 6
    assert source_chain.ready_items == source_chain.total_items
    assert source_chain.conflict_marked_items == 0
    assert source_chain.backend_execution_allowed is False

    assert server_readiness.phase_ready is True
    assert server_readiness.read_only is True
    assert server_readiness.no_mutation_surface is True
    assert server_readiness.mgrep_blocked is True
    assert server_readiness.sqlite_vec_blocked is True
    assert server_readiness.backend_execution_allowed is False

    assert core_binding.total_bindings == 6
    assert core_binding.ready_bindings == core_binding.total_bindings
    assert core_binding.matched_evidence_items == core_binding.total_bindings
    assert core_binding.artifact_ref_matched_bindings == core_binding.total_bindings
    assert core_binding.memory_truth_bindings == core_binding.total_bindings
    assert core_binding.knowledge_graph_projection_bindings == core_binding.total_bindings
    assert core_binding.read_only_bindings == core_binding.total_bindings
    assert core_binding.backend_execution_allowed is False
    assert core_binding_preview["phase_batch_ready"] is True
