from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.compliance_evidence_pack_models import (
    build_compliance_evidence_pack,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.compliance_traceability_builder import (
    build_compliance_traceability_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_audit_read_model import (
    build_regulatory_audit_read_model_preview,
)


def build_compliance_evidence_pack_preview() -> Dict[str, object]:
    evidence_pack = build_compliance_evidence_pack()
    audit = build_regulatory_audit_read_model_preview()
    traceability = build_compliance_traceability_preview()

    preview_path = (
        "compliance_evidence_pack_models",
        "regulatory_audit_read_model",
        "compliance_traceability_builder",
        "regulatory_update_approval_gate_next",
    )

    preview_ready = (
        evidence_pack.evidence_pack_ready
        and audit["preview_ready"] is True
        and traceability["preview_ready"] is True
        and evidence_pack.automatic_resolution_allowed is False
        and evidence_pack.canonical_truth_update_allowed is False
    )

    return {
        "preview_id": "compliance_evidence_pack_preview_step_6_001",
        "preview_ready": preview_ready,
        "roadmap_family": "regulatory_memory_foundation",
        "current_step": "STEP 6 — Compliance Evidence Pack / Audit Read Model",
        "next_step": "STEP 7 — Regulatory Update Approval Gate",
        "preview_path": preview_path,
        "pack_id": evidence_pack.pack_id,
        "evidence_item_count": len(evidence_pack.evidence_items),
        "audit_entry_count": audit["audit_entry_count"],
        "trace_step_count": traceability["trace_step_count"],
        "source_refs": audit["source_refs"],
        "tenant_ids": audit["tenant_ids"],
        "jurisdiction_ids": audit["jurisdiction_ids"],
        "source_to_decision_trace_required": evidence_pack.source_to_decision_trace_required,
        "source_to_decision_trace_ready": traceability["source_to_decision_trace_ready"],
        "audit_read_model_required": evidence_pack.audit_read_model_required,
        "audit_read_model_ready": audit["preview_ready"],
        "operator_visible": audit["operator_visible"],
        "read_only": audit["read_only"],
        "human_review_required": evidence_pack.human_review_required,
        "automatic_resolution_allowed": evidence_pack.automatic_resolution_allowed,
        "canonical_truth_update_allowed": evidence_pack.canonical_truth_update_allowed,
        "runtime_mutation_allowed": evidence_pack.runtime_mutation_allowed,
        "direct_core_write_allowed": evidence_pack.direct_core_write_allowed,
        "deployment_allowed_now": evidence_pack.deployment_allowed_now,
    }
