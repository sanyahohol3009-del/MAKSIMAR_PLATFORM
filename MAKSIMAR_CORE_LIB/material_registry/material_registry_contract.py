from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.constraint_profile_registry import (
    build_constraint_profile_registry_contract,
)


MaterialId = Literal[
    "material_aluminum_001",
    "material_steel_001",
    "material_acrylic_001",
    "material_wood_001",
]

ThermalBehavior = Literal[
    "high_conductivity",
    "medium_conductivity",
    "low_conductivity",
]

FractureProfile = Literal[
    "ductile",
    "brittle",
    "anisotropic",
]

MaterialRegistryStatus = Literal[
    "registered",
]


_MATERIAL_ID_PATTERN = re.compile(r"^material_[a-z][a-z0-9_]*$")
_CONSTRAINT_PROFILE_ID_PATTERN = re.compile(r"^constraint_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class MaterialRegistryEntry:
    """Canonical material registry entry."""

    material_id: MaterialId
    display_name: str
    density_kg_m3: int
    hardness_index: int
    roughness_index: int
    reflectivity_index: int
    thermal_behavior: ThermalBehavior
    fracture_profile: FractureProfile
    compatible_constraint_profile_ids: tuple[str, ...]
    production_usable: bool
    registry_status: MaterialRegistryStatus
    description: str

    def __post_init__(self) -> None:
        """Validate material registry invariants."""
        if not _MATERIAL_ID_PATTERN.fullmatch(self.material_id):
            raise ValueError(f"Invalid material_id: {self.material_id}")

        if not self.display_name.strip():
            raise ValueError(f"display_name must not be empty: {self.material_id}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty: {self.material_id}")

        if self.density_kg_m3 <= 0:
            raise ValueError(f"density_kg_m3 must be positive: {self.material_id}")

        for field_name, value in (
            ("hardness_index", self.hardness_index),
            ("roughness_index", self.roughness_index),
            ("reflectivity_index", self.reflectivity_index),
        ):
            if not 0 <= value <= 100:
                raise ValueError(
                    f"{field_name} must be within 0..100: {self.material_id}"
                )

        if not self.compatible_constraint_profile_ids:
            raise ValueError(
                f"compatible_constraint_profile_ids must not be empty: {self.material_id}"
            )

        if len(set(self.compatible_constraint_profile_ids)) != len(
            self.compatible_constraint_profile_ids
        ):
            raise ValueError(
                f"Duplicate compatible_constraint_profile_ids: {self.material_id}"
            )

        for profile_id in self.compatible_constraint_profile_ids:
            if not _CONSTRAINT_PROFILE_ID_PATTERN.fullmatch(profile_id):
                raise ValueError(
                    f"Invalid constraint profile id '{profile_id}': {self.material_id}"
                )

        if self.registry_status != "registered":
            raise ValueError(
                f"material entry must be registered: {self.material_id}"
            )

        if self.material_id == "material_aluminum_001":
            if self.thermal_behavior != "high_conductivity":
                raise ValueError(
                    f"Aluminum must map to high_conductivity: {self.material_id}"
                )
            if self.fracture_profile != "ductile":
                raise ValueError(
                    f"Aluminum must map to ductile: {self.material_id}"
                )

        if self.material_id == "material_steel_001":
            if self.thermal_behavior != "medium_conductivity":
                raise ValueError(
                    f"Steel must map to medium_conductivity: {self.material_id}"
                )
            if self.fracture_profile != "ductile":
                raise ValueError(
                    f"Steel must map to ductile: {self.material_id}"
                )

        if self.material_id == "material_acrylic_001":
            if self.thermal_behavior != "low_conductivity":
                raise ValueError(
                    f"Acrylic must map to low_conductivity: {self.material_id}"
                )
            if self.fracture_profile != "brittle":
                raise ValueError(
                    f"Acrylic must map to brittle: {self.material_id}"
                )

        if self.material_id == "material_wood_001":
            if self.thermal_behavior != "low_conductivity":
                raise ValueError(
                    f"Wood must map to low_conductivity: {self.material_id}"
                )
            if self.fracture_profile != "anisotropic":
                raise ValueError(
                    f"Wood must map to anisotropic: {self.material_id}"
                )


@dataclass(frozen=True, slots=True)
class MaterialRegistryContract:
    """Unified material registry contract."""

    total_entries: int
    production_usable_entries: int
    brittle_entries: int
    high_reflectivity_entries: int
    registered_entries: int
    entries: tuple[MaterialRegistryEntry, ...]

    def __post_init__(self) -> None:
        """Validate material registry contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        production_usable_entries = sum(
            1 for entry in self.entries if entry.production_usable
        )
        brittle_entries = sum(
            1 for entry in self.entries if entry.fracture_profile == "brittle"
        )
        high_reflectivity_entries = sum(
            1 for entry in self.entries if entry.reflectivity_index >= 70
        )
        registered_entries = sum(
            1 for entry in self.entries if entry.registry_status == "registered"
        )

        if self.production_usable_entries != production_usable_entries:
            raise ValueError(
                "production_usable_entries must match computed count"
            )

        if self.brittle_entries != brittle_entries:
            raise ValueError("brittle_entries must match computed count")

        if self.high_reflectivity_entries != high_reflectivity_entries:
            raise ValueError(
                "high_reflectivity_entries must match computed count"
            )

        if self.registered_entries != registered_entries:
            raise ValueError("registered_entries must match computed count")

        material_ids = tuple(entry.material_id for entry in self.entries)
        if len(set(material_ids)) != len(material_ids):
            raise ValueError("Duplicate material_id values detected")


def build_material_registry_contract() -> MaterialRegistryContract:
    """Build canonical material registry contract."""
    constraint_registry = build_constraint_profile_registry_contract()
    constraint_profile_ids = {
        entry.constraint_profile_id for entry in constraint_registry.entries
    }

    required_profiles = {
        "constraint_strict_execution_001",
        "constraint_engineering_candidate_001",
        "constraint_research_exploratory_001",
        "constraint_control_feedback_001",
    }
    missing_profiles = required_profiles - constraint_profile_ids
    if missing_profiles:
        raise ValueError(
            f"Missing required constraint profiles: {sorted(missing_profiles)}"
        )

    prod_profiles = (
        "constraint_strict_execution_001",
        "constraint_engineering_candidate_001",
    )
    all_profiles = (
        "constraint_strict_execution_001",
        "constraint_engineering_candidate_001",
        "constraint_research_exploratory_001",
        "constraint_control_feedback_001",
    )

    entries = (
        MaterialRegistryEntry(
            material_id="material_aluminum_001",
            display_name="Aluminum",
            density_kg_m3=2700,
            hardness_index=55,
            roughness_index=35,
            reflectivity_index=72,
            thermal_behavior="high_conductivity",
            fracture_profile="ductile",
            compatible_constraint_profile_ids=all_profiles,
            production_usable=True,
            registry_status="registered",
            description="General-purpose aluminum material profile.",
        ),
        MaterialRegistryEntry(
            material_id="material_steel_001",
            display_name="Steel",
            density_kg_m3=7850,
            hardness_index=78,
            roughness_index=42,
            reflectivity_index=58,
            thermal_behavior="medium_conductivity",
            fracture_profile="ductile",
            compatible_constraint_profile_ids=all_profiles,
            production_usable=True,
            registry_status="registered",
            description="General-purpose steel material profile.",
        ),
        MaterialRegistryEntry(
            material_id="material_acrylic_001",
            display_name="Acrylic",
            density_kg_m3=1180,
            hardness_index=32,
            roughness_index=28,
            reflectivity_index=64,
            thermal_behavior="low_conductivity",
            fracture_profile="brittle",
            compatible_constraint_profile_ids=prod_profiles,
            production_usable=True,
            registry_status="registered",
            description="Acrylic material profile for controlled machining and optics-aware work.",
        ),
        MaterialRegistryEntry(
            material_id="material_wood_001",
            display_name="Wood",
            density_kg_m3=700,
            hardness_index=24,
            roughness_index=61,
            reflectivity_index=18,
            thermal_behavior="low_conductivity",
            fracture_profile="anisotropic",
            compatible_constraint_profile_ids=all_profiles,
            production_usable=True,
            registry_status="registered",
            description="Wood material profile with anisotropic behavior.",
        ),
    )

    production_usable_entries = sum(
        1 for entry in entries if entry.production_usable
    )
    brittle_entries = sum(
        1 for entry in entries if entry.fracture_profile == "brittle"
    )
    high_reflectivity_entries = sum(
        1 for entry in entries if entry.reflectivity_index >= 70
    )
    registered_entries = sum(
        1 for entry in entries if entry.registry_status == "registered"
    )

    return MaterialRegistryContract(
        total_entries=len(entries),
        production_usable_entries=production_usable_entries,
        brittle_entries=brittle_entries,
        high_reflectivity_entries=high_reflectivity_entries,
        registered_entries=registered_entries,
        entries=entries,
    )
