from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_audit_visibility_contract import (
    build_operator_audit_visibility_contract,
)


AuditTimelinePanelMode = Literal[
    "audit_timeline_read_only",
]

AuditTimelinePanelStatus = Literal[
    "audit_timeline_visible",
]

ALL_AUDIT_TIMELINE_PANEL_MODES: tuple[AuditTimelinePanelMode, ...] = (
    "audit_timeline_read_only",
)

ALL_AUDIT_TIMELINE_PANEL_STATUSES: tuple[AuditTimelinePanelStatus, ...] = (
    "audit_timeline_visible",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorAuditTimelinePanelEntry:
    """Canonical operator audit-timeline panel entry."""

    panel_id: str
    workspace_id: str
    panel_mode: AuditTimelinePanelMode
    panel_status: AuditTimelinePanelStatus
    total_timeline_items: int
    read_only_timeline_items: int
    approval_bound_timeline_items: int
    blocked_timeline_items: int
    failure_timeline_items: int
    operator_visible: bool
    read_only: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator audit-timeline panel entry."""
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.panel_mode not in ALL_AUDIT_TIMELINE_PANEL_MODES:
            raise ValueError(
                f"panel_mode must be one of {ALL_AUDIT_TIMELINE_PANEL_MODES}, got {self.panel_mode!r}."
            )

        if self.panel_status not in ALL_AUDIT_TIMELINE_PANEL_STATUSES:
            raise ValueError(
                "panel_status must be one of "
                f"{ALL_AUDIT_TIMELINE_PANEL_STATUSES}, got {self.panel_status!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical audit-timeline panels."
            )

        if not self.read_only:
            raise ValueError(
                "read_only must remain true for canonical audit-timeline panels."
            )

        if self.total_timeline_items != (
            self.read_only_timeline_items
            + self.approval_bound_timeline_items
            + self.blocked_timeline_items
            + self.failure_timeline_items
        ):
            raise ValueError(
                "total_timeline_items must equal the sum of timeline item class counts."
            )


@dataclass(frozen=True, slots=True)
class OperatorAuditTimelinePanelContract:
    """Canonical operator audit-timeline panel contract."""

    contract_id: str
    total_entries: int
    operator_visible_entries: int
    read_only_entries: int
    entries: tuple[OperatorAuditTimelinePanelEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator audit-timeline panel contract."""
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


def build_operator_audit_timeline_panel_contract() -> OperatorAuditTimelinePanelContract:
    """Build canonical operator audit-timeline panel contract."""
    audit_contract = build_operator_audit_visibility_contract()

    entries = (
        OperatorAuditTimelinePanelEntry(
            panel_id="panel_operator_audit_timeline_001",
            workspace_id="workspace_operator_main",
            panel_mode="audit_timeline_read_only",
            panel_status="audit_timeline_visible",
            total_timeline_items=audit_contract.total_entries,
            read_only_timeline_items=audit_contract.read_only_entries,
            approval_bound_timeline_items=audit_contract.approval_bound_entries,
            blocked_timeline_items=audit_contract.blocked_entries,
            failure_timeline_items=audit_contract.failure_entries,
            operator_visible=True,
            read_only=True,
            description=(
                "Canonical operator audit-timeline panel entry showing visible audit "
                "events across read-only and approval-bound operator flows."
            ),
        ),
    )

    return OperatorAuditTimelinePanelContract(
        contract_id="operator_audit_timeline_panel_contract_001",
        total_entries=len(entries),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
