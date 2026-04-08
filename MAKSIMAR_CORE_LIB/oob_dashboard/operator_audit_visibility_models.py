from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_control_plane_handoff_models import (
    build_operator_control_plane_handoff_model,
)


AuditVisibilityState = Literal[
    "audit_visible_read_only",
    "audit_visible_approval_bound",
    "audit_visible_blocked",
    "audit_visible_failure",
]

AuditEventClass = Literal[
    "read_only_navigation",
    "approval_bound_control",
    "blocked_control",
    "failed_control",
]

ALL_AUDIT_VISIBILITY_STATES: tuple[AuditVisibilityState, ...] = (
    "audit_visible_read_only",
    "audit_visible_approval_bound",
    "audit_visible_blocked",
    "audit_visible_failure",
)

ALL_AUDIT_EVENT_CLASSES: tuple[AuditEventClass, ...] = (
    "read_only_navigation",
    "approval_bound_control",
    "blocked_control",
    "failed_control",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorAuditVisibilityEntry:
    """Canonical operator audit visibility entry."""

    audit_event_id: str
    handoff_id: str
    operator_intent_id: str
    audit_visibility_state: AuditVisibilityState
    audit_event_class: AuditEventClass
    operator_visible: bool
    requires_audit_trace: bool
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator audit visibility entry."""
        _require_non_empty(self.audit_event_id, "audit_event_id")
        _require_non_empty(self.handoff_id, "handoff_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.audit_visibility_state not in ALL_AUDIT_VISIBILITY_STATES:
            raise ValueError(
                "audit_visibility_state must be one of "
                f"{ALL_AUDIT_VISIBILITY_STATES}, got {self.audit_visibility_state!r}."
            )

        if self.audit_event_class not in ALL_AUDIT_EVENT_CLASSES:
            raise ValueError(
                "audit_event_class must be one of "
                f"{ALL_AUDIT_EVENT_CLASSES}, got {self.audit_event_class!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical operator audit visibility entries."
            )

        if not self.requires_audit_trace:
            raise ValueError(
                "requires_audit_trace must remain true for canonical operator audit visibility entries."
            )

        state_to_class_map = {
            "audit_visible_read_only": "read_only_navigation",
            "audit_visible_approval_bound": "approval_bound_control",
            "audit_visible_blocked": "blocked_control",
            "audit_visible_failure": "failed_control",
        }

        if state_to_class_map[self.audit_visibility_state] != self.audit_event_class:
            raise ValueError(
                "audit_visibility_state and audit_event_class must remain semantically aligned."
            )


@dataclass(frozen=True, slots=True)
class OperatorAuditVisibilityModel:
    """Canonical operator audit visibility model."""

    model_id: str
    total_entries: int
    read_only_entries: int
    approval_bound_entries: int
    blocked_entries: int
    failure_entries: int
    operator_visible_entries: int
    trace_required_entries: int
    entries: tuple[OperatorAuditVisibilityEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator audit visibility model."""
        _require_non_empty(self.model_id, "model_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the model."
            )

        if self.read_only_entries != sum(
            1
            for entry in self.entries
            if entry.audit_visibility_state == "audit_visible_read_only"
        ):
            raise ValueError("read_only_entries must match read-only audit count.")

        if self.approval_bound_entries != sum(
            1
            for entry in self.entries
            if entry.audit_visibility_state == "audit_visible_approval_bound"
        ):
            raise ValueError(
                "approval_bound_entries must match approval-bound audit count."
            )

        if self.blocked_entries != sum(
            1
            for entry in self.entries
            if entry.audit_visibility_state == "audit_visible_blocked"
        ):
            raise ValueError("blocked_entries must match blocked audit count.")

        if self.failure_entries != sum(
            1
            for entry in self.entries
            if entry.audit_visibility_state == "audit_visible_failure"
        ):
            raise ValueError("failure_entries must match failure audit count.")

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )

        if self.trace_required_entries != sum(
            1 for entry in self.entries if entry.requires_audit_trace
        ):
            raise ValueError(
                "trace_required_entries must match requires_audit_trace count."
            )


def build_operator_audit_visibility_model() -> OperatorAuditVisibilityModel:
    """Build canonical operator audit visibility model."""
    handoff_model = build_operator_control_plane_handoff_model()

    state_map = {
        "handoff_not_ready": "audit_visible_read_only",
        "handoff_ready": "audit_visible_approval_bound",
        "handoff_blocked": "audit_visible_blocked",
        "handoff_failed": "audit_visible_failure",
    }

    event_class_map = {
        "handoff_not_ready": "read_only_navigation",
        "handoff_ready": "approval_bound_control",
        "handoff_blocked": "blocked_control",
        "handoff_failed": "failed_control",
    }

    entries = tuple(
        OperatorAuditVisibilityEntry(
            audit_event_id=f"audit_visibility_{index:03d}",
            handoff_id=entry.handoff_id,
            operator_intent_id=entry.operator_intent_id,
            audit_visibility_state=state_map[entry.handoff_state],
            audit_event_class=event_class_map[entry.handoff_state],
            operator_visible=True,
            requires_audit_trace=True,
            trace_id=entry.trace_id,
            description=(
                f"Canonical operator audit visibility entry for {entry.operator_intent_id}."
            ),
        )
        for index, entry in enumerate(
            (
                model_entry
                for model_entry in handoff_model.entries
                if model_entry.handoff_state in state_map
            ),
            start=1,
        )
    )

    return OperatorAuditVisibilityModel(
        model_id="operator_audit_visibility_model_001",
        total_entries=len(entries),
        read_only_entries=sum(
            1
            for entry in entries
            if entry.audit_visibility_state == "audit_visible_read_only"
        ),
        approval_bound_entries=sum(
            1
            for entry in entries
            if entry.audit_visibility_state == "audit_visible_approval_bound"
        ),
        blocked_entries=sum(
            1
            for entry in entries
            if entry.audit_visibility_state == "audit_visible_blocked"
        ),
        failure_entries=sum(
            1
            for entry in entries
            if entry.audit_visibility_state == "audit_visible_failure"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        trace_required_entries=sum(
            1 for entry in entries if entry.requires_audit_trace
        ),
        entries=entries,
    )
