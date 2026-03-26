from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.physics_simulation_mode import (
    build_physics_simulation_mode_contract,
)


ConstraintProfileId = Literal[
    "constraint_strict_execution_001",
    "constraint_engineering_candidate_001",
    "constraint_research_exploratory_001",
    "constraint_control_feedback_001",
]

ConstraintDomain = Literal[
    "machine_safety",
    "material_limits",
    "surface_geometry",
    "optics_display",
]

SimulationMode = Literal[
    "strict_physics",
    "engineering_realistic",
    "research_relaxed",
    "control_learning",
]

ConstraintRegistryStatus = Literal[
    "registered",
]


_PROFILE_ID_PATTERN = re.compile(r"^constraint_[a-z][a-z0-9_]*$")
_DOMAIN_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_MODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


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
class ConstraintProfileEntry:
    """Canonical constraint profile registry entry."""

    constraint_profile_id: ConstraintProfileId
    simulation_mode: SimulationMode
    constraint_domains: tuple[ConstraintDomain, ...]
    strict_machine_limits_required: bool
    material_limit_enforcement_required: bool
    geometry_constraint_required: bool
    optics_constraint_required: bool
    production_execution_allowed: bool
    validation_gate_required: bool
    research_only: bool
    registry_status: ConstraintRegistryStatus
    description: str

    def __post_init__(self) -> None:
        """Validate constraint profile invariants."""
        if not _PROFILE_ID_PATTERN.fullmatch(self.constraint_profile_id):
            raise ValueError(
                f"Invalid constraint_profile_id: {self.constraint_profile_id}"
            )

        if not _MODE_PATTERN.fullmatch(self.simulation_mode):
            raise ValueError(f"Invalid simulation_mode: {self.simulation_mode}")

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.constraint_profile_id}"
            )

        _validate_unique_non_empty_str_tuple(
            values=self.constraint_domains,
            field_name="constraint_domains",
            owner_id=self.constraint_profile_id,
        )

        if len(self.constraint_domains) != 4:
            raise ValueError(
                f"constraint_domains must contain 4 canonical domains: {self.constraint_profile_id}"
            )

        for domain in self.constraint_domains:
            if not _DOMAIN_PATTERN.fullmatch(domain):
                raise ValueError(
                    f"Invalid constraint domain '{domain}' for {self.constraint_profile_id}"
                )

        if not self.strict_machine_limits_required:
            raise ValueError(
                f"strict_machine_limits_required must be True: {self.constraint_profile_id}"
            )
        if not self.material_limit_enforcement_required:
            raise ValueError(
                f"material_limit_enforcement_required must be True: {self.constraint_profile_id}"
            )
        if not self.geometry_constraint_required:
            raise ValueError(
                f"geometry_constraint_required must be True: {self.constraint_profile_id}"
            )
        if not self.optics_constraint_required:
            raise ValueError(
                f"optics_constraint_required must be True: {self.constraint_profile_id}"
            )

        if self.registry_status != "registered":
            raise ValueError(
                f"constraint profile must be registered: {self.constraint_profile_id}"
            )

        if self.simulation_mode == "strict_physics":
            if self.constraint_profile_id != "constraint_strict_execution_001":
                raise ValueError(
                    f"strict_physics must use canonical strict constraint profile: {self.constraint_profile_id}"
                )
            if not self.production_execution_allowed:
                raise ValueError(
                    f"strict_physics must allow production execution: {self.constraint_profile_id}"
                )
            if not self.validation_gate_required:
                raise ValueError(
                    f"strict_physics must require validation gate: {self.constraint_profile_id}"
                )
            if self.research_only:
                raise ValueError(
                    f"strict_physics must not be research_only: {self.constraint_profile_id}"
                )

        if self.simulation_mode == "engineering_realistic":
            if self.constraint_profile_id != "constraint_engineering_candidate_001":
                raise ValueError(
                    f"engineering_realistic must use canonical engineering profile: {self.constraint_profile_id}"
                )
            if not self.production_execution_allowed:
                raise ValueError(
                    f"engineering_realistic must allow production execution path: {self.constraint_profile_id}"
                )
            if not self.validation_gate_required:
                raise ValueError(
                    f"engineering_realistic must require validation gate: {self.constraint_profile_id}"
                )
            if self.research_only:
                raise ValueError(
                    f"engineering_realistic must not be research_only: {self.constraint_profile_id}"
                )

        if self.simulation_mode == "research_relaxed":
            if self.constraint_profile_id != "constraint_research_exploratory_001":
                raise ValueError(
                    f"research_relaxed must use canonical research profile: {self.constraint_profile_id}"
                )
            if self.production_execution_allowed:
                raise ValueError(
                    f"research_relaxed must not allow production execution: {self.constraint_profile_id}"
                )
            if self.validation_gate_required:
                raise ValueError(
                    f"research_relaxed must not require execution validation gate by default: {self.constraint_profile_id}"
                )
            if not self.research_only:
                raise ValueError(
                    f"research_relaxed must be research_only: {self.constraint_profile_id}"
                )

        if self.simulation_mode == "control_learning":
            if self.constraint_profile_id != "constraint_control_feedback_001":
                raise ValueError(
                    f"control_learning must use canonical control profile: {self.constraint_profile_id}"
                )
            if self.production_execution_allowed:
                raise ValueError(
                    f"control_learning must not allow production execution: {self.constraint_profile_id}"
                )
            if self.validation_gate_required:
                raise ValueError(
                    f"control_learning must not require execution validation gate by default: {self.constraint_profile_id}"
                )
            if not self.research_only:
                raise ValueError(
                    f"control_learning must be research_only/control_only: {self.constraint_profile_id}"
                )


@dataclass(frozen=True, slots=True)
class ConstraintProfileRegistryContract:
    """Unified constraint profile registry contract."""

    total_entries: int
    production_allowed_entries: int
    research_only_entries: int
    validation_gate_entries: int
    registered_entries: int
    entries: tuple[ConstraintProfileEntry, ...]

    def __post_init__(self) -> None:
        """Validate constraint profile registry contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        production_allowed_entries = sum(
            1 for entry in self.entries if entry.production_execution_allowed
        )
        research_only_entries = sum(
            1 for entry in self.entries if entry.research_only
        )
        validation_gate_entries = sum(
            1 for entry in self.entries if entry.validation_gate_required
        )
        registered_entries = sum(
            1 for entry in self.entries if entry.registry_status == "registered"
        )

        if self.production_allowed_entries != production_allowed_entries:
            raise ValueError("production_allowed_entries must match computed count")

        if self.research_only_entries != research_only_entries:
            raise ValueError("research_only_entries must match computed count")

        if self.validation_gate_entries != validation_gate_entries:
            raise ValueError("validation_gate_entries must match computed count")

        if self.registered_entries != registered_entries:
            raise ValueError("registered_entries must match computed count")

        entry_ids = tuple(entry.constraint_profile_id for entry in self.entries)
        modes = tuple(entry.simulation_mode for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate constraint_profile_id values detected")

        if len(set(modes)) != len(modes):
            raise ValueError("Duplicate simulation_mode values detected")


def build_constraint_profile_registry_contract() -> ConstraintProfileRegistryContract:
    """Build canonical constraint profile registry contract."""
    simulation_mode_contract = build_physics_simulation_mode_contract()

    required_modes = {
        "strict_physics",
        "engineering_realistic",
        "research_relaxed",
        "control_learning",
    }
    mode_names = {entry.simulation_mode for entry in simulation_mode_contract.entries}
    missing_modes = required_modes - mode_names
    if missing_modes:
        raise ValueError(f"Missing simulation modes: {sorted(missing_modes)}")

    canonical_domains = (
        "machine_safety",
        "material_limits",
        "surface_geometry",
        "optics_display",
    )

    entries = (
        ConstraintProfileEntry(
            constraint_profile_id="constraint_strict_execution_001",
            simulation_mode="strict_physics",
            constraint_domains=canonical_domains,
            strict_machine_limits_required=True,
            material_limit_enforcement_required=True,
            geometry_constraint_required=True,
            optics_constraint_required=True,
            production_execution_allowed=True,
            validation_gate_required=True,
            research_only=False,
            registry_status="registered",
            description="Strict execution constraint profile for production-safe physics.",
        ),
        ConstraintProfileEntry(
            constraint_profile_id="constraint_engineering_candidate_001",
            simulation_mode="engineering_realistic",
            constraint_domains=canonical_domains,
            strict_machine_limits_required=True,
            material_limit_enforcement_required=True,
            geometry_constraint_required=True,
            optics_constraint_required=True,
            production_execution_allowed=True,
            validation_gate_required=True,
            research_only=False,
            registry_status="registered",
            description="Engineering candidate constraint profile before final validation.",
        ),
        ConstraintProfileEntry(
            constraint_profile_id="constraint_research_exploratory_001",
            simulation_mode="research_relaxed",
            constraint_domains=canonical_domains,
            strict_machine_limits_required=True,
            material_limit_enforcement_required=True,
            geometry_constraint_required=True,
            optics_constraint_required=True,
            production_execution_allowed=False,
            validation_gate_required=False,
            research_only=True,
            registry_status="registered",
            description="Research exploratory constraint profile for non-production simulation.",
        ),
        ConstraintProfileEntry(
            constraint_profile_id="constraint_control_feedback_001",
            simulation_mode="control_learning",
            constraint_domains=canonical_domains,
            strict_machine_limits_required=True,
            material_limit_enforcement_required=True,
            geometry_constraint_required=True,
            optics_constraint_required=True,
            production_execution_allowed=False,
            validation_gate_required=False,
            research_only=True,
            registry_status="registered",
            description="Control feedback constraint profile for learning-only simulation traces.",
        ),
    )

    production_allowed_entries = sum(
        1 for entry in entries if entry.production_execution_allowed
    )
    research_only_entries = sum(
        1 for entry in entries if entry.research_only
    )
    validation_gate_entries = sum(
        1 for entry in entries if entry.validation_gate_required
    )
    registered_entries = sum(
        1 for entry in entries if entry.registry_status == "registered"
    )

    return ConstraintProfileRegistryContract(
        total_entries=len(entries),
        production_allowed_entries=production_allowed_entries,
        research_only_entries=research_only_entries,
        validation_gate_entries=validation_gate_entries,
        registered_entries=registered_entries,
        entries=entries,
    )
