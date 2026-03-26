from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_SERVER.MEMORY_REGISTRY import (
    build_memory_registry_contract,
)


MemoryFactClass = Literal[
    "architecture_decision",
    "platform_invariant",
    "roadmap_checkpoint",
]

MemoryApprovalMode = Literal[
    "mandatory_human_approval",
]

MemorySummarizationMode = Literal[
    "summary_required",
]

MemoryDeduplicationMode = Literal[
    "deduplicate_before_write",
]

MemoryConflictMode = Literal[
    "conflict_check_required",
]

MemoryLanguagePolicy = Literal[
    "language_metadata_required",
]

MemoryScriptPolicy = Literal[
    "script_metadata_required",
]

MemoryProvenancePolicy = Literal[
    "provenance_required",
]


@dataclass(frozen=True, slots=True)
class MemoryClassificationPolicyEntry:
    """Canonical memory classification policy entry."""

    module_slug: str
    memory_tier_id: str
    retention_class: str
    accepted_fact_classes: tuple[MemoryFactClass, ...]
    approval_mode: MemoryApprovalMode
    summarization_mode: MemorySummarizationMode
    deduplication_mode: MemoryDeduplicationMode
    conflict_mode: MemoryConflictMode
    language_policy: MemoryLanguagePolicy
    script_policy: MemoryScriptPolicy
    provenance_policy: MemoryProvenancePolicy
    evidence_required: bool
    active: bool
    description: str

    def __post_init__(self) -> None:
        """Validate memory classification policy invariants."""
        if not self.module_slug.strip():
            raise ValueError("module_slug must not be empty")

        if not self.memory_tier_id.strip():
            raise ValueError(
                f"memory_tier_id must not be empty for {self.module_slug}"
            )

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.module_slug}")

        if not self.accepted_fact_classes:
            raise ValueError(
                f"accepted_fact_classes must not be empty for {self.module_slug}"
            )

        if len(set(self.accepted_fact_classes)) != len(self.accepted_fact_classes):
            raise ValueError(
                f"Duplicate accepted_fact_classes detected for {self.module_slug}"
            )

        if not self.active:
            raise ValueError(
                f"inactive memory tier must not appear in classification policy: {self.module_slug}"
            )

        if not self.evidence_required:
            raise ValueError(
                f"memory classification policy must require evidence: {self.module_slug}"
            )

        if self.retention_class == "foundational":
            expected_fact_classes = (
                "architecture_decision",
                "platform_invariant",
                "roadmap_checkpoint",
            )
            if self.accepted_fact_classes != expected_fact_classes:
                raise ValueError(
                    f"foundational memory tier must use canonical fact classes: {self.module_slug}"
                )

            if self.approval_mode != "mandatory_human_approval":
                raise ValueError(
                    f"foundational memory tier must require mandatory_human_approval: {self.module_slug}"
                )

            if self.summarization_mode != "summary_required":
                raise ValueError(
                    f"foundational memory tier must require summary_required: {self.module_slug}"
                )

            if self.deduplication_mode != "deduplicate_before_write":
                raise ValueError(
                    f"foundational memory tier must require deduplicate_before_write: {self.module_slug}"
                )

            if self.conflict_mode != "conflict_check_required":
                raise ValueError(
                    f"foundational memory tier must require conflict_check_required: {self.module_slug}"
                )

            if self.language_policy != "language_metadata_required":
                raise ValueError(
                    f"foundational memory tier must require language metadata: {self.module_slug}"
                )

            if self.script_policy != "script_metadata_required":
                raise ValueError(
                    f"foundational memory tier must require script metadata: {self.module_slug}"
                )

            if self.provenance_policy != "provenance_required":
                raise ValueError(
                    f"foundational memory tier must require provenance: {self.module_slug}"
                )


@dataclass(frozen=True, slots=True)
class MemoryClassificationPolicyContract:
    """Unified memory classification policy contract."""

    total_entries: int
    active_entries: int
    foundational_entries: int
    approval_required_entries: int
    entries: tuple[MemoryClassificationPolicyEntry, ...]

    def __post_init__(self) -> None:
        """Validate memory classification policy contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        active_entries = sum(1 for entry in self.entries if entry.active)
        foundational_entries = sum(
            1 for entry in self.entries if entry.retention_class == "foundational"
        )
        approval_required_entries = sum(
            1
            for entry in self.entries
            if entry.approval_mode == "mandatory_human_approval"
        )

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        if self.foundational_entries != foundational_entries:
            raise ValueError("foundational_entries must match computed count")

        if self.approval_required_entries != approval_required_entries:
            raise ValueError("approval_required_entries must match computed count")

        memory_tier_ids = tuple(entry.memory_tier_id for entry in self.entries)
        if len(set(memory_tier_ids)) != len(memory_tier_ids):
            raise ValueError(
                "Duplicate memory_tier_id values detected in classification policy"
            )


def build_memory_classification_policy_contract() -> MemoryClassificationPolicyContract:
    """Build canonical memory classification policy contract."""
    memory_registry = build_memory_registry_contract()

    entries = []
    for registry_entry in memory_registry.entries:
        entries.append(
            MemoryClassificationPolicyEntry(
                module_slug=registry_entry.module_slug,
                memory_tier_id=registry_entry.memory_tier_id,
                retention_class=registry_entry.retention_class,
                accepted_fact_classes=(
                    "architecture_decision",
                    "platform_invariant",
                    "roadmap_checkpoint",
                ),
                approval_mode="mandatory_human_approval",
                summarization_mode="summary_required",
                deduplication_mode="deduplicate_before_write",
                conflict_mode="conflict_check_required",
                language_policy="language_metadata_required",
                script_policy="script_metadata_required",
                provenance_policy="provenance_required",
                evidence_required=registry_entry.evidence_required,
                active=registry_entry.active,
                description=(
                    f"Memory classification policy for memory_tier={registry_entry.memory_tier_id} "
                    f"with retention_class={registry_entry.retention_class}."
                ),
            )
        )

    active_entries = sum(1 for entry in entries if entry.active)
    foundational_entries = sum(
        1 for entry in entries if entry.retention_class == "foundational"
    )
    approval_required_entries = sum(
        1
        for entry in entries
        if entry.approval_mode == "mandatory_human_approval"
    )

    return MemoryClassificationPolicyContract(
        total_entries=len(entries),
        active_entries=active_entries,
        foundational_entries=foundational_entries,
        approval_required_entries=approval_required_entries,
        entries=tuple(entries),
    )
