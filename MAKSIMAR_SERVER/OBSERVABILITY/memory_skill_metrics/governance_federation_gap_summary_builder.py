from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_policy.governance_federation_gap_report_builder import (
    build_governance_federation_gap_report,
)


def build_governance_federation_gap_summary() -> Dict[str, object]:
    report = build_governance_federation_gap_report()

    return {
        "summary_id": "governance_federation_gap_summary_001",
        "summary_ready": report["gap_pass_ready"],
        "roadmap_family": report["roadmap_family"],
        "current_step": report["current_step"],
        "existing_surfaces_reused": report["existing_surfaces_reused"],
        "missing_required_surface_count": len(report["missing_required_surfaces"]),
        "trust_scope_ready": report["trust_scope_ready"],
        "source_priority_ready": report["source_priority_ready"],
        "federation_policy_ready": report["federation_policy_ready"],
        "tenant_personal_separation_ready": report["tenant_personal_separation_ready"],
        "proposal_audit_allowed_next": report["proposal_audit_allowed_next"],
        "codegen_allowed_now": report["codegen_allowed_now"],
        "sandbox_allowed_now": report["sandbox_allowed_now"],
        "self_expansion_allowed_now": report["self_expansion_allowed_now"],
    }
