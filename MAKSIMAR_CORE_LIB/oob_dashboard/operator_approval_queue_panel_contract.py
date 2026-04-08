from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_approval_decision_contract import (
    build_operator_approval_decision_contract,
)


ApprovalQueuePanelMode = Literal[
    "approval_queue_read_only",
]

ApprovalQueuePanelStatus = Literal[
    "approval_queue_visible",
]

ALL_APPROVAL_QUEUE_PANEL_MODES: tuple[ApprovalQueuePanelMode, ...] = (
    "approval_queue_read_only",
)

ALL_APPROVAL_QUEUE_PANEL_STATUSES: tuple[ApprovalQueuePanelStatus, ...] = (
    "approval_queue_visible",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorApprovalQueuePanelEntry:
    """Canonical operator approval-queue panel entry."""

    panel_id: str
    workspace_id: str
    panel_mode: ApprovalQueuePanelMode
    panel_status: ApprovalQueuePanelStatus
    total_queue_items: int
    pending_approval_items: int
    executable_after_approval_items: int
    operator_visible: bool
    read_only: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator approval-queue panel entry."""
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.panel_mode not in ALL_APPROVAL_QUEUE_PANEL_MODES:
            raise ValueError(
                f"panel_mode must be one of {ALL_APPROVAL_QUEUE_PANEL_MODES}, got {self.panel_mode!r}."
            )

        if self.panel_status not in ALL_APPROVAL_QUEUE_PANEL_STATUSES:
            raise ValueError(
                "panel_status must be one of "
                f"{ALL_APPROVAL_QUEUE_PANEL_STATUSES}, got {self.panel_status!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical approval-queue panels."
            )

        if not self.read_only:
            raise ValueError(
                "read_only must remain true for canonical approval-queue panels."
            )

        if self.pending_approval_items > self.total_queue_items:
            raise ValueError(
                "pending_approval_items cannot exceed total_queue_items."
            )

        if self.executable_after_approval_items > self.total_queue_items:
            raise ValueError(
                "executable_after_approval_items cannot exceed total_queue_items."
            )


@dataclass(frozen=True, slots=True)
class OperatorApprovalQueuePanelContract:
    """Canonical operator approval-queue panel contract."""

    contract_id: str
    total_entries: int
    operator_visible_entries: int
    read_only_entries: int
    entries: tuple[OperatorApprovalQueuePanelEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator approval-queue panel contract."""
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


def build_operator_approval_queue_panel_contract() -> OperatorApprovalQueuePanelContract:
    """Build canonical operator approval-queue panel contract."""
    approval_contract = build_operator_approval_decision_contract()

    entries = (
        OperatorApprovalQueuePanelEntry(
            panel_id="panel_operator_approval_queue_001",
            workspace_id="workspace_operator_main",
            panel_mode="approval_queue_read_only",
            panel_status="approval_queue_visible",
            total_queue_items=approval_contract.total_entries,
            pending_approval_items=approval_contract.pending_approval_entries,
            executable_after_approval_items=approval_contract.executable_after_approval_entries,
            operator_visible=True,
            read_only=True,
            description=(
                "Canonical operator approval-queue panel entry showing approval-bound "
                "items waiting on governed approval flow."
            ),
        ),
    )

    return OperatorApprovalQueuePanelContract(
        contract_id="operator_approval_queue_panel_contract_001",
        total_entries=len(entries),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
