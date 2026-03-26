from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.constraint_profile_registry import (
    build_constraint_profile_registry_contract,
)
from MAKSIMAR_CORE_LIB.material_registry import (
    build_material_registry_contract,
)
from MAKSIMAR_CORE_LIB.physics_simulation_mode import (
    build_physics_simulation_mode_contract,
)
from MAKSIMAR_CORE_LIB.sensor_simulation import (
    build_sensor_simulation_contract,
)
from MAKSIMAR_CORE_LIB.surface_intelligence import (
    build_surface_intelligence_contract,
)


PhysicsValidationDecision = Literal[
    "approved",
    "requires_review",
    "rejected",
]

PhysicsValidationReason = Literal[
    "strict_execution_ready",
    "engineering_candidate_requires_review",
    "research_mode_forbidden_for_execution",
    "control_learning_forbidden_for_execution",
]

SimulationMode = Literal[
    "strict_physics",
    "engineering_realistic",
    "research_relaxed",
    "control_learning",
]

PhysicsValidationStatus = Literal[
    "validated",
]


_GATE_ENTRY_ID_PATTERN = re.compile(r"^physgate_[a-z][a-z0-9_]*$")
_MODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_CONSTRAINT_PROFILE_ID_PATTERN = re.compile(r"^constraint_[a-z][a-z0-9_]*$")
_MATERIAL_ID_PATTERN = re.compile(r"^material_[a-z][a-z0-9_]*$")
_SURFACE_ENTRY_ID_PATTERN = re.compile(r"^surfaceintel_[a-z][a-z0-9_]*$")
_SENSOR_ENTRY_ID_PATTERN = re.compile(r"^sensorsim_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class PhysicsValidationGateEntry:
    """Canonical physics validation gate entry."""

    gate_entry_id: str
    simulation_mode: SimulationMode
    constraint_profile_id: str
    material_id: str
    surface_entry_id: str
    sensor_entry_id: str
    physics_feasibility_passed: bool
    safety_constraints_passed: bool
    machine_constraints_passed: bool
    material_limits_passed: bool
    strict_validation_required: bool
    validation_decision: PhysicsValidationDecision
    validation_reason: PhysicsValidationReason
    execution_allowed: bool
    explainable_required: bool
    validation_status: PhysicsValidationStatus
    description: str

    def __post_init__(self) -> None:
        """Validate physics validation gate invariants."""
        if not _GATE_ENTRY_ID_PATTERN.fullmatch(self.gate_entry_id):
            raise ValueError(f"Invalid gate_entry_id: {self.gate_entry_id}")

        if not _MODE_PATTERN.fullmatch(self.simulation_mode):
            raise ValueError(f"Invalid simulation_mode: {self.simulation_mode}")

        if not _CONSTRAINT_PROFILE_ID_PATTERN.fullmatch(self.constraint_profile_id):
            raise ValueError(
                f"Invalid constraint_profile_id: {self.constraint_profile_id}"
            )

        if not _MATERIAL_ID_PATTERN.fullmatch(self.material_id):
            raise ValueError(f"Invalid material_id: {self.material_id}")

        if not _SURFACE_ENTRY_ID_PATTERN.fullmatch(self.surface_entry_id):
            raise ValueError(f"Invalid surface_entry_id: {self.surface_entry_id}")

        if not _SENSOR_ENTRY_ID_PATTERN.fullmatch(self.sensor_entry_id):
            raise ValueError(f"Invalid sensor_entry_id: {self.sensor_entry_id}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.gate_entry_id}")

        if not self.physics_feasibility_passed:
            raise ValueError(
                f"physics_feasibility_passed must be True in canonical entries: {self.gate_entry_id}"
            )
        if not self.safety_constraints_passed:
            raise ValueError(
                f"safety_constraints_passed must be True in canonical entries: {self.gate_entry_id}"
            )
        if not self.machine_constraints_passed:
            raise ValueError(
                f"machine_constraints_passed must be True in canonical entries: {self.gate_entry_id}"
            )
        if not self.material_limits_passed:
            raise ValueError(
                f"material_limits_passed must be True in canonical entries: {self.gate_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.gate_entry_id}"
            )

        if self.validation_status != "validated":
            raise ValueError(
                f"validation_status must be validated: {self.gate_entry_id}"
            )

        if self.simulation_mode == "strict_physics":
            if self.constraint_profile_id != "constraint_strict_execution_001":
                raise ValueError(
                    f"strict_physics must use strict execution constraint profile: {self.gate_entry_id}"
                )
            if not self.strict_validation_required:
                raise ValueError(
                    f"strict_physics must require strict validation: {self.gate_entry_id}"
                )
            if self.validation_decision != "approved":
                raise ValueError(
                    f"strict_physics must be approved: {self.gate_entry_id}"
                )
            if self.validation_reason != "strict_execution_ready":
                raise ValueError(
                    f"strict_physics must use strict_execution_ready reason: {self.gate_entry_id}"
                )
            if not self.execution_allowed:
                raise ValueError(
                    f"strict_physics must allow execution: {self.gate_entry_id}"
                )

        if self.simulation_mode == "engineering_realistic":
            if self.constraint_profile_id != "constraint_engineering_candidate_001":
                raise ValueError(
                    f"engineering_realistic must use engineering candidate constraint profile: {self.gate_entry_id}"
                )
            if not self.strict_validation_required:
                raise ValueError(
                    f"engineering_realistic must require strict validation: {self.gate_entry_id}"
                )
            if self.validation_decision != "requires_review":
                raise ValueError(
                    f"engineering_realistic must require review: {self.gate_entry_id}"
                )
            if self.validation_reason != "engineering_candidate_requires_review":
                raise ValueError(
                    f"engineering_realistic must use engineering_candidate_requires_review reason: {self.gate_entry_id}"
                )
            if self.execution_allowed:
                raise ValueError(
                    f"engineering_realistic must not directly allow execution: {self.gate_entry_id}"
                )

        if self.simulation_mode == "research_relaxed":
            if self.constraint_profile_id != "constraint_research_exploratory_001":
                raise ValueError(
                    f"research_relaxed must use research exploratory constraint profile: {self.gate_entry_id}"
                )
            if self.strict_validation_required:
                raise ValueError(
                    f"research_relaxed must not require strict validation in default path: {self.gate_entry_id}"
                )
            if self.validation_decision != "rejected":
                raise ValueError(
                    f"research_relaxed must be rejected for execution: {self.gate_entry_id}"
                )
            if self.validation_reason != "research_mode_forbidden_for_execution":
                raise ValueError(
                    f"research_relaxed must use research_mode_forbidden_for_execution reason: {self.gate_entry_id}"
                )
            if self.execution_allowed:
                raise ValueError(
                    f"research_relaxed must not allow execution: {self.gate_entry_id}"
                )

        if self.simulation_mode == "control_learning":
            if self.constraint_profile_id != "constraint_control_feedback_001":
                raise ValueError(
                    f"control_learning must use control feedback constraint profile: {self.gate_entry_id}"
                )
            if self.strict_validation_required:
                raise ValueError(
                    f"control_learning must not require strict validation in default path: {self.gate_entry_id}"
                )
            if self.validation_decision != "rejected":
                raise ValueError(
                    f"control_learning must be rejected for execution: {self.gate_entry_id}"
                )
            if self.validation_reason != "control_learning_forbidden_for_execution":
                raise ValueError(
                    f"control_learning must use control_learning_forbidden_for_execution reason: {self.gate_entry_id}"
                )
            if self.execution_allowed:
                raise ValueError(
                    f"control_learning must not allow execution: {self.gate_entry_id}"
                )


@dataclass(frozen=True, slots=True)
class PhysicsValidationGateContract:
    """Unified physics validation gate contract."""

    total_entries: int
    approved_entries: int
    review_entries: int
    rejected_entries: int
    execution_allowed_entries: int
    validated_entries: int
    entries: tuple[PhysicsValidationGateEntry, ...]

    def __post_init__(self) -> None:
        """Validate physics validation gate contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        approved_entries = sum(
            1 for entry in self.entries if entry.validation_decision == "approved"
        )
        review_entries = sum(
            1
            for entry in self.entries
            if entry.validation_decision == "requires_review"
        )
        rejected_entries = sum(
            1 for entry in self.entries if entry.validation_decision == "rejected"
        )
        execution_allowed_entries = sum(
            1 for entry in self.entries if entry.execution_allowed
        )
        validated_entries = sum(
            1 for entry in self.entries if entry.validation_status == "validated"
        )

        if self.approved_entries != approved_entries:
            raise ValueError("approved_entries must match computed count")

        if self.review_entries != review_entries:
            raise ValueError("review_entries must match computed count")

        if self.rejected_entries != rejected_entries:
            raise ValueError("rejected_entries must match computed count")

        if self.execution_allowed_entries != execution_allowed_entries:
            raise ValueError("execution_allowed_entries must match computed count")

        if self.validated_entries != validated_entries:
            raise ValueError("validated_entries must match computed count")

        entry_ids = tuple(entry.gate_entry_id for entry in self.entries)
        modes = tuple(entry.simulation_mode for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate gate_entry_id values detected")

        if len(set(modes)) != len(modes):
            raise ValueError("Duplicate simulation_mode values detected")


def build_physics_validation_gate_contract() -> PhysicsValidationGateContract:
    """Build canonical physics validation gate contract."""
    mode_contract = build_physics_simulation_mode_contract()
    constraint_contract = build_constraint_profile_registry_contract()
    material_contract = build_material_registry_contract()
    surface_contract = build_surface_intelligence_contract()
    sensor_contract = build_sensor_simulation_contract()

    mode_names = {entry.simulation_mode for entry in mode_contract.entries}
    constraint_ids = {entry.constraint_profile_id for entry in constraint_contract.entries}
    material_ids = {entry.material_id for entry in material_contract.entries}
    surface_ids = {entry.surface_entry_id for entry in surface_contract.entries}
    sensor_ids = {entry.sensor_entry_id for entry in sensor_contract.entries}

    required_modes = {
        "strict_physics",
        "engineering_realistic",
        "research_relaxed",
        "control_learning",
    }
    required_constraints = {
        "constraint_strict_execution_001",
        "constraint_engineering_candidate_001",
        "constraint_research_exploratory_001",
        "constraint_control_feedback_001",
    }
    required_materials = {
        "material_aluminum_001",
        "material_steel_001",
        "material_acrylic_001",
        "material_wood_001",
    }
    required_surfaces = {
        "surfaceintel_aluminum_engraving_001",
        "surfaceintel_steel_cutting_001",
        "surfaceintel_acrylic_engraving_001",
        "surfaceintel_wood_engraving_001",
    }
    required_sensors = {
        "sensorsim_aluminum_001",
        "sensorsim_steel_001",
        "sensorsim_acrylic_001",
        "sensorsim_wood_001",
    }

    if required_modes - mode_names:
        raise ValueError(f"Missing simulation modes: {sorted(required_modes - mode_names)}")
    if required_constraints - constraint_ids:
        raise ValueError(
            f"Missing constraint profiles: {sorted(required_constraints - constraint_ids)}"
        )
    if required_materials - material_ids:
        raise ValueError(
            f"Missing material ids: {sorted(required_materials - material_ids)}"
        )
    if required_surfaces - surface_ids:
        raise ValueError(
            f"Missing surface ids: {sorted(required_surfaces - surface_ids)}"
        )
    if required_sensors - sensor_ids:
        raise ValueError(
            f"Missing sensor ids: {sorted(required_sensors - sensor_ids)}"
        )

    entries = (
        PhysicsValidationGateEntry(
            gate_entry_id="physgate_strict_physics_001",
            simulation_mode="strict_physics",
            constraint_profile_id="constraint_strict_execution_001",
            material_id="material_aluminum_001",
            surface_entry_id="surfaceintel_aluminum_engraving_001",
            sensor_entry_id="sensorsim_aluminum_001",
            physics_feasibility_passed=True,
            safety_constraints_passed=True,
            machine_constraints_passed=True,
            material_limits_passed=True,
            strict_validation_required=True,
            validation_decision="approved",
            validation_reason="strict_execution_ready",
            execution_allowed=True,
            explainable_required=True,
            validation_status="validated",
            description="Physics validation gate profile for strict execution path.",
        ),
        PhysicsValidationGateEntry(
            gate_entry_id="physgate_engineering_realistic_001",
            simulation_mode="engineering_realistic",
            constraint_profile_id="constraint_engineering_candidate_001",
            material_id="material_steel_001",
            surface_entry_id="surfaceintel_steel_cutting_001",
            sensor_entry_id="sensorsim_steel_001",
            physics_feasibility_passed=True,
            safety_constraints_passed=True,
            machine_constraints_passed=True,
            material_limits_passed=True,
            strict_validation_required=True,
            validation_decision="requires_review",
            validation_reason="engineering_candidate_requires_review",
            execution_allowed=False,
            explainable_required=True,
            validation_status="validated",
            description="Physics validation gate profile for engineering candidate path.",
        ),
        PhysicsValidationGateEntry(
            gate_entry_id="physgate_research_relaxed_001",
            simulation_mode="research_relaxed",
            constraint_profile_id="constraint_research_exploratory_001",
            material_id="material_acrylic_001",
            surface_entry_id="surfaceintel_acrylic_engraving_001",
            sensor_entry_id="sensorsim_acrylic_001",
            physics_feasibility_passed=True,
            safety_constraints_passed=True,
            machine_constraints_passed=True,
            material_limits_passed=True,
            strict_validation_required=False,
            validation_decision="rejected",
            validation_reason="research_mode_forbidden_for_execution",
            execution_allowed=False,
            explainable_required=True,
            validation_status="validated",
            description="Physics validation gate profile for research-only path.",
        ),
        PhysicsValidationGateEntry(
            gate_entry_id="physgate_control_learning_001",
            simulation_mode="control_learning",
            constraint_profile_id="constraint_control_feedback_001",
            material_id="material_wood_001",
            surface_entry_id="surfaceintel_wood_engraving_001",
            sensor_entry_id="sensorsim_wood_001",
            physics_feasibility_passed=True,
            safety_constraints_passed=True,
            machine_constraints_passed=True,
            material_limits_passed=True,
            strict_validation_required=False,
            validation_decision="rejected",
            validation_reason="control_learning_forbidden_for_execution",
            execution_allowed=False,
            explainable_required=True,
            validation_status="validated",
            description="Physics validation gate profile for control-learning path.",
        ),
    )

    approved_entries = sum(
        1 for entry in entries if entry.validation_decision == "approved"
    )
    review_entries = sum(
        1 for entry in entries if entry.validation_decision == "requires_review"
    )
    rejected_entries = sum(
        1 for entry in entries if entry.validation_decision == "rejected"
    )
    execution_allowed_entries = sum(
        1 for entry in entries if entry.execution_allowed
    )
    validated_entries = sum(
        1 for entry in entries if entry.validation_status == "validated"
    )

    return PhysicsValidationGateContract(
        total_entries=len(entries),
        approved_entries=approved_entries,
        review_entries=review_entries,
        rejected_entries=rejected_entries,
        execution_allowed_entries=execution_allowed_entries,
        validated_entries=validated_entries,
        entries=entries,
    )
