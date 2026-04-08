from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_audit_visibility_models import (
    ALL_AUDIT_EVENT_CLASSES,
    ALL_AUDIT_VISIBILITY_STATES,
    build_operator_audit_visibility_model,
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorAuditVisibilityContractEntry:
    """Canonical operator audit visibility contract entry."""

    audit_event_id: str
    handoff_id: str
    operator_intent_id: str
    audit_visibility_state: str
    audit_event_class: str
    operator_visible: bool
    requires_audit_trace: bool
    state_registered: bool
    event_class_registered: bool
    structurally_valid: bool
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator audit visibility contract entry."""
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
                "operator_visible must remain true for canonical audit visibility entries."
            )

        if not self.requires_audit_trace:
            raise ValueError(
                "requires_audit_trace must remain true for canonical audit visibility entries."
            )

        if not self.state_registered:
            raise ValueError("state_registered must be true for canonical entries.")

        if not self.event_class_registered:
            raise ValueError(
                "event_class_registered must be true for canonical entries."
            )

        if not self.structurally_valid:
            raise ValueError(
                "structurally_valid must be true for canonical audit visibility entries."
            )


@dataclass(frozen=True, slots=True)
class OperatorAuditVisibilityContract:
    """Canonical operator audit visibility contract."""

    contract_id: str
    total_entries: int
    read_only_entries: int
    approval_bound_entries: int
    blocked_entries: int
    failure_entries: int
    operator_visible_entries: int
    trace_required_entries: int
    structurally_valid_entries: int
    entries: tuple[OperatorAuditVisibilityContractEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator audit visibility contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
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

        if self.structurally_valid_entries != sum(
            1 for entry in self.entries if entry.structurally_valid
        ):
            raise ValueError(
                "structurally_valid_entries must match structurally_valid count."
            )


def build_operator_audit_visibility_contract() -> OperatorAuditVisibilityContract:
    """Build canonical operator audit visibility contract."""
    model = build_operator_audit_visibility_model()

    entries = tuple(
        OperatorAuditVisibilityContractEntry(
            audit_event_id=entry.audit_event_id,
            handoff_id=entry.handoff_id,
            operator_intent_id=entry.operator_intent_id,
            audit_visibility_state=entry.audit_visibility_state,
            audit_event_class=entry.audit_event_class,
            operator_visible=entry.operator_visible,
            requires_audit_trace=entry.requires_audit_trace,
            state_registered=entry.audit_visibility_state in ALL_AUDIT_VISIBILITY_STATES,
            event_class_registered=entry.audit_event_class in ALL_AUDIT_EVENT_CLASSES,
            structurally_valid=(
                bool(entry.audit_event_id.strip())
                and bool(entry.handoff_id.strip())
                and bool(entry.operator_intent_id.strip())
                and bool(entry.trace_id.strip())
                and bool(entry.description.strip())
                and entry.audit_visibility_state in ALL_AUDIT_VISIBILITY_STATES
                and entry.audit_event_class in ALL_AUDIT_EVENT_CLASSES
            ),
            trace_id=entry.trace_id,
            description=entry.description,
        )
        for entry in model.entries
    )

    return OperatorAuditVisibilityContract(
        contract_id="operator_audit_visibility_contract_001",
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
        structurally_valid_entries=sum(
            1 for entry in entries if entry.structurally_valid
        ),
        entries=entries,
    )
