from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.MEMORY_CONFLICT_RESOLUTION.conflict_binding_models import (
    build_conflict_binding_contract,
)
from MAKSIMAR_SERVER.MEMORY_CONFLICT_RESOLUTION.memory_conflict_resolution_contract import (
    build_memory_conflict_resolution_contract,
)


def build_conflict_resolution_summary() -> Dict[str, object]:
    resolution = build_memory_conflict_resolution_contract()
    binding = build_conflict_binding_contract()

    summary_ready = (
        resolution.total_entries == binding.total_bindings
        and resolution.promote_new_version_entries == binding.promote_new_version_bindings
        and resolution.keep_existing_entries == binding.keep_existing_bindings
        and resolution.approval_required_entries == binding.approval_required_bindings
        and binding.ready_bindings == binding.total_bindings
        and binding.evidence_bound_bindings == binding.total_bindings
        and binding.governance_bound_bindings == binding.total_bindings
        and binding.proposal_generated_bindings == binding.total_bindings
        and binding.approval_granted_bindings == binding.total_bindings
        and binding.conflict_marker_bindings == binding.total_bindings
        and binding.resolved_bindings == binding.total_bindings
        and binding.memory_truth_required_bindings == binding.total_bindings
        and binding.knowledge_graph_projection_bindings == binding.total_bindings
        and binding.read_only_bindings == binding.total_bindings
    )

    return {
        "resolution_total_entries": resolution.total_entries,
        "resolution_promote_new_version_entries": resolution.promote_new_version_entries,
        "resolution_keep_existing_entries": resolution.keep_existing_entries,
        "resolution_approval_required_entries": resolution.approval_required_entries,
        "conflict_binding_entries": binding.total_bindings,
        "conflict_ready_bindings": binding.ready_bindings,
        "evidence_bound_bindings": binding.evidence_bound_bindings,
        "governance_bound_bindings": binding.governance_bound_bindings,
        "proposal_generated_bindings": binding.proposal_generated_bindings,
        "approval_required_bindings": binding.approval_required_bindings,
        "approval_granted_bindings": binding.approval_granted_bindings,
        "conflict_marker_bindings": binding.conflict_marker_bindings,
        "resolved_bindings": binding.resolved_bindings,
        "promote_new_version_bindings": binding.promote_new_version_bindings,
        "keep_existing_bindings": binding.keep_existing_bindings,
        "memory_truth_required_bindings": binding.memory_truth_required_bindings,
        "knowledge_graph_projection_bindings": (
            binding.knowledge_graph_projection_bindings
        ),
        "read_only_bindings": binding.read_only_bindings,
        "summary_ready": summary_ready,
    }
