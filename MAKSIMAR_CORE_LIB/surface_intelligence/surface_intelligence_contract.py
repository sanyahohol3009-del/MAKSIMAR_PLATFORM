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


SurfaceScanMode = Literal[
    "full_surface_scan",
]

HeightMapResolutionClass = Literal[
    "fine",
    "medium",
]

SurfaceModelClass = Literal[
    "surface_height_model",
]

ToolProfileClass = Literal[
    "engraving_tip",
    "cutting_head",
]

CorrectionStrategy = Literal[
    "heightmap_based_compensation",
]

SurfaceContractStatus = Literal[
    "defined",
]


_SURFACE_ENTRY_ID_PATTERN = re.compile(r"^surfaceintel_[a-z][a-z0-9_]*$")
_MATERIAL_ID_PATTERN = re.compile(r"^material_[a-z][a-z0-9_]*$")
_CONSTRAINT_PROFILE_ID_PATTERN = re.compile(r"^constraint_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class SurfaceIntelligenceEntry:
    """Canonical surface intelligence entry."""

    surface_entry_id: str
    scan_mode: SurfaceScanMode
    height_map_resolution_class: HeightMapResolutionClass
    surface_model_class: SurfaceModelClass
    tool_profile_class: ToolProfileClass
    correction_strategy: CorrectionStrategy
    material_id: str
    constraint_profile_id: str
    full_scan_required: bool
    partial_probe_allowed: bool
    production_usable: bool
    explainable_required: bool
    contract_status: SurfaceContractStatus
    description: str

    def __post_init__(self) -> None:
        """Validate surface intelligence invariants."""
        if not _SURFACE_ENTRY_ID_PATTERN.fullmatch(self.surface_entry_id):
            raise ValueError(f"Invalid surface_entry_id: {self.surface_entry_id}")

        if not _MATERIAL_ID_PATTERN.fullmatch(self.material_id):
            raise ValueError(f"Invalid material_id: {self.material_id}")

        if not _CONSTRAINT_PROFILE_ID_PATTERN.fullmatch(self.constraint_profile_id):
            raise ValueError(
                f"Invalid constraint_profile_id: {self.constraint_profile_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.surface_entry_id}"
            )

        if self.scan_mode != "full_surface_scan":
            raise ValueError(
                f"surface intelligence must use full_surface_scan: {self.surface_entry_id}"
            )

        if self.surface_model_class != "surface_height_model":
            raise ValueError(
                f"surface intelligence must use surface_height_model: {self.surface_entry_id}"
            )

        if self.correction_strategy != "heightmap_based_compensation":
            raise ValueError(
                f"surface intelligence must use heightmap_based_compensation: {self.surface_entry_id}"
            )

        if not self.full_scan_required:
            raise ValueError(
                f"full_scan_required must be True: {self.surface_entry_id}"
            )

        if self.partial_probe_allowed:
            raise ValueError(
                f"partial_probe_allowed must be False at this step: {self.surface_entry_id}"
            )

        if not self.production_usable:
            raise ValueError(
                f"production_usable must be True: {self.surface_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.surface_entry_id}"
            )

        if self.contract_status != "defined":
            raise ValueError(
                f"surface intelligence contract must be defined: {self.surface_entry_id}"
            )

        if self.surface_entry_id == "surfaceintel_aluminum_engraving_001":
            if self.height_map_resolution_class != "fine":
                raise ValueError(
                    f"Aluminum engraving must use fine resolution: {self.surface_entry_id}"
                )
            if self.tool_profile_class != "engraving_tip":
                raise ValueError(
                    f"Aluminum engraving must use engraving_tip: {self.surface_entry_id}"
                )
            if self.material_id != "material_aluminum_001":
                raise ValueError(
                    f"Aluminum engraving must use material_aluminum_001: {self.surface_entry_id}"
                )
            if self.constraint_profile_id != "constraint_strict_execution_001":
                raise ValueError(
                    f"Aluminum engraving must use strict execution profile: {self.surface_entry_id}"
                )

        if self.surface_entry_id == "surfaceintel_steel_cutting_001":
            if self.height_map_resolution_class != "fine":
                raise ValueError(
                    f"Steel cutting must use fine resolution: {self.surface_entry_id}"
                )
            if self.tool_profile_class != "cutting_head":
                raise ValueError(
                    f"Steel cutting must use cutting_head: {self.surface_entry_id}"
                )
            if self.material_id != "material_steel_001":
                raise ValueError(
                    f"Steel cutting must use material_steel_001: {self.surface_entry_id}"
                )
            if self.constraint_profile_id != "constraint_engineering_candidate_001":
                raise ValueError(
                    f"Steel cutting must use engineering candidate profile: {self.surface_entry_id}"
                )

        if self.surface_entry_id == "surfaceintel_acrylic_engraving_001":
            if self.height_map_resolution_class != "medium":
                raise ValueError(
                    f"Acrylic engraving must use medium resolution: {self.surface_entry_id}"
                )
            if self.tool_profile_class != "engraving_tip":
                raise ValueError(
                    f"Acrylic engraving must use engraving_tip: {self.surface_entry_id}"
                )
            if self.material_id != "material_acrylic_001":
                raise ValueError(
                    f"Acrylic engraving must use material_acrylic_001: {self.surface_entry_id}"
                )
            if self.constraint_profile_id != "constraint_engineering_candidate_001":
                raise ValueError(
                    f"Acrylic engraving must use engineering candidate profile: {self.surface_entry_id}"
                )

        if self.surface_entry_id == "surfaceintel_wood_engraving_001":
            if self.height_map_resolution_class != "medium":
                raise ValueError(
                    f"Wood engraving must use medium resolution: {self.surface_entry_id}"
                )
            if self.tool_profile_class != "engraving_tip":
                raise ValueError(
                    f"Wood engraving must use engraving_tip: {self.surface_entry_id}"
                )
            if self.material_id != "material_wood_001":
                raise ValueError(
                    f"Wood engraving must use material_wood_001: {self.surface_entry_id}"
                )
            if self.constraint_profile_id != "constraint_strict_execution_001":
                raise ValueError(
                    f"Wood engraving must use strict execution profile: {self.surface_entry_id}"
                )


@dataclass(frozen=True, slots=True)
class SurfaceIntelligenceContract:
    """Unified surface intelligence contract."""

    total_entries: int
    fine_resolution_entries: int
    production_usable_entries: int
    explainable_entries: int
    defined_entries: int
    entries: tuple[SurfaceIntelligenceEntry, ...]

    def __post_init__(self) -> None:
        """Validate surface intelligence contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        fine_resolution_entries = sum(
            1 for entry in self.entries if entry.height_map_resolution_class == "fine"
        )
        production_usable_entries = sum(
            1 for entry in self.entries if entry.production_usable
        )
        explainable_entries = sum(
            1 for entry in self.entries if entry.explainable_required
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.contract_status == "defined"
        )

        if self.fine_resolution_entries != fine_resolution_entries:
            raise ValueError("fine_resolution_entries must match computed count")

        if self.production_usable_entries != production_usable_entries:
            raise ValueError("production_usable_entries must match computed count")

        if self.explainable_entries != explainable_entries:
            raise ValueError("explainable_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.surface_entry_id for entry in self.entries)
        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate surface_entry_id values detected")


def build_surface_intelligence_contract() -> SurfaceIntelligenceContract:
    """Build canonical surface intelligence contract."""
    material_registry = build_material_registry_contract()
    constraint_registry = build_constraint_profile_registry_contract()

    material_ids = {entry.material_id for entry in material_registry.entries}
    constraint_ids = {
        entry.constraint_profile_id for entry in constraint_registry.entries
    }

    required_materials = {
        "material_aluminum_001",
        "material_steel_001",
        "material_acrylic_001",
        "material_wood_001",
    }
    required_constraints = {
        "constraint_strict_execution_001",
        "constraint_engineering_candidate_001",
    }

    missing_materials = required_materials - material_ids
    if missing_materials:
        raise ValueError(
            f"Missing required materials: {sorted(missing_materials)}"
        )

    missing_constraints = required_constraints - constraint_ids
    if missing_constraints:
        raise ValueError(
            f"Missing required constraint profiles: {sorted(missing_constraints)}"
        )

    entries = (
        SurfaceIntelligenceEntry(
            surface_entry_id="surfaceintel_aluminum_engraving_001",
            scan_mode="full_surface_scan",
            height_map_resolution_class="fine",
            surface_model_class="surface_height_model",
            tool_profile_class="engraving_tip",
            correction_strategy="heightmap_based_compensation",
            material_id="material_aluminum_001",
            constraint_profile_id="constraint_strict_execution_001",
            full_scan_required=True,
            partial_probe_allowed=False,
            production_usable=True,
            explainable_required=True,
            contract_status="defined",
            description="Surface intelligence profile for aluminum engraving workflow.",
        ),
        SurfaceIntelligenceEntry(
            surface_entry_id="surfaceintel_steel_cutting_001",
            scan_mode="full_surface_scan",
            height_map_resolution_class="fine",
            surface_model_class="surface_height_model",
            tool_profile_class="cutting_head",
            correction_strategy="heightmap_based_compensation",
            material_id="material_steel_001",
            constraint_profile_id="constraint_engineering_candidate_001",
            full_scan_required=True,
            partial_probe_allowed=False,
            production_usable=True,
            explainable_required=True,
            contract_status="defined",
            description="Surface intelligence profile for steel cutting workflow.",
        ),
        SurfaceIntelligenceEntry(
            surface_entry_id="surfaceintel_acrylic_engraving_001",
            scan_mode="full_surface_scan",
            height_map_resolution_class="medium",
            surface_model_class="surface_height_model",
            tool_profile_class="engraving_tip",
            correction_strategy="heightmap_based_compensation",
            material_id="material_acrylic_001",
            constraint_profile_id="constraint_engineering_candidate_001",
            full_scan_required=True,
            partial_probe_allowed=False,
            production_usable=True,
            explainable_required=True,
            contract_status="defined",
            description="Surface intelligence profile for acrylic engraving workflow.",
        ),
        SurfaceIntelligenceEntry(
            surface_entry_id="surfaceintel_wood_engraving_001",
            scan_mode="full_surface_scan",
            height_map_resolution_class="medium",
            surface_model_class="surface_height_model",
            tool_profile_class="engraving_tip",
            correction_strategy="heightmap_based_compensation",
            material_id="material_wood_001",
            constraint_profile_id="constraint_strict_execution_001",
            full_scan_required=True,
            partial_probe_allowed=False,
            production_usable=True,
            explainable_required=True,
            contract_status="defined",
            description="Surface intelligence profile for wood engraving workflow.",
        ),
    )

    fine_resolution_entries = sum(
        1 for entry in entries if entry.height_map_resolution_class == "fine"
    )
    production_usable_entries = sum(
        1 for entry in entries if entry.production_usable
    )
    explainable_entries = sum(
        1 for entry in entries if entry.explainable_required
    )
    defined_entries = sum(
        1 for entry in entries if entry.contract_status == "defined"
    )

    return SurfaceIntelligenceContract(
        total_entries=len(entries),
        fine_resolution_entries=fine_resolution_entries,
        production_usable_entries=production_usable_entries,
        explainable_entries=explainable_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
