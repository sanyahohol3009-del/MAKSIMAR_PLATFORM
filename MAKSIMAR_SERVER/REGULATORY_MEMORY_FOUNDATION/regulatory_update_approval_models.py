from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.compliance_evidence_preview_builder import (
    build_compliance_evidence_pack_preview,
)


RegulatoryUpdateKind = Literal[
    "new_source_version",
    "effective_date_change",
    "supersession_review",
    "conflict_review",
    "jurisdiction_scope_review",
]

RegulatoryApprovalState = Literal[
    "proposal_created",
    "audit_ready",
    "approval_required",
    "approval_granted",
    "approval_rejected",
]


@dataclass(frozen=True, slots=True)
class RegulatoryUpdateProposal:
    proposal_id: str
    update_kind: RegulatoryUpdateKind
    source_ref: str
    tenant_id: str
    jurisdiction_id: str
    previous_version: str
    proposed_version: str
    previous_effective_date: str
    proposed_effective_date: str
    approval_state: RegulatoryApprovalState
    evidence_pack_ready: bool
    audit_read_model_ready: bool
    source_to_decision_trace_ready: bool
    approval_required: bool
    approval_granted: bool
    auto_apply_allowed: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool
    proposal_ready: bool

    def __post_init__(self) -> None:
        if not self.proposal_id:
            raise ValueError("proposal_id must be non-empty")
        if not self.source_ref:
            raise ValueError("source_ref must be non-empty")
        if not self.tenant_id:
            raise ValueError("tenant_id must be non-empty")
        if not self.jurisdiction_id:
            raise ValueError("jurisdiction_id must be non-empty")
        if not self.previous_version:
            raise ValueError("previous_version must be non-empty")
        if not self.proposed_version:
            raise ValueError("proposed_version must be non-empty")
        if not self.previous_effective_date:
            raise ValueError("previous_effective_date must be non-empty")
        if not self.proposed_effective_date:
            raise ValueError("proposed_effective_date must be non-empty")
        if self.evidence_pack_ready is not True:
            raise ValueError("evidence_pack_ready must be True")
        if self.audit_read_model_ready is not True:
            raise ValueError("audit_read_model_ready must be True")
        if self.source_to_decision_trace_ready is not True:
            raise ValueError("source_to_decision_trace_ready must be True")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.approval_granted:
            raise ValueError("approval_granted must be False until explicit approval")
        if self.auto_apply_allowed:
            raise ValueError("auto_apply_allowed must be False")
        if self.canonical_truth_update_allowed:
            raise ValueError("canonical_truth_update_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.proposal_ready is not True:
            raise ValueError("proposal_ready must be True")


@dataclass(frozen=True, slots=True)
class RegulatoryUpdateApprovalRegistry:
    registry_id: str
    proposals: Tuple[RegulatoryUpdateProposal, ...]
    evidence_pack_ready: bool
    approval_gate_required: bool
    approval_required: bool
    approval_granted: bool
    auto_apply_allowed: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool
    direct_core_write_allowed: bool
    deployment_allowed_now: bool
    registry_ready: bool

    def __post_init__(self) -> None:
        if not self.registry_id:
            raise ValueError("registry_id must be non-empty")
        if not self.proposals:
            raise ValueError("proposals must be non-empty")
        proposal_ids = {proposal.proposal_id for proposal in self.proposals}
        if len(proposal_ids) != len(self.proposals):
            raise ValueError("proposal_id values must be unique")
        if self.evidence_pack_ready is not True:
            raise ValueError("evidence_pack_ready must be True")
        if self.approval_gate_required is not True:
            raise ValueError("approval_gate_required must be True")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.approval_granted:
            raise ValueError("approval_granted must be False")
        if self.auto_apply_allowed:
            raise ValueError("auto_apply_allowed must be False")
        if self.canonical_truth_update_allowed:
            raise ValueError("canonical_truth_update_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.deployment_allowed_now:
            raise ValueError("deployment_allowed_now must be False")
        if not all(proposal.proposal_ready for proposal in self.proposals):
            raise ValueError("all regulatory update proposals must be ready")
        if self.registry_ready is not True:
            raise ValueError("registry_ready must be True")


def build_regulatory_update_approval_registry() -> RegulatoryUpdateApprovalRegistry:
    evidence = build_compliance_evidence_pack_preview()

    proposals = (
        RegulatoryUpdateProposal(
            proposal_id="regulatory_update_proposal_de_law_001",
            update_kind="new_source_version",
            source_ref="reg_source_de_demo_law_v1",
            tenant_id="tenant_demo_de_001",
            jurisdiction_id="jurisdiction_de_country",
            previous_version="2026-01-01",
            proposed_version="2026-03-01",
            previous_effective_date="2026-01-01",
            proposed_effective_date="2026-03-15",
            approval_state="approval_required",
            evidence_pack_ready=evidence["preview_ready"],
            audit_read_model_ready=evidence["audit_read_model_ready"],
            source_to_decision_trace_ready=evidence["source_to_decision_trace_ready"],
            approval_required=True,
            approval_granted=False,
            auto_apply_allowed=False,
            canonical_truth_update_allowed=False,
            runtime_mutation_allowed=False,
            proposal_ready=True,
        ),
        RegulatoryUpdateProposal(
            proposal_id="regulatory_update_proposal_ua_policy_supersession_001",
            update_kind="supersession_review",
            source_ref="reg_source_ua_demo_policy_v1",
            tenant_id="tenant_demo_ua_001",
            jurisdiction_id="jurisdiction_ua_country",
            previous_version="2026-02-01",
            proposed_version="2026-02-01-review",
            previous_effective_date="2026-02-10",
            proposed_effective_date="2026-02-10",
            approval_state="approval_required",
            evidence_pack_ready=evidence["preview_ready"],
            audit_read_model_ready=evidence["audit_read_model_ready"],
            source_to_decision_trace_ready=evidence["source_to_decision_trace_ready"],
            approval_required=True,
            approval_granted=False,
            auto_apply_allowed=False,
            canonical_truth_update_allowed=False,
            runtime_mutation_allowed=False,
            proposal_ready=True,
        ),
    )

    return RegulatoryUpdateApprovalRegistry(
        registry_id="regulatory_update_approval_registry_step_7_001",
        proposals=proposals,
        evidence_pack_ready=evidence["preview_ready"],
        approval_gate_required=True,
        approval_required=True,
        approval_granted=False,
        auto_apply_allowed=False,
        canonical_truth_update_allowed=False,
        runtime_mutation_allowed=False,
        direct_core_write_allowed=False,
        deployment_allowed_now=False,
        registry_ready=evidence["preview_ready"] is True,
    )
