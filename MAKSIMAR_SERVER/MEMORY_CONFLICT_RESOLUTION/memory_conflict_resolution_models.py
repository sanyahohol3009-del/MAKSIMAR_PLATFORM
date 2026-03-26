from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.memory_policy import (
    MemoryFactClass,
)


MemoryConflictKind = Literal[
    "revision_conflict",
    "evidence_conflict",
]

MemoryResolutionStrategy = Literal[
    "promote_new_version",
    "keep_existing_record",
]

MemoryResolutionStatus = Literal[
    "resolved",
]


_MEMORY_TIER_ID_PATTERN = re.compile(r"^memory_[a-z][a-z0-9_]*$")
_EVENT_ID_PATTERN = re.compile(r"^event_[a-z][a-z0-9_]*$")
_RECORD_ID_PATTERN = re.compile(r"^memrec_[a-z][a-z0-9_]*$")
_ARCHIVE_ID_PATTERN = re.compile(r"^archive_[a-z][a-z0-9_]*$")
_CONFLICT_CASE_ID_PATTERN = re.compile(r"^conflict_[a-z][a-z0-9_]*$")
_CONFLICT_MARKER_ID_PATTERN = re.compile(r"^conflictmark_[a-z][a-z0-9_]*$")
_APPROVAL_TICKET_ID_PATTERN = re.compile(r"^approval_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class MemoryConflictResolutionEntry:
    """Canonical memory conflict resolution entry."""

    module_slug: str
    memory_tier_id: str
    conflict_case_id: str
    incoming_event_id: str
    existing_record_id: str
    fact_class: MemoryFactClass
    conflict_kind: MemoryConflictKind
    incoming_evidence_rank: int
    existing_evidence_rank: int
    proposal_generated: bool
    approval_required: bool
    approval_ticket_id: str
    approval_granted: bool
    conflict_marker_id: str
    version_incremented: bool
    resolution_strategy: MemoryResolutionStrategy
    resolution_status: MemoryResolutionStatus
    resolved_record_id: str
    archived_record_id: str
    description: str

    def __post_init__(self) -> None:
        """Validate memory conflict resolution invariants."""
        if not self.module_slug.strip():
            raise ValueError("module_slug must not be empty")

        if not _MEMORY_TIER_ID_PATTERN.fullmatch(self.memory_tier_id):
            raise ValueError(f"Invalid memory_tier_id: {self.memory_tier_id}")

        if not _CONFLICT_CASE_ID_PATTERN.fullmatch(self.conflict_case_id):
            raise ValueError(f"Invalid conflict_case_id: {self.conflict_case_id}")

        if not _EVENT_ID_PATTERN.fullmatch(self.incoming_event_id):
            raise ValueError(f"Invalid incoming_event_id: {self.incoming_event_id}")

        if not _RECORD_ID_PATTERN.fullmatch(self.existing_record_id):
            raise ValueError(f"Invalid existing_record_id: {self.existing_record_id}")

        if not _APPROVAL_TICKET_ID_PATTERN.fullmatch(self.approval_ticket_id):
            raise ValueError(f"Invalid approval_ticket_id: {self.approval_ticket_id}")

        if not _CONFLICT_MARKER_ID_PATTERN.fullmatch(self.conflict_marker_id):
            raise ValueError(f"Invalid conflict_marker_id: {self.conflict_marker_id}")

        if not _RECORD_ID_PATTERN.fullmatch(self.resolved_record_id):
            raise ValueError(f"Invalid resolved_record_id: {self.resolved_record_id}")

        if not _ARCHIVE_ID_PATTERN.fullmatch(self.archived_record_id):
            raise ValueError(f"Invalid archived_record_id: {self.archived_record_id}")

        if self.incoming_evidence_rank < 0:
            raise ValueError(
                f"incoming_evidence_rank must be non-negative: {self.conflict_case_id}"
            )

        if self.existing_evidence_rank < 0:
            raise ValueError(
                f"existing_evidence_rank must be non-negative: {self.conflict_case_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.conflict_case_id}"
            )

        if not self.proposal_generated:
            raise ValueError(
                f"conflict resolution must generate proposal: {self.conflict_case_id}"
            )

        if not self.approval_required:
            raise ValueError(
                f"conflict resolution must require approval: {self.conflict_case_id}"
            )

        if not self.approval_granted:
            raise ValueError(
                f"conflict resolution must record granted approval: {self.conflict_case_id}"
            )

        if self.resolution_status != "resolved":
            raise ValueError(
                f"memory conflict resolution entry must be resolved: {self.conflict_case_id}"
            )

        if self.resolution_strategy == "promote_new_version":
            if self.incoming_evidence_rank <= self.existing_evidence_rank:
                raise ValueError(
                    f"promote_new_version requires stronger incoming evidence: {self.conflict_case_id}"
                )
            if not self.version_incremented:
                raise ValueError(
                    f"promote_new_version must increment version: {self.conflict_case_id}"
                )
            if self.resolved_record_id == self.existing_record_id:
                raise ValueError(
                    f"promote_new_version must produce new record id: {self.conflict_case_id}"
                )

        if self.resolution_strategy == "keep_existing_record":
            if self.incoming_evidence_rank > self.existing_evidence_rank:
                raise ValueError(
                    f"keep_existing_record must not discard stronger evidence: {self.conflict_case_id}"
                )
            if self.version_incremented:
                raise ValueError(
                    f"keep_existing_record must not increment version: {self.conflict_case_id}"
                )
            if self.resolved_record_id != self.existing_record_id:
                raise ValueError(
                    f"keep_existing_record must keep existing record id: {self.conflict_case_id}"
                )


@dataclass(frozen=True, slots=True)
class MemoryConflictResolutionContract:
    """Unified memory conflict resolution contract."""

    total_entries: int
    promote_new_version_entries: int
    keep_existing_entries: int
    approval_required_entries: int
    entries: tuple[MemoryConflictResolutionEntry, ...]

    def __post_init__(self) -> None:
        """Validate memory conflict resolution contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        promote_new_version_entries = sum(
            1
            for entry in self.entries
            if entry.resolution_strategy == "promote_new_version"
        )
        keep_existing_entries = sum(
            1
            for entry in self.entries
            if entry.resolution_strategy == "keep_existing_record"
        )
        approval_required_entries = sum(
            1 for entry in self.entries if entry.approval_required
        )

        if self.promote_new_version_entries != promote_new_version_entries:
            raise ValueError(
                "promote_new_version_entries must match computed count"
            )

        if self.keep_existing_entries != keep_existing_entries:
            raise ValueError("keep_existing_entries must match computed count")

        if self.approval_required_entries != approval_required_entries:
            raise ValueError("approval_required_entries must match computed count")

        conflict_case_ids = tuple(entry.conflict_case_id for entry in self.entries)
        incoming_event_ids = tuple(entry.incoming_event_id for entry in self.entries)
        conflict_marker_ids = tuple(entry.conflict_marker_id for entry in self.entries)
        approval_ticket_ids = tuple(entry.approval_ticket_id for entry in self.entries)

        if len(set(conflict_case_ids)) != len(conflict_case_ids):
            raise ValueError("Duplicate conflict_case_id values detected")

        if len(set(incoming_event_ids)) != len(incoming_event_ids):
            raise ValueError("Duplicate incoming_event_id values detected")

        if len(set(conflict_marker_ids)) != len(conflict_marker_ids):
            raise ValueError("Duplicate conflict_marker_id values detected")

        if len(set(approval_ticket_ids)) != len(approval_ticket_ids):
            raise ValueError("Duplicate approval_ticket_id values detected")
