from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


SourcePriorityTier = Literal[
    "constitutional_policy",
    "regulatory_source",
    "enterprise_policy",
    "canonical_project_memory",
    "evidence_pack",
    "history_ingestion",
    "project_notes",
    "subordinate_backend",
]


@dataclass(frozen=True, slots=True)
class MemorySourcePriorityEntry:
    source_id: str
    priority_tier: SourcePriorityTier
    priority_order: int
    source_bound: bool
    evidence_required: bool
    can_override_higher_priority: bool
    may_be_used_as_canonical_truth: bool
    source_ready: bool

    def __post_init__(self) -> None:
        if not self.source_id:
            raise ValueError("source_id must be non-empty")
        if self.priority_order < 1:
            raise ValueError("priority_order must be >= 1")
        if self.source_bound is not True:
            raise ValueError("source_bound must be True")
        if self.evidence_required is not True:
            raise ValueError("evidence_required must be True")
        if self.can_override_higher_priority:
            raise ValueError("can_override_higher_priority must be False")
        if self.priority_tier == "subordinate_backend" and self.may_be_used_as_canonical_truth:
            raise ValueError("subordinate_backend cannot be canonical truth")
        if self.source_ready is not True:
            raise ValueError("source_ready must be True")


@dataclass(frozen=True, slots=True)
class MemorySourcePriorityPolicy:
    policy_id: str
    entries: Tuple[MemorySourcePriorityEntry, ...]
    unique_priority_orders: bool
    subordinate_backend_lowest_priority: bool
    evidence_required_for_all_sources: bool
    no_source_can_override_higher_priority: bool
    source_priority_ready: bool

    def __post_init__(self) -> None:
        if not self.policy_id:
            raise ValueError("policy_id must be non-empty")
        if not self.entries:
            raise ValueError("entries must be non-empty")
        orders = [entry.priority_order for entry in self.entries]
        if len(set(orders)) != len(orders):
            raise ValueError("priority_order values must be unique")
        if not self.unique_priority_orders:
            raise ValueError("unique_priority_orders must be True")
        if not self.subordinate_backend_lowest_priority:
            raise ValueError("subordinate_backend_lowest_priority must be True")
        if not self.evidence_required_for_all_sources:
            raise ValueError("evidence_required_for_all_sources must be True")
        if not self.no_source_can_override_higher_priority:
            raise ValueError("no_source_can_override_higher_priority must be True")
        if not all(entry.source_ready for entry in self.entries):
            raise ValueError("all priority entries must be ready")
        if self.source_priority_ready is not True:
            raise ValueError("source_priority_ready must be True")


def build_memory_source_priority_policy() -> MemorySourcePriorityPolicy:
    entries = (
        MemorySourcePriorityEntry(
            source_id="source_constitutional_policy",
            priority_tier="constitutional_policy",
            priority_order=1,
            source_bound=True,
            evidence_required=True,
            can_override_higher_priority=False,
            may_be_used_as_canonical_truth=True,
            source_ready=True,
        ),
        MemorySourcePriorityEntry(
            source_id="source_regulatory_source",
            priority_tier="regulatory_source",
            priority_order=2,
            source_bound=True,
            evidence_required=True,
            can_override_higher_priority=False,
            may_be_used_as_canonical_truth=False,
            source_ready=True,
        ),
        MemorySourcePriorityEntry(
            source_id="source_enterprise_policy",
            priority_tier="enterprise_policy",
            priority_order=3,
            source_bound=True,
            evidence_required=True,
            can_override_higher_priority=False,
            may_be_used_as_canonical_truth=False,
            source_ready=True,
        ),
        MemorySourcePriorityEntry(
            source_id="source_canonical_project_memory",
            priority_tier="canonical_project_memory",
            priority_order=4,
            source_bound=True,
            evidence_required=True,
            can_override_higher_priority=False,
            may_be_used_as_canonical_truth=True,
            source_ready=True,
        ),
        MemorySourcePriorityEntry(
            source_id="source_evidence_pack",
            priority_tier="evidence_pack",
            priority_order=5,
            source_bound=True,
            evidence_required=True,
            can_override_higher_priority=False,
            may_be_used_as_canonical_truth=False,
            source_ready=True,
        ),
        MemorySourcePriorityEntry(
            source_id="source_history_ingestion",
            priority_tier="history_ingestion",
            priority_order=6,
            source_bound=True,
            evidence_required=True,
            can_override_higher_priority=False,
            may_be_used_as_canonical_truth=False,
            source_ready=True,
        ),
        MemorySourcePriorityEntry(
            source_id="source_project_notes",
            priority_tier="project_notes",
            priority_order=7,
            source_bound=True,
            evidence_required=True,
            can_override_higher_priority=False,
            may_be_used_as_canonical_truth=False,
            source_ready=True,
        ),
        MemorySourcePriorityEntry(
            source_id="source_subordinate_backend",
            priority_tier="subordinate_backend",
            priority_order=8,
            source_bound=True,
            evidence_required=True,
            can_override_higher_priority=False,
            may_be_used_as_canonical_truth=False,
            source_ready=True,
        ),
    )

    max_order = max(entry.priority_order for entry in entries)
    subordinate_order = next(entry.priority_order for entry in entries if entry.priority_tier == "subordinate_backend")

    return MemorySourcePriorityPolicy(
        policy_id="memory_source_priority_policy_001",
        entries=entries,
        unique_priority_orders=True,
        subordinate_backend_lowest_priority=subordinate_order == max_order,
        evidence_required_for_all_sources=all(entry.evidence_required for entry in entries),
        no_source_can_override_higher_priority=not any(entry.can_override_higher_priority for entry in entries),
        source_priority_ready=True,
    )
