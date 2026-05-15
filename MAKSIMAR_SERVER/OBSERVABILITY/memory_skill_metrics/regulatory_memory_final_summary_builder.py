from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_memory_final_closure_builder import (
    build_regulatory_memory_final_closure_preview,
)


def build_regulatory_memory_final_summary() -> Dict[str, object]:
    preview = build_regulatory_memory_final_closure_preview()

    return {
        "summary_id": "regulatory_memory_final_summary_001",
        "summary_ready": preview["preview_ready"],
        "roadmap_family": preview["roadmap_family"],
        "current_closed_phase": preview["current_closed_phase"],
        "next_step": preview["next_step"],
        "closed_step_count": preview["closed_step_count"],
        "acceptance_doc_count": preview["acceptance_doc_count"],
        "memory_foundation_domain_count": preview["memory_foundation_domain_count"],
        "memory_foundation_domains": preview["memory_foundation_domains"],
        "same_tenant_only": preview["same_tenant_only"],
        "read_only": preview["read_only"],
        "leak_detected": preview["leak_detected"],
        "cross_tenant_retrieval_allowed": preview["cross_tenant_retrieval_allowed"],
        "cross_tenant_merge_allowed": preview["cross_tenant_merge_allowed"],
        "cross_jurisdiction_merge_allowed": preview["cross_jurisdiction_merge_allowed"],
        "auto_routing_merge_allowed": preview["auto_routing_merge_allowed"],
        "runtime_mutation_allowed": preview["runtime_mutation_allowed"],
        "direct_core_write_allowed": preview["direct_core_write_allowed"],
        "canonical_truth_update_allowed": preview["canonical_truth_update_allowed"],
        "auto_apply_allowed": preview["auto_apply_allowed"],
        "deployment_allowed_now": preview["deployment_allowed_now"],
        "external_release_allowed_now": preview["external_release_allowed_now"],
        "operator_approval_required_for_future_changes": preview["operator_approval_required_for_future_changes"],
    }
