from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.ar_glasses_display_contract import (
    build_ar_glasses_display_contract,
)
from MAKSIMAR_CORE_LIB.optics_light_field_engine import (
    build_optics_light_field_engine_contract,
)
from MAKSIMAR_CORE_LIB.physics_dashboard_views import (
    build_physics_dashboard_views_contract,
)
from MAKSIMAR_CORE_LIB.wrist_terminal_contract import (
    build_wrist_terminal_contract,
)


SpatialAnchorId = Literal[
    "anchor_surface_map_001",
    "anchor_validation_report_001",
    "anchor_optics_mode_001",
]

ResolvedViewTarget = Literal[
    "view_surface_map_001",
    "view_validation_report_001",
    "view_optics_mode_001",
]

DisplayTargetRole = Literal[
    "engineering_display",
    "primary_dashboard_display",
    "ar_glasses_display",
]

AnchorReferenceMode = Literal[
    "surface_locked",
    "dashboard_locked",
    "optics_locked",
]

ViewResolutionStatus = Literal[
    "resolved",
]


_ENTRY_ID_PATTERN = re.compile(r"^spatialview_[a-z][a-z0-9_]*$")
_ANCHOR_ID_PATTERN = re.compile(r"^anchor_[a-z][a-z0-9_]*$")
_VIEW_ID_PATTERN = re.compile(r"^view_[a-z][a-z0-9_]*$")
_ENGINE_ID_PATTERN = re.compile(r"^opticsengine_[a-z][a-z0-9_]*$")
_WRIST_ID_PATTERN = re.compile(r"^wrist_[a-z][a-z0-9_]*$")
_AR_DISPLAY_ID_PATTERN = re.compile(r"^ar_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class SpatialAnchorResolutionEntry:
    """Canonical spatial anchor / view resolution entry."""

    resolution_entry_id: str
    spatial_anchor_id: SpatialAnchorId
    resolved_view_target: ResolvedViewTarget
    display_target_role: DisplayTargetRole
    linked_optics_engine_id: str
    linked_wrist_terminal_id: str
    linked_ar_display_id: str
    anchor_reference_mode: AnchorReferenceMode
    explainable_required: bool
    read_only: bool
    production_path_allowed: bool
    resolution_status: ViewResolutionStatus
    description: str

    def __post_init__(self) -> None:
        """Validate spatial anchor resolution invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.resolution_entry_id):
            raise ValueError(f"Invalid resolution_entry_id: {self.resolution_entry_id}")

        if not _ANCHOR_ID_PATTERN.fullmatch(self.spatial_anchor_id):
            raise ValueError(f"Invalid spatial_anchor_id: {self.spatial_anchor_id}")

        if not _VIEW_ID_PATTERN.fullmatch(self.resolved_view_target):
            raise ValueError(f"Invalid resolved_view_target: {self.resolved_view_target}")

        if not _ENGINE_ID_PATTERN.fullmatch(self.linked_optics_engine_id):
            raise ValueError(
                f"Invalid linked_optics_engine_id: {self.linked_optics_engine_id}"
            )

        if not _WRIST_ID_PATTERN.fullmatch(self.linked_wrist_terminal_id):
            raise ValueError(
                f"Invalid linked_wrist_terminal_id: {self.linked_wrist_terminal_id}"
            )

        if not _AR_DISPLAY_ID_PATTERN.fullmatch(self.linked_ar_display_id):
            raise ValueError(f"Invalid linked_ar_display_id: {self.linked_ar_display_id}")

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.resolution_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.resolution_entry_id}"
            )

        if not self.read_only:
            raise ValueError(f"read_only must be True: {self.resolution_entry_id}")

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.resolution_entry_id}"
            )

        if self.resolution_status != "resolved":
            raise ValueError(
                f"resolution_status must be resolved: {self.resolution_entry_id}"
            )

        if self.resolution_entry_id == "spatialview_surface_map_001":
            if self.spatial_anchor_id != "anchor_surface_map_001":
                raise ValueError("spatialview_surface_map_001 must use anchor_surface_map_001")
            if self.resolved_view_target != "view_surface_map_001":
                raise ValueError("spatialview_surface_map_001 must resolve view_surface_map_001")
            if self.display_target_role != "engineering_display":
                raise ValueError("spatialview_surface_map_001 must target engineering_display")
            if self.anchor_reference_mode != "surface_locked":
                raise ValueError("spatialview_surface_map_001 must use surface_locked")

        if self.resolution_entry_id == "spatialview_validation_report_001":
            if self.spatial_anchor_id != "anchor_validation_report_001":
                raise ValueError("spatialview_validation_report_001 must use anchor_validation_report_001")
            if self.resolved_view_target != "view_validation_report_001":
                raise ValueError("spatialview_validation_report_001 must resolve view_validation_report_001")
            if self.display_target_role != "primary_dashboard_display":
                raise ValueError("spatialview_validation_report_001 must target primary_dashboard_display")
            if self.anchor_reference_mode != "dashboard_locked":
                raise ValueError("spatialview_validation_report_001 must use dashboard_locked")

        if self.resolution_entry_id == "spatialview_optics_mode_001":
            if self.spatial_anchor_id != "anchor_optics_mode_001":
                raise ValueError("spatialview_optics_mode_001 must use anchor_optics_mode_001")
            if self.resolved_view_target != "view_optics_mode_001":
                raise ValueError("spatialview_optics_mode_001 must resolve view_optics_mode_001")
            if self.display_target_role != "ar_glasses_display":
                raise ValueError("spatialview_optics_mode_001 must target ar_glasses_display")
            if self.anchor_reference_mode != "optics_locked":
                raise ValueError("spatialview_optics_mode_001 must use optics_locked")


@dataclass(frozen=True, slots=True)
class SpatialAnchorResolutionContract:
    """Unified spatial anchor / view resolution contract."""

    total_entries: int
    engineering_target_entries: int
    dashboard_target_entries: int
    ar_target_entries: int
    resolved_entries: int
    entries: tuple[SpatialAnchorResolutionEntry, ...]

    def __post_init__(self) -> None:
        """Validate spatial anchor resolution contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        engineering_target_entries = sum(
            1 for entry in self.entries if entry.display_target_role == "engineering_display"
        )
        dashboard_target_entries = sum(
            1 for entry in self.entries if entry.display_target_role == "primary_dashboard_display"
        )
        ar_target_entries = sum(
            1 for entry in self.entries if entry.display_target_role == "ar_glasses_display"
        )
        resolved_entries = sum(
            1 for entry in self.entries if entry.resolution_status == "resolved"
        )

        if self.engineering_target_entries != engineering_target_entries:
            raise ValueError("engineering_target_entries must match computed count")

        if self.dashboard_target_entries != dashboard_target_entries:
            raise ValueError("dashboard_target_entries must match computed count")

        if self.ar_target_entries != ar_target_entries:
            raise ValueError("ar_target_entries must match computed count")

        if self.resolved_entries != resolved_entries:
            raise ValueError("resolved_entries must match computed count")

        entry_ids = tuple(entry.resolution_entry_id for entry in self.entries)
        anchor_ids = tuple(entry.spatial_anchor_id for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate resolution_entry_id values detected")

        if len(set(anchor_ids)) != len(anchor_ids):
            raise ValueError("Duplicate spatial_anchor_id values detected")


def build_spatial_anchor_resolution_contract() -> SpatialAnchorResolutionContract:
    """Build canonical spatial anchor / view resolution contract."""
    dashboard_contract = build_physics_dashboard_views_contract()
    optics_contract = build_optics_light_field_engine_contract()
    wrist_contract = build_wrist_terminal_contract()
    ar_contract = build_ar_glasses_display_contract()

    view_ids = {entry.view_id for entry in dashboard_contract.entries}
    optics_ids = {entry.engine_entry_id for entry in optics_contract.entries}
    wrist_ids = {entry.wrist_terminal_id for entry in wrist_contract.entries}
    ar_ids = {entry.ar_display_id for entry in ar_contract.entries}

    required_view_ids = {
        "view_surface_map_001",
        "view_validation_report_001",
        "view_optics_mode_001",
    }

    if required_view_ids - view_ids:
        raise ValueError(f"Missing view ids: {sorted(required_view_ids - view_ids)}")

    if "opticsengine_ar_glasses_projection_001" not in optics_ids:
        raise ValueError("Expected opticsengine_ar_glasses_projection_001 in optics contract")

    if "wrist_terminal_core_001" not in wrist_ids:
        raise ValueError("Expected wrist_terminal_core_001 in wrist contract")

    if "ar_glasses_display_core_001" not in ar_ids:
        raise ValueError("Expected ar_glasses_display_core_001 in AR display contract")

    entries = (
        SpatialAnchorResolutionEntry(
            resolution_entry_id="spatialview_surface_map_001",
            spatial_anchor_id="anchor_surface_map_001",
            resolved_view_target="view_surface_map_001",
            display_target_role="engineering_display",
            linked_optics_engine_id="opticsengine_ar_glasses_projection_001",
            linked_wrist_terminal_id="wrist_terminal_core_001",
            linked_ar_display_id="ar_glasses_display_core_001",
            anchor_reference_mode="surface_locked",
            explainable_required=True,
            read_only=True,
            production_path_allowed=True,
            resolution_status="resolved",
            description="Spatial resolution entry for surface map engineering view.",
        ),
        SpatialAnchorResolutionEntry(
            resolution_entry_id="spatialview_validation_report_001",
            spatial_anchor_id="anchor_validation_report_001",
            resolved_view_target="view_validation_report_001",
            display_target_role="primary_dashboard_display",
            linked_optics_engine_id="opticsengine_ar_glasses_projection_001",
            linked_wrist_terminal_id="wrist_terminal_core_001",
            linked_ar_display_id="ar_glasses_display_core_001",
            anchor_reference_mode="dashboard_locked",
            explainable_required=True,
            read_only=True,
            production_path_allowed=True,
            resolution_status="resolved",
            description="Spatial resolution entry for validation report dashboard view.",
        ),
        SpatialAnchorResolutionEntry(
            resolution_entry_id="spatialview_optics_mode_001",
            spatial_anchor_id="anchor_optics_mode_001",
            resolved_view_target="view_optics_mode_001",
            display_target_role="ar_glasses_display",
            linked_optics_engine_id="opticsengine_ar_glasses_projection_001",
            linked_wrist_terminal_id="wrist_terminal_core_001",
            linked_ar_display_id="ar_glasses_display_core_001",
            anchor_reference_mode="optics_locked",
            explainable_required=True,
            read_only=True,
            production_path_allowed=True,
            resolution_status="resolved",
            description="Spatial resolution entry for AR optics mode view.",
        ),
    )

    engineering_target_entries = sum(
        1 for entry in entries if entry.display_target_role == "engineering_display"
    )
    dashboard_target_entries = sum(
        1 for entry in entries if entry.display_target_role == "primary_dashboard_display"
    )
    ar_target_entries = sum(
        1 for entry in entries if entry.display_target_role == "ar_glasses_display"
    )
    resolved_entries = sum(
        1 for entry in entries if entry.resolution_status == "resolved"
    )

    return SpatialAnchorResolutionContract(
        total_entries=len(entries),
        engineering_target_entries=engineering_target_entries,
        dashboard_target_entries=dashboard_target_entries,
        ar_target_entries=ar_target_entries,
        resolved_entries=resolved_entries,
        entries=entries,
    )
