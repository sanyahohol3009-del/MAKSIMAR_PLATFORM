from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OperatorAuditVisibilityEntry:
    """Canonical operator audit visibility entry."""

    dashboard_id: str
    audit_surface_id: str
    audit_scope: str
    audit_visibility_mode: str
    hidden_audit_allowed: bool
    policy_visibility_required: bool
    approval_visibility_required: bool
    description: str

    def __post_init__(self) -> None:
        """Validate audit-visibility entry invariants."""
        if not self.dashboard_id.strip():
            raise ValueError("dashboard_id must not be empty")

        if not self.audit_surface_id.strip():
            raise ValueError("audit_surface_id must not be empty")

        if not self.audit_scope.strip():
            raise ValueError("audit_scope must not be empty")

        if not self.audit_visibility_mode.strip():
            raise ValueError("audit_visibility_mode must not be empty")

        if self.hidden_audit_allowed is not False:
            raise ValueError("hidden_audit_allowed must be False")

        if self.policy_visibility_required is not True:
            raise ValueError("policy_visibility_required must be True")

        if self.approval_visibility_required is not True:
            raise ValueError("approval_visibility_required must be True")

        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class OperatorAuditVisibilityContract:
    """Canonical operator audit visibility contract."""

    entries: tuple[OperatorAuditVisibilityEntry, ...]

    def __post_init__(self) -> None:
        """Validate audit-visibility contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_dashboard_ids: set[str] = set()
        for entry in self.entries:
            if entry.dashboard_id in seen_dashboard_ids:
                raise ValueError(
                    f"duplicate dashboard_id detected: {entry.dashboard_id}"
                )
            seen_dashboard_ids.add(entry.dashboard_id)
