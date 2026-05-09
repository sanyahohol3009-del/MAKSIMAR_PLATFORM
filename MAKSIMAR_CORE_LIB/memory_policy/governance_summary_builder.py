from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_policy.governance_binding_models import (
    build_governance_binding_contract,
)
from MAKSIMAR_CORE_LIB.memory_policy.memory_policy_scope_models import (
    build_memory_policy_scope_contract,
)


def build_governance_summary() -> Dict[str, object]:
    scopes = build_memory_policy_scope_contract()
    governance = build_governance_binding_contract()

    summary_ready = (
        scopes.ready_scopes == scopes.total_scopes
        and scopes.evidence_required_scopes == scopes.total_scopes
        and scopes.approval_required_scopes == scopes.total_scopes
        and scopes.conflict_resolution_required_scopes == scopes.total_scopes
        and scopes.promotion_allowed_scopes == scopes.total_scopes
        and scopes.auto_promotion_allowed_scopes == 0
        and scopes.read_only_scopes == scopes.total_scopes
        and governance.ready_bindings == governance.total_bindings
        and governance.approval_required_bindings == governance.total_bindings
        and governance.controlled_promotion_bindings == governance.total_bindings
        and governance.auto_promotion_allowed_bindings == 0
        and governance.conflict_resolution_required_bindings
        == governance.total_bindings
        and governance.conflict_detected_bindings == 0
        and governance.memory_truth_required_bindings == governance.total_bindings
        and governance.knowledge_graph_projection_bindings == governance.total_bindings
        and governance.read_only_bindings == governance.total_bindings
    )

    return {
        "policy_scope_entries": scopes.total_scopes,
        "policy_scope_ready_entries": scopes.ready_scopes,
        "governance_binding_entries": governance.total_bindings,
        "governance_ready_bindings": governance.ready_bindings,
        "evidence_required_scopes": scopes.evidence_required_scopes,
        "approval_required_scopes": scopes.approval_required_scopes,
        "conflict_resolution_required_scopes": (
            scopes.conflict_resolution_required_scopes
        ),
        "promotion_allowed_scopes": scopes.promotion_allowed_scopes,
        "auto_promotion_allowed_scopes": scopes.auto_promotion_allowed_scopes,
        "conflict_detected_bindings": governance.conflict_detected_bindings,
        "memory_truth_required_bindings": (
            governance.memory_truth_required_bindings
        ),
        "knowledge_graph_projection_bindings": (
            governance.knowledge_graph_projection_bindings
        ),
        "read_only_scopes": scopes.read_only_scopes,
        "read_only_bindings": governance.read_only_bindings,
        "summary_ready": summary_ready,
    }
