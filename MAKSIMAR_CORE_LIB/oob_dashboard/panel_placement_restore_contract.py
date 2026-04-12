from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PanelPlacementRestoreEntry:
    """Canonical backward-compatible panel placement restore entry."""

    panel_placement_restore_id: str
    workspace_id: str
    panel_placement_restore_state: str
    panel_placement_restore_class: str
    dashboard_session_restore_ready: bool
    display_assignment_restore_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        if not self.dashboard_session_restore_ready:
            raise ValueError("dashboard_session_restore_ready must remain true")
        if not self.display_assignment_restore_ready:
            raise ValueError("display_assignment_restore_ready must remain true")
        if not self.truth_bound:
            raise ValueError("truth_bound must remain true")


@dataclass(frozen=True)
class PanelPlacementRestoreContract:
    """Canonical backward-compatible panel placement restore contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[PanelPlacementRestoreEntry, ...]
    operator_visible: bool
    description: str


def build_panel_placement_restore_contract() -> PanelPlacementRestoreContract:
    """Build canonical backward-compatible panel placement restore contract."""
    entries = (
        PanelPlacementRestoreEntry(
            panel_placement_restore_id="panel_placement_restore_001",
            workspace_id="workspace_foundation_monitoring",
            panel_placement_restore_state="panel_placement_restore_ready",
            panel_placement_restore_class="dashboard_panel_placement_restore",
            dashboard_session_restore_ready=True,
            display_assignment_restore_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical panel placement restore entry.",
        ),
    )

    return PanelPlacementRestoreContract(
        contract_id="panel_placement_restore_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.panel_placement_restore_state == "panel_placement_restore_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
        operator_visible=True,
        description="Canonical backward-compatible panel placement restore contract.",
    )
