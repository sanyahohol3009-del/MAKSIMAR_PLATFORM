from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.compliance_evidence_pack_models import (
    build_compliance_evidence_pack,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_conflict_preview_builder import (
    build_regulatory_conflict_drift_supersession_preview,
)


@dataclass(frozen=True, slots=True)
class RegulatoryAuditReadEntry:
    audit_entry_id: str
    evidence_id: str
    source_ref: str
    tenant_id: str
    jurisdiction_id: str
    source_version: str
    effective_date: str
    review_state: str
    source_to_decision_trace_available: bool
    operator_visible: bool
    read_only: bool
    mutation_allowed: bool
    entry_ready: bool

    def __post_init__(self) -> None:
        if not self.audit_entry_id:
            raise ValueError("audit_entry_id must be non-empty")
        if not self.evidence_id:
            raise ValueError("evidence_id must be non-empty")
        if not self.source_ref:
            raise ValueError("source_ref must be non-empty")
        if not self.tenant_id:
            raise ValueError("tenant_id must be non-empty")
        if not self.jurisdiction_id:
            raise ValueError("jurisdiction_id must be non-empty")
        if not self.source_version:
            raise ValueError("source_version must be non-empty")
        if not self.effective_date:
            raise ValueError("effective_date must be non-empty")
        if self.source_to_decision_trace_available is not True:
            raise ValueError("source_to_decision_trace_available must be True")
        if self.operator_visible is not True:
            raise ValueError("operator_visible must be True")
        if self.read_only is not True:
            raise ValueError("read_only must be True")
        if self.mutation_allowed:
            raise ValueError("mutation_allowed must be False")
        if self.entry_ready is not True:
            raise ValueError("entry_ready must be True")


@dataclass(frozen=True, slots=True)
class RegulatoryAuditReadModel:
    read_model_id: str
    audit_entries: Tuple[RegulatoryAuditReadEntry, ...]
    evidence_pack_ready: bool
    conflict_drift_supersession_ready: bool
    audit_read_model_ready: bool
    operator_visible: bool
    read_only: bool
    mutation_allowed: bool
    human_review_required: bool
    automatic_resolution_allowed: bool
    canonical_truth_update_allowed: bool

    def __post_init__(self) -> None:
        if not self.read_model_id:
            raise ValueError("read_model_id must be non-empty")
        if not self.audit_entries:
            raise ValueError("audit_entries must be non-empty")
        entry_ids = {entry.audit_entry_id for entry in self.audit_entries}
        if len(entry_ids) != len(self.audit_entries):
            raise ValueError("audit_entry_id values must be unique")
        if self.evidence_pack_ready is not True:
            raise ValueError("evidence_pack_ready must be True")
        if self.conflict_drift_supersession_ready is not True:
            raise ValueError("conflict_drift_supersession_ready must be True")
        if self.audit_read_model_ready is not True:
            raise ValueError("audit_read_model_ready must be True")
        if self.operator_visible is not True:
            raise ValueError("operator_visible must be True")
        if self.read_only is not True:
            raise ValueError("read_only must be True")
        if self.mutation_allowed:
            raise ValueError("mutation_allowed must be False")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.automatic_resolution_allowed:
            raise ValueError("automatic_resolution_allowed must be False")
        if self.canonical_truth_update_allowed:
            raise ValueError("canonical_truth_update_allowed must be False")
        if not all(entry.entry_ready for entry in self.audit_entries):
            raise ValueError("all audit entries must be ready")


def build_regulatory_audit_read_model() -> RegulatoryAuditReadModel:
    evidence_pack = build_compliance_evidence_pack()
    conflict_preview = build_regulatory_conflict_drift_supersession_preview()

    entries = tuple(
        RegulatoryAuditReadEntry(
            audit_entry_id=f"audit_read_{item.evidence_id}",
            evidence_id=item.evidence_id,
            source_ref=item.source_ref,
            tenant_id=item.tenant_id,
            jurisdiction_id=item.jurisdiction_id,
            source_version=item.source_version,
            effective_date=item.effective_date,
            review_state=item.review_state,
            source_to_decision_trace_available=True,
            operator_visible=True,
            read_only=True,
            mutation_allowed=False,
            entry_ready=True,
        )
        for item in evidence_pack.evidence_items
    )

    return RegulatoryAuditReadModel(
        read_model_id="regulatory_audit_read_model_step_6_001",
        audit_entries=entries,
        evidence_pack_ready=evidence_pack.evidence_pack_ready,
        conflict_drift_supersession_ready=conflict_preview["preview_ready"],
        audit_read_model_ready=evidence_pack.evidence_pack_ready and conflict_preview["preview_ready"] is True,
        operator_visible=True,
        read_only=True,
        mutation_allowed=False,
        human_review_required=True,
        automatic_resolution_allowed=False,
        canonical_truth_update_allowed=False,
    )


def build_regulatory_audit_read_model_preview() -> Dict[str, object]:
    read_model = build_regulatory_audit_read_model()

    return {
        "preview_id": "regulatory_audit_read_model_preview_step_6_001",
        "preview_ready": read_model.audit_read_model_ready,
        "read_model_id": read_model.read_model_id,
        "audit_entry_count": len(read_model.audit_entries),
        "source_refs": tuple(entry.source_ref for entry in read_model.audit_entries),
        "tenant_ids": tuple(sorted({entry.tenant_id for entry in read_model.audit_entries})),
        "jurisdiction_ids": tuple(sorted({entry.jurisdiction_id for entry in read_model.audit_entries})),
        "evidence_pack_ready": read_model.evidence_pack_ready,
        "conflict_drift_supersession_ready": read_model.conflict_drift_supersession_ready,
        "operator_visible": read_model.operator_visible,
        "read_only": read_model.read_only,
        "mutation_allowed": read_model.mutation_allowed,
        "human_review_required": read_model.human_review_required,
        "automatic_resolution_allowed": read_model.automatic_resolution_allowed,
        "canonical_truth_update_allowed": read_model.canonical_truth_update_allowed,
    }
