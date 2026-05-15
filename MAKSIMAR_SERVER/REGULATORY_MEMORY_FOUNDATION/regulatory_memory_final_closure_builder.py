from __future__ import annotations

from typing import Dict, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_memory_final_index import (
    build_regulatory_memory_final_index_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_routing_preview_builder import (
    build_regulatory_routing_preview,
)


MEMORY_FOUNDATION_DOMAINS: Tuple[str, ...] = (
    "personal_project_memory",
    "enterprise_memory",
    "regulatory_memory",
    "tenant_memory",
    "country_jurisdiction_memory",
    "evidence_source_version_memory",
    "governance_federation_memory",
    "routing_retrieval_memory",
    "audit_approval_memory",
)


def build_regulatory_memory_final_closure() -> Dict[str, object]:
    index = build_regulatory_memory_final_index_preview()
    routing = build_regulatory_routing_preview()

    final_closure_ready = (
        index["preview_ready"] is True
        and routing["preview_ready"] is True
        and routing["leak_detected"] is False
        and routing["cross_tenant_retrieval_allowed"] is False
        and routing["cross_tenant_merge_allowed"] is False
        and routing["auto_routing_merge_allowed"] is False
    )

    return {
        "closure_id": "regulatory_memory_final_closure_001",
        "closure_ready": final_closure_ready,
        "roadmap_family": "regulatory_memory_foundation",
        "current_closed_phase": "REGULATORY_MEMORY_FOUNDATION_FINAL_CLOSURE",
        "next_step": "Memory Foundation Complete / Next Roadmap Selection",
        "closed_step_count": index["closed_step_count"],
        "acceptance_doc_count": index["acceptance_doc_count"],
        "memory_foundation_domains": MEMORY_FOUNDATION_DOMAINS,
        "memory_foundation_domain_count": len(MEMORY_FOUNDATION_DOMAINS),
        "routing_preview_ready": routing["preview_ready"],
        "regulatory_final_index_ready": index["preview_ready"],
        "same_tenant_only": routing["same_tenant_only"],
        "read_only": routing["read_only"],
        "leak_detected": routing["leak_detected"],
        "cross_tenant_retrieval_allowed": routing["cross_tenant_retrieval_allowed"],
        "cross_tenant_merge_allowed": routing["cross_tenant_merge_allowed"],
        "cross_jurisdiction_merge_allowed": routing["cross_jurisdiction_merge_allowed"],
        "auto_routing_merge_allowed": routing["auto_routing_merge_allowed"],
        "runtime_mutation_allowed": False,
        "direct_core_write_allowed": False,
        "canonical_truth_update_allowed": False,
        "auto_apply_allowed": False,
        "deployment_allowed_now": False,
        "external_release_allowed_now": False,
        "operator_approval_required_for_future_changes": True,
    }


def build_regulatory_memory_final_closure_preview() -> Dict[str, object]:
    closure = build_regulatory_memory_final_closure()

    return {
        "preview_id": "regulatory_memory_final_closure_preview_001",
        "preview_ready": closure["closure_ready"],
        **closure,
    }
