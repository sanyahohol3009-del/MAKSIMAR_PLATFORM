from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.ar_glasses_display_contract import (
    build_ar_glasses_display_contract,
)
from MAKSIMAR_CORE_LIB.physics_dashboard_views import (
    build_physics_dashboard_views_contract,
)
from MAKSIMAR_CORE_LIB.spatial_anchor_resolution import (
    build_spatial_anchor_resolution_contract,
)
from MAKSIMAR_CORE_LIB.wrist_terminal_contract import (
    build_wrist_terminal_contract,
)


IntegrationMode = Literal[
    "wrist_to_engineering_display",
    "wrist_to_dashboard_display",
    "wrist_to_ar_display",
]

IntegratedViewId = Literal[
    "view_surface_map_001",
    "view_validation_report_001",
    "view_optics_mode_001",
]

IntegrationAuthority = Literal[
    "display_only_handoff",
]

IntegrationStatus = Literal[
    "integrated",
]


_ENTRY_ID_PATTERN = re.compile(r"^wristdisplayint_[a-z][a-z0-9_]*$")
_WRIST_ID_PATTERN = re.compile(r"^wrist_[a-z][a-z0-9_]*$")
_AR_ID_PATTERN = re.compile(r"^ar_[a-z][a-z0-9_]*$")
_VIEW_ID_PATTERN = re.compile(r"^view_[a-z][a-z0-9_]*$")
_RESOLUTION_ID_PATTERN = re.compile(r"^spatialview_[a-z][a-z0-9_]*$")
_PANEL_ID_PATTERN = re.compile(r"^panel_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class WristPscDisplayIntegrationEntry:
    """Canonical wrist + PSC + display integration entry."""

    integration_entry_id: str
    integration_mode: IntegrationMode
    wrist_terminal_id: str
    ar_display_id: str
    resolution_entry_id: str
    resolved_view_id: IntegratedViewId
    source_panel_id: str
    display_target_role: str
    integration_authority: IntegrationAuthority
    explainable_required: bool
    read_only: bool
    production_path_allowed: bool
    integration_status: IntegrationStatus
    description: str

    def __post_init__(self) -> None:
        """Validate wrist + PSC + display integration invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.integration_entry_id):
            raise ValueError(
                f"Invalid integration_entry_id: {self.integration_entry_id}"
            )

        if not _WRIST_ID_PATTERN.fullmatch(self.wrist_terminal_id):
            raise ValueError(f"Invalid wrist_terminal_id: {self.wrist_terminal_id}")

        if not _AR_ID_PATTERN.fullmatch(self.ar_display_id):
            raise ValueError(f"Invalid ar_display_id: {self.ar_display_id}")

        if not _RESOLUTION_ID_PATTERN.fullmatch(self.resolution_entry_id):
            raise ValueError(
                f"Invalid resolution_entry_id: {self.resolution_entry_id}"
            )

        if not _VIEW_ID_PATTERN.fullmatch(self.resolved_view_id):
            raise ValueError(f"Invalid resolved_view_id: {self.resolved_view_id}")

        if not _PANEL_ID_PATTERN.fullmatch(self.source_panel_id):
            raise ValueError(f"Invalid source_panel_id: {self.source_panel_id}")

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.integration_entry_id}"
            )

        if self.integration_authority != "display_only_handoff":
            raise ValueError(
                f"integration_authority must be display_only_handoff: {self.integration_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.integration_entry_id}"
            )

        if not self.read_only:
            raise ValueError(f"read_only must be True: {self.integration_entry_id}")

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.integration_entry_id}"
            )

        if self.integration_status != "integrated":
            raise ValueError(
                f"integration_status must be integrated: {self.integration_entry_id}"
            )

        if self.integration_mode == "wrist_to_engineering_display":
            if self.resolution_entry_id != "spatialview_surface_map_001":
                raise ValueError(
                    "wrist_to_engineering_display must use spatialview_surface_map_001"
                )
            if self.resolved_view_id != "view_surface_map_001":
                raise ValueError(
                    "wrist_to_engineering_display must use view_surface_map_001"
                )
            if self.source_panel_id != "panel_surface_map_001":
                raise ValueError(
                    "wrist_to_engineering_display must use panel_surface_map_001"
                )
            if self.display_target_role != "engineering_display":
                raise ValueError(
                    "wrist_to_engineering_display must target engineering_display"
                )

        if self.integration_mode == "wrist_to_dashboard_display":
            if self.resolution_entry_id != "spatialview_validation_report_001":
                raise ValueError(
                    "wrist_to_dashboard_display must use spatialview_validation_report_001"
                )
            if self.resolved_view_id != "view_validation_report_001":
                raise ValueError(
                    "wrist_to_dashboard_display must use view_validation_report_001"
                )
            if self.source_panel_id != "panel_validation_report_001":
                raise ValueError(
                    "wrist_to_dashboard_display must use panel_validation_report_001"
                )
            if self.display_target_role != "primary_dashboard_display":
                raise ValueError(
                    "wrist_to_dashboard_display must target primary_dashboard_display"
                )

        if self.integration_mode == "wrist_to_ar_display":
            if self.resolution_entry_id != "spatialview_optics_mode_001":
                raise ValueError(
                    "wrist_to_ar_display must use spatialview_optics_mode_001"
                )
            if self.resolved_view_id != "view_optics_mode_001":
                raise ValueError(
                    "wrist_to_ar_display must use view_optics_mode_001"
                )
            if self.source_panel_id != "panel_optics_mode_001":
                raise ValueError(
                    "wrist_to_ar_display must use panel_optics_mode_001"
                )
            if self.display_target_role != "ar_glasses_display":
                raise ValueError(
                    "wrist_to_ar_display must target ar_glasses_display"
                )


@dataclass(frozen=True, slots=True)
class WristPscDisplayIntegrationContract:
    """Unified wrist + PSC + display integration contract."""

    total_entries: int
    engineering_entries: int
    dashboard_entries: int
    ar_entries: int
    integrated_entries: int
    entries: tuple[WristPscDisplayIntegrationEntry, ...]

    def __post_init__(self) -> None:
        """Validate wrist + PSC + display integration contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        engineering_entries = sum(
            1
            for entry in self.entries
            if entry.display_target_role == "engineering_display"
        )
        dashboard_entries = sum(
            1
            for entry in self.entries
            if entry.display_target_role == "primary_dashboard_display"
        )
        ar_entries = sum(
            1 for entry in self.entries if entry.display_target_role == "ar_glasses_display"
        )
        integrated_entries = sum(
            1 for entry in self.entries if entry.integration_status == "integrated"
        )

        if self.engineering_entries != engineering_entries:
            raise ValueError("engineering_entries must match computed count")

        if self.dashboard_entries != dashboard_entries:
            raise ValueError("dashboard_entries must match computed count")

        if self.ar_entries != ar_entries:
            raise ValueError("ar_entries must match computed count")

        if self.integrated_entries != integrated_entries:
            raise ValueError("integrated_entries must match computed count")

        entry_ids = tuple(entry.integration_entry_id for entry in self.entries)
        modes = tuple(entry.integration_mode for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate integration_entry_id values detected")

        if len(set(modes)) != len(modes):
            raise ValueError("Duplicate integration_mode values detected")


def build_wrist_psc_display_integration_contract() -> WristPscDisplayIntegrationContract:
    """Build canonical wrist + PSC + display integration contract."""
    wrist_contract = build_wrist_terminal_contract()
    ar_contract = build_ar_glasses_display_contract()
    resolution_contract = build_spatial_anchor_resolution_contract()
    dashboard_contract = build_physics_dashboard_views_contract()

    wrist_ids = {entry.wrist_terminal_id for entry in wrist_contract.entries}
    ar_ids = {entry.ar_display_id for entry in ar_contract.entries}
    resolution_ids = {entry.resolution_entry_id for entry in resolution_contract.entries}
    panel_ids = {entry.panel_id for entry in dashboard_contract.entries}

    if "wrist_terminal_core_001" not in wrist_ids:
        raise ValueError("Expected wrist_terminal_core_001 in wrist contract")

    if "ar_glasses_display_core_001" not in ar_ids:
        raise ValueError("Expected ar_glasses_display_core_001 in AR display contract")

    required_resolution_ids = {
        "spatialview_surface_map_001",
        "spatialview_validation_report_001",
        "spatialview_optics_mode_001",
    }
    missing_resolution_ids = required_resolution_ids - resolution_ids
    if missing_resolution_ids:
        raise ValueError(
            f"Missing resolution ids: {sorted(missing_resolution_ids)}"
        )

    required_panel_ids = {
        "panel_surface_map_001",
        "panel_validation_report_001",
        "panel_optics_mode_001",
    }
    missing_panel_ids = required_panel_ids - panel_ids
    if missing_panel_ids:
        raise ValueError(f"Missing panel ids: {sorted(missing_panel_ids)}")

    entries = (
        WristPscDisplayIntegrationEntry(
            integration_entry_id="wristdisplayint_engineering_001",
            integration_mode="wrist_to_engineering_display",
            wrist_terminal_id="wrist_terminal_core_001",
            ar_display_id="ar_glasses_display_core_001",
            resolution_entry_id="spatialview_surface_map_001",
            resolved_view_id="view_surface_map_001",
            source_panel_id="panel_surface_map_001",
            display_target_role="engineering_display",
            integration_authority="display_only_handoff",
            explainable_required=True,
            read_only=True,
            production_path_allowed=True,
            integration_status="integrated",
            description="Integrated wrist → PSC → engineering display handoff.",
        ),
        WristPscDisplayIntegrationEntry(
            integration_entry_id="wristdisplayint_dashboard_001",
            integration_mode="wrist_to_dashboard_display",
            wrist_terminal_id="wrist_terminal_core_001",
            ar_display_id="ar_glasses_display_core_001",
            resolution_entry_id="spatialview_validation_report_001",
            resolved_view_id="view_validation_report_001",
            source_panel_id="panel_validation_report_001",
            display_target_role="primary_dashboard_display",
            integration_authority="display_only_handoff",
            explainable_required=True,
            read_only=True,
            production_path_allowed=True,
            integration_status="integrated",
            description="Integrated wrist → PSC → dashboard display handoff.",
        ),
        WristPscDisplayIntegrationEntry(
            integration_entry_id="wristdisplayint_ar_001",
            integration_mode="wrist_to_ar_display",
            wrist_terminal_id="wrist_terminal_core_001",
            ar_display_id="ar_glasses_display_core_001",
            resolution_entry_id="spatialview_optics_mode_001",
            resolved_view_id="view_optics_mode_001",
            source_panel_id="panel_optics_mode_001",
            display_target_role="ar_glasses_display",
            integration_authority="display_only_handoff",
            explainable_required=True,
            read_only=True,
            production_path_allowed=True,
            integration_status="integrated",
            description="Integrated wrist → PSC → AR display handoff.",
        ),
    )

    engineering_entries = sum(
        1 for entry in entries if entry.display_target_role == "engineering_display"
    )
    dashboard_entries = sum(
        1
        for entry in entries
        if entry.display_target_role == "primary_dashboard_display"
    )
    ar_entries = sum(
        1 for entry in entries if entry.display_target_role == "ar_glasses_display"
    )
    integrated_entries = sum(
        1 for entry in entries if entry.integration_status == "integrated"
    )

    return WristPscDisplayIntegrationContract(
        total_entries=len(entries),
        engineering_entries=engineering_entries,
        dashboard_entries=dashboard_entries,
        ar_entries=ar_entries,
        integrated_entries=integrated_entries,
        entries=entries,
    )
