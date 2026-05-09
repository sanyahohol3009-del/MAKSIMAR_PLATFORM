from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy import (
    build_governance_binding_contract,
    build_governance_preview,
    build_governance_summary,
    build_memory_policy_scope_contract,
)
from MAKSIMAR_SERVER.MEMORY_CONFLICT_RESOLUTION import (
    build_conflict_binding_contract,
    build_conflict_resolution_summary,
)
from MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE import (
    build_promotion_binding_contract,
    build_promotion_summary,
)


def test_phase_2_3_final_acceptance_smoke() -> None:
    scopes = build_memory_policy_scope_contract()
    governance = build_governance_binding_contract()
    governance_summary = build_governance_summary()
    governance_preview = build_governance_preview()
    promotion = build_promotion_binding_contract()
    promotion_summary = build_promotion_summary()
    conflict = build_conflict_binding_contract()
    conflict_summary = build_conflict_resolution_summary()

    assert scopes.ready_scopes == scopes.total_scopes
    assert scopes.evidence_required_scopes == scopes.total_scopes
    assert scopes.approval_required_scopes == scopes.total_scopes
    assert scopes.conflict_resolution_required_scopes == scopes.total_scopes
    assert scopes.promotion_allowed_scopes == scopes.total_scopes
    assert scopes.auto_promotion_allowed_scopes == 0
    assert scopes.read_only_scopes == scopes.total_scopes

    assert governance.ready_bindings == governance.total_bindings
    assert governance.auto_promotion_allowed_bindings == 0
    assert governance.conflict_detected_bindings == 0
    assert governance.memory_truth_required_bindings == governance.total_bindings
    assert governance.knowledge_graph_projection_bindings == governance.total_bindings
    assert governance.read_only_bindings == governance.total_bindings
    assert governance_summary["summary_ready"] is True
    assert governance_preview["phase_batch_ready"] is True

    assert promotion.ready_bindings == promotion.total_bindings
    assert promotion.governance_bound_bindings == promotion.total_bindings
    assert promotion.auto_promotion_allowed_bindings == 0
    assert promotion.approval_required_bindings == promotion.total_bindings
    assert promotion_summary["summary_ready"] is True

    assert conflict.ready_bindings == conflict.total_bindings
    assert conflict.governance_bound_bindings == conflict.total_bindings
    assert conflict.approval_required_bindings == conflict.total_bindings
    assert conflict.approval_granted_bindings == conflict.total_bindings
    assert conflict.resolved_bindings == conflict.total_bindings
    assert conflict_summary["summary_ready"] is True
