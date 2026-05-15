from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_source_version_models import (
    build_regulatory_source_version_registry,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.source_version_precedence_preview_builder import (
    build_source_version_precedence_preview,
)


RegulatoryConflictKind = Literal[
    "jurisdiction_overlap",
    "effective_date_overlap",
    "source_status_conflict",
    "precedence_conflict",
    "draft_vs_active_conflict",
]

RegulatoryConflictSeverity = Literal["low", "medium", "high", "critical"]


@dataclass(frozen=True, slots=True)
class RegulatoryConflictCandidate:
    candidate_id: str
    conflict_kind: RegulatoryConflictKind
    severity: RegulatoryConflictSeverity
    source_refs: Tuple[str, ...]
    tenant_id: str
    jurisdiction_ids: Tuple[str, ...]
    source_version_present: bool
    effective_date_present: bool
    precedence_present: bool
    human_review_required: bool
    automatic_resolution_allowed: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool
    candidate_ready: bool

    def __post_init__(self) -> None:
        if not self.candidate_id:
            raise ValueError("candidate_id must be non-empty")
        if not self.source_refs:
            raise ValueError("source_refs must be non-empty")
        if not self.tenant_id:
            raise ValueError("tenant_id must be non-empty")
        if not self.jurisdiction_ids:
            raise ValueError("jurisdiction_ids must be non-empty")
        if self.source_version_present is not True:
            raise ValueError("source_version_present must be True")
        if self.effective_date_present is not True:
            raise ValueError("effective_date_present must be True")
        if self.precedence_present is not True:
            raise ValueError("precedence_present must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.automatic_resolution_allowed:
            raise ValueError("automatic_resolution_allowed must be False")
        if self.canonical_truth_update_allowed:
            raise ValueError("canonical_truth_update_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.candidate_ready is not True:
            raise ValueError("candidate_ready must be True")


@dataclass(frozen=True, slots=True)
class RegulatoryConflictRegistry:
    registry_id: str
    candidates: Tuple[RegulatoryConflictCandidate, ...]
    source_version_precedence_ready: bool
    conflict_detection_ready: bool
    human_review_required: bool
    automatic_resolution_allowed: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool
    direct_core_write_allowed: bool
    deployment_allowed_now: bool

    def __post_init__(self) -> None:
        if not self.registry_id:
            raise ValueError("registry_id must be non-empty")
        if not self.candidates:
            raise ValueError("candidates must be non-empty")
        candidate_ids = {candidate.candidate_id for candidate in self.candidates}
        if len(candidate_ids) != len(self.candidates):
            raise ValueError("candidate_id values must be unique")
        if self.source_version_precedence_ready is not True:
            raise ValueError("source_version_precedence_ready must be True")
        if self.conflict_detection_ready is not True:
            raise ValueError("conflict_detection_ready must be True")
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
        if not all(candidate.candidate_ready for candidate in self.candidates):
            raise ValueError("all conflict candidates must be ready")


def build_regulatory_conflict_registry() -> RegulatoryConflictRegistry:
    source_registry = build_regulatory_source_version_registry()
    precedence = build_source_version_precedence_preview()

    de_tenant_sources = tuple(
        source for source in source_registry.sources if source.tenant_id == "tenant_demo_de_001"
    )
    draft_sources = tuple(
        source for source in source_registry.sources if source.source_status == "draft"
    )

    candidates = (
        RegulatoryConflictCandidate(
            candidate_id="regulatory_conflict_de_eu_overlap_001",
            conflict_kind="jurisdiction_overlap",
            severity="medium",
            source_refs=tuple(source.source_ref for source in de_tenant_sources),
            tenant_id="tenant_demo_de_001",
            jurisdiction_ids=tuple(source.jurisdiction_id for source in de_tenant_sources),
            source_version_present=True,
            effective_date_present=True,
            precedence_present=True,
            human_review_required=True,
            automatic_resolution_allowed=False,
            canonical_truth_update_allowed=False,
            runtime_mutation_allowed=False,
            candidate_ready=True,
        ),
        RegulatoryConflictCandidate(
            candidate_id="regulatory_conflict_draft_review_ua_001",
            conflict_kind="draft_vs_active_conflict",
            severity="low",
            source_refs=tuple(source.source_ref for source in draft_sources),
            tenant_id="tenant_demo_ua_001",
            jurisdiction_ids=tuple(source.jurisdiction_id for source in draft_sources),
            source_version_present=True,
            effective_date_present=True,
            precedence_present=True,
            human_review_required=True,
            automatic_resolution_allowed=False,
            canonical_truth_update_allowed=False,
            runtime_mutation_allowed=False,
            candidate_ready=True,
        ),
    )

    return RegulatoryConflictRegistry(
        registry_id="regulatory_conflict_registry_step_5_001",
        candidates=candidates,
        source_version_precedence_ready=precedence["preview_ready"],
        conflict_detection_ready=precedence["preview_ready"] is True,
        human_review_required=True,
        automatic_resolution_allowed=False,
        canonical_truth_update_allowed=False,
        runtime_mutation_allowed=False,
        direct_core_write_allowed=False,
        deployment_allowed_now=False,
    )
