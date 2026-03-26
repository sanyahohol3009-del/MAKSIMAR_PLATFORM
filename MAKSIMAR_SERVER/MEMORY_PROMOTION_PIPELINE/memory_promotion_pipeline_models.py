from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.memory_policy import (
    MemoryFactClass,
)


MemoryPromotionDisposition = Literal[
    "promoted",
    "archived",
]

MemoryArchiveReason = Literal[
    "",
    "duplicate_candidate",
    "conflict_detected",
]

MemoryLanguageCode = Literal[
    "en",
    "ru",
    "uk",
    "de",
]


_MEMORY_TIER_ID_PATTERN = re.compile(r"^memory_[a-z][a-z0-9_]*$")
_EVENT_ID_PATTERN = re.compile(r"^event_[a-z][a-z0-9_]*$")
_PROMOTED_RECORD_ID_PATTERN = re.compile(r"^memrec_[a-z][a-z0-9_]*$")
_ARCHIVED_RECORD_ID_PATTERN = re.compile(r"^archive_[a-z][a-z0-9_]*$")
_PROVENANCE_REF_PATTERN = re.compile(r"^prov_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class MemoryPromotionPipelineEntry:
    """Canonical memory promotion pipeline entry."""

    module_slug: str
    memory_tier_id: str
    input_event_id: str
    fact_class: MemoryFactClass
    language_code: MemoryLanguageCode
    script_name: str
    provenance_ref: str
    classification_passed: bool
    summarization_performed: bool
    evidence_bound: bool
    deduplication_passed: bool
    conflict_check_performed: bool
    conflict_check_passed: bool
    final_disposition: MemoryPromotionDisposition
    archive_reason: MemoryArchiveReason
    promoted_record_id: str
    archived_record_id: str
    description: str

    def __post_init__(self) -> None:
        """Validate memory promotion pipeline invariants."""
        if not self.module_slug.strip():
            raise ValueError("module_slug must not be empty")

        if not _MEMORY_TIER_ID_PATTERN.fullmatch(self.memory_tier_id):
            raise ValueError(f"Invalid memory_tier_id: {self.memory_tier_id}")

        if not _EVENT_ID_PATTERN.fullmatch(self.input_event_id):
            raise ValueError(f"Invalid input_event_id: {self.input_event_id}")

        if not _PROVENANCE_REF_PATTERN.fullmatch(self.provenance_ref):
            raise ValueError(f"Invalid provenance_ref: {self.provenance_ref}")

        if not self.script_name.strip():
            raise ValueError(f"script_name must not be empty for {self.input_event_id}")

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.input_event_id}"
            )

        if not self.classification_passed:
            raise ValueError(
                f"memory promotion entry must pass classification: {self.input_event_id}"
            )

        if not self.summarization_performed:
            raise ValueError(
                f"memory promotion entry must perform summarization: {self.input_event_id}"
            )

        if not self.evidence_bound:
            raise ValueError(
                f"memory promotion entry must bind evidence: {self.input_event_id}"
            )

        if self.final_disposition == "promoted":
            if not self.deduplication_passed:
                raise ValueError(
                    f"promoted entry must pass deduplication: {self.input_event_id}"
                )
            if not self.conflict_check_performed:
                raise ValueError(
                    f"promoted entry must perform conflict check: {self.input_event_id}"
                )
            if not self.conflict_check_passed:
                raise ValueError(
                    f"promoted entry must pass conflict check: {self.input_event_id}"
                )
            if self.archive_reason != "":
                raise ValueError(
                    f"promoted entry must not define archive_reason: {self.input_event_id}"
                )
            if not _PROMOTED_RECORD_ID_PATTERN.fullmatch(self.promoted_record_id):
                raise ValueError(
                    f"promoted entry must define valid promoted_record_id: {self.input_event_id}"
                )
            if self.archived_record_id != "":
                raise ValueError(
                    f"promoted entry must not define archived_record_id: {self.input_event_id}"
                )

        if self.final_disposition == "archived":
            if self.promoted_record_id != "":
                raise ValueError(
                    f"archived entry must not define promoted_record_id: {self.input_event_id}"
                )
            if not _ARCHIVED_RECORD_ID_PATTERN.fullmatch(self.archived_record_id):
                raise ValueError(
                    f"archived entry must define valid archived_record_id: {self.input_event_id}"
                )
            if self.archive_reason == "":
                raise ValueError(
                    f"archived entry must define archive_reason: {self.input_event_id}"
                )

            if self.archive_reason == "duplicate_candidate":
                if self.deduplication_passed:
                    raise ValueError(
                        f"duplicate_candidate archive must fail deduplication: {self.input_event_id}"
                    )
                if self.conflict_check_performed:
                    raise ValueError(
                        f"duplicate_candidate archive must not perform conflict check: {self.input_event_id}"
                    )
                if self.conflict_check_passed:
                    raise ValueError(
                        f"duplicate_candidate archive must not pass conflict check: {self.input_event_id}"
                    )

            if self.archive_reason == "conflict_detected":
                if not self.deduplication_passed:
                    raise ValueError(
                        f"conflict_detected archive must pass deduplication: {self.input_event_id}"
                    )
                if not self.conflict_check_performed:
                    raise ValueError(
                        f"conflict_detected archive must perform conflict check: {self.input_event_id}"
                    )
                if self.conflict_check_passed:
                    raise ValueError(
                        f"conflict_detected archive must fail conflict check: {self.input_event_id}"
                    )


@dataclass(frozen=True, slots=True)
class MemoryPromotionPipelineContract:
    """Unified memory promotion pipeline contract."""

    total_entries: int
    promoted_entries: int
    archived_entries: int
    evidence_bound_entries: int
    entries: tuple[MemoryPromotionPipelineEntry, ...]

    def __post_init__(self) -> None:
        """Validate memory promotion pipeline contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        promoted_entries = sum(
            1 for entry in self.entries if entry.final_disposition == "promoted"
        )
        archived_entries = sum(
            1 for entry in self.entries if entry.final_disposition == "archived"
        )
        evidence_bound_entries = sum(
            1 for entry in self.entries if entry.evidence_bound
        )

        if self.promoted_entries != promoted_entries:
            raise ValueError("promoted_entries must match computed count")

        if self.archived_entries != archived_entries:
            raise ValueError("archived_entries must match computed count")

        if self.evidence_bound_entries != evidence_bound_entries:
            raise ValueError("evidence_bound_entries must match computed count")

        input_event_ids = tuple(entry.input_event_id for entry in self.entries)
        provenance_refs = tuple(entry.provenance_ref for entry in self.entries)

        if len(set(input_event_ids)) != len(input_event_ids):
            raise ValueError("Duplicate input_event_id values detected")

        if len(set(provenance_refs)) != len(provenance_refs):
            raise ValueError("Duplicate provenance_ref values detected")
