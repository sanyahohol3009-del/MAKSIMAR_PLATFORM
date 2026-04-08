from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_intent_models import (
    build_operator_intent_model,
)


IntentKind = Literal[
    "view_request",
    "navigation_request",
    "control_request",
]

IntentSource = Literal[
    "dashboard_operator_surface",
]

IntentStatus = Literal[
    "intent_only",
]


ALL_INTENT_KINDS: tuple[IntentKind, ...] = (
    "view_request",
    "navigation_request",
    "control_request",
)

ALL_INTENT_SOURCES: tuple[IntentSource, ...] = (
    "dashboard_operator_surface",
)

ALL_INTENT_STATUSES: tuple[IntentStatus, ...] = (
    "intent_only",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorIntentEntry:
    """Canonical operator intent entry."""

    operator_intent_id: str
    dashboard_id: str
    workspace_id: str
    intent_kind: IntentKind
    intent_source: IntentSource
    intent_status: IntentStatus
    approval_required: bool
    direct_execution_allowed: bool
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator intent entry fields."""
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.intent_kind not in ALL_INTENT_KINDS:
            raise ValueError(
                f"intent_kind must be one of {ALL_INTENT_KINDS}, got {self.intent_kind!r}."
            )

        if self.intent_source not in ALL_INTENT_SOURCES:
            raise ValueError(
                "intent_source must be one of "
                f"{ALL_INTENT_SOURCES}, got {self.intent_source!r}."
            )

        if self.intent_status not in ALL_INTENT_STATUSES:
            raise ValueError(
                "intent_status must be one of "
                f"{ALL_INTENT_STATUSES}, got {self.intent_status!r}."
            )

        if self.direct_execution_allowed:
            raise ValueError(
                "direct_execution_allowed must remain false for canonical operator intents."
            )

        if self.intent_kind in {"view_request", "navigation_request"} and self.approval_required:
            raise ValueError(
                "view_request and navigation_request intents must not require approval."
            )

        if self.intent_kind == "control_request" and not self.approval_required:
            raise ValueError(
                "control_request intents must require approval."
            )


@dataclass(frozen=True, slots=True)
class OperatorIntentContract:
    """Canonical operator intent contract."""

    total_entries: int
    view_request_entries: int
    navigation_request_entries: int
    control_request_entries: int
    approval_required_entries: int
    entries: tuple[OperatorIntentEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator intent contract fields."""
        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.view_request_entries != sum(
            1 for entry in self.entries if entry.intent_kind == "view_request"
        ):
            raise ValueError(
                "view_request_entries must match view_request count."
            )

        if self.navigation_request_entries != sum(
            1 for entry in self.entries if entry.intent_kind == "navigation_request"
        ):
            raise ValueError(
                "navigation_request_entries must match navigation_request count."
            )

        if self.control_request_entries != sum(
            1 for entry in self.entries if entry.intent_kind == "control_request"
        ):
            raise ValueError(
                "control_request_entries must match control_request count."
            )

        if self.approval_required_entries != sum(
            1 for entry in self.entries if entry.approval_required
        ):
            raise ValueError(
                "approval_required_entries must match approval_required count."
            )


def build_operator_intent_contract() -> OperatorIntentContract:
    """Build canonical operator intent contract."""
    model = build_operator_intent_model()

    entries = tuple(
        OperatorIntentEntry(
            operator_intent_id=entry.operator_intent_id,
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            intent_kind=entry.intent_kind,
            intent_source="dashboard_operator_surface",
            intent_status="intent_only",
            approval_required=entry.approval_required,
            direct_execution_allowed=False,
            trace_id=entry.trace_id,
            description=entry.description,
        )
        for entry in model.entries
    )

    return OperatorIntentContract(
        total_entries=len(entries),
        view_request_entries=sum(
            1 for entry in entries if entry.intent_kind == "view_request"
        ),
        navigation_request_entries=sum(
            1 for entry in entries if entry.intent_kind == "navigation_request"
        ),
        control_request_entries=sum(
            1 for entry in entries if entry.intent_kind == "control_request"
        ),
        approval_required_entries=sum(
            1 for entry in entries if entry.approval_required
        ),
        entries=entries,
    )
