from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


MemoryRetentionClass = Literal[
    "foundational",
    "operational",
    "ephemeral",
]

MemoryRegistryWritePolicy = Literal[
    "approval_required",
    "restricted_write",
]

MemoryRegistryReadPolicy = Literal[
    "scoped_read",
    "owner_scoped_read",
]


_MEMORY_TIER_ID_PATTERN = re.compile(r"^memory_[a-z][a-z0-9_]*$")
_MODULE_ID_PATTERN = re.compile(r"^module_memory_tier_[a-z][a-z0-9_]*$")
_PANEL_ID_PATTERN = re.compile(r"^panel_[a-z][a-z0-9_]*$")
_LANGUAGE_CODE_PATTERN = re.compile(r"^[a-z]{2,3}$")


def _validate_unique_non_empty_str_tuple(
    *,
    values: tuple[str, ...],
    field_name: str,
    owner_id: str,
) -> None:
    """Validate tuple items are non-empty and unique."""
    if len(set(values)) != len(values):
        raise ValueError(f"Duplicate values in {field_name} for {owner_id}")

    for value in values:
        if not value.strip():
            raise ValueError(f"{field_name} contains empty value for {owner_id}")


@dataclass(frozen=True, slots=True)
class MemoryRegistryEntry:
    """Canonical memory registry entry."""

    module_slug: str
    module_id: str
    memory_tier_id: str
    retention_class: MemoryRetentionClass
    write_policy: MemoryRegistryWritePolicy
    read_policy: MemoryRegistryReadPolicy
    evidence_required: bool
    conflict_resolution_required: bool
    explanation_available: bool
    panel_ids: tuple[str, ...]
    supported_languages: tuple[str, ...]
    supported_scripts: tuple[str, ...]
    active: bool
    description: str

    def __post_init__(self) -> None:
        """Validate memory registry entry invariants."""
        if not self.module_slug.strip():
            raise ValueError("module_slug must not be empty")

        if not _MODULE_ID_PATTERN.fullmatch(self.module_id):
            raise ValueError(f"Invalid module_id: {self.module_id}")

        if not _MEMORY_TIER_ID_PATTERN.fullmatch(self.memory_tier_id):
            raise ValueError(f"Invalid memory_tier_id: {self.memory_tier_id}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.module_slug}")

        if not self.panel_ids:
            raise ValueError(f"panel_ids must not be empty for {self.module_slug}")

        for panel_id in self.panel_ids:
            if not _PANEL_ID_PATTERN.fullmatch(panel_id):
                raise ValueError(f"Invalid panel_id: {panel_id}")

        _validate_unique_non_empty_str_tuple(
            values=self.panel_ids,
            field_name="panel_ids",
            owner_id=self.module_slug,
        )
        _validate_unique_non_empty_str_tuple(
            values=self.supported_languages,
            field_name="supported_languages",
            owner_id=self.module_slug,
        )
        _validate_unique_non_empty_str_tuple(
            values=self.supported_scripts,
            field_name="supported_scripts",
            owner_id=self.module_slug,
        )

        for language_code in self.supported_languages:
            if not _LANGUAGE_CODE_PATTERN.fullmatch(language_code):
                raise ValueError(f"Invalid language code: {language_code}")

        if self.write_policy == "approval_required" and not self.evidence_required:
            raise ValueError(
                f"approval_required memory tier must require evidence: {self.module_slug}"
            )

        if self.retention_class == "foundational" and not self.conflict_resolution_required:
            raise ValueError(
                f"foundational memory tier must require conflict resolution: {self.module_slug}"
            )

        if not self.explanation_available:
            raise ValueError(
                f"memory registry entry must provide explainability: {self.module_slug}"
            )

        if not self.active:
            raise ValueError(
                f"inactive memory tier must not be registered: {self.module_slug}"
            )


@dataclass(frozen=True, slots=True)
class MemoryRegistryContract:
    """Unified memory registry contract."""

    total_entries: int
    active_entries: int
    foundational_entries: int
    approval_required_entries: int
    entries: tuple[MemoryRegistryEntry, ...]

    def __post_init__(self) -> None:
        """Validate memory registry contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        active_entries = sum(1 for entry in self.entries if entry.active)
        foundational_entries = sum(
            1 for entry in self.entries if entry.retention_class == "foundational"
        )
        approval_required_entries = sum(
            1 for entry in self.entries if entry.write_policy == "approval_required"
        )

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        if self.foundational_entries != foundational_entries:
            raise ValueError("foundational_entries must match computed count")

        if self.approval_required_entries != approval_required_entries:
            raise ValueError("approval_required_entries must match computed count")

        module_ids = tuple(entry.module_id for entry in self.entries)
        memory_tier_ids = tuple(entry.memory_tier_id for entry in self.entries)

        if len(set(module_ids)) != len(module_ids):
            raise ValueError("Duplicate module_ids detected in memory registry")

        if len(set(memory_tier_ids)) != len(memory_tier_ids):
            raise ValueError("Duplicate memory_tier_ids detected in memory registry")
