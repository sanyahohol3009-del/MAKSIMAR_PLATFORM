from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.effective_date_precedence_models import (
    build_effective_date_precedence_matrix,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_source_version_models import (
    build_regulatory_source_version_registry,
)


@dataclass(frozen=True, slots=True)
class LegalPrecedenceResolverResult:
    resolver_id: str
    applicable_source_refs: Tuple[str, ...]
    draft_review_source_refs: Tuple[str, ...]
    source_count: int
    precedence_entry_count: int
    source_version_required: bool
    effective_date_required: bool
    precedence_required: bool
    human_review_required: bool
    automatic_resolution_allowed: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool
    resolver_ready: bool

    def __post_init__(self) -> None:
        if not self.resolver_id:
            raise ValueError("resolver_id must be non-empty")
        if self.source_count <= 0:
            raise ValueError("source_count must be > 0")
        if self.precedence_entry_count <= 0:
            raise ValueError("precedence_entry_count must be > 0")
        if self.source_version_required is not True:
            raise ValueError("source_version_required must be True")
        if self.effective_date_required is not True:
            raise ValueError("effective_date_required must be True")
        if self.precedence_required is not True:
            raise ValueError("precedence_required must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.automatic_resolution_allowed:
            raise ValueError("automatic_resolution_allowed must be False")
        if self.canonical_truth_update_allowed:
            raise ValueError("canonical_truth_update_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.resolver_ready is not True:
            raise ValueError("resolver_ready must be True")


def build_legal_precedence_resolver_result() -> LegalPrecedenceResolverResult:
    registry = build_regulatory_source_version_registry()
    matrix = build_effective_date_precedence_matrix()

    applicable = tuple(
        entry.source_ref for entry in matrix.entries if entry.decision == "applicable"
    )
    draft_review = tuple(
        entry.source_ref for entry in matrix.entries if entry.decision == "draft_review_only"
    )

    return LegalPrecedenceResolverResult(
        resolver_id="legal_precedence_resolver_result_step_4_001",
        applicable_source_refs=applicable,
        draft_review_source_refs=draft_review,
        source_count=len(registry.sources),
        precedence_entry_count=len(matrix.entries),
        source_version_required=registry.source_version_required,
        effective_date_required=registry.effective_date_required,
        precedence_required=registry.precedence_required,
        human_review_required=True,
        automatic_resolution_allowed=matrix.automatic_resolution_allowed,
        canonical_truth_update_allowed=matrix.canonical_truth_update_allowed,
        runtime_mutation_allowed=matrix.runtime_mutation_allowed,
        resolver_ready=registry.registry_ready and matrix.matrix_ready,
    )


def build_legal_precedence_resolver_preview() -> Dict[str, object]:
    result = build_legal_precedence_resolver_result()

    return {
        "preview_id": "legal_precedence_resolver_preview_step_4_001",
        "preview_ready": result.resolver_ready,
        "resolver_id": result.resolver_id,
        "applicable_source_refs": result.applicable_source_refs,
        "draft_review_source_refs": result.draft_review_source_refs,
        "source_count": result.source_count,
        "precedence_entry_count": result.precedence_entry_count,
        "source_version_required": result.source_version_required,
        "effective_date_required": result.effective_date_required,
        "precedence_required": result.precedence_required,
        "human_review_required": result.human_review_required,
        "automatic_resolution_allowed": result.automatic_resolution_allowed,
        "canonical_truth_update_allowed": result.canonical_truth_update_allowed,
        "runtime_mutation_allowed": result.runtime_mutation_allowed,
    }
