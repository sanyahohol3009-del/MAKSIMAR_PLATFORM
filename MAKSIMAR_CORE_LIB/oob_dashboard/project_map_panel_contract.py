from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ProjectMapPanelEntry:
    """Canonical project map panel entry."""

    module_id: str
    layer_name: str
    criticality: str
    read_only_view_available: bool
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class ProjectMapPanelContract:
    """Canonical project map panel contract."""

    panel_id: str
    total_entries: int
    read_only_entries: int
    main_dashboard_visible_entries: int
    oob_visible_entries: int
    entries: Tuple[ProjectMapPanelEntry, ...]
    operator_visible: bool
    description: str


def build_project_map_panel_contract() -> ProjectMapPanelContract:
    """Build canonical project map panel contract."""
    entries = (
        ProjectMapPanelEntry(
            module_id="control_plane",
            layer_name="server_control_plane",
            criticality="high",
            read_only_view_available=True,
            operator_visible=True,
            description="Canonical control plane module.",
        ),
        ProjectMapPanelEntry(
            module_id="execution_control",
            layer_name="server_execution_control",
            criticality="high",
            read_only_view_available=True,
            operator_visible=True,
            description="Canonical execution control module.",
        ),
        ProjectMapPanelEntry(
            module_id="oob_dashboard",
            layer_name="read_only_ui",
            criticality="medium",
            read_only_view_available=True,
            operator_visible=True,
            description="Canonical OOB dashboard module.",
        ),
    )

    return ProjectMapPanelContract(
        panel_id="panel_project_map",
        total_entries=len(entries),
        read_only_entries=len(entries),
        main_dashboard_visible_entries=len(entries),
        oob_visible_entries=len(entries),
        entries=entries,
        operator_visible=True,
        description="Canonical project map panel contract.",
    )
