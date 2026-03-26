from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


ModuleKind = Literal[
    "skill",
    "memory_tier",
    "extension_cube",
]

ModuleDomainClass = Literal[
    "general",
    "simulation",
    "robotics",
    "media",
    "automation",
    "memory",
    "observability",
]

ModulePolicyProfile = Literal[
    "read_only",
    "sandbox_required",
    "approval_required",
    "execution_guarded",
]

ModuleObservabilityProfile = Literal[
    "basic",
    "extended",
    "critical",
]

DisplayRole = Literal[
    "primary_dashboard_display",
    "monitoring_display",
    "engineering_display",
    "presentation_display",
    "mobile_display_proxy",
]


_MODULE_SLUG_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_LANGUAGE_CODE_PATTERN = re.compile(r"^[a-z]{2,3}$")
_CONTRACT_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_VIEW_ID_PATTERN = re.compile(r"^view_[a-z0-9_]+$")


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
class ModuleManifestEntry:
    """Canonical manifest entry for extensible modules."""

    module_kind: ModuleKind
    module_slug: str
    display_name: str
    domain_class: ModuleDomainClass
    input_contract_ids: tuple[str, ...]
    output_contract_ids: tuple[str, ...]
    policy_profile: ModulePolicyProfile
    observability_profile: ModuleObservabilityProfile
    dashboard_view_ids: tuple[str, ...]
    supported_display_roles: tuple[DisplayRole, ...]
    explanation_available: bool
    multi_display_allowed: bool
    engine_adapter_required: bool
    supported_languages: tuple[str, ...]
    supported_scripts: tuple[str, ...]
    active: bool

    def __post_init__(self) -> None:
        """Validate module manifest entry invariants."""
        if not _MODULE_SLUG_PATTERN.fullmatch(self.module_slug):
            raise ValueError(
                f"module_slug must match ^[a-z][a-z0-9_]*$: {self.module_slug}"
            )

        if not self.display_name.strip():
            raise ValueError(f"display_name must not be empty for {self.module_slug}")

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
            values=self.dashboard_view_ids,
            field_name="dashboard_view_ids",
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

        if len(set(self.supported_display_roles)) != len(self.supported_display_roles):
            raise ValueError(
                f"Duplicate supported_display_roles detected for {self.module_slug}"
            )

        if not self.supported_display_roles:
            raise ValueError(
                f"supported_display_roles must not be empty for {self.module_slug}"
            )

        if self.module_kind == "skill":
            if not self.input_contract_ids:
                raise ValueError(
                    f"skill manifest must define input_contract_ids: {self.module_slug}"
                )
            if not self.output_contract_ids:
                raise ValueError(
                    f"skill manifest must define output_contract_ids: {self.module_slug}"
                )

        if self.module_kind == "memory_tier":
            if self.domain_class != "memory":
                raise ValueError(
                    f"memory_tier manifest must use domain_class='memory': {self.module_slug}"
                )
            if self.engine_adapter_required:
                raise ValueError(
                    f"memory_tier manifest must not require engine adapter: {self.module_slug}"
                )

        if self.module_kind == "extension_cube":
            if not self.dashboard_view_ids:
                raise ValueError(
                    f"extension_cube manifest must define dashboard views: {self.module_slug}"
                )

        if self.explanation_available and not self.dashboard_view_ids:
            raise ValueError(
                f"explanation_available requires dashboard_view_ids: {self.module_slug}"
            )

        if self.multi_display_allowed and len(self.supported_display_roles) < 2:
            raise ValueError(
                f"multi_display_allowed requires at least two display roles: {self.module_slug}"
            )

        for contract_id in self.input_contract_ids + self.output_contract_ids:
            if not _CONTRACT_ID_PATTERN.fullmatch(contract_id):
                raise ValueError(
                    f"contract id must match ^[a-z][a-z0-9_]*$: {contract_id}"
                )

        for view_id in self.dashboard_view_ids:
            if not _VIEW_ID_PATTERN.fullmatch(view_id):
                raise ValueError(
                    f"dashboard view id must match ^view_[a-z0-9_]+$: {view_id}"
                )

        for language_code in self.supported_languages:
            if not _LANGUAGE_CODE_PATTERN.fullmatch(language_code):
                raise ValueError(
                    f"language code must match ^[a-z]{{2,3}}$: {language_code}"
                )

        for script_name in self.supported_scripts:
            if not script_name.strip():
                raise ValueError(
                    f"supported_scripts must not contain empty value: {self.module_slug}"
                )

        if self.policy_profile == "read_only" and self.engine_adapter_required:
            raise ValueError(
                f"read_only manifest must not require engine adapter: {self.module_slug}"
            )

        if not self.active and self.engine_adapter_required:
            raise ValueError(
                f"inactive manifest must not require engine adapter: {self.module_slug}"
            )


@dataclass(frozen=True, slots=True)
class ModuleManifestSchemaContract:
    """Unified canonical module manifest schema contract."""

    schema_version: str
    total_manifests: int
    manifests: tuple[ModuleManifestEntry, ...]

    def __post_init__(self) -> None:
        """Validate module manifest schema contract invariants."""
        if not self.schema_version.strip():
            raise ValueError("schema_version must not be empty")

        if self.total_manifests != len(self.manifests):
            raise ValueError("total_manifests must match manifests length")

        slugs = tuple(entry.module_slug for entry in self.manifests)
        if len(set(slugs)) != len(slugs):
            raise ValueError("Duplicate module_slug values detected in manifest schema")

        display_names = tuple(entry.display_name for entry in self.manifests)
        if len(set(display_names)) != len(display_names):
            raise ValueError("Duplicate display_name values detected in manifest schema")


def build_module_manifest_schema_contract() -> ModuleManifestSchemaContract:
    """Build canonical module manifest schema contract."""
    manifests = (
        ModuleManifestEntry(
            module_kind="skill",
            module_slug="simulation_analysis",
            display_name="Simulation Analysis Skill",
            domain_class="simulation",
            input_contract_ids=(
                "simulation_engine_request",
                "validation_context",
            ),
            output_contract_ids=(
                "simulation_engine_result",
                "proposal_package",
            ),
            policy_profile="sandbox_required",
            observability_profile="extended",
            dashboard_view_ids=(
                "view_simulation_skill_overview",
            ),
            supported_display_roles=(
                "engineering_display",
                "primary_dashboard_display",
                "mobile_display_proxy",
            ),
            explanation_available=True,
            multi_display_allowed=True,
            engine_adapter_required=True,
            supported_languages=(
                "en",
                "ru",
                "uk",
                "de",
            ),
            supported_scripts=(
                "Latin",
                "Cyrillic",
            ),
            active=True,
        ),
        ModuleManifestEntry(
            module_kind="memory_tier",
            module_slug="project_architecture",
            display_name="Project Architecture Memory Tier",
            domain_class="memory",
            input_contract_ids=(
                "memory_write_request",
                "evidence_binding",
            ),
            output_contract_ids=(
                "memory_read_result",
            ),
            policy_profile="approval_required",
            observability_profile="critical",
            dashboard_view_ids=(
                "view_memory_project_architecture",
            ),
            supported_display_roles=(
                "primary_dashboard_display",
                "mobile_display_proxy",
            ),
            explanation_available=True,
            multi_display_allowed=True,
            engine_adapter_required=False,
            supported_languages=(
                "en",
                "ru",
                "uk",
                "de",
            ),
            supported_scripts=(
                "Latin",
                "Cyrillic",
            ),
            active=True,
        ),
        ModuleManifestEntry(
            module_kind="extension_cube",
            module_slug="monitoring_panel",
            display_name="Monitoring Panel Cube",
            domain_class="observability",
            input_contract_ids=(
                "execution_view_query",
            ),
            output_contract_ids=(
                "execution_view_result",
            ),
            policy_profile="read_only",
            observability_profile="basic",
            dashboard_view_ids=(
                "view_monitoring_panel",
            ),
            supported_display_roles=(
                "monitoring_display",
                "primary_dashboard_display",
            ),
            explanation_available=True,
            multi_display_allowed=True,
            engine_adapter_required=False,
            supported_languages=(
                "en",
                "ru",
                "uk",
                "de",
            ),
            supported_scripts=(
                "Latin",
                "Cyrillic",
            ),
            active=True,
        ),
    )

    return ModuleManifestSchemaContract(
        schema_version="1.0.0",
        total_manifests=len(manifests),
        manifests=manifests,
    )
