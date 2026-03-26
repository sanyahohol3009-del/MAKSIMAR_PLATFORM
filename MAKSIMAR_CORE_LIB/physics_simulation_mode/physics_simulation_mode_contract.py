from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


PhysicsSimulationMode = Literal[
    "strict_physics",
    "engineering_realistic",
    "research_relaxed",
    "control_learning",
]

PhysicsTruthClass = Literal[
    "strict_engineering_truth",
    "engineering_candidate",
    "research_only",
    "control_feedback_only",
]

PhysicsExecutionEligibility = Literal[
    "allowed_for_execution",
    "requires_validation_gate",
    "forbidden_for_execution",
]

PhysicsDocumentationLevel = Literal[
    "full_trace_required",
    "engineering_summary_required",
    "research_trace_required",
    "control_feedback_trace_required",
]

PhysicsModeStatus = Literal[
    "defined",
]


_MODE_ENTRY_ID_PATTERN = re.compile(r"^physmode_[a-z][a-z0-9_]*$")
_MODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class PhysicsSimulationModeEntry:
    """Canonical physics simulation mode entry."""

    mode_entry_id: str
    simulation_mode: PhysicsSimulationMode
    truth_class: PhysicsTruthClass
    execution_eligibility: PhysicsExecutionEligibility
    strict_validation_required: bool
    material_registry_required: bool
    constraint_profile_required: bool
    documentation_level: PhysicsDocumentationLevel
    dashboard_explainable_required: bool
    production_path_allowed: bool
    research_path_allowed: bool
    mode_status: PhysicsModeStatus
    description: str

    def __post_init__(self) -> None:
        """Validate physics simulation mode invariants."""
        if not _MODE_ENTRY_ID_PATTERN.fullmatch(self.mode_entry_id):
            raise ValueError(f"Invalid mode_entry_id: {self.mode_entry_id}")

        if not _MODE_PATTERN.fullmatch(self.simulation_mode):
            raise ValueError(f"Invalid simulation_mode: {self.simulation_mode}")

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.mode_entry_id}"
            )

        if not self.material_registry_required:
            raise ValueError(
                f"material_registry_required must be True: {self.mode_entry_id}"
            )

        if not self.constraint_profile_required:
            raise ValueError(
                f"constraint_profile_required must be True: {self.mode_entry_id}"
            )

        if not self.dashboard_explainable_required:
            raise ValueError(
                f"dashboard_explainable_required must be True: {self.mode_entry_id}"
            )

        if self.mode_status != "defined":
            raise ValueError(
                f"physics mode entry must be defined: {self.mode_entry_id}"
            )

        if self.simulation_mode == "strict_physics":
            if self.truth_class != "strict_engineering_truth":
                raise ValueError(
                    f"strict_physics must map to strict_engineering_truth: {self.mode_entry_id}"
                )
            if self.execution_eligibility != "allowed_for_execution":
                raise ValueError(
                    f"strict_physics must be allowed_for_execution: {self.mode_entry_id}"
                )
            if not self.strict_validation_required:
                raise ValueError(
                    f"strict_physics must require strict validation: {self.mode_entry_id}"
                )
            if self.documentation_level != "full_trace_required":
                raise ValueError(
                    f"strict_physics must require full trace: {self.mode_entry_id}"
                )
            if not self.production_path_allowed:
                raise ValueError(
                    f"strict_physics must allow production path: {self.mode_entry_id}"
                )
            if self.research_path_allowed:
                raise ValueError(
                    f"strict_physics must not be research-only path: {self.mode_entry_id}"
                )

        if self.simulation_mode == "engineering_realistic":
            if self.truth_class != "engineering_candidate":
                raise ValueError(
                    f"engineering_realistic must map to engineering_candidate: {self.mode_entry_id}"
                )
            if self.execution_eligibility != "requires_validation_gate":
                raise ValueError(
                    f"engineering_realistic must require validation gate: {self.mode_entry_id}"
                )
            if not self.strict_validation_required:
                raise ValueError(
                    f"engineering_realistic must require strict validation: {self.mode_entry_id}"
                )
            if self.documentation_level != "engineering_summary_required":
                raise ValueError(
                    f"engineering_realistic must require engineering summary: {self.mode_entry_id}"
                )
            if not self.production_path_allowed:
                raise ValueError(
                    f"engineering_realistic must allow production path: {self.mode_entry_id}"
                )
            if self.research_path_allowed:
                raise ValueError(
                    f"engineering_realistic must not be research-only path: {self.mode_entry_id}"
                )

        if self.simulation_mode == "research_relaxed":
            if self.truth_class != "research_only":
                raise ValueError(
                    f"research_relaxed must map to research_only: {self.mode_entry_id}"
                )
            if self.execution_eligibility != "forbidden_for_execution":
                raise ValueError(
                    f"research_relaxed must be forbidden_for_execution: {self.mode_entry_id}"
                )
            if self.strict_validation_required:
                raise ValueError(
                    f"research_relaxed must not require strict validation for default research flow: {self.mode_entry_id}"
                )
            if self.documentation_level != "research_trace_required":
                raise ValueError(
                    f"research_relaxed must require research trace: {self.mode_entry_id}"
                )
            if self.production_path_allowed:
                raise ValueError(
                    f"research_relaxed must not allow production path: {self.mode_entry_id}"
                )
            if not self.research_path_allowed:
                raise ValueError(
                    f"research_relaxed must allow research path: {self.mode_entry_id}"
                )

        if self.simulation_mode == "control_learning":
            if self.truth_class != "control_feedback_only":
                raise ValueError(
                    f"control_learning must map to control_feedback_only: {self.mode_entry_id}"
                )
            if self.execution_eligibility != "forbidden_for_execution":
                raise ValueError(
                    f"control_learning must be forbidden_for_execution: {self.mode_entry_id}"
                )
            if self.strict_validation_required:
                raise ValueError(
                    f"control_learning must not require strict validation in default feedback path: {self.mode_entry_id}"
                )
            if self.documentation_level != "control_feedback_trace_required":
                raise ValueError(
                    f"control_learning must require control feedback trace: {self.mode_entry_id}"
                )
            if self.production_path_allowed:
                raise ValueError(
                    f"control_learning must not allow production path: {self.mode_entry_id}"
                )
            if not self.research_path_allowed:
                raise ValueError(
                    f"control_learning must allow research/control path: {self.mode_entry_id}"
                )


@dataclass(frozen=True, slots=True)
class PhysicsSimulationModeContract:
    """Unified physics simulation mode contract."""

    total_entries: int
    production_path_entries: int
    research_path_entries: int
    execution_allowed_entries: int
    defined_entries: int
    entries: tuple[PhysicsSimulationModeEntry, ...]

    def __post_init__(self) -> None:
        """Validate physics simulation mode contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        production_path_entries = sum(
            1 for entry in self.entries if entry.production_path_allowed
        )
        research_path_entries = sum(
            1 for entry in self.entries if entry.research_path_allowed
        )
        execution_allowed_entries = sum(
            1
            for entry in self.entries
            if entry.execution_eligibility == "allowed_for_execution"
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.mode_status == "defined"
        )

        if self.production_path_entries != production_path_entries:
            raise ValueError("production_path_entries must match computed count")

        if self.research_path_entries != research_path_entries:
            raise ValueError("research_path_entries must match computed count")

        if self.execution_allowed_entries != execution_allowed_entries:
            raise ValueError("execution_allowed_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.mode_entry_id for entry in self.entries)
        modes = tuple(entry.simulation_mode for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate mode_entry_id values detected")

        if len(set(modes)) != len(modes):
            raise ValueError("Duplicate simulation_mode values detected")


def build_physics_simulation_mode_contract() -> PhysicsSimulationModeContract:
    """Build canonical physics simulation mode contract."""
    entries = (
        PhysicsSimulationModeEntry(
            mode_entry_id="physmode_strict_physics_001",
            simulation_mode="strict_physics",
            truth_class="strict_engineering_truth",
            execution_eligibility="allowed_for_execution",
            strict_validation_required=True,
            material_registry_required=True,
            constraint_profile_required=True,
            documentation_level="full_trace_required",
            dashboard_explainable_required=True,
            production_path_allowed=True,
            research_path_allowed=False,
            mode_status="defined",
            description="Strict physics mode for execution-safe engineering truth.",
        ),
        PhysicsSimulationModeEntry(
            mode_entry_id="physmode_engineering_realistic_001",
            simulation_mode="engineering_realistic",
            truth_class="engineering_candidate",
            execution_eligibility="requires_validation_gate",
            strict_validation_required=True,
            material_registry_required=True,
            constraint_profile_required=True,
            documentation_level="engineering_summary_required",
            dashboard_explainable_required=True,
            production_path_allowed=True,
            research_path_allowed=False,
            mode_status="defined",
            description="Engineering-realistic mode for candidate results before validation gate.",
        ),
        PhysicsSimulationModeEntry(
            mode_entry_id="physmode_research_relaxed_001",
            simulation_mode="research_relaxed",
            truth_class="research_only",
            execution_eligibility="forbidden_for_execution",
            strict_validation_required=False,
            material_registry_required=True,
            constraint_profile_required=True,
            documentation_level="research_trace_required",
            dashboard_explainable_required=True,
            production_path_allowed=False,
            research_path_allowed=True,
            mode_status="defined",
            description="Research-relaxed mode for exploratory simulation only.",
        ),
        PhysicsSimulationModeEntry(
            mode_entry_id="physmode_control_learning_001",
            simulation_mode="control_learning",
            truth_class="control_feedback_only",
            execution_eligibility="forbidden_for_execution",
            strict_validation_required=False,
            material_registry_required=True,
            constraint_profile_required=True,
            documentation_level="control_feedback_trace_required",
            dashboard_explainable_required=True,
            production_path_allowed=False,
            research_path_allowed=True,
            mode_status="defined",
            description="Control-learning mode for feedback and learning traces only.",
        ),
    )

    production_path_entries = sum(
        1 for entry in entries if entry.production_path_allowed
    )
    research_path_entries = sum(
        1 for entry in entries if entry.research_path_allowed
    )
    execution_allowed_entries = sum(
        1
        for entry in entries
        if entry.execution_eligibility == "allowed_for_execution"
    )
    defined_entries = sum(
        1 for entry in entries if entry.mode_status == "defined"
    )

    return PhysicsSimulationModeContract(
        total_entries=len(entries),
        production_path_entries=production_path_entries,
        research_path_entries=research_path_entries,
        execution_allowed_entries=execution_allowed_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
