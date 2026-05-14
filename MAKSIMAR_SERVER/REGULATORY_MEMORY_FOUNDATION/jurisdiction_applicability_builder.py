from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.country_jurisdiction_binding import (
    build_country_jurisdiction_binding_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.jurisdiction_registry_models import (
    build_jurisdiction_registry,
)


@dataclass(frozen=True, slots=True)
class JurisdictionApplicabilityMatrix:
    matrix_id: str
    jurisdiction_ids: Tuple[str, ...]
    applicability_pairs: Tuple[Tuple[str, str], ...]
    country_jurisdiction_binding_ready: bool
    applicability_scope_required: bool
    source_bound_required: bool
    version_required: bool
    effective_date_required: bool
    cross_jurisdiction_merge_allowed: bool
    applicability_matrix_ready: bool

    def __post_init__(self) -> None:
        if not self.matrix_id:
            raise ValueError("matrix_id must be non-empty")
        if not self.jurisdiction_ids:
            raise ValueError("jurisdiction_ids must be non-empty")
        if not self.applicability_pairs:
            raise ValueError("applicability_pairs must be non-empty")
        if self.country_jurisdiction_binding_ready is not True:
            raise ValueError("country_jurisdiction_binding_ready must be True")
        if self.applicability_scope_required is not True:
            raise ValueError("applicability_scope_required must be True")
        if self.source_bound_required is not True:
            raise ValueError("source_bound_required must be True")
        if self.version_required is not True:
            raise ValueError("version_required must be True")
        if self.effective_date_required is not True:
            raise ValueError("effective_date_required must be True")
        if self.cross_jurisdiction_merge_allowed:
            raise ValueError("cross_jurisdiction_merge_allowed must be False")
        if self.applicability_matrix_ready is not True:
            raise ValueError("applicability_matrix_ready must be True")


def build_jurisdiction_applicability_matrix() -> JurisdictionApplicabilityMatrix:
    binding = build_country_jurisdiction_binding_preview()
    registry = build_jurisdiction_registry()

    applicability_pairs = tuple(
        (entry.jurisdiction_id, scope)
        for entry in registry.entries
        for scope in entry.applicability_scopes
    )

    return JurisdictionApplicabilityMatrix(
        matrix_id="jurisdiction_applicability_matrix_step_2_001",
        jurisdiction_ids=tuple(entry.jurisdiction_id for entry in registry.entries),
        applicability_pairs=applicability_pairs,
        country_jurisdiction_binding_ready=binding["preview_ready"],
        applicability_scope_required=registry.applicability_scope_required,
        source_bound_required=registry.source_bound_required,
        version_required=True,
        effective_date_required=True,
        cross_jurisdiction_merge_allowed=registry.cross_jurisdiction_merge_allowed,
        applicability_matrix_ready=binding["preview_ready"] is True and registry.registry_ready,
    )


def build_jurisdiction_applicability_preview() -> Dict[str, object]:
    matrix = build_jurisdiction_applicability_matrix()

    return {
        "preview_id": "jurisdiction_applicability_preview_step_2_001",
        "preview_ready": matrix.applicability_matrix_ready,
        "matrix_id": matrix.matrix_id,
        "jurisdiction_ids": matrix.jurisdiction_ids,
        "applicability_pairs": matrix.applicability_pairs,
        "jurisdiction_count": len(matrix.jurisdiction_ids),
        "applicability_pair_count": len(matrix.applicability_pairs),
        "applicability_scope_required": matrix.applicability_scope_required,
        "source_bound_required": matrix.source_bound_required,
        "version_required": matrix.version_required,
        "effective_date_required": matrix.effective_date_required,
        "cross_jurisdiction_merge_allowed": matrix.cross_jurisdiction_merge_allowed,
    }
