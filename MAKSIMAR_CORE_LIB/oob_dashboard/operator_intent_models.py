from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


OperatorIntentId = str
TraceId = str

IntentKind = Literal[
    "view_request",
    "navigation_request",
    "control_request",
    "approval_request",
    "system_action_request",
]

IntentState = Literal[
    "intent_created",
    "intent_validated",
    "intent_blocked",
    "intent_pending_approval",
    "intent_approved",
    "intent_rejected",
    "intent_handoff_ready",
    "intent_handed_off",
]

RequestedActionKind = Literal[
    "view_panel",
    "navigate_workspace",
    "request_control_surface",
    "request_approval_flow",
    "request_system_action",
]

ALL_INTENT_KINDS: tuple[IntentKind, ...] = (
    "view_request",
    "navigation_request",
    "control_request",
    "approval_request",
    "system_action_request",
)

ALL_INTENT_STATES: tuple[IntentState, ...] = (
    "intent_created",
    "intent_validated",
    "intent_blocked",
    "intent_pending_approval",
    "intent_approved",
    "intent_rejected",
    "intent_handoff_ready",
    "intent_handed_off",
)

ALL_REQUESTED_ACTION_KINDS: tuple[RequestedActionKind, ...] = (
    "view_panel",
    "navigate_workspace",
    "request_control_surface",
    "request_approval_flow",
    "request_system_action",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorIntentEntry:
    """Canonical operator intent entry.

    This model represents a dashboard-originated operator request before any
    direct execution occurs. The entry is intentionally action-adjacent but
    non-executing: it captures intent semantics, approval requirements, and
    trace visibility without bypassing policy or control-plane boundaries.
    """

    operator_intent_id: OperatorIntentId
    panel_id: str
    workspace_id: str
    display_target_id: str
    intent_kind: IntentKind
    requested_action: RequestedActionKind
    intent_state: IntentState
    requested_by: str
    requested_at: str
    approval_required: bool
    trace_id: TraceId
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator intent entry fields."""
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.requested_by, "requested_by")
        _require_non_empty(self.requested_at, "requested_at")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.intent_kind not in ALL_INTENT_KINDS:
            raise ValueError(
                f"intent_kind must be one of {ALL_INTENT_KINDS}, got {self.intent_kind!r}."
            )

        if self.intent_state not in ALL_INTENT_STATES:
            raise ValueError(
                f"intent_state must be one of {ALL_INTENT_STATES}, got {self.intent_state!r}."
            )

        if self.requested_action not in ALL_REQUESTED_ACTION_KINDS:
            raise ValueError(
                "requested_action must be one of "
                f"{ALL_REQUESTED_ACTION_KINDS}, got {self.requested_action!r}."
            )


@dataclass(frozen=True, slots=True)
class OperatorIntentModel:
    """Canonical operator intent model.

    This model groups dashboard-originated operator intents into a normalized
    read-safe structure that can be consumed by later vocabulary, approval,
    handoff, and audit layers.
    """

    model_id: str
    total_entries: int
    approval_required_entries: int
    unique_panels: int
    entries: tuple[OperatorIntentEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator intent model fields."""
        _require_non_empty(self.model_id, "model_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the model."
            )

        if self.approval_required_entries != sum(
            1 for entry in self.entries if entry.approval_required
        ):
            raise ValueError(
                "approval_required_entries must match approval-required entry count."
            )

        if self.unique_panels != len({entry.panel_id for entry in self.entries}):
            raise ValueError(
                "unique_panels must match the number of distinct panel_id values."
            )


def build_operator_intent_model() -> OperatorIntentModel:
    """Build canonical operator intent model.

    The baseline model intentionally includes representative operator-surface
    intents only. It does not execute actions and does not bypass policy.
    """

    entries = (
        OperatorIntentEntry(
            operator_intent_id="operator_intent_001",
            panel_id="panel_chat",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            intent_kind="view_request",
            requested_action="view_panel",
            intent_state="intent_created",
            requested_by="operator_primary",
            requested_at="runtime_unbound",
            approval_required=False,
            trace_id="trace_operator_intent_001",
            description=(
                "Canonical operator view intent originating from the chat panel "
                "within the main operator workspace."
            ),
        ),
        OperatorIntentEntry(
            operator_intent_id="operator_intent_002",
            panel_id="panel_settings",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            intent_kind="navigation_request",
            requested_action="navigate_workspace",
            intent_state="intent_validated",
            requested_by="operator_primary",
            requested_at="runtime_unbound",
            approval_required=False,
            trace_id="trace_operator_intent_002",
            description=(
                "Canonical operator navigation intent originating from the settings "
                "panel within the main operator workspace."
            ),
        ),
        OperatorIntentEntry(
            operator_intent_id="operator_intent_003",
            panel_id="panel_gesture_control",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            intent_kind="control_request",
            requested_action="request_control_surface",
            intent_state="intent_pending_approval",
            requested_by="operator_primary",
            requested_at="runtime_unbound",
            approval_required=True,
            trace_id="trace_operator_intent_003",
            description=(
                "Canonical operator control intent originating from the gesture "
                "control panel and remaining approval-bound before any handoff."
            ),
        ),
    )

    return OperatorIntentModel(
        model_id="operator_intent_model_001",
        total_entries=len(entries),
        approval_required_entries=sum(1 for entry in entries if entry.approval_required),
        unique_panels=len({entry.panel_id for entry in entries}),
        entries=entries,
    )
