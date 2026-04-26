from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_audit_visibility_contract import (
    build_operator_audit_visibility_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_interaction_read_model_contract import (
    build_operator_interaction_read_model_contract,
)


AuditTimelineState = Literal[
    "audit_timeline_ready",
]
AuditTimelineClass = Literal[
    "operator_action_audit_entry",
]

ALL_AUDIT_TIMELINE_STATES: tuple[AuditTimelineState, ...] = (
    "audit_timeline_ready",
)
ALL_AUDIT_TIMELINE_CLASSES: tuple[AuditTimelineClass, ...] = (
    "operator_action_audit_entry",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class AuditTimelinePanelContentEntry:
    """Canonical audit-timeline panel content entry."""

    audit_timeline_entry_id: str
    operator_intent_id: str
    dashboard_id: str
    workspace_id: str
    audit_timeline_state: AuditTimelineState
    audit_timeline_class: AuditTimelineClass
    intent_kind: Literal["view_request", "navigation_request", "control_request"]
    audit_visible: bool
    approval_required: bool
    operator_visible: bool
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.audit_timeline_entry_id, "audit_timeline_entry_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.audit_timeline_state not in ALL_AUDIT_TIMELINE_STATES:
            raise ValueError(
                "audit_timeline_state must be one of "
                f"{ALL_AUDIT_TIMELINE_STATES}, got {self.audit_timeline_state!r}."
            )

        if self.audit_timeline_class not in ALL_AUDIT_TIMELINE_CLASSES:
            raise ValueError(
                "audit_timeline_class must be one of "
                f"{ALL_AUDIT_TIMELINE_CLASSES}, got {self.audit_timeline_class!r}."
            )

        if self.intent_kind not in {
            "view_request",
            "navigation_request",
            "control_request",
        }:
            raise ValueError("intent_kind is not supported.")

        if not self.audit_visible:
            raise ValueError(
                "audit_visible must remain true for canonical audit timeline entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical audit timeline entries."
            )


@dataclass(frozen=True, slots=True)
class AuditTimelinePanelContentContract:
    """Canonical audit-timeline panel content contract."""

    contract_id: str
    total_entries: int
    audit_visible_entries: int
    approval_required_entries: int
    operator_visible_entries: int
    entries: tuple[AuditTimelinePanelContentEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.audit_visible_entries != sum(
            1 for entry in self.entries if entry.audit_visible
        ):
            raise ValueError("audit_visible_entries must match audit_visible count.")

        if self.approval_required_entries != sum(
            1 for entry in self.entries if entry.approval_required
        ):
            raise ValueError(
                "approval_required_entries must match approval_required count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_audit_timeline_panel_content_contract() -> AuditTimelinePanelContentContract:
    """Build canonical audit-timeline panel content contract."""
    read_model_contract = build_operator_interaction_read_model_contract()
    audit_contract = build_operator_audit_visibility_contract()

    audit_by_dashboard = {
        entry.dashboard_id: entry for entry in audit_contract.entries
    }

    entries = tuple(
        AuditTimelinePanelContentEntry(
            audit_timeline_entry_id=f"audit_timeline_entry_{index:03d}",
            operator_intent_id=entry.operator_intent_id,
            dashboard_id=entry.dashboard_id,
            workspace_id=entry.workspace_id,
            audit_timeline_state="audit_timeline_ready",
            audit_timeline_class="operator_action_audit_entry",
            intent_kind=entry.intent_kind,
            audit_visible=(
                audit_by_dashboard[entry.dashboard_id].policy_visibility_required
                and audit_by_dashboard[entry.dashboard_id].approval_visibility_required
            ),
            approval_required=entry.approval_required,
            operator_visible=entry.operator_visible,
            trace_id=entry.trace_id,
            description=(
                "Canonical audit timeline panel content entry for "
                f"{entry.operator_intent_id}."
            ),
        )
        for index, entry in enumerate(read_model_contract.entries, start=1)
    )

    return AuditTimelinePanelContentContract(
        contract_id="audit_timeline_panel_content_contract_001",
        total_entries=len(entries),
        audit_visible_entries=sum(1 for entry in entries if entry.audit_visible),
        approval_required_entries=sum(
            1 for entry in entries if entry.approval_required
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
