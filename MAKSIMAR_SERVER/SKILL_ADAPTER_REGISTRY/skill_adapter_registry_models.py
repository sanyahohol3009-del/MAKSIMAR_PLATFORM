from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.module_manifest import (
    ModuleDomainClass,
    ModuleObservabilityProfile,
    ModulePolicyProfile,
)


SkillAdapterExecutionMode = Literal[
    "sandboxed",
    "guarded",
    "read_only",
]

SkillAdapterRegistrationStatus = Literal[
    "registered",
]


_SKILL_ID_PATTERN = re.compile(r"^skill_[a-z][a-z0-9_]*_[a-z][a-z0-9_]*$")
_MODULE_ID_PATTERN = re.compile(r"^module_skill_[a-z][a-z0-9_]*$")
_WORKER_ID_PATTERN = re.compile(r"^worker_[a-z][a-z0-9_]*_001$")
_CONTRACT_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
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
class SkillAdapterRegistryEntry:
    """Canonical skill adapter registry entry."""

    module_slug: str
    module_id: str
    skill_id: str
    worker_id: str
    domain_class: ModuleDomainClass
    input_contract_ids: tuple[str, ...]
    output_contract_ids: tuple[str, ...]
    policy_profile: ModulePolicyProfile
    observability_profile: ModuleObservabilityProfile
    panel_ids: tuple[str, ...]
    supported_languages: tuple[str, ...]
    supported_scripts: tuple[str, ...]
    engine_adapter_required: bool
    adapter_execution_mode: SkillAdapterExecutionMode
    registration_status: SkillAdapterRegistrationStatus
    active: bool
    description: str

    def __post_init__(self) -> None:
        """Validate skill adapter registry invariants."""
        if not self.module_slug.strip():
            raise ValueError("module_slug must not be empty")

        if not _MODULE_ID_PATTERN.fullmatch(self.module_id):
            raise ValueError(f"Invalid module_id: {self.module_id}")

        if not _SKILL_ID_PATTERN.fullmatch(self.skill_id):
            raise ValueError(f"Invalid skill_id: {self.skill_id}")

        if not _WORKER_ID_PATTERN.fullmatch(self.worker_id):
            raise ValueError(f"Invalid worker_id: {self.worker_id}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.module_slug}")

        if not self.active:
            raise ValueError(f"inactive skill must not be registered: {self.module_slug}")

        if self.registration_status != "registered":
            raise ValueError(
                f"skill adapter registry entry must be registered: {self.module_slug}"
            )

        if not self.engine_adapter_required:
            raise ValueError(
                f"skill adapter registry entry must require engine adapter: {self.module_slug}"
            )

        if self.adapter_execution_mode == "read_only":
            raise ValueError(
                f"skill adapter registry entry must not use read_only mode: {self.module_slug}"
            )

        if self.policy_profile == "sandbox_required":
            if self.adapter_execution_mode != "sandboxed":
                raise ValueError(
                    f"sandbox_required skill must use sandboxed mode: {self.module_slug}"
                )

        if self.policy_profile in ("approval_required", "execution_guarded"):
            if self.adapter_execution_mode != "guarded":
                raise ValueError(
                    f"guarded skill policy must use guarded mode: {self.module_slug}"
                )

        if not self.input_contract_ids:
            raise ValueError(
                f"skill adapter registry must define input_contract_ids: {self.module_slug}"
            )

        if not self.output_contract_ids:
            raise ValueError(
                f"skill adapter registry must define output_contract_ids: {self.module_slug}"
            )

        if not self.panel_ids:
            raise ValueError(
                f"skill adapter registry must define panel_ids: {self.module_slug}"
            )

        _validate_unique_non_empty_str_tuple(
            values=self.input_contract_ids,
            field_name="input_contract_ids",
            owner_id=self.module_slug,
        )
        _validate_unique_non_empty_str_tuple(
            values=self.output_contract_ids,
            field_name="output_contract_ids",
            owner_id=self.module_slug,
        )
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

        for contract_id in self.input_contract_ids + self.output_contract_ids:
            if not _CONTRACT_ID_PATTERN.fullmatch(contract_id):
                raise ValueError(f"Invalid contract_id: {contract_id}")

        for panel_id in self.panel_ids:
            if not _PANEL_ID_PATTERN.fullmatch(panel_id):
                raise ValueError(f"Invalid panel_id: {panel_id}")

        for language_code in self.supported_languages:
            if not _LANGUAGE_CODE_PATTERN.fullmatch(language_code):
                raise ValueError(f"Invalid language code: {language_code}")


@dataclass(frozen=True, slots=True)
class SkillAdapterRegistryContract:
    """Unified skill adapter registry contract."""

    total_entries: int
    active_entries: int
    sandboxed_entries: int
    engine_adapter_entries: int
    entries: tuple[SkillAdapterRegistryEntry, ...]

    def __post_init__(self) -> None:
        """Validate skill adapter registry contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        active_entries = sum(1 for entry in self.entries if entry.active)
        sandboxed_entries = sum(
            1 for entry in self.entries if entry.adapter_execution_mode == "sandboxed"
        )
        engine_adapter_entries = sum(
            1 for entry in self.entries if entry.engine_adapter_required
        )

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        if self.sandboxed_entries != sandboxed_entries:
            raise ValueError("sandboxed_entries must match computed count")

        if self.engine_adapter_entries != engine_adapter_entries:
            raise ValueError("engine_adapter_entries must match computed count")

        module_ids = tuple(entry.module_id for entry in self.entries)
        skill_ids = tuple(entry.skill_id for entry in self.entries)
        worker_ids = tuple(entry.worker_id for entry in self.entries)

        if len(set(module_ids)) != len(module_ids):
            raise ValueError("Duplicate module_ids detected in skill registry")

        if len(set(skill_ids)) != len(skill_ids):
            raise ValueError("Duplicate skill_ids detected in skill registry")

        if len(set(worker_ids)) != len(worker_ids):
            raise ValueError("Duplicate worker_ids detected in skill registry")
