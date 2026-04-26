from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_interaction_surface_contract import (
    build_main_operator_interaction_surface_contract,
)


ActionQueueState = Literal[
    "action_queue_ready",
]
ActionQueueClass = Literal[
    "read_only_action_entry",
    "approval_bound_action_entry",
]

ALL_ACTION_QUEUE_STATES: tuple[ActionQueueState, ...] = (
    "action_queue_ready",
)
ALL_ACTION_QUEUE_CLASSES: tuple[ActionQueueClass, ...] = (
    "read_only_action_entry",
    "approval_bound_action_entry",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ActionQueuePanelContentEntry:
    """Canonical action-queue panel content entry."""

    action_queue_entry_id: str
    operator_intent_id: str
    dashboard_id: str
    workspace_id: str
    action_queue_state: ActionQueueState
    action_queue_class: ActionQueueClass
    intent_kind: Literal["view_request", "navigation_request", "control_request"]
    approval_required: bool
    handoff_ready: bool
    operator_visible: bool
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.action_queue_entry_id, "action_queue_entry_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.action_queue_state not in ALL_ACTION_QUEUE_STATES:
            raise ValueError(
                "action_queue_state must be one of "
                f"{ALL_ACTION_QUEUE_STATES}, got {self.action_queue_state!r}."
            )

        if self.action_queue_class not in ALL_ACTION_QUEUE_CLASSES:
            raise ValueError(
                "action_queue_class must be one of "
                f"{ALL_ACTION_QUEUE_CLASSES}, got {self.action_queue_class!r}."
            )

        if self.intent_kind not in {
            "view_request",
            "navigation_request",
            "control_request",
        }:
            raise ValueError("intent_kind is not supported.")

        if not self.handoff_ready:
            raise ValueError(
                "handoff_ready must remain true for canonical action queue panel entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical action queue panel entries."
            )

        if (
            self.action_queue_class == "approval_bound_action_entry"
            and not self.approval_required
        ):
            raise ValueError(
                "approval_bound_action_entry must have approval_required=True."
            )

        if (
            self.action_queue_class == "read_only_action_entry"
            and self.approval_required
        ):
            raise ValueError(
                "read_only_action_entry must have approval_required=False."
            )


@dataclass(frozen=True, slots=True)
class ActionQueuePanelContentContract:
    """Canonical action-queue panel content contract."""

    contract_id: str
    total_entries: int
    read_only_entries: int
    approval_bound_entries: int
    handoff_ready_entries: int
    operator_visible_entries: int
    entries: tuple[ActionQueuePanelContentEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.read_only_entries != sum(
            1 for entry in self.entries if entry.action_queue_class == "read_only_action_entry"
        ):
            raise ValueError("read_only_entries must match read_only_action_entry count.")

        if self.approval_bound_entries != sum(
            1
            for entry in self.entries
            if entry.action_queue_class == "approval_bound_action_entry"
        ):
            raise ValueError(
                "approval_bound_entries must match approval_bound_action_entry count."
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


def build_action_queue_panel_content_contract() -> ActionQueuePanelContentContract:
    """Build canonical action-queue panel content contract."""
    interaction_surface_contract = build_main_operator_interaction_surface_contract()

    entries = tuple(
        ActionQueuePanelContentEntry(
            action_queue_entry_id=f"action_queue_entry_{index:03d}",
            operator_intent_id=entry.operator_intent_id,
            dashboard_id=entry.dashboard_id,
            workspace_id=entry.workspace_id,
            action_queue_state="action_queue_ready",
            action_queue_class=(
                "approval_bound_action_entry"
                if entry.approval_required
                else "read_only_action_entry"
            ),
            intent_kind=entry.intent_kind,
            approval_required=entry.approval_required,
            handoff_ready=entry.handoff_ready,
            operator_visible=entry.operator_visible,
            trace_id=entry.trace_id,
            description=(
                "Canonical action queue panel content entry for "
                f"{entry.operator_intent_id}."
            ),
        )
        for index, entry in enumerate(interaction_surface_contract.entries, start=1)
    )

    return ActionQueuePanelContentContract(
        contract_id="action_queue_panel_content_contract_001",
        total_entries=len(entries),
        read_only_entries=sum(
            1 for entry in entries if entry.action_queue_class == "read_only_action_entry"
        ),
        approval_bound_entries=sum(
            1
            for entry in entries
            if entry.action_queue_class == "approval_bound_action_entry"
        ),
        handoff_ready_entries=sum(1 for entry in entries if entry.handoff_ready),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
