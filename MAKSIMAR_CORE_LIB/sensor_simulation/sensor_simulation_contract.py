from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.material_registry import (
    build_material_registry_contract,
)
from MAKSIMAR_CORE_LIB.surface_intelligence import (
    build_surface_intelligence_contract,
)


SensorSimulationMode = Literal[
    "surface_scan_simulation",
]

NoiseModelClass = Literal[
    "low_noise",
    "medium_noise",
]

ReflectionModelClass = Literal[
    "diffuse_weighted",
    "reflective_adjusted",
]

SensorOutputQuality = Literal[
    "high_fidelity",
    "engineering_grade",
]

SensorExecutionEligibility = Literal[
    "allowed_for_precompute",
    "requires_validation_gate",
]

SensorSimulationStatus = Literal[
    "defined",
]


_SENSOR_ENTRY_ID_PATTERN = re.compile(r"^sensorsim_[a-z][a-z0-9_]*$")
_SURFACE_ENTRY_ID_PATTERN = re.compile(r"^surfaceintel_[a-z][a-z0-9_]*$")
_MATERIAL_ID_PATTERN = re.compile(r"^material_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class SensorSimulationEntry:
    """Canonical sensor simulation entry."""

    sensor_entry_id: str
    simulation_mode: SensorSimulationMode
    surface_entry_id: str
    material_id: str
    noise_model_class: NoiseModelClass
    reflection_model_class: ReflectionModelClass
    output_quality: SensorOutputQuality
    full_surface_scan_required: bool
    precompute_allowed: bool
    validation_gate_required: bool
    explainable_required: bool
    production_usable: bool
    simulation_status: SensorSimulationStatus
    description: str

    def __post_init__(self) -> None:
        """Validate sensor simulation invariants."""
        if not _SENSOR_ENTRY_ID_PATTERN.fullmatch(self.sensor_entry_id):
            raise ValueError(f"Invalid sensor_entry_id: {self.sensor_entry_id}")

        if not _SURFACE_ENTRY_ID_PATTERN.fullmatch(self.surface_entry_id):
            raise ValueError(f"Invalid surface_entry_id: {self.surface_entry_id}")

        if not _MATERIAL_ID_PATTERN.fullmatch(self.material_id):
            raise ValueError(f"Invalid material_id: {self.material_id}")

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.sensor_entry_id}"
            )

        if self.simulation_mode != "surface_scan_simulation":
            raise ValueError(
                f"sensor simulation must use surface_scan_simulation: {self.sensor_entry_id}"
            )

        if not self.full_surface_scan_required:
            raise ValueError(
                f"full_surface_scan_required must be True: {self.sensor_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.sensor_entry_id}"
            )

        if not self.production_usable:
            raise ValueError(
                f"production_usable must be True: {self.sensor_entry_id}"
            )

        if self.simulation_status != "defined":
            raise ValueError(
                f"sensor simulation must be defined: {self.sensor_entry_id}"
            )

        if self.sensor_entry_id == "sensorsim_aluminum_001":
            if self.surface_entry_id != "surfaceintel_aluminum_engraving_001":
                raise ValueError(
                    f"sensorsim_aluminum_001 must use aluminum surface profile: {self.sensor_entry_id}"
                )
            if self.material_id != "material_aluminum_001":
                raise ValueError(
                    f"sensorsim_aluminum_001 must use material_aluminum_001: {self.sensor_entry_id}"
                )
            if self.noise_model_class != "low_noise":
                raise ValueError(
                    f"sensorsim_aluminum_001 must use low_noise: {self.sensor_entry_id}"
                )
            if self.reflection_model_class != "reflective_adjusted":
                raise ValueError(
                    f"sensorsim_aluminum_001 must use reflective_adjusted: {self.sensor_entry_id}"
                )
            if self.output_quality != "high_fidelity":
                raise ValueError(
                    f"sensorsim_aluminum_001 must use high_fidelity: {self.sensor_entry_id}"
                )
            if not self.precompute_allowed:
                raise ValueError(
                    f"sensorsim_aluminum_001 must allow precompute: {self.sensor_entry_id}"
                )
            if self.validation_gate_required:
                raise ValueError(
                    f"sensorsim_aluminum_001 must not require validation gate at sensor stage: {self.sensor_entry_id}"
                )

        if self.sensor_entry_id == "sensorsim_steel_001":
            if self.surface_entry_id != "surfaceintel_steel_cutting_001":
                raise ValueError(
                    f"sensorsim_steel_001 must use steel surface profile: {self.sensor_entry_id}"
                )
            if self.material_id != "material_steel_001":
                raise ValueError(
                    f"sensorsim_steel_001 must use material_steel_001: {self.sensor_entry_id}"
                )
            if self.noise_model_class != "medium_noise":
                raise ValueError(
                    f"sensorsim_steel_001 must use medium_noise: {self.sensor_entry_id}"
                )
            if self.reflection_model_class != "reflective_adjusted":
                raise ValueError(
                    f"sensorsim_steel_001 must use reflective_adjusted: {self.sensor_entry_id}"
                )
            if self.output_quality != "engineering_grade":
                raise ValueError(
                    f"sensorsim_steel_001 must use engineering_grade: {self.sensor_entry_id}"
                )
            if not self.precompute_allowed:
                raise ValueError(
                    f"sensorsim_steel_001 must allow precompute: {self.sensor_entry_id}"
                )
            if not self.validation_gate_required:
                raise ValueError(
                    f"sensorsim_steel_001 must require validation gate: {self.sensor_entry_id}"
                )

        if self.sensor_entry_id == "sensorsim_acrylic_001":
            if self.surface_entry_id != "surfaceintel_acrylic_engraving_001":
                raise ValueError(
                    f"sensorsim_acrylic_001 must use acrylic surface profile: {self.sensor_entry_id}"
                )
            if self.material_id != "material_acrylic_001":
                raise ValueError(
                    f"sensorsim_acrylic_001 must use material_acrylic_001: {self.sensor_entry_id}"
                )
            if self.noise_model_class != "medium_noise":
                raise ValueError(
                    f"sensorsim_acrylic_001 must use medium_noise: {self.sensor_entry_id}"
                )
            if self.reflection_model_class != "diffuse_weighted":
                raise ValueError(
                    f"sensorsim_acrylic_001 must use diffuse_weighted: {self.sensor_entry_id}"
                )
            if self.output_quality != "engineering_grade":
                raise ValueError(
                    f"sensorsim_acrylic_001 must use engineering_grade: {self.sensor_entry_id}"
                )
            if not self.precompute_allowed:
                raise ValueError(
                    f"sensorsim_acrylic_001 must allow precompute: {self.sensor_entry_id}"
                )
            if not self.validation_gate_required:
                raise ValueError(
                    f"sensorsim_acrylic_001 must require validation gate: {self.sensor_entry_id}"
                )

        if self.sensor_entry_id == "sensorsim_wood_001":
            if self.surface_entry_id != "surfaceintel_wood_engraving_001":
                raise ValueError(
                    f"sensorsim_wood_001 must use wood surface profile: {self.sensor_entry_id}"
                )
            if self.material_id != "material_wood_001":
                raise ValueError(
                    f"sensorsim_wood_001 must use material_wood_001: {self.sensor_entry_id}"
                )
            if self.noise_model_class != "medium_noise":
                raise ValueError(
                    f"sensorsim_wood_001 must use medium_noise: {self.sensor_entry_id}"
                )
            if self.reflection_model_class != "diffuse_weighted":
                raise ValueError(
                    f"sensorsim_wood_001 must use diffuse_weighted: {self.sensor_entry_id}"
                )
            if self.output_quality != "engineering_grade":
                raise ValueError(
                    f"sensorsim_wood_001 must use engineering_grade: {self.sensor_entry_id}"
                )
            if not self.precompute_allowed:
                raise ValueError(
                    f"sensorsim_wood_001 must allow precompute: {self.sensor_entry_id}"
                )
            if self.validation_gate_required:
                raise ValueError(
                    f"sensorsim_wood_001 must not require validation gate at sensor stage: {self.sensor_entry_id}"
                )


@dataclass(frozen=True, slots=True)
class SensorSimulationContract:
    """Unified sensor simulation contract."""

    total_entries: int
    high_fidelity_entries: int
    validation_gate_entries: int
    production_usable_entries: int
    defined_entries: int
    entries: tuple[SensorSimulationEntry, ...]

    def __post_init__(self) -> None:
        """Validate sensor simulation contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        high_fidelity_entries = sum(
            1 for entry in self.entries if entry.output_quality == "high_fidelity"
        )
        validation_gate_entries = sum(
            1 for entry in self.entries if entry.validation_gate_required
        )
        production_usable_entries = sum(
            1 for entry in self.entries if entry.production_usable
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.simulation_status == "defined"
        )

        if self.high_fidelity_entries != high_fidelity_entries:
            raise ValueError("high_fidelity_entries must match computed count")

        if self.validation_gate_entries != validation_gate_entries:
            raise ValueError("validation_gate_entries must match computed count")

        if self.production_usable_entries != production_usable_entries:
            raise ValueError("production_usable_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.sensor_entry_id for entry in self.entries)
        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate sensor_entry_id values detected")


def build_sensor_simulation_contract() -> SensorSimulationContract:
    """Build canonical sensor simulation contract."""
    surface_contract = build_surface_intelligence_contract()
    material_contract = build_material_registry_contract()

    surface_ids = {entry.surface_entry_id for entry in surface_contract.entries}
    material_ids = {entry.material_id for entry in material_contract.entries}

    required_surface_ids = {
        "surfaceintel_aluminum_engraving_001",
        "surfaceintel_steel_cutting_001",
        "surfaceintel_acrylic_engraving_001",
        "surfaceintel_wood_engraving_001",
    }
    required_material_ids = {
        "material_aluminum_001",
        "material_steel_001",
        "material_acrylic_001",
        "material_wood_001",
    }

    missing_surface_ids = required_surface_ids - surface_ids
    if missing_surface_ids:
        raise ValueError(
            f"Missing required surface intelligence entries: {sorted(missing_surface_ids)}"
        )

    missing_material_ids = required_material_ids - material_ids
    if missing_material_ids:
        raise ValueError(
            f"Missing required material entries: {sorted(missing_material_ids)}"
        )

    entries = (
        SensorSimulationEntry(
            sensor_entry_id="sensorsim_aluminum_001",
            simulation_mode="surface_scan_simulation",
            surface_entry_id="surfaceintel_aluminum_engraving_001",
            material_id="material_aluminum_001",
            noise_model_class="low_noise",
            reflection_model_class="reflective_adjusted",
            output_quality="high_fidelity",
            full_surface_scan_required=True,
            precompute_allowed=True,
            validation_gate_required=False,
            explainable_required=True,
            production_usable=True,
            simulation_status="defined",
            description="Sensor simulation profile for aluminum surface scan.",
        ),
        SensorSimulationEntry(
            sensor_entry_id="sensorsim_steel_001",
            simulation_mode="surface_scan_simulation",
            surface_entry_id="surfaceintel_steel_cutting_001",
            material_id="material_steel_001",
            noise_model_class="medium_noise",
            reflection_model_class="reflective_adjusted",
            output_quality="engineering_grade",
            full_surface_scan_required=True,
            precompute_allowed=True,
            validation_gate_required=True,
            explainable_required=True,
            production_usable=True,
            simulation_status="defined",
            description="Sensor simulation profile for steel surface scan.",
        ),
        SensorSimulationEntry(
            sensor_entry_id="sensorsim_acrylic_001",
            simulation_mode="surface_scan_simulation",
            surface_entry_id="surfaceintel_acrylic_engraving_001",
            material_id="material_acrylic_001",
            noise_model_class="medium_noise",
            reflection_model_class="diffuse_weighted",
            output_quality="engineering_grade",
            full_surface_scan_required=True,
            precompute_allowed=True,
            validation_gate_required=True,
            explainable_required=True,
            production_usable=True,
            simulation_status="defined",
            description="Sensor simulation profile for acrylic surface scan.",
        ),
        SensorSimulationEntry(
            sensor_entry_id="sensorsim_wood_001",
            simulation_mode="surface_scan_simulation",
            surface_entry_id="surfaceintel_wood_engraving_001",
            material_id="material_wood_001",
            noise_model_class="medium_noise",
            reflection_model_class="diffuse_weighted",
            output_quality="engineering_grade",
            full_surface_scan_required=True,
            precompute_allowed=True,
            validation_gate_required=False,
            explainable_required=True,
            production_usable=True,
            simulation_status="defined",
            description="Sensor simulation profile for wood surface scan.",
        ),
    )

    high_fidelity_entries = sum(
        1 for entry in entries if entry.output_quality == "high_fidelity"
    )
    validation_gate_entries = sum(
        1 for entry in entries if entry.validation_gate_required
    )
    production_usable_entries = sum(
        1 for entry in entries if entry.production_usable
    )
    defined_entries = sum(
        1 for entry in entries if entry.simulation_status == "defined"
    )

    return SensorSimulationContract(
        total_entries=len(entries),
        high_fidelity_entries=high_fidelity_entries,
        validation_gate_entries=validation_gate_entries,
        production_usable_entries=production_usable_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
