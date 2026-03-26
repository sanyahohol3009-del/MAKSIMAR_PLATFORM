from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.module_manifest import (
    ModuleKind,
)


RegistryEnrollmentStatus = Literal[
    "enrolled",
    "skipped_inactive",
]

RegistryEnrollmentTarget = Literal[
    "module_registry",
    "memory_registry",
    "skill_registry",
    "dashboard_registry",
]


@dataclass(frozen=True, slots=True)
class RegistryAutoEnrollmentEntry:
    """Registry auto-enrollment entry derived from manifest and canonical IDs."""

    module_kind: ModuleKind
    module_slug: str
    module_id: str
    enrollment_target: RegistryEnrollmentTarget
    enrollment_status: RegistryEnrollmentStatus
    skill_id: str
    memory_tier_id: str
    panel_ids: tuple[str, ...]
    active: bool
    description: str

    def __post_init__(self) -> None:
        """Validate registry auto-enrollment entry invariants."""
        if not self.module_slug.strip():
            raise ValueError("module_slug must not be empty")

        if not self.module_id.strip():
            raise ValueError(f"module_id must not be empty for {self.module_slug}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.module_slug}")

        if len(set(self.panel_ids)) != len(self.panel_ids):
            raise ValueError(f"Duplicate panel_ids detected for {self.module_slug}")

        if self.enrollment_status == "enrolled" and not self.active:
            raise ValueError(
                f"inactive entry must not have enrolled status: {self.module_slug}"
            )

        if self.enrollment_status == "skipped_inactive" and self.active:
            raise ValueError(
                f"active entry must not have skipped_inactive status: {self.module_slug}"
            )

        if self.module_kind == "skill":
            if self.enrollment_target != "skill_registry":
                raise ValueError(
                    f"skill must enroll into skill_registry: {self.module_slug}"
                )
            if self.skill_id == "":
                raise ValueError(
                    f"skill enrollment must define skill_id: {self.module_slug}"
                )
            if self.memory_tier_id != "":
                raise ValueError(
                    f"skill enrollment must not define memory_tier_id: {self.module_slug}"
                )

        if self.module_kind == "memory_tier":
            if self.enrollment_target != "memory_registry":
                raise ValueError(
                    f"memory_tier must enroll into memory_registry: {self.module_slug}"
                )
            if self.memory_tier_id == "":
                raise ValueError(
                    f"memory_tier enrollment must define memory_tier_id: {self.module_slug}"
                )
            if self.skill_id != "":
                raise ValueError(
                    f"memory_tier enrollment must not define skill_id: {self.module_slug}"
                )

        if self.module_kind == "extension_cube":
            if self.enrollment_target != "dashboard_registry":
                raise ValueError(
                    f"extension_cube must enroll into dashboard_registry: {self.module_slug}"
                )
            if not self.panel_ids:
                raise ValueError(
                    f"extension_cube enrollment must define panel_ids: {self.module_slug}"
                )
            if self.skill_id != "":
                raise ValueError(
                    f"extension_cube enrollment must not define skill_id: {self.module_slug}"
                )
            if self.memory_tier_id != "":
                raise ValueError(
                    f"extension_cube enrollment must not define memory_tier_id: {self.module_slug}"
                )


@dataclass(frozen=True, slots=True)
class RegistryAutoEnrollmentContract:
    """Unified registry auto-enrollment contract."""

    total_entries: int
    enrolled_entries: int
    skill_registry_entries: int
    memory_registry_entries: int
    dashboard_registry_entries: int
    entries: tuple[RegistryAutoEnrollmentEntry, ...]

    def __post_init__(self) -> None:
        """Validate registry auto-enrollment contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        enrolled_entries = sum(
            1 for entry in self.entries if entry.enrollment_status == "enrolled"
        )
        skill_registry_entries = sum(
            1 for entry in self.entries if entry.enrollment_target == "skill_registry"
        )
        memory_registry_entries = sum(
            1 for entry in self.entries if entry.enrollment_target == "memory_registry"
        )
        dashboard_registry_entries = sum(
            1
            for entry in self.entries
            if entry.enrollment_target == "dashboard_registry"
        )

        if self.enrolled_entries != enrolled_entries:
            raise ValueError("enrolled_entries must match computed count")

        if self.skill_registry_entries != skill_registry_entries:
            raise ValueError("skill_registry_entries must match computed count")

        if self.memory_registry_entries != memory_registry_entries:
            raise ValueError("memory_registry_entries must match computed count")

        if self.dashboard_registry_entries != dashboard_registry_entries:
            raise ValueError("dashboard_registry_entries must match computed count")

        module_ids = tuple(entry.module_id for entry in self.entries)
        if len(set(module_ids)) != len(module_ids):
            raise ValueError("Duplicate module_ids detected in auto-enrollment")
