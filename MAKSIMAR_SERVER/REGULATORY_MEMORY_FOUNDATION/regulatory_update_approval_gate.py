from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_update_approval_models import (
    build_regulatory_update_approval_registry,
)


@dataclass(frozen=True, slots=True)
class RegulatoryUpdateApprovalGate:
    gate_id: str
    proposal_ids: Tuple[str, ...]
    registry_ready: bool
    approval_gate_required: bool
    approval_required: bool
    approval_granted: bool
    proposal_only: bool
    diff_required: bool
    operator_review_required: bool
    auto_apply_allowed: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool
    direct_core_write_allowed: bool
    deployment_allowed_now: bool
    gate_ready: bool

    def __post_init__(self) -> None:
        if not self.gate_id:
            raise ValueError("gate_id must be non-empty")
        if not self.proposal_ids:
            raise ValueError("proposal_ids must be non-empty")
        if self.registry_ready is not True:
            raise ValueError("registry_ready must be True")
        if self.approval_gate_required is not True:
            raise ValueError("approval_gate_required must be True")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.approval_granted:
            raise ValueError("approval_granted must be False")
        if self.proposal_only is not True:
            raise ValueError("proposal_only must be True")
        if self.diff_required is not True:
            raise ValueError("diff_required must be True")
        if self.operator_review_required is not True:
            raise ValueError("operator_review_required must be True")
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
        if self.gate_ready is not True:
            raise ValueError("gate_ready must be True")


def build_regulatory_update_approval_gate() -> RegulatoryUpdateApprovalGate:
    registry = build_regulatory_update_approval_registry()

    return RegulatoryUpdateApprovalGate(
        gate_id="regulatory_update_approval_gate_step_7_001",
        proposal_ids=tuple(proposal.proposal_id for proposal in registry.proposals),
        registry_ready=registry.registry_ready,
        approval_gate_required=registry.approval_gate_required,
        approval_required=registry.approval_required,
        approval_granted=registry.approval_granted,
        proposal_only=True,
        diff_required=True,
        operator_review_required=True,
        auto_apply_allowed=registry.auto_apply_allowed,
        canonical_truth_update_allowed=registry.canonical_truth_update_allowed,
        runtime_mutation_allowed=registry.runtime_mutation_allowed,
        direct_core_write_allowed=registry.direct_core_write_allowed,
        deployment_allowed_now=registry.deployment_allowed_now,
        gate_ready=registry.registry_ready,
    )


def build_regulatory_update_approval_gate_preview() -> Dict[str, object]:
    gate = build_regulatory_update_approval_gate()

    return {
        "preview_id": "regulatory_update_approval_gate_preview_step_7_001",
        "preview_ready": gate.gate_ready,
        "gate_id": gate.gate_id,
        "proposal_ids": gate.proposal_ids,
        "proposal_count": len(gate.proposal_ids),
        "registry_ready": gate.registry_ready,
        "approval_gate_required": gate.approval_gate_required,
        "approval_required": gate.approval_required,
        "approval_granted": gate.approval_granted,
        "proposal_only": gate.proposal_only,
        "diff_required": gate.diff_required,
        "operator_review_required": gate.operator_review_required,
        "auto_apply_allowed": gate.auto_apply_allowed,
        "canonical_truth_update_allowed": gate.canonical_truth_update_allowed,
        "runtime_mutation_allowed": gate.runtime_mutation_allowed,
        "direct_core_write_allowed": gate.direct_core_write_allowed,
        "deployment_allowed_now": gate.deployment_allowed_now,
    }
