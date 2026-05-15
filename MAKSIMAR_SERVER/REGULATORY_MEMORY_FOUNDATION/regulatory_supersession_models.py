from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_drift_detector import (
    build_regulatory_drift_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_source_version_models import (
    build_regulatory_source_version_registry,
)


@dataclass(frozen=True, slots=True)
class RegulatorySupersessionCandidate:
    candidate_id: str
    superseding_source_ref: str
    current_source_ref: str
    tenant_id: str
    jurisdiction_id: str
    source_version_present: bool
    effective_date_present: bool
    approval_required: bool
    human_review_required: bool
    supersession_applied: bool
    automatic_resolution_allowed: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool
    candidate_ready: bool

    def __post_init__(self) -> None:
        if not self.candidate_id:
            raise ValueError("candidate_id must be non-empty")
        if not self.superseding_source_ref:
            raise ValueError("superseding_source_ref must be non-empty")
        if not self.current_source_ref:
            raise ValueError("current_source_ref must be non-empty")
        if not self.tenant_id:
            raise ValueError("tenant_id must be non-empty")
        if not self.jurisdiction_id:
            raise ValueError("jurisdiction_id must be non-empty")
        if self.source_version_present is not True:
            raise ValueError("source_version_present must be True")
        if self.effective_date_present is not True:
            raise ValueError("effective_date_present must be True")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.supersession_applied:
            raise ValueError("supersession_applied must be False")
        if self.automatic_resolution_allowed:
            raise ValueError("automatic_resolution_allowed must be False")
        if self.canonical_truth_update_allowed:
            raise ValueError("canonical_truth_update_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.candidate_ready is not True:
            raise ValueError("candidate_ready must be True")


@dataclass(frozen=True, slots=True)
class RegulatorySupersessionRegistry:
    registry_id: str
    candidates: Tuple[RegulatorySupersessionCandidate, ...]
    drift_detection_ready: bool
    supersession_registry_ready: bool
    approval_required: bool
    human_review_required: bool
    supersession_applied: bool
    automatic_resolution_allowed: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        if not self.registry_id:
            raise ValueError("registry_id must be non-empty")
        if not self.candidates:
            raise ValueError("candidates must be non-empty")
        candidate_ids = {candidate.candidate_id for candidate in self.candidates}
        if len(candidate_ids) != len(self.candidates):
            raise ValueError("candidate_id values must be unique")
        if self.drift_detection_ready is not True:
            raise ValueError("drift_detection_ready must be True")
        if self.supersession_registry_ready is not True:
            raise ValueError("supersession_registry_ready must be True")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.supersession_applied:
            raise ValueError("supersession_applied must be False")
        if self.automatic_resolution_allowed:
            raise ValueError("automatic_resolution_allowed must be False")
        if self.canonical_truth_update_allowed:
            raise ValueError("canonical_truth_update_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not all(candidate.candidate_ready for candidate in self.candidates):
            raise ValueError("all supersession candidates must be ready")


def build_regulatory_supersession_registry() -> RegulatorySupersessionRegistry:
    drift = build_regulatory_drift_preview()
    source_registry = build_regulatory_source_version_registry()

    draft_source = next(source for source in source_registry.sources if source.source_status == "draft")

    candidates = (
        RegulatorySupersessionCandidate(
            candidate_id="regulatory_supersession_candidate_ua_policy_001",
            superseding_source_ref=draft_source.source_ref,
            current_source_ref="manual_review_required_before_supersession",
            tenant_id=draft_source.tenant_id,
            jurisdiction_id=draft_source.jurisdiction_id,
            source_version_present=True,
            effective_date_present=True,
            approval_required=True,
            human_review_required=True,
            supersession_applied=False,
            automatic_resolution_allowed=False,
            canonical_truth_update_allowed=False,
            runtime_mutation_allowed=False,
            candidate_ready=True,
        ),
    )

    return RegulatorySupersessionRegistry(
        registry_id="regulatory_supersession_registry_step_5_001",
        candidates=candidates,
        drift_detection_ready=drift["preview_ready"],
        supersession_registry_ready=drift["preview_ready"] is True,
        approval_required=True,
        human_review_required=True,
        supersession_applied=False,
        automatic_resolution_allowed=False,
        canonical_truth_update_allowed=False,
        runtime_mutation_allowed=False,
    )


def build_regulatory_supersession_preview() -> Dict[str, object]:
    registry = build_regulatory_supersession_registry()

    return {
        "preview_id": "regulatory_supersession_preview_step_5_001",
        "preview_ready": registry.supersession_registry_ready,
        "registry_id": registry.registry_id,
        "candidate_count": len(registry.candidates),
        "candidate_ids": tuple(candidate.candidate_id for candidate in registry.candidates),
        "drift_detection_ready": registry.drift_detection_ready,
        "approval_required": registry.approval_required,
        "human_review_required": registry.human_review_required,
        "supersession_applied": registry.supersession_applied,
        "automatic_resolution_allowed": registry.automatic_resolution_allowed,
        "canonical_truth_update_allowed": registry.canonical_truth_update_allowed,
        "runtime_mutation_allowed": registry.runtime_mutation_allowed,
    }
