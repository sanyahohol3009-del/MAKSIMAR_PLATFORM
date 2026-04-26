from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_interaction_surface_contract import (
    build_main_operator_interaction_surface_contract,
)


ApprovalQueueState = Literal[
    "approval_queue_ready",
]
ApprovalQueueClass = Literal[
    "pending_approval_entry",
]

ALL_APPROVAL_QUEUE_STATES: tuple[ApprovalQueueState, ...] = (
    "approval_queue_ready",
)
ALL_APPROVAL_QUEUE_CLASSES: tuple[ApprovalQueueClass, ...] = (
    "pending_approval_entry",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ApprovalQueuePanelContentEntry:
    """Canonical approval-queue panel content entry."""

    approval_queue_entry_id: str
    operator_intent_id: str
    dashboard_id: str
    workspace_id: str
    approval_queue_state: ApprovalQueueState
    approval_queue_class: ApprovalQueueClass
    intent_kind: Literal["control_request"]
    pending_approval_visible: bool
    approval_required: bool
    handoff_ready: bool
    operator_visible: bool
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.approval_queue_entry_id, "approval_queue_entry_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.approval_queue_state not in ALL_APPROVAL_QUEUE_STATES:
            raise ValueError(
                "approval_queue_state must be one of "
                f"{ALL_APPROVAL_QUEUE_STATES}, got {self.approval_queue_state!r}."
            )

        if self.approval_queue_class not in ALL_APPROVAL_QUEUE_CLASSES:
            raise ValueError(
                "approval_queue_class must be one of "
                f"{ALL_APPROVAL_QUEUE_CLASSES}, got {self.approval_queue_class!r}."
            )

        if self.intent_kind != "control_request":
            raise ValueError(
                "approval queue panel entries must remain limited to control_request."
            )

        if not self.pending_approval_visible:
            raise ValueError(
                "pending_approval_visible must remain true for canonical approval queue entries."
            )

        if not self.approval_required:
            raise ValueError(
                "approval_required must remain true for canonical approval queue entries."
            )

        if not self.handoff_ready:
            raise ValueError(
                "handoff_ready must remain true for canonical approval queue entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical approval queue entries."
            )


@dataclass(frozen=True, slots=True)
class ApprovalQueuePanelContentContract:
    """Canonical approval-queue panel content contract."""

    contract_id: str
    total_entries: int
    pending_approval_entries: int
    handoff_ready_entries: int
    operator_visible_entries: int
    entries: tuple[ApprovalQueuePanelContentEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.pending_approval_entries != len(self.entries):
            raise ValueError(
                "pending_approval_entries must match the number of approval queue entries."
            )

        if self.handoff_ready_entries != sum(
            1 for entry in self.entries if entry.handoff_ready
        ):
            raise ValueError("handoff_ready_entries must match handoff_ready count.")

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_approval_queue_panel_content_contract() -> ApprovalQueuePanelContentContract:
    """Build canonical approval-queue panel content contract."""
    interaction_surface_contract = build_main_operator_interaction_surface_contract()

    filtered_entries = tuple(
        entry
        for entry in interaction_surface_contract.entries
        if entry.approval_required and entry.pending_approval_visible
    )

    entries = tuple(
        ApprovalQueuePanelContentEntry(
            approval_queue_entry_id=f"approval_queue_entry_{index:03d}",
            operator_intent_id=entry.operator_intent_id,
            dashboard_id=entry.dashboard_id,
            workspace_id=entry.workspace_id,
            approval_queue_state="approval_queue_ready",
            approval_queue_class="pending_approval_entry",
            intent_kind="control_request",
            pending_approval_visible=entry.pending_approval_visible,
            approval_required=entry.approval_required,
            handoff_ready=entry.handoff_ready,
            operator_visible=entry.operator_visible,
            trace_id=entry.trace_id,
            description=(
                "Canonical approval queue panel content entry for "
                f"{entry.operator_intent_id}."
            ),
        )
        for index, entry in enumerate(filtered_entries, start=1)
    )

    return ApprovalQueuePanelContentContract(
        contract_id="approval_queue_panel_content_contract_001",
        total_entries=len(entries),
        pending_approval_entries=len(entries),
        handoff_ready_entries=sum(1 for entry in entries if entry.handoff_ready),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
