from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_source_version_models import (
    build_regulatory_source_version_registry,
)


PrecedenceLevel = Literal["global_reference", "union", "country", "tenant_policy"]
PrecedenceDecision = Literal["applicable", "shadowed_by_higher_precedence", "draft_review_only"]


@dataclass(frozen=True, slots=True)
class EffectiveDatePrecedenceEntry:
    precedence_entry_id: str
    source_ref: str
    jurisdiction_id: str
    tenant_scope_id: str
    precedence_level: PrecedenceLevel
    precedence_rank: int
    effective_date: str
    decision: PrecedenceDecision
    source_version_present: bool
    effective_date_present: bool
    precedence_rank_valid: bool
    automatic_resolution_allowed: bool
    human_review_required: bool
    entry_ready: bool

    def __post_init__(self) -> None:
        if not self.precedence_entry_id:
            raise ValueError("precedence_entry_id must be non-empty")
        if not self.source_ref:
            raise ValueError("source_ref must be non-empty")
        if not self.jurisdiction_id:
            raise ValueError("jurisdiction_id must be non-empty")
        if not self.tenant_scope_id:
            raise ValueError("tenant_scope_id must be non-empty")
        if self.precedence_rank < 0:
            raise ValueError("precedence_rank must be >= 0")
        date.fromisoformat(self.effective_date)
        if self.source_version_present is not True:
            raise ValueError("source_version_present must be True")
        if self.effective_date_present is not True:
            raise ValueError("effective_date_present must be True")
        if self.precedence_rank_valid is not True:
            raise ValueError("precedence_rank_valid must be True")
        if self.automatic_resolution_allowed:
            raise ValueError("automatic_resolution_allowed must be False")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.entry_ready is not True:
            raise ValueError("entry_ready must be True")


@dataclass(frozen=True, slots=True)
class EffectiveDatePrecedenceMatrix:
    matrix_id: str
    entries: Tuple[EffectiveDatePrecedenceEntry, ...]
    source_registry_ready: bool
    source_version_required: bool
    effective_date_required: bool
    precedence_required: bool
    automatic_resolution_allowed: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool
    matrix_ready: bool

    def __post_init__(self) -> None:
        if not self.matrix_id:
            raise ValueError("matrix_id must be non-empty")
        if not self.entries:
            raise ValueError("entries must be non-empty")
        entry_ids = {entry.precedence_entry_id for entry in self.entries}
        if len(entry_ids) != len(self.entries):
            raise ValueError("precedence_entry_id values must be unique")
        if self.source_registry_ready is not True:
            raise ValueError("source_registry_ready must be True")
        if self.source_version_required is not True:
            raise ValueError("source_version_required must be True")
        if self.effective_date_required is not True:
            raise ValueError("effective_date_required must be True")
        if self.precedence_required is not True:
            raise ValueError("precedence_required must be True")
        if self.automatic_resolution_allowed:
            raise ValueError("automatic_resolution_allowed must be False")
        if self.canonical_truth_update_allowed:
            raise ValueError("canonical_truth_update_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not all(entry.entry_ready for entry in self.entries):
            raise ValueError("all precedence entries must be ready")
        if self.matrix_ready is not True:
            raise ValueError("matrix_ready must be True")


def _precedence_level_for_jurisdiction(jurisdiction_id: str) -> PrecedenceLevel:
    if jurisdiction_id == "jurisdiction_eu_union":
        return "union"
    if jurisdiction_id.endswith("_country"):
        return "country"
    if jurisdiction_id == "jurisdiction_global_reference":
        return "global_reference"
    return "tenant_policy"


def _rank_for_level(level: PrecedenceLevel) -> int:
    return {
        "global_reference": 10,
        "union": 30,
        "country": 40,
        "tenant_policy": 50,
    }[level]


def build_effective_date_precedence_matrix() -> EffectiveDatePrecedenceMatrix:
    registry = build_regulatory_source_version_registry()

    entries = tuple(
        EffectiveDatePrecedenceEntry(
            precedence_entry_id=f"precedence_{source.source_ref}",
            source_ref=source.source_ref,
            jurisdiction_id=source.jurisdiction_id,
            tenant_scope_id=source.tenant_scope_id,
            precedence_level=_precedence_level_for_jurisdiction(source.jurisdiction_id),
            precedence_rank=_rank_for_level(_precedence_level_for_jurisdiction(source.jurisdiction_id)),
            effective_date=source.effective_date,
            decision="draft_review_only" if source.source_status == "draft" else "applicable",
            source_version_present=bool(source.source_version),
            effective_date_present=bool(source.effective_date),
            precedence_rank_valid=True,
            automatic_resolution_allowed=False,
            human_review_required=True,
            entry_ready=True,
        )
        for source in registry.sources
    )

    return EffectiveDatePrecedenceMatrix(
        matrix_id="effective_date_precedence_matrix_step_4_001",
        entries=entries,
        source_registry_ready=registry.registry_ready,
        source_version_required=registry.source_version_required,
        effective_date_required=registry.effective_date_required,
        precedence_required=registry.precedence_required,
        automatic_resolution_allowed=False,
        canonical_truth_update_allowed=False,
        runtime_mutation_allowed=False,
        matrix_ready=registry.registry_ready,
    )
