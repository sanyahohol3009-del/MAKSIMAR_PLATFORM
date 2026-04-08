from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_interaction_read_model_contract import (
    build_operator_interaction_read_model_contract,
)


ActionQueuePanelMode = Literal[
    "read_only_action_queue",
]

ActionQueuePanelStatus = Literal[
    "action_queue_visible",
]

ALL_ACTION_QUEUE_PANEL_MODES: tuple[ActionQueuePanelMode, ...] = (
    "read_only_action_queue",
)

ALL_ACTION_QUEUE_PANEL_STATUSES: tuple[ActionQueuePanelStatus, ...] = (
    "action_queue_visible",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorActionQueuePanelEntry:
    """Canonical operator action-queue panel entry."""

    panel_id: str
    workspace_id: str
    interaction_surface_id: str
    panel_mode: ActionQueuePanelMode
    panel_status: ActionQueuePanelStatus
    total_queue_items: int
    read_only_queue_items: int
    approval_bound_queue_items: int
    handoff_ready_queue_items: int
    operator_visible: bool
    read_only: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator action-queue panel entry."""
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.interaction_surface_id, "interaction_surface_id")
        _require_non_empty(self.description, "description")

        if self.panel_mode not in ALL_ACTION_QUEUE_PANEL_MODES:
            raise ValueError(
                f"panel_mode must be one of {ALL_ACTION_QUEUE_PANEL_MODES}, got {self.panel_mode!r}."
            )

        if self.panel_status not in ALL_ACTION_QUEUE_PANEL_STATUSES:
            raise ValueError(
                "panel_status must be one of "
                f"{ALL_ACTION_QUEUE_PANEL_STATUSES}, got {self.panel_status!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical action-queue panels."
            )

        if not self.read_only:
            raise ValueError(
                "read_only must remain true for canonical action-queue panels."
            )

        if self.total_queue_items != (
            self.read_only_queue_items + self.approval_bound_queue_items
        ):
            raise ValueError(
                "total_queue_items must equal read_only_queue_items + approval_bound_queue_items."
            )


@dataclass(frozen=True, slots=True)
class OperatorActionQueuePanelContract:
    """Canonical operator action-queue panel contract."""

    contract_id: str
    total_entries: int
    operator_visible_entries: int
    read_only_entries: int
    entries: tuple[OperatorActionQueuePanelEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator action-queue panel contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )

        if self.read_only_entries != sum(
            1 for entry in self.entries if entry.read_only
        ):
            raise ValueError(
                "read_only_entries must match read_only count."
            )


def build_operator_action_queue_panel_contract() -> OperatorActionQueuePanelContract:
    """Build canonical operator action-queue panel contract."""
    interaction_contract = build_operator_interaction_read_model_contract()

    entries = (
        OperatorActionQueuePanelEntry(
            panel_id="panel_operator_action_queue_001",
            workspace_id="workspace_operator_main",
            interaction_surface_id="main_operator_interaction_surface_001",
            panel_mode="read_only_action_queue",
            panel_status="action_queue_visible",
            total_queue_items=interaction_contract.total_entries,
            read_only_queue_items=interaction_contract.read_only_lane_entries,
            approval_bound_queue_items=interaction_contract.approval_bound_lane_entries,
            handoff_ready_queue_items=interaction_contract.handoff_ready_entries,
            operator_visible=True,
            read_only=True,
            description=(
                "Canonical operator action-queue panel entry showing visible interaction items "
                "across read-only and approval-bound lanes."
            ),
        ),
    )

    return OperatorActionQueuePanelContract(
        contract_id="operator_action_queue_panel_contract_001",
        total_entries=len(entries),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
