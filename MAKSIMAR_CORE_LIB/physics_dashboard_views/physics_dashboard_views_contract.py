from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.material_registry import (
    build_material_registry_contract,
)
from MAKSIMAR_CORE_LIB.optics_light_field_engine import (
    build_optics_light_field_engine_contract,
)
from MAKSIMAR_CORE_LIB.physics_validation_gate import (
    build_physics_validation_gate_contract,
)
from MAKSIMAR_CORE_LIB.surface_intelligence import (
    build_surface_intelligence_contract,
)


PhysicsPanelId = Literal[
    "panel_surface_map_001",
    "panel_material_profile_001",
    "panel_validation_report_001",
    "panel_optics_mode_001",
    "panel_project_export_001",
]

PhysicsViewKind = Literal[
    "surface_map_view",
    "material_profile_view",
    "validation_report_view",
    "optics_mode_view",
    "project_export_view",
]

DisplayRole = Literal[
    "engineering_display",
    "primary_dashboard_display",
]

DashboardVisibilityMode = Literal[
    "read_only",
]

PhysicsDashboardStatus = Literal[
    "defined",
]


_PANEL_ID_PATTERN = re.compile(r"^panel_[a-z][a-z0-9_]*$")
_VIEW_ID_PATTERN = re.compile(r"^view_[a-z][a-z0-9_]*$")
_GATE_ID_PATTERN = re.compile(r"^physgate_[a-z][a-z0-9_]*$")
_ENGINE_ID_PATTERN = re.compile(r"^opticsengine_[a-z][a-z0-9_]*$")
_SURFACE_ID_PATTERN = re.compile(r"^surfaceintel_[a-z][a-z0-9_]*$")
_MATERIAL_ID_PATTERN = re.compile(r"^material_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class PhysicsDashboardViewEntry:
    """Canonical physics dashboard / explainable view entry."""

    panel_id: PhysicsPanelId
    view_id: str
    view_kind: PhysicsViewKind
    display_role: DisplayRole
    visibility_mode: DashboardVisibilityMode
    explainable_required: bool
    read_only: bool
    linked_surface_entry_id: str | None
    linked_material_id: str | None
    linked_validation_gate_id: str | None
    linked_optics_engine_id: str | None
    export_capable: bool
    dashboard_status: PhysicsDashboardStatus
    description: str

    def __post_init__(self) -> None:
        """Validate physics dashboard view invariants."""
        if not _PANEL_ID_PATTERN.fullmatch(self.panel_id):
            raise ValueError(f"Invalid panel_id: {self.panel_id}")

        if not _VIEW_ID_PATTERN.fullmatch(self.view_id):
            raise ValueError(f"Invalid view_id: {self.view_id}")

        if self.linked_surface_entry_id is not None:
            if not _SURFACE_ID_PATTERN.fullmatch(self.linked_surface_entry_id):
                raise ValueError(
                    f"Invalid linked_surface_entry_id: {self.linked_surface_entry_id}"
                )

        if self.linked_material_id is not None:
            if not _MATERIAL_ID_PATTERN.fullmatch(self.linked_material_id):
                raise ValueError(
                    f"Invalid linked_material_id: {self.linked_material_id}"
                )

        if self.linked_validation_gate_id is not None:
            if not _GATE_ID_PATTERN.fullmatch(self.linked_validation_gate_id):
                raise ValueError(
                    f"Invalid linked_validation_gate_id: {self.linked_validation_gate_id}"
                )

        if self.linked_optics_engine_id is not None:
            if not _ENGINE_ID_PATTERN.fullmatch(self.linked_optics_engine_id):
                raise ValueError(
                    f"Invalid linked_optics_engine_id: {self.linked_optics_engine_id}"
                )

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.panel_id}")

        if self.visibility_mode != "read_only":
            raise ValueError(f"Physics dashboard must be read_only: {self.panel_id}")

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True for {self.panel_id}"
            )

        if not self.read_only:
            raise ValueError(f"read_only must be True for {self.panel_id}")

        if self.dashboard_status != "defined":
            raise ValueError(
                f"dashboard_status must be defined for {self.panel_id}"
            )

        if self.panel_id == "panel_surface_map_001":
            if self.view_kind != "surface_map_view":
                raise ValueError("panel_surface_map_001 must use surface_map_view")
            if self.display_role != "engineering_display":
                raise ValueError(
                    "panel_surface_map_001 must target engineering_display"
                )
            if self.linked_surface_entry_id != "surfaceintel_aluminum_engraving_001":
                raise ValueError(
                    "panel_surface_map_001 must link surfaceintel_aluminum_engraving_001"
                )
            if self.linked_material_id != "material_aluminum_001":
                raise ValueError(
                    "panel_surface_map_001 must link material_aluminum_001"
                )
            if self.export_capable:
                raise ValueError("panel_surface_map_001 must not be export_capable")

        if self.panel_id == "panel_material_profile_001":
            if self.view_kind != "material_profile_view":
                raise ValueError(
                    "panel_material_profile_001 must use material_profile_view"
                )
            if self.display_role != "engineering_display":
                raise ValueError(
                    "panel_material_profile_001 must target engineering_display"
                )
            if self.linked_material_id != "material_steel_001":
                raise ValueError(
                    "panel_material_profile_001 must link material_steel_001"
                )
            if self.export_capable:
                raise ValueError(
                    "panel_material_profile_001 must not be export_capable"
                )

        if self.panel_id == "panel_validation_report_001":
            if self.view_kind != "validation_report_view":
                raise ValueError(
                    "panel_validation_report_001 must use validation_report_view"
                )
            if self.display_role != "primary_dashboard_display":
                raise ValueError(
                    "panel_validation_report_001 must target primary_dashboard_display"
                )
            if (
                self.linked_validation_gate_id
                != "physgate_engineering_realistic_001"
            ):
                raise ValueError(
                    "panel_validation_report_001 must link physgate_engineering_realistic_001"
                )
            if self.export_capable:
                raise ValueError(
                    "panel_validation_report_001 must not be export_capable"
                )

        if self.panel_id == "panel_optics_mode_001":
            if self.view_kind != "optics_mode_view":
                raise ValueError("panel_optics_mode_001 must use optics_mode_view")
            if self.display_role != "engineering_display":
                raise ValueError(
                    "panel_optics_mode_001 must target engineering_display"
                )
            if (
                self.linked_optics_engine_id
                != "opticsengine_projection_assisted_spatial_001"
            ):
                raise ValueError(
                    "panel_optics_mode_001 must link opticsengine_projection_assisted_spatial_001"
                )
            if self.export_capable:
                raise ValueError("panel_optics_mode_001 must not be export_capable")

        if self.panel_id == "panel_project_export_001":
            if self.view_kind != "project_export_view":
                raise ValueError("panel_project_export_001 must use project_export_view")
            if self.display_role != "primary_dashboard_display":
                raise ValueError(
                    "panel_project_export_001 must target primary_dashboard_display"
                )
            if not self.export_capable:
                raise ValueError("panel_project_export_001 must be export_capable")
            if (
                self.linked_validation_gate_id
                != "physgate_strict_physics_001"
            ):
                raise ValueError(
                    "panel_project_export_001 must link physgate_strict_physics_001"
                )


@dataclass(frozen=True, slots=True)
class PhysicsDashboardViewsContract:
    """Unified physics dashboard / explainable views contract."""

    total_entries: int
    engineering_display_entries: int
    primary_dashboard_entries: int
    export_capable_entries: int
    defined_entries: int
    entries: tuple[PhysicsDashboardViewEntry, ...]

    def __post_init__(self) -> None:
        """Validate physics dashboard contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        engineering_display_entries = sum(
            1 for entry in self.entries if entry.display_role == "engineering_display"
        )
        primary_dashboard_entries = sum(
            1
            for entry in self.entries
            if entry.display_role == "primary_dashboard_display"
        )
        export_capable_entries = sum(
            1 for entry in self.entries if entry.export_capable
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.dashboard_status == "defined"
        )

        if self.engineering_display_entries != engineering_display_entries:
            raise ValueError(
                "engineering_display_entries must match computed count"
            )

        if self.primary_dashboard_entries != primary_dashboard_entries:
            raise ValueError(
                "primary_dashboard_entries must match computed count"
            )

        if self.export_capable_entries != export_capable_entries:
            raise ValueError("export_capable_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        panel_ids = tuple(entry.panel_id for entry in self.entries)
        view_ids = tuple(entry.view_id for entry in self.entries)

        if len(set(panel_ids)) != len(panel_ids):
            raise ValueError("Duplicate panel_id values detected")

        if len(set(view_ids)) != len(view_ids):
            raise ValueError("Duplicate view_id values detected")


def build_physics_dashboard_views_contract() -> PhysicsDashboardViewsContract:
    """Build canonical physics dashboard / explainable views contract."""
    surface_contract = build_surface_intelligence_contract()
    material_contract = build_material_registry_contract()
    gate_contract = build_physics_validation_gate_contract()
    optics_contract = build_optics_light_field_engine_contract()

    surface_ids = {entry.surface_entry_id for entry in surface_contract.entries}
    material_ids = {entry.material_id for entry in material_contract.entries}
    gate_ids = {entry.gate_entry_id for entry in gate_contract.entries}
    optics_ids = {entry.engine_entry_id for entry in optics_contract.entries}

    required_surface_ids = {"surfaceintel_aluminum_engraving_001"}
    required_material_ids = {"material_aluminum_001", "material_steel_001"}
    required_gate_ids = {
        "physgate_strict_physics_001",
        "physgate_engineering_realistic_001",
    }
    required_optics_ids = {"opticsengine_projection_assisted_spatial_001"}

    if required_surface_ids - surface_ids:
        raise ValueError(
            f"Missing surface ids: {sorted(required_surface_ids - surface_ids)}"
        )
    if required_material_ids - material_ids:
        raise ValueError(
            f"Missing material ids: {sorted(required_material_ids - material_ids)}"
        )
    if required_gate_ids - gate_ids:
        raise ValueError(
            f"Missing gate ids: {sorted(required_gate_ids - gate_ids)}"
        )
    if required_optics_ids - optics_ids:
        raise ValueError(
            f"Missing optics ids: {sorted(required_optics_ids - optics_ids)}"
        )

    entries = (
        PhysicsDashboardViewEntry(
            panel_id="panel_surface_map_001",
            view_id="view_surface_map_001",
            view_kind="surface_map_view",
            display_role="engineering_display",
            visibility_mode="read_only",
            explainable_required=True,
            read_only=True,
            linked_surface_entry_id="surfaceintel_aluminum_engraving_001",
            linked_material_id="material_aluminum_001",
            linked_validation_gate_id=None,
            linked_optics_engine_id=None,
            export_capable=False,
            dashboard_status="defined",
            description="Read-only explainable surface map panel.",
        ),
        PhysicsDashboardViewEntry(
            panel_id="panel_material_profile_001",
            view_id="view_material_profile_001",
            view_kind="material_profile_view",
            display_role="engineering_display",
            visibility_mode="read_only",
            explainable_required=True,
            read_only=True,
            linked_surface_entry_id=None,
            linked_material_id="material_steel_001",
            linked_validation_gate_id=None,
            linked_optics_engine_id=None,
            export_capable=False,
            dashboard_status="defined",
            description="Read-only explainable material profile panel.",
        ),
        PhysicsDashboardViewEntry(
            panel_id="panel_validation_report_001",
            view_id="view_validation_report_001",
            view_kind="validation_report_view",
            display_role="primary_dashboard_display",
            visibility_mode="read_only",
            explainable_required=True,
            read_only=True,
            linked_surface_entry_id=None,
            linked_material_id=None,
            linked_validation_gate_id="physgate_engineering_realistic_001",
            linked_optics_engine_id=None,
            export_capable=False,
            dashboard_status="defined",
            description="Read-only explainable validation report panel.",
        ),
        PhysicsDashboardViewEntry(
            panel_id="panel_optics_mode_001",
            view_id="view_optics_mode_001",
            view_kind="optics_mode_view",
            display_role="engineering_display",
            visibility_mode="read_only",
            explainable_required=True,
            read_only=True,
            linked_surface_entry_id=None,
            linked_material_id=None,
            linked_validation_gate_id=None,
            linked_optics_engine_id="opticsengine_projection_assisted_spatial_001",
            export_capable=False,
            dashboard_status="defined",
            description="Read-only explainable optics mode panel.",
        ),
        PhysicsDashboardViewEntry(
            panel_id="panel_project_export_001",
            view_id="view_project_export_001",
            view_kind="project_export_view",
            display_role="primary_dashboard_display",
            visibility_mode="read_only",
            explainable_required=True,
            read_only=True,
            linked_surface_entry_id=None,
            linked_material_id=None,
            linked_validation_gate_id="physgate_strict_physics_001",
            linked_optics_engine_id=None,
            export_capable=True,
            dashboard_status="defined",
            description="Read-only explainable project export panel.",
        ),
    )

    engineering_display_entries = sum(
        1 for entry in entries if entry.display_role == "engineering_display"
    )
    primary_dashboard_entries = sum(
        1
        for entry in entries
        if entry.display_role == "primary_dashboard_display"
    )
    export_capable_entries = sum(
        1 for entry in entries if entry.export_capable
    )
    defined_entries = sum(
        1 for entry in entries if entry.dashboard_status == "defined"
    )

    return PhysicsDashboardViewsContract(
        total_entries=len(entries),
        engineering_display_entries=engineering_display_entries,
        primary_dashboard_entries=primary_dashboard_entries,
        export_capable_entries=export_capable_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
