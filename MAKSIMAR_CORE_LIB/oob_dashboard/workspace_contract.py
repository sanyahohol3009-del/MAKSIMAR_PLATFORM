from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class WorkspaceDisplay:
    """Canonical backward-compatible display contract entry."""

    display_id: int
    display_target_id: str
    display_role: str
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class WorkspacePlacement:
    """Canonical backward-compatible workspace placement entry."""

    placement_id: str
    workspace_id: str
    panel_id: str
    display_id: int
    display_target_id: str
    zone_id: str
    slot_id: str
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class WorkspaceContract:
    """Canonical backward-compatible workspace contract."""

    contract_id: str
    displays: Tuple[WorkspaceDisplay, ...]
    placements: Tuple[WorkspacePlacement, ...]
    operator_visible: bool
    description: str


def build_dashboard_workspace_contract() -> WorkspaceContract:
    """Build the canonical workspace contract expected by the smoke tests."""
    displays = (
        WorkspaceDisplay(
            display_id=0,
            display_target_id="display_primary_operator",
            display_role="primary_operator",
            operator_visible=True,
            description="Primary operator display.",
        ),
        WorkspaceDisplay(
            display_id=1,
            display_target_id="display_secondary_diagnostics",
            display_role="secondary_diagnostics",
            operator_visible=True,
            description="Secondary diagnostics display.",
        ),
        WorkspaceDisplay(
            display_id=2,
            display_target_id="display_tertiary_expansion",
            display_role="tertiary_expansion",
            operator_visible=True,
            description="Tertiary expansion display.",
        ),
    )

    placements = (
        WorkspacePlacement(
            placement_id="workspace_placement_001",
            workspace_id="workspace_foundation_monitoring",
            panel_id="panel_consistency",
            display_id=1,
            display_target_id="display_secondary_diagnostics",
            zone_id="zone_main",
            slot_id="slot_001",
            operator_visible=True,
            description="Consistency panel placement.",
        ),
        WorkspacePlacement(
            placement_id="workspace_placement_002",
            workspace_id="workspace_foundation_monitoring",
            panel_id="panel_snapshot",
            display_id=1,
            display_target_id="display_secondary_diagnostics",
            zone_id="zone_main",
            slot_id="slot_002",
            operator_visible=True,
            description="Snapshot panel placement.",
        ),
        WorkspacePlacement(
            placement_id="workspace_placement_003",
            workspace_id="workspace_foundation_monitoring",
            panel_id="panel_incident",
            display_id=1,
            display_target_id="display_secondary_diagnostics",
            zone_id="zone_main",
            slot_id="slot_003",
            operator_visible=True,
            description="Incident panel placement.",
        ),
        WorkspacePlacement(
            placement_id="workspace_placement_004",
            workspace_id="workspace_expansion_observability",
            panel_id="panel_diagnostics",
            display_id=2,
            display_target_id="display_tertiary_expansion",
            zone_id="zone_main",
            slot_id="slot_001",
            operator_visible=True,
            description="Diagnostics panel placement.",
        ),
        WorkspacePlacement(
            placement_id="workspace_placement_005",
            workspace_id="workspace_operator_main",
            panel_id="panel_chat",
            display_id=0,
            display_target_id="display_primary_operator",
            zone_id="zone_main",
            slot_id="slot_001",
            operator_visible=True,
            description="Chat panel placement.",
        ),
        WorkspacePlacement(
            placement_id="workspace_placement_006",
            workspace_id="workspace_operator_main",
            panel_id="panel_settings",
            display_id=0,
            display_target_id="display_primary_operator",
            zone_id="zone_sidebar",
            slot_id="slot_001",
            operator_visible=True,
            description="Settings panel placement.",
        ),
        WorkspacePlacement(
            placement_id="workspace_placement_007",
            workspace_id="workspace_operator_main",
            panel_id="panel_gesture_control",
            display_id=0,
            display_target_id="display_primary_operator",
            zone_id="zone_sidebar",
            slot_id="slot_002",
            operator_visible=True,
            description="Gesture control panel placement.",
        ),
    )

    return WorkspaceContract(
        contract_id="workspace_contract_001",
        displays=displays,
        placements=placements,
        operator_visible=True,
        description="Canonical backward-compatible workspace contract.",
    )


# Backward-compatible alias used by some legacy callers.
def build_workspace_contract() -> WorkspaceContract:
    """Backward-compatible alias for workspace contract builder."""
    return build_dashboard_workspace_contract()
