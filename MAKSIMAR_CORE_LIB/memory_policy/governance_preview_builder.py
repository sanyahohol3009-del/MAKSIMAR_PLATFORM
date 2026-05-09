from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_policy.governance_summary_builder import (
    build_governance_summary,
)


_GOVERNANCE_PREVIEW_FLOW = (
    "memory_classification_policy",
    "memory_policy_scope",
    "core_evidence_memory",
    "governance_binding",
    "approval_required_gate",
    "conflict_resolution_gate",
    "controlled_promotion_gate",
    "knowledge_graph_projection_gate",
    "read_only_gate",
    "governance_preview",
)


def build_governance_preview() -> Dict[str, object]:
    summary = build_governance_summary()

    return {
        "flow": _GOVERNANCE_PREVIEW_FLOW,
        "policy_scope_entries": summary["policy_scope_entries"],
        "policy_scope_ready_entries": summary["policy_scope_ready_entries"],
        "governance_binding_entries": summary["governance_binding_entries"],
        "governance_ready_bindings": summary["governance_ready_bindings"],
        "evidence_required_scopes": summary["evidence_required_scopes"],
        "approval_required_scopes": summary["approval_required_scopes"],
        "conflict_resolution_required_scopes": (
            summary["conflict_resolution_required_scopes"]
        ),
        "promotion_allowed_scopes": summary["promotion_allowed_scopes"],
        "auto_promotion_allowed_scopes": summary["auto_promotion_allowed_scopes"],
        "conflict_detected_bindings": summary["conflict_detected_bindings"],
        "memory_truth_required_bindings": (
            summary["memory_truth_required_bindings"]
        ),
        "knowledge_graph_projection_bindings": (
            summary["knowledge_graph_projection_bindings"]
        ),
        "read_only_scopes": summary["read_only_scopes"],
        "read_only_bindings": summary["read_only_bindings"],
        "summary_ready": summary["summary_ready"],
        "preview_ready": True,
        "phase_batch_ready": bool(summary["summary_ready"]),
    }
