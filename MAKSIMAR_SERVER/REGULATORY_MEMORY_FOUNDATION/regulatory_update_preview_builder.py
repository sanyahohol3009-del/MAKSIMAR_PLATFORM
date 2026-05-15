from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_update_approval_gate import (
    build_regulatory_update_approval_gate_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_update_approval_models import (
    build_regulatory_update_approval_registry,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_update_diff_builder import (
    build_regulatory_update_diff_preview,
)


def build_regulatory_update_approval_preview() -> Dict[str, object]:
    registry = build_regulatory_update_approval_registry()
    gate = build_regulatory_update_approval_gate_preview()
    diff = build_regulatory_update_diff_preview()

    preview_path = (
        "regulatory_update_approval_models",
        "regulatory_update_approval_gate",
        "regulatory_update_diff_builder",
        "regulatory_routing_no_cross_tenant_leak_next",
    )

    preview_ready = (
        registry.registry_ready
        and gate["preview_ready"] is True
        and diff["preview_ready"] is True
        and registry.approval_required is True
        and registry.approval_granted is False
        and registry.auto_apply_allowed is False
        and registry.canonical_truth_update_allowed is False
    )

    return {
        "preview_id": "regulatory_update_approval_preview_step_7_001",
        "preview_ready": preview_ready,
        "roadmap_family": "regulatory_memory_foundation",
        "current_step": "STEP 7 — Regulatory Update Approval Gate",
        "next_step": "STEP 8 — Regulatory Routing / No Cross-Tenant Leak",
        "preview_path": preview_path,
        "registry_id": registry.registry_id,
        "proposal_count": len(registry.proposals),
        "proposal_ids": tuple(proposal.proposal_id for proposal in registry.proposals),
        "diff_entry_count": diff["diff_entry_count"],
        "source_refs": diff["source_refs"],
        "evidence_pack_ready": registry.evidence_pack_ready,
        "approval_gate_required": registry.approval_gate_required,
        "approval_required": registry.approval_required,
        "approval_granted": registry.approval_granted,
        "proposal_only": gate["proposal_only"],
        "diff_required": gate["diff_required"],
        "operator_review_required": gate["operator_review_required"],
        "auto_apply_allowed": registry.auto_apply_allowed,
        "canonical_truth_update_allowed": registry.canonical_truth_update_allowed,
        "runtime_mutation_allowed": registry.runtime_mutation_allowed,
        "direct_core_write_allowed": registry.direct_core_write_allowed,
        "deployment_allowed_now": registry.deployment_allowed_now,
    }
