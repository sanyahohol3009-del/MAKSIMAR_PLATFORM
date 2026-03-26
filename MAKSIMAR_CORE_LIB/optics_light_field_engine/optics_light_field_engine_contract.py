from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.constraint_profile_registry import (
    build_constraint_profile_registry_contract,
)
from MAKSIMAR_CORE_LIB.physics_simulation_mode import (
    build_physics_simulation_mode_contract,
)
from MAKSIMAR_CORE_LIB.physics_validation_gate import (
    build_physics_validation_gate_contract,
)


OpticsMode = Literal[
    "ar_glasses_projection",
    "projection_assisted_spatial",
    "controlled_scattering_research",
    "beam_intersection_research",
]

BeamModelClass = Literal[
    "guided_projection",
    "free_space_projection",
    "controlled_scattering",
    "intersection_field",
]

EnergyEnvelopeClass = Literal[
    "low_energy_safe",
    "bounded_energy_research",
]

VisibilityClass = Literal[
    "private_display",
    "shared_projection",
    "research_visibility_only",
]

DisplayModeSelection = Literal[
    "ar_glasses_display",
    "wall_projection_display",
    "research_optics_display",
]

ExecutionEligibility = Literal[
    "allowed_for_private_display",
    "requires_validation_gate",
    "forbidden_for_execution",
]

OpticsEngineStatus = Literal[
    "defined",
]


_ENGINE_ENTRY_ID_PATTERN = re.compile(r"^opticsengine_[a-z][a-z0-9_]*$")
_MODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_CONSTRAINT_PROFILE_ID_PATTERN = re.compile(r"^constraint_[a-z][a-z0-9_]*$")
_GATE_ENTRY_ID_PATTERN = re.compile(r"^physgate_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class OpticsLightFieldEngineEntry:
    """Canonical optics / light field engine entry."""

    engine_entry_id: str
    optics_mode: OpticsMode
    simulation_mode: str
    constraint_profile_id: str
    physics_gate_entry_id: str
    beam_model_class: BeamModelClass
    energy_envelope_class: EnergyEnvelopeClass
    visibility_class: VisibilityClass
    display_mode_selection: DisplayModeSelection
    safety_limits_required: bool
    visibility_score_required: bool
    intersection_geometry_required: bool
    execution_eligibility: ExecutionEligibility
    research_only: bool
    explainable_required: bool
    engine_status: OpticsEngineStatus
    description: str

    def __post_init__(self) -> None:
        """Validate optics engine invariants."""
        if not _ENGINE_ENTRY_ID_PATTERN.fullmatch(self.engine_entry_id):
            raise ValueError(f"Invalid engine_entry_id: {self.engine_entry_id}")

        if not _MODE_PATTERN.fullmatch(self.simulation_mode):
            raise ValueError(f"Invalid simulation_mode: {self.simulation_mode}")

        if not _CONSTRAINT_PROFILE_ID_PATTERN.fullmatch(self.constraint_profile_id):
            raise ValueError(
                f"Invalid constraint_profile_id: {self.constraint_profile_id}"
            )

        if not _GATE_ENTRY_ID_PATTERN.fullmatch(self.physics_gate_entry_id):
            raise ValueError(
                f"Invalid physics_gate_entry_id: {self.physics_gate_entry_id}"
            )

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.engine_entry_id}")

        if not self.safety_limits_required:
            raise ValueError(
                f"safety_limits_required must be True: {self.engine_entry_id}"
            )

        if not self.visibility_score_required:
            raise ValueError(
                f"visibility_score_required must be True: {self.engine_entry_id}"
            )

        if not self.intersection_geometry_required:
            raise ValueError(
                f"intersection_geometry_required must be True: {self.engine_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.engine_entry_id}"
            )

        if self.engine_status != "defined":
            raise ValueError(
                f"optics engine entry must be defined: {self.engine_entry_id}"
            )

        if self.optics_mode == "ar_glasses_projection":
            if self.simulation_mode != "strict_physics":
                raise ValueError(
                    f"ar_glasses_projection must use strict_physics: {self.engine_entry_id}"
                )
            if self.constraint_profile_id != "constraint_strict_execution_001":
                raise ValueError(
                    f"ar_glasses_projection must use strict execution constraint profile: {self.engine_entry_id}"
                )
            if self.physics_gate_entry_id != "physgate_strict_physics_001":
                raise ValueError(
                    f"ar_glasses_projection must use strict physics gate: {self.engine_entry_id}"
                )
            if self.beam_model_class != "guided_projection":
                raise ValueError(
                    f"ar_glasses_projection must use guided_projection: {self.engine_entry_id}"
                )
            if self.energy_envelope_class != "low_energy_safe":
                raise ValueError(
                    f"ar_glasses_projection must use low_energy_safe: {self.engine_entry_id}"
                )
            if self.visibility_class != "private_display":
                raise ValueError(
                    f"ar_glasses_projection must use private_display: {self.engine_entry_id}"
                )
            if self.display_mode_selection != "ar_glasses_display":
                raise ValueError(
                    f"ar_glasses_projection must use ar_glasses_display: {self.engine_entry_id}"
                )
            if self.execution_eligibility != "allowed_for_private_display":
                raise ValueError(
                    f"ar_glasses_projection must be allowed_for_private_display: {self.engine_entry_id}"
                )
            if self.research_only:
                raise ValueError(
                    f"ar_glasses_projection must not be research_only: {self.engine_entry_id}"
                )

        if self.optics_mode == "projection_assisted_spatial":
            if self.simulation_mode != "engineering_realistic":
                raise ValueError(
                    f"projection_assisted_spatial must use engineering_realistic: {self.engine_entry_id}"
                )
            if self.constraint_profile_id != "constraint_engineering_candidate_001":
                raise ValueError(
                    f"projection_assisted_spatial must use engineering candidate profile: {self.engine_entry_id}"
                )
            if self.physics_gate_entry_id != "physgate_engineering_realistic_001":
                raise ValueError(
                    f"projection_assisted_spatial must use engineering physics gate: {self.engine_entry_id}"
                )
            if self.beam_model_class != "free_space_projection":
                raise ValueError(
                    f"projection_assisted_spatial must use free_space_projection: {self.engine_entry_id}"
                )
            if self.energy_envelope_class != "low_energy_safe":
                raise ValueError(
                    f"projection_assisted_spatial must use low_energy_safe: {self.engine_entry_id}"
                )
            if self.visibility_class != "shared_projection":
                raise ValueError(
                    f"projection_assisted_spatial must use shared_projection: {self.engine_entry_id}"
                )
            if self.display_mode_selection != "wall_projection_display":
                raise ValueError(
                    f"projection_assisted_spatial must use wall_projection_display: {self.engine_entry_id}"
                )
            if self.execution_eligibility != "requires_validation_gate":
                raise ValueError(
                    f"projection_assisted_spatial must require validation gate: {self.engine_entry_id}"
                )
            if self.research_only:
                raise ValueError(
                    f"projection_assisted_spatial must not be research_only: {self.engine_entry_id}"
                )

        if self.optics_mode == "controlled_scattering_research":
            if self.simulation_mode != "research_relaxed":
                raise ValueError(
                    f"controlled_scattering_research must use research_relaxed: {self.engine_entry_id}"
                )
            if self.constraint_profile_id != "constraint_research_exploratory_001":
                raise ValueError(
                    f"controlled_scattering_research must use research exploratory profile: {self.engine_entry_id}"
                )
            if self.physics_gate_entry_id != "physgate_research_relaxed_001":
                raise ValueError(
                    f"controlled_scattering_research must use research physics gate: {self.engine_entry_id}"
                )
            if self.beam_model_class != "controlled_scattering":
                raise ValueError(
                    f"controlled_scattering_research must use controlled_scattering: {self.engine_entry_id}"
                )
            if self.energy_envelope_class != "bounded_energy_research":
                raise ValueError(
                    f"controlled_scattering_research must use bounded_energy_research: {self.engine_entry_id}"
                )
            if self.visibility_class != "research_visibility_only":
                raise ValueError(
                    f"controlled_scattering_research must use research_visibility_only: {self.engine_entry_id}"
                )
            if self.display_mode_selection != "research_optics_display":
                raise ValueError(
                    f"controlled_scattering_research must use research_optics_display: {self.engine_entry_id}"
                )
            if self.execution_eligibility != "forbidden_for_execution":
                raise ValueError(
                    f"controlled_scattering_research must be forbidden_for_execution: {self.engine_entry_id}"
                )
            if not self.research_only:
                raise ValueError(
                    f"controlled_scattering_research must be research_only: {self.engine_entry_id}"
                )

        if self.optics_mode == "beam_intersection_research":
            if self.simulation_mode != "control_learning":
                raise ValueError(
                    f"beam_intersection_research must use control_learning: {self.engine_entry_id}"
                )
            if self.constraint_profile_id != "constraint_control_feedback_001":
                raise ValueError(
                    f"beam_intersection_research must use control feedback profile: {self.engine_entry_id}"
                )
            if self.physics_gate_entry_id != "physgate_control_learning_001":
                raise ValueError(
                    f"beam_intersection_research must use control learning physics gate: {self.engine_entry_id}"
                )
            if self.beam_model_class != "intersection_field":
                raise ValueError(
                    f"beam_intersection_research must use intersection_field: {self.engine_entry_id}"
                )
            if self.energy_envelope_class != "bounded_energy_research":
                raise ValueError(
                    f"beam_intersection_research must use bounded_energy_research: {self.engine_entry_id}"
                )
            if self.visibility_class != "research_visibility_only":
                raise ValueError(
                    f"beam_intersection_research must use research_visibility_only: {self.engine_entry_id}"
                )
            if self.display_mode_selection != "research_optics_display":
                raise ValueError(
                    f"beam_intersection_research must use research_optics_display: {self.engine_entry_id}"
                )
            if self.execution_eligibility != "forbidden_for_execution":
                raise ValueError(
                    f"beam_intersection_research must be forbidden_for_execution: {self.engine_entry_id}"
                )
            if not self.research_only:
                raise ValueError(
                    f"beam_intersection_research must be research_only: {self.engine_entry_id}"
                )


@dataclass(frozen=True, slots=True)
class OpticsLightFieldEngineContract:
    """Unified optics / light field engine contract."""

    total_entries: int
    private_display_entries: int
    shared_projection_entries: int
    research_only_entries: int
    execution_allowed_entries: int
    defined_entries: int
    entries: tuple[OpticsLightFieldEngineEntry, ...]

    def __post_init__(self) -> None:
        """Validate optics engine contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        private_display_entries = sum(
            1 for entry in self.entries if entry.visibility_class == "private_display"
        )
        shared_projection_entries = sum(
            1 for entry in self.entries if entry.visibility_class == "shared_projection"
        )
        research_only_entries = sum(
            1 for entry in self.entries if entry.research_only
        )
        execution_allowed_entries = sum(
            1
            for entry in self.entries
            if entry.execution_eligibility == "allowed_for_private_display"
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.engine_status == "defined"
        )

        if self.private_display_entries != private_display_entries:
            raise ValueError("private_display_entries must match computed count")

        if self.shared_projection_entries != shared_projection_entries:
            raise ValueError("shared_projection_entries must match computed count")

        if self.research_only_entries != research_only_entries:
            raise ValueError("research_only_entries must match computed count")

        if self.execution_allowed_entries != execution_allowed_entries:
            raise ValueError("execution_allowed_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.engine_entry_id for entry in self.entries)
        modes = tuple(entry.optics_mode for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate engine_entry_id values detected")

        if len(set(modes)) != len(modes):
            raise ValueError("Duplicate optics_mode values detected")


def build_optics_light_field_engine_contract() -> OpticsLightFieldEngineContract:
    """Build canonical optics / light field engine contract."""
    simulation_mode_contract = build_physics_simulation_mode_contract()
    constraint_registry = build_constraint_profile_registry_contract()
    physics_gate = build_physics_validation_gate_contract()

    simulation_modes = {entry.simulation_mode for entry in simulation_mode_contract.entries}
    constraint_ids = {entry.constraint_profile_id for entry in constraint_registry.entries}
    gate_ids = {entry.gate_entry_id for entry in physics_gate.entries}

    required_simulation_modes = {
        "strict_physics",
        "engineering_realistic",
        "research_relaxed",
        "control_learning",
    }
    required_constraint_ids = {
        "constraint_strict_execution_001",
        "constraint_engineering_candidate_001",
        "constraint_research_exploratory_001",
        "constraint_control_feedback_001",
    }
    required_gate_ids = {
        "physgate_strict_physics_001",
        "physgate_engineering_realistic_001",
        "physgate_research_relaxed_001",
        "physgate_control_learning_001",
    }

    missing_modes = required_simulation_modes - simulation_modes
    if missing_modes:
        raise ValueError(f"Missing simulation modes: {sorted(missing_modes)}")

    missing_constraints = required_constraint_ids - constraint_ids
    if missing_constraints:
        raise ValueError(
            f"Missing constraint profiles: {sorted(missing_constraints)}"
        )

    missing_gates = required_gate_ids - gate_ids
    if missing_gates:
        raise ValueError(f"Missing physics gate ids: {sorted(missing_gates)}")

    entries = (
        OpticsLightFieldEngineEntry(
            engine_entry_id="opticsengine_ar_glasses_projection_001",
            optics_mode="ar_glasses_projection",
            simulation_mode="strict_physics",
            constraint_profile_id="constraint_strict_execution_001",
            physics_gate_entry_id="physgate_strict_physics_001",
            beam_model_class="guided_projection",
            energy_envelope_class="low_energy_safe",
            visibility_class="private_display",
            display_mode_selection="ar_glasses_display",
            safety_limits_required=True,
            visibility_score_required=True,
            intersection_geometry_required=True,
            execution_eligibility="allowed_for_private_display",
            research_only=False,
            explainable_required=True,
            engine_status="defined",
            description="Optics engine profile for AR glasses private projection.",
        ),
        OpticsLightFieldEngineEntry(
            engine_entry_id="opticsengine_projection_assisted_spatial_001",
            optics_mode="projection_assisted_spatial",
            simulation_mode="engineering_realistic",
            constraint_profile_id="constraint_engineering_candidate_001",
            physics_gate_entry_id="physgate_engineering_realistic_001",
            beam_model_class="free_space_projection",
            energy_envelope_class="low_energy_safe",
            visibility_class="shared_projection",
            display_mode_selection="wall_projection_display",
            safety_limits_required=True,
            visibility_score_required=True,
            intersection_geometry_required=True,
            execution_eligibility="requires_validation_gate",
            research_only=False,
            explainable_required=True,
            engine_status="defined",
            description="Optics engine profile for projection-assisted spatial display.",
        ),
        OpticsLightFieldEngineEntry(
            engine_entry_id="opticsengine_controlled_scattering_research_001",
            optics_mode="controlled_scattering_research",
            simulation_mode="research_relaxed",
            constraint_profile_id="constraint_research_exploratory_001",
            physics_gate_entry_id="physgate_research_relaxed_001",
            beam_model_class="controlled_scattering",
            energy_envelope_class="bounded_energy_research",
            visibility_class="research_visibility_only",
            display_mode_selection="research_optics_display",
            safety_limits_required=True,
            visibility_score_required=True,
            intersection_geometry_required=True,
            execution_eligibility="forbidden_for_execution",
            research_only=True,
            explainable_required=True,
            engine_status="defined",
            description="Optics engine profile for controlled scattering research path.",
        ),
        OpticsLightFieldEngineEntry(
            engine_entry_id="opticsengine_beam_intersection_research_001",
            optics_mode="beam_intersection_research",
            simulation_mode="control_learning",
            constraint_profile_id="constraint_control_feedback_001",
            physics_gate_entry_id="physgate_control_learning_001",
            beam_model_class="intersection_field",
            energy_envelope_class="bounded_energy_research",
            visibility_class="research_visibility_only",
            display_mode_selection="research_optics_display",
            safety_limits_required=True,
            visibility_score_required=True,
            intersection_geometry_required=True,
            execution_eligibility="forbidden_for_execution",
            research_only=True,
            explainable_required=True,
            engine_status="defined",
            description="Optics engine profile for beam intersection research path.",
        ),
    )

    private_display_entries = sum(
        1 for entry in entries if entry.visibility_class == "private_display"
    )
    shared_projection_entries = sum(
        1 for entry in entries if entry.visibility_class == "shared_projection"
    )
    research_only_entries = sum(
        1 for entry in entries if entry.research_only
    )
    execution_allowed_entries = sum(
        1
        for entry in entries
        if entry.execution_eligibility == "allowed_for_private_display"
    )
    defined_entries = sum(
        1 for entry in entries if entry.engine_status == "defined"
    )

    return OpticsLightFieldEngineContract(
        total_entries=len(entries),
        private_display_entries=private_display_entries,
        shared_projection_entries=shared_projection_entries,
        research_only_entries=research_only_entries,
        execution_allowed_entries=execution_allowed_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
