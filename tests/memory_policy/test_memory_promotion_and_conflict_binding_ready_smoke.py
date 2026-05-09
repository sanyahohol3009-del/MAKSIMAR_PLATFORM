from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy import (
    build_governance_binding_contract,
    build_governance_preview,
)
from MAKSIMAR_SERVER.MEMORY_CONFLICT_RESOLUTION import (
    build_conflict_binding_contract,
    build_conflict_resolution_summary,
)
from MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE import (
    build_promotion_binding_contract,
    build_promotion_summary,
)


def test_memory_promotion_and_conflict_binding_ready_smoke() -> None:
    governance = build_governance_binding_contract()
    governance_preview = build_governance_preview()
    promotion = build_promotion_binding_contract()
    promotion_summary = build_promotion_summary()
    conflict = build_conflict_binding_contract()
    conflict_summary = build_conflict_resolution_summary()

    assert governance.ready_bindings == governance.total_bindings
    assert governance.approval_required_bindings == governance.total_bindings
    assert governance.auto_promotion_allowed_bindings == 0
    assert governance.conflict_resolution_required_bindings == governance.total_bindings
    assert governance.memory_truth_required_bindings == governance.total_bindings
    assert governance.knowledge_graph_projection_bindings == governance.total_bindings
    assert governance.read_only_bindings == governance.total_bindings
    assert governance_preview["phase_batch_ready"] is True

    assert promotion.ready_bindings == promotion.total_bindings
    assert promotion.evidence_bound_bindings == promotion.total_bindings
    assert promotion.governance_bound_bindings == promotion.total_bindings
    assert promotion.approval_required_bindings == promotion.total_bindings
    assert promotion.auto_promotion_allowed_bindings == 0
    assert promotion.controlled_promotion_bindings == promotion.total_bindings
    assert promotion.read_only_bindings == promotion.total_bindings
    assert promotion_summary["summary_ready"] is True

    assert conflict.ready_bindings == conflict.total_bindings
    assert conflict.evidence_bound_bindings == conflict.total_bindings
    assert conflict.governance_bound_bindings == conflict.total_bindings
    assert conflict.approval_required_bindings == conflict.total_bindings
    assert conflict.approval_granted_bindings == conflict.total_bindings
    assert conflict.resolved_bindings == conflict.total_bindings
    assert conflict.memory_truth_required_bindings == conflict.total_bindings
    assert conflict.knowledge_graph_projection_bindings == conflict.total_bindings
    assert conflict.read_only_bindings == conflict.total_bindings
    assert conflict_summary["summary_ready"] is True
