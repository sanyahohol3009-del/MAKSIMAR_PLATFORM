from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_conflict_preview_builder import (
    build_regulatory_conflict_drift_supersession_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_source_version_models import (
    build_regulatory_source_version_registry,
)


EvidenceItemKind = Literal[
    "source_version",
    "effective_date",
    "jurisdiction_binding",
    "tenant_scope_binding",
    "conflict_candidate",
    "drift_signal",
    "supersession_candidate",
]

EvidenceReviewState = Literal["read_only", "requires_human_review", "approval_pending"]


@dataclass(frozen=True, slots=True)
class ComplianceEvidenceItem:
    evidence_id: str
    evidence_kind: EvidenceItemKind
    source_ref: str
    tenant_id: str
    jurisdiction_id: str
    source_version: str
    effective_date: str
    review_state: EvidenceReviewState
    source_bound: bool
    version_present: bool
    effective_date_present: bool
    trace_required: bool
    human_review_required: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool
    evidence_ready: bool

    def __post_init__(self) -> None:
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
        if self.source_bound is not True:
            raise ValueError("source_bound must be True")
        if self.version_present is not True:
            raise ValueError("version_present must be True")
        if self.effective_date_present is not True:
            raise ValueError("effective_date_present must be True")
        if self.trace_required is not True:
            raise ValueError("trace_required must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.canonical_truth_update_allowed:
            raise ValueError("canonical_truth_update_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.evidence_ready is not True:
            raise ValueError("evidence_ready must be True")


@dataclass(frozen=True, slots=True)
class ComplianceEvidencePack:
    pack_id: str
    evidence_items: Tuple[ComplianceEvidenceItem, ...]
    source_registry_ready: bool
    conflict_drift_supersession_ready: bool
    evidence_pack_ready: bool
    source_to_decision_trace_required: bool
    audit_read_model_required: bool
    human_review_required: bool
    automatic_resolution_allowed: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool
    direct_core_write_allowed: bool
    deployment_allowed_now: bool

    def __post_init__(self) -> None:
        if not self.pack_id:
            raise ValueError("pack_id must be non-empty")
        if not self.evidence_items:
            raise ValueError("evidence_items must be non-empty")
        evidence_ids = {item.evidence_id for item in self.evidence_items}
        if len(evidence_ids) != len(self.evidence_items):
            raise ValueError("evidence_id values must be unique")
        if self.source_registry_ready is not True:
            raise ValueError("source_registry_ready must be True")
        if self.conflict_drift_supersession_ready is not True:
            raise ValueError("conflict_drift_supersession_ready must be True")
        if self.evidence_pack_ready is not True:
            raise ValueError("evidence_pack_ready must be True")
        if self.source_to_decision_trace_required is not True:
            raise ValueError("source_to_decision_trace_required must be True")
        if self.audit_read_model_required is not True:
            raise ValueError("audit_read_model_required must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.automatic_resolution_allowed:
            raise ValueError("automatic_resolution_allowed must be False")
        if self.canonical_truth_update_allowed:
            raise ValueError("canonical_truth_update_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.deployment_allowed_now:
            raise ValueError("deployment_allowed_now must be False")
        if not all(item.evidence_ready for item in self.evidence_items):
            raise ValueError("all evidence items must be ready")


def build_compliance_evidence_pack() -> ComplianceEvidencePack:
    source_registry = build_regulatory_source_version_registry()
    conflict_preview = build_regulatory_conflict_drift_supersession_preview()

    evidence_items = tuple(
        ComplianceEvidenceItem(
            evidence_id=f"compliance_evidence_{source.source_ref}",
            evidence_kind="source_version",
            source_ref=source.source_ref,
            tenant_id=source.tenant_id,
            jurisdiction_id=source.jurisdiction_id,
            source_version=source.source_version,
            effective_date=source.effective_date,
            review_state="requires_human_review",
            source_bound=True,
            version_present=True,
            effective_date_present=True,
            trace_required=True,
            human_review_required=True,
            canonical_truth_update_allowed=False,
            runtime_mutation_allowed=False,
            evidence_ready=True,
        )
        for source in source_registry.sources
    )

    return ComplianceEvidencePack(
        pack_id="compliance_evidence_pack_step_6_001",
        evidence_items=evidence_items,
        source_registry_ready=source_registry.registry_ready,
        conflict_drift_supersession_ready=conflict_preview["preview_ready"],
        evidence_pack_ready=source_registry.registry_ready and conflict_preview["preview_ready"] is True,
        source_to_decision_trace_required=True,
        audit_read_model_required=True,
        human_review_required=True,
        automatic_resolution_allowed=False,
        canonical_truth_update_allowed=False,
        runtime_mutation_allowed=False,
        direct_core_write_allowed=False,
        deployment_allowed_now=False,
    )
