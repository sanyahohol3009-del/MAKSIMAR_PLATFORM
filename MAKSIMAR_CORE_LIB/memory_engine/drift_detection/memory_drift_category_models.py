from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True, slots=True)
class MemoryDriftCategory:
    category_id: str
    label: str
    description: str
    human_review_required: bool
    auto_resolution_allowed: bool
    canonical_truth_change_allowed: bool
    category_ready: bool

    def __post_init__(self) -> None:
        if not self.category_id:
            raise ValueError("category_id must be non-empty")
        if not self.label:
            raise ValueError("label must be non-empty")
        if not self.description:
            raise ValueError("description must be non-empty")
        if not self.human_review_required:
            raise ValueError("human_review_required must be True")
        if self.auto_resolution_allowed:
            raise ValueError("auto_resolution_allowed must be False")
        if self.canonical_truth_change_allowed:
            raise ValueError("canonical_truth_change_allowed must be False")
        if not self.category_ready:
            raise ValueError("category_ready must be True")


def build_memory_drift_categories() -> Tuple[MemoryDriftCategory, ...]:
    return (
        MemoryDriftCategory(
            category_id="semantic_conflict",
            label="Semantic conflict",
            description="Two memories appear to describe incompatible meaning.",
            human_review_required=True,
            auto_resolution_allowed=False,
            canonical_truth_change_allowed=False,
            category_ready=True,
        ),
        MemoryDriftCategory(
            category_id="source_date_conflict",
            label="Source date conflict",
            description="A newer source may supersede an older memory, but truth is not changed automatically.",
            human_review_required=True,
            auto_resolution_allowed=False,
            canonical_truth_change_allowed=False,
            category_ready=True,
        ),
        MemoryDriftCategory(
            category_id="jurisdiction_conflict",
            label="Jurisdiction conflict",
            description="Memory may be valid only for a specific country, tenant, or legal scope.",
            human_review_required=True,
            auto_resolution_allowed=False,
            canonical_truth_change_allowed=False,
            category_ready=True,
        ),
        MemoryDriftCategory(
            category_id="scope_conflict",
            label="Scope conflict",
            description="Implementation scope may differ from roadmap scope.",
            human_review_required=True,
            auto_resolution_allowed=False,
            canonical_truth_change_allowed=False,
            category_ready=True,
        ),
        MemoryDriftCategory(
            category_id="artifact_version_conflict",
            label="Artifact version conflict",
            description="A newer artifact version may conflict with an earlier artifact reference.",
            human_review_required=True,
            auto_resolution_allowed=False,
            canonical_truth_change_allowed=False,
            category_ready=True,
        ),
    )
